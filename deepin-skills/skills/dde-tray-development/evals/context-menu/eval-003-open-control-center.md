# Eval: 菜单项打开控制中心

## 任务

用户需要在菜单中添加一个选项，点击后打开控制中心的指定模块。

指导用户使用 dde-am 打开应用。

## 期望输出

回答应：
1. 展示 invokedMenuItem 中处理菜单点击
2. 展示使用 dde-am 启动控制中心
3. 展示指定模块参数
4. 说明 Wayland 下的窗口激活

## 验证要点

- [ ] 使用 dde-am org.deepin.dde.control-center -- -p module
- [ ] 或在 itemCommand 中返回命令
- [ ] 说明 dde-am 处理 xdg-activation token
- [ ] 比直接执行命令的优势
