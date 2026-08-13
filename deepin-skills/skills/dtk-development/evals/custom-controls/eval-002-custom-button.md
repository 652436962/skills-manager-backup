# 自定义按钮

## 任务

创建一个自定义按钮控件，要求：
1. 按钮外观随主题变化
2. hover 时有高亮效果
3. pressed 时有按下效果
4. 支持键盘焦点

## 验证要点

- [ ] 继承 QAbstractButton
- [ ] 重写 paintEvent 使用 style()->drawControl()
- [ ] 处理 QStyle::State_MouseOver 状态
- [ ] 处理 QStyle::State_Sunken 状态

## 参考

参见 [按钮规范](../../references/widgets/button.md) 了解 DTK 按钮的正确实现方式。
