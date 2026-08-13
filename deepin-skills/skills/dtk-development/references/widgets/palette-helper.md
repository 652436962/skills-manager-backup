# DPaletteHelper 调色板助手

## 1. 概述与适用场景

`DPaletteHelper`（dtkwidget）是 DPalette 的 QWidget 端辅助类。用于获取和设置 QWidget 的 DTK 调色板。

**适用场景：**
- 获取控件的 DPalette（含 DTK 扩展色）
- 设置控件的调色板
- 重置控件调色板为系统默认

## 2. 核心 API

### 2.1 获取控件调色板

```cpp
#include <DPaletteHelper>

// 获取控件调色板
DPalette dp = DPaletteHelper::instance()->palette(widget);

// 获取指定基色的调色板
DPalette dp = DPaletteHelper::instance()->palette(widget, QPalette());

// 使用调色板颜色
QColor titleColor = dp.color(DPalette::TextTitle);
QColor tipsColor = dp.color(DPalette::TextTips);
```

### 2.2 设置控件调色板

```cpp
DPalette dp = DPaletteHelper::instance()->palette(widget);
dp.setColor(DPalette::ItemBackground, QColor("#f0f0f0"));
dp.setColor(DPalette::TextTitle, QColor("#303030"));
DPaletteHelper::instance()->setPalette(widget, dp);
```

### 2.3 重置控件调色板

```cpp
DPaletteHelper::instance()->resetPalette(widget);
```

## 3. 与 DGuiApplicationHelper 的关系

```
DGuiApplicationHelper（全局调色板）
    │
    ├─ applicationPalette()  → 全局应用调色板
    │
    └─ DPaletteHelper（控件调色板）
        ├─ palette(widget)   → 控件当前调色板（含控件自定义覆盖）
        ├─ setPalette()      → 设置控件调色板（覆盖全局）
        └─ resetPalette()    → 重置为全局调色板
```

## 4. 完整示例

```cpp
#include <DPaletteHelper>
#include <DLabel>

class MyWidget : public QWidget {
    void updateColors() {
        DPalette dp = DPaletteHelper::instance()->palette(this);
        
        // 修改背景色
        dp.setColor(DPalette::ItemBackground, QColor(0, 0, 0, 20));
        DPaletteHelper::instance()->setPalette(this, dp);
    }
};
```

## 5. 相关文档

- [../theme/palette.md](../theme/palette.md) - DPalette 调色板规范
- [../utilities/gui-helper.md](../utilities/gui-helper.md) - DGuiApplicationHelper
