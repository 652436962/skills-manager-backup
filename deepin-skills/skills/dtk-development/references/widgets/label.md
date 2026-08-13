# DLabel 标签控件

## 1. 概述与适用场景

`DLabel`（dtkwidget）是 QLabel 的 DTK 扩展。在 QLabel 基础上增加了前景色主题感知和文本省略功能。

**适用场景：**
- 所有需要显示文本/图标的标签
- 需要主题感知前景色的标签
- 需要文本省略（...）的标签

## 2. DLabel 扩展功能

### 2.1 前景色设置

```cpp
#include <DLabel>

auto *label = new DLabel("标题", this);

// 使用 DPalette::ColorType 设置前景色（主题感知）
label->setForegroundRole(DPalette::TextTitle);

// 使用 QPalette::ColorRole 设置前景色
label->setForegroundRole(QPalette::Highlight);
```

### 2.2 文本省略

```cpp
auto *label = new DLabel(this);
label->setElideMode(Qt::ElideRight);  // 右侧省略 "很长的文..."
label->setElideMode(Qt::ElideMiddle); // 中间省略 "很...文"
label->setElideMode(Qt::ElideLeft);   // 左侧省略 "...长文本"
label->setElideMode(Qt::ElideNone);   // 不省略

Qt::TextElideMode mode = label->elideMode();
```

### 2.3 结合 DFontSizeManager

```cpp
#include <DLabel>
#include <DFontSizeManager>

auto *title = new DLabel("大标题");
DFontSizeManager::instance()->bind(title, DFontSizeManager::T4);

auto *body = new DLabel("正文");
DFontSizeManager::instance()->bind(body, DFontSizeManager::T6);
```

## 3. 与 QLabel 的差异

| 功能 | QLabel | DLabel |
|------|--------|--------|
| `setForegroundRole(DPalette::ColorType)` | 不支持 | 支持（主题感知） |
| `setElideMode()` | 不支持 | 支持 |
| 其余功能 | 完全继承 | 完全继承 |

## 4. 常见错误与避坑

### 错误 1：使用 QLabel 而非 DLabel

```cpp
// ❌ 错误：QLabel 不支持 DPalette 前景色
auto *label = new QLabel("标题");
label->setForegroundRole(DPalette::TextTitle); // 不生效

// ✅ 正确：使用 DLabel
auto *label = new DLabel("标题");
label->setForegroundRole(DPalette::TextTitle);
```

### 错误 2：用 QSS 设置颜色

```cpp
// ❌ 错误：QSS 不响应主题切换
label->setStyleSheet("color: red;");

// ✅ 正确：使用 DPalette
label->setForegroundRole(DPalette::TextWarning);
```

## 5. 相关文档

- [button.md](button.md) - 按钮规范
- [input.md](input.md) - 输入控件
- [../utilities/font-manager.md](../utilities/font-manager.md) - 字体管理器
- [../theme/palette.md](../theme/palette.md) - 调色板规范
