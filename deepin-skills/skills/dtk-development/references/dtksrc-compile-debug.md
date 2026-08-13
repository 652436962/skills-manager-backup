# DTK 源码编译与调试

> 适用场景：修改 DTK 自身源码（dtkcore/dtkgui/dtkwidget/dtkdeclarative/dtklog 及平台插件）后，需要编译、运行和调试。

---

## 1. DTK5/DTK6 同一套代码

DTK 各项目（dtkcore、dtkgui、dtkwidget、dtkdeclarative、dtklog）以及两个平台插件的 DTK5 和 DTK6 是**同一套代码**，通过 CMake option `DTK5` 切换编译目标。修改代码时需**同时保证 DTK5 和 DTK6 都能编译运行**。

`dtkcommon` 是唯一的例外——它不区分 DTK5/DTK6。

### 1.1 发布版本规则

DTK5 和 DTK6 由同一项目源码构建时，**发布版本号必须保持一致**。例如项目发布版本为 `6.7.44` 时，DTK5 和 DTK6 均为 `6.7.44`，不能把 DTK5 写成 `5.7.44`。

`DTK_VERSION_MAJOR` 的 `5`/`6` 只用于区分 Qt ABI、CMake 包名、库名和安装路径，不是发布版本号。各 DTK 项目的补丁版本可独立发布，因此应以项目的 `VERSION` 文件或 `debian/changelog` 为准。

| 项目 | DTK5 发布版本示例 | DTK6 发布版本示例 |
|------|------------------|------------------|
| dtkcore | 6.7.44 | 6.7.44 |
| dtkgui | 6.7.44 | 6.7.44 |
| dtkwidget | 6.7.44 | 6.7.44 |
| dtkdeclarative | 6.7.44 | 6.7.44 |
| dtklog | 6.7.44 | 6.7.44 |
| dde-qtintegration | 6.7.44 | 6.7.44 |
| dde-qtplatform-plugins | 6.7.44 | 6.7.44 |

表中的 `6.7.44` 仅说明同一项目的两种构建变体必须配对使用同一发布版本，并不要求不同 DTK 项目同步发布相同补丁版本。

### 1.2 CMake 编译切换

`DTK5` option 控制以下 CMake 变量，决定包名、target 名、库名和安装路径：

| 变量 | DTK5=ON | DTK5=OFF |
|------|---------|----------|
| `DTK_VERSION_MAJOR` | `5` | `6` |
| `DTK_NAME_SUFFIX` | `""`（空） | `"6"` |
| `QT_VERSION_MAJOR` | `5` | `6` |

### 1.3 区分 DTK5/DTK6 代码的方式

**方式一：预处理器宏（C++ 代码中）**

通过 `DTK_VERSION_MAJOR` 或 `QT_VERSION_MAJOR` 宏在 C++ 中条件编译：

```cpp
#if DTK_VERSION_MAJOR == 6
    // DTK6 专有代码
#else
    // DTK5 专有代码
#endif
```

**方式二：目录区分（CMake 中）**

在 CMakeLists.txt 中按版本添加不同的源文件目录。例如 dtkdeclarative 的 DTK6 QML 源码放在独立的 `qt6/src` 目录：

```cmake
if(NOT DTK5)
    add_subdirectory(qt6)
endif()
```

### 1.4 命名对照表

| 维度 | DTK5 | DTK6 |
|------|------|------|
| Qt 版本 | Qt 5 | Qt 6 |
| CMake 包名 | `DtkCore`, `DtkGui`, `DtkWidget` | `Dtk6Core`, `Dtk6Gui`, `Dtk6Widget` |
| CMake target | `Dtk::Core`, `Dtk::Gui`, `Dtk::Widget` | `Dtk6::Core`, `Dtk6::Gui`, `Dtk6::Widget` |
| 库文件名 | `libdtkcore.so.5` | `libdtk6core.so.6` |
| 头文件路径 | `/usr/include/dtk5/DCore/` | `/usr/include/dtk6/DCore/` |
| pkg-config | `dtkcore` | `dtk6core` |

### 1.5 DTK5 与 DTK6 API 差异

DTK6 中已移除的 API（DTK5 仍可用）：`DApplicationHelper`、`DApplicationSettings`、`DThemeManager`、`DImageButton`、`DSegmentedControl`、`DToast`、`DArrowLineExpand`、`DExpandGroup`。

DTK6 移除了 `gsettings-qt` 和 `libxdg` 依赖。

### 1.6 开发原则

- **除了 dtkdeclarative 的 QML 部分只维护 DTK6（DTK5 仅需保证编译通过和运行），其余项目（dtkcore、dtkgui、dtkwidget、dtklog）的 DTK5 和 DTK6 都需要完整支持**
- 新需求/Bug 修复优先保证 DTK6，同时确保 DTK5 也能编译运行并保持功能一致

---

## 2. 安装编译依赖

DTK 项目通过 `debian/control` 声明编译依赖，使用 `apt build-dep` 自动安装，无需手动列出包名。

### 2.1 安装编译依赖

```bash
# 进入目标项目目录
cd <dtk-project-path>

# 自动安装 debian/control 中声明的所有编译依赖
sudo apt build-dep .
```

### 2.2 构建 Profile

DTK 项目通过 debian build profile 控制 DTK5/DTK6 构建：

```bash
# 仅编译 DTK5（跳过 DTK6 包）
dpkg-buildpackage -b -Pnodtk6

# 仅编译 DTK6（跳过 DTK5 包）
dpkg-buildpackage -b -Pnodtk5

# 跳过文档包，加速编译
dpkg-buildpackage -b -Pnodoc

# 组合使用：仅 DTK5 + 跳过文档
dpkg-buildpackage -b -Pnodtk6,nodoc
```

