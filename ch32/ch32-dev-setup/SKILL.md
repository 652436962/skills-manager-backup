---
name: "ch32-dev-setup"
description: "CH32 开发环境安装。跨平台（Windows/macOS/Linux）支持，兼容 MounRiver Studio（路径A）和纯 CLI（路径B）两种方式。检测已有安装，仅安装缺失组件。覆盖 riscv-none-embed 工具链、WCH-Link 调试器、OpenOCD/wchisp 烧录工具。Call first before any CH32 development."
---

# CH32 开发环境安装

> 跨平台支持：**Windows** / **macOS** / **Linux**。
> 两条路径任选：**路径 A**（MounRiver Studio 已安装）或 **路径 B**（纯 CLI，全部开源）。

---

## Pre-flight: 环境检测（⚠️ 必须最先执行）

### Shell 检测

```
AI 操作流程:
1. 执行 uname -s 检测当前环境
2. 根据结果判断:
```

| `uname -s` 输出 | 平台/Shell | AI 动作 |
|-----------------|-----------|---------|
| `Linux` | Linux ✅ | 继续工具链检测 |
| `Darwin` | macOS ✅ | 继续工具链检测 |
| `MSYS_NT-*` / `MINGW64_NT-*` | Windows + MSYS2 ✅ | 继续工具链检测 |
| **其他** (含 PowerShell 执行失败) | **Windows 非 MSYS2** ❌ | 引导使用 MSYS2 / Git Bash / MRS 内置终端 |

### 工具链检测

#### 1. 检测 MRS（路径 A）

```bash
# Windows
ls -d "/c/MounRiver"*/MounRiver_Studio.exe 2>/dev/null
# Linux / macOS
ls -d "$HOME/MounRiver"* 2>/dev/null
```

#### 2. 检测独立工具链包 MRS_Toolchain（Linux）

```bash
# 通配匹配任意版本（当前 V240，后续升级版本号变化也自动覆盖）
ls -d "$HOME"/MRS_Toolchain_Linux_X64_V* 2>/dev/null
```

#### 3. 检测系统工具链（路径 B）

```bash
riscv-none-embed-gcc --version 2>/dev/null | head -1
cmake --version 2>/dev/null | head -1
ninja --version 2>/dev/null
which wchisp 2>/dev/null
```

#### 4. 判断路径

| 条件 | 路径 | 说明 |
|------|------|------|
| MRS 已安装 | **路径 A** | 取其内置 riscv-none-embed-gcc + OpenOCD |
| 存在 `~/MRS_Toolchain_Linux_X64_V*` | **路径 B** | 用该独立工具链包（含 GCC + OpenOCD）；多版本并存时取版本号最新者 |
| 无 MRS + 工具链就绪 | **路径 B** | 纯 CLI，全部开源 |
| 无 MRS + 工具链缺失 | **先装工具链 → 路径 B** | AI 自动从官网下载最新包（见「缺失处理」）→ 解压到 `~/`；API 不可用时提示用户手动下载 |

> ⚠️ **缺失处理（重要）**：独立工具链包命名带版本号（`MRS_Toolchain_Linux_X64_V*`，当前 V240），**不硬编码任何版本**，一律以官网 API 返回的最新版本为准。包体积大（V240 约 393MB、解压后约 2.7GB），下载耗时较长，**AI 执行下载前应先告知用户来源与体积**，然后按 Step 1「自动下载」流程操作：
>
> 1. 官网 API 查询最新版本 → 获取签名直链 → `curl` 下载到 `~/Downloads/`（命令见 Step 1，2026-09 验证可用）
> 2. 下载成功后解压到 `~/`，以实际解压出的目录 `~/MRS_Toolchain_Linux_X64_V*` 为基准继续配置
> 3. 若 API 不可用（网络不通 / 官网改版），**停止自动下载**，向用户输出以下提示，待用户告知压缩包路径后从 Step 1 步骤 2 继续：
>
> ```
> 无法从官网自动获取工具链（https://mounriver.com/download），请手动下载最新版
> MRS_Toolchain_Linux_X64_V*.tar.xz 后告诉我压缩包路径，解压与配置由我来完成。
> ```

---

## Step 1: 安装工具链（仅缺失项）

### 路径 A: MounRiver Studio（Windows / Linux）

从沁恒官网下载 MRS 安装包（含 IDE + riscv-none-embed 工具链 + OpenOCD + WCH-Link 驱动）。

Linux 版解压后工具链路径通常为：
```
<MRS解压目录>/tools/RISC-V Embedded GCC/bin/riscv-none-embed-gcc
<MRS解压目录>/tools/OpenOCD/bin/openocd
```

