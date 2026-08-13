# 平台抽象层

## 1. 概述

DTK 平台抽象层将窗口装饰操作和主题配置抽象为跨平台接口，使应用无需关心底层运行在 X11、Wayland（kwayland）还是 Treeland 合成器上。

**两层架构：**

```
dtkgui 层（平台抽象，公共 API）
  DPlatformHandle（窗口操作）   DPlatformTheme（主题配置）
         ↓                              ↓
  DPlatformWindowInterface      DPlatformInterface
    （抽象基类/虚函数）            （抽象基类/虚函数）
         ↓                              ↓
  DXCB* / DTreeLand*            DXCB* / DTreeland*
    （平台具体实现）                （平台具体实现）

QPA 插件层
  DPlatformIntegration（X11 QPA）   DWaylandIntegration（Wayland QPA）
    → 提供底层窗口系统集成            → 提供底层窗口系统集成
```

## 2. DPlatformHandle — 窗口操作

`DPlatformHandle` 是窗口操作的公共入口，每个 `QWindow` 对应一个实例。提供圆角、阴影、边框、模糊、无标题栏等跨平台窗口装饰能力。

### 2.1 头文件与构造

```cpp
#include <DPlatformHandle>

// 为 QWindow 启用 DTK 平台窗口装饰
DPlatformHandle *handle = new DPlatformHandle(window, window);

// 或直接创建（构造时自动关联 window）
DPlatformHandle handle(window);
```

构造时自动根据当前平台（`IsXWindowPlatform` / `IsWaylandPlatform`）创建对应的 `DPlatformWindowInterface` 实现。

### 2.2 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `windowRadius` | `int` | 窗口圆角半径 |
| `borderWidth` | `int` | 边框宽度 |
| `borderColor` | `QColor` | 边框颜色 |
| `shadowRadius` | `int` | 阴影半径 |
| `shadowOffset` | `QPoint` | 阴影偏移 |
| `shadowColor` | `QColor` | 阴影颜色 |
| `clipPath` | `QPainterPath` | 窗口裁剪路径 |
| `frameMask` | `QRegion` | 窗口区域遮罩 |
| `frameMargins` | `QMargins` | 窗口装饰边距（只读） |
| `translucentBackground` | `bool` | 半透明背景 |
| `enableSystemResize` | `bool` | 启用系统级窗口缩放 |
| `enableSystemMove` | `bool` | 启用系统级窗口移动 |
| `enableBlurWindow` | `bool` | 启用窗口模糊效果 |
| `autoInputMaskByClipPath` | `bool` | 根据 clipPath 自动设置输入遮罩 |
| `realWindowId` | `WId` | 实际窗口 ID（只读） |

### 2.3 EffectScene 窗口动效

| 枚举 | 说明 |
|------|------|
| `EffectNoRadius` | 取消窗口圆角 |
| `EffectNoShadow` | 取消窗口阴影 |
| `EffectNoBorder` | 取消窗口边框 |
| `EffectNoStart` | 取消启动场景动效 |
| `EffectNoClose` | 取消关闭场景动效 |
| `EffectNoMaximize` | 取消最大化场景动效 |
| `EffectNoMinimize` | 取消最小化场景动效 |

### 2.4 EffectType 启动动效

| 枚举 | 说明 |
|------|------|
| `EffectNormal` | 标准缩放动效 |
| `EffectCursor` | 鼠标位置展开动效 |
| `EffectTop` | 从上往下展开 |
| `EffectBottom` | 从下往上展开 |
| `EffectOut` | 由外向内 |

### 2.5 窗口模糊

```cpp
#include <DPlatformHandle>

// 方式一：矩形区域模糊
DPlatformHandle::WMBlurArea area = dMakeWMBlurArea(0, 0, 200, 100, 8, 8);
DPlatformHandle::setWindowBlurAreaByWM(window, {area});

// 方式二：路径区域模糊
QPainterPath path;
path.addRoundedRect(QRectF(0, 0, 200, 100), 8, 8);
DPlatformHandle::setWindowBlurAreaByWM(window, {path});

// 方式三：通过 handle 实例
handle->setWindowBlurAreaByWM({path});
```

### 2.6 无标题栏窗口（CSD）

```cpp
#include <DPlatformHandle>

// 启用无标题栏模式（客户端自绘标题栏）
DPlatformHandle::setEnabledNoTitlebarForWindow(window, true);

// 检查是否已启用
bool noTitlebar = DPlatformHandle::isEnabledNoTitlebar(window);
```

### 2.7 静态工具方法

```cpp
// 为窗口启用 DXCB 平台支持
DPlatformHandle::enableDXcbForWindow(window);
DPlatformHandle::enableDXcbForWindow(window, true);  // redirectContent

// 检查平台
bool isDxcb = DPlatformHandle::isDXcbPlatform();
bool isEnabled = DPlatformHandle::isEnabledDXcb(window);
```

## 3. DPlatformTheme — 主题配置

`DPlatformTheme` 提供系统级主题配置访问，包括字体、颜色、图标主题、光标等设置。

### 3.1 头文件与获取

