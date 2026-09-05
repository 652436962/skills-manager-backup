---
name: "ch32"
description: "CH32 系列 RISC-V 单片机开发入口 skill。自动索引子 skill 完成环境部署、项目初始化、调试排错全流程。当用户进行 CH32V 系列（CH32V003/103/203/208/303/305/307/317 等）开发时调用。"
---

# CH32 开发 Skill

针对沁恒 CH32V 全系列（V003/V103/V203/V208/V303/V305/V307/V317 等）RISC-V 单片机的端到端开发技能集。

## 子 Skill 索引

| Skill | 文件 | 功能 |
|-------|------|------|
| **ch32-dev-setup** | [SKILL.md](ch32-dev-setup/SKILL.md) | 环境检测 + 工具链配置（MRS_Toolchain_Linux_X64_V240 / MRS 内置 / xPack），缺失时提示手动下载；WCH-Link/OpenOCD/wchisp 支持，CLI/MRS 双路径 |
| **ch32-project-init** | [SKILL.md](ch32-project-init/SKILL.md) | 芯片选型 → 开发模式（SPL 标准外设库/CMSIS 寄存器, C/C++）→ 外设配置 → CMakeLists 生成 → 编译 → 烧录 |
| **ch32-debug** | [SKILL.md](ch32-debug/SKILL.md) | 串口日志 + WCH-Link/OpenOCD 调试，根因分析，RISC-V Trap/HardFault 排查 |

## 开发流程

```
ch32-dev-setup               ch32-project-init             ch32-debug
(环境安装)          ──→        (项目初始化)            ──→    (调试排错)
```

1. **ch32-dev-setup**：检测 Shell 环境与工具链，缺失时提示手动下载 `MRS_Toolchain_Linux_X64_V240`；配置 WCH-Link 调试器、OpenOCD/wchisp 烧录工具
2. **ch32-project-init**：收集芯片型号、开发模式、时钟方案、外设需求，生成 CMake 项目
3. **ch32-debug**：开发过程中排查编译错误、运行时 crash、外设驱动问题

## 使用方式

直接描述你的开发需求，系统会自动按需调用对应的子 skill。例如：

- "帮我搭建 CH32V307 开发环境" → 调用 `ch32-dev-setup`
- "创建一个 CH32V307 用标准外设库驱动 USART 的项目" → 调用 `ch32-project-init`
- "代码烧进去不运行，帮忙看看" → 调用 `ch32-debug`
