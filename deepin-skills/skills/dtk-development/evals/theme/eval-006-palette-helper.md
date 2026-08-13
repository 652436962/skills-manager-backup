# 控件调色板助手

## 任务

为控件设置自定义颜色，要求：
1. 设置按钮背景色为指定颜色
2. 设置按钮文字颜色
3. 确保主题切换时颜色仍然正确

## 验证要点

- [ ] #include <DPaletteHelper>
- [ ] DPaletteHelper::instance()->palette(widget) 获取调色板
- [ ] palette.setColor() 设置颜色
- [ ] DPaletteHelper::instance()->setPalette(widget, palette) 应用调色板

## 参考

参见 [调色板助手](../../references/widgets/palette-helper.md) 了解 DPaletteHelper 的用法。