```cpp
#include <DPlatformTheme>
#include <DGuiApplicationHelper>

// 获取应用主题
DPlatformTheme *theme = DGuiApplicationHelper::instance()->applicationTheme();
```

### 3.2 字体配置

| 属性 | 类型 | 说明 |
|------|------|------|
| `fontName` | `QByteArray` | 系统字体名称 |
| `monoFontName` | `QByteArray` | 等宽字体名称 |
| `fontPointSize` | `qreal` | 字体大小（pt） |
| `gtkFontName` | `QByteArray` | GTK 字体名称（如 "Noto Sans 10"） |

### 3.3 主题与颜色

| 属性 | 类型 | 说明 |
|------|------|------|
| `themeName` | `QByteArray` | 主题名称 |
| `iconThemeName` | `QByteArray` | 图标主题名称 |
| `soundThemeName` | `QByteArray` | 声音主题名称 |
| `activeColor` | `QColor` | 活跃色（强调色） |
| `darkActiveColor` | `QColor` | 暗色主题活跃色 |
| `windowRadius` | `int` | 窗口圆角（系统默认值） |

### 3.4 输入配置

| 属性 | 类型 | 说明 |
|------|------|------|
| `cursorBlinkTime` | `int` | 光标闪烁时间 |
| `cursorBlinkTimeout` | `int` | 光标闪烁超时 |
| `cursorBlink` | `bool` | 光标是否闪烁 |
| `doubleClickDistance` | `int` | 双击距离阈值 |
| `doubleClickTime` | `int` | 双击时间阈值 |
| `dndDragThreshold` | `int` | 拖拽阈值 |

### 3.5 大小模式

| 属性 | 类型 | 说明 |
|------|------|------|
| `sizeMode` | `int` | 大小模式（NormalMode/CompactMode） |
| `scrollBarPolicy` | `int` | 滚动条策略 |

## 4. 平台分发机制

### 4.1 窗口接口分发

`DPlatformHandle` 构造时调用 `createWindowInterface()`（`dplatformhandle.cpp:307-328`）：

```
DPlatformHandle(window)
  → OutsideWindowInterfaceCreator（外部注册，优先级最高）
  → DGuiApplicationHelper::IsXWindowPlatform
    → DXCBPlatformWindowInterface（X11，dxcb 协议）
  → DGuiApplicationHelper::IsWaylandPlatform
    → DTreeLandPlatformWindowInterface（Treeland，Wayland personalization 协议）
  → DPlatformWindowInterface（空实现，无平台特效）
```

### 4.2 主题接口分发

`DPlatformTheme` 构造时类似分发：

```
DPlatformTheme(window)
  → IsWaylandPlatform → DTreelandPlatformInterface
  → IsXWindowPlatform → DXCBPlatformInterface
```

## 5. 平台实现详情

### 5.1 X11 实现

| 类 | 项目 | 文件 | 说明 |
|----|------|------|------|
| `DXCBPlatformWindowInterface` | dtkgui | `src/plugins/platform/xcb/dxcbplatformwindowinterface.h` | X11 窗口操作（圆角、阴影、模糊、无标题栏） |
| `DXCBPlatformInterface` | dtkgui | `src/plugins/platform/xcb/dxcbplatforminterface.h` | X11 主题配置（通过 XSettings 原子） |
| `DNoTitlebarWindowHelper` | dde-qtplatform-plugins | `xcb/dnotitlebarwindowhelper.h` | 无标题栏窗口拖拽移动实现 |

通过 X11 原子协议（`_DEEPIN_SCISSOR_WINDOW` 等）与合成器通信。

**窗口拖拽：** X11 下由 QPA 插件中的 `DNoTitlebarWindowHelper` 实现。它通过 `DVtableHook` 钩入 `QWindow::event`，拦截鼠标事件后发送 `_NET_WM_MOVERESIZE_MOVE` 客户端消息至窗口管理器完成窗口移动。

### 5.2 Treeland 实现（dtkgui）

| 类 | 文件 | 说明 |
|----|------|------|
| `DTreeLandPlatformWindowInterface` | `src/plugins/platform/treeland/dtreelandplatformwindowinterface.h` | Treeland 窗口操作 |
| `DTreelandPlatformInterface` | `src/plugins/platform/treeland/dtreelandplatforminterface.h` | Treeland 主题配置 |
| `MoveWindowHelper` | `src/plugins/platform/treeland/dtreelandplatformwindowinterface.cpp` | 无标题栏窗口拖拽移动实现 |

通过 Wayland 协议 `treeland_personalization_manager_v1` 与 Treeland 合成器通信：
- `PersonalizationWindowContext` — 窗口级设置（titlebar、圆角、模糊）
- `PersonalizationAppearanceContext` — 外观设置（图标主题、活跃色、窗口主题）
- `PersonalizationFontContext` — 字体设置（font、monospace_font、font_size）

**窗口拖拽：** Treeland 下由 `dtkgui` 中的 `MoveWindowHelper` 实现。它同样通过 `DVtableHook` 钩入 `QWindow::event`，拦截鼠标事件后调用 `QPlatformWindow::startSystemMove()` 由合成器接管窗口移动。

