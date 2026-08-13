# 自定义控件风格

## 任务

为自定义控件实现主题感知，要求：
1. 控件背景随主题变化
2. 背景色使用语义化颜色（如项背景色）
3. 支持 hover 和 pressed 状态视觉反馈

## 验证要点

- [ ] 继承 QWidget 并实现 paintEvent
- [ ] 使用 style()->drawPrimitive() 绘制背景
- [ ] 使用 DStyle::PE_ItemBackground 图元
- [ ] 使用 DPaletteHelper 获取主题感知颜色

## 参考

参见 [样式系统](../../references/widgets/style.md) 了解自定义绘制的正确方式。
