# Eval: 插件不显示问题排查

## 任务

用户开发的插件编译安装成功，但在控制中心中不显示。帮助用户排查问题。

## 期望输出

回答应：
1. 列出常见原因（DConfig hideModule、QML visible、DBus 条件）
2. 给出检查 DConfig 的命令
3. 提供完整的检查清单

## 验证要点

- [ ] 提到检查 `hideModule` DConfig 配置
- [ ] 提到检查 `{Name}.qml` 中 `visible` 属性
- [ ] 提到检查 DBus 条件是否满足
- [ ] 提到检查插件目录结构
