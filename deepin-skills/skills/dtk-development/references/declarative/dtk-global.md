# D.DTK QML 全局对象

## 1. 概述与适用场景

`DTK` 是 dtkdeclarative 提供的 QML 全局单例对象，是 QML 应用访问 DTK 核心功能的主要入口。

**适用场景：**
- 获取字体管理器
- 判断/监听主题类型
- 创建图标调色板
- 创建语义化颜色
- 访问平台主题

## 2. 枚举

### 2.1 ControlState

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | `NormalState` | 正常状态 |
| 1 | `HoveredState` | 悬停状态 |
| 2 | `PressedState` | 按下状态 |
| 3 | `DisabledState` | 禁用状态 |
| 4 | `InactiveState` | 非活跃状态 |

### 2.2 ZOrder

| 值 | 名称 | 说明 |
|----|------|------|
| -99 | `BottomOrder` | 底层 |
| -1 | `BelowOrder` | 下层 |
| 0 | `NormalOrder` | 正常层 |
| 1 | `AboveOrder` | 上层 |
| 99 | `TopOrder` | 顶层 |

## 3. 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `fontManager` | `DFontManager*` | 字体管理器 |
| `themeType` | `ColorType` | 当前主题类型 |
| `hasBlurWindow` | `bool` | 是否支持模糊窗口 |
| `hasComposite` | `bool` | 是否有合成器 |
| `hasNoTitlebar` | `bool` | 是否无标题栏模式 |
| `hasAnimation` | `bool` | 是否有动画 |
| `hasInWindowBlur` | `bool` | 是否支持窗口内模糊 |
| `isSoftwareRender` | `bool` | 是否软件渲染 |
| `windowManagerName` | `WMName` | 窗口管理器名称 |
| `platformTheme` | `DPlatformThemeProxy*` | 平台主题代理 |
| `palette` | `QPalette/QQuickPalette*` | 应用调色板 |
| `inactivePalette` | `QPalette/QQuickPalette*` | 非活跃调色板 |
| `deepinDistributionOrgLogo` | `QString` | 发行版 Logo 路径 |
| `deepinWebsiteName` | `QString` | 发行版网站名 |
| `deepinWebsiteLink` | `QString` | 发行版网站链接 |

## 4. 方法

### 4.1 makeIconPalette

创建图标调色板，用于 `DciIcon` 的主题感知着色：

```qml
import org.deepin.dtk 1.0

DciIcon {
    name: "my-icon"
    palette: D.DTK.makeIconPalette(D.DTK.palette)
}
```

### 4.2 makeColor

创建语义化颜色，支持 HSL 调整：

```qml
// 从调色板角色创建
Palette {
    normal: D.DTK.makeColor(Color.Highlight)
    hovered: D.DTK.makeColor(Color.Highlight).lightness(+10)
    pressed: D.DTK.makeColor(Color.Highlight).opacity(-10)
}

// 从 QColor 创建
Palette {
    normal: D.DTK.makeColor("#ff0000")
}
```

`Color.Type` 枚举：

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | `Invalid` | 无效 |
| 1 | `Highlight` | 高亮色 |
| 2 | `HighlightedText` | 高亮文本色 |

颜色调整方法链：

| 方法 | 参数范围 | 说明 |
|------|---------|------|
| `.lightness(n)` | -100 ~ +100 | 明度调整 |
| `.opacity(n)` | -100 ~ +100 | 透明度调整 |
| `.saturation(n)` | -100 ~ +100 | 饱和度调整 |
| `.hue(n)` | -100 ~ +100 | 色相调整 |

### 4.3 blendColor

混合两个颜色：

```qml
color: D.DTK.blendColor("#ff0000", "#0000ff")
```

### 4.4 toColorType

颜色转主题类型：

```qml
var type = D.DTK.toColorType(someColor)
if (type === ApplicationHelper.DarkType) { /* 深色 */ }
```

### 4.5 selectColor

根据窗口颜色选择亮/暗色：

```qml
color: D.DTK.selectColor(windowColor, lightColor, darkColor)
```

### 4.6 sendMessage

发送浮动消息：

```qml
// 简单消息
D.DTK.sendMessage(rootItem, "操作成功", "dialog-ok", 3000)

// 按 ID 关闭
D.DTK.closeMessage(rootItem, "msg-id")
```

### 4.7 sendSystemMessage

发送系统通知：

```qml
D.DTK.sendSystemMessage("标题", "内容", "app-icon", [], {}, 3000)
```

### 4.8 cursorPosition

获取光标位置：

```qml
var pos = D.DTK.cursorPosition()
```

## 5. fontManager 用法

```qml
import org.deepin.dtk 1.0

Text {
    font: D.DTK.fontManager.t4  // 标题字体
}

Text {
    font: D.DTK.fontManager.t6  // 正文字体
}

Text {
    font: D.DTK.fontManager.t8  // 辅助文本字体
}
```

字体大小完整对照表见 [font-manager.md](../utilities/font-manager.md)。

## 6. themeType 用法

```qml
import org.deepin.dtk 1.0

// 判断主题
if (D.DTK.themeType === ApplicationHelper.DarkType) {
    bgColor = "#1a1a1a"
} else {
    bgColor = "#f0f0f0"
}

// 监听主题变化
Connections {
    target: D.DTK
    function onThemeTypeChanged(type) {
        // 刷新 UI
    }
}
```

## 7. 信号

| 信号 | 说明 |
|------|------|
| `themeTypeChanged(ColorType)` | 主题类型变化 |
| `hasBlurWindowChanged()` | 模糊窗口支持变化 |
| `hasCompositeChanged()` | 合成器状态变化 |
| `hasNoTitlebarChanged()` | 无标题栏模式变化 |
| `hasAnimationChanged()` | 动画支持变化 |
| `hasInWindowBlurChanged()` | 窗口内模糊支持变化 |
| `paletteChanged()` | 调色板变化 |
| `inactivePaletteChanged()` | 非活跃调色板变化 |

## 8. 常见错误与避坑

### 错误 1：硬编码字体大小

```qml
// ❌ 错误：硬编码像素大小
font.pixelSize: 14

// ✅ 正确：使用 fontManager
font: D.DTK.fontManager.t6
```

### 错误 2：硬编码主题颜色

```qml
// ❌ 错误：硬编码颜色，不响应主题切换
color: "#f0f0f0"

// ✅ 正确：使用 Palette + ColorSelector
backgroundColor: Palette {
    normal: D.DTK.makeColor(Color.Highlight)
    normal: D.DTK.makeColor(Color.Highlight)
    normalDark: D.DTK.makeColor(Color.Highlight)
}
```

## 9. 相关文档

- [color-selector.md](color-selector.md) - ColorSelector 取色器
- [dwindow.md](dwindow.md) - DWindow 窗口附加属性
- [dci-icon.md](dci-icon.md) - QML 中使用 dci 图标
- [../utilities/gui-helper.md](../utilities/gui-helper.md) - DGuiApplicationHelper
- [../utilities/font-manager.md](../utilities/font-manager.md) - 字体管理器
