# dci 图标规范

## 1. 概述与适用场景

**dci** (Deepin Component Icon) 是 DTK 自有的矢量图标格式，基于 `DDciFile` 封装，支持：

- **多主题**：内置 Light/Dark 两套图标，自动适配主题切换
- **多状态**：Normal/Disabled/Hover/Pressed 四种状态
- **动画**：支持逐帧动画，通过 `DDciIconPlayer` 驱动
- **调色板着色**：通过 `DDciIconPalette` 对图标前景/背景着色

**适用场景：**
- 需要跟随主题切换的图标
- 需要动画效果的图标（如加载动画）
- 需要多状态展示的图标
- DDE 应用内的自定义图标

**不适用场景：**
- 仅需 XDG 图标主题中的标准图标 → 仍通过 `DIconTheme::findQIcon()` 统一查找
- DTK 已提供的标准 UI 图标 → 直接使用对应的 builtin 图标名称

## 2. 文件格式规范

### 2.1 目录结构

dci 是一个包含主题、尺寸和状态资源的容器文件，不应把 Light/Dark 或不同尺寸拆成多个同名 `.dci` 文件。制作图标时应先按 DCI 规则组织源资源，再生成单个 `.dci`：

```
my-icon/
├── light/
│   ├── normal/
│   ├── hover/
│   ├── pressed/
│   └── disabled/
└── dark/
    ├── normal/
    ├── hover/
    ├── pressed/
    └── disabled/

# 上述主题/状态及各尺寸资源最终生成：my-icon.dci
```

### 2.2 命名规则

- 文件名使用小写字母和连字符：`my-icon-name.dci`
- 一个逻辑图标生成一个 `.dci` 文件，Light/Dark、尺寸和状态均由文件内部资源表达
- 同一图标各主题、尺寸和状态的源资源必须保持一致的语义和画布规则
- 打开、关闭、添加等通用操作先查找 DTK 已有图标；只有应用专属图标才新增 DCI

### 2.3 使用原则

应用应按 DCI 规范组织图标并通过名称使用。大多数应用不需要修改 DCI 搜索路径；只有确实使用自定义 DCI 搜索根目录时，才配置 `setDciThemeSearchPaths()`：

```cpp
#include <DIconTheme>

QIcon icon = DIconTheme::findQIcon("my-icon");
button->setIcon(icon);
```

如果确实需要使用自定义 DCI 搜索根目录，可在图标查找前配置；这不是普通应用的必需步骤：

```cpp
QStringList paths = DIconTheme::dciThemeSearchPaths();
paths.append("/path/to/custom-dci-root");
DIconTheme::setDciThemeSearchPaths(paths);
```

`DIconTheme::setDciThemeSearchPaths()` 会影响整个进程的图标查找行为。常规应用应先按 DCI 规范组织资源并使用默认搜索链路；不要为了修复图标名称、目录或资源组织错误而调用该 API，也不要把 `:/icons`、`/usr/share/icons` 等不符合 DCI 规则的目录当作通用配置。

## 3. API 用法

### 3.1 按名称加载图标

```cpp
#include <DIconTheme>

// 应用控件统一按名称加载
QIcon icon = DIconTheme::findQIcon("my-icon-name");

// 回退图标同样按名称加载
QIcon fallback = DIconTheme::findQIcon("default");
QIcon iconWithFallback = DIconTheme::findQIcon("my-icon-name", fallback);
```

即使图标位于 DTK 的 `/dsg/built-in-icons` 资源前缀下，调用方也只传基础名称，例如 `default`。不要写成 `:/dsg/built-in-icons/default.dci` 或其他资源绝对路径。

只有播放 DCI 动画、读取 DCI 属性或自行绘制时才直接使用 `DDciIcon::fromTheme("my-icon-name")`。

### 3.2 显示图标

```cpp
#include <DDciIcon>
#include <DGuiApplicationHelper>

DDciIcon icon = DDciIcon::fromTheme("my-icon");
auto theme = DGuiApplicationHelper::instance()->themeType() == DGuiApplicationHelper::DarkType
             ? DDciIcon::Dark : DDciIcon::Light;

// 获取 QPixmap
qreal dpr = widget->devicePixelRatioF();
QPixmap pix = icon.pixmap(dpr, 32, theme, DDciIcon::Normal);
label->setPixmap(pix);

// 直接绘制
QPainter painter(this);
icon.paint(&painter, rect, dpr, theme, DDciIcon::Normal);
```

### 3.3 主题切换

```cpp
// 监听主题切换信号，刷新图标
connect(DGuiApplicationHelper::instance(), &DGuiApplicationHelper::themeTypeChanged,
        this, &MyWidget::updateIcon);

void MyWidget::updateIcon() {
    auto theme = DGuiApplicationHelper::instance()->themeType() == DGuiApplicationHelper::DarkType
                 ? DDciIcon::Dark : DDciIcon::Light;
    m_pixmap = m_icon.pixmap(devicePixelRatioF(), 32, theme);
    update();
}
```

### 3.4 调色板着色

