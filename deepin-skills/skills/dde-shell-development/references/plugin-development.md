# dde-shell 插件开发

## 插件类型

| 类型 | 基类 | 场景 | 可含子插件 |
|------|------|------|-----------|
| Applet | `DApplet` | 基础部件（天气、时钟、网络状态） | 否 |
| Containment | `DContainment` | 容器（应用抽屉、设置分组） | 是 |
| Panel | `DPanel` | 顶级面板（Dock、顶栏、侧栏） | 是 |

继承关系：`QObject → DApplet → DContainment → DPanel`

## 目录结构

```
my-plugin/
├── CMakeLists.txt
├── myapplet.h / myapplet.cpp
├── package/
│   ├── metadata.json
│   └── main.qml
└── translations/
    └── <plugin-id>.ts / <plugin-id>_zh_CN.ts ...
```

## 一、Applet 插件

### 纯 QML Applet（无 C++）

CMakeLists.txt：
```cmake
ds_install_package(PACKAGE org.deepin.ds.example.applet)
```

metadata.json：
```json
{
    "Plugin": {
        "Version": "1.0",
        "Id": "org.deepin.ds.example.applet",
        "Url": "main.qml",
        "Parent": "org.deepin.ds.dock"
    }
}
```

main.qml：
```qml
import QtQuick
import QtQuick.Controls
import org.deepin.ds 1.0

AppletItem {
    implicitWidth: 100; implicitHeight: 100
    Text {
        anchors.centerIn: parent
        text: Applet.pluginId
    }
}
```

### 带 C++ 后端的 Applet

头文件：
```cpp
#pragma once
#include <applet.h>
DS_USE_NAMESPACE

class WeatherApplet : public DApplet
{
    Q_OBJECT
    Q_PROPERTY(QString temperature READ temperature NOTIFY temperatureChanged)
public:
    explicit WeatherApplet(QObject *parent = nullptr);
    virtual bool load() override;
    virtual bool init() override;
    QString temperature() const;
signals:
    void temperatureChanged();
private:
    QString m_temperature;
};
```

实现文件：
```cpp
#include "weatherapplet.h"
#include <pluginfactory.h>

WeatherApplet::WeatherApplet(QObject *parent) : DApplet(parent) {}

bool WeatherApplet::load() {
    // 从 DConfig / appletData() 加载配置
    return true;
}

bool WeatherApplet::init() {
    DApplet::init();
    connect(this, &DApplet::rootObjectChanged, this, [this]() {
        auto *root = qobject_cast<DAppletItem *>(rootObject());
        if (root) { /* 可获取 root->width(), root->height() */ }
    });
    return true;
}

QString WeatherApplet::temperature() const { return m_temperature; }

D_APPLET_CLASS(WeatherApplet)
#include "weatherapplet.moc"
```

#### C++ 插件注册（不可省略）

每个 C++ Applet、Containment 或 Panel 必须在一个实现文件中完成以下注册：

```cpp
#include <pluginfactory.h>

// 类实现……

D_APPLET_CLASS(WeatherApplet)
#include "weatherapplet.moc"
```

- `D_APPLET_CLASS(ClassName)` 为插件生成带 `Q_PLUGIN_METADATA` 的 `DAppletFactory`；缺少它时，`.so` 仍可能链接成功，但 dde-shell 无法通过 `QPluginLoader` 创建插件实例。
- 宏在整个插件中只使用一次，类名必须与实际的 `DApplet`、`DContainment` 或 `DPanel` 子类一致。
- `#include "<实现文件名>.moc"` 紧跟宏之后；例如宏位于 `weatherapplet.cpp`，就包含 `"weatherapplet.moc"`。宏会在 `.cpp` 中生成带 `Q_OBJECT` 的工厂类，因此不能只依赖头文件的 AUTOMOC 输出。

CMakeLists.txt：
```cmake
find_package(DDEShell REQUIRED)

add_library(ds-weather SHARED
    weatherapplet.h weatherapplet.cpp
)
target_link_libraries(ds-weather PRIVATE Dde::Shell)
ds_install_package(PACKAGE org.deepin.ds.weather TARGET ds-weather)
```

### QWidget Applet

无 QML，init() 中创建 QWidget，metadata.json 不设 `Url`。

```cpp
bool WidgetApplet::init() {
    auto w = new QWidget();
    w->setFixedSize(200, 200); w->show();
    return DApplet::init();
}
```

CMake 需额外链接 `Qt::Widgets` 和 `Dtk::Widget`。

## 二、Containment 插件

子插件通过 `DAppletData::setGroupList()` 传入，框架自动加载。

实现：
```cpp
#include <containment.h>
#include <pluginfactory.h>
#include <pluginloader.h>
DS_USE_NAMESPACE

class MyContainment : public DContainment
{
    Q_OBJECT
public:
    bool load() override {
        QList<DAppletData> groups;
        auto children = DPluginLoader::instance()->childrenPlugin(pluginId());
        for (auto item : children)
            groups << DAppletData::fromPluginMetaData(item);
        auto data = appletData();
        data.setGroupList(groups);
        setAppletData(data);
        return DApplet::load();
    }
};

D_APPLET_CLASS(MyContainment)
#include "mycontainment.moc"
```

