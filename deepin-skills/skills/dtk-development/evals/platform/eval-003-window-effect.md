# Eval: 窗口动效设置

## 任务

为窗口设置平台特效（如圆角、模糊）：
1. 禁用启动动效
2. 禁用关闭动效
3. 设置启动动效为从鼠标位置展开

## 期望输出

代码应：
1. 使用 EffectScene 枚举禁用动效
2. 使用 EffectType 枚举设置动效类型

## 验证要点

- [ ] handle->setEffectScene(DPlatformHandle::EffectNoStart)
- [ ] handle->setEffectScene(DPlatformHandle::EffectNoClose)
- [ ] handle->setEffectType(DPlatformHandle::EffectCursor)
- [ ] 了解 EffectScene 和 EffectType 枚举值
