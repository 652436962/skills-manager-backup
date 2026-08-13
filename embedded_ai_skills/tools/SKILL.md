---
name: "tools"
description: "嵌入式开发辅助工具 skill 集合入口。索引串口调试工具与 EDA 工具 skill。当用户需要进行串口监视、AT 命令测试、固件验证，或使用 EasyEDA 进行原理图/PCB 设计时调用。"
---

# 工具类 Skill

嵌入式开发辅助工具集合。

## 子 Skill 索引

| Skill | 文件 | 功能 |
|-------|------|------|
| **easyeda-api** | [SKILL.md](easyeda-api/SKILL.md) | EasyEDA Pro API：原理图/PCB 设计、扩展开发 |
| **emberinter** | [SKILL.md](emberinter/SKILL.md) | EmberInterDebugTool 串口调试、AT 命令测试 |

## 使用方式

- "用 EasyEDA 画原理图 / PCB 布局" → 调用 `easyeda-api`
- "串口监视 / AT 命令测试 / 固件验证" → 调用 `emberinter`
