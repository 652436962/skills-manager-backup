# Eval: 创建浮动覆盖层

## 任务

用户需要创建一个不占排除区域的浮动覆盖窗口（如通知弹窗）。

指导用户配置 DLayerShellWindow 创建浮动覆盖层。

## 期望输出

回答应：
1. 展示不设置 exclusionZone
2. 展示 LayerOverlay 层级
3. 展示键盘交互模式设置
4. 说明与面板的区别

## 验证要点

- [ ] layer: LayerOverlay
- [ ] 不设置或 exclusionZone: 0
- [ ] keyboardInteractivity: KeyboardInteractivityOnDemand
- [ ] 说明浮动窗口不阻止其他窗口
