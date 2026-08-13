# Eval: 创建基础托盘插件

## 任务

用户想创建一个简单的托盘插件，在托盘区显示一个图标。

指导用户实现 PluginsItemInterfaceV2 接口。

## 期望输出

回答应：
1. 展示类声明和 Q_INTERFACES 宏
2. 展示必须实现的接口（pluginName、init、itemWidget）
3. 展示 flags() 返回正确的类型标志
4. 说明 IID 使用

## 验证要点

- [ ] 继承 QObject 和 PluginsItemInterfaceV2
- [ ] Q_INTERFACES(PluginsItemInterfaceV2)
- [ ] pluginName() 返回唯一标识
- [ ] init() 保存 proxyInter
- [ ] flags() 至少返回 Type_Tray，不强制添加与任务无关的属性标志
- [ ] IID 使用 "com.deepin.dock.PluginsItemInterface_V2"