### 5.3 QPA 层（dde-qtplatform-plugins）

| 类 | 源码路径 | 说明 |
|----|----------|------|
| `DPlatformIntegration` | `xcb/` | 扩展 `QXcbIntegration`，提供 DFrameWindow（阴影/边框/圆角窗口装饰）、窗口事件钩子、HiDPI |
| `DWaylandIntegration` | `wayland/dwayland/` | 扩展 `QWaylandIntegration`，提供 deepin Wayland 集成 |
| `DWaylandShellManager` | `wayland/wayland-shell/` | KWayland Shell 协议管理（plasma shell、SSD、模糊、dock strut） |

## 6. 典型使用场景

### 6.1 自定义窗口圆角和阴影

```cpp
#include <DPlatformHandle>
#include <QQuickView>

QQuickView view;
view.setColor(QColor(Qt::transparent));
view.setFlags(Qt::FramelessWindowHint);

DPlatformHandle handle(&view);
handle.setWindowRadius(18);
handle.setShadowRadius(60);
handle.setShadowOffset(QPoint(0, 10));
handle.setShadowColor(QColor(0, 0, 0, 50));
handle.setBorderWidth(1);
handle.setBorderColor(QColor(0, 0, 0, 25));
handle.setEnableSystemResize(true);
handle.setEnableSystemMove(true);
```

### 6.2 窗口模糊效果

```cpp
#include <DPlatformHandle>

DPlatformHandle handle(window);
handle.setEnableBlurWindow(true);

// 设置模糊区域（标题栏区域）
QPainterPath blurPath;
blurPath.addRect(0, 0, window->width(), 40);
handle.setWindowBlurAreaByWM({blurPath});
```

### 6.3 读取系统主题配置

```cpp
#include <DPlatformTheme>
#include <DGuiApplicationHelper>

auto theme = DGuiApplicationHelper::instance()->applicationTheme();
qDebug() << "Font:" << theme->fontName() << theme->fontPointSize();
qDebug() << "Icon theme:" << theme->iconThemeName();
qDebug() << "Active color:" << theme->activeColor();
qDebug() << "Window radius:" << theme->windowRadius();

// 监听变化
connect(theme, &DPlatformTheme::fontNameChanged, []() {
    qDebug() << "System font changed";
});
connect(theme, &DPlatformTheme::activeColorChanged, []() {
    qDebug() << "Active color changed";
});
```

### 6.4 检测当前平台

```cpp
#include <DGuiApplicationHelper>

auto helper = DGuiApplicationHelper::instance();

if (helper->testAttribute(DGuiApplicationHelper::IsWaylandPlatform)) {
    // 运行在 Wayland/Treeland
} else if (helper->testAttribute(DGuiApplicationHelper::IsXWindowPlatform)) {
    // 运行在 X11
}
```

## 7. 数据流全景

```
系统配置 (DConf/GSettings)
    │
    ▼
DThemeSettings
    │ 读取字体/主题/颜色配置
    ▼
DPlatformTheme (dtkgui)
    │ fontNameChanged / activeColorChanged 等信号
    ├──► QDeepinTheme::font() → QGuiApplication::setFont()
    │      → DGuiApplicationHelper::fontChanged
    │      → DFontManager → t1()-t11() 字体层级
    │
    └──► DPalette 颜色更新
           → DGuiApplicationHelper::themeTypeChanged
           → DStyleHelper 自动选择状态颜色（Widget）
           → ColorSelector 自动更新颜色属性（QML）

平台窗口 (X11 / Wayland / Treeland)
    │
    ▼
DPlatformHandle (dtkgui)
    │ 平台分发 → DXCB* / DTreeLand*
    │
    ├──► X11: dxcb 协议 (_DEEPIN_SCISSOR_WINDOW 等)
    │      → DPlatformIntegration (QPA 插件)
    │      → DFrameWindow (阴影/边框/圆角装饰窗口)
    │
  └──► Treeland: treeland_personalization_manager_v1 协议
         → PersonalizationWindowContext (窗口级设置)
         → PersonalizationAppearanceContext (外观设置)

窗口拖拽 (enableSystemMove)
  │
  ├─► X11: DNoTitlebarWindowHelper (QPA 插件)
  │      → vtHook QWindow::event 拦截 MousePress/Move
  │      → Utility::startWindowSystemMove()
  │      → _NET_WM_MOVERESIZE_MOVE X11 ClientMessage
  │
  ├─► dwayland: DNoTitlebarWlWindowHelper (QPA 插件)
  │      → vtHook QWindow::event 拦截 MousePress/Move
  │      → QWaylandWindow::startSystemMove()
  │
  └─► Treeland: MoveWindowHelper (dtkgui)
         → vtHook QWindow::event 拦截 MousePress/Move
         → QPlatformWindow::startSystemMove()
```

## 8. 相关文档

- [architecture.md](architecture.md) — DTK 核心架构总览
- [theme/index.md](theme/index.md) — 主题系统（含图标、调色板、字体）
