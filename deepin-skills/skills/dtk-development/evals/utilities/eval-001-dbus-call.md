# Eval: DBus 通信

## 任务

调用 DBus 方法实现进程间通信，要求：
1. 服务名 "com.deepin.SessionManager"
2. 路径 "/com/deepin/SessionManager"
3. 接口 "com.deepin.SessionManager"
4. 调用方法 "Logout"

## 期望输出

代码应：
1. 创建 DDBusSender
2. 设置服务、路径、接口
3. 调用方法

## 验证要点

- [ ] #include <DDBusSender>
- [ ] DDBusSender()
- [ ] .service("com.deepin.SessionManager")
- [ ] .path("/com/deepin/SessionManager")
- [ ] .interface("com.deepin.SessionManager")
- [ ] .call("Logout")
