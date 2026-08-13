# 视图控件规范

## 1. 概述与适用场景

| 控件 | 适用场景 |
|------|----------|
| `DListView` | 列表视图（带 DTK 样式） |
| `DSimpleListView` | 简单列表视图 |
| `DStyledItemDelegate` | 自定义列表项绘制 |
| `DSimpleListItem` | 简单列表项基类 |

## 2. DListView 用法

### 2.1 基本列表

```cpp
#include <DListView>

auto *listView = new DListView(this);
auto *model = new QStandardItemModel(this);

for (int i = 0; i < 10; ++i) {
    auto *item = new QStandardItem(QString("项目 %1").arg(i + 1));
    model->appendRow(item);
}

listView->setModel(model);
```

### 2.2 带 DStyledItemDelegate

```cpp
#include <DListView>
#include <DStyledItemDelegate>

auto *listView = new DListView(this);
listView->setItemDelegate(new DStyledItemDelegate(this));
```

## 3. 修改列表背景、选中颜色和文字

```cpp
#include <DListView>
#include <DPalette>
#include <DPaletteHelper>

DListView *view = new DListView(this);
DPalette palette = DPaletteHelper::instance()->palette(view);
palette.setColor(QPalette::Base, QColor("#FAFAFC"));
palette.setColor(QPalette::Text, QColor("#242428"));
palette.setColor(QPalette::Highlight, QColor("#DCE7FF"));
palette.setColor(QPalette::HighlightedText, QColor("#173A7A"));
palette.setColor(DPalette::ItemBackground, QColor("#EEF3FF"));
DPaletteHelper::instance()->setPalette(view, palette);
```

`Base` 是视图底色，`Text` 是普通文字，`Highlight`/`HighlightedText` 是选中项背景和前景，`ItemBackground` 用于 hover 等弱反馈。模型通过 `Qt::BackgroundRole` 提供的背景或 delegate 的自绘背景可能覆盖 style 的 item 背景。单个 item 的字体和图标可分别通过 `Qt::FontRole`、`Qt::DecorationRole` 设置。

## 4. 常见错误与避坑

### 错误 1：不设置 DStyledItemDelegate

```cpp
// ⚠️ 默认 delegate 可能缺少 DTK 样式
auto *listView = new DListView(this);

// ✅ 使用 DStyledItemDelegate 获取 DTK 样式
listView->setItemDelegate(new DStyledItemDelegate(this));
```

## 5. 相关文档

- [index.md](index.md) - 控件选择决策树
