# Eval: 插件激活状态

## 任务

用户的插件需要报告自身是否处于激活状态（如蓝牙已连接）。

指导用户使用 MSG_ITEM_ACTIVE_STATE。

## 期望输出

回答应：
1. 展示发送激活状态消息
2. 说明 true/false 含义
3. 展示状态变化时发送
4. 说明用途

## 验证要点

- [ ] msgType: "itemActiveState"
- [ ] data: { "itemActiveState": true/false }
- [ ] 通过 m_messageCallback 发送
- [ ] true 表示激活状态（如蓝牙已连接）
