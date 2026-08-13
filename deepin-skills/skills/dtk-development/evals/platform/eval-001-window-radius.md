# Eval: 窗口圆角设置

## 任务

为窗口设置圆角效果：
1. 为 QWindow 设置 10px 圆角
2. 同时设置边框宽度和颜色
3. 确保在 X11 和 Wayland 上都能工作

## 期望输出

代码应：
1. 创建 DPlatformHandle 实例
2. 设置 windowRadius 属性
3. 设置 borderWidth 和 borderColor

## 验证要点

- [ ] #include <DPlatformHandle>
- [ ] new DPlatformHandle(window, window)
- [ ] handle->setWindowRadius(10)
- [ ] handle->setBorderWidth(1)
- [ ] handle->setBorderColor(QColor(0, 0, 0, 50))
