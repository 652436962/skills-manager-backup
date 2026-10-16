#!/usr/bin/env python3
"""
静态站点文章正文 HTML → Markdown 精确转换器（适配 Hugo PaperMod / VitePress 等）。

相比通用正则转换脚本，本脚本基于 html.parser 做结构化解析，能够完整保留：
  - <table> 表格（通用脚本会整段丢失）
  - 相对路径图片 / 链接（自动补全站点域名）
  - 标题（自动剔除 <a hidden class=anchor> 造成的尾部 "#"）
  - <pre><code class=language-xxx> 的语言标记
  - 有序 / 无序列表（含嵌套缩进）
  - 行内 code / strong / em

用法:
  python3 convert_papermod.py --html-file ./raw.html --url <文章URL> \
      [--title "标题"] [--base https://example.com] [--out out.md]

不传 --out 时由标题自动生成文件名。
"""

import argparse
import html
import re
from html.parser import HTMLParser
from pathlib import Path

BODY_START_PATTERNS = [
    # 微信公众号
    r'<div[^>]*id="js_content"[^>]*>',
    # 静态博客 / 文档站
    r'<div[^>]*class="?post-content"?[^>]*>',
    r'<div[^>]*class="?[^"]*article-content[^"]*"?[^>]*>',
    r'<article[^>]*>',
]
BODY_END_PATTERNS = [
    r'<div[^>]*class="rich_media_tool',      # 微信：正文结束
    r'<footer[^>]*class="?post-footer"?[^>]*>',
    r'</article>',
]

# 需要整体丢弃内容的标签
DROP_TAGS = {"script", "style", "noscript", "svg", "canvas", "iframe", "button", "video", "audio"}


def _match_div_end(html_text: str) -> int:
    """从位置 0 处的 <div ...> 开始，按嵌套配对找到对应的 </div> 结束位置。"""
    depth = 0
    for m in re.finditer(r"<(/?)div\b[^>]*>", html_text, re.I):
        if m.group(1):
            depth -= 1
            if depth == 0:
                return m.start()
        else:
            depth += 1
    return len(html_text)


def extract_body(raw: str) -> str:
    start = -1
    for pat in BODY_START_PATTERNS:
        m = re.search(pat, raw)
        if m:
            start = m.start() if "js_content" in pat else m.end()
            break
    if start == -1:
        return raw

    if raw.startswith("<div", start):
        # 微信这类场景：用 div 嵌套配对，避免把点赞/分享 UI 也收进来
        chunk = raw[start:]
        return chunk[: _match_div_end(chunk)]

    end = len(raw)
    for pat in BODY_END_PATTERNS:
        m = re.search(pat, raw[start:])
        if m:
            end = start + m.start()
            break
    return raw[start:end]


