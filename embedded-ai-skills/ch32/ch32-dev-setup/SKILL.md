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

#### 2. 检测系统工具链（路径 B）

```bash
riscv-none-embed-gcc --version 2>/dev/null | head -1
cmake --version 2>/dev/null | head -1
ninja --version 2>/dev/null
which wchisp 2>/dev/null
```

#### 3. 判断路径

| 条件 | 路径 | 说明 |
|------|------|------|
| MRS 已安装 | **路径 A** | 取其内置 riscv-none-embed-gcc + OpenOCD |
| 无 MRS + 工具链就绪 | **路径 B** | 纯 CLI，全部开源 |
| 无 MRS + 工具链缺失 | **先装工具链 → 路径 B** | 按下方对应平台命令安装 |

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

| 平台 | 工具 | 安装方式 |
|------|------|---------|
| **Linux / macOS** | riscv-none-embed-gcc | 下载 xPack 发行版：https://github.com/xpack-dev-tools/riscv-none-embed-gcc-xpack/releases ，解压后加入 PATH |
| **Linux (apt)** | riscv-none-embed-gcc | 无官方 apt 包，用上述 xPack 或 MRS 内置工具链 |
| **所有平台** | cmake / ninja | `apt install cmake ninja-build` / `brew install cmake ninja` |
| **所有平台** | wchisp（烧录） | `cargo install wchisp`（需 Rust）或从 https://github.com/ch32-rs/wchisp/releases 下载预编译包 |

**PATH 配置示例（Linux）：**

```bash
export PATH="$HOME/ch32-tools/riscv-none-embed/bin:$PATH"
```

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
