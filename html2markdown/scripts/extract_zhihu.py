#!/usr/bin/env python3
"""从知乎 SPA 原始 HTML 中抽出正文容器，包成 <div id="js_content"> 以复用 convert_papermod.py。

同时清理知乎正文里的两类噪音链接：
  1. zhida.zhihu.com/search?...  平台关键词跳转链接 -> 只保留文字
  2. link.zhihu.com / link.juejin.cn 的 ?target= 多重跳转 -> 解出真实 URL
"""
import html as htmlmod
import re
import sys
from pathlib import Path
from urllib.parse import unquote


def match_div_end(text, start):
    depth = 0
    for m in re.finditer(r"<(/?)div\b[^>]*>", text[start:], re.I):
        if m.group(1):
            depth -= 1
            if depth == 0:
                return start + m.start()
        else:
            depth += 1
    return len(text)


def resolve_target(url):
    """反复解包 link.zhihu.com / link.juejin.cn 之类的跳转参数。"""
    for _ in range(5):
        m = re.search(r"[?&]target=([^&]+)", url)
        if not m:
            break
        nxt = unquote(m.group(1))
        if nxt == url:
            break
        url = nxt
    return url


A_RE = re.compile(r"<a\b([^>]*)>(.*?)</a>", re.S | re.I)
HREF_RE = re.compile(r'href="([^"]*)"', re.I)


def clean_links(text):
    def repl(m):
        attrs, inner = m.group(1), m.group(2)
        hm = HREF_RE.search(attrs)
        if not hm:
            return inner
        href = htmlmod.unescape(hm.group(1))
        if "zhida.zhihu.com" in href:
            # 关键词搜索跳转，无信息量，只留文字
            return inner
        real = resolve_target(href)
        if real != href:
            attrs = HREF_RE.sub('href="%s"' % htmlmod.escape(real, quote=True), attrs, count=1)
        return "<a%s>%s</a>" % (attrs, inner)

    return A_RE.sub(repl, text)


src = Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore")

m = re.search(r'<div[^>]*class="[^"]*Post-RichText[^"]*"[^>]*>', src)
if not m:
    m = re.search(r'<div[^>]*class="[^"]*RichText ztext[^"]*"[^>]*>', src)
if not m:
    sys.exit("未找到正文容器")

start = m.start()
end = match_div_end(src, start)
body = clean_links(src[start:end])

# 标题
tm = re.search(r'<h1[^>]*class="Post-Title"[^>]*>(.*?)</h1>', src, re.S)
title = re.sub(r"<[^>]+>", "", tm.group(1)).strip() if tm else ""

out = (
    "<html><head><meta charset='utf-8'><title>%s</title></head><body>"
    '<div id="js_content">%s</div></body></html>' % (title, body)
)
Path(sys.argv[2]).write_text(out, encoding="utf-8")
print("title:", title)
print("body_len:", len(body), "imgs:", len(re.findall(r"<img", body)))
print("剩余 zhida 链接:", body.count("zhida.zhihu.com"))
