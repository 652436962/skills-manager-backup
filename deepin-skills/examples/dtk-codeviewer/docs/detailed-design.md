dtk-codeviewer 是 `dtk-development` skill 的综合开发示例。界面部分用于展示 DTK 控件和主题能力，应用入口与工程文件用于展示单实例、日志、翻译、配置、资源组织、系统安装及 Debian 打包。项目以规范演示和回归验证为主要目的，不定位为完整代码编辑器。

## 1. 文件结构

```text
dtk-codeviewer/
├── CMakeLists.txt
├── configs/
├── data/
│   └── org.deepin.dtk.codeviewer.desktop
├── debian/
├── docs/
├── resources/
│   ├── icons.qrc
│   └── icons/
├── translations/
│   ├── dtk-codeviewer_en.ts
│   └── dtk-codeviewer_zh_CN.ts
└── src/
    ├── main.cpp
    ├── mainwindow.h/.cpp
    ├── tabmanager.h/.cpp
    └── codeview.h/.cpp
```

## 2. 类设计

### 2.1 MainWindow

继承 `DMainWindow`，负责窗口级视觉效果、控件布局、信号协调和设置持久化。

**主要成员：**

| 变量 | 类型 | 说明 |
|------|------|------|
| m_windowBlur | DBlurEffectWidget* | 覆盖整个窗口的统一模糊层 |
| m_fallbackSurface | FallbackSurface* | 无模糊能力时覆盖整个窗口的主题色表面 |
| m_backgroundSurface | QWidget* | 承载标签栏、编辑区和底部区域 |
| m_tabBar | DTabBar* | 文件标签及添加按钮 |
| m_tabManager | TabManager* | 标签和文件加载管理器 |
| m_codeView | CodeView* | 代码内容视图 |
| m_spinFont | DSpinBox* | 10px～24px 字体输入 |
| m_sliderOpacity | DSlider* | 0%～100% 模糊遮罩透明度 |
| m_opacityLabel | DLabel* | 当前透明度百分比 |
| m_loadProgress | DWaterProgress* | 居中的水波加载提示 |
| m_statusLabel | DLabel* | 当前文件状态 |
| m_config | DConfig* | 窗口尺寸、字号和透明度配置 |

**关键方法：**

| 方法 | 说明 |
|------|------|
| setupUI() | 创建统一模糊层和内容布局 |
| setupConnections() | 连接标签、加载和控制控件信号 |
| setupTitlebar() | 设置标题、图标、主题菜单和透明背景 |
| onOpenFile() | 非阻塞打开 DFileDialog |
| onFontSizeChanged(int) | 将 DSpinBox 值应用到 CodeView |
| onOpacityChanged(int) | 更新模糊遮罩和百分比标签 |
| updateWindowEffects() | 根据合成器和模糊能力切换模糊层或回退表面 |
| applySurfaceOpacity(int) | 将 0～100 映射为模糊 maskAlpha 和回退表面 alpha |
| showLoadingIndicator() | 显示并启动 DWaterProgress |
| tryHideLoadingIndicator() | 文件与内容加载均结束后隐藏提示 |
| resizeEvent() | 保持模糊层覆盖整个窗口 |
| saveWindowState()/restoreWindowState() | 保存和恢复尺寸、字号、透明度 |

### 2.2 TabManager

继承 `QObject`，管理 `FileTab` 数据、标签状态以及文件读取。

```cpp
struct FileTab {
    QString filePath;
    QString fileName;
    QString content;
    int lineCount;
    qint64 fileSize;
};
```

文件通过 256 KiB 分块读取，使用 `QStringDecoder::Utf8` 增量解码。每次 `QTimer` 超时只处理一个分块，让主事件循环有机会继续绘制和响应输入。

**关键接口和信号：**

| 名称 | 说明 |
|------|------|
| addTab(const QString&) | 开始读取文件或切换到已打开标签 |
| removeTab(int) | 删除标签及其缓存 |
| isLoading() | 判断是否正在读取文件 |
| fileLoadStarted | 通知主窗口显示加载提示 |
| fileLoadProgress | 报告文件读取百分比 |
| fileOpened / fileOpenFailed | 报告打开结果 |
| fileLoadFinished | 通知文件读取结束 |

### 2.3 CodeView

继承 `QWidget`，内部使用只读 `DPlainTextEdit`。

- 小于等于 1 MiB 的文本直接设置。
- 大文本按 64 KiB 分块插入文档。
- 字体优先使用 `DPlatformTheme::monoFontName`，回退到系统固定宽度字体，并通过 `QFont::setPixelSize()` 应用 DSpinBox 值。
- 系统字体或等宽字体变化时重新应用字体族，同时保留用户字号。
- 编辑器背景 alpha 设置为 0，透出窗口统一模糊层。
- 行号区域只遍历并绘制当前可见文本块，避免为大文件创建大量子控件。

