# DToolTip 工具提示

## 1. 概述与适用场景

`DToolTip`（dtkwidget）扩展 Qt 工具提示。提供条件显示和省略检测功能。

**适用场景：**
- 文本被省略时才显示提示
- 控制工具提示的显示模式
- 自定义提示文本格式

## 2. ToolTipShowMode 枚举

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | `NotShow` | 不显示 |
| 1 | `AlwaysShow` | 总是显示 |
| 2 | `ShowWhenElided` | 文本被省略时显示 |
| 3 | `Default` | 默认（等同 AlwaysShow） |

## 3. 核心 API

### 3.1 设置提示显示模式

```cpp
#include <DToolTip>

// 文本省略时才显示提示
DToolTip::setToolTipShowMode(label, DToolTip::ShowWhenElided);

// 总是显示提示
DToolTip::setToolTipShowMode(label, DToolTip::AlwaysShow);

// 查询当前模式
DToolTip::ToolTipShowMode mode = DToolTip::toolTipShowMode(label);
```

### 3.2 设置提示文本格式

```cpp
// 设置为富文本
DToolTip::setToolTipTextFormat(Qt::RichText);

// 设置为纯文本
DToolTip::setToolTipTextFormat(Qt::PlainText);

// 查询
Qt::TextFormat fmt = DToolTip::toolTipTextFormat();
```

### 3.3 包裹提示文本

```cpp
QString wrapped = DToolTip::wrapToolTipText("很长的提示文本");
```

### 3.4 条件显示控制

```cpp
// 检查是否需要更新提示
bool need = DToolTip::needUpdateToolTip(widget, true);

// 控制是否显示提示
DToolTip::setShowToolTip(widget, false);
```

### 3.5 直接创建 DToolTip

```cpp
auto *tip = new DToolTip("提示内容", true); // true = 自动关闭
tip->show(QPoint(100, 100), 3000); // 显示 3 秒
```

## 4. 典型用法

### 4.1 DLabel 省略时显示提示

```cpp
auto *label = new DLabel("很长的文本内容可能会被省略", this);
label->setElideMode(Qt::ElideRight);
label->setToolTip("很长的文本内容可能会被省略");
DToolTip::setToolTipShowMode(label, DToolTip::ShowWhenElided);
```

### 4.2 全局设置提示文本格式

```cpp
// 在 main.cpp 中设置
DToolTip::setToolTipTextFormat(Qt::RichText);
```

## 5. 相关文档

- [label.md](label.md) - DLabel 标签控件
- [message.md](message.md) - 消息提示
