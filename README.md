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
| `html2markdown` | 将网页文章转换为结构化 Markdown 文件，自动保留图片 |

## 使用方法

每个 skill 是一个独立的目录，包含 `SKILL.md` 文件，描述该 skill 的触发条件和执行步骤。

## 授权

MIT License
