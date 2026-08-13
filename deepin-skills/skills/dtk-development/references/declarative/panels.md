# 面板与视觉效果控件

## 1. 概述与适用场景

DTK QML 提供面板和视觉效果组件，用于构建容器背景、浮动面板等。

**适用场景：**
- 控件背景面板 → `BoxPanel`
- 浮动面板 → `FloatingPanel`
- 高亮面板 → `HighlightPanel`

**相关组件：**
- `BoxPanel` — 盒模型背景面板
- `FloatingPanel` — 浮动面板
- `HighlightPanel` — 高亮面板

## 2. BoxPanel

盒模型背景面板，DTK 按钮/面板的核心背景组件。组合了：
- 渐变背景（`color1` → `color2`）
- 外阴影（`BoxShadow`，仅 `CommonColor` 族）
- 内阴影 x2（`BoxInsetShadow`，仅 `CommonColor` 族）
- 内边框（`InsideBoxBorder`）
- 外边框（`OutsideBoxBorder`）

所有颜色属性均为 `Palette` 类型，通过 `ColorSelector` 自动跟随状态。

| 属性 | 类型 | 说明 |
|------|------|------|
| `radius` | `int` | 圆角半径 |
| `color1` / `color2` | `Palette` | 渐变背景颜色（相等时无渐变） |
| `insideBorderColor` / `outsideBorderColor` | `Palette` | 内外边框颜色 |
| `dropShadowColor` | `Palette` | 外阴影颜色 |
| `innerShadowColor1` / `innerShadowColor2` | `Palette` | 内阴影颜色 |
| `boxShadowBlur` / `boxShadowOffsetY` | `int` | 阴影模糊和偏移 |
| `backgroundFlowsHovered` | `bool` | hover 状态是否影响背景渐变（默认 true） |

## 2. ButtonPanel

按钮面板，继承 `BoxPanel`。根据 `button` 的 `checked`/`highlighted` 状态自动切换调色板源：
- normal → `DS.Style.button.*`
- checked → `DS.Style.checkedButton.*`
- highlighted → `DS.Style.highlightedButton.*`

按下时减少阴影（blur 6→4），hover 时启动 `CicleSpreadAnimation` 圆形扩散动画（`CommonColor` 族）。`flat` 按钮仅在有状态或焦点时显示背景。

```qml
ButtonPanel {
    button: parentButton
    radius: 8
}
```

## 3. ButtonBox

按钮组容器，继承 `Control`。将多个按钮放在 `RowLayout` 中，使用 `ButtonPanel` 统一背景，`ButtonGroup` 管理互斥。

```qml
ButtonBox {
    Button { text: "左"; checkable: true }
    Button { text: "中"; checkable: true }
    Button { text: "右"; checkable: true }
}
```

## 4. FloatingPanel

浮动面板，继承 `Control`。半透明模糊背景（`InWindowBlur`）+ 外阴影（`BoxShadow`）+ 圆角剪切（`ItemViewport`）+ 内外边框。用于 Popup/Menu/ToolTip 背景。暗色主题时额外显示内边框。

```qml
FloatingPanel {
    radius: 12
    blurRadius: 12
    backgroundColor: Palette { normal: Qt.rgba(1, 1, 1, 0.8) }
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `backgroundColor` | `Palette` | 背景颜色 |
| `dropShadowColor` | `Palette` | 阴影颜色 |
| `outsideBorderColor` / `insideBorderColor` | `Palette` | 内外边框颜色 |
| `radius` | `int` | 圆角半径 |
| `blurRadius` | `int` | 模糊半径 |

## 5. HighlightPanel

高亮选中面板。组合高亮色矩形 + 外阴影（`BoxShadow`）+ 内阴影（`BoxInsetShadow`）。用于 MenuItem 和 ItemDelegate 的 hover/选中背景。

```qml
HighlightPanel {
    anchors.fill: parent
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `backgroundColor` | `Palette` | 高亮背景颜色 |
| `outerShadowColor` / `innerShadowColor` | `Palette` | 外/内阴影颜色 |

## 6. 阴影与边框

### BoxShadow

外阴影组件，通过 `D.DTK.makeShadowImageUrl()` 生成阴影图片，使用 `BorderImage` 九宫格渲染。

```qml
BoxShadow {
    anchors.fill: parent
    shadowBlur: 10
    shadowOffsetY: 4
    shadowColor: "#20000000"
    cornerRadius: 8
    hollow: true   // 镂空阴影
}
```

| 属性 | 类型 | 说明 |
|------|------|------|
| `shadowBlur` | `int` | 模糊半径 |
| `shadowOffsetX` / `shadowOffsetY` | `int` | 阴影偏移 |
| `shadowColor` | `color` | 阴影颜色 |
| `cornerRadius` | `int` | 统一圆角 |
| `topLeftRadius` ... `bottomRightRadius` | `int` | 四角独立半径 |
| `spread` | `int` | 扩散 |
| `hollow` | `bool` | 是否中空（镂空阴影） |

### BoxInsetShadow

内阴影组件，参数同 `BoxShadow`。

### InsideBoxBorder / OutsideBoxBorder

内外边框组件。`InsideBoxBorder` 向内收缩半像素，`OutsideBoxBorder` 向外扩展半像素。

```qml
InsideBoxBorder {
    radius: 8; color: "#10000000"; borderWidth: 1
}
```

### FocusBoxBorder

焦点指示边框。使用镂空 `BoxShadow` 实现发光焦点环。

```qml
FocusBoxBorder {
    color: control.palette.highlight
    radius: 8
    borderWidth: 2
}
```

### CicleSpreadAnimation

圆形扩散动画。从指定 `centerPoint` 向外扩散的遮罩动画，用于按钮 hover 效果。

```qml
CicleSpreadAnimation {
    centerPoint: Qt.point(mouse.x, mouse.y)
    // start() / stop()
}
```

## 7. 相关文档

- [dialogs.md](dialogs.md) — 对话框与窗口控件
- [buttons.md](buttons.md) — 按钮类控件
