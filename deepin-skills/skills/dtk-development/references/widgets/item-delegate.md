# DStyledItemDelegate 列表项委托

## 1. 概述与适用场景

`DStyledItemDelegate`（dtkwidget）提供 DTK 风格的列表项绘制。配合 DListView/DTreeView 使用，提供圆角背景、间距、统一项大小等 DTK 样式。

`DStandardItem` 和 `DViewItemAction` 提供列表项的 DTK 扩展数据模型，支持通过属性接口自定义背景色、文字颜色、操作按钮和嵌入控件，**无需重写 paint()**。

**适用场景：**
- DListView/DTreeView 的列表项样式
- 需要圆角背景的列表
- 列表项带图标/操作按钮
- 需要自定义项背景色或文字颜色

## 2. BackgroundType 枚举

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | `NoBackground` | 无背景 |
| 1 | `ClipCornerBackground` | 裁剪圆角背景（首尾项圆角） |
| 2 | `RoundedBackground` | 圆角背景 |
| 0x100 | `NoNormalState` | 禁用 Normal 状态背景 |

## 3. DStyledItemDelegate 用法

### 3.1 基本用法

```cpp
#include <DStyledItemDelegate>
#include <DListView>

auto *listView = new DListView(this);
auto *delegate = new DStyledItemDelegate(listView);
listView->setItemDelegate(delegate);
```

### 3.2 设置背景类型

```cpp
// 圆角背景（最常用）
delegate->setBackgroundType(DStyledItemDelegate::RoundedBackground);

// 裁剪圆角（首尾项圆角，适合分组列表）
delegate->setBackgroundType(DStyledItemDelegate::ClipCornerBackground);

// 无背景
delegate->setBackgroundType(DStyledItemDelegate::NoBackground);
```

### 3.3 设置间距和大小

```cpp
delegate->setMargins(QMargins(10, 5, 10, 5));
delegate->setItemSize(QSize(300, 50));
delegate->setItemSpacing(5);
```

### 3.4 通过 DListView 设置

DListView 提供便捷接口，内部转发给 DStyledItemDelegate：

```cpp
listView->setBackgroundType(DStyledItemDelegate::RoundedBackground);
listView->setItemMargins(QMargins(10, 5, 10, 5));
listView->setItemSize(QSize(300, 50));
listView->setItemSpacing(5);
listView->setItemRadius(8);  // 自定义圆角半径
```

## 4. DStandardItem 用法

### 4.1 基本列表项

```cpp
#include <DStandardItem>

auto *item = new DStandardItem("列表项");
```

### 4.2 自定义项背景色

通过 `setBackgroundRole()` 设置单个项的背景色，支持 `DPalette::ColorType` 和 `QPalette::ColorRole`：

```cpp
// 使用 DPalette 颜色类型（推荐）
item->setBackgroundRole(DPalette::ItemBackground);
item->setBackgroundRole(DPalette::LightLively);
item->setBackgroundRole(DPalette::Warning);

// 使用 QPalette 颜色角色
item->setBackgroundRole(QPalette::Highlight);
```

### 4.3 自定义项文字颜色

通过 `setTextColorRole()` 设置单个项的文字颜色：

```cpp
// 使用 DPalette 颜色类型（推荐）
item->setTextColorRole(DPalette::TextTitle);
item->setTextColorRole(DPalette::TextWarning);
item->setTextColorRole(DPalette::TextDanger);

// 使用 QPalette 颜色角色
item->setTextColorRole(QPalette::Highlight);
```

### 4.4 自定义项字体大小

```cpp
item->setFontSize(DFontSizeManager::T5);
```

### 4.5 添加操作按钮

```cpp
auto *editAction = new DViewItemAction(Qt::AlignRight, QSize(16, 16), QSize(), true);
editAction->setIcon(DIconTheme::findQIcon("edit"));
editAction->setClickAreaMargins(QMargins(5, 5, 5, 5));

auto *deleteAction = new DViewItemAction(Qt::AlignRight, QSize(16, 16), QSize(), true);
deleteAction->setIcon(DIconTheme::findQIcon("delete"));

item->setActionList(Qt::RightEdge, {editAction, deleteAction});
```

### 4.6 设置 DCI 图标

