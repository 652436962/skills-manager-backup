## 1. 项目定位

本项目是 `dtk-development` skill 的综合示例。Code Viewer 提供直观的业务场景，便于同时展示 QWidget 控件、主题视觉和大文件处理；应用入口、配置、日志、翻译、单实例、资源安装和 Debian 打包则用于展示 DTK 项目从开发到交付的完整工程结构。

设计时遵循以下原则：

1. 优先使用 DTK 提供的应用接口、控件、图标、字体、主题和配置能力。
2. 不为展示控件而重复使用同一种输入方式，确保 Demo 能覆盖不同控件的适用场景。
3. 界面功能与应用基础设施并重，既能观察 UI 效果，也能参考真实项目组织方式。
4. 对大文件、平台模糊能力、配置缺失和重复启动等边界情况提供可验证的回退行为。

## 2. 总体架构

```text
+--------------------------------------------------+
| DApplication：单实例、翻译、日志、应用元数据       |
+--------------------------------------------------+
| DMainWindow + 全窗口 DBlurEffectWidget            |
|  +--------------------------------------------+  |
|  | DTitlebar                                  |  |
|  +--------------------------------------------+  |
|  | DTabBar：[+] [file1.cpp ×] [file2.h ×]     |  |
|  +--------------------------------------------+  |
|  | CodeView / DPlainTextEdit + 可见行号        |  |
|  |          DWaterProgress（加载时居中）        |  |
|  +--------------------------------------------+  |
|  | DSpinBox 字号 | DSlider 透明度 | DLabel 百分比 |  |
|  +--------------------------------------------+  |
|  | DLabel：文件路径 | 行数 | 文件大小           |  |
|  +--------------------------------------------+  |
+--------------------------------------------------+
```

## 3. 模块划分

| 模块 | 文件 | 职责 |
|------|------|------|
| 应用入口 | main.cpp | 在 DApplication 前设置 appId，初始化单实例、翻译和分类日志 |
| 主窗口 | mainwindow.h/.cpp | 布局、模糊/主题色回退、DConfig 和控件状态 |
| 标签管理 | tabmanager.h/.cpp | 标签增删切换、文件异步分块读取 |
| 代码视图 | codeview.h/.cpp | 分块写入文本、只读编辑器和可见行号绘制 |
| 配置元数据 | configs/*.json | 窗口尺寸、字号和透明度默认值及权限 |
| 翻译资源 | translations/*.ts | 通过 Qt 从源码提取的中英文翻译及 QM 生成输入 |
| 桌面集成 | data/*.desktop | 启动器名称、图标、分类和单实例声明 |
| 工程与打包 | CMakeLists.txt、debian/ | 依赖、资源、翻译、安装路径和 Debian 包管理 |

## 4. 数据流

```text
DTabBar 添加按钮
    -> DFileDialog 选择文件
    -> TabManager 使用 QTimer 分块读取并解码
    -> fileLoadProgress 更新 DWaterProgress
    -> 添加标签并交给 CodeView
    -> CodeView 使用 QTimer 分块写入大文本
    -> contentLoadProgress 更新 DWaterProgress
    -> 状态栏与 DMessageManager 更新

DSpinBox 修改字号
    -> CodeView::setFontSize()
    -> DPlainTextEdit 使用系统等宽字体和对应 pixelSize

DSlider 修改透明度
    -> DBlurEffectWidget::setMaskAlpha() 或主题色回退 alpha
    -> 标题栏和内容区同步变化
```

## 5. 关键技术选型

| 技术点 | 方案 | 理由 |
|--------|------|------|
| 标签管理 | DTabBar | 同时展示添加、移动和关闭标签能力 |
| 字体控制 | DSpinBox | 字号是离散整数，适合精确输入 |
| 透明度控制 | DSlider | 透明度是连续范围，适合快速拖动预览 |
| 加载反馈 | DWaterProgress | 使用 DTK 水波球展示加载状态 |
| 模糊背景 | DBlurEffectWidget + 回退表面 | 按平台能力启停，标题栏和内容区始终共享背景层 |
| 大文件处理 | QTimer 分块读取和写入 | 避免一次性 I/O、解码和文档布局阻塞 |
| 文件对话框 | DFileDialog | 使用 DTK 文件选择控件 |
| 消息与日志 | DMessageManager + DLogManager | 展示应用内提示和日志能力 |
| 配置 | DConfig | 使用 DTK 用户级配置并支持外部 valueChanged |
| 翻译 | Qt Linguist + DApplication::loadTranslator | 按 DTK 应用名和标准安装目录加载本地化资源 |
| 单实例 | DApplication::setSingleInstance | 阻止重复窗口并通知原实例重新激活 |
| 工程管理 | CMake + GNUInstallDirs + debhelper | 统一管理构建、资源、安装和 Debian 打包 |

## 6. CMake 依赖

```text
Qt6::Core
Qt6::Widgets
Qt6::LinguistTools（构建期生成翻译）
Dtk6::Core
Dtk6::Gui
Dtk6::Widget
```