动态创建：`createApplet(DAppletData(data));`

QML 入口：
```qml
ContainmentItem {
    RowLayout {
        Repeater {
            model: Containment.appletItems
            delegate: Control { contentItem: model.data }
        }
    }
}
```

## 三、Panel 插件

管理主窗口 + 3 个辅助窗口（popup/tooltip/menu）。

实现：
```cpp
#include <panel.h>
#include <pluginfactory.h>
DS_USE_NAMESPACE

class MyPanel : public DPanel
{
    Q_OBJECT
public:
    explicit MyPanel(QObject *p = nullptr) : DPanel(p) {}
    bool load() override { return DPanel::load(); }
    bool init() override {
        DPanel::init();
        connect(this, &DApplet::rootObjectChanged, this, [this]() {
            Q_ASSERT(rootObject() && window());
        });
        return true;
    }
};

D_APPLET_CLASS(MyPanel)
#include "mypanel.moc"
```

QML Layer Shell Window：
```qml
import QtQuick
import QtQuick.Controls
import QtQuick.Window
import org.deepin.ds 1.0

Window {
    visible: true; height: 50
    DLayerShellWindow.anchors: DLayerShellWindow.AnchorBottom
        | DLayerShellWindow.AnchorLeft | DLayerShellWindow.AnchorRight
    RowLayout {
        anchors.fill: parent
        Repeater {
            model: Applet.appletItems
            delegate: Control { contentItem: model.data }
        }
    }
}
```

## 四、CMake 集成

### ds_install_package

安装包和库：

```cmake
ds_install_package(PACKAGE <plugin-id> TARGET <library-name>)
```

纯 QML 插件可不传 TARGET。内部自动处理 PREFIX/OUTPUT_NAME 设置和安装路径。

### ds_handle_package_translation

配置翻译：

```cmake
ds_handle_package_translation(PACKAGE <plugin-id>)
```

自动扫描 package/ 下 QML 文件和当前目录 C++ 文件，生成 23 种语言翻译并安装到正确路径。

### 依赖

```cmake
find_package(DDEShell REQUIRED)
target_link_libraries(my-plugin PRIVATE Dde::Shell)
```

### 构建

```bash
cmake -B build -DCMAKE_INSTALL_PREFIX=/usr
cmake --build build -j$(nproc)
sudo cmake --install build
```

## 五、Debian 打包

dde-shell 相关的依赖：

```
Build-Depends: libdde-shell-dev (>= 0.0.10)
Depends: dde-shell (>= 2.0)
```

`.install` 文件：
```
usr/lib/dde-shell/plugins/*
usr/share/dde-shell/*
```

## 六、翻译

QML: `qsTr("Hello")`，C++: `tr("Hello")`。通过 `ds_handle_package_translation` 自动处理 23 种语言。

## 七、元数据

| 字段 | 必需 | 说明 |
|------|------|------|
| Plugin.Version | 是 | 版本号 |
| Plugin.Id | 是 | 反向域名，如 `org.deepin.ds.weather` |
| Plugin.Url | 否 | QML 入口，QWidget 不填 |
| Plugin.Parent | 否 | 父插件 ID |
| Plugin.ContainmentType | 否 | `"Panel"` 或 `"Containment"` |

## 八、安装路径

- Package: `/usr/share/dde-shell/<plugin-id>/`
- 插件库: `/usr/lib/dde-shell/plugins/`
- 翻译: `/usr/share/dde-shell/<plugin-id>/translations/`

## 九、跨插件通信

通过 DAppletBridge 访问其他已加载插件：

```cpp
DAppletBridge bridge("org.deepin.ds.weather");
if (bridge.isValid() && bridge.applet()) {
    bridge.applet()->property("temperature").toInt();
    QMetaObject::invokeMethod(bridge.applet(), "getData",
        Qt::DirectConnection, Q_RETURN_ARG(QString, result));
    connect(bridge.applet(), SIGNAL(changed(int)), this, SLOT(onChanged(int)));
}
```

QML 端：
```qml
var weather = DS.applet("org.deepin.ds.weather")
if (weather && weather.rootObject) {
    console.log(weather.rootObject.temperature)
}
```

插件暴露自定义接口：重写 `createProxyMeta()` 返回代理对象。

## 十、测试

```bash
# 列出所有插件
dde-shell --list

# 测试单个插件
dde-shell -p <plugin-id>

# 测试多个插件
dde-shell -p <plugin-id1> -p <plugin-id2>

# 禁用指定插件
dde-shell -d <plugin-id>

# 按分类加载面板
dde-shell -C <category>

# 重启系统服务
systemctl --user restart dde-shell@DDE

# 从 build 目录加载（自动检测同级 packages/ 和 plugins/）
./build/shell/dde-shell -p <plugin-id>

# 指定自定义路径加载
DDE_SHELL_PACKAGE_PATH=/path/to/packages \
DDE_SHELL_PLUGIN_PATH=/path/to/plugins \
./build/shell/dde-shell -p <plugin-id>
```
