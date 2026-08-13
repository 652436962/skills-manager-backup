# 调色板规范

## 1. 概述与适用场景

**DPalette** 是 DTK 扩展 Qt 的 `QPalette` 提供的主题感知调色板。特点：

- **主题扩展色**：提供 DTK 特有的语义化颜色（如 `TextTitle`、`TextWarning`）
- **主题感知**：自动跟随系统主题（Light/Dark）切换
- **与 DStyle 协作**：通过 `DStyle` 获取经过状态处理的画笔

**适用场景：**
- 自定义控件的背景色、前景色
- 列表项背景色
- 警告文本颜色
- 标题文本颜色
- 占位符文本颜色

## 2. 取色规则

### 2.1 DPalette::ColorType 颜色类型

| 颜色类型 | 用途 | 示例 |
|----------|------|------|
| `ItemBackground` | 列表项背景色 | 列表项、表格行 |
| `TextTitle` | 标题型文本 | 对话框标题、分组标题 |
| `TextTips` | 提示性文本 | 描述文字、帮助文本 |
| `TextWarning` | 警告类型文本 | 错误提示、警告信息 |
| `TextLively` | 活跃式文本 | 强调文字（不受活跃色影响） |
| `LightLively` | 活跃式按钮亮色 | 推荐按钮背景（不受活跃色影响） |
| `DarkLively` | 活跃式按钮暗色 | 推荐按钮渐变（不受活跃色影响） |
| `FrameBorder` | 控件边框颜色 | 输入框边框、分组边框 |
| `PlaceholderText` | 占位符文本 | 输入框占位内容 |
| `FrameShadowBorder` | 阴影边框颜色 | 与阴影叠加的边框 |
| `ObviousBackground` | 明显背景色 | 突出显示的区域 |

### 2.2 标准调色板获取

```cpp
#include <DPalette>
#include <DGuiApplicationHelper>

// 获取标准调色板（Light 或 Dark）
DPalette lightPalette = DGuiApplicationHelper::standardPalette(
    DGuiApplicationHelper::LightType);
DPalette darkPalette = DGuiApplicationHelper::standardPalette(
    DGuiApplicationHelper::DarkType);

// 获取应用调色板
DPalette appPalette = DGuiApplicationHelper::instance()->applicationPalette();

// 获取当前主题的调色板
auto themeType = DGuiApplicationHelper::instance()->themeType();
DPalette palette = DGuiApplicationHelper::standardPalette(themeType);
```

## 3. API 用法

### 3.1 获取颜色

```cpp
#include <DPalette>
#include <DGuiApplicationHelper>

DPalette palette = DGuiApplicationHelper::instance()->applicationPalette();

// 获取当前颜色组的颜色
QColor titleColor = palette.color(DPalette::TextTitle);
QColor tipsColor = palette.color(DPalette::TextTips);
QColor warningColor = palette.color(DPalette::TextWarning);
QColor itemBg = palette.color(DPalette::ItemBackground);

// 获取指定颜色组的颜色
QColor disabledTitle = palette.color(QPalette::Disabled, DPalette::TextTitle);

// 使用便捷函数
QBrush titleBrush = palette.textTitle();
QBrush tipsBrush = palette.textTips();
QBrush warningBrush = palette.textWarning();
QBrush itemBgBrush = palette.itemBackground();
```

### 3.2 设置颜色

```cpp
#include <DPalette>

DPalette palette;

// 设置当前颜色组的颜色
palette.setColor(DPalette::TextTitle, QColor("#303030"));
palette.setColor(DPalette::TextWarning, QColor("#FF5722"));

// 设置指定颜色组的颜色
palette.setColor(QPalette::Disabled, DPalette::TextTitle, QColor("#999999"));

// 设置画笔
palette.setBrush(DPalette::ItemBackground, QBrush(QColor("#F5F5F5")));

// 设置应用调色板
DGuiApplicationHelper::instance()->setApplicationPalette(palette);
```

### 3.3 生成调色板

```cpp
#include <DGuiApplicationHelper>

DPalette palette;

// 从 QPalette::ColorRole 生成颜色
DGuiApplicationHelper::generatePaletteColor(palette, QPalette::WindowText, 
    DGuiApplicationHelper::LightType);

// 从 DPalette::ColorType 生成颜色
DGuiApplicationHelper::generatePaletteColor(palette, DPalette::TextTitle, 
    DGuiApplicationHelper::LightType);

// 生成完整调色板
DGuiApplicationHelper::generatePalette(palette, DGuiApplicationHelper::DarkType);
```

### 3.4 DGuiApplicationHelper 核心 Palette API

```cpp
#include <DGuiApplicationHelper>

// 获取应用调色板
DPalette appPalette = DGuiApplicationHelper::instance()->applicationPalette();

// 获取指定主题类型的应用调色板
DPalette lightAppPalette = DGuiApplicationHelper::instance()->applicationPalette(
    DGuiApplicationHelper::LightType);
DPalette darkAppPalette = DGuiApplicationHelper::instance()->applicationPalette(
    DGuiApplicationHelper::DarkType);

// 获取标准调色板（系统默认）
DPalette standardLight = DGuiApplicationHelper::standardPalette(
    DGuiApplicationHelper::LightType);
DPalette standardDark = DGuiApplicationHelper::standardPalette(
    DGuiApplicationHelper::DarkType);

// 从 DPlatformTheme 获取调色板
DPlatformTheme *theme = DGuiApplicationHelper::instance()->applicationTheme();
DPalette palette = DGuiApplicationHelper::fetchPalette(theme);
```

