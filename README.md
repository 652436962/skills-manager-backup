# my-skills

我的 AI Agent Skills 集合，用于扩展 Qoder、opencode 等 AI 编码助手的能力，由 **Skills Manager** 统一管理与部署。

## 目录结构

本仓库即 Skills Manager 的中央仓库（自动 git 备份至 `652436962/skills-manager-backup`）：

```
skills/                      # ~/.skills-manager/skills（中央仓库根目录）
├── README.md
├── .skills-manager/         # Skills Manager 元数据（注册/场景跟踪文件，勿手动修改）
│   ├── protocol.json        # 合并协议版本
│   ├── schema.json          # 数据模型版本
│   ├── skills/              # 每个 skill 的注册信息：<skill_id>.json
│   ├── scenarios/           # 场景（预设）定义：<scenario_id>.json
│   └── scenario-skills/     # 场景-技能成员关系：<scenario_id>/<skill_id>.json
├── deepin-skills/           # deepin/UOS 桌面开发技能集
├── easyeda-api/             # 嘉立创 EDA（EasyEDA Pro）API 技能
├── embedded-ai-skills/      # 嵌入式 AI 开发技能集
├── find-skills/             # 查找并安装 Agent Skill
├── force-zh-reply/          # 强制简体中文回复
├── html2markdown/           # 网页文章转 Markdown
└── qt-serial-debug/         # 串口/网络/Modbus 自动化调试
```

## 已收录 Skills

| Skill | 说明 | 触发词 / 使用场景 |
|-------|------|-------------------|
| `qt-serial-debug` | 通过 QtSerialAssist 的 MCP 工具（`/opt/QtSerialAssist/mcp-server/`）对串口/网络/Modbus 设备自动化调试：枚举/打开串口、发送指令等待回包、Modbus 读写寄存器、终端登录 uboot、快捷命令、批量回归测试 | 串口调试、读保持寄存器、Modbus、登录 uboot、批量回归测试 |
| `html2markdown` | 将网页文章转换为结构化 Markdown 文件，自动保留图片到对应位置 | 整理为 markdown、转成 md、保存文章、html2markdown |
| `deepin-skills` | deepin/UOS 桌面开发技能集合入口：自动索引全部子 skill，覆盖 DDE 控制中心、dde-shell 面板、托盘插件与 DTK 桌面应用的开发维护 | deepin/UOS v25、DDE 控制中心、dde-shell、托盘插件、DTK 应用开发 |
| `easyeda-api` | 嘉立创 EDA（EasyEDA Pro）API：PCB 设计、原理图编辑、封装/符号管理、项目操作；支持 EDA 内实时调试与扩展开发（120+ 类、62 枚举、70 接口） | 嘉立创EDA，启动！、立创EDA，启动！、EDA，启动！、EasyEDA、PCB、原理图、PCB设计、schematic、footprint |
| `embedded-ai-skills` | 嵌入式 AI 开发技能集合入口：覆盖 ESP32、nRF528xx、STM32、ZMK 键盘固件及辅助工具（EasyEDA、串口调试）的完整开发流程 | 嵌入式开发、ESP32、nRF528xx、STM32、ZMK 键盘固件、MCU、固件烧录调试 |
| `find-skills` | 发现并安装 Agent Skill：当用户寻找能做某事的功能或表达扩展 Agent 能力的意愿时使用 | "我该如何做 X"、"帮我找一个能做 X 的 skill"、"有没有做 X 的 skill" |
| `force-zh-reply` | 让 AI 在整个对话中主要使用简体中文回复，代码与专业英文术语保留原样，不受用户输入外文影响 | 常驻生效，无特定触发词 |

## Skills Manager 使用说明

### 数据位置

| 内容 | 路径 |
|------|------|
| 中央仓库（git 备份源） | `~/.skills-manager/skills` |
| 数据库（重建缓存） | `~/.skills-manager/skills-manager.db` |
| GUI 配置 | `~/.config/skills-manager/repo-config.json` |
| 运行日志 | `~/.local/share/com.agentskills.desktop/logs/skills-manager.log` |

> 技能库状态以中央仓库 `.skills-manager/` 下的跟踪文件为准，数据库由 GUI 启动时据此重建；直接改数据库无法生效。

### Agent 部署目录

每个 skill 通过符号链接部署到各 Agent 的技能目录（目标统一指向中央仓库）：

- `~/.agents/skills/`（Cline / Warp）
- `~/.config/opencode/skills/`（opencode）
- `~/.qoder/skills/`（Qoder）、`~/.codebuddy/skills/`（CodeBuddy）
- `~/.gemini/skills/`（Gemini CLI）、`~/.grok/skills/`（Grok）、`~/.copilot/skills/`（GitHub Copilot）
- `~/.uos-ai/skills/`（uos-ai，自定义工具）

### CLI 常用命令

```bash
skills-manager-cli skills list          # 查看技能库
skills-manager-cli skills adopt <目录>  # 从目录导入/注册 skill
skills-manager-cli skills sync          # 按当前预设同步部署到全部 Agent
skills-manager-cli skills install <ref> # 安装 skill（本地路径 / git / owner/repo）
skills-manager-cli presets list         # 查看预设（场景）
skills-manager-cli agents list          # 查看已安装的 Agent
```

### 注意事项

- 变更 skill 目录后需在 Skills Manager GUI 中触发重新索引（或重启），数据库才会重建。
- 不要在 GUI 中把 `~/.skills-manager/skills`（仓库根目录）当作导入源，会触发防递归保护报错；应导入具体 skill 目录。
- 重命名 skill 目录时，需同步更新 `.skills-manager/skills/<skill_id>.json` 与各 Agent 部署链接，否则会被判定为"原来源路径不存在"而移除。

## 使用方法

每个 skill 是一个独立的目录，包含 `SKILL.md` 文件，描述该 skill 的触发条件和执行步骤。

## 授权

MIT License
