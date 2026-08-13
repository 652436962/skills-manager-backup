# Eval: 配置插件 flags

## 任务

用户想创建一个可以在控制中心设置显隐的托盘插件。

指导用户正确配置 PluginFlags。

## 期望输出

回答应：
1. 列出 Type 标志及其含义
2. 列出 Attribute 标志及其含义
3. 展示 Type_Tray 与 Attribute_CanSetting 组合
4. 说明 icon() 方法的实现要求

## 验证要点

- [ ] Type_Tray (0x10) 用于托盘区
- [ ] Attribute_CanSetting (0x800) 允许控制中心显隐
- [ ] 设置 Attribute_CanSetting 时必须实现 icon()
- [ ] icon() 需要处理亮色/暗色主题
- [ ] 图标需安装到 share/dde-dock/icons/dcc-setting/
