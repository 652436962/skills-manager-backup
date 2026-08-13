# LayerShell 使用

`DLayerShellWindow` 是 dde-shell 提供的 Wayland `wlr-layer-shell` QML 接口，可独立于插件体系使用。

**导入**: `import org.deepin.ds 1.0`

## DLayerShellWindow

QML 附加属性，附加在 `Window` 上。

### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `anchors` | `Anchors` | 锚定屏幕边缘（位或组合） |
| `layer` | `Layer` | 窗口层级（Background/Buttom/Top/Overlay） |
| `leftMargin` | `int` | 左边距 |
| `rightMargin` | `int` | 右边距 |
| `topMargin` | `int` | 上边距 |
| `bottomMargin` | `int` | 下边距 |
| `exclusionZone` | `int32` | 排除区域大小，阻止其他窗口覆盖 |
| `keyboardInteractivity` | `KeyboardInteractivity` | 键盘交互模式 |
| `scope` | `QString` | 窗口标识，用于同层排序 |
| `screenConfiguration` | `ScreenConfiguration` | 屏幕选择策略 |
| `closeOnDismissed` | `bool` | 被 compositor 关闭时是否销毁窗口 |
| `preferredWidth` | `int` | 首选宽度（可 reset） |
| `preferredHeight` | `int` | 首选高度（可 reset） |
| `inputRegion` | `QRegion` | 输入区域 |

### Anchor 枚举

| 值 | 说明 |
|---|------|
| `AnchorNone = 0` | 无锚定 |
| `AnchorTop = 1` | 顶部 |
| `AnchorBottom = 2` | 底部 |
| `AnchorLeft = 4` | 左侧 |
| `AnchorRight = 8` | 右侧 |

位或组合使用。

### Layer 枚举

| 值 | 说明 |
|---|------|
| `LayerBackground = 0` | 背景层 |
| `LayerButtom = 1` | 底层 |
| `LayerTop = 2` | 顶层 |
| `LayerOverlay = 3` | 覆盖层 |

### KeyboardInteractivity 枚举

| 值 | 说明 |
|---|------|
| `KeyboardInteractivityNone = 0` | 不响应键盘 |
| `KeyboardInteractivityExclusive = 1` | 独占键盘 |
| `KeyboardInteractivityOnDemand = 2` | 按需获取键盘焦点 |

### 使用示例

**底部面板**:
```qml
import org.deepin.ds 1.0

Window {
    visible: true; height: 50
    DLayerShellWindow.anchors: DLayerShellWindow.AnchorBottom
        | DLayerShellWindow.AnchorLeft
        | DLayerShellWindow.AnchorRight
    DLayerShellWindow.layer: DLayerShellWindow.LayerTop
    DLayerShellWindow.exclusionZone: 50
}
```

**顶栏**:
```qml
DLayerShellWindow.anchors: DLayerShellWindow.AnchorTop
    | DLayerShellWindow.AnchorLeft | DLayerShellWindow.AnchorRight
```

**侧栏**:
```qml
DLayerShellWindow.anchors: DLayerShellWindow.AnchorTop
    | DLayerShellWindow.AnchorBottom | DLayerShellWindow.AnchorLeft
```

**浮动覆盖层（不占排除区域）**:
```qml
Window {
    visible: true
    DLayerShellWindow.anchors: DLayerShellWindow.AnchorBottom | DLayerShellWindow.AnchorRight
    DLayerShellWindow.layer: DLayerShellWindow.LayerOverlay
    DLayerShellWindow.keyboardInteractivity: DLayerShellWindow.KeyboardInteractivityOnDemand
}
```

## 独立使用（非插件场景）

不依赖 dde-shell 插件体系，直接使用 LayerShell 窗口。

### QML 方式

```qml
import org.deepin.ds 1.0

Window {
    DLayerShellWindow.anchors: DLayerShellWindow.AnchorBottom
        | DLayerShellWindow.AnchorLeft | DLayerShellWindow.AnchorRight
}
```

### C++ 方式

通过 `DLayerShellWindow::get()` 直接操作已有 `QWindow`：

```cpp
#include <dlayershellwindow.h>
DS_USE_NAMESPACE

auto window = new QQuickWindow();
window->setVisible(true);

auto *shell = DLayerShellWindow::get(window);
shell->setAnchors(DLayerShellWindow::AnchorBottom
    | DLayerShellWindow::AnchorLeft
    | DLayerShellWindow::AnchorRight);
shell->setLayer(DLayerShellWindow::LayerTop);
shell->setExclusiveZone(50);
```

C++ 方式同样链接 `Dde::Shell`，不依赖 QML 导入。

## 实现

- Wayland 端: `wlr-layer-shell-unstable-v1.xml` 协议
- X11 端: `x11dlayershellemulation.cpp` 回退模拟

**关键源文件**: `frame/layershell/dlayershellwindow.h/cpp`
