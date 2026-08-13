---
name: "deepin-skills"
description: "deepin/UOS 桌面开发技能集合入口 skill。自动索引全部子 skill，覆盖 DDE 控制中心、dde-shell 面板、托盘插件与 DTK 桌面应用的开发维护。当用户进行 deepin/UOS v25 原生应用或 DDE 桌面插件开发时调用。"
---

# deepin Skills — deepin/UOS 桌面开发技能集

面向 deepin/UOS v25 原生应用和 DDE 桌面插件开发的技能集合。

## 子 Skill 索引

| Skill | 文件 | 功能 |
|-------|------|------|
| **dde-control-center-development** | [SKILL.md](skills/dde-control-center-development/SKILL.md) | DDE 控制中心框架与插件开发（设置模块、模块树、DccObject、QML、D-Bus） |
| **dde-shell-development** | [SKILL.md](skills/dde-shell-development/SKILL.md) | dde-shell Applet/Containment/Panel 插件及 LayerShell 窗口开发 |
| **dde-tray-development** | [SKILL.md](skills/dde-tray-development/SKILL.md) | dde-tray-loader 托盘和快捷面板插件开发（PluginsItemInterfaceV2、Dock 消息协议） |
| **dtk-development** | [SKILL.md](skills/dtk-development/SKILL.md) | DTK 桌面应用开发（DTK5/DTK6：QWidget/QML、主题、DConfig、D-Bus） |

## 使用方式

描述你的 deepin/UOS 开发需求，系统会自动定位并调用对应子 skill 的完整流程。例如：

- "为控制中心新增一个系统设置模块" → 调用 `dde-control-center-development`
- "开发一个任务栏网络状态插件" → 调用 `dde-shell-development`
- "实现托盘图标和右键菜单" → 调用 `dde-tray-development`
- "创建一个 DTK 设置窗口应用" → 调用 `dtk-development`
