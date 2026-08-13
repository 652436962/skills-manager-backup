# ColorSelector 取色器

## 1. 概述

ColorSelector 是 DTK 统一颜色系统的核心，作为**附加属性**（attached property）自动跟随控件状态选择对应颜色。它将控件的状态（Normal/Hovered/Pressed/Disabled/Inactive）、当前主题（亮色/暗色）、颜色族（common/crystal）集成在一起，只需在 QML 中定义 `Palette` 调色板属性，即可在 `background`、`contentItem` 等处通过 `ColorSelector` 自动获取当前正确的颜色。

**颜色系统三层架构：**

```
Palette（调色板）→ 控件 Palette 属性 → ColorSelector（取色器）
  定义状态颜色           声明属性名          自动选择当前颜色
```

- **Palette**：定义每种状态（normal、hovered、pressed、disabled）和每种主题（亮色/暗色）下不同颜色族（common/crystal）的颜色
- **控件 Palette 属性**：如 `backgroundColor`、`textColor`，声明为 `property Palette`
- **ColorSelector**：附加属性，读取控件的 Palette 属性，根据当前状态自动返回对应颜色

## 2. ColorSelector 属性

ColorSelector 是附加属性，不可直接创建，仅在控件拥有 `Palette` 属性时自动创建。

| 属性 | 类型 | 读写 | 说明 |
|------|------|------|------|
| `control` | `Item` | 只读 | 绑定的 Control 对象，自动寻找最近的父类 Control |
| `controlTheme` | `enumeration` | 只读 | 当前主题：`ApplicationHelper.LightType` / `DarkType` / `UnknowType` |
| `controlState` | `enumeration` | 只读 | 控件状态：`DTK.NormalState` / `HoveredState` / `PressedState` / `DisabledState` / `InactiveState` |
| `family` | `enumeration` | 读写 | 颜色族：`Palette.CommonColor`（默认） / `Palette.CrystalColor` |
| `hovered` | `bool` | 读写 | 启用/禁用 hovered 状态（未设置时跟随控件） |
| `pressed` | `bool` | 读写 | 启用/禁用 pressed 状态 |
| `disabled` | `bool` | 读写 | 启用/禁用 disabled 状态 |
| `inactived` | `bool` | 读写 | 启用/禁用 inactived 状态 |

**信号：** `colorPropertyChanged(string name)` — ColorSelector 记录的某颜色属性值变化时触发

**颜色族说明：**

| 颜色族 | 枚举值 | 用途 |
|--------|--------|------|
| common | `Palette.CommonColor` | 默认颜色族，用于普通窗口控件 |
| crystal | `Palette.CrystalColor` | 水晶颜色族，用于对话框等半透明背景场景 |

## 3. Palette 调色板

Palette 定义控件每种状态下的颜色。每个状态支持亮色/暗色主题和 common/crystal 颜色族。

### 3.1 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `enabled` | `bool` | 是否启用（默认 true），禁用时取色器向上查找同名 Palette |
| `normal` | `color` / `DQuickControlColor` | Normal 状态颜色（默认亮色主题 common 族） |
| `normalDark` | `color` / `DQuickControlColor` | Normal 状态暗色主题颜色 |
| `hovered` | `color` / `DQuickControlColor` | Hovered 状态颜色 |
| `hoveredDark` | `color` / `DQuickControlColor` | Hovered 状态暗色主题颜色 |
| `pressed` | `color` / `DQuickControlColor` | Pressed 状态颜色 |
| `pressedDark` | `color` / `DQuickControlColor` | Pressed 状态暗色主题颜色 |
| `disabled` | `color` / `DQuickControlColor` | Disabled 状态颜色 |
| `disabledDark` | `color` / `DQuickControlColor` | Disabled 状态暗色主题颜色 |

### 3.2 基本用法

```qml
Palette {
    normal: "red"
    hovered: "green"
    pressed: "blue"
    disabled: "black"
}
```

未指定某状态时，取色器使用 `normal` 状态的颜色。

### 3.3 暗色主题

当亮暗主题颜色不同时，使用 `Dark` 后缀指定暗色值：

```qml
Palette {
    normal: "red"
    normalDark: "black"
    hovered: "green"
    hoveredDark: "yellow"
}
```

