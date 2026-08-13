# Eval: DAppletData 数据模型

## 任务

用户需要理解 DAppletData 和 DPluginMetaData 的区别。

解释两个数据类的作用和使用场景。

## 期望输出

回答应：
1. 说明 DPluginMetaData 是静态元数据
2. 说明 DAppletData 是运行时实例数据
3. 展示从 metadata 构建 appletData
4. 说明 groupList 的用途

## 验证要点

- [ ] DPluginMetaData 来自 metadata.json
- [ ] DAppletData 描述实例配置
- [ ] DAppletData::fromPluginMetaData() 转换方法
- [ ] groupList 用于 Containment 管理子插件
- [ ] setAppletData() / appletData() 的读写方式
