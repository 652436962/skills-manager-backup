# 消息与提示控件规范

## 1. 概述与适用场景

| 控件 | 适用场景 | 位置 |
|------|----------|------|
| `DMessageManager` + `DFloatingMessage` | 窗口内消息提示 | 窗口顶部 |
| `DFloatingWidget` | 自定义浮动内容 | 窗口内任意 |
| `DToolTip` | 简短提示 | 鼠标附近 |

**不适用场景：**
- 模态确认 → 使用 `DDialog`
- 系统级通知 → 使用 `DNotifySender`

## 2. DMessageManager + DFloatingMessage

### 2.1 临时消息

```cpp
#include <DMessageManager>
#include <DFloatingMessage>

// 临时消息（自动消失）
DMessageManager::instance()->sendMessage(this, 
    QIcon(), "操作成功");
```

### 2.2 常驻消息

```cpp
#include <DMessageManager>
#include <DFloatingMessage>

auto *msg = new DFloatingMessage(DFloatingMessage::ResidentType, this);
msg->setMessage("正在同步数据...");
msg->setIcon(DIconTheme::findQIcon("icon_info"));

connect(msg, &DFloatingMessage::closeButtonClicked, []() {
    qInfo() << "User closed message";
});

DMessageManager::instance()->sendMessage(this, msg);
```

### 2.3 带 dci 图标的消息

```cpp
#include <DMessageManager>
#include <DFloatingMessage>
#include <DDciIcon>

DDciIcon icon = DDciIcon::fromTheme("status-info");
DMessageManager::instance()->sendMessage(this, icon, "同步完成");
```

## 3. DFloatingMessage 消息类型

| 类型 | 说明 | 自动关闭 |
|------|------|----------|
| `TransientType` | 临时消息 | ✅ 自动消失（约 3 秒） |
| `ResidentType` | 常驻消息 | ❌ 用户手动关闭 |

## 4. DToolTip 自定义提示

```cpp
#include <DToolTip>

// 设置提示文本格式
DToolTip::setToolTipTextFormat(Qt::PlainText);

// 获取当前格式
Qt::TextFormat format = DToolTip::toolTipTextFormat();
```

## 5. 关键 API

### DMessageManager

| 方法 | 说明 |
|------|------|
| `instance()` | 获取单例 |
| `sendMessage(widget, icon, text)` | 发送临时消息 |
| `sendMessage(widget, DFloatingMessage*)` | 发送自定义消息 |
| `setContentMargens(widget, margins)` | 设置消息显示区域边距 |

### DFloatingMessage

| 方法 | 说明 |
|------|------|
| `setIcon(QIcon)` | 设置图标 |
| `setIcon(DDciIcon)` | 设置 dci 图标 |
| `setMessage(QString)` | 设置消息文本 |
| `setWidget(QWidget*)` | 设置自定义控件 |
| `setDuration(int)` | 设置临时消息显示时长 |
| `messageType()` | 获取消息类型 |

## 6. 常见错误与避坑

### 错误 1：使用废弃的 DToast

```cpp
// ❌ 错误：DToast 已废弃
auto *toast = new DToast(this);

// ✅ 正确：使用 DMessageManager
DMessageManager::instance()->sendMessage(this, QIcon(), "提示消息");
```

### 错误 2：临时消息设置过长时长

```cpp
// ❌ 错误：临时消息不应常驻
auto *msg = new DFloatingMessage(DFloatingMessage::TransientType);
msg->setDuration(60000); // 60秒

// ✅ 正确：需要长时间显示时使用常驻消息
auto *msg = new DFloatingMessage(DFloatingMessage::ResidentType);
```

## 7. 相关文档

- [index.md](index.md) - 控件选择决策树
- [dialog.md](dialog.md) - 对话框规范