### 3.4 颜色族

`Palette` 的每个状态（normal、hovered 等）是 `DQuickControlColor` 类型，支持 QML 分组属性语法 `normal { common: ...; crystal: ... }`，也支持子属性直接赋值 `pressed.crystal: "#cdd6e0"`。

```qml
Palette {
    normal {
        common: "#f0f0f0"
        crystal: Qt.rgba(0.20, 0.2, 0.2, 0.1)
    }
    hovered: "#d2d2d2"             // 仅 common 族，crystal 未设置
    pressed.crystal: "#cdd6e0"     // 仅 crystal 族，common 未设置
}
```

### 3.5 颜色回退（Fallback）机制

当某状态的颜色未设置时，ColorSelector 会按优先级回退查找。以下按状态分类说明：

**一般状态（Normal / Hovered / Pressed）回退链：**

```
指定状态(指定颜色族, 指定主题)
  → 同主题 Normal(指定颜色族)      // 状态回退：如 hovered 未设则取 normal
  → 指定状态(Common 族, 指定主题)  // 颜色族回退：crystal 未设则取 common
  → 同主题 Normal(Common 族)       // 双重回退
```

**Disabled 状态特殊处理：** Disabled 优先使用自身的 Disabled 颜色。若未设置，回退到 Normal 状态，走上述一般回退链。

**暗色主题回退：** 若暗色主题下所有回退均无效，尝试使用亮色主题对应颜色并进行颜色反转（非 Highlight/HighlightedText 类型时），即 `color = QColor(255-r, 255-g, 255-b, a)`。

**Inactive 状态：** 启用 `UseInactiveColorGroup` 属性时，Inactive 状态的颜色会与窗口背景色混合（暗色主题 alpha=0.6，亮色主题 alpha=0.4），模拟未激活窗口的视觉效果。

**示例：** 以下 Palette 中 hovered 只设了 common 族，crystal 族未设：

```qml
Palette {
    normal {
        common: "red"
        crystal: Qt.rgba(0.2, 0.2, 0.2, 0.1)
    }
    hovered: "green"  // 仅 common，crystal 未设置
}
```

当 `ColorSelector.family: Palette.CrystalColor` 且控件处于 hovered 状态时，`hovered.crystal` 未设置，回退链为：
1. `hovered.crystal` → 无效
2. `normal.crystal` → `Qt.rgba(0.2, 0.2, 0.2, 0.1)` ✓

### 3.6 禁用

设置 `enabled: false` 后，取色器忽略此 Palette，向上层 Control 查找同名属性：

```qml
Palette {
    normal: "red"
    enabled: false
}
```

### 3.7 QPalette 适配

```qml
Palette {
    normal: DTK.makeColor(Color.Highlight)
    hovered: DTK.makeColor(Color.Highlight).lightness(+10)
    pressed: DTK.makeColor(Color.Highlight).opacity(-10)
}
```

可用调整方法：`lightness()`、`opacity()`、`saturation()`、`hue()`，取值范围 [-100, +100]。

## 4. 使用 ColorSelector

### 4.1 自定义控件中使用

```qml
Control {
    id: control
    hoverEnabled: true

    property Palette backgroundColor: Palette {
        normal: "red"
        hovered: "green"
    }
    property Palette textColor: Palette {
        normal: "white"
        hovered: "yellow"
    }

    background: Rectangle {
        color: control.ColorSelector.backgroundColor
    }
    contentItem: Text {
        text: "按钮"
        color: control.ColorSelector.textColor
    }
}
```

### 4.2 运行时修改调色板

直接修改 Palette 的状态颜色：

```qml
MouseArea {
    onClicked: {
        rect.backgroundColor.hovered = "yellow"
    }
}
```

替换整个 Palette：

```qml
MouseArea {
    Palette { id: otherPalette; normal: "black"; hovered: "gray" }
    onClicked: {
        rect.backgroundColor = otherPalette
    }
}
```

### 4.3 通过 ColorSelector 覆盖

```qml
// 覆盖
rect.ColorSelector.backgroundColor = otherPalette

// 复原
rect.ColorSelector.backgroundColor = undefined
```

