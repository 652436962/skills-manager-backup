# DConfig C++ 使用

## 1. 概述与适用场景

DConfig 是 DTK 提供的跨进程配置管理方案，支持应用配置的持久化存储、跨应用共享和 OEM 覆盖。

**适用场景：**
- 应用需要持久化配置
- 多个应用需要共享配置
- 需要区分用户配置或系统级配置
- OEM 需要预置默认配置

**相关接口：**
- `DConfig` — C++ 配置读写类
- `DConfig::create()` — 创建配置实例
- `DConfig::value()` / `setValue()` — 读写配置值

## 2. 直接使用 DConfig

### 2.1 头文件与 CMake

```cpp
#include <DConfig>

// CMake（详见 [app-dev-with-dtk.md](../app-dev-with-dtk.md)）
find_package(Dtk6Core REQUIRED)
target_link_libraries(your_target Dtk6::Core)
```

### 2.2 基本用法

```cpp
auto *config = new DConfig("example", "", this);
if (!config->isValid()) {
    qWarning() << "DConfig is unavailable; using application defaults";
    // 保留默认值，应用仍应能够启动。
}

// 读取
bool canExit = config->isValid()
             ? config->value("canExit", true).toBool()
             : true;

if (config->isValid()) {
    // 写入
    config->setValue("canExit", false);

    // 监听变化
    connect(config, &DConfig::valueChanged, [](const QString &key) {
        qInfo() << "Config changed:" << key;
    });
}

if (config->isValid()) {
    // 重置为默认值
    config->reset("canExit");

    // 查询是否为默认值
    config->isDefaultValue("canExit");
}
```

### 2.3 创建方式

```cpp
// 默认：使用 DSGApplication::id() 获取 appId
explicit DConfig(const QString &name, const QString &subpath = QString(),
                 QObject *parent = nullptr);

// 仅在无法使用默认 appId 时显式指定
static DConfig *create(const QString &appId, const QString &name,
                       const QString &subpath = QString(),
                       QObject *parent = nullptr);

// 应用无关配置
static DConfig *createGeneric(const QString &name,
                              const QString &subpath = QString(),
                              QObject *parent = nullptr);

// 全局设置
static void setAppId(const QString &appId);
static QThread *globalThread();
```

> **注意**：不指定 appId 时，DConfig 会通过 `DSGApplication::id()` 获取默认 appId。如果默认 appId 无法满足需求，再使用 `create()` 显式指定。

应用不应自行拼接配置目录或使用 `QSettings` 替代 DConfig 的持久化职责。配置元数据不可用时使用代码中的 fallback，并通过日志记录一次原因；不要因为配置服务不可用而阻塞主窗口创建。

### 2.4 实例方法

```cpp
// 读写
QVariant value(const QString &key, const QVariant &fallback = QVariant()) const;
void setValue(const QString &key, const QVariant &value);

// 查询
QStringList keyList() const;
bool isValid() const;
bool isDefaultValue(const QString &key) const;
bool isReadOnly(const QString &key) const;

// 属性
QString name() const;
QString subpath() const;

// 重置
void reset(const QString &key);
```

### 2.5 信号

```cpp
Q_SIGNALS:
    void valueChanged(const QString &key);
```

### 2.6 带 subpath 使用

```cpp
// subpath 用于配置分层，格式以 / 开头
auto *configV1 = new DConfig("settings", "", this);
auto *configV2 = new DConfig("settings", "/v2", this);
```

## 2. dconfig2cpp：JSON 生成类型安全的 C++ 类

### 2.1 工具用法

```bash
dconfig2cpp -c MyConfig -o my_config.hpp configs/example.json
```

选项：

| 选项 | 说明 |
|------|------|
| `-c` / `--class-name` | 生成类名（默认 `dconfig_` + 文件名） |
| `-o` / `--output` | 输出头文件路径 |
| `--force-request-thread` | 强制传入 QThread 参数 |
| `--no-comment` | 不生成注释 |

### 2.2 生成类特性

- 每个配置项对应一个 `Q_PROPERTY`，类型自动推导：`bool` / `qlonglong` / `double` / `QString` / `QList<QVariant>` / `QVariantMap`
- `create(appId, subpath, parent)` / `createGeneric(subpath, parent)` 等工厂方法
- 线程安全的异步初始化（`DConfig::globalThread()`）
- `valueChanged(key, value)` 和各属性 `xxxChanged()` 信号
- `isInitializeSucceeded()` / `isInitializeFailed()` / `isInitializing()` 状态查询

### 2.3 使用生成类

```cpp
#include "my_config.hpp"

class MyWindow : public QWidget {
    MyConfig *m_cfg;
    void initConfig() {
        // 创建（异步初始化）
        m_cfg = MyConfig::create("org.deepin.myapp");

        // 连接初始化信号，receiver 为 m_cfg 自身
        connect(m_cfg, &MyConfig::configInitializeSucceed, m_cfg, [this]() {
            qInfo() << "Config ready, canExit:" << m_cfg->canExit();
        });
        connect(m_cfg, &MyConfig::configInitializeFailed, m_cfg, [this]() {
            qWarning() << "Config init failed";
        });

        // 监听属性变化
        connect(m_cfg, &MyConfig::canExitChanged, m_cfg, [this]() {
            qInfo() << "canExit changed:" << m_cfg->canExit();
        });
        connect(m_cfg, &MyConfig::valueChanged, m_cfg,
                [this](const QString &key, const QVariant &value) {
            qInfo() << key << "->" << value;
        });
    }

    void saveConfig() {
        if (!m_cfg->isInitializeSucceeded())
            return;

        // 类型安全读写
        m_cfg->setCanExit(false);

        // 重置
        m_cfg->resetCanExit();

        // 获取底层 DConfig 对象
        auto *dconfig = m_cfg->config();
    }
};
```

> **注意**：`configInitializeSucceed` 信号回调中使用 `m_cfg` 而非信号参数中的 `DConfig*` 指针。信号确保回调执行时配置已完全初始化，直接通过生成的属性读写即可。

### 2.4 CMake 集成

```cmake
find_package(Dtk6Core REQUIRED)

dtk_add_config_to_cpp(GENERATED_SOURCES
    ${CMAKE_SOURCE_DIR}/configs/example.json
    CLASS_NAME MyConfig
    OUTPUT_FILE_NAME my_config.hpp)
```

### 2.5 生成类状态机

```
Invalid → Initializing → Succeeded  (初始化成功)
                       → Failed     (初始化失败)
                       → Destroyed  (对象销毁)
```

- 初始化中可安全销毁对象
- 初始化完成前读取属性返回 meta 中定义的默认值
- 初始化后 `config()` 方法返回底层 `DConfig` 对象

## 3. 相关文档

- [concepts.md](concepts.md) - 核心概念
- [dconfig-dbus.md](dconfig-dbus.md) - DBus 方式
- [dconfig-debug.md](dconfig-debug.md) - 调试
