# 单实例应用

## 1. 概述

DTK 在 dtkgui 层提供基于 `QLocalServer`/`QLocalSocket` 的单实例机制，确保同一应用只运行一个进程。第二个实例启动时会通知第一个实例，并传递启动参数。非 dtkwidget 应用可直接使用 `DGuiApplicationHelper` 的接口。

## 2. 基本用法

```cpp
#include <DGuiApplicationHelper>
#include <QApplication>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    if (!DGuiApplicationHelper::setSingleInstance("myapp")) {
        qInfo() << "另一实例已在运行，退出";
        return 0;
    }

    // 监听新实例启动
    QObject::connect(DGuiApplicationHelper::instance(),
                     &DGuiApplicationHelper::newProcessInstance,
                     [](qint64 pid, const QStringList &args) {
        qInfo() << "新实例启动:" << pid << args;
        // 在此激活窗口
    });

    return app.exec();
}
```

使用 `DApplication`（dtkwidget）时，直接调用 `DApplication::setSingleInstance(key)`，并监听 `newInstanceStarted()`。第二个进程应退出，原进程负责恢复并激活自己的窗口。

## 3. 原理

### 3.1 QLocalServer 竞争机制

```
第一个进程
  → QLockFile("_d_dtk_single_instance_<uid>_<key>.lock").tryLock() 成功
  → QLocalServer.listen("_d_dtk_single_instance_<uid>_<key>")
  → 进入事件循环，等待新连接

第二个进程
  → QLockFile.tryLock() 失败
  → QLocalSocket 连接到第一个进程的 QLocalServer
  → 接收第一个进程的信息（pid, args）
  → 发送自己的信息（pid, args）
  → 退出
```

### 3.2 进程间传递的数据

通过 `QDataStream` 序列化传递（v2 协议）：

1. **协议版本号** (`quint8`) — 当前版本 2
2. **进程 PID** (`qint64`)
3. **启动参数** (`QStringList`) — `QApplication::arguments()`
4. **环境变量** (`QStringList`) — v2 新增，仅转发白名单中的 key

白名单当前包含 `XDG_ACTIVATION_TOKEN`，用于 Wayland 下将新实例的窗口激活 token 传递给第一个实例的进程环境（`qputenv`），确保窗口能正确获取焦点。

### 3.3 SingleScope 作用域

| 枚举 | 说明 |
|------|------|
| `UserScope` | 同一用户下唯一（默认） |
| `GroupScope` | 同一用户组下唯一 |
| `WorldScope` | 全局唯一 |

```cpp
DGuiApplicationHelper::setSingleInstance("myapp", DGuiApplicationHelper::GroupScope);
```

## 4. 窗口激活

收到 `DGuiApplicationHelper::newProcessInstance` 信号后手动激活窗口：

```cpp
QObject::connect(DGuiApplicationHelper::instance(),
                 &DGuiApplicationHelper::newProcessInstance,
                 [](qint64 pid, const QStringList &args) {
    for (QWidget *w : qApp->topLevelWidgets()) {
        if (auto *mainWin = qobject_cast<QMainWindow*>(w)) {
            if (mainWin->isMinimized())
                mainWin->showNormal();
            else
                mainWin->show();
            mainWin->raise();
            mainWin->activateWindow();
            break;
        }
    }
});
```

## 5. 沙箱环境（Flatpak）

需编译时启用 `DTK_DBUS_SINGLEINSTANCE` 宏，通过注册 DBus 服务名 `com.deepin.SingleInstance.<key>` 判断唯一性。无法注册说明已有实例。

## 6. 注意事项

- `setSingleInstanceInterval(ms)` 必须在 `setSingleInstance()` 之前调用，控制新实例等待第一个实例响应的超时时间（默认 3000ms）
- Linux 下 socket key 包含 uid 和 pid namespace，确保不同用户和容器隔离
- 新实例带来的文件或命令行参数必须在通知回调中交给原进程处理，不能只激活窗口后丢弃参数

## 7. 相关文档

- [index.md](index.md) — 工具类索引
- [log.md](log.md) — 日志系统