## 3. 布局设计

```text
+--------------------------------------------------+
| DTitlebar                                        |
+--------------------------------------------------+
| DTabBar [+] [file1.cpp ×] [file2.h ×]            |
+--------------------------------------------------+
| 行号 | DPlainTextEdit                             |
|      |              DWaterProgress                |
+--------------------------------------------------+
| 字体图标 | DSpinBox 14 px | Opacity | DSlider | 80% |
+--------------------------------------------------+
| 文件路径 | 行数 | 文件大小                        |
+--------------------------------------------------+
```

字体和透明度刻意使用不同控件：

- `DSpinBox`：适合离散、需要精确输入的像素字号。
- `DSlider`：适合连续拖动并即时预览的透明度。

## 4. 交互流程

### 4.1 打开文件

```text
点击 DTabBar 添加按钮
    -> DFileDialog 选择文件
    -> TabManager 分块读取
    -> DWaterProgress 使用 0%～50% 显示读取进度
    -> 新建标签
    -> CodeView 分块写入大文本
    -> 同一个 DWaterProgress 使用 50%～100% 显示内容写入进度
    -> 更新状态和操作提示
```

### 4.2 关闭与切换标签

```text
DTabBar::tabCloseRequested
    -> TabManager::removeTab()
    -> 没有标签时清空 CodeView 和状态栏

DTabBar::currentChanged
    -> TabManager::tabChanged
    -> CodeView 显示对应缓存内容
```

### 4.3 字体与透明度

```text
DSpinBox::valueChanged
    -> CodeView::setFontSize()

DSlider::valueChanged
    -> MainWindow::applySurfaceOpacity()
    -> DBlurEffectWidget::setMaskAlpha()
```

## 5. 图标与主题

- 应用图标使用 `dtk-codeviewer.dci`，开发运行时按 DTK 规范放置在 Qt 资源路径 `:/dsg/built-in-icons/dtk-codeviewer.dci`，安装包同时安装到系统路径 `/usr/share/dsg/icons/dtk-codeviewer.dci`。应用通过 `DIconTheme::findQIcon("dtk-codeviewer")` 加载，不注册自定义 DCI 搜索路径，由 DTK 默认路径和 DCI 引擎自动处理主题及尺寸。
- 文件打开成功、错误和字体提示图标通过 `DIconTheme` 查找；builtin 名称不携带尺寸后缀。
- `DTitlebar` 保留系统窗口按钮和主题切换菜单，不添加重复的打开、关闭按钮。
- `DBlurEffectWidget` 使用 `AutoColor` 和系统窗口圆角；无合成器或模糊能力时改用主题色回退表面。
- DConfig 元数据安装到 `share/dsg/configs/org.deepin.dtk.codeviewer/`，不可用时只记录一次警告并使用默认值。
- 日志按 application、configuration、fileload 分类，并同时支持控制台和文件 appender。
- CMake 通过 Qt `qt_add_translations()` 提供 `update_translations` 和 `release_translations` 目标，从源码更新中英文 TS，并生成对应 QM。
- `DApplication::loadTranslator()` 根据可执行文件名 `dtk-codeviewer` 加载翻译，QM 安装到 `/usr/share/dtk-codeviewer/translations/`。
- 文件日志使用 `DLogManager` 默认路径，不由应用设置或创建自定义日志目录。

## 6. 安装与 Debian 打包

- `cmake --install` 安装可执行文件到 `${CMAKE_INSTALL_BINDIR}`，desktop 文件到 `${CMAKE_INSTALL_DATADIR}/applications`，DCI 图标到 `${CMAKE_INSTALL_DATADIR}/dsg/icons`，翻译到 `${CMAKE_INSTALL_DATADIR}/dtk-codeviewer/translations`。
- 在 Debian 系统中执行 `dpkg-buildpackage -us -uc -b`，`debian/rules` 会调用 CMake 安装规则生成 `dtk-codeviewer` 二进制包。
- desktop 文件的 `Icon=dtk-codeviewer` 与系统 DCI 文件名一致，桌面环境通过 DTK DCI 主题路径按当前主题和尺寸加载图标。

## 7. 回归关注点

1. 窗口中只有透明度控制使用 `DSlider`，字体控制必须是 `DSpinBox`。
2. 模糊层 geometry 始终等于窗口 rect。
3. 编辑器背景保持透明，标题栏和内容区视觉一致。
4. 加载大文件时 `setContent()` 快速返回，事件循环持续产生心跳。
5. DWaterProgress 在文件读取和内容写入均完成后才隐藏。
6. 打开文件时水波控件只启动并显示一次，读取和内容写入阶段的进度连续递增，不从 100% 重置为 0%。
7. 无模糊能力时回退表面覆盖范围仍等于窗口 rect，内容保持可读。
8. DConfig 有效时保存并响应外部变化，无效时使用内置默认值。
