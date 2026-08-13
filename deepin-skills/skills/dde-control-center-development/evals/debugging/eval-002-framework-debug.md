# Eval: 调试修改后的框架代码

## 任务

用户修改了 `libdde-control-center.so` 框架代码，需要调试修改后的效果。项目路径为 `~/dde-control-center`，构建目录为 `build`。

指导用户正确设置环境变量加载构建产物。

## 期望输出

回答应：
1. 列出需要设置的环境变量（LD_LIBRARY_PATH、QT_PLUGIN_PATH、QML2_IMPORT_PATH）
2. 给出完整的命令示例
3. 解释每个环境变量的作用

## 验证要点

- [ ] 提到 `export LD_LIBRARY_PATH=/path/to/build/lib:$LD_LIBRARY_PATH`
- [ ] 提到 `export QT_PLUGIN_PATH` 和 `QML2_IMPORT_PATH`
- [ ] 说明仍需通过系统 wrapper 启动
- [ ] 解释环境变量如何让进程加载构建产物而非系统版本
