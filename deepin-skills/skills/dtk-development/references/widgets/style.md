# DStyle / ChameleonStyle 使用指南

## 1. 概述

DTK QWidget 控件外观由两层组成：
- `DStyle`（dtkwidget）：DTK 扩展风格类，定义图元、像素度量、状态画刷
- `ChameleonStyle`（dde-qtintegration）：实际绘制实现

**适用场景**：自定义控件时复用 DTK 风格元素

**相关接口**：
- `DStyle` — DTK 扩展风格类
- `DStyleHelper` — 风格辅助类，简化 DStyle 调用
- `DPaletteHelper` — 调色板辅助类

## 2. 自定义控件复用 DTK 风格

**优先使用标准 QStyleOption**，而不是复制源码：

```cpp
void MyButton::paintEvent(QPaintEvent *)
{
    QStyleOptionButton option;
    option.initFrom(this);
    option.rect = rect();
    option.text = text();
    option.icon = icon();
    
    if (isDown()) option.state |= QStyle::State_Sunken;
    if (isChecked()) option.state |= QStyle::State_On;

    QPainter painter(this);
    style()->drawControl(QStyle::CE_PushButton, &option, &painter, this);
}
```

**使用 DStyleHelper** 获取 DTK 特有资源：

```cpp
DStyleHelper helper(style());
QColor text = helper.getColor(&option, DPalette::TextTitle);
helper.drawPrimitive(DStyle::PE_ItemBackground, &option, &painter, this);
```

## 3. 状态与颜色

### 3.1 状态来源

从 `QStyleOption::state` 读取，不要查询鼠标位置：

| 状态 | 含义 |
|---|---|
| `State_Enabled` | 可用 |
| `State_MouseOver` | hover |
| `State_Sunken` | pressed |
| `State_On` / `State_Off` | checked / unchecked |
| `State_Selected` | 项被选中 |
| `State_HasFocus` | 有焦点 |

### 3.2 颜色角色

通过 `DPaletteHelper` 获取 DTK 扩展颜色：

| 角色 | 用途 |
|---|---|
| `QPalette::Button` | 按钮背景 |
| `QPalette::ButtonText` | 按钮文字 |
| `QPalette::Base` | 输入框背景 |
| `QPalette::Highlight` | 选中/强调 |
| `DPalette::FrameBorder` | 边框 |
| `DPalette::TextTips` | 提示文字 |
| `DPalette::TextWarning` | 警告文字 |

## 4. 像素度量与标准图标

```cpp
#include <DStyle>

// 标准图标
QIcon closeIcon = DStyle::standardIcon(style(), DStyle::SP_CloseButton);

// 像素度量
int radius = DStyle::pixelMetric(style(), DStyle::PM_FrameRadius);
int focusWidth = DStyle::pixelMetric(style(), DStyle::PM_FocusBorderWidth);
```

## 5. 列表项定制

**优先使用 DStyledItemDelegate**，而非自绘：

| 需求 | 方法 |
|------|------|
| 圆角背景 | `delegate->setBackgroundType(RoundedBackground)` |
| 自定义背景色 | `item->setBackgroundRole(DPalette::ColorType)` |
| 自定义文字色 | `item->setTextColorRole(DPalette::ColorType)` |
| 添加操作按钮 | `item->setActionList(Qt::Edge, {actions})` |

详见 [item-delegate.md](item-delegate.md)。

## 6. 注意事项

1. `initFrom()` 不会自动补齐 checked/down/selected，需手动设置
2. 始终传入 `this` 作为 widget 参数
3. RTL 使用 `visualRect()` 处理方向
4. 焦点框最后绘制，使用 pixel metric 而非写死像素值
5. 自绘区域必须与 `hitTestComplexControl()`/`subControlRect()` 一致

## 相关文档

- [palette.md](../theme/palette.md) — DPalette 语义色
- [chameleon-style.md](../theme/chameleon-style.md) — 风格插件架构
