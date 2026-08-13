# 主题系统

## 触发关键词

本文档适用于以下任务场景：

**自然语言描述：**
- 图标使用/主题切换/调色板
- 主题图标（通过 `DIconTheme::findQIcon()` 统一查找 DCI、builtin 和 XDG 图标）
- 字体大小/亮暗主题
- 控件颜色/语义化颜色

**API 接口描述：**
- DDciIcon / DPalette / DGuiApplicationHelper
- DFontManager / DFontSizeManager
- DIconTheme / DStyleHelper

---

## 概述

DTK 主题系统涵盖视觉表现的各个方面：

- **图标**：优先通过 `DIconTheme::findQIcon()` 使用 DCI、builtin 或 XDG 主题图标；需要直接播放 DCI 动画时再使用 `DDciIcon`
- **调色板**：`DPalette` 语义化颜色、`DGuiApplicationHelper` 亮暗主题切换
- **字体**：`DFontManager` T1-T11 层级字体体系
- **控件风格**：`DStyle` / `DStyleHelper` 控件渲染与状态颜色

## 快速路由

| 场景 | 参考文档 |
|------|----------|
| dci 图标完整规范 | [dci.md](dci.md) |
| builtin 图标列表与用法 | [builtin.md](builtin.md) |
| icon theme 图标（XDG） | [icontheme.md](icontheme.md) |
| 调色板（DPalette） | [palette.md](palette.md) |
| 控件风格 API 与定制 | [Widget 控件风格](../widgets/style.md) |
| Chameleon 风格概览 | [chameleon-style.md](chameleon-style.md) |
| 监听亮暗主题切换 | [theme-switch.md](theme-switch.md) |

## 相关文档

- [../widgets/style.md](../widgets/style.md) — 控件风格规范
- [../widgets/palette-helper.md](../widgets/palette-helper.md) — 调色板助手
