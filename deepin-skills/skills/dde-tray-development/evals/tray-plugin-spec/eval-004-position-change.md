# Eval: 处理任务栏位置变化

## 任务

用户的托盘图标需要根据任务栏位置调整显示方向。

指导用户实现 positionChanged 接口。

## 期望输出

回答应：
1. 展示 positionChanged 接口实现
2. 展示 Dock::Position 枚举值
3. 展示根据位置更新控件
4. 说明刷新控件的时机

## 验证要点

- [ ] 覆写 positionChanged(const Dock::Position)
- [ ] Position::Top/Right/Bottom/Left 枚举值
- [ ] 更新控件显示后调用 itemUpdate
- [ ] 说明位置变化时的刷新流程
