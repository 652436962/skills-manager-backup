# 调试技巧与常见问题

## 本地运行与调试

`--spec` 参数指定插件搜索目录，跳过系统默认路径，直接加载构建产物。始终通过系统的 `dde-control-center` wrapper 启动（非构建目录下的同名二进制），以确保 security loader 提供 D-Bus 授权：

```bash
dde-control-center --spec /path/to/build/lib/plugins_v1.1/
```

**路径说明**：`--spec` 接受绝对路径或相对于当前工作目录的路径。假设项目源码在 `~/dde-control-center`，构建目录为 `~/dde-control-center/build`，则：

| 工作目录 | --spec 参数 |
|----------|-------------|
| `~/dde-control-center` | `--spec ./build/lib/plugins_v1.1/` |
| `~/dde-control-center/build` | `--spec ./lib/plugins_v1.1/` |
| 任意目录 | `--spec ~/dde-control-center/build/lib/plugins_v1.1/` |

> **注意**：`--spec` 只替换插件搜索路径，不影响框架库（`libdde-control-center.so`）和 QML 引擎插件的加载。如果修改了框架代码，需要额外设置环境变量，见下文。

### 仅修改插件

只修改了插件 QML 或 C++ 代码，框架未改动：

```bash
# 1. 先关闭已运行的控制中心实例（单实例限制）
killall dde-control-center 2>/dev/null

# 2. 通过系统 wrapper 启动，指定构建目录的插件路径
#    wrapper 会通过 security loader 启动，确保 D-Bus 授权正常
dde-control-center --spec /path/to/build/lib/plugins_v1.1/
```

> **安全加载说明**：`/usr/bin/dde-control-center` 是 shell 包装脚本，内部通过 `deepin-security-loader` 启动真正的二进制（`/usr/libexec/deepin/dde-control-center`）。直接运行构建目录的 `./bin/dde-control-center` 会绕过安全加载，导致需要授权的系统 D-Bus 调用失败。调试插件时始终使用系统 wrapper + `--spec` 即可正常工作。

### 修改了框架代码

修改了 `libdde-control-center.so`、QML 框架组件（`org.deepin.dcc` 模块）或 `dde-control-center` 可执行文件本身时，需要设置环境变量确保加载构建产物而非系统安装版本，但仍通过系统 wrapper 启动以保证 D-Bus 授权：

```bash
# 1. 先关闭已运行的控制中心实例
killall dde-control-center 2>/dev/null

# 2. 设置环境变量，指向构建目录的库
export LD_LIBRARY_PATH=/path/to/build/lib:${LD_LIBRARY_PATH}
export QT_PLUGIN_PATH=/path/to/build/lib:${QT_PLUGIN_PATH}
export QML2_IMPORT_PATH=/path/to/build/lib:${QML2_IMPORT_PATH}

# 3. 通过系统 wrapper 启动
dde-control-center --spec /path/to/build/lib/plugins_v1.1/
```

> **注意**：`LD_LIBRARY_PATH` 和 `QML2_IMPORT_PATH` 只影响动态库和 QML 模块的搜索路径。二进制本身仍由 wrapper 中的路径（`/usr/libexec/deepin/dde-control-center`）决定，如需替换二进制则需先安装到系统路径。

**环境变量说明**：

| 变量 | 作用 |
|------|------|
| `LD_LIBRARY_PATH` | 让插件 `.so` 加载构建目录的 `libdde-control-center.so`，而非 `/usr/lib/` 下的系统版本 |
| `QT_PLUGIN_PATH` | 让 Qt 找到构建目录中的 QML 插件 |
| `QML2_IMPORT_PATH` | 让 QML 引擎从构建目录加载 `org.deepin.dcc` 模块 |

### 验证加载路径

```bash
# 检查插件 .so 实际链接的框架库路径
ldd ~/dde-control-center/build/lib/plugins_v1.1/accounts/accounts.so | grep dde-control-center

# 检查运行时进程的库映射
cat /proc/$(pidof dde-control-center)/maps | grep dde-control-center
```

