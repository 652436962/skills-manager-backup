# DDesktopServices 桌面服务

## 1. 概述与适用场景

`DDesktopServices`（dtkgui）提供桌面环境集成功能。包括文件管理器操作、系统音效播放等。

> 注意：dtkwidget 中也有同名类但已废弃，请使用 `Dtk::Gui::DDesktopServices`。

**适用场景：**
- 在文件管理器中显示文件/文件夹
- 播放系统音效
- 移动文件到回收站
- 显示文件属性对话框

## 2. SystemSoundEffect 枚举

| 值 | 名称 | 说明 |
|----|------|------|
| 1 | `SSE_Notifications` | 通知音效 |
| 2 | `SEE_Screenshot` | 截图音效（⚠️ 源码拼写错误，应为 SSE_） |
| 3 | `SSE_EmptyTrash` | 清空回收站 |
| 4 | `SSE_SendFileComplete` | 发送文件完成 |
| 5 | `SSE_BootUp` | 开机 |
| 6 | `SSE_Shutdown` | 关机 |
| 7 | `SSE_Logout` | 注销 |
| 8 | `SSE_WakeUp` | 唤醒 |
| 9 | `SSE_VolumeChange` | 音量变化 |
| 10 | `SSE_LowBattery` | 低电量 |
| 11 | `SSE_PlugIn` | 设备插入 |
| 12 | `SSE_PlugOut` | 设备拔出 |
| 13 | `SSE_DeviceAdded` | 设备添加 |
| 14 | `SSE_DeviceRemoved` | 设备移除 |
| 15 | `SSE_Error` | 错误 |

> ⚠️ `SEE_Screenshot` 是源码中的已知拼写错误，前缀应为 `SSE_`。

## 3. 文件管理器操作

### 3.1 显示文件夹

```cpp
#include <DDesktopServices>

// 显示单个文件夹
DDesktopServices::showFolder("/home/user/Documents");

// 显示多个文件夹
DDesktopServices::showFolders({"/home/user/Doc1", "/home/user/Doc2"});

// 使用 URL
DDesktopServices::showFolder(QUrl("file:///home/user/Documents"));
```

### 3.2 显示文件

```cpp
// 在文件管理器中选中文件
DDesktopServices::showFileItem("/home/user/file.txt");

// 选中多个文件
DDesktopServices::showFileItems({"/home/user/f1.txt", "/home/user/f2.txt"});
```

### 3.3 显示属性

```cpp
// 显示文件属性对话框
DDesktopServices::showFileItemProperty("/home/user/file.txt");

// 多文件属性
DDesktopServices::showFileItemProperties({"/home/user/f1", "/home/user/f2"});
```

### 3.4 移到回收站

```cpp
DDesktopServices::trash("/home/user/unwanted.txt");
DDesktopServices::trash(QUrl("file:///home/user/unwanted.txt"));
```

## 4. 系统音效

```cpp
#include <DDesktopServices>

// 播放系统音效
DDesktopServices::playSystemSoundEffect(DDesktopServices::SSE_Notifications);
DDesktopServices::playSystemSoundEffect(DDesktopServices::SSE_Error);

// 按名称播放
DDesktopServices::playSystemSoundEffect("message");

// 预览音效
DDesktopServices::previewSystemSoundEffect(DDesktopServices::SSE_Notifications);

// 获取音效名称
QString name = DDesktopServices::getNameByEffectType(DDesktopServices::SSE_Notifications);
```

## 5. 错误处理

```cpp
if (!DDesktopServices::showFolder(path)) {
    QString error = DDesktopServices::errorMessage();
    qWarning() << "Failed to show folder:" << error;
}
```

## 6. 常见错误与避坑

### 错误 1：使用 dtkwidget 的废弃版本

```cpp
// ❌ 错误：dtkwidget 版本已废弃
#include <DDesktopServices>  // dtkwidget
DDesktopServices::showFolder(path);

// ✅ 正确：使用 dtkgui 版本
#include <DDesktopServices>  // dtkgui
DDesktopServices::showFolder(path);
```

### 错误 2：使用 SEE_Screenshot 拼写错误枚举

```cpp
// ⚠️ 源码拼写错误，但必须这样用
DDesktopServices::playSystemSoundEffect(DDesktopServices::SEE_Screenshot);
// 注意：前缀是 SEE_ 不是 SSE_
```

## 7. 相关文档

- [sysinfo.md](sysinfo.md) - 系统信息
- [gui-helper.md](gui-helper.md) - DGuiApplicationHelper