```cpp
DDciIcon dciIcon = DDciIcon::fromTheme("my-icon");
item->setDciIcon(dciIcon);
```

### 4.7 添加文本扩展内容

`setTextActionList()` 在主文本下方添加多行文本内容：

```cpp
auto *subAction = new DViewItemAction(Qt::AlignLeft, QSize(), QSize(), false);
subAction->setText("副标题");
subAction->setTextColorRole(DPalette::TextTips);
subAction->setFontSize(DFontSizeManager::T8);

item->setTextActionList({subAction});
```

## 5. DViewItemAction 详解

| 方法 | 说明 |
|------|------|
| `setAlignment(Qt::Alignment)` | 设置对齐方式 |
| `setIconSize(QSize)` | 设置图标大小 |
| `setMaximumSize(QSize)` | 设置最大尺寸 |
| `setClickAreaMargins(QMargins)` | 设置点击区域边距 |
| `setTextColorRole(DPalette::ColorType)` | 设置文本颜色类型 |
| `setTextColorRole(QPalette::ColorRole)` | 设置文本颜色角色 |
| `setFontSize(DFontSizeManager::SizeType)` | 设置字体大小 |
| `setClickable(bool)` | 设置是否可点击 |
| `setWidget(QWidget*)` | 设置自定义控件（如开关、进度条） |
| `setDciIcon(DDciIcon)` | 设置 DCI 图标 |
| `setVisible(bool)` | 设置是否可见 |

### 5.1 嵌入自定义控件

通过 `DViewItemAction::setWidget()` 在列表项中嵌入任意 QWidget，如开关、进度条、标签等：

```cpp
auto *switchAction = new DViewItemAction(Qt::AlignRight, QSize(50, 30), QSize(50, 30), false);
auto *toggleSwitch = new DSwitchButton;
switchAction->setWidget(toggleSwitch);

item->setActionList(Qt::RightEdge, {switchAction});
```

嵌入的控件由 DStyledItemDelegate 在 paint 时自动定位，无需手动管理 geometry。

## 6. 自定义列表项的正确方式

**不要重写 paint()。** DStyledItemDelegate 已内置圆角背景、hover/选中效果、操作按钮绘制等逻辑，通过属性接口即可完成大部分自定义需求：

| 需求 | 正确做法 |
|------|---------|
| 圆角背景 | `delegate->setBackgroundType(RoundedBackground)` |
| 自定义项背景色 | `item->setBackgroundRole(DPalette::ColorType)` |
| 自定义项文字颜色 | `item->setTextColorRole(DPalette::ColorType)` |
| 自定义字体大小 | `item->setFontSize(DFontSizeManager::SizeType)` |
| 添加操作按钮 | `item->setActionList(Qt::Edge, {actions})` |
| 嵌入自定义控件 | `action->setWidget(widget)` |
| 自定义圆角半径 | `listView->setItemRadius(int)` |
| 调整项间距/边距 | `delegate->setMargins()` / `setItemSpacing()` |
| 统一项大小 | `delegate->setItemSize(QSize)` |

## 7. 常见错误与避坑

### 错误 1：不设置 DStyledItemDelegate

```cpp
// ❌ 错误：DListView 缺少 DTK 样式
auto *listView = new DListView(this);

// ✅ 正确：设置 DStyledItemDelegate
auto *listView = new DListView(this);
listView->setItemDelegate(new DStyledItemDelegate(listView));
```

### 错误 2：继承 DStyledItemDelegate 重写 paint()

```cpp
// ❌ 错误：不必要的复杂度
class MyDelegate : public DStyledItemDelegate {
    void paint(QPainter *painter, const QStyleOptionViewItem &option,
               const QModelIndex &index) const override {
        // 大量绘制代码...
    }
};

// ✅ 正确：使用属性接口
auto *delegate = new DStyledItemDelegate(listView);
delegate->setBackgroundType(DStyledItemDelegate::RoundedBackground);
item->setBackgroundRole(DPalette::Warning);
item->setTextColorRole(DPalette::TextWarning);
```

## 8. 相关文档

- [view.md](view.md) - 视图控件
- [label.md](label.md) - DLabel
- [../theme/palette.md](../theme/palette.md) - 调色板规范
