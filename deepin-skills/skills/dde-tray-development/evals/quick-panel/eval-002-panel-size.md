# Eval: 快捷面板控件尺寸

## 任务

用户的快捷面板控件显示不正常，可能尺寸设置有误。

指导用户正确设置快捷面板控件尺寸。

## 期望输出

回答应：
1. 说明只设置 setFixedHeight 不设置 setFixedSize
2. 展示各布局对应的宽度
3. 说明图标尺寸
4. 解释宽度由框架自动设置

## 验证要点

- [ ] 只用 setFixedHeight(Dock::QUICK_ITEM_HEIGHT)
- [ ] 不要使用 setFixedSize() 锁定宽度
- [ ] Quick_Panel_Single: 70x60
- [ ] Quick_Panel_Multi: 150x60
- [ ] Quick_Panel_Full: 310x60
- [ ] 图标尺寸: 24x24 (Dock::QUICK_PANEL_ICON_SIZE)
