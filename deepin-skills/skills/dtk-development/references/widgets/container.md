# 容器与分组控件规范

## 1. 概述与适用场景

| 控件 | 适用场景 |
|------|----------|
| `DFrame` | 带圆角边框的容器 |
| `DBackgroundGroup` | 带背景色的分组 |
| `DHeaderLine` | 带标题的分割线 |
| `DHorizontalLine` | 水平分割线 |
| `DVerticalLine` | 垂直分割线 |

## 2. 各控件用法

### 2.1 DFrame — 带边框容器

```cpp
#include <DFrame>

auto *frame = new DFrame(this);
frame->setFrameRounded(true);
frame->setBackgroundRole(DPalette::ItemBackground);

auto *layout = new QVBoxLayout(frame);
layout->addWidget(new QLabel("内容"));
```

### 2.2 DBackgroundGroup — 背景分组

```cpp
#include <DBackgroundGroup>

auto *group = new DBackgroundGroup(this);
group->setBackgroundRole(DPalette::ObviousBackground);

auto *layout = new QVBoxLayout(group);
layout->addWidget(new QPushButton("选项1"));
layout->addWidget(new QPushButton("选项2"));
```

### 2.3 DHeaderLine — 标题行

```cpp
#include <DHeaderLine>

auto *header = new DHeaderLine(this);
header->setTitle("高级设置");
```

### 2.4 分割线

```cpp
// 水平分割线
auto *hline = new DHorizontalLine(this);

// 垂直分割线
auto *vline = new DVerticalLine(this);
```

## 3. 相关文档

- [index.md](index.md) - 控件选择决策树
- [navigation.md](navigation.md) - 导航与布局控件
