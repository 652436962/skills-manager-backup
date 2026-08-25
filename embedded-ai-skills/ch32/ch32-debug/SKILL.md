---
name: "ch32-debug"
description: "CH32 调试排错。运行时 crash / RISC-V Trap/HardFault / 外设不工作 / 编译链接问题，通过串口日志 + WCH-Link/OpenOCD 定位根因。Call after flash programming if target misbehaves."
---

# CH32 调试排错

> 方法：**串口日志**（最快）→ **OpenOCD/WCH-Link 调试**（深层次）→ **根因分析** → **报告输出**

---

## Pre-flight: 收集问题信息

| 必问项 | 示例 |
|--------|------|
| 芯片型号 | CH32V307 |
| 现象 | 上电 LED 不闪 / 死机 / 数据不对 |
| 最近改动 | 刚加了 XX 外设 |

## Step 1: 串口日志（第一优先）

### 打开调试串口

```bash
# Linux 常见 USB 转串口
ls /dev/ttyUSB* /dev/ttyACM*
# 例：minicom 连接 115200-8-N-1
minicom -D /dev/ttyUSB0 -b 115200
# 或 screen
screen /dev/ttyUSB0 115200
```

### 确认 printf 重定向已生效

```c
// main.c 中调用，底层依赖 Debug/debug.c
USART_Printf_Init(115200);
printf("SystemClk:%d\r\n", SystemCoreClock);
```

| 现象 | 结论 |
|------|------|
| 有打印且正常 | 程序已运行，问题在具体逻辑/外设 |
| 无打印但 LED 正常 | 只查 printf 重定向/串口线 |
| 完全无反应 | 程序未运行 → 进 Step 2 硬件调试 |

## Step 2: OpenOCD 硬件调试（程序未运行 / 死机）

```bash
# 连接 + 读取 CPU 状态
openocd -f interface/wch-link.cfg -f target/wch_riscv.cfg \
    -c "init" -c "halt" -c "reg pc" -c "reg mepc" -c "reg mcause" -c "shutdown"
```

### 判断依据

| mcause | 含义 | 排查方向 |
|--------|------|---------|
| `3` | 机器软件中断（定时器等） | 检查中断服务函数是否已实现 |
| `7` | 机器定时器中断 | 定时器配置 / 时钟分频 |
| `11` | 外部中断 | EXTI / NVIC 配置 |
| `2` | 非法指令 | 指令集不匹配（软/硬浮点 ABI 混用） |
| `0` | 指令取指错误 | 跳转到无效地址 / 未初始化函数指针 |
| `1` | 指令访问错误 | 访问了未使能的外设地址 |
| `5` | 断点 | 正常调试暂停 |
| `6` | 取指总线错误 | 地址越界 |

### RISC-V Trap 排查（core_riscv.c 的 TrapHandler）

- `mepc`：出错指令地址 → 用 `riscv-none-embed-addr2line -e <APP>.elf <mepc>` 定位到源码行
- `mcause`：异常类型（上表）
- `mtval`：访问出错的目标地址

```bash
riscv-none-embed-addr2line -e build/<APP>/<APP>.elf 0x0000012c
```

## Step 3: 常见问题根因速查

### 1. 编译/链接

| 问题 | 原因 | 解决 |
|------|------|------|
| `cannot open linker script` | SRC 路径错 | 检查顶层 CMakeLists 的 `SRC_DIR` |
| 缺外设符号 | 静态库 `--gc-sections` 丢弃未引用 .c | 把对应 `.c` 直接加进 APP_SRCS |
| `riscv-none-embed-gcc: No such file` | 工具链不在 PATH | 加 PATH 或用 MRS 内置工具链 |
| 指令集 ABI 不匹配 | 不同文件 march/mabi 不一致 | 统一 `-march=rv32imac -mabi=ilp32` |

### 2. 运行时

| 现象 | 原因 | 解决 |
|------|------|------|
| 上电完全无反应 | 烧录地址错 / 启动文件缺失 | 确认烧到 0x00000000，检查 Link.ld |
| 程序卡在 Trap | 外设时钟未使能 | `RCC_APB1/APB2PeriphClockCmd(..., ENABLE)` |
| EXTI 不进中断 | 缺 AFIO 时钟或 `GPIO_EXTILineConfig` | 开 AFIO 时钟 + 配置线映射 |
| DMA 不工作 | 通道/外设请求配置错 | 核对 DMA_Channel 与外设请求映射表 |
| 浮点计算异常 | 硬浮点型号用了软浮点 ABI 或反之 | 全工程统一 march/mabi |
| printf 无输出 | 缺 `debug.c` 或未初始化 | 链接 debug.c 并调用 `USART_Printf_Init` |
| 复位原因不明确 | — | 用 RCC 复位标志：`RCC_GetFlagStatus(RCC_FLAG_... )` |

### 3. 外设不工作（通用排查顺序）

1. **时钟**：外设对应 `RCC_APBxPeriphClockCmd` 是否 ENABLE
2. **GPIO 复用**：`GPIO_PinRemapConfig` / `GPIO_Mode` 是否正确（如 USART 的 `GPIO_Mode_AF_PP`）
3. **中断**：`NVIC_Init` 优先级分组 + `ch32v30x_it.c` 中的服务函数名是否与向量表一致
4. **引脚冲突**：CH32V307 多个外设复用同一引脚（如 PA9 既是 USART1_TX 又是 DVP_D0），确认无冲突
5. **参考官方例程**：对照 opench-ch32v307/firmware 仓库的例程排查寄存器配置

## Step 4: 修复与验证

- 修改后重新编译烧录，回到 Step 1 串口日志验证
- 每改一个变量（时钟 / 引脚 / 中断）做一次小步验证，避免大改

## Step 5: 输出调试报告

- **现象描述**：发生了什么（串口日志、LED 状态）
- **根因**：明确到寄存器/配置项
- **修复方案**：具体修改内容
- **验证结果**：修改后现象是否消失

## 常用命令汇总

```bash
# 连接并读寄存器
openocd -f interface/wch-link.cfg -f target/wch_riscv.cfg -c "init" -c "halt" -c "reg" -c "shutdown"

# 程序烧录 + 复位运行
openocd -f interface/wch-link.cfg -f target/wch_riscv.cfg \
    -c "program <APP>.elf verify reset exit"

# 地址转源码行（mepc/mcause 定位）
riscv-none-embed-addr2line -e <APP>.elf <address>

# 反汇编
riscv-none-embed-objdump -S <APP>.elf | less
```
