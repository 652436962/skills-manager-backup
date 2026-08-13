---
name: dde-control-center-development
description: "用于 deepin/UOS v25 的 DDE 控制中心框架与插件开发维护。当用户需要新增或修改控制中心设置模块、模块树与搜索、DccObject、控制中心 QML 组件、D-Bus 数据交互、插件构建安装或加载调试时使用。"
---

# DDE 控制中心开发指南

DDE 控制中心（dde-control-center）是 DDE 桌面环境的系统设置面板，采用插件化架构，框架只负责模块树管理、导航、搜索和页面布局，所有具体功能均由插件实现。

## 适用范围

- 默认目标为 deepin/UOS v25 和对应的 Qt 6 控制中心插件接口。
- 开始前检查目标仓库分支、`debian/changelog`、CMake 依赖和现有插件写法；若不是 v25，不要直接套用本文档中的 API、安装路径或调试命令。
- 本 skill 只负责控制中心框架和插件，不覆盖独立桌面应用、任务栏或 Shell 扩展。

## 关键约束

- v25 C++ 插件通过 `DCC_FACTORY_CLASS` 注册数据对象，并使用 `DdeControlCenter` 提供的 CMake target 和安装宏；不要套用旧版插件基类或托盘插件接口。
- `--spec` 只替换控制中心插件搜索路径。修改框架库或 QML 引擎组件时，还要设置构建目录对应的动态库和 QML 导入路径，并确认进程实际加载的新产物。
- 插件根 `{Name}.qml` 创建模块元数据时不能依赖 `dccData`；数据对象在插件工厂加载后才可用于后续页面。

## 默认工作流

1. 先判断任务属于框架、插件、API 查询还是故障排查，并检查目标工程中已有的相邻实现。
2. 从下表读取完成任务所需的最少参考文档；涉及现有代码时，以目标仓库的头文件、CMake 宏和同类插件为最终依据。
3. 保持现有插件目录、命名、模块树和 Interaction/Model/Worker 分层方式，避免为局部需求引入新的架构。
4. 完成代码、QML、CMake、翻译和打包文件中与任务直接相关的改动。
5. 按改动范围构建目标插件或控制中心，并使用 `--spec` 或构建目录环境变量验证实际加载的是新产物。
6. 交付前检查插件是否显示、导航和搜索是否可达、QML 是否有运行时错误、D-Bus 数据是否更新，并报告未能执行的验证。

## 快速路由

| 场景 | 参考文档 |
|------|----------|
| 了解控制中心架构与设计原理 | [references/architecture.md](references/architecture.md) |
| 从零开始创建新插件（CMake、打包、翻译、安装） | [references/plugin-development.md](references/plugin-development.md) |
| 查找 C++ API（DccObject、DccApp、DccFactory 等） | [references/cpp-api.md](references/cpp-api.md) |
| 查找 QML 组件（DccGroupView、DccRepeater、DccDBusInterface 等） | [references/qml-api.md](references/qml-api.md) |
| 调试技巧与常见问题排查 | [references/debugging.md](references/debugging.md) |

## Evals 测试用例

验证 skill 有效性的测试用例，共 21 个，按功能模块分类组织。详见 [evals/README.md](evals/README.md)。

## 相关代码仓库

- 控制中心框架：https://github.com/linuxdeepin/dde-control-center
- 示例插件：`examples/plugin-example/`
