# QML Style 单例与应用级样式覆盖

## 1. 概述与适用场景

dtkdeclarative 提供两套样式机制，用于控件样式定制和应用级样式覆盖。

**适用场景：**
- 单个控件样式定制 → 控件 `style` 属性
- 应用级样式覆盖 → `Style` 单例

**相关接口：**
- 控件 `style` 属性 — 单个控件样式参数
- `Style` 单例 — 应用级样式覆盖

## 2. 两层"style"不要混淆

dtkdeclarative 中存在两套职责不同的样式机制：

| 层次 | URI / 名称 | 职责 |
|---|---|---|
| Qt Quick Controls 风格插件 | `Chameleon` | `dtkdeclarative/chameleon/` 提供 `Button.qml`、`CheckBox.qml` 等同名映射，使标准 Qt Quick Controls 使用 DTK 控件实现 |
| DTK 样式数据单例 | `org.deepin.dtk.style 1.0` 中的 `Style` | 集中提供尺寸、间距、圆角和各状态调色板，供 `org.deepin.dtk` 控件绘制时读取 |

前者决定"标准控件由哪套 QML 实现"，后者决定 DTK 控件实现使用哪些设计参数。它们可以同时工作，但不是同一个插件。

## 3. URI 和注册过程
