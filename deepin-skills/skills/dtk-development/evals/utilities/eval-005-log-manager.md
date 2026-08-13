# Eval: 日志管理

## 任务

配置应用日志系统：
1. 注册控制台输出
2. 注册文件输出
3. 在实际使用日志的源文件声明 category

## 验证要点

- [ ] #include <DLog>
- [ ] registerConsoleAppender()
- [ ] registerFileAppender()
- [ ] 使用 `DLogManager::registerConsoleAppender()` 和 `DLogManager::registerFileAppender()`
- [ ] 未设置固定日志路径或日志格式
- [ ] 使用处包含 `Q_LOGGING_CATEGORY`
