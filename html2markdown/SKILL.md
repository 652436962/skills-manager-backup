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
# 步骤1: 下载原始 HTML
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY \
  wget -q -O /tmp/article_raw.html \
  --header="User-Agent: Mozilla/5.0" \
  "文章URL"

# 步骤2: 用 --html-file 模式运行脚本
python3 ~/.codebuddy/skills/html2markdown/scripts/convert.py \
  --html-file /tmp/article_raw.html "文章URL" "输出文件名.md"
```

- 第一个参数：`--html-file <html文件路径>`
- 第二个参数：文章完整链接
- 第三个参数（可选）：输出文件名，不指定则自动用文章标题命名

### 2. 检查结果

脚本执行后：
- 检查输出是否成功（应显示 "已生成 Markdown 文件" 和图片数量）
- 使用 `open_result_view` 展示生成的文件
- 如生成的 Markdown 图片数量明显偏少，说明图片提取不全，需要手动补全

### 3. 图片不全时的处理

如果图片未正确提取（常见于 SPA 动态渲染页面），需要：
1. 分析原始 HTML 中的图片 URL 格式（可能在 `<script>` JSON 数据中）
2. 提取完整图片 URL（含查询参数，如签名等）
3. 根据原文上下文将图片插入到 Markdown 对应位置

## 注意事项

- 转换脚本依赖 Python 3 标准库，无需额外安装依赖
- 图片链接指向原图床，需联网查看
- **图片 URL 含查询参数时务必保留**，某些 CDN 依赖签名参数加载图片
- 代码块会被保留为 Markdown 代码块格式
- 对于 SPA 动态渲染页面，图片可能在内嵌 JSON 中，需额外处理
