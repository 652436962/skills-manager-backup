# QWidget 控件选择决策树

## 触发关键词

本文档适用于以下任务场景：

**自然语言描述：**
- 创建对话框/主窗口/按钮
- 控件选择/使用什么控件
- 输入框/下拉框/开关按钮
- 列表视图/树形视图
- 进度条/滑动条/消息提示

**API 接口描述：**
- DDialog / DMainWindow / DButton
- DLineEdit / DComboBox / DSpinBox
- DListView / DTreeView / DStyledItemDelegate
- DProgressBar / DSlider / DMessageManager

---

## 概述

DTK 提供丰富的 QWidget 控件，本文档帮助您快速选择正确的控件。

## 快速决策树

```
需要什么类型的控件？
    │
    ├─ 对话框 → DDialog（简单交互）、DInputDialog（输入）、DFileDialog（文件选择）
    │
    ├─ 窗口 → DMainWindow（主窗口）、DTitlebar（标题栏）
    │
    ├─ 按钮 → 需要推荐样式？
    │           ├─ 是 → DSuggestButton
    │           └─ 否 → 需要警告样式？
    │                     ├─ 是 → DWarningButton
    │                     └─ 否 → 仅显示图标？
    │                               ├─ 是 → DIconButton
    │                               └─ 否 → DPushButton / DToolButton
    │
    ├─ 输入 → 单行文本？
    │           ├─ 是 → 需要搜索？
    │           │         ├─ 是 → DSearchEdit
    │           │         └─ 否 → 需要密码？
    │           │                   ├─ 是 → DPasswordEdit
    │           │                   └─ 否 → DLineEdit
    │           └─ 否 → 多行文本 → DTextEdit
    │                     或 数值 → DSpinBox / DDoubleSpinBox
    │                     或 快捷键 → DKeySequenceEdit
    │
    ├─ 开关 → DSwitchButton
    │
    └─ 选择 → 下拉选择 → DComboBox
              或 多选 → DCheckBox
              或 单选 → DRadioButton
```

## API 速查表

### 对话框

| 控件 | 头文件 | 用途 |
|------|--------|------|
| `DDialog` | `#include <DDialog>` | 通用对话框 |
| `DInputDialog` | `#include <DInputDialog>` | 输入对话框 |
| `DFileDialog` | `#include <DFileDialog>` | 文件选择对话框 |
| `DAboutDialog` | `#include <DAboutDialog>` | 关于对话框 |
| `DSettingsDialog` | `#include <DSettingsDialog>` | 设置对话框 |

### 窗口

| 控件 | 头文件 | 用途 |
|------|--------|------|
| `DMainWindow` | `#include <DMainWindow>` | 主窗口 |
| `DTitlebar` | `#include <DTitlebar>` | 标题栏 |
| `DApplication` | `#include <DApplication>` | 应用入口 |

### 按钮

| 控件 | 头文件 | 用途 |
|------|--------|------|
| `DSuggestButton` | `#include <DSuggestButton>` | 推荐按钮（主要操作） |
| `DWarningButton` | `#include <DWarningButton>` | 警告按钮（危险操作） |
| `DIconButton` | `#include <DIconButton>` | 图标按钮 |
| `DSwitchButton` | `#include <DSwitchButton>` | 开关按钮 |
| `DButtonBox` | `#include <DButtonBox>` | 按钮组 |
| `DFloatingButton` | `#include <DFloatingButton>` | 浮动按钮 |

### 输入

| 控件 | 头文件 | 用途 |
|------|--------|------|
| `DLineEdit` | `#include <DLineEdit>` | 单行输入 |
| `DSearchEdit` | `#include <DSearchEdit>` | 搜索输入 |
| `DPasswordEdit` | `#include <DPasswordEdit>` | 密码输入 |
| `DTextEdit` | `#include <DTextEdit>` | 多行文本 |
| `DSpinBox` | `#include <DSpinBox>` | 整数输入 |
| `DComboBox` | `#include <DComboBox>` | 下拉选择 |

### 视图

| 控件 | 头文件 | 用途 |
|------|--------|------|
| `DListView` | `#include <DListView>` | 列表视图 |
| `DTreeView` | `#include <DTreeView>` | 树形视图 |
| `DStyledItemDelegate` | `#include <DStyledItemDelegate>` | 列表项委托 |

### 其他

| 控件 | 头文件 | 用途 |
|------|--------|------|
| `DProgressBar` | `#include <DProgressBar>` | 进度条 |
| `DSlider` | `#include <DSlider>` | 滑动条 |
| `DMessageManager` | `#include <DMessageManager>` | 消息管理 |
| `DToolTip` | `#include <DToolTip>` | 工具提示 |

## 相关文档

- [dialog.md](dialog.md) — 对话框详细规范
- [window.md](window.md) — 窗口详细规范
- [button.md](button.md) — 按钮详细规范
- [input.md](input.md) — 输入控件详细规范
- [view.md](view.md) — 视图控件
- [item-delegate.md](item-delegate.md) — 列表项委托
- [progress.md](progress.md) — 进度与状态
- [message.md](message.md) — 消息与通知
- [style.md](style.md) — 控件绘制机制
