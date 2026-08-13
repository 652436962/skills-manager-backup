# 输入类控件

## 1. 概述与适用场景

DTK QML 提供多种输入控件，支持文本输入、搜索、密码、数值调节等场景。

**适用场景：**
- 普通文本输入 → `TextField`
- 搜索输入 → `SearchEdit`
- 密码输入 → `PasswordField`
- 数值调节 → `SpinBox`

**相关组件：**
- `TextField` — 文本输入框
- `SearchEdit` — 搜索框
- `PasswordField` — 密码输入框
- `SpinBox` — 数值调节框

## 2. TextField

文本输入框，继承 `T.TextField`。使用 `EditPanel` 背景，支持 alert 状态，内置右键菜单（复制/粘贴/全选/撤销/重做）。

```qml
TextField {
    placeholderText: "请输入..."
    onTextChanged: console.log(text)
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `placeholderTextColor` | `Palette` | 占位文本颜色 |
| `backgroundColor` | `Palette` | 背景颜色 |
| `alertText` | `string` | 警告文本 |
| `alertDuration` | `int` | 警告显示时长（ms） |
| `showAlert` | `bool` | 是否显示警告 |

**注意事项：** 禁用状态 opacity 0.4，自带右键上下文菜单（复制/剪切/粘贴/全选/撤销/重做）。

## 2. LineEdit

带清除按钮的输入框，继承 `TextField`。输入内容后自动显示清除按钮。

```qml
LineEdit {
    placeholderText: "搜索..."
}
```

## 3. SearchEdit

搜索输入框，继承 `LineEdit`。未激活时在中央显示搜索图标（`action_search`）和占位文本，激活后图标和文本平滑动画移到左侧。

```qml
SearchEdit {
    placeholder: "搜索设置"
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `placeholder` | `string` | 未激活时显示的占位文本 |
| `editting` | `bool` | 是否处于编辑状态（只读） |

## 4. PasswordEdit

密码输入框，继承 `LineEdit`。带密码显隐切换按钮（`entry_password_shown`/`entry_password_hide` 图标），默认 `echoMode: Password`。

```qml
PasswordEdit {
    width: 200
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `isEchoMode` | `bool` | 当前是否明文显示（只读） |
| `echoButtonVisible` | `bool` | 是否显示切换按钮 |
| `toggleEchoMode()` | 方法 | 切换显隐状态 |

## 5. SpinBox

数字输入框，继承 `T.SpinBox`。使用 `EditPanel` 背景和 `SpinBoxIndicator` 上下箭头（带 inactive 状态），内置 `IntValidator`。支持 alert 状态。

```qml
SpinBox {
    from: 0
    to: 100
    value: 50
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `alertText` / `alertDuration` / `showAlert` | — | Alert 状态控制 |

## 6. PlusMinusSpinBox

带加减重置按钮的 SpinBox，继承 `FocusScope`。左侧显示减号/复位按钮，中间 SpinBox，右侧加号按钮。

```qml
PlusMinusSpinBox {
    spinBox.from: 0
    spinBox.to: 100
    upButtonVisible: true
    downButtonVisible: true
    resetButtonVisible: true
}
```

## 7. IpV4LineEdit

IPv4 地址输入框，继承 `FocusScope`。4 个 0-255 的数字输入域，用点分隔。支持 alert 状态。

```qml
IpV4LineEdit {
    text: "192.168.1.1"
}
```

## 8. KeySequenceEdit

快捷键编辑控件，继承 `Control`。捕获按键组合并以 `KeySequenceLabel` 显示，使用 `D.KeySequenceListener` C++ 后端。

```qml
KeySequenceEdit {
    placeholderText: "设置快捷键..."
    keys: ["Ctrl+Shift+T"]
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `keys` | `string[]` | 当前按键组合 |
| `placeholderText` | `string` | 占位文本 |

## 9. ComboBox

下拉选择框，继承 `T.ComboBox`。支持图标（`iconNameRole`）、可编辑模式、alert 状态。弹窗使用 `FloatingPanel` + `ArrowListView`，委托使用 `MenuItem`。可编辑模式下显示分隔线和箭头指示器。

```qml
ComboBox {
    model: ["选项1", "选项2", "选项3"]
    iconNameRole: "icon"
    currentIndex: 0
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `iconNameRole` | `string` | 模型中的图标名称字段 |
| `alertText` / `alertDuration` / `showAlert` | — | Alert 状态控制 |
| `maxVisibleItems` | `int` | 弹出列表最多可见项数 |
| `separatorColor` | `Palette` | 编辑模式下分隔符颜色 |

## 10. 相关文档

- [buttons.md](buttons.md) — 按钮类控件
- [color-selector.md](color-selector.md) — ColorSelector 取色器
