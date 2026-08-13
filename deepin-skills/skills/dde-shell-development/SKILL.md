---
name: dde-shell-development
description: "用于 deepin/UOS v25 的 dde-shell Applet、Containment、Panel 插件及 LayerShell 窗口开发维护。当用户需要扩展 Dock、顶栏、侧栏等 Shell 面板，使用 DApplet/DPanel、Shell QML API、插件桥接，或创建贴靠屏幕边缘的 Wayland 窗口时使用。"
---

# dde-shell 开发指南

dde-shell 是 DDE 桌面环境的 Shell 核心，负责 Dock、顶栏、侧栏等面板的插件化管理。采用三层插件模型（Applet → Containment → Panel），支持 QML 界面和 C++ 后端。

## 适用范围

- 默认目标为 deepin/UOS v25、dde-shell 2.x 和对应的 Qt 6 接口。
- 开始前检查目标仓库分支、`debian/changelog`、插件元数据和已有同类插件；若版本不匹配，以目标源码导出的 API 为准。
- 仅在目标使用 dde-shell package、`DApplet`、`DContainment`、`DPanel` 或 LayerShell 接口时采用本文档，不覆盖 `PluginsItemInterfaceV2` 插件体系。

## 关键约束

- 先根据宿主和父子关系选择 Applet、Containment 或 Panel；插件 ID、`Plugin.Parent`、安装包目录和运行时父插件必须一致。
- 每个 C++ Applet、Containment 或 Panel 的实现文件必须包含 `<pluginfactory.h>`，并在文件末尾依次写入 `D_APPLET_CLASS(ClassName)` 和 `#include "<实现文件名>.moc"`。缺少工厂注册时动态库可能构建成功，但 dde-shell 无法实例化并加载插件。
- Applet/Containment/Panel 属于 dde-shell 插件体系，不要混用 dde-tray-loader 的 IID、flags 或消息协议。
- LayerShell 窗口必须同时核对目标屏幕、锚点、层级和键盘交互；只有需要保留工作区的面板才设置排他区域，并验证多屏和热插拔行为。

## 默认工作流

1. 判断需求属于 Applet、Containment、Panel 还是独立 LayerShell 窗口，并确认是否属于独立的托盘插件体系。
2. 检查目标工程的插件元数据、父子关系、安装路径和现有 CMake 辅助函数，再读取下表中的最少参考文档。
3. 优先沿用相邻插件的 QML/C++ 组织、生命周期和跨插件通信方式。
4. 完成实现及必要的 CMake、元数据、翻译和打包改动。
5. 构建目标后，用 `dde-shell -p <plugin-id>` 或构建目录的自定义路径进行隔离加载；LayerShell 窗口还要验证锚点、层级、排他区域和多屏行为。
6. 交付前检查插件发现、父子加载、QML 错误、窗口交互和重启后的行为，并报告未执行的验证。

## 快速路由

| 场景 | 参考文档 |
|------|----------|
| 了解 dde-shell 架构与设计原理 | [design.md](references/design.md) |
| 开发 Applet/Containment/Panel 插件 | [plugin-development.md](references/plugin-development.md) |
| 使用 LayerShell 锚定窗口 | [layershell.md](references/layershell.md) |
| 查找 C++ 和 QML API | [api/index.md](references/api/index.md) |

## Evals 测试用例

验证 skill 有效性的测试用例，共 19 个，按功能模块分类组织。详见 [evals/README.md](evals/README.md)。
