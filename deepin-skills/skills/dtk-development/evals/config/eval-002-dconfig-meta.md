# DConfig meta 文件

## 任务

为应用配置编写元数据文件，要求：
1. 应用标识为 "com.example.app"
2. 包含一个字符串配置项（用户名）
3. 包含一个布尔配置项（是否启用）

## 验证要点

- [ ] JSON 格式正确
- [ ] version 字段为 1.0
- [ ] contents 对象包含配置项定义
- [ ] 每个配置项有 key、value、visibility 等字段
