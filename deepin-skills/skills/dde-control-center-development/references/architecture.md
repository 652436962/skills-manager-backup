# 控制中心架构与设计原理

## 核心设计

DDE 控制中心（dde-control-center v6.x，V25）采用**插件化架构**，基于 Qt 6 + DTK 6 + QML。

核心理念：

1. **功能全部由插件实现** — 框架不包含任何业务功能
2. **树形数据模型** — DccObject 组成树，通过 `parentName`（URL 路径如 `"system/display"`）建立父子关系
3. **C++ 数据 + QML 界面分离** — C++ 处理数据和逻辑，QML 负责渲染
4. **声明式配置** — 插件的显隐和启禁可通过 DConfig 统一配置，修改即时生效

## 架构层次

```
DccManager (主控制器，实现 DccApp + DBus 接口)
├── QQmlApplicationEngine (QML 引擎, URI: org.deepin.dcc)
├── DccPluginManager (扫描并加载所有插件)
│   └── DccPluginLoader × N (每个插件一个加载器)
├── NavigationModel (面包屑导航)
├── SearchModel (搜索过滤)
└── ControlCenterDBusAdaptor (DBus: org.deepin.dde.ControlCenter1)
```

## DccObject 树

所有界面内容由 DccObject 组成的树表达：

```
root
├── system (weight=10, 分组容器)
│   ├── display (weight=10)
│   │   ├── brightness
│   │   └── resolution
│   └── sound (weight=20)
├── personalization (weight=30)
└── device (weight=40, 分组容器)
    ├── bluetooth (weight=10)
    └── mouse (weight=30)
```

每个 DccObject 通过 `name`（唯一 ID）+ `parentName`（父项 URL）定位。`parentName` 使用 `/` 分隔多级路径，`name` 不能包含 `/`。

## 插件加载状态机

每个插件经历确定的状态转移：

```
PluginBegin
  → MetaDataLoad (安装翻译、解析 metadata.json)
    → MetaDataEnd (失败则 MetaDataErr)
  → ModuleLoad (加载 {Name}.qml，创建模块 DccObject)
    → ModuleEnd (失败则 ModuleErr)
  → DataBegin (线程池异步执行)
    → DataLoad (加载 .so，检查 DccFactory_iid)
    → DataEnd (失败则 DataErr)
  → MainObjLoad (加载 {Name}Main.qml，注入 dccData)
    → MainObjEnd (失败则 MainObjErr)
  → addMainObject (同步属性到模块对象)
→ PluginEnd
```

关键点：`DccFactory::create()` 在线程池中执行，完成后 data 对象通过 `moveToThread()` 移动回主线程。构造函数中创建的子对象必须纳入 QObject 树（以 data 对象为 parent），否则不会随主线程移动。

## 两种插件类型

### QML-Only 插件（无 .so）

只有 QML 文件，用于分组容器（`system`、`device`）或纯展示页面。CMakeLists.txt 只调用 `dcc_install_plugin(NAME ...)`，不调用 `add_library()`。

### 完整插件（有 .so）

有 C++ 编译产物，通过 `DCC_FACTORY_CLASS` 宏注册。需要 `add_library(... MODULE ...)` 和 `target_link_libraries(... Dde::Control-Center ...)`。

## 插件格式版本

| 特性 | v1.0 | v1.1（当前推荐） |
|------|------|-----------------|
| 安装目录 | `plugins_v1.0/` | `plugins_v1.1/` |
| QML 加载 | 直接文件路径 | QML 模块导入（URI = name） |
| 主页面 | `main.qml` | `{Name}Main.qml` |
| 元数据 | 无 | `metadata.json` |
| QML 文件命名 | 不限制 | 必须首字母大写 |

## 插件安装路径

```
/usr/lib/{multiarch}/dde-control-center/plugins_v1.1/{name}/
├── qmldir
├── lib{name}_qmlplugin.so    # QML 资源编译产物
├── {name}.so                  # C++ 插件（仅完整插件）
└── translations/
```

翻译安装到 `/usr/share/dde-control-center/translations/v1.1/`。

## DConfig 配置

控制中心通过 DConfig 管理模块显隐和禁用：

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `hideModule` | `string[]` | 隐藏的模块名列表 |
| `disableModule` | `string[]` | 禁用的模块名列表 |

```bash
# 查看/设置
dde-dconfig get org.deepin.dde.control-center -r org.deepin.dde.control-center hideModule
dde-dconfig set org.deepin.dde.control-center org.deepin.dde.control-center hideModule '["display"]'
dde-dconfig reset org.deepin.dde.control-center org.deepin.dde.control-center hideModule
```

插件加载前检查模块名是否在 `hideModule` 中，若在则跳过加载。DccObject 的只读属性 `visibleToApp` 和 `enabledToApp` 反映了结合配置后的最终状态。

## DBus 接口

- 服务名：`org.deepin.dde.ControlCenter1`
- 对象路径：`/org/deepin/dde/ControlCenter1`
- 主要方法：`Show()`、`Hide()`、`ShowPage(url)`、`Toggle()`、`GetAllModule()`、`Exit()`
- Grand Search 子接口：`org.deepin.dde.ControlCenter1.GrandSearch`（`Search`/`Stop`/`Action`）

## 相关文档

- [plugin-development.md](plugin-development.md) — 插件开发
- [cpp-api.md](cpp-api.md) — C++ API 参考
- [qml-api.md](qml-api.md) — QML API 参考