### 路径 B: 纯 CLI

**工具链首选来源：MRS 官方 Linux x64 独立工具链包 `MRS_Toolchain_Linux_X64_V*`** —— 含 `riscv-none-embed` 交叉编译链 + OpenOCD，无需安装完整 IDE。命名带版本号（当前 V240），**不硬编码具体版本**，升级后以最新 release 为准；包体积较大（V240 约 393MB，`.tar.xz`，解压后约 2.7GB），以实际为准。

**解压位置：`~/`**，解压后目录为 `~/MRS_Toolchain_Linux_X64_V<版本>/`。压缩包内含同名顶层目录，执行 `tar -xJf <压缩包> -C ~` 即解压到位；解压后以实际目录名（记为 `$MRS_TC`）为基准配置 PATH 与验证，不写死版本号；若解压后目录名与 `MRS_Toolchain_Linux_X64_V*` 模式不符，应将其移到 `~/MRS_Toolchain_Linux_X64_V<实际版本>/` 后再配置。

> 来源：官网下载页 https://mounriver.com/download（「Linux → Toolchain&Debugger」区）。**AI 自动下载**：经官网 API 动态查询最新版本并获取签名直链后 curl 下载（见下）；API 不可用（网络/官网改版）时提示用户从该页面手动下载，AI 收到压缩包路径后继续。

**官网 API（自动下载链路，2026-09 验证可用；路径 B 首选）：**
- 版本查询：`GET https://api.mounriver.com/mountriver/api/version/fetchRecentOpenOcd?osType=LINUX&lang=zh`，`result[]` 中取 `version` 最大项，记录 `id` / `fileName` / `fileSize`
- 直链获取：`GET https://api.mounriver.com/mountriver/api/version/fetchRecentOpenOcdUrl?resourceId=<id>`，`result` 为带签名直链（含 `sign/time/from` 参数，**限时有效**，获取后须立即下载；中断重试需重新获取）
- 页面兜底：https://mounriver.com/download（人工下载入口，亦用于核对版本与文件大小）
- GitHub 仓库 release（社区维护镜像，用户自选）
- 若用户提供具体下载链接或版本号，一律以用户提供的为准

#### 安装流程（Linux）

分工：步骤 1~4 均由 AI 执行（下载前向用户说明来源与体积）；仅当 API 不可用、改由用户手动下载时，从步骤 2 开始。

```bash
# ===== 1. AI 从官网自动下载最新版工具链（版本/文件名由 API 返回，不硬编码） =====
# 1a. 查询版本列表（输出: <id> <version> <fileName> <fileSize>，可能多行，取 version 最大行）
curl -sL --max-time 30 "https://api.mounriver.com/mountriver/api/version/fetchRecentOpenOcd?osType=LINUX&lang=zh" \
  | python3 -c "import sys,json;[print(i['id'],i['version'],i['fileName'],i['fileSize']) for i in (json.load(sys.stdin).get('result') or [])]"
# 1b. 用上一步的 <id> 获取带签名直链（限时有效，立即执行 1c）
dlurl=$(curl -sL --max-time 30 "https://api.mounriver.com/mountriver/api/version/fetchRecentOpenOcdUrl?resourceId=<id>" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['result'])")
# 1c. 下载到 ~/Downloads（断点续传；392MB 需数分钟，可后台执行）
mkdir -p "$HOME/Downloads"
curl -L -C - --max-time 3600 -o "$HOME/Downloads/<fileName>" "$dlurl"
ls -l "$HOME/Downloads/<fileName>"   # 校验：字节数应等于 1a 输出的 fileSize，不符则删除重下

# ===== 2. AI 解压到指定目录 ~/（若为手动下载的包，先用其路径替换 $HOME/Downloads/<fileName>） =====
tar -xJf "$HOME/Downloads/<fileName>" -C ~
# 解压后取实际目录，口径与 Pre-flight 检测一致：多版本并存时取版本号最新者
MRS_TC=$(ls -d "$HOME"/MRS_Toolchain_Linux_X64_V* | sort -V | tail -1)
echo "MRS_TC=$MRS_TC"   # 确认解压出的实际目录

# ===== 3. AI 配置 PATH（当前会话生效） =====
export PATH="$MRS_TC/Toolchain/RISC-V Embedded GCC/bin:$PATH"
export PATH="$MRS_TC/OpenOCD/OpenOCD/bin:$PATH"
# 持久化：将上面两条 export 中的 $MRS_TC 替换为第 2 步 echo 出的实际路径后，追加到 ~/.bashrc / ~/.zshrc

# ===== 4. AI 验证 =====
riscv-none-embed-gcc --version | head -1   # 应输出版本号
openocd --version | head -1
```

