# Eval: 窗口模糊效果

## 任务

为窗口启用模糊背景效果：
1. 启用窗口背景模糊
2. 设置半透明背景
3. 设置模糊区域

## 期望输出

代码应：
1. 设置 enableBlurWindow 属性
2. 设置 translucentBackground 属性
3. 正确处理模糊区域

## 验证要点

- [ ] handle->setEnableBlurWindow(true)
- [ ] handle->setTranslucentBackground(true)
- [ ] 了解模糊效果的平台差异（X11/Wayland）