如果输出包含 `/usr/lib/` 路径而非 `build/lib/`，说明 `LD_LIBRARY_PATH` 未生效。

## 不能混用 ASAN

控制中心本身没有使用 AddressSanitizer 编译时，不能加载使用 ASAN 编译的插件（加载会失败）。

## 线程安全

`DccFactory::create()` 在线程池中执行，完成后 data 对象移动到主线程。构造函数中创建的所有 QObject 必须纳入 QObject 树（以 data 对象为 parent 或其子孙），否则不会随主线程移动。

```cpp
// 错误
MyModule::MyModule(QObject *parent) : QObject(parent) {
    m_worker = new Worker();  // 无 parent，停留在线程池线程
}

// 正确
MyModule::MyModule(QObject *parent) : QObject(parent) {
    m_worker = new Worker(this);  // 纳入 QObject 树
}
```

## 常见问题

### 插件不显示

1. 检查 hideModule：
   ```bash
   dde-dconfig get org.deepin.dde.control-center -r org.deepin.dde.control-center hideModule
   ```
2. 检查 `{Name}.qml` 中 `visible` 是否为 `false`
3. 检查 DBus 条件是否满足
4. 检查插件目录结构：`ls plugins_v1.1/myplugin/`

### dccData 为 undefined

1. 确认是否在 `{Name}.qml` 中访问（C++ 插件此时未加载）
2. 确认 `DCC_FACTORY_CLASS(YourClass)` 正确调用
3. 确认 `#include "yourclass.moc"` 是 `.moc` 不是 `.h`
4. 确认 CMake 链接了 `Dde::Control-Center`

### QML 修改不生效

1. QML 文件名必须首字母大写
2. 不能用 `main.qml`（已废弃），必须 `{Name}Main.qml`
3. 清除 QML 缓存：`rm -rf ~/.cache/dde-control-center/qmlcache/`
4. 确认重新编译了 QML 模块：`cmake --build . --target myplugin_qml`

### 搜索不到设置项

1. 确认 `canSearch` 为 `true`（默认值）
2. 确认 `displayName`/`description` 包含关键字
3. DccSettingsView 中的设置项默认参与搜索

### 图标不显示

1. 图标文件必须在 `qml/` 目录下
2. 图标格式为 `.dci`
3. `icon` 属性值与文件名匹配（不含扩展名）

### DBus 属性不更新

1. 检查 `connection` 类型（`SessionBus` vs `SystemBus`）
2. 验证 DBus 服务存在：
   ```bash
   busctl --user introspect org.deepin.dde.Appearance1 /org/deepin/dde/Appearance1
   ```
3. 属性名与 QML 保留字冲突时使用 `suffix`

## 诊断命令

```bash
# 查看 QML 运行时错误
dde-control-center --spec /path/to/plugins 2>&1 | grep -i "error\|warning"

# 验证 .so 插件包含工厂接口
strings /path/to/myplugin.so | grep DccFactory

# 验证安装路径
ls /usr/lib/x86_64-linux-gnu/dde-control-center/plugins_v1.1/myplugin/

# 重启 DConfig daemon
systemctl --user restart dde-dconfig-daemon.service
```

## 完整检查清单

```
[ ] CMake PLUGIN_NAME 与 {Name}.qml 中 name 一致
[ ] 插件目录名与插件名一致: src/plugin-{name}/
[ ] {Name}.qml 存在且 name 正确
[ ] {Name}Main.qml 存在（非 main.qml）
[ ] .so 文件编译成功且包含 DCC_FACTORY_CLASS
[ ] qmldir 文件存在
[ ] 不在 DConfig hideModule 列表中
[ ] {Name}.qml 中 visible 不为 false
[ ] 所有 QML 文件名首字母大写
[ ] 所有 QObject 子对象有 parent
```

## 相关文档

- [plugin-development.md](plugin-development.md) — 插件开发
- [architecture.md](architecture.md) — 架构与加载流程
