# 图标主题规范

## 1. 概述与适用场景

**DIconTheme** 是 DTK 的统一主题图标查找入口，兼容 DCI、builtin 和 XDG 图标主题，并负责按名称选择可用图标。它也提供与系统 XDG 图标主题交互的能力。特点：

- **XDG 兼容**：遵循 freedesktop.org 图标主题规范
- **系统集成**：自动读取系统图标主题配置
- **多主题支持**：按名称自动选择 DCI 的主题、尺寸和状态资源
- **缓存优化**：内置图标缓存，提升查找性能

**适用场景：**
- 应用控件需要使用 DCI、builtin 或 XDG 主题图标
- 需要兼容其他桌面环境的应用
- 使用系统图标主题的图标
- 跨桌面应用开发

**不适用场景：**
- DDE 应用自定义图标 → 使用 **dci 图标**
- 需要动画效果 → 使用 **dci 图标**
- DTK 标准 UI 图标 → 使用 **builtin 图标**

## 2. 与系统图标主题的交互

### 2.1 图标主题搜索路径

DIconTheme 遵循 XDG 基础目录规范，在以下路径搜索图标：

```
~/.local/share/icons/
~/.icons/
/usr/share/icons/
/usr/share/pixmaps/
```

### 2.2 DCI 图标使用原则

应用先按 DCI 规范组织主题、尺寸和状态资源，再通过基础名称调用 `DIconTheme::findQIcon()`。大多数应用无需调用 `setDciThemeSearchPaths()`；只有确实使用自定义 DCI 搜索根目录时才配置它，并注意该 API 会改变整个进程的查找行为。

DTK builtin 资源同样只传基础名称。即使内部资源位于 `/dsg/built-in-icons` 前缀，也应写成 `DIconTheme::findQIcon("default")`，不应在业务代码中展开资源路径。

## 3. API 用法

### 3.1 查找图标

```cpp
#include <DIconTheme>

// 查找图标（按优先级：dci → builtin → icon theme）
QIcon icon = DIconTheme::findQIcon("document-open");

// 查找图标，带回退
QIcon fallback = DIconTheme::findQIcon("default");
QIcon icon = DIconTheme::findQIcon("document-open", fallback);

// 查找图标，带选项
QIcon icon = DIconTheme::findQIcon("document-open", 
    DIconTheme::Options());
```

**⚠️ 参数顺序差异**

顶层 API `DIconTheme::findQIcon()` 与 `DIconTheme::Cached::findQIcon()` 参数顺序不同：

```cpp
// 顶层 API（无缓存）：iconName, fallback, options
QIcon DIconTheme::findQIcon(const QString &iconName, const QIcon &fallback, Options options);

// Cached API：iconName, options, fallback  （顺序不同！）
QIcon DIconTheme::Cached::findQIcon(const QString &iconName, Options options, const QIcon &fallback);
```

使用缓存查找时注意参数顺序：

```cpp
auto *cache = DIconTheme::cached();

// ⚠️ Cached::findQIcon 参数顺序：iconName, options, fallback
QIcon icon = cache->findQIcon("my-icon", DIconTheme::Options(), fallbackIcon);
```

### 3.2 创建图标引擎

```cpp
#include <DIconTheme>

// 创建图标引擎（用于自定义绘制）
QIconEngine *engine = DIconTheme::createIconEngine("my-icon", 
    DIconTheme::DontFallbackToQIconFromTheme);

QIcon icon(engine);
```

### 3.3 查找 dci 图标文件

```cpp
#include <DIconTheme>

// 仅在调试图标发现问题时查找实际文件；普通控件不需要路径
QString dciPath = DIconTheme::findDciIconFile("my-icon", "deepin");

不要在应用控件中依赖这个实际路径，也不要用它替代按名称查找；应用资源应按 DCI 规则组织并交给 DTK 查找链路处理。
```

### 3.4 图标类型检查

```cpp
#include <DIconTheme>

QIcon icon = DIconTheme::findQIcon("document-open");

// 检查是否为内置图标
if (DIconTheme::isBuiltinIcon(icon)) {
    qInfo() << "This is a builtin icon";
}

// 检查是否为 XDG 图标主题图标
if (DIconTheme::isXdgIcon(icon)) {
    qInfo() << "This is an XDG icon theme icon";
}
```

### 3.5 缓存管理

```cpp
#include <DIconTheme>

// 获取缓存实例
auto *cache = DIconTheme::cached();

// 查找缓存中的图标
QIcon cachedIcon = cache->findQIcon("document-open");

// 查找缓存中的 dci 文件路径
QString dciPath = cache->findDciIconFile("my-icon", "deepin");

// 设置缓存上限
cache->setMaxCost(1024 * 1024); // 1MB

// 清除缓存
cache->clear();
```

## 4. 主题切换时的图标更新

当系统主题切换时，需要更新使用 DIconTheme 的图标：

```cpp
#include <DIconTheme>
#include <DGuiApplicationHelper>
#include <QLabel>

class ThemeAwareIconLabel : public QLabel {
public:
    ThemeAwareIconLabel(const QString &iconName, QWidget *parent = nullptr)
        : QLabel(parent), m_iconName(iconName) {
        updateIcon();
        connect(DGuiApplicationHelper::instance(), 
                &DGuiApplicationHelper::themeTypeChanged,
                this, &ThemeAwareIconLabel::updateIcon);
    }

private:
    void updateIcon() {
        QIcon icon = DIconTheme::findQIcon(m_iconName);
        setPixmap(icon.pixmap(32));
    }
    QString m_iconName;
};
```

## 5. 完整示例

### 5.1 使用系统图标主题

```cpp
#include <DIconTheme>
#include <QAction>
#include <QToolBar>

class MainWindow : public QMainWindow {
public:
    MainWindow() {
        auto *toolbar = addToolBar("Main Toolbar");
        
        // 使用系统图标主题的图标
        auto *newAction = new QAction(
            DIconTheme::findQIcon("document-new"), "新建", this);
        auto *openAction = new QAction(
            DIconTheme::findQIcon("document-open"), "打开", this);
        auto *saveAction = new QAction(
            DIconTheme::findQIcon("document-save"), "保存", this);
        
        toolbar->addAction(newAction);
        toolbar->addAction(openAction);
        toolbar->addAction(saveAction);
    }
};
```

### 5.2 带缓存的图标查找

```cpp
#include <DIconTheme>

class IconManager {
public:
    static IconManager *instance() {
        static IconManager mgr;
        return &mgr;
    }

    QIcon icon(const QString &name) {
        auto *cache = DIconTheme::cached();
        return cache->findQIcon(name);
    }

    void clearCache() {
        DIconTheme::cached()->clear();
    }
};
```

## 6. 相关文档

- [index.md](index.md) - 图标系统决策树
- [dci.md](dci.md) - dci 图标规范
- [builtin.md](builtin.md) - builtin 图标规范
- [../theme/palette.md](palette.md) - 调色板与主题配色
