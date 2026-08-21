# Embedded Skills Hub / 嵌入式开发技能集

[中文版](#chinese) | [English Version](#english)

---

<a id="chinese"></a>
## 中文版

###  这是什么？

这是一个收集和分享 **嵌入式开发 AI 技能（Skill）** 的开源仓库。

每个 Skill 是一个 Markdown 文件，被 AI 编程助手（如 Trae、Cursor、Copilot 等）加载后，能够引导 AI 正确完成嵌入式开发任务——从环境搭建、项目创建、编译、烧录到调试，全链路覆盖。

###  目标

嵌入式开发环境搭建繁琐，不同芯片、不同开发板、不同工具链之间的差异巨大。我们希望通过社区共建的方式，沉淀出一套可靠的 AI 可执行知识库，让任何开发者都能**用一句话开始嵌入式开发**。

###  当前 Skills

| Skill | 描述 | 适用场景 |
|--------|------|----------|
| [stm32_dev](./stm32-dev/SKILL.md) | STM32 纯 CLI 开发指南 | STM32 ARM Cortex-M 系列芯片开发，无需 CubeMX / CubeIDE GUI |

###  如何使用

1. 将 SKILL.md 文件放入 AI 编程助手的 Skills 目录（如 Trae 的 `~/.trae-cn/skills/`）
2. 在对话中提及相关话题，AI 会自动加载 Skill
3. 或手动 `@skill-name` 调用

###  贡献

欢迎贡献新的 Skill 或改进现有 Skill：

- **添加新 Skill**：创建 `芯片或工具名/SKILL.md`，遵循现有格式
- **改进现有 Skill**：提交 PR，说明你遇到的硬件问题和解决方案
- **特别欢迎**：不同芯片系列（ESP32、nRF52、GD32 等）、不同 RTOS（FreeRTOS、RT-Thread、Zephyr）、不同调试器的实战经验

###  Skill 编写原则

- **经验 ≠ 标准 SOP**：每个 Skill 中的步骤均标注为特定硬件的参考经验，AI 必须先确认用户硬件配置
- **跨平台**：标注 Windows/macOS/Linux 的差异点
- **可验证**：关键步骤附带预期输出的样例
- **完整链路**：覆盖从环境搭建到程序运行的闭环

###  协议

MIT License

---

<a id="english"></a>
## English Version

###  What is This?

An open-source repository collecting and sharing **AI Skills for embedded development**.

Each Skill is a Markdown file that, when loaded by AI coding assistants (Trae, Cursor, Copilot, etc.), guides the AI to correctly perform embedded development tasks — from environment setup, project creation, compilation, flashing, to debugging, covering the full workflow.

###  Goal

Embedded development environment setup is notoriously tedious, with huge variations across different chips, boards, and toolchains. We aim to build a reliable AI-executable knowledge base through community collaboration, so that any developer can **start embedded development with a single prompt**.

###  Current Skills

| Skill | Description | Use Case |
|--------|-------------|----------|
| [stm32_dev](./stm32-dev/SKILL.md) | STM32 Pure CLI Development Guide | STM32 ARM Cortex-M series, no CubeMX / CubeIDE GUI needed |

###  How to Use

1. Copy the SKILL.md file into your AI assistant's Skills directory (e.g., `~/.trae-cn/skills/` for Trae)
2. The AI auto-loads the Skill when related topics come up in conversation
3. Or manually invoke with `@skill-name`

###  Contributing

Contributions of new Skills or improvements to existing ones are welcome:

- **Add a new Skill**: Create `chip-or-tool-name/SKILL.md`, following the existing format
- **Improve existing Skills**: Submit a PR describing your hardware scenario and solution
- **Especially welcome**: Real-world experience with different MCU families (ESP32, nRF52, GD32, etc.), different RTOS (FreeRTOS, RT-Thread, Zephyr), and different debug probes

###  Skill Design Principles

- **Experience ≠ Standard SOP**: Every step in a Skill is annotated as reference experience from specific hardware. The AI must confirm the user's hardware configuration first.
- **Cross-platform**: Windows/macOS/Linux differences are clearly marked
- **Verifiable**: Key steps include expected output samples
- **End-to-end**: Covers the full loop from environment setup to running code

###  License

MIT License
