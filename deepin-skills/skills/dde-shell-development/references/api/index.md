# dde-shell 导出 API

## 触发关键词

本文档适用于以下任务场景：

**自然语言描述：**
- dde-shell插件开发
- 插件加载/跨插件通信
- 面板/停靠区/ containment
- QML面板/Applet

**API 接口描述：**
- DApplet / DContainment / DPanel
- DPluginLoader / DAppletBridge
- AppletItem / ContainmentItem

---

## 概述

libdde-shell 导出 C++ 和 QML 两套 API，所有 C++ 类位于 `ds` 命名空间。

## API 索引

| 分类 | 文档 | 包含类/接口 |
|------|------|------------|
| 核心类 | [core.md](core.md) | DApplet, DContainment, DPanel, DAppletBridge, DPluginLoader |
| QML 接口 | [qml-api.md](qml-api.md) | AppletItem, ContainmentItem, PanelPopup, DS |
