# 菜单类控件

## 1. 概述与适用场景

DTK QML 提供菜单组件，支持右键菜单、下拉菜单、子菜单等场景。

**适用场景：**
- 右键菜单 → `Menu`
- 菜单项 → `MenuItem`
- 分隔线 → `MenuSeparator`

**相关组件：**
- `Menu` — 菜单
- `MenuItem` — 菜单项
- `MenuSeparator` — 分隔线

## 2. Menu

菜单，继承 `T.Menu`。使用 `FloatingPanel` 背景，`ArrowListView` 内容滚动，支持 `header`/`footer` 自定义组件。当父窗口失去激活时自动关闭。

```qml
Menu {
    MenuItem { text: "新建" }
    MenuItem { text: "打开" }
    MenuSeparator { }
    MenuItem { text: "退出" }
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `closeOnInactive` | `bool` | 是否在窗口失活时关闭（默认 true） |
| `maxVisibleItems` | `int` | 最多可见菜单项数 |
| `backgroundColor` | `Palette` | 背景颜色 |
| `header` / `footer` | `Component` | 头部/底部自定义组件 |

## 2. MenuItem

菜单项，继承 `T.MenuItem`。选中时显示 `menu_select` 勾选图标，子菜单项带 `menu_arrow` 箭头，hover/press 时 `HighlightPanel` 高亮。

```qml
MenuItem {
    text: "复制"
    icon.name: "action_copy"
    onTriggered: console.log("copy")
}
```

| 自定义属性 | 类型 | 说明 |
|-----------|------|------|
| `useIndicatorPadding` | `bool` | 是否为勾选指示器预留空间 |
| `textColor` | `Palette` | 文本颜色（highlighted 时自动切换为 checkedButton 颜色） |
| `subMenuBackgroundColor` | `Palette` | 子菜单打开时背景色 |

## 3. MenuSeparator

菜单分隔线，继承 `T.MenuSeparator`。支持带文本标题的分隔线（设置 `text` 时显示文字标签，否则显示线段）。

```qml
MenuSeparator { }
MenuSeparator { text: "编辑" }
```

## 4. ThemeMenu

主题切换菜单，继承 `Menu`。内置亮色/暗色/系统三种主题选项，使用 `ActionGroup` 互斥，调用 `D.ApplicationHelper.paletteType` 切换。

```qml
ThemeMenu { }
```

## 5. 相关文档

- [panels.md](panels.md) — FloatingPanel / HighlightPanel 面板组件
- [dialogs.md](dialogs.md) — 对话框与窗口控件
