# QML API

**导入**: `import org.deepin.ds 1.0`

所有类型注册在 `org.deepin.ds` 模块下。

## 根元素

### AppletItem

Applet 插件根元素，继承 `QQuickItem`。

**附加属性 `Applet`**:
| 属性 | 说明 |
|------|------|
| `Applet.id` | 插件实例 ID |
| `Applet.pluginId` | 插件 ID |
| `Applet.rootObject` | QML 根对象 |
| `Applet.parent` | 父插件 |

```qml
AppletItem {
    implicitWidth: 100; implicitHeight: 100
    Text { text: Applet.pluginId }
}
```

### ContainmentItem

Containment 插件根元素，继承 `AppletItem`。

**附加属性 `Containment`**:
| 属性 | 说明 |
|------|------|
| `Containment.appletItems` | 子 applet 的 QML 列表模型 |

```qml
ContainmentItem {
    Repeater {
        model: Containment.appletItems
        delegate: Control { contentItem: model.data }
    }
}
```

## 窗口组件

### PanelPopupWindow

弹窗窗口基类，继承 `PopupWindow`。Panel 子 applet 中弹出面板时使用的容器窗口。

| 属性 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `xOffset` | `real` | `0` | 水平偏移 |
| `yOffset` | `real` | `0` | 垂直偏移 |
| `margins` | `int` | `10` | 屏幕边距 |
| `currentItem` | `Item` | — | 当前显示的内容项 |
| `requestedWidth` | `int` | `10` | 内容请求宽度 |
| `requestedHeight` | `int` | `10` | 内容请求高度 |

窗口标志: X11 下 `Qt.Tool | Qt.WindowStaysOnTopHint`，Wayland 下 `Qt.Popup`。

### PanelToolTipWindow

继承 `PanelPopupWindow`。提示窗口，标志 `Qt.ToolTip | Qt.WindowStaysOnTopHint`。窗口圆角 8，阴影半径 8。

### PanelMenuWindow

继承 `PanelPopupWindow`。菜单窗口，标志 `Qt.Popup | Qt.WindowStaysOnTopHint`。

**属性**: `mainMenuWindow`(QtObject) — 区分主菜单与子菜单窗口（grabMouse 用）。

### PanelPopup / PanelToolTip / PanelMenu

对应三种窗口的内容组件，在子 applet 中直接使用：

```qml
PanelPopup {
    id: popup; width: 200; height: 300
    Button { text: "content" }
}
PanelToolTip {
    text: "tooltip content"
}
PanelMenu {
    width: 200; height: 400
    ListView { ... }
}
```

### QuickDragWindow

透明拖拽窗口，标志 `Qt.FramelessWindowHint | Qt.BypassWindowManagerHint | Qt.WindowTransparentForInput | Qt.WindowDoesNotAcceptFocus`。用于拖拽操作时的跟随窗口。

## 附加属性

### Panel

Panel 子 applet 中可用：

| 属性 | 说明 |
|------|------|
| `Panel.rootObject` | Panel 根对象 |
| `Panel.id` | Panel 实例 ID |

### DLayerShellWindow

详见 [layershell.md](../layershell.md)。

### DQuickDrag

附加属性，用于拖拽功能的 QML 集成。可附加到任意 `Item` 上，启动拖拽时自动创建 `QuickDragWindow`。

## 全局对象

### DS

单例对象。

| 方法 | 说明 |
|------|------|
| `DS.applet(pluginId)` | 按插件 ID 获取 applet 引用 |

```qml
var weather = DS.applet("org.deepin.ds.weather")
if (weather && weather.rootObject) {
    console.log(weather.rootObject.temperature)
}
```

## 数据模型

### DListToTableProxyModel

`ListModel` 到表格模型的代理，用于 `TreeView`/`TableView` 场景。

```qml
DListToTableProxyModel {
    sourceModel: listModel
    roles: [4096, 4097, 4098]
}
```

## 完整 QML 类型表

| QML 类型 | C++ 类 | 可创建 | 说明 |
|----------|--------|--------|------|
| `AppletItem` | `DAppletItem` | 是 | Applet 根元素 |
| `ContainmentItem` | `DContainmentItem` | 是 | Containment 根元素 |
| `PanelPopup` | — | 是 | 弹窗内容 |
| `PanelToolTip` | — | 是 | 提示内容 |
| `PanelMenu` | — | 是 | 菜单内容 |
| `PanelPopupWindow` | — | 是 | 弹窗窗口 |
| `PanelToolTipWindow` | — | 是 | 提示窗口 |
| `PanelMenuWindow` | — | 是 | 菜单窗口 |
| `QuickDragWindow` | — | 是 | 拖拽跟随窗口 |
| `PopupWindow` | `PopupWindow` | 是 | 弹窗窗口基类 |
| `DLayerShellWindow` | `DLayerShellWindow` | 是 | Layer Shell 窗口 |
| `DListToTableProxyModel` | `ListToTableProxyModel` | 是 | 列表→表格模型代理 |
| `DQuickDrag` | `DQuickDrag` | 否 | 拖拽附加属性 |
| `DS` | `DQmlGlobal` | 单例 | 全局对象 |
| `Applet` | `DAppletItem` | 否 | Applet 附加属性 |
| `Containment` | `DContainmentItem` | 否 | Containment 附加属性 |
| `Panel` | `DPanel` | 否 | Panel 附加属性 |
