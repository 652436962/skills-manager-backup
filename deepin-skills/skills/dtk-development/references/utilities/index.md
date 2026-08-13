# 工具类与核心类

## 触发关键词

本文档适用于以下任务场景：

**自然语言描述：**
- 获取系统信息/系统版本
- DBus通信/进程间通信
- 窗口管理器特性
- 打开文件/打开URL
- 日志管理/单实例
- 拼音转换/文件系统工具

**API 接口描述：**
- DSysInfo / DDBusSender / DWindowManagerHelper
- DDesktopServices / DLogManager / DSingleton

---

## 概述

DTK 工具类与核心类提供主题系统、字体管理、系统信息、DBus 通信、窗口管理、日志、单实例等跨项目通用功能，主要来自 dtkcore/dtkgui/dtkwidget。

## 类索引

| 类名 | 所属模块 | 文档 |
|------|---------|------|
| DGuiApplicationHelper | dtkgui | [gui-helper.md](gui-helper.md) |
| DFontSizeManager | dtkgui/dtkwidget | [font-manager.md](font-manager.md) |
| DSysInfo | dtkcore | [sysinfo.md](sysinfo.md) |
| DDBusSender | dtkcore | [dbus.md](dbus.md) |
| DPaletteHelper | dtkwidget | [../widgets/palette-helper.md](../widgets/palette-helper.md) |
| DWindowManagerHelper | dtkgui | [window-manager.md](window-manager.md) |
| DDesktopServices | dtkcore/dtkgui | [desktop-services.md](desktop-services.md) |
| DLogManager | dtkcore | [log.md](log.md) |
| DSingleton | dtkcore | [singleton.md](singleton.md) |

## 快速决策树

```
需要什么功能？
    │
    ├─ 主题/调色板/平台判断？
    │   └─ DGuiApplicationHelper → [gui-helper.md](gui-helper.md)
    │
    ├─ 字体大小管理？
    │   └─ DFontSizeManager / DFontManager → [font-manager.md](font-manager.md)
    │
    ├─ 系统版本/类型判断？
    │   └─ DSysInfo → [sysinfo.md](sysinfo.md)
    │
    ├─ DBus 通信？
    │   └─ DDBusSender / DDBusInterface → [dbus.md](dbus.md)
    │
    ├─ 窗口管理器/装饰控制？
    │   └─ DWindowManagerHelper → [window-manager.md](window-manager.md)
    │
    ├─ 文件管理器/系统音效？
    │   └─ DDesktopServices → [desktop-services.md](desktop-services.md)
    │
    ├─ 日志？
    │   └─ DLogManager → [log.md](log.md)
    │
    └─ 单实例/进程间通信？
        └─ DSingleton → [singleton.md](singleton.md)
```

## 相关文档

- [../theme/index.md](../theme/index.md) — 主题系统（调色板/图标/风格）
- [../config/index.md](../config/index.md) — DConfig 配置系统
- [../architecture.md](../architecture.md) — DTK 核心架构
