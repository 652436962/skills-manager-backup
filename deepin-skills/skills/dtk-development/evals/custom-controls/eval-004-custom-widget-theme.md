# 自定义控件主题感知

## 任务

创建一个主题感知的自定义控件，要求：
1. 系统主题切换时自动更新颜色
2. 使用语义化颜色（如文字颜色、背景颜色）
3. 支持自定义调色板扩展

## 验证要点

- [ ] 连接 DGuiApplicationHelper::themeTypeChanged 信号
- [ ] 使用 DPalette::ColorType 获取语义颜色
- [ ] 在 paintEvent 中使用 DStyleHelper 或 DPaletteHelper

## 参考

参见 [调色板规范](../../references/theme/palette.md) 了解主题感知的实现方式。
