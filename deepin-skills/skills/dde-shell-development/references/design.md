# dde-shell 设计原理

## 总体架构

```
dde-shell 可执行程序
├── QML Scene (SceneWindow)
│   ├── Panel (Dock)
│   │   ├── Applet
│   │   └── Applet
│   ├── Panel (Notification)
│   │   └── Applet
│   └── Panel (...)
└── libdde-shell (frame)
    ├── PluginLoader    # 插件发现/加载
    ├── AppletBridge    # 跨插件通信
    ├── Layer Shell     # Wayland 窗口管理
    └── Factory         # Qt Plugin 注册
```

## 三层插件模型

```
QObject → DApplet → DContainment → DPanel
```

- **DApplet**: 最小功能单元，叶子节点
- **DContainment**: 容器，通过 `groupList` 管理子插件
- **DPanel**: 顶级面板，增加窗口管理（主窗口 + popup/tooltip/menu）

## 元数据驱动的插件发现

启动时扫描 `/usr/share/dde-shell/<plugin-id>/` 和 `/usr/lib/dde-shell/plugins/`。

`DPluginLoader` 单例负责：
1. 读取 `package/metadata.json` 构建 `DPluginMetaData`
2. 解析 `Parent` 字段构建插件树
3. 按需加载 `.so`（通过 Qt Plugin 系统）

## 父子层级加载

从根插件开始递归加载：

```
Panel::load()
  → 读取 groupList
  → 对每个子插件 loadApplet(child)
      → 构造子 DApplet
      → 子 load() → 子 init()
  → Panel::init()
  → 创建 QML Window
      → Repeater + Applet.appletItems 渲染子 item
```

同插件实例生命周期：构造 → `load()` → `init()` → `rootObjectChanged`

## 数据模型

- **DPluginMetaData**: 静态/类级，描述插件类型（来自 metadata.json）
- **DAppletData**: 运行时/实例级，描述一个插件实例
- **DAppletItemModel**: `QAbstractListModel`，暴露子 applet 的 QML item 给 QML（role: `Qt::UserRole+1`，即 `model.data`）

## 跨插件通信：Bridge + Proxy

```
Plugin A → DAppletBridge("id") → DAppletProxy → Plugin B
```

- Bridge 查找目标插件并构建代理
- Proxy 提供属性读写、信号连接
- `createProxyMeta()` 控制暴露的自定义接口
- QML 端: `DS.applet(pluginId)`

## QML 集成

通过 Qt QML Plugin 注册类型到 `org.deepin.ds 1.0`。附加属性机制 (`qmlAttachedProperties`) 让子 Applet 能访问父级上下文。

## Layer Shell

DPanel 使用 Wayland `wlr-layer-shell` 协议锚定屏幕边缘。`DLayerShellWindow` 提供 QML 附加属性。支持 X11 回退模拟。

## 插件注册：D_APPLET_CLASS

```cpp
D_APPLET_CLASS(MyPlugin)
```

展开为匿名 namespace 中的 `DAppletFactory` 子类，通过 `Q_PLUGIN_METADATA` 注册 Qt Plugin。框架通过 `QPluginLoader` 加载 `.so`。

## DConfig 集成

```cpp
auto config = DConfig::create("org.deepin.dde.shell", PLUGIN_ID);
config->value("key", defaultVal);
```

配置元数据在 `configs/<plugin-id>.json`，通过 `dtk_add_config_meta_files` 注册。

## 安装路径

| 内容 | 路径 |
|------|------|
| 包 | `/usr/share/dde-shell/<plugin-id>/` |
| .so | `/usr/lib/dde-shell/plugins/` |
| 翻译 | `/usr/share/dde-shell/<plugin-id>/translations/` |
| DConfig 元数据 | `/etc/dsg/configs/<appid>/<plugin-id>.json` |

## 关键源文件

| 功能 | 源文件 |
|------|--------|
| 入口 | `shell/main.cpp` |
| 插件加载 | `frame/pluginloader.h` |
| 工厂 | `frame/pluginfactory.h` |
| Applet | `frame/applet.h` |
| Containment | `frame/containment.h` |
| Panel | `frame/panel.h` |
| Bridge | `frame/appletbridge.h`, `frame/appletproxy.h` |
| QML 组件 | `frame/appletitem.h`, `frame/containmentitem.h` |
| Layer Shell | `frame/layershell/dlayershellwindow.h` |
| CMake 宏 | `cmake/DDEShellPackageMacros.cmake` |
