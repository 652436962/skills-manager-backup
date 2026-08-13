# Eval: 创建 Panel 面板插件

## 任务

用户想创建一个 Dock 面板插件，需要在屏幕底部显示。

指导用户创建 Panel 插件并配置 LayerShell 窗口。

## 期望输出

回答应：
1. 展示 DPanel 继承类实现
2. 展示 QML Window 配置 DLayerShellWindow
3. 展示 anchors 和 layer 设置
4. 说明 Panel 与 Containment 的区别

## 验证要点

- [ ] 类继承 DPanel
- [ ] QML 中使用 Window 并设置 DLayerShellWindow 附加属性
- [ ] 设置正确的 anchors（如 AnchorBottom | AnchorLeft | AnchorRight）
- [ ] 设置 layer 为 LayerTop
- [ ] 说明 Panel 有 window()、popupWindow() 等窗口管理接口
