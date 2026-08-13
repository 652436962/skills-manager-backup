# DApplication 应用类

## 1. 概述与适用场景

`DApplication`（dtkwidget）是 DTK 应用的入口类，替代 `QApplication`。它提供单实例控制、翻译加载、关于对话框、产品信息等 DDE 应用标准功能。

**适用场景：**
- 所有 DDE 应用的 main 函数入口
- 单实例应用控制
- 加载翻译文件
- 设置产品信息（名称/图标/描述/许可证）

## 2. 基本用法

### 2.1 替代 QApplication

```cpp
#include <DApplication>
#include <DMainWindow>
#include <DWidgetUtil>
#include <DIconTheme>

int main(int argc, char *argv[]) {
    DApplication a(argc, argv);
    a.setApplicationName("my-app");

    a.setProductName("我的应用");
    a.setProductIcon(DIconTheme::findQIcon("my-app"));
    a.setApplicationDescription("这是一个示例应用");
    a.setApplicationHomePage("https://example.com");
    a.setApplicationLicense("GPLv3");

    a.loadTranslator();

    DMainWindow w;
    w.show();
    DApplication::setOOMScoreAdj(0);
    return a.exec();
}
```

> DTK 重定义了 `qApp` 宏为 `DApplication*`，可直接使用 `qApp->xxx()` 访问 DTK 扩展方法。

## 3. 单实例控制

可执行文件名、`applicationName`、应用 ID 和单实例 key 是不同概念。通常将 `applicationName` 设置为可执行文件名，将稳定且唯一的应用 ID 用作单实例 key。DConfig 默认通过 `DSGApplication::id()` 获取 appId，只有默认值无法满足需求时才显式指定其他 appId。

```cpp
DApplication a(argc, argv);

if (!a.setSingleInstance("org.deepin.dtk.myapp")) {
    qWarning() << "Another instance is running";
    return 0;
}

// 带作用域
a.setSingleInstance("org.deepin.dtk.myapp", DApplication::UserScope);
```

监听新实例启动：

```cpp
DMainWindow w;
connect(&a, &DApplication::newInstanceStarted, &w, [&w]() {
    if (w.isMinimized())
        w.showNormal();
    else
        w.show();
    w.raise();
    w.activateWindow();
});
```

## 4. 翻译加载

```cpp
// 必须在创建任何可翻译 UI 前加载翻译。
// QM 文件 basename 应与 applicationName 一致。
a.loadTranslator();

// 指定语言回退
a.loadTranslator(QList<QLocale>() << QLocale::Chinese << QLocale::English);
```

`DApplication::translate()` 是 DTK 中使用最频繁的方法之一：

```cpp
QString text = DApplication::translate("Context", "Source Text");
```

专业单位不应进入翻译，例如：

```cpp
const QString unit = QStringLiteral("px");
```

## 5. 产品信息

```cpp
a.setProductName("文件管理器");
a.setProductIcon(DIconTheme::findQIcon("deepin-file-manager"));
a.setApplicationDescription("深度文件管理器");
a.setApplicationHomePage("https://www.deepin.org");
a.setApplicationAcknowledgementPage("https://www.deepin.org/acknowledgement");
a.setApplicationAcknowledgementVisible(true);
a.setApplicationLicense("GPLv3");
```

## 6. 菜单显示控制

```cpp
// 菜单项显示快捷键文本
a.setVisibleMenuShortcutText(true);

// 菜单项显示复选框
a.setVisibleMenuCheckboxWidget(true);

// 菜单项显示图标
a.setVisibleMenuIcon(true);
```

## 7. 关于对话框

```cpp
// 自动生成关于对话框
// 需要先设置 productName/productIcon/applicationDescription 等
a.setApplicationCreditsFile(":/credits.html");
a.setLicensePath(":/license/gpl-3.0.txt");

// 自定义关于对话框
auto *aboutDlg = new DAboutDialog(this);
a.setAboutDialog(aboutDlg);
```

## 8. 版本信息

```cpp
// 编译时 DTK 版本
int buildVer = DApplication::buildDtkVersion();

// 运行时 DTK 版本
int runtimeVer = DApplication::runtimeDtkVersion();

// 应用构建版本（使用 VERSION 宏）
QString ver = DApplication::buildVersion("1.0.0");
```

## 9. 虚拟键盘适配

```cpp
// 适配虚拟键盘（平板模式）
a.acclimatizeVirtualKeyboard(mainWindow);

// 忽略虚拟键盘
a.ignoreVirtualKeyboard(someWindow);

// 查询状态
bool adapted = a.isAcclimatizedVirtualKeyboard(mainWindow);
```

## 10. 自定义 Help/About/Quit 处理

```cpp
class MyHandler : public DAppHandler {
    void handleHelpAction() override { /* 打开帮助 */ }
    void handleAboutAction() override { /* 显示关于 */ }
    void handleQuitAction() override { /* 自定义退出 */ }
};

a.setCustomHandler(new MyHandler);
```

## 11. 信号

| 信号 | 说明 |
|------|------|
| `newInstanceStarted()` | 新实例启动 |
| `iconThemeChanged()` | 图标主题变化 |
| `screenDevicePixelRatioChanged(QScreen*)` | 屏幕 DPI 变化 |

## 12. 常见错误与避坑

### 错误 1：使用 QApplication 而非 DApplication

```cpp
// ❌ 错误：无法获取 DTK 特性
QApplication app(argc, argv);

// ✅ 正确：使用 DApplication
DApplication app(argc, argv);
```

### 错误 2：单实例 key 冲突

```cpp
// ❌ 错误：多个应用使用相同 key
a.setSingleInstance("deepin-app");

// ✅ 正确：使用应用专属 key
a.setSingleInstance("org.deepin.file-manager");
```

### 错误 3：loadTranslator 位置错误

```cpp
// ❌ 错误：在创建窗口后才加载翻译
DMainWindow w;
w.show();
a.loadTranslator(); // 窗口文字未翻译

// ✅ 正确：在创建窗口前加载
a.loadTranslator();
DMainWindow w;
w.show();
```

## 13. 相关文档

- [window.md](window.md) - 窗口规范
- [../utilities/gui-helper.md](../utilities/gui-helper.md) - DGuiApplicationHelper
- [../utilities/log.md](../utilities/log.md) - 日志系统
