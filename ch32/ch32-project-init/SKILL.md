---
name: "ch32-project-init"
description: "CH32 项目初始化。芯片选型 → 开发模式（标准外设库 SPL/CMSIS 寄存器, C/C++）→ 时钟配置 → 外设配置 → 生成 CMake 工程 → 编译 → 烧录。完整可执行的开发全流程。"
---

# CH32 项目初始化

> 核心流程：**芯片选型 → 开发模式 → 时钟 → 外设 → 生成工程 → 编译 → 烧录**

---

## Step 0: 芯片选型（确认芯片型号）

| 型号 | 内核 | 主频 | Flash/RAM | 特色外设 |
|------|------|------|-----------|---------|
| CH32V003 | RV32EC | 48MHz | 16KB/2KB | 最便宜入门 |
| CH32V103 | RV32IMAC | 72MHz | 64KB/20KB | 替代 STM32F103 |
| CH32V203 | RV32IMAC | 144MHz | 256KB/64KB | 大容量通用 |
| CH32V208 | RV32IMAC | 144MHz | 128KB/64KB | BLE 5.3 + 以太网 |
| CH32V303 | RV32IMAC | 144MHz | 256KB/64KB | 通用增强 |
| CH32V305 | RV32IMACF | 144MHz | 256KB/64KB | USB2.0 高速 OTG |
| **CH32V307** | **RV32IMACF** | **144MHz** | **256KB/64KB** | **USB 高速 + 千兆以太网(内置10M PHY) + DVP + FSMC** |
| CH32V317 | RV32IMACF | 144MHz | 128KB/64KB | USB 高速 + 千兆以太网 |

**关键判断：**
- `RV32IMACF`（V305/V307/V317）带单精度硬件浮点，可用 `-march=rv32imacf -mabi=ilp32f`；也可按软浮点 `-march=rv32imac -mabi=ilp32` 编译（例程默认软浮点，兼容性最好）
- 外设库：`ch32v10x`（V103）、`ch32v20x`（V203/V208）、`ch32v30x`（V303/V305/V307/V317）、CH32V003 用 MRS 专用库
- 调试口 SWD：CH32V307/305/317 为 **PA13/PA14**，其余系列也是 PA13/PA14

## Step 1: 确认开发模式

| 模式 | 适用 | 特点 |
|------|------|------|
| **SPL 标准外设库** | 大部分项目 | 函数级封装（`GPIO_Init`/`USART_Init`），开发快，推荐 |
| 寄存器直操作 | 极致精简/学习 | 依赖 `ch32v30x.h` 头文件定义，可混合 SPL |
| C / C++ | 任选 | C++ 需在编译选项加 `-fno-exceptions -fno-rtti` 等 |

## Step 2: 时钟配置

`system_ch32v30x.c` 中的 `SYSTEM_CLOCK` 宏决定系统时钟（HSE/HSI 倍频到 PLL）：

| SYSTEM_CLOCK | 主频 | 说明 |
|--------------|------|------|
| `SYSTEM_CLOCK_8MHZ` | 8MHz | 内部/外部晶振直通 |
| `SYSTEM_CLOCK_72MHZ` | 72MHz | 与 STM32F1 常用时钟一致 |
| `SYSTEM_CLOCK_96MHZ` | 96MHz | |
| `SYSTEM_CLOCK_120MHZ` | 120MHz | |
| `SYSTEM_CLOCK_144MHZ` | 144MHz | 满频，需确认外设总线时钟分频 |

> 注意：APB1/APB2 分频由 `RCC_APB1PeriphClockCmd`/`RCC_APB2PeriphClockCmd` 配置，定时器时钟会自动 ×2，与 STM32 SPL 一致。

## Step 3: 外设配置（对话式收集）

向用户收集（缺失时给默认值，直接继续）：

| 项 | 默认值 |
|----|--------|
| 目标芯片 | CH32V307VCT6 |
| 主频 | 144MHz |
| 调试口 | USART1 / PA9(TX), PA10(RX) / 115200-8-N-1 |
| 构建系统 | CMake + Ninja（命令行）或 MRS |
| 外设 | 按需（GPIO/USART/SPI/I2C/ADC/TIM/DMA/ETH/DVP/FSMC/CAN/USB...） |

## Step 4: 生成工程结构

