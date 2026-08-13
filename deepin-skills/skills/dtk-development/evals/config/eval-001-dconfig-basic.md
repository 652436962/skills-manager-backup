# Eval: 使用 DConfig 存储配置

## 任务

使用配置系统存储应用设置，要求：
1. 使用应用默认 appId
2. 读取键值 "window-width"，默认值 800
3. 写入新值 1024

## 期望输出

代码应：
1. 创建 DConfig 对象
2. 使用 value() 读取配置
3. 使用 setValue() 写入配置

## 验证要点

- [ ] #include <DConfig>
- [ ] 优先使用 `DConfig` 构造函数和 `DSGApplication::id()` 默认 appId
- [ ] 使用 value(key, fallback) 读取
- [ ] 使用 setValue(key, value) 写入
- [ ] 只有默认 appId 无法满足需求时才使用 `DConfig::create(appId, ...)`
