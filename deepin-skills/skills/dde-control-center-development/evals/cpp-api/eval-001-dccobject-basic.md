# DccObject 基本用法

## 任务

在控制中心创建一个功能模块，要求：
1. 模块有内部名称和显示名称
2. 模块有图标
3. 模块添加到指定父模块下

## 验证要点

- [ ] #include <DccObject>
- [ ] setName() 设置模块名
- [ ] setDisplayName() 设置显示名
- [ ] 父模块调用 addChild() 添加子模块
