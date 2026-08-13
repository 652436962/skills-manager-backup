# 字体大小层级

## 任务

使用系统字体大小层级，要求：
1. 获取指定层级的字体大小
2. 应用到标签控件
3. 监听系统字体变化并更新

## 验证要点

- [ ] #include <DFontSizeManager>
- [ ] DFontSizeManager::instance()->t4() 获取字体
- [ ] 或 bind(widget, SizeType) 绑定字体
- [ ] 连接 fontChanged 信号监听变化
