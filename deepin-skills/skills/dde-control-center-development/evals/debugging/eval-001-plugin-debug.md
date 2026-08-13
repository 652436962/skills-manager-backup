# Eval: 使用 --spec 参数调试插件

## 任务

用户开发了一个控制中心插件，修改后需要本地调试。项目路径为 `~/dde-control-center`，构建目录为 `build`。

指导用户使用 `--spec` 参数加载构建产物。

## 期望输出

回答应：
1. 说明关闭已有实例的必要性（单实例限制）
2. 给出正确的 `--spec` 参数路径示例
3. 解释安全加载机制（wrapper + security loader）

## 验证要点

- [ ] 提到 `killall dde-control-center`
- [ ] 提到 `--spec` 参数指定插件路径
- [ ] 说明使用系统 wrapper 启动而非直接运行构建产物
- [ ] 解释安全加载对 D-Bus 授权的必要性
