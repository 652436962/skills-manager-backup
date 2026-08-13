# Eval: 调色板系统架构

## 任务

理解 DTK 调色板系统的架构：
1. 说明 DPalette 如何扩展 QPalette
2. 解释 DGuiApplicationHelper 在主题管理中的作用
3. 说明 DStyleHelper 如何实现控件状态颜色

## 期望输出

回答应：
1. 描述调色板数据流
2. 说明主题切换的响应机制
3. 解释状态颜色（hover/press/disabled）的选择逻辑

## 验证要点

- [ ] DPalette 扩展 QPalette，增加语义颜色
- [ ] DGuiApplicationHelper 提供主题切换信号
- [ ] DStyleHelper 根据控件状态选择调色板颜色
- [ ] 数据流：系统主题 → DGuiApplicationHelper → DPalette → DStyleHelper → 控件
