---
name: "embedded_ai_skills"
description: "嵌入式 AI 开发技能集合入口 skill。自动索引全部子 skill，覆盖 ESP32、nRF528xx、STM32、ZMK 键盘固件以及辅助工具（EasyEDA、串口调试）的完整开发流程。当用户进行嵌入式开发（MCU 芯片、固件开发、烧录调试）时调用。"
---

# Embedded AI Skills — 嵌入式开发技能集

一个覆盖主流嵌入式平台的端到端开发技能集合。

## 子 Skill 索引

| Skill | 文件 | 功能 |
|-------|------|------|
| **esp32** | [SKILL.md](esp32/SKILL.md) | ESP32 系列入口：IDF / Arduino 框架选择、开发、调试 |
| **nrf-528xx** | [SKILL.md](nrf-528xx/SKILL.md) | nRF528xx 入口：SDK 安装、项目初始化、调试 |
| **stm32** | [SKILL.md](stm32/SKILL.md) | STM32 入口：环境安装、项目初始化、调试 |
| **stm32-dev** | [SKILL.md](stm32-dev/SKILL.md) | STM32 纯 CLI 开发指南（无需 CubeMX / CubeIDE GUI） |
| **tools** | [SKILL.md](tools/SKILL.md) | 工具类：EasyEDA 原理图/PCB 设计、串口调试 |
| **zmk-project-init** | [SKILL.md](zmk-project-init/SKILL.md) | ZMK 键盘固件项目创建/配置/编译/烧录 |

## 使用方式

描述你的嵌入式开发需求，系统会自动定位并调用对应子 skill 的完整流程。例如：

- "ESP32 开发环境搭建" → 调用 `esp32` 下的 esp32-dev / esp32-dev-idf / esp32-dev-arduino
- "nRF52840 项目初始化" → 调用 `nrf-528xx` 下的 nrf-connect-project-init
- "STM32 编译报错" → 调用 `stm32` 下的 stm32-debug
- "创建 ZMK 键盘项目" → 调用 `zmk-project-init`
