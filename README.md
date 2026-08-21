# my-skills

我的 AI Agent Skills 集合，用于扩展 Qoder 等 AI 编码助手的能力。

## 目录结构

```
my-skills/
├── skills/          # Skill 定义（SKILL.md 等）
└── README.md
```

## 已收录 Skills

| Skill | 说明 |
|-------|------|
| `qt-serial-debug` | 通过 QtSerialAssist 的 MCP 工具（`/opt/QtSerialAssist/mcp-server/`）对串口/网络/Modbus 设备自动化调试：枚举/打开串口、发送指令等待回包、Modbus 读写寄存器、终端登录 uboot、快捷命令、批量回归测试 |
| `html2markdown` | 将网页文章转换为结构化 Markdown 文件，自动保留图片到对应位置。触发词：整理为 markdown、转成 md、保存文章 等 |
| `deepin-skills` | deepin/UOS 桌面开发技能集合入口：自动索引全部子 skill，覆盖 DDE 控制中心、dde-shell 面板、托盘插件与 DTK 桌面应用的开发维护 |
| `easyeda-api` | 嘉立创 EDA（EasyEDA Pro）API：PCB 设计、原理图编辑、封装/符号管理、项目操作；支持 EDA 内实时调试与扩展开发（120+ 类、62 枚举、70 接口） |
| `embedded-ai-skills` | 嵌入式 AI 开发技能集合入口：覆盖 ESP32、nRF528xx、STM32、ZMK 键盘固件及辅助工具（EasyEDA、串口调试）的完整开发流程 |
| `find-skills` | 发现并安装 Agent Skill：当用户寻找能做某事的功能或表达扩展 Agent 能力的意愿时使用 |
| `force-zh-reply` | 让 AI 在整个对话中主要使用简体中文回复，代码与专业英文术语保留原样，不受用户输入外文影响 |

## 使用方法

每个 skill 是一个独立的目录，包含 `SKILL.md` 文件，描述该 skill 的触发条件和执行步骤。

## 授权

MIT License
