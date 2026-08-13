# 主题切换机制

## 1. 概述与适用场景

DTK 应用需要响应系统主题变化，在亮色和暗色主题之间切换时自动更新界面颜色、图标等视觉元素。

**适用场景：**
- 自定义控件需要响应主题变化
- 应用需要手动切换主题
- 界面元素需要根据主题选择不同资源（如图标）

**相关接口：**
- `DGuiApplicationHelper::themeTypeChanged` 信号 — 监听主题类型变化
- `DGuiApplicationHelper::applicationPaletteChanged` 信号 — 监听调色板变化
- `DGuiApplicationHelper::themeType()` — 获取当前主题类型
- `DGuiApplicationHelper::setPaletteType()` — 手动设置主题

## 2. 监听主题变化

```cpp
#include <DGuiApplicationHelper>

// 监听主题类型变化
connect(DGuiApplicationHelper::instance(), 
        &DGuiApplicationHelper::themeTypeChanged,
        this, &MyWidget::onThemeChanged);

// 监听调色板变化
connect(DGuiApplicationHelper::instance(),
        &DGuiApplicationHelper::applicationPaletteChanged,
        this, &MyWidget::onPaletteChanged);
```

## 3. 响应主题切换

```cpp
void MyWidget::onThemeChanged(DGuiApplicationHelper::ColorType type) {
    // 刷新图标
    if (type == DGuiApplicationHelper::DarkType) {
        m_icon = DDciIcon::Dark;
    } else {
        m_icon = DDciIcon::Light;
    }
    update();
}
```

## 4. 手动切换主题

```cpp
#include <DGuiApplicationHelper>

// 切换到深色主题
DGuiApplicationHelper::instance()->setPaletteType(DGuiApplicationHelper::DarkType);

// 切换到浅色主题
DGuiApplicationHelper::instance()->setPaletteType(DGuiApplicationHelper::LightType);
```

## 5. 相关文档

- [palette.md](palette.md) - 调色板规范
- [Widget 控件风格](../widgets/style.md) - 风格规范
