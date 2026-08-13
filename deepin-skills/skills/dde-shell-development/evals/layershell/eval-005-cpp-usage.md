# Eval: C++ 中使用 LayerShell

## 任务

用户需要在 C++ 代码中使用 LayerShell（不使用 QML）。

指导用户通过 DLayerShellWindow::get() 操作 QWindow。

## 期望输出

回答应：
1. 展示 DLayerShellWindow::get() 获取 shell 对象
2. 展示 setAnchors、setLayer、setExclusiveZone
3. 说明需要先显示窗口
4. 展示完整 C++ 示例

## 验证要点

- [ ] DLayerShellWindow::get(window) 获取 shell 对象
- [ ] window->setVisible(true) 先显示窗口
- [ ] shell->setAnchors() 设置锚定
- [ ] shell->setLayer() 设置层级
- [ ] 链接 Dde::Shell 库
