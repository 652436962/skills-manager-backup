# builtin 图标规范

## 1. 概述与适用场景

**builtin 图标**是 DTK 内置在资源文件中的图标集合，特点：

- **内置资源**：随 dtkgui/dtkwidget 打包，无需额外文件
- **主题感知**：自动适配 Light/Dark 主题
- **即用即得**：通过图标名称直接调用，无需关心路径

**适用场景：**
- DTK 应用内的标准 UI 图标
- 对话框按钮图标（确定、取消、警告等）
- 工具栏通用图标
- 需要主题切换但无需动画的图标

**不适用场景：**
- 应用特有的自定义图标 → 使用 **dci 图标**
- 需要兼容其他桌面环境 → 使用 **icon theme 图标**

## 2. 文件格式规范

builtin 图标由 DTK 内部资源注册，通过图标名称引用。资源前缀是 DTK 的实现细节，应用代码不应拼接或直接加载它。

### 2.1 图标命名格式

资源文件名格式为 `<icon-name>_<size>px.svg`，但 `DIconTheme::findQIcon()` 的参数必须使用不含尺寸后缀的基础名称。例如：
- `window-close_round` - 窗口关闭按钮（资源尺寸 30px）
- `icon_fail` - 失败图标（资源尺寸 128px）
- `icon_success` - 成功图标（资源尺寸 128px）
- `icon_warning` - 警告图标（资源尺寸 32px）
- `icon_ok` - 确认图标（资源尺寸 32px）
- `icon_info` - 信息图标（资源尺寸 32px）

`DBuiltinIconEngine` 通过基础名称匹配资源，并从文件名的 `_NNpx` 部分解析可用尺寸；不要将 `_NNpx` 传给 `findQIcon()`。

### 2.2 DIconTheme::findQIcon 查找链路

`DIconTheme::findQIcon(iconName)` 按以下优先级查找图标：

```
1. dci 图标（按 iconName 查找）
      ↓ 未找到
2. builtin 图标（由 DTK 内部资源按名称查找）
      ↓ 未找到
3. XDG 图标主题（QIcon::fromTheme，除非指定 DontFallbackToQIconFromTheme）
```

## 3. API 用法

### 3.1 加载图标

```cpp
#include <DIconTheme>

// 方式 1：查找图标（按优先级：dci → builtin → xdg）
QIcon icon = DIconTheme::findQIcon("window-close_round");

// 方式 2：指定回退图标
QIcon fallback = DIconTheme::findQIcon("default");
QIcon icon = DIconTheme::findQIcon("window-close_round", fallback);

// 方式 3：带选项查找（跳过 dci，直接查找 builtin）
QIcon icon = DIconTheme::findQIcon("icon_warning", DIconTheme::IgnoreDciIcons);
```

### 3.2 检查图标类型

```cpp
#include <DIconTheme>

QIcon icon = DIconTheme::findQIcon("icon_ok");

// 检查是否为内置图标
if (DIconTheme::isBuiltinIcon(icon)) {
    // 这是 DTK 内置图标
}

// 检查是否为 XDG 图标主题图标
if (DIconTheme::isXdgIcon(icon)) {
    // 这是系统图标主题图标
}
```

### 3.3 使用选项控制查找行为

```cpp
#include <DIconTheme>

// 不回退到 QIcon::fromTheme
QIcon icon = DIconTheme::findQIcon("my-icon", 
    DIconTheme::DontFallbackToQIconFromTheme);

// 忽略 builtin 图标，只查找 dci 和 icon theme
QIcon icon = DIconTheme::findQIcon("my-icon", 
    DIconTheme::IgnoreBuiltinIcons);

// 忽略 dci 图标，只查找 builtin 和 icon theme
QIcon icon = DIconTheme::findQIcon("my-icon", 
    DIconTheme::IgnoreDciIcons);

// 组合选项：忽略缓存和 builtin
QIcon icon = DIconTheme::findQIcon("my-icon", 
    DIconTheme::IgnoreIconCache | DIconTheme::IgnoreBuiltinIcons);
```

### 3.4 图标缓存管理

