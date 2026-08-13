#!/usr/bin/env python3
"""
网页文章转 Markdown 转换脚本。
用法: python3 convert.py --html-file <html文件> <文章URL> [输出文件名.md]
"""

import re
import sys
import urllib.request
import html
from pathlib import Path


def fetch_html(url: str) -> str:
    """下载网页的 HTML 源码（绕过代理环境）。"""
    import os
    import subprocess

    # 方式1: 用 wget 绕过代理下载
    try:
        env = os.environ.copy()
        for var in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY",
                     "all_proxy", "ALL_PROXY"]:
            env.pop(var, None)
        result = subprocess.run(
            ["wget", "-q", "-O", "-",
             "--header=User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
             url],
            capture_output=True, text=True, timeout=30, env=env
        )
        if result.returncode == 0 and len(result.stdout) > 1000:
            return result.stdout
    except Exception:
        pass

    # 方式2: 用 Python urllib 直接请求
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def strip_tags(text: str) -> str:
    """去除 HTML 标签，保留纯文本。"""
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_title(html_content: str) -> str:
    """提取文章标题（支持多种网站）。"""
    # 尝试从 og:title meta 标签提取
    m = re.search(r'<meta[^>]*property="og:title"[^>]*content="([^"]*)"', html_content)
    if m:
        title = m.group(1).strip()
        if title:
            return title
    # 尝试从 <title> 中提取
    m = re.search(r"<title>(.*?)</title>", html_content, re.DOTALL)
    if m:
        title = strip_tags(m.group(1))
        # 移除常见站点后缀
        for suffix in ["博客园", "blog", "segmentfault", "企业博客"]:
            title = re.sub(rf"\s*[-–—|]\s*{suffix}\s*$", "", title).strip()
            title = re.sub(rf"\s*[-–—|]\s*.*?{suffix}\s*$", "", title).strip()
        if title:
            return title
    # 尝试从 h1 提取
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html_content, re.DOTALL)
    if m:
        title = strip_tags(m.group(1))
        if len(title) > 3:
            return title
    return "Untitled"


def extract_post_body(html_content: str) -> str:
    """提取文章正文部分的 HTML（支持多种网站）。"""
    # 博客园
    for pat in [
        r'id="cnblogs_post_body"(.*?)<div class="clear"></div>',
        r'class="postBody".*?>(.*?)<div class="clear"></div>',
    ]:
        m = re.search(pat, html_content, re.DOTALL)
        if m:
            return m.group(1)
    # 火山引擎 / SPA 站点：尝试从 JSON-LD 或 script 标签提取
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html_content, re.DOTALL)
    if m:
        import json
        try:
            data = json.loads(m.group(1))
            if "articleBody" in data:
                return data["articleBody"]
        except Exception:
            pass
    # 通用：尝试找 <article> 标签
    m = re.search(r"<article[^>]*>(.*?)</article>", html_content, re.DOTALL)
    if m:
        body = m.group(1)
        if len(body) > 500:
            return body
    # 通用：尝试 .post-content / .article-content / .markdown-body
    for cls in ["post-content", "article-content", "article-body", "markdown-body", "entry-content"]:
        m = re.search(rf'class="[^"]*\b{cls}\b[^"]*"[^>]*>(.*?)(?=<div class="(?:footer|comment|related|sidebar|recommend))', html_content, re.DOTALL)
        if m and len(m.group(1)) > 500:
            return m.group(1)
    return ""


def extract_images(body_html: str) -> list:
    """
    从正文 HTML 中提取所有图片，返回 [(image_url, preceding_text), ...]
    preceding_text 是图片之前的最近一段文字，用于确定图片在文章中的位置。
    """
    # 找到所有 img 标签
    img_tags = list(re.finditer(r"<img[^>]*?>", body_html, re.IGNORECASE))
    results = []

    for tag_match in img_tags:
        tag = tag_match.group(0)
        # 优先取 data-src（懒加载原图），否则取 src
        data_src = re.search(r'data-src="([^"]*)"', tag)
        src = re.search(r'\ssrc="([^"]*)"', tag)
        url = data_src.group(1) if data_src else (src.group(1) if src else None)

        if url and url.startswith("http"):
            # 解码 HTML 实体（&#x26; -> & 等），保留完整 URL 含查询参数
            url = html.unescape(url)

            # 获取图片前 500 字符的文本，用于定位上下文
            start = max(0, tag_match.start() - 500)
            context = body_html[start : tag_match.start()]
            preceding_text = strip_tags(context)[-200:]

            results.append((url, preceding_text))

    # 去重（保留首次出现的顺序）
    seen = set()
    unique = []
    for url, context in results:
        if url not in seen:
            seen.add(url)
            unique.append((url, context))

    return unique


