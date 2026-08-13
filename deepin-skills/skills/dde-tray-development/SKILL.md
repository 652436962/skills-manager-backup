---
name: dde-tray-development
description: "用于 deepin/UOS v25 的 dde-tray-loader 托盘和快捷面板插件开发维护。当用户需要实现 PluginsItemInterfaceV2、托盘图标、PluginFlags、快捷面板控件与详情页、Dock 消息协议、右键菜单或插件加载显示排查时使用。"
---

# DDE 托盘插件开发指南

DDE 托盘插件运行在任务栏托盘区域，继承 PluginsItemInterfaceV2 接口，可实现托盘图标、快捷面板控件、右键菜单等功能。

## 适用范围

- 默认目标为 deepin/UOS v25 的 `dde-tray-loader`、V2 IID 和 Dock Plugin API `2.0.0`。
- 开始前检查目标源码是否包含 `PluginsItemInterfaceV2` 和 `dde-tray-loader`；本 skill 不覆盖 `DApplet`、`DPanel` 或 LayerShell 插件体系。
- 普通 Qt `QSystemTrayIcon` 应用不属于 DDE 托盘插件。

## 关键约束

- `Type_Tray` 与 `Type_Quick` 互斥；快捷面板插件必须选择一个 `Quick_Panel_*` 布局标志，基础托盘插件不要附加无关能力。
- 使用 `Attribute_CanSetting` 时必须实现控制中心图标接口并安装对应资源；否则不要声明该属性。
- `PluginProxyInterface` 由 loader 管理，插件只保存指针，不负责释放。快捷面板宽度由布局标志决定，控件只固定框架规定的高度。

## 默认工作流

1. 先确认目标是纯托盘、快捷面板、详情页、消息协议还是右键菜单，并核对接口和 API 版本。
2. 检查目标项目已有插件、`PluginFlags`、IID、安装路径和翻译加载方式，再读取下表中的最少参考文档。
3. 只选择任务需要的类型和属性标志；不要把 `Attribute_CanSetting`、拖拽或快捷面板能力强加给基础托盘插件。
4. 实现插件接口、控件和必要的消息处理，并同步修改 CMake、JSON 元数据、翻译和安装规则。
5. 构建安装后验证插件被 loader 发现，托盘或快捷面板正确显示，消息、菜单、详情页和位置变化按需求工作。
6. 检查亮暗主题图标、控制中心显隐、重启持久化和日志错误，并报告未执行的验证。

## 快速路由

| 场景 | 参考文档 |
|------|----------|
| 了解托盘插件接口规范 | [references/tray-plugin-spec.md](references/tray-plugin-spec.md) |
| 开发快捷面板插件 | [references/quick-panel-guide.md](references/quick-panel-guide.md) |
| 实现消息协议通信 | [references/message-protocol.md](references/message-protocol.md) |
| 实现右键菜单 | [references/context-menu.md](references/context-menu.md) |

## Evals 测试用例

验证 skill 有效性的测试用例，共 13 个，按功能模块分类组织。详见 [evals/README.md](evals/README.md)。