```cpp
#include <DIconTheme>

// 获取缓存实例
auto *cache = DIconTheme::cached();

// 设置最大缓存大小
cache->setMaxCost(1024 * 1024); // 1MB

// 清除缓存
cache->clear();

// 从缓存查找
QIcon icon = cache->findQIcon("dialog-ok");

// 查找 dci 图标文件路径
QString dciPath = cache->findDciIconFile("my-icon", "deepin");
```

## 4. 完整示例

### 4.1 标准按钮图标

```cpp
#include <DIconTheme>

// 创建带内置图标的按钮
auto *btn = new DPushButton("确定", this);
btn->setIcon(DIconTheme::findQIcon("icon_ok"));

auto *cancelBtn = new DPushButton("取消", this);
cancelBtn->setIcon(DIconTheme::findQIcon("window-close_round"));
```

### 4.2 警告对话框图标

```cpp
#include <DIconTheme>
#include <DDialog>

auto *dialog = new DDialog(this);
dialog->setIcon(DIconTheme::findQIcon("icon_warning"));
dialog->setTitle("警告");
dialog->setMessage("确定要删除此文件吗？");
dialog->exec();
```

### 4.3 状态图标

```cpp
#include <DIconTheme>
#include <QLabel>

// 成功/失败状态图标
auto *successLabel = new QLabel(this);
successLabel->setPixmap(DIconTheme::findQIcon("icon_success").pixmap(64));

auto *failLabel = new QLabel(this);
failLabel->setPixmap(DIconTheme::findQIcon("icon_fail").pixmap(64));
```

## 5. 常用 builtin 图标列表

以下为实际存在的 builtin 图标名称（来自 dtkgui 资源文件）：

| 图标名称 | 尺寸 | 用途 |
|----------|------|------|
| `window-close_round` | 30px | 窗口关闭按钮 |
| `icon_ok` | 32px | 确认/成功 |
| `icon_info` | 32px | 信息提示 |
| `icon_warning` | 32px | 警告提示 |
| `icon_success` | 128px | 成功状态（大图标） |
| `icon_fail` | 128px | 失败状态（大图标） |
| `button_voice` | 30px | 音量按钮 |
| `button_voice_active` | 30px | 音量激活状态 |
| `button_edit-clear` | 30px | 清除按钮 |
| `list_add` | 16px | 列表添加项 |
| `list_delete` | 16px | 列表删除项 |
| `caps_lock` | 16px | 大写锁定指示 |
| `password_show` | 24px | 显示密码 |
| `password_hide` | 24px | 隐藏密码 |
| `edit` | 12px | 编辑按钮 |
| `mark_indicator` | 12px | 标记指示器 |
| `fork_indicator` | 24px | 分叉指示器 |
| `lock_indicator` | 24px | 锁定指示器 |
| `unlock_indicator` | 24px | 解锁指示器 |
| `search_indicator` | 20px | 搜索指示器 |
| `checked` | 20px | 选中状态 |
| `unchecked` | 20px | 未选中状态 |
| `go-next` | 12px | 前进箭头 |
| `go-previous` | 12px | 后退箭头 |
| `go-up` | 12px | 向上箭头 |
| `go-down` | 12px | 向下箭头 |

**注意**：builtin 图标名称与 XDG 图标主题名称不同，必须使用上述实际名称。

## 6. 与 dci/icontheme 的选择建议

| 对比项 | builtin 图标 | dci 图标 | icon theme 图标 |
|--------|-------------|----------|----------------|
| 来源 | DTK 内置 | 应用自定义 | 系统图标主题 |
| 主题切换 | ✅ 自动 | ✅ 自动 | ⚠️ 需处理 |
| 动画 | ❌ 不支持 | ✅ 支持 | ❌ 不支持 |
| 自定义 | ❌ 仅限内置 | ✅ 完全自定义 | ✅ 主题可换 |
| XDG 兼容 | ❌ DTK 专用 | ❌ DTK 专用 | ✅ 标准规范 |

**选择建议：**
- 标准 UI 图标（按钮、对话框） → **builtin 图标**
- 应用自定义图标（Logo、特色图标） → **dci 图标**
- 需要跨桌面兼容 → **icon theme 图标**
