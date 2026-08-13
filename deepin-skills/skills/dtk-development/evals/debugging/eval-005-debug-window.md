# Eval: 调试窗口效果问题

## 任务

调试窗口模糊效果不显示的问题：
1. 检查平台支持
2. 检查窗口属性设置
3. 检查合成器状态

## 验证要点

- [ ] 确认 DGuiApplicationHelper::isXWindowPlatform()
- [ ] 检查 DPlatformHandle 设置
- [ ] 验证合成器（compositor）是否启用
