---
name: find-skills
description: 当用户提出诸如"我该如何做 X"、"帮我找一个能做 X 的 skill"、"有没有能……的 skill"等问题，或表达出扩展 Agent 能力的意愿时，帮助用户发现并安装 Agent Skill。当用户在寻找某种可能已存在可安装 skill 的功能时，应使用此 skill。
---

# 查找 Skill

此 skill 帮助你从开放的 Agent Skill 生态系统中发现并安装 skill。

## 何时使用此 Skill

在用户出现以下情况时使用此 skill：

- 询问"我该如何做 X"，而 X 可能是已有现成 skill 的常见任务
- 说"帮我找一个能做 X 的 skill"或"有没有做 X 的 skill"
- 询问"你能做 X 吗"，而 X 是某种专业化能力
- 表达出扩展 Agent 能力的意愿
- 想要搜索工具、模板或工作流
- 提到希望在某个特定领域获得帮助（设计、测试、部署等）

## 什么是 Skills CLI？

Skills CLI（`npx skills`）是开放 Agent Skill 生态系统的包管理器。Skill 是模块化的软件包，通过专业知识、工作流和工具来扩展 Agent 的能力。

**核心命令：**

- `npx skills find [query] [--owner <owner>]` - 交互式或按关键词搜索 skill，可选择限定某个 GitHub 所有者
- `npx skills add <package>` - 从 GitHub 或其他来源安装 skill
- `npx skills check` - 检查 skill 更新
- `npx skills update` - 更新所有已安装的 skill

**在线浏览 skill：** https://skills.sh/

## 如何帮助用户查找 Skill

### 第 1 步：理解用户需求

当用户寻求帮助时，先明确：

1. 所属领域（如 React、测试、设计、部署）
2. 具体任务（如编写测试、创建动画、审查 PR）
3. 该任务是否足够常见，很可能已有对应的 skill

### 第 2 步：优先查看排行榜

在运行 CLI 搜索之前，先查看 [skills.sh 排行榜](https://skills.sh/)，看该领域是否已有知名 skill。排行榜按总安装量对 skill 排名，能突显最受欢迎、经过实战检验的选项。

例如，Web 开发领域的热门 skill 包括：
- `vercel-labs/agent-skills` — React、Next.js、Web 设计（各 10 万+ 安装量）
- `anthropics/skills` — 前端设计、文档处理（10 万+ 安装量）

### 第 3 步：搜索 Skill

如果排行榜无法满足用户需求，运行查找命令：

```bash
npx skills find [query] [--owner <owner>]
```

例如：

- 用户问"如何让我的 React 应用更快？" → `npx skills find react performance`
- 用户问"能帮我做 PR 审查吗？" → `npx skills find pr review`
- 用户问"我需要创建变更日志" → `npx skills find changelog`

### 第 4 步：推荐前先验证质量

**不要仅凭搜索结果就推荐某个 skill。** 务必核实：

1. **安装量** — 优先选择安装量 1K+ 的 skill。安装量低于 100 的要谨慎对待。
2. **来源信誉** — 官方来源（`vercel-labs`、`anthropics`、`microsoft`）比不知名作者更值得信赖。
3. **GitHub Star 数** — 检查源仓库。来自 Star 数少于 100 的仓库的 skill 应持怀疑态度。

### 第 5 步：向用户展示选项

找到相关 skill 后，向用户展示以下信息：

1. Skill 名称及其功能
2. 安装量和来源
3. 可以运行的安装命令
4. skills.sh 上的详情链接

回复示例：

```
我找到了一个可能有帮助的 skill！"react-best-practices" skill 提供
来自 Vercel 工程团队的 React 和 Next.js 性能优化指南。
（18.5 万安装量）

安装方式：
npx skills add vercel-labs/agent-skills@react-best-practices

了解更多：https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

### 第 6 步：主动提供安装

如果用户希望继续，你可以帮其安装该 skill：

```bash
npx skills add <owner/repo@skill> -g -y
```

`-g` 参数表示全局安装（用户级别），`-y` 表示跳过确认提示。

## 常见 Skill 分类

搜索时可以参考以下常见分类：

| 分类     | 示例查询关键词                            |
| -------- | ---------------------------------------- |
| Web 开发 | react, nextjs, typescript, css, tailwind |
| 测试     | testing, jest, playwright, e2e           |
| DevOps   | deploy, docker, kubernetes, ci-cd        |
| 文档     | docs, readme, changelog, api-docs        |
| 代码质量 | review, lint, refactor, best-practices   |
| 设计     | ui, ux, design-system, accessibility     |
| 生产力   | workflow, automation, git                |

## 高效搜索技巧

1. **使用具体的关键词**："react testing" 比单独的 "testing" 效果更好
2. **尝试同义词**：如果 "deploy" 搜不到，试试 "deployment" 或 "ci-cd"
3. **查看热门来源**：许多 skill 来自 `vercel-labs/agent-skills` 或 `ComposioHQ/awesome-claude-skills`

## 未找到 Skill 时

如果不存在相关的 skill：

1. 如实告知未找到现有的 skill
2. 主动提出用你的通用能力直接帮助完成任务
3. 建议用户可以用 `npx skills init` 创建自己的 skill

示例：

```
我搜索了与"xyz"相关的 skill，但没有找到匹配项。
我仍然可以直接帮你完成这个任务！需要我继续吗？

如果这是你经常做的事情，你可以创建自己的 skill：
npx skills init my-xyz-skill
```
