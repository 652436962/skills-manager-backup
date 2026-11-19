# CHANGELOG

## 版本索引

| 版本 | 日期/说明 |
| ---- | --------- |
| [V1.3.0](#v1.3.0) | 2026-11-19 (cc511b9) |

<a id="v1.3.0"></a>
## [V1.3.0] - 2026-11-19

### 功能新增：设备状态上屏推送程序

**背景**：采集器持续写入最新分钟数据，需要把设备状态按自定义字库协议推送到 LED 屏。

**主要功能：**

- 每分钟第 `copy_second` 秒原子复制 `/lechi/data/latest.dat` 到 `/lechi/display/lastest.dat`；
- 解析 CSV，支持 `CNC`/`CDP`/`CDPT` 等 2 字段变长要素，避免整行错位；
- 2 页 × 4 行、24 点阵，页面按 `page_interval_sec` 轮播；
- `align=left` + 行首空格手动布局，支持一行多内容 `|` 分割；
- 0xD1 文字、0xD4 校时（长度 8、年份大端）、0xD5 亮度；
- 连续失败/数据过期时强制状态页显示“通信中断”；
- 程序内建日志：4 MB × 4 归档、保留 3 天、跨天轮转；
- Buildroot `S99display` 启动脚本；
- `--once`、`--dry-run`、`--verbose`、`--config`；
- 一天数据读取与冠层缓存内部库。

### 优化：Buildroot 部署

- CMakeLists 默认写死 OK3568 交叉编译器，支持 `OK3568_CROSS=OFF` 本机测试；
- 增加 `scripts/package.sh`、`deploy.sh`、`install.sh`，生成 `lib/display-ok3568.tar.gz`；
- 部署包包含 `lib/gconv`，解决目标机 `iconv_open(GB2312) failed`；
- 兼容 BusyBox tar（使用 `gzip -dc | tar xf -`）。

### 缺陷修复：现场路径与显示内容

**现象**：设备上复制源文件失败；屏上内容不显示；日志看不到实际推送文本。

**根因**：

- 源路径曾写成 `/lechi/date/lastest.dat`，实际为 `/lechi/data/latest.dat`；
- 目标 rootfs 缺少 glibc gconv 模块；
- 日志只记录帧数，没有记录渲染文本。

**修改：**

- `src_file` 默认值和 `display.conf` 改为 `/lechi/data/latest.dat`；
- 增加 `lib/gconv` 和安装脚本；
- 每个数据轮打印第 1 页 4 行实际文本，`debug` 级别打印帧十六进制和页面切换文本。

### 验证

- 本机 CMake 构建、`ctest` 全部通过；
- OK3568 交叉编译通过，产物为 aarch64；
- qemu 运行 `display --version` 和核心测试通过；
- LED 屏模拟器验证：校时、亮度、2 页显示、居中/空格布局、页面轮播、通信中断页、恢复均正常。

**修改文件：** `CMakeLists.txt`, `src/`, `tests/`, `scripts/`, `lib/`, `display.conf`, `README.md`, `docus/`

**版本记录：** `VERSION` 中 `GIT_COMMIT=cc511b9`，标签 `v1.3.0`。
