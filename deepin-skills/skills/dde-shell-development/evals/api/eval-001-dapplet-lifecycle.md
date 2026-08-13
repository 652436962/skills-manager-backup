# Eval: DApplet 生命周期

## 任务

用户想了解 DApplet 插件的生命周期，以便正确初始化资源。

解释 DApplet 的生命周期和各阶段的作用。

## 期望输出

回答应：
1. 说明生命周期顺序：构造 → load() → init() → rootObjectChanged
2. 解释各阶段的职责
3. 说明 rootObjectChanged 信号的触发时机
4. 给出资源初始化的最佳实践

## 验证要点

- [ ] 说明构造函数中不应做复杂初始化
- [ ] load() 用于加载配置和数据
- [ ] init() 用于初始化 QML 和连接信号
- [ ] rootObjectChanged 表示 QML 根对象已创建
- [ ] 说明 DApplet::init() 需要调用父类实现
