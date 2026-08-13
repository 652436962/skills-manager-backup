# 进度与滑动控件

## 1. 概述与适用场景

DTK QML 提供进度指示和滑动控件，用于显示进度和数值调节。

**适用场景：**
- 进度条 → `ProgressBar`
- 水波进度 → `WaterProgressBar`
- 滑动条 → `Slider`
- 忙碌指示 → `BusyIndicator`

**相关组件：**
- `ProgressBar` — 进度条
- `WaterProgressBar` — 水波进度
- `Slider` — 滑动条
- `BusyIndicator` — 忙碌指示器

## 2. ProgressBar

进度条，继承 `T.ProgressBar`。使用内部 `ProgressBarImpl` 和 `ProgressBarPanel` 渲染。

```qml
ProgressBar {
    from: 0; to: 100
    value: 75
    formatText: "%p%"
}
```

## 2. EmbeddedProgressBar

嵌入式小进度条，继承 `T.ProgressBar`。默认 48x6 尺寸，适合在列表项或小块区域使用。支持 `backgroundColor` 和 `progressBackgroundColor` 调色板。

```qml
EmbeddedProgressBar {
    value: 0.5
    backgroundColor: Palette { normal: "#eee" }
    progressBackgroundColor: Palette { normal: "blue" }
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `backgroundColor` | `Palette` | 轨道背景颜色 |
| `progressBackgroundColor` | `Palette` | 进度条背景颜色 |

## 3. WaterProgressBar

水波进度条，继承 `Control`。使用 `D.WaterProgressAttribute` C++ 类型驱动水波动画（前后波浪层），带气泡弹出效果和 `ItemViewport` 圆角裁剪。

```qml
WaterProgressBar {
    value: 60
    running: true
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `value` | `real` | 进度值 0-100 |
| `running` | `bool` | 是否运行动画 |
| `backgroundColor1` / `backgroundColor2` | `Palette` | 背景渐变色 |
| `dropShadowColor` / `popBackgroundColor` / `textColor` | `Palette` | 阴影/气泡/文字颜色 |

## 4. BusyIndicator

加载指示器，继承 `T.BusyIndicator`。使用 webp 动画 spinner 图片，通过 `D.ColorOverlay` 叠加主题色，无限旋转动画。

```qml
BusyIndicator {
    running: true
    fillColor: Palette { normal: "blue" }
}
```

## 5. ScrollBar

滚动条，继承 `T.ScrollBar`。4 种状态动画过渡，带内外边框：

| 状态 | 宽度 | 说明 |
|------|------|------|
| hide | 窄 | 不活动或内容未超出时渐变透明 |
| normal | 窄 | 滚动时显示 |
| hover | 宽 | 鼠标悬停 |
| active | 宽 | 拖动中 |

`ScrollView` 自动绑定 DTK `ScrollBar`。`ScrollBar` 也可手动使用。

## 6. Slider

滑块，继承 `T.Slider`。使用 `ShapePath` 绘制虚线滑槽，支持 6 种把手类型，可选高亮已通过区域（`highlightedPassedGroove`）。

```qml
Slider {
    from: 0; to: 100
    value: 50
    handleType: Slider.ArrowUp
    highlightedPassedGroove: true
    dashPattern: [0.5, 0.25]
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `grooveColor` | `Palette` | 滑槽颜色 |
| `handleType` | `enum` | 把手方向类型 |
| `dashOffset` / `dashPattern` | `real` / `var` | 虚线偏移和模式 |
| `highlightedPassedGroove` | `bool` | 高亮已通过区域（palette.highlight） |

**HandleType 枚举：** `NoArrowHorizontal` / `NoArrowVertical` / `ArrowUp` / `ArrowLeft` / `ArrowBottom` / `ArrowRight`

## 7. TipsSlider

带刻度标签的滑块，继承 `Control`。内置 `Slider` + `Grid` 排列的 `SliderTipItem` 刻度，`tickDirection` 控制刻度在滑块前/后端。

```qml
TipsSlider {
    slider.value: 50
    tickDirection: TipsSlider.Front
    SliderTipItem { text: "0" }
    SliderTipItem { text: "50" }
    SliderTipItem { text: "100" }
}
```

**TickDirection 枚举：** `Front` / `Back`

## 8. 相关文档

- [panels.md](panels.md) — 面板组件（BoxPanel/ButtonPanel 用于进度条背景）
- [buttons.md](buttons.md) — 按钮类控件
