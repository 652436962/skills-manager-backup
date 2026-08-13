---
name: dtk-development
description: "用于 deepin/UOS v25 的 DTK（deepin Tool Kit）桌面应用开发维护，同时支持 DTK5 和 DTK6。当用户需要创建或修改 DTK QWidget/QML 应用，选择控件，实现主题、调色板、DCI 图标、DConfig、D-Bus、通知、单实例、窗口效果、平台适配，或编译调试 DTK 源码时使用。"
---

# DTK 开发指南

DTK 是深度桌面环境的核心开发框架，覆盖应用界面与交互、主题与视觉、配置、系统集成、工程构建和源码调试。按功能快速定位对应文档。

## 适用范围

- 默认目标为 deepin/UOS v25，同时支持 DTK5/Qt 5 和 DTK6/Qt 6。开始实现前先从 CMake 包名、链接库和源码分支确认 DTK/Qt 主版本，并全程使用对应版本的 API、模块名和构建配置，不要混用。
- 本 skill 负责普通 DTK 应用和 DTK 框架源码，不覆盖 DDE 组件各自的插件框架；涉及通用 DTK API 时仍可使用对应参考。

## 关键约束

- 先确定 Qt/DTK 主版本，再选择包名、target、头文件、库和安装路径；同一构建链路中不要混用 DTK5/Qt 5 与 DTK6/Qt 6。
- DCI 和 DTK builtin 图标默认通过基础名称查找，不在业务代码中展开资源绝对路径，也不要为普通图标修改进程级搜索目录。
- 使用 DConfig 时保持应用 ID、配置 name、meta 和 override 一致；排查缓存前先确认 daemon 版本和实际状态目录，不硬编码历史路径。
- 修改 DTK 框架源码后，要确认应用实际加载的是构建产物，而不是只验证编译成功后继续运行系统安装库。

## 默认工作流

1. 检查目标工程的 Qt/DTK 主版本、QWidget 或 QML 技术栈、应用 ID、构建方式和现有代码约定。
2. 判断问题属于应用层还是 DTK 框架层，并从下表读取完成任务所需的最少参考文档。
3. 优先使用目标项目已有模式和 DTK 公开 API；修改 DTK 源码前先定位实际绘制、平台插件或配置链路。
4. 完成实现及必要的 CMake、资源、DConfig、翻译、桌面文件和 Debian 打包改动。
5. 构建最小相关目标并运行验证；主题和窗口问题至少覆盖亮暗主题以及当前使用的 X11/Wayland 后端。
6. 交付前检查日志、单实例恢复、图标查找、配置默认值和安装后运行结果，并报告未执行的验证。

## 文档路由

| 场景 | 参考文档 |
|------|----------|
| 了解 DTK 架构、项目关系或定位跨应用共性问题 | [architecture.md](references/architecture.md) |
| 创建 DTK 应用、配置 CMake、应用身份、翻译、日志和依赖 | [app-dev-with-dtk.md](references/app-dev-with-dtk.md) |
| 修改、编译和调试 DTK 源码 | [dtksrc-compile-debug.md](references/dtksrc-compile-debug.md) |
| 选择和使用 QWidget 控件 | [widgets/index.md](references/widgets/index.md) |
| 选择和使用 QML 控件 | [declarative/index.md](references/declarative/index.md) |
| 查看 QWidget 与 QML 可运行示例 | [examples.md](references/examples.md) |
| 处理主题、配色、主题图标、字体和控件风格 | [theme/index.md](references/theme/index.md) |
| 处理窗口装饰、模糊效果和平台兼容 | [platform-abstraction.md](references/platform-abstraction.md) |
| 管理应用配置和 DConfig | [config/index.md](references/config/index.md) |
| 使用应用入口、默认日志、DBus、通知、单实例及系统服务 | [widgets/application.md](references/widgets/application.md)、[utilities/index.md](references/utilities/index.md) |

## 高频场景直达

- **自定义控件使用主题图标** → [theme/palette.md](references/theme/palette.md)
- **应用控件使用主题图标** → [theme/icontheme.md](references/theme/icontheme.md)
- **QML 中显示 dci 图标** → [declarative/dci-icon.md](references/declarative/dci-icon.md)
- **DGuiApplicationHelper 主题/调色板** → [utilities/gui-helper.md](references/utilities/gui-helper.md)
- **DSysInfo 系统版本判断** → [utilities/sysinfo.md](references/utilities/sysinfo.md)
- **DDBusSender DBus 通信** → [utilities/dbus.md](references/utilities/dbus.md)
- **DWindowManagerHelper 窗口管理** → [utilities/window-manager.md](references/utilities/window-manager.md)
- **QML D.DTK 全局对象** → [declarative/dtk-global.md](references/declarative/dtk-global.md)
- **DBlurEffectWidget 模糊效果** → [widgets/blur-effect.md](references/widgets/blur-effect.md)
- **DStyledItemDelegate 列表项** → [widgets/item-delegate.md](references/widgets/item-delegate.md)
- **DProgressBar 进度条** → [widgets/progress.md](references/widgets/progress.md)
- **DInputDialog 输入对话框** → [widgets/dialog.md](references/widgets/dialog.md)

创建或维护 DTK 应用时，先确认应用身份、翻译加载时机、默认日志初始化、图标名称查找、单实例窗口恢复和 DConfig 默认 appId，再进入具体控件实现。

## Evals 测试用例

验证 skill 有效性的测试用例，共 79 个，按功能模块分类组织。详见 [evals/README.md](evals/README.md)。
