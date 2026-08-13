# DWindowManagerHelper 窗口管理

## 1. 概述与适用场景

`DWindowManagerHelper`（dtkgui）提供窗口管理器相关功能查询和控制。主要用于控制窗口装饰、检测合成器能力。

**适用场景：**
- 检查窗口管理器能力（模糊/合成/无边框）
- 控制窗口按钮和装饰
- 设置窗口类型

## 2. 枚举

### 2.1 MotifFunction

| 值 | 名称 | 说明 |
|----|------|------|
| 1 << 1 | `FUNC_RESIZE` | 可调整大小 |
| 1 << 2 | `FUNC_MOVE` | 可移动 |
| 1 << 3 | `FUNC_MINIMIZE` | 可最小化 |
| 1 << 4 | `FUNC_MAXIMIZE` | 可最大化 |
| 1 << 5 | `FUNC_CLOSE` | 可关闭 |
| — | `FUNC_ALL` | 全部功能 |

### 2.2 MotifDecoration

| 值 | 名称 | 说明 |
|----|------|------|
| 1 << 1 | `DECOR_BORDER` | 边框 |
| 1 << 2 | `DECOR_RESIZEH` | 调整大小手柄 |
| 1 << 3 | `DECOR_TITLE` | 标题栏 |
| 1 << 4 | `DECOR_MENU` | 窗口菜单 |
| 1 << 5 | `DECOR_MINIMIZE` | 最小化按钮 |
| 1 << 6 | `DECOR_MAXIMIZE` | 最大化按钮 |
| — | `DECOR_ALL` | 全部装饰 |

### 2.3 WMName

| 值 | 名称 |
|----|------|
| 0 | `OtherWM` |
| 1 | `DeepinWM` |
| 2 | `KWinWM` |

### 2.4 WmWindowType

| 值 | 名称 | 说明 |
|----|------|------|
| 0x000000 | `UnknowWindowType` | 未知 |
| 0x000001 | `NormalType` | 普通窗口 |
| 0x000002 | `DesktopType` | 桌面 |
| 0x000004 | `DockType` | Dock/面板 |
| 0x000008 | `ToolbarType` | 工具栏 |
| 0x000010 | `MenuType` | 菜单 |
| 0x000020 | `UtilityType` | 工具窗口 |
| 0x000040 | `SplashType` | 启动画面 |
| 0x000080 | `DialogType` | 对话框 |
| 0x000400 | `TooltipType` | 提示 |
| 0x000800 | `NotificationType` | 通知 |

## 3. 核心 API

### 3.1 单例与能力查询

```cpp
#include <DWindowManagerHelper>

auto *wm = DWindowManagerHelper::instance();

// 查询窗口管理器能力
bool hasBlur = wm->hasBlurWindow();       // 是否支持模糊窗口
bool hasComposite = wm->hasComposite();   // 是否有合成器
bool noTitlebar = wm->hasNoTitlebar();    // 是否无标题栏模式

// 窗口管理器名称
DWindowManagerHelper::WMName name = wm->windowManagerName();
QString nameStr = wm->windowManagerNameString();
```

### 3.2 窗口功能控制

```cpp
// 禁用关闭按钮
DWindowManagerHelper::setMotifFunctions(window,
    DWindowManagerHelper::FUNC_CLOSE, false);

// 禁用所有按钮（仅保留关闭）
DWindowManagerHelper::setMotifFunctions(window,
    DWindowManagerHelper::FUNC_RESIZE | DWindowManagerHelper::FUNC_MOVE
    | DWindowManagerHelper::FUNC_CLOSE);

// 查询当前功能
DWindowManagerHelper::MotifFunctions funcs =
    DWindowManagerHelper::getMotifFunctions(window);
```

### 3.3 窗口装饰控制

```cpp
// 移除标题栏
DWindowManagerHelper::setMotifDecorations(window,
    DWindowManagerHelper::DECOR_BORDER | DWindowManagerHelper::DECOR_RESIZEH);

// 查询装饰
DWindowManagerHelper::MotifDecorations decors =
    DWindowManagerHelper::getMotifDecorations(window);
```

### 3.4 窗口类型设置

```cpp
// 设置为 Dock 类型
DWindowManagerHelper::setWmWindowTypes(window,
    DWindowManagerHelper::DockType);

// 设置为通知类型
DWindowManagerHelper::setWmWindowTypes(window,
    DWindowManagerHelper::NotificationType);
```

### 3.5 其他功能

```cpp
// 弹出系统窗口菜单
DWindowManagerHelper::popupSystemWindowMenu(window);

// 设置 WM 类名
DWindowManagerHelper::setWmClassName("my-app");

// 获取所有窗口 ID
QVector<quint32> ids = wm->allWindowIdList();
QVector<quint32> currentIds = wm->currentWorkspaceWindowIdList();
```

## 4. 监听变化

```cpp
connect(wm, &DWindowManagerHelper::hasCompositeChanged, this, [](bool has) {
    // 合成器状态变化
});

connect(wm, &DWindowManagerHelper::hasBlurWindowChanged, this, [](bool has) {
    // 模糊支持变化
});

connect(wm, &DWindowManagerHelper::windowListChanged, this, [this]() {
    // 窗口列表变化
});
```

## 5. QML 用法

```qml
import org.deepin.dtk 1.0

// 查询能力
if (D.WindowManagerHelper.hasComposite) { ... }
if (D.WindowManagerHelper.hasBlurWindow) { ... }
```

## 6. 常见错误与避坑

### 错误 1：在 Wayland 上使用 Motif 功能

```cpp
// MotifFunction/MotifDecoration 仅在 X11 下有效
// Wayland 下应使用 DLayerShellWindow 或其他 Wayland 协议
if (DGuiApplicationHelper::testAttribute(DGuiApplicationHelper::IsXWindowPlatform)) {
    DWindowManagerHelper::setMotifFunctions(window, ...);
}
```

### 错误 2：FUNC_ALL 包含关闭按钮

```cpp
// ❌ 错误：FUNC_ALL 包含关闭，无法禁用所有按钮
DWindowManagerHelper::setMotifFunctions(window, DWindowManagerHelper::FUNC_ALL);

// ✅ 正确：显式指定需要的功能
DWindowManagerHelper::setMotifFunctions(window,
    DWindowManagerHelper::FUNC_RESIZE | DWindowManagerHelper::FUNC_MOVE);
```

## 7. 相关文档

- [gui-helper.md](gui-helper.md) - DGuiApplicationHelper
- [platform-abstraction.md](../platform-abstraction.md) - 平台抽象层