```
<project>/
├── CMakeLists.txt          # 顶层：工具链 + 外设库 + 子目录
├── common/                 # 共享文件（例程风格）
│   ├── ch32v30x_conf.h     # 外设库配置（按需开启 .h 包含）
│   ├── system_ch32v30x.c   # 系统时钟（SYSTEM_CLOCK 宏）
│   └── system_ch32v30x.h
├── User/
│   ├── main.c              # 用户主程序
│   ├── ch32v30x_it.c       # 中断服务函数
│   └── ch32v30x_it.h
└── SRC/                    # 标准外设库（引用仓库或拷贝）
    ├── Core/core_riscv.c
    ├── Debug/debug.c
    ├── Peripheral/src/*.c
    ├── Peripheral/inc/*.h
    ├── Startup/startup_ch32v30x.S
    └── Ld/Link.ld
```

**SPL 外设库获取**：优先复用已有仓库（如 `opench-ch32v307/firmware/SRC`），否则从 MRS 示例工程或官方 GitHub 复制。

**`ch32v30x_conf.h` 要点**：按需 `#include "ch32v30x_<外设>.h"`（含 `ch32v30x_eth.h`/`ch32v30x_dvp.h` 等特色外设），并定义 `USE_STDPERIPH_DRIVER` 与 `SYSTEM_CLOCK` 宏（后者也可在 system 文件定义）。

## Step 5: CMakeLists 模板（例程工程实际验证）

### 顶层 `CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.10)
project(<PROJECT> C ASM)

# ---------- 工具链 ----------
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR RISCV)
set(TOOLCHAIN_PREFIX riscv-none-embed-)
if(WIN32)
    set(TOOLCHAIN_SUFFIX ".exe")
else()
    set(TOOLCHAIN_SUFFIX "")
endif()
set(CMAKE_C_COMPILER ${TOOLCHAIN_PREFIX}gcc${TOOLCHAIN_SUFFIX})
set(CMAKE_ASM_COMPILER ${TOOLCHAIN_PREFIX}gcc${TOOLCHAIN_SUFFIX})
set(CMAKE_OBJCOPY ${TOOLCHAIN_PREFIX}objcopy${TOOLCHAIN_SUFFIX})
set(CMAKE_OBJDUMP ${TOOLCHAIN_PREFIX}objdump${TOOLCHAIN_SUFFIX})
set(CMAKE_SIZE ${TOOLCHAIN_PREFIX}size${TOOLCHAIN_SUFFIX})

# ---------- 编译选项（按芯片选 march/mabi） ----------
set(MCU_FLAG "-march=rv32imac -mabi=ilp32")   # V307 默认软浮点
set(CMAKE_C_FLAGS "${MCU_FLAG} -Og -g -ffreestanding -fno-common")
set(CMAKE_ASM_FLAGS "${MCU_FLAG} -Og -g -ffreestanding")
set(CMAKE_EXE_LINKER_FLAGS
    "${MCU_FLAG} -nostartfiles -Xlinker --gc-sections --specs=nano.specs --specs=nosys.specs")

# ---------- SPL 外设库 ----------
set(SRC_DIR "<SPL库路径>/SRC")
set(LINKER_SCRIPT "${SRC_DIR}/Ld/Link.ld")
file(GLOB SRC_SRCS
    "${SRC_DIR}/Core/core_riscv.c"
    "${SRC_DIR}/Debug/debug.c"
    "${SRC_DIR}/Peripheral/src/*.c"
    "${SRC_DIR}/Startup/startup_ch32v30x.S"
    "${CMAKE_CURRENT_SOURCE_DIR}/common/system_ch32v30x.c")
add_library(CH32SRC STATIC ${SRC_SRCs})
target_include_directories(CH32SRC PUBLIC
    "${SRC_DIR}/Core"
    "${SRC_DIR}/Debug"
    "${SRC_DIR}/Peripheral/inc"
    "${CMAKE_CURRENT_SOURCE_DIR}/common")