如果只是本地 cmake 编译调试，直接用 `-DDTK5=ON` 或 `-DDTK5=OFF` 即可（见第 3 节）。

---

## 3. 编译命令

### 3.1 DTK 项目编译

```bash
mkdir -p build && cd build

# 编译 DTK5
cmake .. -DDTK5=ON -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=/usr
make -j$(nproc)

# 编译 DTK6
cmake .. -DDTK5=OFF -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=/usr
make -j$(nproc)
```

### 3.2 编译选项

| 选项 | 说明 |
|------|------|
| `-DDTK5=ON` / `-DDTK5=OFF` | 切换 DTK5/DTK6 编译目标 |
| `-DCMAKE_BUILD_TYPE=Debug` | Debug 构建，带调试符号，使用 `-O0 -g -fno-omit-frame-pointer` |
| `-DCMAKE_BUILD_TYPE=Release` | Release 构建，DTK 使用 `-Ofast` 替代 `-O3` |
| `-DCMAKE_INSTALL_PREFIX=/usr` | 安装路径，DTK 项目编译时建议指定 |
| `-DENABLE_TESTING=ON` | 启用单元测试编译 |

### 3.3 平台插件

两个平台插件建议直接安装到系统中测试：

```bash
cmake .. -DDTK5=OFF -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=/usr
make -j$(nproc)
sudo make install
```

---

## 4. 调试

### 4.1 使用本地编译的库调试

当本地编译了 DTK 项目后，在没有安装到系统的情况下，通过环境变量指向本地 build 目录来调试：

```bash
# 本地编译了 dtkwidget 和 dtkdeclarative，运行使用了它们的应用
LD_LIBRARY_PATH=/path/to/dtkwidget/build6/src \
LD_LIBRARY_PATH=/path/to/dtkdeclarative/build6/qt6/src:$LD_LIBRARY_PATH \
./build6/examples/collections/collections

# 本地编译了 dtkdeclarative，运行 dde-control-center 测试 QML 效果
LD_LIBRARY_PATH=/path/to/dtkdeclarative/build6/qt6/src \
QML_IMPORT_PATH=/path/to/dtkdeclarative/build6/plugins \
dde-control-center -s
```

| 环境变量 | 作用 | 示例值 |
|----------|------|--------|
| `LD_LIBRARY_PATH` | 运行时库搜索路径 | `/path/to/dtkdeclarative/build6/qt6/src` |
| `QML_IMPORT_PATH` | QML 模块搜索路径 | `/path/to/dtkdeclarative/build6/plugins` |

### 4.2 QT 调试变量

| 环境变量 | 作用 | 示例值 |
|----------|------|--------|
| `QT_QPA_PLATFORM` | 指定平台插件 | `dxcb`（X11 深度集成）, `offscreen`（无头测试）, `wayland` |
| `QT_QPA_PLATFORM_PLUGIN_PATH` | 自定义平台插件搜索路径 | `./plugins/platforms` |
| `QT_LOGGING_RULES` | Qt 日志分类过滤 | `qt.qpa.*=true`, `*.debug=false` |

### 4.3 DTK 专用调试变量

| 环境变量 | 作用 | 示例值 |
|----------|------|--------|
| `DTK_DISABLED_LOGGING_RULES` | 禁用 DTK 自动日志规则 | `1`（任意非空值） |
| `DTK_LOGGING_FALLBACK_APPID` | 日志框架回退应用 ID | `myapp` |
| `DTK_FORCE_CONSOLE_LOGGING` | 强制输出日志到控制台 | `1` |
| `DTK_FORCE_RASTER_WIDGETS` | 强制光栅渲染模式 | `1` |
| `DTK_DISABLED_SPECIAL_EFFECTS` | 禁用 DTK 特效 | `1` |
| `D_DTK_DISABLE_ANIMATIONS` | 禁用 DTK 动画 | `1`（任意非空值） |
| `D_DTK_SIZEMODE` | 覆盖 DConfig 尺寸模式设置 | `compact` |
| `DXCB_FAKE_PLATFORM_NAME_XCB` | 使用 DXCB 时设置为 `true` | `true` |
| `DTK_USE_SEMAPHORE_SINGLEINSTANCE` | 用信号量实现单实例（替代 DBus） | `1` |
| `DTK_DBUS_SINGLEINSTANCE` | Flatpak 环境 DBus 单实例兼容 | `1` |
| `DDE_SESSION_PROCESS_COOKIE_ID` | DDE 会话 cookie | DDE 内部使用 |

### 4.4 调试工具变量

| 环境变量 | 作用 | 示例值 |
|----------|------|--------|
| `ASAN_OPTIONS` | AddressSanitizer 选项 | `halt_on_error=0:new_delete_type_mismatch=0` |

### 4.5 调试启动示例

```bash
# 在 X11 下使用本地编译的库调试
LD_LIBRARY_PATH=./build6/src \
QT_QPA_PLATFORM=dxcb \
QT_LOGGING_RULES="*.debug=true" \
D_DTK_DISABLE_ANIMATIONS=1 \
./myapp

# 无图形界面的调试（off-screen）
QT_QPA_PLATFORM=offscreen \
DTK_DISABLED_SPECIAL_EFFECTS=1 \
./myapp

# 使用 ASan 调试
ASAN_OPTIONS="halt_on_error=0:new_delete_type_mismatch=0" \
QT_QPA_PLATFORM=dxcb \
./myapp
```
