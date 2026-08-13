# 控件颜色跟随主题切换

## 任务

创建一个自定义标签，要求：
1. 背景色使用项背景色语义
2. 文字颜色使用标题文字颜色语义
3. 当系统主题切换时自动更新颜色

## 验证要点

- [ ] 使用 #include <DPalette> 和 #include <DGuiApplicationHelper>
- [ ] 连接 themeTypeChanged 信号监听主题变化
- [ ] 使用 DPalette::ItemBackground 获取背景色
- [ ] 使用 DPalette::TextTitle 获取文字颜色
