# 列表项委托

## 任务

实现自定义列表项的外观效果，要求：
1. 列表项有圆角背景
2. 某些项使用特殊背景色（如警告状态）
3. 某些项的文字使用特殊颜色（如警告文本）
4. 列表项右侧添加操作按钮（如编辑、删除图标）
5. 列表项中嵌入自定义控件（如开关按钮）

## 验证要点

- [ ] 使用 DTK 提供的属性接口完成自定义，而非重写 paint()
- [ ] 背景色、文字颜色、操作按钮均通过 DStandardItem/DViewItemAction 设置
- [ ] 自定义控件通过 DViewItemAction::setWidget() 嵌入

## 参考

参见 [列表项委托](../../references/widgets/item-delegate.md) 了解：
- DStandardItem 属性设置方法
- DViewItemAction 操作按钮添加方法
- 列表项自定义绘制与属性接口的选择
