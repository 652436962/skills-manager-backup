# ChameleonStyle 实现细节

本文档描述 DTK QWidget 控件的底层绘制机制，供需要深度定制或排查问题的开发者参考。

## 绘制入口分工

| 入口 | 用途 | 典型元素 |
|---|---|---|
| `drawPrimitive()` | 不可拆分的背景、边框、指示器 | 按钮背景、输入框、复选框、单选框、箭头 |
| `drawControl()` | 完整控件或控件标签 | 按钮、菜单项、标签页、进度条、表头 |
| `drawComplexControl()` | 多子区域控件 | 工具按钮、组合框、滑块、微调框 |
| `subElementRect()` | 普通控件内部区域 | 图标、文本、焦点框、指示器 |
| `subControlRect()` | 复杂控件子区域 | 下拉箭头、滑块手柄 |

## 状态组合优先级

1. `!Enabled` → Disabled 色组
2. `Sunken` 覆盖 `MouseOver`
3. `On/Selected` → Highlight
4. `HasFocus` → 焦点边框叠加
5. 方向/RTL → 区域方向

## 具体控件绘制

### 按钮

`CE_PushButton` 组合：
- `PE_PanelButtonCommand`：圆角背景
- `CE_PushButtonLabel`：图标+文字

背景色按状态变化：
- Normal：Button 色
- Hover：增亮
- Pressed：加深
- Disabled：降低 alpha

### 输入框

`CE_LineEdit` / `CE_ComboBox`：
- `PE_FrameLineEdit`：圆角边框
- 警告/错误状态使用 `DPalette::TextWarning` / `DPalette::FrameBorderWarning`

### 复选框/单选框

`PE_IndicatorCheckBox` / `PE_IndicatorRadioButton`：
- 三态：unchecked → partial → checked
- 动画：DTK 使用 `DGraphicsGlowEffect` 实现选中动画

### 滚动条

`CC_ScrollBar`：
- `SC_ScrollBarAddPage` / `SC_ScrollBarSubPage`：轨道
- `SC_ScrollBarSlider`：滑块
- 半透明悬浮模式：hover 时显示，否则透明

### 滑块

`CC_Slider`：
- `SC_SliderGroove`：轨道
- `SC_SliderHandle`：手柄
- Highlight 表示已走过区间

### 进度条

`CE_ProgressBar`：
- `CE_ProgressBarGroove`：圆角轨道
- `CE_ProgressBarContents`：按进度填充
- `CE_ProgressBarLabel`：百分比文本

## 源码位置

- `dtkwidget/src/widgets/dstyle.cpp`
- `dde-qtintegration/styleplugins/chameleon/chameleonstyle.cpp`
