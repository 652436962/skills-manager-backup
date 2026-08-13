# 核心类 API

所有类位于 `ds` 命名空间，导入方式：`DS_USE_NAMESPACE` / `DS_BEGIN_NAMESPACE` / `DS_END_NAMESPACE`。

类层次：
```
QObject
├── DPluginMetaData → DAppletData
├── DPluginLoader（单例）
├── DApplet → DContainment → DPanel
├── DAppletBridge → DAppletProxy
└── DAppletFactory
```

## DApplet

**头文件**: `applet.h`，继承 `QObject, DObject`。所有插件基类。

**属性**: `id`(QString,CONSTANT), `pluginId`(QString,CONSTANT), `parent`(DApplet*,CONSTANT), `rootObject`(QObject*,NOTIFY)

**方法**:
```cpp
QString id() const;
QString pluginId() const;
QObject *rootObject() const;
DApplet *parentApplet() const;
DPluginMetaData pluginMetaData() const;
DAppletData appletData() const;
void setAppletData(const DAppletData &data);
void setRootObject(QObject *root);

virtual bool load();
virtual bool init();
virtual QObject *createProxyMeta();  // 暴露给其他插件的代理
```

**信号**: `rootObjectChanged()`

**生命周期**: 构造 → `load()` → `init()` → `rootObjectChanged`

**注册**: `D_APPLET_CLASS(ClassName)` 在 .cpp 中使用一次。需 `#include <pluginfactory.h>`，使用后 `#include "classname.moc"`。

## DContainment

**头文件**: `containment.h`，继承 `DApplet`。管理子 Applet 的容器。

**属性**: `appletItems`(DAppletItemModel*,CONSTANT)

**方法**:
```cpp
DApplet *createApplet(const DAppletData &data);
void removeApplet(DApplet *applet);
QList<DApplet *> applets() const;
QList<QObject *> appletItems();
DAppletItemModel *appletItemModel() const;
DApplet *applet(const QString &id) const;
virtual bool load() override;
virtual bool init() override;
```

**DAppletItemModel**: QML 列表模型，role `Data`(Qt::UserRole+1)，`model.data` 是子 applet 根 QML 元素。

## DPanel

**头文件**: `panel.h`，继承 `DContainment`。顶级面板容器，管理主窗口 + popup/tooltip/menu 三窗口。

**属性**: `popupWindow`(QQuickWindow*,NOTIFY), `toolTipWindow`(QQuickWindow*,NOTIFY), `menuWindow`(QQuickWindow*,NOTIFY)

**方法**:
```cpp
QQuickWindow *window() const;
QQuickWindow *popupWindow() const;
QQuickWindow *toolTipWindow() const;
QQuickWindow *menuWindow() const;
virtual bool load() override;
virtual bool init() override;
static DPanel *qmlAttachedProperties(QObject *object);
```

**信号**: `popupWindowChanged()`, `toolTipWindowChanged()`, `menuWindowChanged()`

**QML 声明**: `QML_DECLARE_TYPEINFO(DS_NAMESPACE::DPanel, QML_HAS_ATTACHED_PROPERTIES)`

## DAppletBridge

**头文件**: `appletbridge.h`，继承 `QObject, DObject`。跨插件通信桥。

```cpp
DAppletBridge(const QString &pluginId, QObject *parent = nullptr);
bool isValid() const;
QString pluginId() const;
QList<DAppletProxy *> applets() const;
DAppletProxy *applet() const;
```

使用：
```cpp
DAppletBridge bridge("org.deepin.ds.weather");
if (bridge.isValid() && bridge.applet()) {
    bridge.applet()->property("temperature").toInt();
    QMetaObject::invokeMethod(bridge.applet(), "getData",
        Qt::DirectConnection, Q_RETURN_ARG(QString, result));
    connect(bridge.applet(), SIGNAL(changed(int)), this, SLOT(onChanged(int)));
}
```

## DAppletProxy

**头文件**: `appletproxy.h`，继承 `QObject, DObject`。远程插件代理。插件通过重写 `createProxyMeta()` 暴露自定义接口。

## DPluginLoader

**头文件**: `pluginloader.h`，单例。

```cpp
static DPluginLoader *instance();
void destroy();
QList<DPluginMetaData> plugins() const;
QList<DPluginMetaData> rootPlugins() const;
DPluginMetaData plugin(const QString &pluginId) const;
QList<DPluginMetaData> childrenPlugin(const QString &pluginId) const;
DPluginMetaData parentPlugin(const QString &pluginId) const;
DApplet *loadApplet(const DAppletData &data);
DApplet *rootApplet() const;
void addPackageDir(const QString &dir);
void addPluginDir(const QString &dir);
QStringList pluginDirs() const;
void setPluginDirs(const QStringList &dirs);
QStringList disabledApplets() const;
void setDisabledApplets(const QStringList &pluginIds);
```

## DPluginMetaData

**头文件**: `pluginmetadata.h`。从 `package/metadata.json` 解析。

```cpp
bool isValid() const;
QVariant value(const QString &key, const QVariant &defaultValue = QVariant()) const;
QString pluginId() const;
QString pluginDir() const;
QString url() const;
static DPluginMetaData fromJsonFile(const QString &file);
static DPluginMetaData fromJsonString(const QByteArray &data);
static DPluginMetaData rootPluginMetaData();
static bool isRootPlugin(const QString &pluginId);
```

## DAppletData

**头文件**: `appletdata.h`。插件实例运行时配置。

```cpp
bool isValid() const;
QVariant value(const QString &key, const QVariant &defaultValue = QVariant()) const;
QString id() const;
void setId(const QString &id);
QString pluginId() const;
QList<DAppletData> groupList() const;
void setGroupList(const QList<DAppletData> &groupList);
QVariantMap toMap() const;
static DAppletData fromPluginMetaData(const DPluginMetaData &metaData);
```

## DAppletFactory

**头文件**: `pluginfactory.h`。`D_APPLET_CLASS` 宏展开为此类的子类。

```cpp
using CreateAppletFunction = std::function<DApplet *(QObject *)>;
void registerInstance(CreateAppletFunction func);
template<class T>
static inline T *registerApplet(QObject *parent) { return new T(parent); }
virtual DApplet *create(QObject *parent = nullptr);
```
