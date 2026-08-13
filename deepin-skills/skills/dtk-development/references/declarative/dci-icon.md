# QML 中使用 dci 图标

## 1. 概述

在 QML 中使用 dci 图标，可通过 `DciIcon` 组件（对应 C++ 后端 `DQuickDciIconImage`）。

## 2. 属性速查

| 属性 | 类型 | 说明 |
|------|------|------|
| `name` | `QString` | dci 图标名称 |
| `mode` | `DQMLGlobalObject::ControlState` | 控件状态：NormalState / HoveredState / PressedState / DisabledState / InactiveState |
| `theme` | `DGuiApplicationHelper::ColorType` | 主题：LightType / DarkType |
| `palette` | `DDciIconPalette` | 图标调色板，用于着色 |
| `sourceSize` | `QSize` | 图标源尺寸 |
| `mirror` | `bool` | 是否镜像翻转 |
| `fallbackToQIcon` | `bool` | 找不到 dci 图标时是否回退到 QIcon |
| `asynchronous` | `bool` | 是否异步加载 |
| `cache` | `bool` | 是否缓存 |
| `retainWhileLoading` | `bool` | 加载期间保留旧图（Qt >= 6.8.0） |
| `fillMode` | `QQuickImage::FillMode` | 填充模式 |

## 3. 使用方式

### 3.1 基本用法

```qml
import org.deepin.dtk 1.0

DciIcon {
    name: "my-icon"
    sourceSize: Qt.size(32, 32)
}
```

### 3.2 在按钮中使用

```qml
import org.deepin.dtk 1.0

Button {
    icon.name: "action-icon"
    icon.width: 24
    icon.height: 24
    text: "操作"
}
```

## 4. 主题与状态

DciIcon 通过设置 `theme` 和 `mode` 属性来响应主题切换和控件状态：

- **`theme`**：`DGuiApplicationHelper.LightType` / `DGuiApplicationHelper.DarkType`，控制图标选择亮/暗主题版本
- **`mode`**：`DQMLGlobalObject.NormalState` / `HoveredState` / `PressedState` / `DisabledState` / `InactiveState`，控制图标选择对应交互状态的渲染
- **`palette`**：通过 `D.DTK.makeIconPalette()` 将 QPalette 转为 DDciIconPalette，使图标颜色与控件配色一致

这些值可以从控件已有的 `icon` 属性获取，也可以结合 [ColorSelector](color-selector.md) 获取控件的当前主题和状态：

```qml
import org.deepin.dtk 1.0

DciIcon {
    palette: D.DTK.makeIconPalette(control.palette)
    mode: control.D.ColorSelector.controlState
    theme: control.D.ColorSelector.controlTheme
    name: control.icon.name
    sourceSize: Qt.size(control.icon.width, control.icon.height)
}
```

如果只需主题切换，可直接设置 theme：

```qml
DciIcon {
    name: "my-icon"
    sourceSize: Qt.size(32, 32)
    theme: DGuiApplicationHelper.LightType
}
```

## 5. 相关文档

- [../theme/dci.md](../theme/dci.md) - dci 图标完整规范
- [color-selector.md](color-selector.md) — ColorSelector 取色器与 Palette 调色板
- [index.md](index.md) - QML 控件选择
