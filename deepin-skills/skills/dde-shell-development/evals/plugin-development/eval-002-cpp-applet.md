# Eval: 创建带 C++ 后端的 Applet

## 任务

用户想创建一个天气插件，需要从网络获取天气数据并在 QML 中显示。

指导用户创建带 C++ 后端的 Applet 插件。

## 期望输出

回答应：
1. 展示 C++ 头文件和实现文件
2. 展示 D_APPLET_CLASS 宏及紧随其后的实现文件 moc include
3. 展示 load() 和 init() 的实现
4. 展示 Q_PROPERTY 暴露给 QML

## 验证要点

- [ ] 类继承 DApplet 并使用 Q_OBJECT 宏
- [ ] 使用 Q_PROPERTY 暴露属性给 QML
- [ ] 正确实现 load() 和 init() 虚函数
- [ ] 包含 `<pluginfactory.h>`，使用 `D_APPLET_CLASS(ClassName)` 注册插件
- [ ] 注册宏后包含与实现文件同名的 moc 文件（如 `#include "weatherapplet.moc"`）
- [ ] CMakeLists.txt 链接 Dde::Shell
