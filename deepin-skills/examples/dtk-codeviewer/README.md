# DTK Code Viewer

## 项目背景

dtk-codeviewer 是一个使用 `dtk-development` skill 指导开发的 DTK6 示例项目。项目以代码和文本文件查看器为业务载体，主要目标不是实现完整的代码编辑器，而是展示如何按照 DTK 应用开发规范完成从需求分析、技术选型、界面实现到系统集成、构建安装和 Debian 打包的完整流程。

项目既展示 DTK 控件，也覆盖一个桌面应用通常需要的基础能力：

- 使用 `DApplication` 管理应用元数据、翻译和单实例；第二个进程退出后重新激活已有窗口。
- 使用 Qt logging category 和 `DLogManager` 输出分类日志，并采用 DTK 默认日志路径和格式。
- 使用 Qt Linguist 和 `DApplication::loadTranslator()` 提供中文翻译。
- 使用 `DConfig` 管理字号、透明度和窗口尺寸等用户配置。
- 使用 `DIconTheme` 和 DCI 应用图标适配主题及图标尺寸。
- 使用 `DBlurEffectWidget`、DTK 字体体系和主题调色板实现一致的窗口视觉效果。
- 使用 `DTabBar`、`DFileDialog`、`DWaterProgress`、`DSpinBox`、`DSlider` 等不同控件展示典型交互。
- 使用事件循环分块完成大文件读取和内容写入，避免阻塞主线程。
- 使用 CMake 管理源码、资源、翻译和安装规则，并提供 desktop 文件与 Debian 打包配置。

因此，本项目可以作为 `dtk-development` skill 的配套 Demo，用于学习、验证和回归 DTK 应用开发规范，而不是面向生产环境的完整代码查看或编辑产品。

## Skill 覆盖范围

| 方向 | 示例内容 |
|------|----------|
| 应用生命周期 | DApplication、单实例、已有窗口重新激活、应用元数据 |
| 控件与交互 | 标签页、文件对话框、水波加载、消息提示、字号和透明度控制 |
| 主题与视觉 | DCI 图标、系统字体、主题调色板、全窗口模糊和能力回退 |
| 数据与性能 | UTF-8 增量解码、大文件分块读取、文本分块写入 |
| 应用基础设施 | 分类日志、中文翻译、DConfig 配置持久化 |
| 项目工程管理 | CMake 目标、资源组织、翻译生成、安装规则、desktop 和 Debian 包 |
| 质量验证 | 构建检查、安装内容检查、大文件响应性和加载进度回归 |

## 文档

- [需求说明](https://github.com/linuxdeepin/deepin-skills/blob/master/examples/dtk-codeviewer/docs/requirements.md)
- [概要设计](https://github.com/linuxdeepin/deepin-skills/blob/master/examples/dtk-codeviewer/docs/outline-design.md)
- [详细设计](https://github.com/linuxdeepin/deepin-skills/blob/master/examples/dtk-codeviewer/docs/detailed-design.md)

## 构建

```bash
cmake -S . -B build -DCMAKE_INSTALL_PREFIX=/usr
cmake --build build
```

## Debian 打包

```bash
dpkg-buildpackage -us -uc -b
```
