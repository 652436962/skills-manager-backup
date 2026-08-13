# Eval: 调试主题问题

## 任务

调试控件颜色不跟随主题切换的问题：
1. 检查当前主题类型
2. 检查控件调色板
3. 检查信号连接

## 验证要点

- [ ] 使用 DGuiApplicationHelper::instance()->themeType()
- [ ] 检查 DPaletteHelper::instance()->palette(widget)
- [ ] 验证 themeTypeChanged 信号是否连接
