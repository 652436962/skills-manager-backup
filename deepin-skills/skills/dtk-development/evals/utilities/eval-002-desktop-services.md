# Eval: 桌面服务

## 任务

打开 URL 和文件位置：
1. 在默认浏览器打开 URL
2. 在文件管理器中显示文件
3. 打开文件

## 验证要点

- [ ] #include <DDesktopServices>
- [ ] DDesktopServices::openUrl(QUrl("https://..."))
- [ ] DDesktopServices::showFile(filePath)
