# 窗口规范

## 1. 概述与适用场景

DTK 提供 `DMainWindow` 作为主窗口基类，自动集成：
- 标题栏（`DTitlebar`）
- 窗口圆角和阴影
- 侧边栏支持
- 主题感知

**适用场景：**
- DDE 应用的主窗口
- 需要标题栏自定义的窗口
- 需要侧边栏布局的窗口

**不适用场景：**
- 对话框 → 使用 `DDialog`
- 工具窗口 → 使用 `QWidget` + `DPlatformWindowHandle`

## 2. DMainWindow 核心用法

### 2.1 基本窗口

```cpp
#include <DMainWindow>
#include <DWidgetUtil>

class MainWindow : public DMainWindow {
public:
    MainWindow() {
        setCentralWidget(new QLabel("Hello DTK"));
        resize(800, 600);
    }
};

// main.cpp
#include <DApplication>

int main(int argc, char *argv[]) {
    DApplication a(argc, argv);
    MainWindow w;
    w.show();
    return a.exec();
}
```

### 2.2 标题栏操作

```cpp
#include <DMainWindow>

class MainWindow : public DMainWindow {
public:
    MainWindow() {
        // 获取标题栏
        DTitlebar *tb = titlebar();
        
        // 设置标题
        tb->setTitle("我的应用");
        
        // 设置图标
        tb->setIcon(QIcon(":/icon.png"));
        
        // 设置菜单
        auto *menu = new QMenu(this);
        menu->addAction("设置", this, &MainWindow::openSettings);
        menu->addAction("关于", this, &MainWindow::showAbout);
        tb->setMenu(menu);
        
        // 隐藏菜单按钮
        tb->setMenuVisible(false);
        
        // 禁用主题切换菜单
        tb->setSwitchThemeMenuVisible(false);
    }
};
```

### 2.3 侧边栏

```cpp
#include <DMainWindow>

class MainWindow : public DMainWindow {
public:
    MainWindow() {
        // 创建侧边栏
        auto *sidebar = new QWidget(this);
        auto *sidebarLayout = new QVBoxLayout(sidebar);
        sidebarLayout->addWidget(new QPushButton("选项1"));
        sidebarLayout->addWidget(new QPushButton("选项2"));
        
        // 设置侧边栏
        setSidebarWidget(sidebar);
        setSidebarWidth(200);
        setSidebarVisible(true);
        
        // 折叠/展开
        setSidebarExpanded(true);
    }
};
```

### 2.4 窗口效果

```cpp
// 圆角
setWindowRadius(10);

// 边框
setBorderWidth(1);
setBorderColor(QColor(0, 0, 0, 30));

// 阴影
setShadowRadius(20);
setShadowOffset(QPoint(0, 5));
setShadowColor(QColor(0, 0, 0, 50));

// 半透明背景
setTranslucentBackground(true);

// 模糊窗口
setEnableBlurWindow(true);
```

### 2.5 消息提示

```cpp
#include <DFloatingMessage>

// 简单消息
sendMessage(QIcon(), "操作成功");

// 自定义消息
auto *msg = new DFloatingMessage(DFloatingMessage::TransientType, this);
msg->setMessage("正在处理...");
sendMessage(msg);
```

## 3. DTitlebar 自定义

### 3.1 添加控件

```cpp
DTitlebar *tb = titlebar();

// 添加控件到标题栏
auto *searchEdit = new DSearchEdit(this);
tb->addWidget(searchEdit, Qt::AlignLeft);

// 自定义控件（居中）
auto *customWidget = new QWidget(this);
tb->setCustomWidget(customWidget, true); // true = 居中
```

### 3.2 禁用按钮

```cpp
// 禁用最大化按钮
tb->setDisableFlags(Qt::WindowMaximizeButtonHint);

// 隐藏全屏按钮
tb->setFullScreenButtonVisible(false);
```

## 4. 关键 API

### DMainWindow

| 方法 | 说明 |
|------|------|
| `titlebar()` | 获取标题栏对象 |
| `setSidebarWidget(QWidget*)` | 设置侧边栏 |
| `setSidebarWidth(int)` | 设置侧边栏宽度 |
| `setSidebarVisible(bool)` | 显示/隐藏侧边栏 |
| `setSidebarExpanded(bool)` | 展开/折叠侧边栏 |
| `setWindowRadius(int)` | 设置圆角 |
| `setTranslucentBackground(bool)` | 设置半透明背景 |
| `sendMessage(QIcon, QString)` | 显示消息 |

### DTitlebar

| 方法 | 说明 |
|------|------|
| `setTitle(QString)` | 设置标题 |
| `setIcon(QIcon)` | 设置图标 |
| `setMenu(QMenu*)` | 设置菜单 |
| `setMenuVisible(bool)` | 显示/隐藏菜单按钮 |
| `addWidget(QWidget*, alignment)` | 添加控件 |
| `setCustomWidget(QWidget*, fixCenter)` | 设置自定义控件 |
| `setDisableFlags(Qt::WindowFlags)` | 禁用窗口按钮 |
| `setSplitScreenEnabled(bool)` | 启用分屏按钮 |

## 5. 常见错误与避坑

### 错误 1：使用废弃的 sidebarVisble

```cpp
// ❌ 错误：sidebarVisble 拼写错误且已废弃
bool visible = sidebarVisble();

// ✅ 正确：使用 sidebarVisible
bool visible = sidebarVisible();
```

### 错误 2：未设置 DApplication

```cpp
// ❌ 错误：使用 QApplication，无法获取 DTK 特性
QApplication app(argc, argv);

// ✅ 正确：使用 DApplication
DApplication app(argc, argv);
```

### 错误 3：窗口效果未生效

```cpp
// 需要平台支持，检查是否为 DXcb 窗口
if (isDXcbWindow()) {
    setWindowRadius(10);
    setEnableBlurWindow(true);
}
```

## 6. 相关文档

- [index.md](index.md) - 控件选择决策树
- [dialog.md](dialog.md) - 对话框规范
- [application.md](application.md) - DApplication 应用入口
- [blur-effect.md](blur-effect.md) - DBlurEffectWidget 模糊效果
