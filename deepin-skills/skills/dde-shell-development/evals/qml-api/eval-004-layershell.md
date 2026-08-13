# Eval: LayerShell 窗口

## 任务

用户需要在 Wayland 上创建锚定屏幕边缘的窗口。

指导用户使用 LayerShell 附加属性实现窗口锚定。

## 期望输出

回答应：
1. 展示锚定边设置方式
2. 展示层级设置
3. 展示排除区域设置
4. 说明键盘交互模式

## 验证要点

- [ ] DLayerShellWindow.anchors 设置锚定边
- [ ] DLayerShellWindow.layer 设置层级
- [ ] DLayerShellWindow.exclusionZone 设置排除区域
- [ ] DLayerShellWindow.keyboardInteractivity 设置键盘交互
- [ ] 说明 Anchor 枚举值可位或组合

## 参考

参见 [LayerShell 窗口](../../references/layershell.md) 了解 Wayland 窗口锚定的实现。
