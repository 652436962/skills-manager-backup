# 内置图标

## 任务

使用系统内置图标，要求：
1. 查找一个常用图标（如"确定"图标）
2. 判断该图标是否为系统内置
3. 应用到按钮上

## 验证要点

- [ ] #include <DIconTheme>
- [ ] DIconTheme::findQIcon("dialog-ok") 查找图标
- [ ] DIconTheme::isBuiltinIcon() 判断是否内置
