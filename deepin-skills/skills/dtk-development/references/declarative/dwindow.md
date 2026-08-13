# D.DWindow QML 窗口附加属性

## 1. 概述与适用场景

`DWindow` 是 dtkdeclarative 提供的 QML 附加属性类型。用于在 QML 窗口上设置 DTK 特有的窗口效果（圆角、阴影、模糊、边框等）。

**适用场景：**
- 设置窗口圆角
- 启用窗口模糊
- 设置窗口阴影和边框
- 控制窗口装饰

## 2. 使用方式

`DWindow` 是附加属性，不可直接创建，通过 `DWindow.xxx` 语法在 Window 上使用：

```qml
import org.deepin.dtk 1.0

ApplicationWindow {
    id: window
    visible: true
    width: 800; height: 600

    DWindow.enabled: true
    DWindow.windowRadius: 18
    DWindow.enableBlurWindow: true
    DWindow.shadowColor: Qt.rgba(0, 0, 0, 0.2)
}
```

## 3. 属性

### 3.1 基础属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `enabled` | `bool` | 是否启用 DTK 窗口样式 |
| `windowRadius` | `int` | 窗口圆角半径 |
| `borderWidth` | `int` | 边框宽度 |
| `borderColor` | `QColor` | 边框颜色 |
| `translucentBackground` | `bool` | 是否半透明背景 |

### 3.2 阴影属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `shadowRadius` | `int` | 阴影半径 |
| `shadowOffset` | `QPoint` | 阴影偏移 |
| `shadowColor` | `QColor` | 阴影颜色 |

### 3.3 模糊与系统控制

| 属性 | 类型 | 说明 |
|------|------|------|
| `enableBlurWindow` | `bool` | 启用窗口模糊 |
| `enableSystemResize` | `bool` | 允许系统调整窗口大小 |
| `enableSystemMove` | `bool` | 允许系统移动窗口 |
| `alphaBufferSize` | `int` | Alpha 缓冲区大小 |

### 3.4 窗口类型与装饰

| 属性 | 类型 | 说明 |
|------|------|------|
| `wmWindowTypes` | `WmWindowTypes` | 窗口管理器类型标志 |
| `motifFunctions` | `MotifFunctions` | Motif 功能标志 |
| `motifDecorations` | `MotifDecorations` | Motif 装饰标志 |

### 3.5 主题与效果

| 属性 | 类型 | 说明 |
|------|------|------|
| `themeType` | `ColorType` | 窗口级主题覆盖（Qt6） |
| `windowEffect` | `EffectScenes` | 窗口场景效果 |
| `windowStartUpEffect` | `EffectTypes` | 窗口启动效果 |

### 3.6 其他

| 属性 | 类型 | 说明 |
|------|------|------|
| `clipPath` | `QQuickPath*` | 窗口裁剪路径 |
| `overlayExited` | `QQuickTransition*` | 覆盖层退出过渡 |
| `loadingOverlay` | `QQmlComponent*` | 加载覆盖层组件 |

## 4. 方法

### 4.1 窗口操作

```qml
DWindow.popupSystemWindowMenu()
DWindow.showMinimized()
DWindow.showMaximized()
DWindow.showFullScreen()
DWindow.showNormal()
```

### 4.2 模糊区域

```qml
// 设置矩形模糊区域
DWindow.setWindowBlurAreaByWM(areas)

// 设置路径模糊区域
DWindow.setWindowBlurAreaByWM(pathList)

// 设置裁剪路径
DWindow.setClipPathByWM(clipPath)
```

## 5. 典型用法

### 5.1 标准主窗口

```qml
ApplicationWindow {
    DWindow.enabled: true
    DWindow.windowRadius: 18
    DWindow.enableBlurWindow: false
    DWindow.shadowColor: Qt.rgba(0, 0, 0, 0.15)
    DWindow.shadowOffset: Qt.point(0, 4)
}
```

### 5.2 模糊窗口

```qml
ApplicationWindow {
    DWindow.enabled: true
    DWindow.windowRadius: 18
    DWindow.enableBlurWindow: true
    DWindow.translucentBackground: true
}
```

### 5.3 无边框工具窗口

```qml
ApplicationWindow {
    flags: Qt.Tool | Qt.FramelessWindowHint
    DWindow.enabled: true
    DWindow.windowRadius: 8
    DWindow.enableSystemMove: true
    DWindow.enableSystemResize: true
}
```

### 5.4 窗口级主题覆盖（Qt6）

```qml
ApplicationWindow {
    DWindow.themeType: ApplicationHelper.DarkType
    // 重置为跟随系统
    // DWindow.themeType: undefined
}
```

## 6. EffectScene 标志

| 值 | 名称 | 说明 |
|----|------|------|
| 0x01 | `EffectNoRadius` | 无圆角 |
| 0x02 | `EffectNoShadow` | 无阴影 |
| 0x04 | `EffectNoBorder` | 无边框 |
| 0x10 | `EffectNoStart` | 无启动动画 |
| 0x20 | `EffectNoClose` | 无关闭动画 |
| 0x40 | `EffectNoMaximize` | 无最大化动画 |
| 0x80 | `EffectNoMinimize` | 无最小化动画 |

## 7. 信号

| 信号 | 说明 |
|------|------|
| `enabledChanged()` | 启用状态变化 |
| `windowRadiusChanged()` | 圆角变化 |
| `borderWidthChanged()` | 边框宽度变化 |
| `borderColorChanged()` | 边框颜色变化 |
| `shadowRadiusChanged()` | 阴影半径变化 |
| `shadowOffsetChanged()` | 阴影偏移变化 |
| `shadowColorChanged()` | 阴影颜色变化 |
| `translucentBackgroundChanged()` | 半透明背景变化 |
| `enableSystemResizeChanged()` | 系统调整大小变化 |
| `enableSystemMoveChanged()` | 系统移动变化 |
| `enableBlurWindowChanged()` | 模糊启用变化 |
| `alphaBufferSizeChanged()` | Alpha 缓冲区变化 |
| `clipPathChanged()` | 裁剪路径变化 |
| `wmWindowTypesChanged()` | 窗口类型变化 |
| `motifFunctionsChanged()` | Motif 功能变化 |
| `motifDecorationsChanged()` | Motif 装饰变化 |
| `overlayExitedChanged()` | 覆盖层退出变化 |
| `loadingOverlayChanged()` | 加载覆盖层变化 |
| `themeTypeChanged()` | 主题类型变化 |
| `windowEffectChanged()` | 窗口效果变化 |
| `windowStartUpEffectChanged()` | 启动效果变化 |

## 8. 常见错误与避坑

### 错误 1：忘记设置 DWindow.enabled

```qml
// ❌ 错误：未启用 DTK 窗口样式
ApplicationWindow {
    DWindow.windowRadius: 18  // 不生效
}

// ✅ 正确：先启用
ApplicationWindow {
    DWindow.enabled: true
    DWindow.windowRadius: 18
}
```

### 错误 2：模糊窗口未设置半透明背景

```qml
// ❌ 错误：模糊效果可能不正确
DWindow.enableBlurWindow: true

// ✅ 正确：同时设置半透明背景
DWindow.enableBlurWindow: true
DWindow.translucentBackground: true
```

## 9. 相关文档

- [dtk-global.md](dtk-global.md) - D.DTK 全局对象
- [dialogs.md](dialogs.md) - QML 对话框与窗口
- [effects.md](effects.md) - QML 视觉效果
- [../utilities/window-manager.md](../utilities/window-manager.md) - 窗口管理助手