def classify_image(context_text: str) -> tuple:
    """
    根据上下文文本判断图片类型，返回 (category, label)。
    用于帮助确定图片在 Markdown 中的插入位置。
    """
    ctx_lower = context_text.lower()

    # 实战示例区域
    if "cursor界面" in ctx_lower or "cursor 界面" in ctx_lower:
        return ("example_cursor", "Cursor 界面")
    if "blender界面" in ctx_lower or "blender 界面" in ctx_lower:
        return ("example_blender", "Blender 界面")

    # 章节标题检测
    if "验证安装" in context_text or "--version" in context_text:
        return ("verify", "验证安装")
    if "github" in ctx_lower and ("仓库" in context_text or "repository" in ctx_lower):
        return ("github", "GitHub仓库")
    if "文件夹" in context_text or "文件结构" in context_text or "解压" in context_text:
        return ("folder", "文件结构")
    if "偏好设置" in context_text or "preferences" in ctx_lower:
        return ("prefs", "偏好设置")
    if "插件" in context_text and "选项卡" in context_text:
        return ("addons_tab", "插件选项卡")
    if "安装" in context_text and "addon" in ctx_lower:
        return ("install_btn", "安装插件")
    if "启用插件" in context_text or ("勾选" in context_text and "mcp" in ctx_lower):
        return ("enable", "启用插件")
    if "侧边栏" in context_text or "blendermcp" in ctx_lower:
        return ("sidebar", "BlenderMCP侧边栏")
    if "配置" in context_text and ("面板" in context_text or "端口" in context_text):
        return ("config", "配置面板")
    if "设置" in context_text and "cursor" in ctx_lower:
        return ("cursor_settings", "Cursor设置")
    if "mcp" in ctx_lower and ("配置" in context_text or "菜单" in context_text):
        return ("mcp_menu", "MCP配置")
    if "全局" in context_text and "mcp" in ctx_lower:
        return ("global_mcp", "全局MCP")
    if "json" in ctx_lower and "配置" in context_text:
        return ("json_config", "JSON配置")
    if "服务列表" in context_text or ("blender" in ctx_lower and "服务" in context_text):
        return ("service_list", "服务列表")
    if "connect" in ctx_lower and "claude" in ctx_lower:
        return ("connect", "连接MCP")
    if "running" in ctx_lower or "9876" in context_text:
        return ("running", "运行状态")
    if "工具" in context_text and ("列表" in context_text or "mcp" in ctx_lower):
        return ("tools", "工具列表")
    if "状态" in context_text and ("正确" in context_text or "对" in context_text):
        return ("status_ok", "正确状态")
    if "连通性" in context_text or "测试" in context_text:
        return ("test", "测试")
    if "球体" in context_text or "立方体" in context_text:
        return ("result", "测试结果")
    if "基础场景" in context_text or "低多边形" in context_text:
        return ("example1", "示例1")
    if "材质" in context_text and "渲染" in context_text:
        return ("example2", "示例2")
    if "资产" in context_text or "poly haven" in ctx_lower or "hdr" in ctx_lower:
        return ("example3", "示例3")
    if "动画" in context_text and "关键帧" in context_text:
        return ("example4", "示例4")
    if "场景信息" in context_text:
        return ("example5", "示例5")

    return ("other", "")


