# 对话框与窗口控件

## 1. 概述与适用场景

DTK QML 提供窗口和对话框组件，支持 DTK 风格的标题栏、边框和视觉效果。

**适用场景：**
- 应用主窗口 → `ApplicationWindow`
- 对话框窗口 → `DialogWindow`
- 内嵌对话框 → `Dialog`

**相关组件：**
- `ApplicationWindow` — 应用主窗口
- `DialogWindow` — 对话框窗口
- `Dialog` — 内嵌对话框

## 2. ApplicationWindow

应用主窗口，继承 `T.ApplicationWindow`。自动设置 DTK 调色板和默认字体（`D.DTK.fontManager.t6`），根据窗口激活状态切换 palette。

```qml
ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "My App"
}
```

## 2. DialogWindow

对话框窗口，继承 `Window`。`ColorSelector.family: CrystalColor`（水晶颜色族），禁用系统缩放，使用 `DialogType` 窗口类型。包含 `DialogTitleBar` 标题栏和内容区域。关闭时调用 `hide()` 而非 `close()`。

```qml
DialogWindow {
    width: 400
    height: 300
    icon: "dialog-icon"
    header: DialogTitleBar { title: "设置" }
    ColumnLayout {
        // 对话框内容
    }
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `header` | `Component` | 自定义标题栏组件 |
| `icon` | `string` | 窗口图标 |
| `content` | 默认属性 | 对话框内容区域 |

## 3. DialogTitleBar

对话框标题栏，继承 `Control`。支持标题、图标、自定义内容，右键弹出系统窗口菜单，支持 `InWindowBlur` 模糊背景。

```qml
DialogTitleBar {
    title: "确认"
    icon.name: "app-icon"
}
```

## 4. AboutDialog

关于对话框，继承 `DialogWindow`。显示产品名称、版本、描述、公司标志、网站链接、许可证信息。

```qml
AboutDialog {
    productName: "我的应用"
    version: "1.0.0"
    description: "这是一个示例应用"
    companyLogo: "company-logo"
    websiteName: "官方网站"
    websiteLink: "https://example.com"
}
```

## 5. TitleBar

应用标题栏，继承 `Control`。包含：
- 应用图标 + 标题文本
- 左右自定义内容区（`leftContent`/`content`）
- 选项菜单（自动包含 ThemeMenu、HelpAction、AboutAction、QuitAction）
- 窗口控制按钮组（最小化/最大化/关闭/全屏）
- 双击切换最大化、右键弹出系统菜单、全屏自动隐藏

```qml
ApplicationWindow {
    TitleBar {
        title: "My App"
        icon.name: "app-icon"
        fullScreenButtonVisible: true
        autoHideOnFullscreen: true
        leftContent: RowLayout { /* 自定义左侧控件 */ }
        content: Label { text: "自定义标题" }
    }
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `title` | `string` | 标题文本 |
| `icon` | 别名 | 图标 DciIcon 组件 |
| `leftContent` | `Component` | 左侧自定义组件 |
| `content` | `Component` | 中央自定义组件 |
| `menu` | `Component` | 选项菜单组件 |
| `menuDisabled` | `bool` | 禁用选项菜单 |
| `aboutDialog` | `Component` | 关于对话框组件 |
| `fullScreenButtonVisible` | `bool` | 是否显示全屏按钮 |
| `autoHideOnFullscreen` | `bool` | 全屏时自动隐藏 |
| `separatorVisible` | `bool` | 是否显示底部分隔线 |
| `enableInWindowBlendBlur` | `bool` | 是否启用窗口内模糊 |

## 6. WindowButtonGroup

窗口按钮组，继承 `RowLayout`。自动生成最小化/退出全屏/最大化/关闭按钮，根据 `D.DWindow` 的 motif 装饰来决定按钮可用性（如 `FUNC_RESIZE` 控制最大化按钮）。

```qml
WindowButtonGroup {
    textColor: Palette { normal: "white" }
    fullScreenButtonVisible: true
}
```

## 7. Popup

弹出层，继承 `T.Popup`。使用 `FloatingPanel` 背景，当父窗口失去激活时自动关闭。

```qml
Popup {
    width: 200; height: 100
    closeOnInactive: true
}
```

## 8. ArrowShapePopup

带箭头弹出层，继承 `Popup`。使用 `ArrowBoxPath` 裁剪形状指向目标控件，带内窗口模糊、外阴影、内外边框。`arrowDirection` 控制箭头朝向。

```qml
ArrowShapePopup {
    arrowDirection: ArrowBoxPath.Down
    arrowX: 100
    arrowY: 0
    roundedRadius: 8
}
```

## 9. FloatingMessage

浮动消息（Toast），继承 C++ `FloatingMessageContainer`。显示图标+文本+关闭按钮，默认 4 秒自动消失。

```qml
FloatingMessage {
    icon: "dialog-warning"
    message: "操作成功"
}
```

## 10. AlertToolTip

警告提示框，继承 `ToolTip`。红色文本、带三角箭头指向 `target` 控件，显示时带缩放/透明度动画过渡，不自动关闭。

```qml
AlertToolTip {
    text: "密码不能为空"
    target: passwordField
    visible: true
}
```

## 11. 相关文档

- [panels.md](panels.md) — FloatingPanel / HighlightPanel 面板组件
- [menus.md](menus.md) — Menu 菜单系统
- [color-selector.md](color-selector.md) — ColorSelector 取色器