class MarkdownConverter(HTMLParser):
    def __init__(self, base: str = ""):
        super().__init__(convert_charrefs=True)
        self.base = base.rstrip("/")
        self.out = []
        self.pre_depth = 0
        self.pre_buf = []
        self.pre_lang = ""
        self.inline_code = False
        self.inline_buf = []
        self.in_table = False
        self.table = None
        self.row = None
        self.cell = None
        self.header_phase = False
        self.list_depth = 0
        self.skip_anchor = False
        self.anchor_depth = 0
        self.anchor_href = ""
        self.link_text = []
        self.drop_depth = 0
        self.bq_stack = []

    # ---- output routing ----
    def emit(self, s):
        self.out.append(s)

    def emit_inline(self, s):
        """行内标记：在表格单元格内写进单元格，否则写进主输出。"""
        if self.cell is not None:
            self.cell.append(s)
        else:
            self.out.append(s)

    def absolutize(self, href: str) -> str:
        if not href:
            return href
        if href.startswith(("http://", "https://", "mailto:", "#", "data:")):
            return href
        if href.startswith("/") and self.base:
            return self.base + href
        return href

    # ---- tags ----
    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        cls = a.get("class", "")

        if tag in DROP_TAGS:
            self.drop_depth += 1
            return
        if self.drop_depth:
            return

        if tag == "a" and "anchor" in cls.split():
            self.skip_anchor = True  # 标题锚点 <a hidden class=anchor>#</a>
            return
        if self.skip_anchor:
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.emit("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "p":
            # 列表项内部（<li><p>…</p></li>，微信常见）不再插入空行
            if self.list_depth == 0:
                self.emit("\n\n")
        elif tag in ("strong", "b"):
            self.emit_inline("**")
        elif tag in ("em", "i"):
            self.emit_inline("*")
        elif tag == "del" or tag == "s":
            self.emit_inline("~~")
        elif tag == "br":
            if self.pre_depth:
                self.pre_buf.append("\n")
            else:
                self.emit("  \n")
        elif tag == "hr":
            self.emit("\n\n---\n\n")
        elif tag == "pre":
            if self.pre_depth == 0:
                self.pre_buf = []
                self.pre_lang = ""
                # 微信公众号用 <pre lang="bash">，静态站用 <code class=language-bash>
                self.pre_lang = a.get("lang", "") or ""
                if self.pre_lang == "text":
                    self.pre_lang = ""   # 微信的“text”并非真实语言
            self.pre_depth += 1
        elif tag == "code":
            if self.pre_depth:
                if not self.pre_lang:
                    m = re.search(r"language-([\w+#-]+)", cls)
                    self.pre_lang = a.get("data-lang") or (m.group(1) if m else "")
            else:
                self.inline_buf = []
                self.inline_code = True
        elif tag == "table":
            self.in_table = True
            self.table = []
            self.header_phase = True
        elif tag == "thead":
            self.header_phase = True
        elif tag == "tbody":
            self.header_phase = False
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.cell = []
        elif tag in ("ul", "ol"):
            self.list_depth += 1
            self.emit("\n")
        elif tag == "li":
            indent = "  " * max(0, self.list_depth - 1)
            self.emit(f"\n{indent}- ")
        elif tag == "blockquote":
            self.bq_stack.append(self.out)
            self.out = []
        elif tag == "img":
            # 微信公众号用 data-src 懒加载，静态站用 src
            src = a.get("data-src") or a.get("src") or ""
            if src.startswith("//"):
                src = "https:" + src
            src = self.absolutize(src)
            alt = a.get("alt", "")
            if src and not src.startswith("data:"):
                self.emit(f"\n\n![{alt}]({src})\n\n")
        elif tag == "a":
            self.anchor_depth += 1
            self.anchor_href = a.get("href", "")
            self.link_text = []

    def handle_endtag(self, tag):
        if tag in DROP_TAGS:
            if self.drop_depth:
                self.drop_depth -= 1
            return
        if self.drop_depth:
            return

        if tag == "a" and self.skip_anchor:
            self.skip_anchor = False
            return
        if self.skip_anchor:
            return

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.emit("\n")
        elif tag in ("strong", "b"):
            self.emit_inline("**")
        elif tag in ("em", "i"):
            self.emit_inline("*")
        elif tag in ("del", "s"):
            self.emit_inline("~~")
        elif tag == "p":
            if self.list_depth == 0:
                self.emit("\n")
        elif tag == "pre":
            self.pre_depth -= 1
            if self.pre_depth == 0:
                code = "".join(self.pre_buf).rstrip("\n")
                self.emit(f"\n\n```{self.pre_lang}\n{code}\n```\n\n")
        elif tag == "code":
            if self.pre_depth:
                pass
            elif self.inline_code:
                txt = "".join(self.inline_buf)
                if txt.strip():
                    self.emit("`" + txt + "`")
                self.inline_code = False
        elif tag == "table":
            self.in_table = False
            if self.table:
                self.emit("\n\n" + self.render_table(self.table) + "\n\n")
            self.table = None
        elif tag == "thead":
            self.header_phase = False
        elif tag == "tr":
            if self.in_table and self.row is not None:
                self.table.append((self.header_phase, self.row))
                self.row = None
        elif tag in ("td", "th"):
            if self.cell is not None and self.row is not None:
                self.row.append("".join(self.cell).strip())
            self.cell = None
        elif tag in ("ul", "ol"):
            self.list_depth = max(0, self.list_depth - 1)
        elif tag == "blockquote":
            inner = "".join(self.out)
            self.out = self.bq_stack.pop() if self.bq_stack else []
            inner = re.sub(r"\n{2,}", "\n", inner).strip()
            if inner:
                prefixed = "\n".join(
                    ("> " + ln) if ln.strip() else ">" for ln in inner.split("\n")
                )
                self.emit("\n\n" + prefixed + "\n\n")
        elif tag == "a":
            self.anchor_depth = max(0, self.anchor_depth - 1)
            if self.anchor_depth == 0 and not self.skip_anchor:
                text = "".join(self.link_text).strip()
                href = self.absolutize(self.anchor_href)
                if text:
                    self.emit_inline(f"[{text}]({href})")
                elif href:
                    self.emit_inline(href)
                self.anchor_href = ""
                self.link_text = []

    def handle_data(self, data):
        if self.drop_depth or self.skip_anchor:
            return
        if self.pre_depth:
            self.pre_buf.append(data)
            return
        if self.cell is not None:
            self.cell.append(data)
            return
        if self.inline_code:
            self.inline_buf.append(data)
            return
        if self.anchor_depth:
            self.link_text.append(data)
            return
        self.emit(data)

    @staticmethod
    def render_table(rows):
        header, body = None, []
        for is_header, cells in rows:
            if header is None and is_header:
                header = cells
            else:
                body.append(cells)
        if header is None:
            header = body.pop(0) if body else []
        ncol = len(header) or (len(body[0]) if body else 0)
        lines = ["| " + " | ".join(header) + " |",
                 "| " + " | ".join(["---"] * ncol) + " |"]
        for r in body:
            r = r + [""] * (ncol - len(r))
            lines.append("| " + " | ".join(r[:ncol]) + " |")
        return "\n".join(lines)


def convert(raw: str, url: str, title: str, base: str) -> str:
    body = extract_body(raw)
    p = MarkdownConverter(base)
    p.feed(body)
    text = "".join(p.out)
    text = text.replace("\u00a0", " ")          # 微信大量使用 &nbsp;
    text = text.replace("\u200b", "")           # 零宽空格
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"^[ \t]+```", "```", text, flags=re.M)   # 只吃行首空格，勿吞掉空行
    text = re.sub(r"^([ \t]*-) +", r"\1 ", text, flags=re.M)  # 列表项后多余空格
    text = text.strip()
    header = f"# {title}\n\n> 原文链接：[{url}]({url})\n\n"
    footer = f"\n\n---\n\n*原文链接：[{url}]({url})*\n"
    return header + text + footer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html-file", required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--base", default="")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    raw = Path(args.html_file).read_text(encoding="utf-8", errors="replace")
    title = args.title
    if not title:
        for pat in (
            r'<meta[^>]*property="og:title"[^>]*content="([^"]*)"',
            r'<h1[^>]*id="activity-name"[^>]*>(.*?)</h1>',   # 微信公众号
            r"var msg_title\s*=\s*'([^']*)'",
            r"<title>(.*?)</title>",
        ):
            m = re.search(pat, raw, re.S)
            if m:
                cand = re.sub(r"<[^>]+>", "", m.group(1))
                cand = html.unescape(cand).strip()
                if cand:
                    title = cand
                    break
    title = title or "Untitled"

    base = args.base
    if not base:
        m = re.match(r"(https?://[^/]+)", args.url)
        base = m.group(1) if m else ""

    doc = convert(raw, args.url, title, base)
    out = args.out
    if not out:
        slug = re.sub(r"[^\w\-]+", "-", title.lower()).strip("-")[:60]
        out = f"{slug}.md"
    Path(out).write_text(doc, encoding="utf-8")
    in_fence = False
    n_img = n_row = n_code = n_head = 0
    for ln in doc.splitlines():
        if ln.startswith("```"):
            n_code += 1
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if ln.strip().startswith("!["):
            n_img += 1
        if ln.startswith("| "):
            n_row += 1
        if re.match(r"^#{1,6} ", ln):
            n_head += 1
    print(f"标题: {title}")
    print(f"图片: {n_img}  表格行: {n_row}  代码围栏: {n_code}  标题: {n_head}")
    print(f"✅ 已生成: {out}")


if __name__ == "__main__":
    main()