def html_to_markdown(body_html: str, images: list) -> str:
    """
    将正文 HTML 转换为 Markdown，并在对应位置插入图片。
    """

    # 先按行处理 body_html，逐步构建 Markdown
    # 关键思路：在遇到图片位置时插入 Markdown 图片语法
    md_lines = []
    img_index = 0  # 当前处理的图片索引
    current_pos = 0  # 当前在 body_html 中的位置

    # 找到所有段落分隔点：图片标签、块级元素开头
    tokens = []

    # 收集图片标签位置
    for tag_match in re.finditer(r"<img[^>]*?>", body_html, re.IGNORECASE):
        tag = tag_match.group(0)
        data_src = re.search(r'data-src="([^"]*)"', tag)
        src = re.search(r'\ssrc="([^"]*)"', tag)
        url = data_src.group(1) if data_src else (src.group(1) if src else None)
        if url and url.startswith("http"):
            tokens.append(("image", tag_match.start(), html.unescape(url)))

    # 收集标题位置
    for h_match in re.finditer(r"<(h[2-6])[^>]*>(.*?)</\1>", body_html, re.DOTALL):
        level = int(h_match.group(1)[1])
        text = strip_tags(h_match.group(2))
        if text:
            tokens.append(("heading", h_match.start(), (level, text)))

    # 收集 <p> 段落
    for p_match in re.finditer(r"<p[^>]*>(.*?)</p>", body_html, re.DOTALL):
        text = strip_tags(p_match.group(1))
        if text and len(text) > 5:
            tokens.append(("paragraph", p_match.start(), text))

    # 收集代码块 <pre>
    for pre_match in re.finditer(
        r"<pre[^>]*>(.*?)</pre>", body_html, re.DOTALL
    ):
        code = pre_match.group(1)
        # 移除 <code> 标签
        code = re.sub(r"</?code[^>]*>", "", code)
        code = html.unescape(code).strip()
        if code:
            tokens.append(("code", pre_match.start(), code))

    # 收集 <blockquote>
    for bq_match in re.finditer(
        r"<blockquote[^>]*>(.*?)</blockquote>", body_html, re.DOTALL
    ):
        text = strip_tags(bq_match.group(1))
        if text:
            tokens.append(("blockquote", bq_match.start(), text))

    # 收集列表 <ul>/<ol>
    for list_match in re.finditer(
        r"<(ul|ol)[^>]*>(.*?)</\1>", body_html, re.DOTALL
    ):
        list_type = list_match.group(1)
        items = re.findall(r"<li[^>]*>(.*?)</li>", list_match.group(2), re.DOTALL)
        clean_items = [strip_tags(item) for item in items if strip_tags(item)]
        if clean_items:
            tokens.append(("list", list_match.start(), (list_type, clean_items)))

    # 按位置排序
    tokens.sort(key=lambda x: x[1])

    # 已使用的图片 URL（去重）
    used_images = set()

    for token_type, pos, data in tokens:
        if token_type == "image":
            url = data
            if url in used_images:
                continue
            # 去重：只保留没出现过的图片
            already_used = False
            for u in used_images:
                # 比较文件名（图片通常同名）
                if Path(u).name == Path(url).name:
                    already_used = True
                    break
            if already_used:
                continue
            used_images.add(url)

            # 获取上下文确定标签
            context_start = max(0, pos - 500)
            ctx_text = strip_tags(body_html[context_start:pos])
            category, label = classify_image(ctx_text)

            if label:
                if category == "example_cursor":
                    md_lines.append(f"\n**{label}：**\n")
                elif category == "example_blender":
                    md_lines.append(f"\n**{label}：**\n")
                else:
                    md_lines.append(f"\n**{label}**\n")
            md_lines.append(f"\n![{label or '图片'}]({url})\n")

        elif token_type == "heading":
            level, text = data
            # 跳过已有标题（避免与文章标题重复）
            if text not in ["", "前言"]:
                md_lines.append(f"\n{'#' * (level + 1)} {text}\n")

        elif token_type == "paragraph":
            md_lines.append(f"\n{data}\n")

        elif token_type == "code":
            md_lines.append(f"\n```\n{data}\n```\n")

        elif token_type == "blockquote":
            md_lines.append(f"\n> {data}\n")

        elif token_type == "list":
            list_type, items = data
            for i, item in enumerate(items, 1):
                prefix = f"{i}." if list_type == "ol" else "-"
                md_lines.append(f"{prefix} {item}")
            md_lines.append("")

    return "\n".join(md_lines)


def deduplicate_images(images: list) -> list:
    """按文件名去重，保留首次出现的顺序。"""
    seen_names = set()
    result = []
    for url, context in images:
        name = Path(url).name
        if name not in seen_names:
            seen_names.add(name)
            result.append((url, context))
    return result


def convert_from_html(html_content: str, url: str, output_path: str | None = None) -> str:
    """从 HTML 源码生成 Markdown（用于外部已获取 HTML 的场景）。"""
    title = extract_title(html_content)
    body_html = extract_post_body(html_content)

    if not body_html:
        print("❌ 无法提取文章正文，请检查 HTML 是否完整")
        sys.exit(1)

    images = extract_images(body_html)
    images = deduplicate_images(images)
    print(f"🖼️  找到 {len(images)} 张图片")

    markdown = html_to_markdown(body_html, images)
    return _write_markdown(title, url, markdown, output_path)


def convert_from_url(url: str, output_path: str | None = None) -> str:
    """从 URL 下载并生成 Markdown（需要直接网络访问）。"""
    print(f"📥 下载页面: {url}")
    html_content = fetch_html(url)
    return convert_from_html(html_content, url, output_path)


def _write_markdown(title: str, url: str, markdown: str, output_path: str | None = None) -> str:
    """写入最终的 Markdown 文件。"""
    full_md = f"""# {title}

> **原文链接**：[{url}]({url})

{markdown}

---

*原文链接：[{url}]({url})*
"""

    if not output_path:
        safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
        safe_title = re.sub(r"\s+", "-", safe_title)[:80]
        output_path = f"{safe_title}.md"

    output_path = str(Path(output_path).with_suffix(".md"))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_md)

    print(f"✅ 已生成 Markdown 文件: {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 convert.py --html-file <html文件路径> <文章URL> [输出文件名.md]")
        print("示例:")
        print("  python3 convert.py --html-file /tmp/page.html https://example.com/article/123")
        sys.exit(1)

    if sys.argv[1] == "--html-file":
        if len(sys.argv) < 4:
            print("❌ --html-file 需要提供 HTML 文件路径和文章 URL")
            sys.exit(1)
        html_path = sys.argv[2]
        url = sys.argv[3]
        output = sys.argv[4] if len(sys.argv) > 4 else None
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        convert_from_html(html_content, url, output)
    else:
        url = sys.argv[1]
        output = sys.argv[2] if len(sys.argv) > 2 else None
        convert_from_url(url, output)
