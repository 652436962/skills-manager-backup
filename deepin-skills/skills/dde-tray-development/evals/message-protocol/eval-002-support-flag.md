# Eval: 插件可用性通知

## 任务

用户的插件可能在某些情况下不可用，需要通知任务栏。

指导用户使用 MSG_GET_SUPPORT_FLAG 和 MSG_SUPPORT_FLAG_CHANGED。

## 期望输出

回答应：
1. 展示 message() 处理 MSG_GET_SUPPORT_FLAG
2. 展示主动发送 MSG_SUPPORT_FLAG_CHANGED
3. 说明返回格式
4. 说明触发时机

## 验证要点

- [ ] message() 处理 "getSupportFlag"
- [ ] 返回 { "supportFlag": true/false }
- [ ] 状态变化时通过回调发送 "supportFlagChanged"
- [ ] 说明使用场景（如蓝牙未开启时）
