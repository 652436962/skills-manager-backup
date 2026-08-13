# Eval: 实现右键菜单

## 任务

用户需要为托盘插件添加右键菜单。

指导用户实现 itemContextMenu 和 invokedMenuItem。

## 期望输出

回答应：
1. 展示 itemContextMenu 返回 JSON
2. 展示菜单项字段（itemId、itemText、isCheckable）
3. 展示 invokedMenuItem 处理点击
4. 说明预定义菜单项 ID

## 验证要点

- [ ] itemContextMenu 返回 { "items": [...] }
- [ ] 菜单项包含 itemId、itemText、isCheckable、isActive、checked
- [ ] invokedMenuItem(menuId, checked) 处理点击
- [ ] 不要使用保留 ID: dock-item-id、undock-item-id
