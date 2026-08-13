# Eval: 调试风格问题

## 任务

调试控件样式不正确的问题：
1. 检查当前使用的 QStyle
2. 确认 Chameleon 风格已加载
3. 检查样式绘制

## 验证要点

- [ ] 使用 widget->style()->objectName() 检查风格名
- [ ] 确认风格为 "chameleon"
- [ ] 使用 QT_DEBUG_PLUGINS=1 排查插件加载
