# Eval: 主窗口与标题栏

## 任务

创建一个主窗口，要求：
1. 窗口最小尺寸 800x600
2. 标题栏显示 "我的应用"
3. 标题栏包含菜单按钮

## 期望输出

代码应：
1. 使用 DTK 主窗口类
2. 通过标题栏接口设置标题和菜单
3. 正确配置窗口属性

## 验证要点

- [ ] #include <DMainWindow>
- [ ] #include <DTitlebar>
- [ ] titlebar()->setTitle("我的应用")
- [ ] titlebar()->setMenu(menu)

## 参考

参见 [窗口与标题栏](../../references/widgets/view.md) 了解主窗口和标题栏的使用。
