# Eval: 单实例应用

## 任务

实现单实例应用程序：
1. 设置与可执行文件一致的 applicationName
2. 检查是否已有实例运行
3. 第二个进程退出，原窗口从隐藏或最小化状态恢复并激活
4. 将第二个进程的文件或命令行参数交给原进程处理

## 验证要点

- [ ] `DApplication::setApplicationName()` 与可执行文件名一致
- [ ] `DApplication::setSingleInstance("唯一应用 ID")`
- [ ] `newInstanceStarted` 或等价新实例信号
- [ ] `showNormal()`/`show()`、`raise()`、`activateWindow()`
- [ ] 新实例参数未被丢弃
