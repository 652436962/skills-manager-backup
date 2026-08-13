# 工具集

## 1. 文件系统

### 1.1 DStandardPaths — 标准路径

```cpp
#include <DStandardPaths>

QString config = DStandardPaths::writableLocation(QStandardPaths::AppConfigLocation);
QString data = DStandardPaths::writableLocation(QStandardPaths::AppDataLocation);
QString cache = DStandardPaths::writableLocation(QStandardPaths::CacheLocation);
QString temp = DStandardPaths::writableLocation(QStandardPaths::TempLocation);
```

### 1.2 DFileWatcher — 文件监听

```cpp
#include <DFileWatcher>

auto *watcher = new DFileWatcher("/path/to/file", this);
connect(watcher, &DFileWatcher::fileModified, [](const QUrl &url) {
    qInfo() << "File modified:" << url;
});
```

### 1.3 DTrashManager — 回收站

```cpp
#include <DTrashManager>

DTrashManager::instance()->moveToTrash("/path/to/file");
DTrashManager::instance()->cleanTrash();
```

## 2. DBus 辅助

| 类 | 用途 | 详见 |
|----|------|------|
| `DDBusSender` | 链式构建器模式，适合单次 DBus 调用 | [dbus.md](dbus.md) |
| `DDBusInterface` | 继承 `QDBusAbstractInterface`，支持自动服务监听、属性同步、信号转发 | [dbus.md](dbus.md) |

## 3. 通知系统

`DNotifySender` 采用链式构建器模式，位于 `DUtil` 命名空间。

```cpp
#include <DNotifySender>

using namespace Dtk::Core::DUtil;

// 简单通知
DNotifySender("下载完成")
    .appBody("文件已保存到 /home/user/Downloads")
    .call();

// 带图标和超时
DNotifySender("操作完成")
    .appIcon("dialog-ok")
    .appBody("所有文件已同步")
    .timeOut(5000)
    .call();

// 带动作按钮
DNotifySender("确认删除")
    .appBody("确定要删除此文件吗？")
    .appIcon("dialog-warning")
    .actions({"open", "打开", "cancel", "取消"})
    .call();

// 更新已有通知
DNotifySender("下载进度")
    .appBody("50%")
    .replaceId(1)
    .call();
```

| 链式方法 | 说明 |
|----------|------|
| `DNotifySender(summary)` | 构造，传入通知标题 |
| `.appName(name)` | 应用名称 |
| `.appIcon(icon)` | 图标名称 |
| `.appBody(body)` | 通知正文 |
| `.replaceId(id)` | 替换 ID（更新已有通知） |
| `.timeOut(ms)` | 超时时间（毫秒） |
| `.actions(list)` | 动作列表（成对：id, 标签） |
| `.hints(map)` | 额外提示 |
| `.call()` | 发送通知 |

## 4. 系统信息

`DSysInfo` 提供操作系统类型、版本、硬件信息等静态查询接口。完整 API 和枚举参考 → [sysinfo.md](sysinfo.md)

## 5. 拼音转换

拼音功能为 dtkcore 中的自由函数，位于 `Dtk::Core` 命名空间。

### 头文件

```cpp
#include <dpinyin.h>
```

### 基本用法

```cpp
// 无多音字支持，返回单个字符串
QString pinyin = Dtk::Core::Chinese2Pinyin("中国");  // "zhongguo"

// 多音字支持，返回所有组合
QStringList list = Dtk::Core::pinyin("重庆");  // [ "chongqing", "zhongqing" ]

// 首字母
QStringList fl = Dtk::Core::firstLetters("中国");  // [ "zg" ]
```

### 声调控制

`ToneStyle` 枚举控制输出格式：

| 值 | 示例输出 |
|----|----------|
| `TS_NoneTone` | `"zhongguo"` |
| `TS_Tone`（默认） | `"zhōngguó"` |
| `TS_ToneNum` | `"zhong1guo2"` |

```cpp
Dtk::Core::pinyin("中国", Dtk::Core::TS_Tone);
Dtk::Core::firstLetters("中国", Dtk::Core::TS_Tone);
```

## 6. 相关文档

- [index.md](index.md) — 工具类索引
- [log.md](log.md) — 日志系统
- [singleton.md](singleton.md) — 单实例应用