### 4.4 子控件继承父 Control 的调色板

子控件可读取父 Control 的调色板属性：

```qml
Control {
    id: control
    property Palette backgroundColor: Palette {
        normal: "red"
        hovered: "green"
    }

    Rectangle {
        property Palette borderColor: Palette {
            normal: "blue"
            hovered: "yellow"
        }
        // 继承父 Control 的 backgroundColor
        color: ColorSelector.backgroundColor
        // 使用自身的 borderColor
        border.color: ColorSelector.borderColor
    }
}
```

> **注意：** 子控件必须有至少一个 `Palette` 属性，ColorSelector 才会为其创建。子控件仅读取自身和最近父 Control 的调色板。

### 4.5 覆盖已有控件的颜色

```qml
Button {
    text: "按钮"
    textColor: Palette {
        normal: "red"
        hovered: "blue"
    }
}
```

## 5. 状态过滤

ColorSelector 可精确控制哪些状态生效。

### 5.1 仅处理单一状态

```qml
Button {
    text: "Hovered 状态"
    ColorSelector.hovered: true     // 仅处理 hovered
}
```

### 5.2 禁用某状态

```qml
Button {
    text: "禁用 Hovered"
    ColorSelector.hovered: false    // 禁用 hovered
}
```

### 5.3 组合使用

```qml
Button {
    text: "仅 Hovered"
    ColorSelector.hovered: true
    ColorSelector.pressed: false
    ColorSelector.disabled: false
}
```

> **注意：** 状态过滤仅接受直接 bool 赋值，不支持属性绑定。推荐仅启用一种状态。

## 6. 使用 crystal 颜色族

对话框等半透明背景场景中，将 ColorSelector 切换到 crystal 颜色族：

```qml
FloatingPanel {
    backgroundColor: Palette {
        normal {
            common: "#f0f0f0"
            crystal: Qt.rgba(0.20, 0.2, 0.2, 0.1)
        }
        hovered: "#d2d2d2"
        pressed.crystal: "#cdd6e0"
    }

    ColorSelector.family: Palette.CrystalColor

    contentItem: ListView {
        model: 6
        delegate: MenuItem { text: "菜单项" + modelData }
    }
}
```

## 7. 标准控件 Palette 属性对照

| 控件 | 可覆盖的 Palette 属性 |
|------|----------------------|
| `Button` / `FloatingButton` / `WarningButton` | `textColor` |
| `ActionButton` | `textColor` |
| `BoxPanel` / `ButtonPanel` | `color1`, `color2`, `insideBorderColor`, `outsideBorderColor`, `dropShadowColor`, `innerShadowColor1`, `innerShadowColor2` |
| `BusyIndicator` | `fillColor` |
| `ButtonIndicator` | `backgroundColor` |
| `CheckDelegate` | `backgroundColor` |
| `ComboBox` | `separatorColor` |
| `EditPanel` | `backgroundColor`, `alertBackgroundColor` |
| `EmbeddedProgressBar` | `backgroundColor`, `progressBackgroundColor` |
| `FloatingPanel` | `backgroundColor`, `dropShadowColor`, `borderColor` |
| `HighlightPanel` | `backgroundColor`, `outerShadowColor`, `innerShadowColor` |
| `IpV4LineEdit` | `backgroundColor` |
| `ItemDelegate` | `checkedTextColor` |
| `KeySequenceEdit` | `backgroundColor`, `placeholderTextColor` |
| `MenuItem` | `subMenuBackgroundColor`, `itemColor` |
| `Slider` | `grooveColor` |
| `SliderTipItem` | `tickColor`, `textColor` |
| `SpinBoxIndicator` | `inactiveBackgroundColor` |
| `Switch` | `backgroundColor`, `handleColor` |
| `TextField` | `backgroundColor` |
| `TitleBar` | `textColor` |
| `ToolButton` | `textColor` |
| `WaterProgressBar` | `backgroundColor1`, `backgroundColor2`, `dropShadowColor`, `popBackgroundColor`, `textColor` |
| `WindowButton` / `WindowButtonGroup` | `textColor` |

## 8. 相关文档

- [index.md](index.md) — QML 控件选择决策树
- [effects.md](effects.md) — QML 效果组件
