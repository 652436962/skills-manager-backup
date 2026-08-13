# DDBusSender DBus 通信

## 1. 概述与适用场景

`DDBusSender`（dtkcore）提供流畅构建器模式的 DBus 方法调用。与 `QDBusInterface` 相比，它不需要 introspection 开销，适合简单的 DBus 调用。

**适用场景：**
- 调用 DBus 方法
- 读写 DBus 属性
- 简单的 Session/System Bus 通信

## 2. 流畅构建器模式

`DDBusSender` 使用链式调用构建 DBus 请求，核心是三步：`service → path → interface → method/property`。

### 2.1 方法调用

```cpp
#include <DDBusSender>

// Session Bus 调用（无参数）
DDBusSender()
    .service("org.deepin.dde.Launcher1")
    .path("/org/deepin/dde/Launcher1")
    .interface("org.deepin.dde.Launcher1")
    .method("Show")
    .call();

// 发送系统通知（Notify 方法完整示例）
DDBusSender()
    .service("org.freedesktop.Notifications")
    .path("/org/freedesktop/Notifications")
    .interface("org.freedesktop.Notifications")
    .method("Notify")
    .arg(QString("MyApp"))           // app_name
    .arg(0U)                          // replaces_id
    .arg(QString("dialog-information")) // app_icon
    .arg(QString("通知标题"))          // summary
    .arg(QString("通知内容"))          // body
    .arg(QStringList())               // actions
    .arg(QVariantMap())               // hints
    .arg(5000)                        // expire_timeout
    .call();

// System Bus 调用
DDBusSender::system()
    .service("org.freedesktop.login1")
    .path("/org/freedesktop/login1")
    .interface("org.freedesktop.login1.Manager")
    .method("PowerOff")
    .arg(false)
    .call();
```

### 2.2 属性读取

```cpp
QDBusPendingCall reply = DDBusSender()
    .service("org.deepin.dde.Appearance1")
    .path("/org/deepin/dde/Appearance1")
    .interface("org.deepin.dde.Appearance1")
    .property("FontSize")
    .get();
```

### 2.3 属性写入

```cpp
DDBusSender()
    .service("org.deepin.dde.Appearance1")
    .path("/org/deepin/dde/Appearance1")
    .interface("org.deepin.dde.Appearance1")
    .property("FontSize")
    .set(14);
```

## 3. 处理异步返回

`call()` 返回 `QDBusPendingCall`，需要异步处理：

```cpp
QDBusPendingCall asyncCall = DDBusSender()
    .service("org.deepin.dde.Dock1")
    .path("/org/deepin/dde/Dock1")
    .interface("org.deepin.dde.Dock1")
    .method("GetDockedApps")
    .call();

QDBusPendingCallWatcher *watcher = new QDBusPendingCallWatcher(asyncCall, this);
connect(watcher, &QDBusPendingCallWatcher::finished, this, [this](QDBusPendingCallWatcher *w) {
    QDBusPendingReply<QList<QDBusObjectPath>> reply = *w;
    if (reply.isError()) {
        qWarning() << "DBus error:" << reply.error().message();
    } else {
        QList<QDBusObjectPath> apps = reply.value();
        // 处理结果
    }
    w->deleteLater();
});
```

## 4. DDBusInterface 高级用法

`DDBusInterface`（dtkcore）继承 `QDBusAbstractInterface`，提供属性自动同步功能：

```cpp
#include <DDBusInterface>

auto *iface = new DDBusInterface(
    "org.deepin.dde.Appearance1",
    "/org/deepin/dde/Appearance1",
    "org.deepin.dde.Appearance1",
    QDBusConnection::sessionBus(),
    this);

// 检查服务是否可用
if (iface->serviceValid()) { ... }

// 监听服务可用性变化
connect(iface, &DDBusInterface::serviceValidChanged, [](bool valid) {
    qInfo() << "Service valid:" << valid;
});
```

### 属性自动同步

当 `DDBusInterface` 设置了 parent 对象时，会自动将 DBus 属性变化同步到 parent 的 Q_PROPERTY：

```cpp
class MyController : public QObject {
    Q_OBJECT
    Q_PROPERTY(int fontSize READ fontSize NOTIFY fontSizeChanged)
    // ...
};

auto *iface = new DDBusInterface("...", "/...", "...", QDBusConnection::sessionBus(), myController);
// DBus PropertiesChanged 信号会自动更新 myController 的 Q_PROPERTY
```

## 5. 选择决策

```
需要 DBus 通信？
    │
    ├─ 一次性调用，无需缓存？
    │   └─ DDBusSender（轻量，无需 introspection）
    │
    ├─ 需要属性自动同步？
    │   └─ DDBusInterface（自动 PropertiesChanged 监听）
    │
    └─ 需要完整 introspection？
        └─ QDBusInterface（Qt 原生）
```

## 6. 常见错误与避坑

### 错误 1：忽略异步返回错误

```cpp
// ❌ 错误：不检查返回
DDBusSender().service("...").path("...").interface("...").method("Foo").call();

// ✅ 正确：检查错误
QDBusPendingCall call = DDBusSender()...call();
auto *watcher = new QDBusPendingCallWatcher(call, this);
connect(watcher, &QDBusPendingCallWatcher::finished, [](QDBusPendingCallWatcher *w) {
    if (w->isError()) qWarning() << w->error();
    w->deleteLater();
});
```

### 错误 2：在 System Bus 上使用默认 Session Bus

```cpp
// ❌ 错误：System Bus 服务必须用 system()
DDBusSender().service("org.freedesktop.login1")... // 默认 session bus

// ✅ 正确
DDBusSender::system().service("org.freedesktop.login1")...
```

### 错误 3：arg() 使用 C 字符串

```cpp
// ❌ 错误：C 字符串会被推导为 const char*
.arg("标题")

// ✅ 正确：显式使用 QString
.arg(QString("标题"))
```

## 7. 相关文档

- [log.md](log.md) - 日志系统
- [sysinfo.md](sysinfo.md) - 系统信息
