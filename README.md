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
├── esp32/                   # ESP32 系列（乐鑫）开发技能集
├── stm32/                   # STM32 系列开发技能集
├── ch32/                    # CH32 RISC-V（沁恒）开发技能集
├── nrf-528xx/               # nRF528xx（Nordic）开发技能集
├── tools/                   # 嵌入式辅助工具（EasyEDA、串口调试）
├── zmk-project-init/        # ZMK 键盘固件项目初始化
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
| `esp32` | ESP32 系列（ESP32 / S3 / C3）开发入口：自动索引环境部署 / 项目初始化 / 调试排错全流程 | ESP32、ESP32-S3、ESP32-C3、乐鑫、IDF、Arduino |
| `stm32` | STM32 全系列开发入口：环境安装 / 项目初始化 / 调试排错全流程 | STM32、STM32F1/F4/L4/G0/H7、ST-Link |
| `ch32` | CH32 RISC-V 系列开发入口：环境安装 / 项目初始化 / 调试排错全流程 | CH32V003/103/203/303/307/317、沁恒、WCH-Link |
| `nrf-528xx` | nRF528xx 系列开发入口：SDK 安装 / 项目初始化 / 调试排错全流程 | nRF52、nRF52840、nRF52832、Nordic、Zephyr |
| `tools` | 嵌入式辅助工具入口：EasyEDA 原理图/PCB 设计、串口调试 | EasyEDA、嘉立创 EDA、原理图、PCB、串口监视、AT 命令 |
| `zmk-project-init` | ZMK 键盘固件项目：创建无线/有线键盘工程、添加自定义 shield、配置/编译/烧录 | ZMK、键盘固件、机械键盘、shield |
| `find-skills` | 发现并安装 Agent Skill：当用户寻找能做某事的功能或表达扩展 Agent 能力的意愿时使用 | "我该如何做 X"、"帮我找一个能做 X 的 skill"、"有没有做 X 的 skill" |
| `force-zh-reply` | 让 AI 在整个对话中主要使用简体中文回复，代码与专业英文术语保留原样，不受用户输入外文影响 | 常驻生效，无特定触发词 |

## 嵌入式开发技能集（平台级拆分）

嵌入式开发技能按 **平台** 拆分为独立顶层 skill（esp32 / stm32 / ch32 / nrf-528xx / tools / zmk-project-init），每个平台内部再按 **任务** 组织子 skill（环境部署 / 项目初始化 / 调试排错）。这样每个入口的触发描述聚焦、按需加载，避免集合入口描述稀释导致误触发或冗余加载。

> 该结构由原 `embedded-ai-skills` 集合入口按平台拆分而来，子技能文件全部保留原样。

### 各平台内部结构

| 平台 | 子 Skill | 功能 |
|------|----------|------|
| **ESP32**（含 S3 / C3） | `esp32/esp32-dev` | 开发入口：先询问用户选择 **IDF** 还是 **Arduino** 框架，再加载对应子 skill |
| | `esp32/esp32-dev-idf` | ESP-IDF（官方框架）开发：环境安装、工程创建、编译/烧录/监视、JTAG 调试，支持 Windows/Linux/macOS |
| | `esp32/esp32-dev-arduino` | Arduino CLI 开发：arduino-cli 安装、ESP32 内核配置、编译/上传/串口监视 |
| | `esp32/esp32-debug` | 调试排错：串口日志 + USB-JTAG（OpenOCD + GDB）系统化定位崩溃/BUG 根因 |
| **nRF528xx**（nRF52 / 52840 / 52832） | `nrf-528xx/nrf-connect-sdk-setup` | nRF Connect SDK（Zephyr 基座）环境搭建 SOP：检测已装组件，仅安装缺失项 |
| | `nrf-528xx/nrf-connect-project-init` | 项目初始化：自动侦测芯片型号，交互确认 GPIO/SPI/I2C/UART 资源与语言，搭建 CMake 工程并编译烧录验证 |
| | `nrf-528xx/nrf-528xx-debug` | 调试排错：串口/RTT 日志 + J-Link，环境准备→问题理解→代码研读→根因分析→报告输出 |
| **STM32** | `stm32/stm32-dev-setup` | 开发环境安装：跨平台，兼容 CubeIDE（路径 A）与纯 CLI（路径 B） |
| | `stm32/stm32-project-init` | 项目初始化：交互收集芯片型号、开发模式（HAL/CMSIS、C/C++）、时钟与外设需求，生成 CMakeLists.txt 与 hal_conf.h 并编译烧录 |
| | `stm32/stm32-debug` | 调试排错：串口日志 + ST-Link 根因分析 |
| **CH32**（沁恒 RISC-V） | `ch32/ch32-dev-setup` | 环境检测 + 工具链配置（MRS_Toolchain / MRS 内置 / xPack），WCH-Link/OpenOCD/wchisp 支持，CLI/MRS 双路径 |
| | `ch32/ch32-project-init` | 项目初始化：芯片选型 → 开发模式（SPL/CMSIS, C/C++）→ 外设配置 → CMakeLists 生成 → 编译 → 烧录 |
| | `ch32/ch32-debug` | 调试排错：串口日志 + WCH-Link/OpenOCD，RISC-V Trap/HardFault 排查 |
| **辅助工具** | `tools/easyeda-api` | 嘉立创 EDA（EasyEDA Pro）原理图 / PCB 设计，支持 EDA 内实时调试与扩展开发 |
| | `tools/emberinter` | EmberInterDebugTool CLI：串口监视、设备通信、固件验证、AT 命令测试 |
| **其他平台** | `zmk-project-init` | ZMK 键盘固件项目：创建无线/有线键盘工程、添加自定义 shield、配置/编译/烧录 |

### 使用示例

- "ESP32 开发环境搭建" → 调用 `esp32` 下的 `esp32-dev` → `esp32-dev-idf` / `esp32-dev-arduino`
- "nRF52840 项目初始化" → 调用 `nrf-528xx` 下的 `nrf-connect-project-init`
- "STM32 编译报错" → 调用 `stm32` 下的 `stm32-debug`
- "CH32V307 开发环境搭建" → 调用 `ch32` 下的 `ch32-dev-setup`
- "用 EasyEDA 画原理图 / PCB 布局" → 调用 `tools` 下的 `easyeda-api`
- "创建 ZMK 键盘项目" → 调用 `zmk-project-init`

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
- 移除 skill 时建议通过 GUI 的删除操作完成，会同步清理注册文件与各 Agent 部署链接。

## 使用方法

每个 skill 是一个独立的目录，包含 `SKILL.md` 文件，描述该 skill 的触发条件和执行步骤。

## 授权

MIT License