```cpp
#include <DDciIconPalette>

// 从 QPalette 创建调色板
DDciIconPalette palette = DDciIconPalette::fromQPalette(qApp->palette());

// 自定义调色板
DDciIconPalette palette(QColor("#000000"), QColor("#ffffff"),
                        QColor("#007AFF"), QColor("#ffffff"));

// 使用调色板渲染图标
QPixmap pix = icon.pixmap(dpr, 32, theme, DDciIcon::Normal, palette);
```

#### DDciIconPalette 颜色角色

`DDciIconPalette` 定义四个颜色角色，用于控制 dci 图标的着色：

| 颜色角色 | 方法 | 用途 |
|----------|------|------|
| `Foreground` | `foreground()` / `setForeground()` | 前景色（图标主体颜色） |
| `Background` | `background()` / `setBackground()` | 背景色（图标填充颜色） |
| `Highlight` | `highlight()` / `setHighlight()` | 高亮色（选中/激活状态） |
| `HighlightForeground` | `highlightForeground()` / `setHighlightForeground()` | 高亮前景色 |

```cpp
DDciIconPalette palette;

// 设置前景色（图标线条/填充的主体颜色）
palette.setForeground(QColor("#303030"));

// 设置背景色（图标背景填充）
palette.setBackground(QColor("#FFFFFF"));

// 设置高亮色（选中状态背景）
palette.setHighlight(QColor("#007AFF"));

// 设置高亮前景色（选中状态文字/图标）
palette.setHighlightForeground(QColor("#FFFFFF"));

// 转换为字符串（用于序列化）
QString str = DDciIconPalette::convertToString(palette);

// 从字符串恢复
DDciIconPalette restored = DDciIconPalette::convertFromString(str);
```

### 3.5 检查图标属性

```cpp
// 获取可用尺寸
QList<int> sizes = icon.availableSizes(DDciIcon::Light, DDciIcon::Normal);

// 检查是否支持调色板
bool hasPalette = icon.isSupportedAttribute(result, DDciIcon::HasPalette);

// 检查是否为空
if (icon.isNull()) { /* 加载失败 */ }
```

## 4. 完整示例

### 4.1 静态图标

```cpp
#include <DDciIcon>
#include <DGuiApplicationHelper>
#include <QLabel>

class ThemeIconLabel : public QLabel {
public:
    ThemeIconLabel(const QString &iconName, int size = 32, QWidget *parent = nullptr)
        : QLabel(parent), m_size(size) {
        m_icon = DDciIcon::fromTheme(iconName);
        refreshPixmap();
        connect(DGuiApplicationHelper::instance(), &DGuiApplicationHelper::themeTypeChanged,
                this, &ThemeIconLabel::refreshPixmap);
    }
    void refreshPixmap() {
        auto theme = DGuiApplicationHelper::instance()->themeType()
                     == DGuiApplicationHelper::DarkType ? DDciIcon::Dark : DDciIcon::Light;
        setPixmap(m_icon.pixmap(devicePixelRatioF(), m_size, theme));
    }
private:
    DDciIcon m_icon; int m_size;
};
```

### 4.2 动态图标（动画）

```cpp
#include <DDciIcon>
#include <DDciIconPlayer>
#include <DGuiApplicationHelper>
#include <QLabel>

class AnimatedIconLabel : public QLabel {
public:
    AnimatedIconLabel(const QString &iconName, int size = 32, QWidget *parent = nullptr)
        : QLabel(parent) {
        auto *player = new DDciIconPlayer(this);
        player->setIcon(DDciIcon::fromTheme(iconName));
        player->setIconSize(size);
        auto theme = DGuiApplicationHelper::instance()->themeType()
                     == DGuiApplicationHelper::DarkType ? DDciIcon::Dark : DDciIcon::Light;
        player->setTheme(theme);
        connect(player, &DDciIconPlayer::updated, this, [=]() {
            setPixmap(QPixmap::fromImage(player->currentImage()));
        });
        player->play(DDciIcon::Normal);
    }
};
```

## 5. 与 builtin/icontheme 的选择建议

| 对比项 | dci 图标 | builtin 图标 | icon theme 图标 |
|--------|----------|-------------|----------------|
| 主题切换 | ✅ 内置支持 | ✅ 内置支持 | ⚠️ 需手动处理 |
| 动画 | ✅ 支持 | ❌ 不支持 | ❌ 不支持 |
| 调色板着色 | ✅ 支持 | ❌ 不支持 | ❌ 不支持 |
| 多状态 | ✅ 4 种状态 | ❌ 2 种状态 | ❌ 2 种状态 |
| XDG 兼容 | ❌ DTK 专用 | ❌ DTK 专用 | ✅ 标准规范 |
| 图标来源 | 需提供 .dci 文件 | DTK 内置 | 系统图标主题 |
| 适用场景 | DDE 应用自定义图标 | DTK 标准 UI 图标 | 跨桌面兼容图标 |

**选择建议：**
- DDE 应用内的功能性图标 → **dci 图标**
- DTK 标准控件图标（如对话框按钮） → **builtin 图标**
- 需要兼容其他桌面环境 → **icon theme 图标**
