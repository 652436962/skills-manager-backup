# Eval: 实现消息处理

## 任务

用户需要在插件中处理任务栏发来的消息。

指导用户实现 message() 接口和 setMessageCallback。

## 期望输出

回答应：
1. 展示 setMessageCallback 保存回调
2. 展示 message() 解析 JSON
3. 展示返回 JSON 格式
4. 说明消息类型常量

## 验证要点

- [ ] setMessageCallback(cb) 保存回调函数
- [ ] message() 解析 msgType 和 data 字段
- [ ] 使用 QJsonDocument 解析和构建
- [ ] 返回格式包含 msgType 和 data
- [ ] 说明 MessageCallbackFunc 是 C 函数指针
