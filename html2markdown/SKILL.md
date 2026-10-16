---
name: html2markdown
description: "将网页文章自动转换为结构化的 Markdown 文件。从原始 HTML 提取标题、正文、代码块，并自动保留所有图片到对应位置。触发词：整理为markdown、转成md、保存文章、html2markdown 等。"
---

# 网页文章转 Markdown

将网页文章链接自动转换为结构化的 Markdown 文件，完整保留原文排版和图片。

## 使用场景

- 用户提供文章 URL，要求整理为 Markdown 文件
- 用户想离线保存技术文章
- 用户需要将文章内容迁移到其他平台

## 工作流程

### 1. 获取 HTML 并执行转换

收到文章链接后，先用 wget 绕过代理下载原始 HTML，再运行转换脚本：

```bash
# 步骤1: 下载原始 HTML（务必下载到当前工作目录，不要用 /tmp——
# 转换脚本运行在独立沙箱中，读不到 /tmp 里的文件）
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY \
  wget -q -O ./article_raw.html \
  --header="User-Agent: Mozilla/5.0" \
  "文章URL"
```

**脚本二选一：**

| 脚本 | 适用页面 | 特点 |
| --- | --- | --- |
| `scripts/convert_papermod.py`（**首选**） | 静态博客/文档站（Hugo PaperMod、VitePress、Hexo、Jekyll）+ **微信公众号文章** | 结构化解析，完整保留表格、图片、代码语言、列表、引用块；自动剔除标题锚点 `#`；自动处理微信的 `data-src` 懒加载图与 `&nbsp;` |
| `scripts/convert.py` | 仅作兜底 | 通用正则，表格/图片易丢，需人工补 |

```bash
# 首选：静态站点 / 微信公众号
python3 ~/.workbuddy/skills/html2markdown/scripts/convert_papermod.py \
  --html-file ./article_raw.html \
  --url "文章URL" \
  [--title "文章标题"] [--base https://example.com] [--out 输出文件名.md]

# 兜底：通用正则
python3 ~/.workbuddy/skills/html2markdown/scripts/convert.py \
  --html-file ./article_raw.html "文章URL" "输出文件名.md"
```

`convert_papermod.py` 参数说明：
- `--html-file` / `--url`：必填；`--title` 省略时依次尝试 `og:title` → 微信 `#activity-name` → `var msg_title` → `<title>`
- `--base` 省略时自动取 URL 的协议+域名，用于补全 `/images/x.jpg` 这类相对路径
- `--out` 省略时按标题生成文件名
- 脚本会输出「图片 / 表格行 / 代码围栏 / 标题」四项计数（标题计数已排除代码块内的 `#` 注释行），便于直接核对完整性

**已内置的页面适配**（无需再手写转换器）：

| 页面特征 | 处理方式 |
| --- | --- |
| 微信 `<div id="js_content">` | 按 `<div>` 嵌套配对截取正文，避免把点赞/分享 UI 收进来 |
| 微信图片懒加载 `data-src` | 优先取 `data-src`，其次 `src`；自动补 `https:` 协议头 |
| 微信 `<pre lang="bash">` | 语言取自 `lang` 属性；`lang="text"` 视为无语言 |
| 微信 `<li><p>…</p></li>` | 列表项内不再插入空行，避免出现「`-` 单独一行」 |
| `<blockquote>` | 缓冲后按行加 `> ` 前缀，避免正文掉到引用块外 |
| 标题锚点 `<a hidden class=anchor>#</a>` | 整体丢弃，标题末尾不留 `#` |
| `&nbsp;` / 零宽空格 / 行首多余空格 | 统一清理 |

### 2. 检查结果

脚本执行后：
- 检查输出是否成功（应显示 "已生成 Markdown 文件" 和图片数量）
- 使用 `present_files` 展示生成的文件
- 如生成的 Markdown 图片数量明显偏少，说明图片提取不全，需要手动补全

### 3. 结果校验

脚本执行后必然做一次核对，不要凭感觉认为转换正确：

```bash
# 原图数量 vs 生成文件里的图片数量，必须一致
grep -oE '<img[^>]*>' 原始HTML | wc -l
grep -c '!\[' 输出文件.md
# 表格数量
grep -oE '<table' 原始HTML | wc -l
grep -c '^| ' 输出文件.md
```

再抽查：标题是否残留 `#`、代码块是否有语言围栏、参考链接是否保留了 URL、图片 URL 是否返回 200：

```bash
curl -s -o /dev/null -w '%{http_code} %{url_effective}\n' -L 图片URL
```

**仅在使用 `convert.py` 时**需要按下面两种情况人工补全：

1. **SPA / 动态渲染页面**：图片可能在 `<script>` 内嵌 JSON 中。用
   `grep -oE '<img[^>]*>' 原始HTML` 抓全部 `<img>`，再按上下文插入。
2. **静态站点**：`convert.py` 会丢掉 `<table>`（整个表格消失）、相对路径图片
   （`src=/images/x.jpg`）、链接 URL，标题末尾还会残留锚点 `#`。
   → 改用 `convert_papermod.py` 即可，无需手写转换器。

## 中英双版本（可选）

用户要求「中文版本」时：新建 `<原名>.zh.md`，逐节翻译，并遵守
- 命令、配置、日志输出、代码块 **原样保留**，不做任何改动
- 专有名词中英对照（Grandmaster 主时钟、holdover 保持、falseticker 错误报时源等）
- 数字与单位原样（ns/µs/ms、价格、时长）
- 翻译后用上面的计数命令核对：中英两版的图片/代码围栏/表格行/标题数应完全一致

## 注意事项

- 转换脚本依赖 Python 3 标准库，无需额外安装依赖
- 图片链接指向原图床，需联网查看
- **图片 URL 含查询参数时务必保留**，某些 CDN 依赖签名参数加载图片
- 代码块会被保留为 Markdown 代码块格式
- 对于 SPA 动态渲染页面，图片可能在内嵌 JSON 中，需额外处理
