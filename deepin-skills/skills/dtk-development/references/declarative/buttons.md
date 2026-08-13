# 按钮类控件

## 1. 概述与适用场景

DTK QML 提供多种按钮控件，用于不同的交互场景。

**适用场景：**
- 普通按钮操作 → `Button`
- 主要推荐操作 → `RecommandButton`
- 危险警告操作 → `WarningButton`
- 图标按钮 → `IconButton`

**相关组件：**
- `Button` — 标准按钮
- `RecommandButton` — 推荐按钮
- `WarningButton` — 警告按钮
- `IconButton` — 图标按钮

## 2. Button

标准按钮，继承 `T.Button`，带渐变背景（`BoxPanel`）、内外阴影、通过 `ColorSelector` 自动跟随主题和状态。

```qml
Button {
    text: "确定"
    icon.name: "action_ok"
    onClicked: console.log("clicked")
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `textColor` | `Palette` | 文本和图标颜色调色板 |

**注意事项：**
- `icon.name` 优先通过 `D.DTK.makeIcon()` 查找 dci 图标路径
- 禁用状态下自动设置 `opacity: 0.4`
- `contentItem` 使用 `D.IconLabel`，支持 `TextUnderIcon` 等显示模式
- 背景使用 `ButtonPanel`，根据 `checked`/`highlighted` 状态切换样式

## 2. RecommandButton

推荐按钮（主操作按钮），继承 `Button`，固定 `highlighted: true`，使用高亮样式（不同的背景渐变和阴影）。

```qml
RecommandButton {
    text: "保存"
}
```

## 3. WarningButton

警告/危险操作按钮，继承 `Button`，文本调色板指向 `DS.Style.warningButton.text`（红色/橙色系）。

```qml
WarningButton {
    text: "删除"
}
```

## 4. ToolButton

工具栏按钮，继承 `T.ToolButton`。默认 `flat: true`、`display: TextUnderIcon`、使用 `CrystalColor` 颜色族。适合工具栏场景。

```qml
ToolButton {
    text: "工具"
    icon.name: "action_tool"
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `textColor` | `Palette` | 文本颜色调色板 |

## 5. IconButton

纯图标按钮，继承 `Button`。正方形、`contentItem` 直接使用 `D.DciIcon`。

```qml
IconButton {
    icon.name: "entry_clear"
}
```

## 6. ActionButton

透明图标按钮，继承 `T.Button`。无背景（`background: null`），仅在按下时显示文本颜色变化。适合输入框内的清除按钮等。

```qml
ActionButton {
    icon.name: "entry_clear"
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `textColor` | `Palette` | 图标颜色调色板 |

## 7. FloatingButton

圆形浮动按钮，继承 `Button`。不可复选，始终 `checked: true`，背景圆角为 `width/2`。`RoundButton` 是其别名。

```qml
FloatingButton {
    icon.name: "action_add"
}
```

## 8. DelayButton

长按确认按钮，继承 `T.DelayButton`。按住时显示从左到右的进度动画（高亮色填充），释放后触发 `activated`。

```qml
DelayButton {
    text: "长按确认"
    delay: 1000  // 毫秒
    onActivated: console.log("confirmed")
}
```

## 9. RadioButton

单选按钮，继承 `T.RadioButton`。使用 dci 图标 `radio_checked`/`radio_unchecked` 作为指示器，聚焦时显示 `radio_focus`。

```qml
RadioButton {
    text: "选项A"
    checked: true
}
```

## 10. CheckBox

复选框，继承 `T.CheckBox`。使用 dci 图标 `checkbox_checked`/`checkbox_unchecked`/`checkbox_mix` 作为指示器，支持三态 `checkState`。

```qml
CheckBox {
    text: "启用"
    checkState: Qt.Checked
}
```

## 11. Switch

开关按钮，继承 `T.Switch`。带平滑动画的滑动开关，使用 `switch_button` dci 图标作为滑块。

```qml
Switch {
    text: "WiFi"
    checked: true
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `backgroundColor` | `Palette` | 轨道背景颜色 |
| `handleColor` | `Palette` | 滑块颜色 |

## 12. 相关文档

- [inputs.md](inputs.md) — 输入类控件
- [color-selector.md](color-selector.md) — ColorSelector 取色器
- [dci-icon.md](dci-icon.md) — dci 图标使用
