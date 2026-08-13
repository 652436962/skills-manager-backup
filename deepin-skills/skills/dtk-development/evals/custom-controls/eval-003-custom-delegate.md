# 自定义列表委托

## 任务

实现列表项的自定义外观效果，要求：
1. 列表项有圆角背景
2. 选中时有高亮效果
3. hover 时有视觉反馈
4. 颜色随主题变化

## 验证要点

- [ ] 继承 DStyledItemDelegate
- [ ] 使用 DStyleHelper::getColor() 获取颜色
- [ ] 使用 DPaletteHelper 获取主题感知颜色
- [ ] 或使用 DStandardItem 属性接口而非重写 paint()

## 参考

参见 [列表项委托](../../references/widgets/item-delegate.md) 了解：
- DStyledItemDelegate 继承与自定义绘制
- DStandardItem 属性接口的使用方式
- 两种自定义方式的适用场景
