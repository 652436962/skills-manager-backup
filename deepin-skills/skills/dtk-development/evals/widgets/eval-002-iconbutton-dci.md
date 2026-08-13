# Eval: 图标按钮使用 DCI 图标

## 任务

创建一个图标按钮，要求：
1. 按 DCI 规范组织动态资源
2. 通过图标名称查找图标，不拼接资源路径
3. 点击时输出日志

## 期望输出

代码应：
1. 创建图标按钮
2. 使用 DCI 图标格式设置图标
3. 连接点击信号

## 验证要点

- [ ] #include <DIconButton>
- [ ] #include <DDciIcon>
- [ ] 使用 `DIconTheme::findQIcon("action")` 按名称查找图标
- [ ] 常规场景未调用 `setDciThemeSearchPaths()`；如确需自定义搜索根目录，说明调用原因和影响范围
- [ ] button->setIcon(icon)

## 参考

参见 [按钮控件](../../references/widgets/button.md) 了解 DIconButton 和 DCI 图标的用法。