add_subdirectory(<APP>)
```

### 子工程 `CMakeLists.txt`（每个应用一个目录）

```cmake
get_filename_component(APP_NAME ${CMAKE_CURRENT_SOURCE_DIR} NAME)
file(GLOB_RECURSE APP_SRCS "${CMAKE_CURRENT_SOURCE_DIR}/User/*.c")
add_executable(${APP_NAME}.elf ${APP_SRCS})
target_include_directories(${APP_NAME}.elf PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/User")
target_link_libraries(${APP_NAME}.elf CH32SRC)
set_target_properties(${APP_NAME}.elf PROPERTIES
    LINK_FLAGS "-T${LINKER_SCRIPT}"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${APP_NAME}")
add_custom_command(TARGET ${APP_NAME}.elf POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} -O binary "$<TARGET_FILE:${APP_NAME}.elf>" "${CMAKE_BINARY_DIR}/${APP_NAME}/${APP_NAME}.bin"
    COMMAND ${CMAKE_OBJCOPY} -O ihex   "$<TARGET_FILE:${APP_NAME}.elf>" "${CMAKE_BINARY_DIR}/${APP_NAME}/${APP_NAME}.hex"
    COMMAND ${CMAKE_SIZE} "$<TARGET_FILE:${APP_NAME}.elf>"
    COMMENT "Generate ${APP_NAME} bin/hex")
```

> **静态库符号抽取陷阱**：若链接报错提示库内符号未定义（如被闭源库引用的 `ETH_ReadPHYRegister`），说明该 `.c` 未被抽取——将对应 `.c` 直接从库中拆出、加入 `APP_SRCS` 直接编译进目标即可。

## Step 6: main.c 骨架

```c
#include "ch32v30x.h"

void GPIO_Config(void);   // 外设配置函数

int main(void)
{
    SystemCoreClockUpdate();   // 或 NVIC_PriorityGroupConfig + Delay_Init
    Delay_Init();
    USART_Printf_Init(115200); // 需要 debug.c / printf 重定向
    GPIO_Config();

    printf("SystemClk:%d\r\n", SystemCoreClock);
    while(1)
    {
        // 主循环
    }
}

void GPIO_Config(void)
{
    GPIO_InitTypeDef GPIO_InitStructure = {0};

    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC, ENABLE);
    GPIO_InitStructure.GPIO_Pin  = GPIO_Pin_0;           // PC0: LED
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOC, &GPIO_InitStructure);
}
```

**中断服务函数**写在 `ch32v30x_it.c`（如 `EXTI7_IRQHandler`、`TIM2_IRQHandler`），函数名必须与启动文件 `startup_ch32v30x.S` 的向量表一致。

## Step 7: 编译

```bash
cmake -S . -B build -G Ninja
cmake --build build
# 产物：build/<APP>/<APP>.elf / .hex / .bin
```

## Step 8: 烧录（三选一）

### 方式 1: WCH-Link + OpenOCD（推荐，可调试）

```bash
openocd -f interface/wch-link.cfg -f target/wch_riscv.cfg \
    -c "program build/<APP>/<APP>.elf verify reset exit"
```

### 方式 2: wchisp（CLI 烧录，无需 OpenOCD）

```bash
wchisp flash build/<APP>/<APP>.bin
```

### 方式 3: WCHISPTool（串口 ISP，无需调试器）

1. 目标板 BOOT0 拉高 → 复位进入 Bootloader
2. WCHISPTool 选择芯片与串口，下载 `<APP>.hex`
3. 烧录完成 BOOT0 拉低复位运行

> CH32 的 Flash 起始地址为 **0x00000000**（不是 STM32 的 0x08000000），链接脚本 `Link.ld` 已处理，无需手动偏移。

---

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `cannot open linker script` | SRC 路径错误 | 检查 `SRC_DIR` 与 `LINKER_SCRIPT` |
| 链接缺符号（外设 .c 未被抽） | 静态库 `--gc-sections` 丢弃 | 将对应 `.c` 直接加入 APP_SRCS |
| 上电不运行 | 烧录地址/启动文件缺失 | 确认 `.hex` 起始于 0x00000000，检查 `startup_ch32v30x.S` 已链接 |
| printf 不输出 | 缺 `debug.c` 或 `printf` 重定向 | 链接 `Debug/debug.c`（`USART_Printf_Init`） |
| 警告：`printf` 隐式声明 | 库文件缺 `stdio.h` | 对单个文件加 `-Wno-implicit-function-declaration` |
| EXTI 中断不进 | 未开 `AFIO` 时钟/映射 | `RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE)` + `GPIO_EXTILineConfig` |

## 后续

编译烧录后出现运行问题时，调用 `ch32-debug` skill 排查。