### 3.5 颜色调整

```cpp
#include <DGuiApplicationHelper>

QColor baseColor(100, 150, 200);

// 调整颜色（各参数为相对偏移量 -128 ~ 127）
QColor adjusted = DGuiApplicationHelper::adjustColor(
    baseColor, 
    10,   // 色相偏移
    20,   // 饱和度偏移
    -10,  // 明度偏移
    0,    // R 偏移
    0,    // G 偏移
    0,    // B 偏移
    0     // Alpha 偏移
);

// 混合两个颜色
QColor blended = DGuiApplicationHelper::blendColor(
    QColor("#FF0000"),  // 底色
    QColor("#0000FF")   // 叠加色
);
```

## 4. 与 DStyle 的关系

`DStyle` 提供了根据控件状态自动处理颜色的功能：

```cpp
#include <DStyle>
#include <DPalette>

// 在自定义控件的 paintEvent 中使用
void MyWidget::paintEvent(QPaintEvent *event) {
    QPainter painter(this);
    DStyleHelper helper(style());
    
    // 获取经过状态处理的颜色（自动处理 hover/press 等）
    QColor bgColor = helper.getColor(this, DPalette::ItemBackground);
    QColor textColor = helper.getColor(this, DPalette::TextTitle);
    
    painter.fillRect(rect(), bgColor);
    painter.setPen(textColor);
    painter.drawText(rect(), Qt::AlignCenter, "Hello");
}
```

### 4.1 generatedBrush 方法

```cpp
#include <DStyle>

DStyleHelper helper(style());

// 根据状态生成画笔
QBrush brush = helper.generatedBrush(
    option,                    // QStyleOption
    palette.brush(DPalette::ItemBackground),  // 基础画笔
    QPalette::Normal,          // 颜色组
    DPalette::ItemBackground   // 颜色类型
);

// 使用 DStyle 状态标志
QBrush brush = helper.generatedBrush(
    DStyle::SS_HoverState | DStyle::SS_FocusFlag,  // 状态
    baseBrush,
    QPalette::Normal,
    DPalette::ItemBackground,
    option
);
```

## 5. 主题切换时调色板更新

```cpp
#include <DGuiApplicationHelper>
#include <DPalette>

class MyWidget : public QWidget {
public:
    MyWidget(QWidget *parent = nullptr) : QWidget(parent) {
        connect(DGuiApplicationHelper::instance(), 
                &DGuiApplicationHelper::themeTypeChanged,
                this, &MyWidget::onThemeChanged);
    }

private:
    void onThemeChanged(DGuiApplicationHelper::ColorType type) {
        // 调色板会自动更新，只需刷新绘制
        update();
    }
};
```

### 5.1 监听调色板变化

```cpp
connect(DGuiApplicationHelper::instance(), 
        &DGuiApplicationHelper::applicationPaletteChanged,
        this, [this]() {
    // 应用调色板已更改
    update();
});
```

## 6. 完整示例

### 6.1 自定义控件使用 DPalette

```cpp
#include <DPalette>
#include <DGuiApplicationHelper>
#include <DStyle>
#include <QPainter>

class StatusLabel : public QWidget {
public:
    StatusLabel(const QString &text, QWidget *parent = nullptr)
        : QWidget(parent), m_text(text) {
        setFixedHeight(40);
    }

    void setType(DPalette::ColorType type) {
        m_colorType = type;
        update();
    }

protected:
    void paintEvent(QPaintEvent *) override {
        QPainter painter(this);
        DStyleHelper helper(style());
        
        // 获取背景色
        QColor bgColor = helper.getColor(this, DPalette::ItemBackground);
        painter.fillRect(rect(), bgColor);
        
        // 获取文本颜色
        QColor textColor = helper.getColor(this, m_colorType);
        painter.setPen(textColor);
        painter.drawText(rect(), Qt::AlignCenter, m_text);
    }

private:
    QString m_text;
    DPalette::ColorType m_colorType = DPalette::TextTitle;
};
```

### 6.2 判断颜色主题类型

```cpp
#include <DGuiApplicationHelper>

QColor color(50, 50, 50);

// 根据颜色亮度判断主题类型
DGuiApplicationHelper::ColorType type = 
    DGuiApplicationHelper::toColorType(color);

if (type == DGuiApplicationHelper::DarkType) {
    // 颜色偏深色
} else {
    // 颜色偏浅色
}
```

## 7. QSS 注意事项

DTK 应用**不要使用 QSS（Qt Style Sheets）** 设置颜色样式。QSS 会绕过 DTK
主题系统，硬编码的颜色无法跟随系统亮暗主题切换。

```cpp
// ❌ 错误：QSS 硬编码颜色，不响应主题切换
widget->setStyleSheet("background-color: #f0f0f0; color: #1a1a1a;");

// ✅ 正确：使用 DPalette 语义化颜色
DPalette dp = widget->palette();
dp.setColor(DPalette::ItemBackground, QColor("#f0f0f0"));
dp.setColor(DPalette::TextTitle, QColor("#1a1a1a"));
widget->setPalette(dp);
```

## 8. 相关文档

- [index.md](index.md) - 主题系统总览（含图标）
- [Widget 控件风格](../widgets/style.md) - DStyle 风格规范
- [theme-switch.md](theme-switch.md) - 主题切换机制
