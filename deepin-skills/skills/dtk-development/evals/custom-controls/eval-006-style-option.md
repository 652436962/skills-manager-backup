# 使用 StyleOption

## 任务

在自定义绘制中正确使用 StyleOption，要求：
1. 初始化样式选项对象
2. 设置控件状态（hover、pressed、enabled 等）
3. 传递给样式系统进行绘制

## 验证要点

- [ ] 使用 initFrom() 初始化 QStyleOption
- [ ] 设置 state 的 hover/pressed 等标志
- [ ] 使用正确的 QStyle::ControlElement 或 PrimitiveElement
