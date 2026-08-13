# Eval: 使用 PluginProxyInterface

## 任务

用户需要在插件中主动通知任务栏刷新控件。

指导用户使用 m_proxyInter 与任务栏交互。

## 期望输出

回答应：
1. 展示 itemAdded 添加控件
2. 展示 itemUpdate 刷新控件
3. 展示 itemRemoved 移除控件
4. 展示 saveValue/getValue 保存配置

## 验证要点

- [ ] init() 中保存 proxyInter 到 m_proxyInter
- [ ] itemAdded(this, itemKey) 添加控件
- [ ] itemUpdate(this, itemKey) 通知刷新
- [ ] itemRemoved(this, itemKey) 移除控件
- [ ] saveValue(this, key, value) 保存配置
- [ ] getValue(this, key, fallback) 读取配置
