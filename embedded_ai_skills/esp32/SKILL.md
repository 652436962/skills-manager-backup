---
name: "esp32"
description: "ESP32 系列单片机开发入口 skill。自动索引子 skill 完成环境部署、项目初始化、调试排错全流程。当用户进行 ESP32/ESP32-S3/ESP32-C3 等芯片开发时调用。"
---

# ESP32 开发 Skill

针对乐鑫 ESP32 系列（ESP32, ESP32-S3, ESP32-C3 等）的端到端开发技能集。

## 子 Skill 索引

| Skill | 文件 | 功能 |
|-------|------|------|
| **esp32-dev** | [SKILL.md](esp32-dev/SKILL.md) | 开发入口：询问用户选择 IDF 或 Arduino 框架 |
| **esp32-dev-idf** | [SKILL.md](esp32-dev-idf/SKILL.md) | ESP-IDF 官方框架：环境搭建、编译烧录、JTAG 调试 |
| **esp32-dev-arduino** | [SKILL.md](esp32-dev-arduino/SKILL.md) | Arduino CLI：安装、编译、上传、监视 |
| **esp32-debug** | [SKILL.md](esp32-debug/SKILL.md) | 串口日志 + USB-JTAG (OpenOCD + GDB) 系统化调试 |

## 开发流程

1. **esp32-dev**：确认用户选择的开发框架（IDF / Arduino），加载对应子 skill
2. **esp32-dev-idf / esp32-dev-arduino**：环境搭建、项目创建、编译烧录、串口监视
3. **esp32-debug**：排查崩溃、异常、外设驱动问题

## 使用方式

直接描述你的开发需求，系统会自动按需调用对应的子 skill。例如：

- "帮我搭建 ESP32 的开发环境" → 调用 `esp32-dev`
- "用 ESP-IDF 创建一个 SPI 项目" → 调用 `esp32-dev-idf`
- "ESP32 上电就崩溃" → 调用 `esp32-debug`