验证通过后，回到「Step 4: 验证环境」继续检查 cmake / ninja / wchisp，全部通过即完成环境安装。

#### 包内目录结构

```
~/MRS_Toolchain_Linux_X64_V<版本>/   # 版本号随包升级变化，如当前 V240
├── Toolchain/
│   ├── arm-none-eabi-gcc/
│   ├── RISC-V Embedded GCC/          # riscv-none-embed 编译链
│   │   └── bin/riscv-none-embed-gcc
│   ├── RISC-V Embedded GCC12/
│   ├── RISC-V Embedded GCC15/
│   └── sub_manifest.json
└── OpenOCD/
    └── OpenOCD/
        └── bin/openocd
```

> 提示：其他 GCC 版本（GCC12/GCC15）在同级目录，切换版本只需改 PATH 前缀；OpenOCD 的 wch-riscv 支持已内置，无需额外配置。

| 平台 | 工具 | 安装方式 |
|------|------|---------|
| **Linux（推荐）** | riscv-none-embed-gcc | 上述独立工具链包流程（`MRS_Toolchain_Linux_X64_V*`，当前 V240）；备选 xPack：https://github.com/xpack-dev-tools/riscv-none-embed-gcc-xpack/releases |
| **macOS** | riscv-none-embed-gcc | xPack 发行版（同上），解压后加入 PATH |
| **所有平台** | cmake / ninja | `apt install cmake ninja-build` / `brew install cmake ninja` |
| **所有平台** | wchisp（烧录） | `cargo install wchisp`（需 Rust）或从 https://github.com/ch32-rs/wchisp/releases 下载预编译包 |

---

## Step 2: WCH-Link 调试器支持

### 硬件接线

```
WCH-Link                    目标板
3V3   ────────────────→  3.3V
GND   ────────────────→  GND
SWDIO ────────────────→  SWDIO (CH32V307: PA13)
SWCLK ────────────────→  SWCLK (CH32V307: PA14)
```

> CH32V307/305/317 的 SWD 引脚为 PA13/PA14（与其他 CH32V 系列及 STM32 一致）。

### 模式检查（Windows）

WCH-Link 有 **RV 模式**（RISC-V 调试）和 **ARM 模式**（DAP-Link）两种固件模式，CH32 必须使用 **RV 模式**。用 WCH-LinkUtility 切换并确认指示灯状态。

> Linux/macOS 下 WCH-Link 免驱（USB HID），RV 模式下 Windows 也免驱。

### 验证 WCH-Link

```bash
lsusb | grep -i wch   # 应出现 WCH 设备
# 或
dmesg | grep -i ch34  # 常见 USB 转串口 CH340/CH341
```

---

## Step 3: OpenOCD 安装与配置

### 获取支持 wch-riscv 的 OpenOCD

MRS 内置的 OpenOCD 支持 `wch-riscv` 目标；开源版需确认编译时启用了 RISC-V 支持。

### 验证 OpenOCD

```bash
openocd -f interface/wch-link.cfg -f target/wch_riscv.cfg \
    -c "init" -c "halt" -c "reg" -c "resume" -c "shutdown" 2>&1
```

> 如能正常输出 RISC-V 寄存器（`x0`~`x31`、`pc`、`mstatus`、`mepc` 等），说明 WCH-Link 调试通道正常。

### 常见问题

| 现象 | 原因 | 解决 |
|------|------|------|
| `Error: open failed` | WCH-Link 处于 ARM 模式 | 用 WCH-LinkUtility 切到 RV 模式 |
| `target not halted` | SWD 接线错误/供电不足 | 检查接线，目标板独立供电 |
| `unable to find wch-link.cfg` | OpenOCD 版本过旧 | 使用 MRS 内置 OpenOCD |

---

## Step 4: 验证环境

### 工具链验证

```bash
riscv-none-embed-gcc --version | head -1
cmake --version | head -1
ninja --version
wchisp --version
```

### 烧录工具验证（wchisp）

```bash
wchisp list   # 列出已连接的 WCH-Link
```

| 结果 | 动作 |
|------|------|
| 列出 WCH-Link 设备 | ✅ 继续 |
| 无设备 | ❌ 检查 USB 连接与模式 |

---

## 完成标志

- [x] `riscv-none-embed-gcc --version` 正常
- [x] `cmake --version` 正常
- [x] `ninja --version` 正常
- [x] WCH-Link 处于 RV 模式且被系统识别
- [x] OpenOCD 能连接并读取 RISC-V 寄存器
- [x] `wchisp` 可用

## 后续

环境安装完毕后，使用 `ch32-project-init` skill 创建项目并编译烧录。
