# 导航与布局控件规范

## 1. 概述与适用场景

| 控件 | 适用场景 |
|------|----------|
| `DTabBar` | 标签页切换 |
| `DDrawer` / `DDrawerGroup` | 可展开/折叠的分组 |
| `DFrame` | 带圆角边框的容器 |
| `DBackgroundGroup` | 带背景色的分组 |
| `DHeaderLine` | 带标题的分组行 |
| `DStackWidget` | 页面堆栈切换 |

## 2. 各控件用法

### 2.1 DTabBar — 标签页

```cpp
#include <DTabBar>

auto *tabBar = new DTabBar(this);
tabBar->addTab("常规");
tabBar->addTab("高级");
tabBar->addTab("关于");

connect(tabBar, &DTabBar::currentChanged, [stack](int index) {
    stack->setCurrentIndex(index);
});
```

### 2.2 DDrawer — 可折叠分组

```cpp
#include <DDrawer>

auto *drawer = new DDrawer(this);

// 设置标题
auto *header = new QPushButton("高级设置", this);
drawer->setHeader(header);

// 设置内容
auto *content = new QWidget(this);
auto *layout = new QVBoxLayout(content);
layout->addWidget(new QLabel("设置项1"));
layout->addWidget(new QLabel("设置项2"));
drawer->setContent(content);

// 展开/折叠
drawer->setExpand(true);

connect(drawer, &DDrawer::expandChange, [](bool expanded) {
    qInfo() << "Expanded:" << expanded;
});
```

### 2.3 DDrawerGroup — 分组管理

```cpp
#include <DDrawerGroup>

auto *group = new DDrawerGroup(this);

// 添加多个 DDrawer
auto *drawer1 = new DDrawer(this);
auto *drawer2 = new DDrawer(this);
group->addExpand(drawer1);
group->addExpand(drawer2);

// DDrawerGroup 自动确保同一时间只展开一个
```

### 2.4 DFrame — 容器

```cpp
#include <DFrame>

auto *frame = new DFrame(this);
frame->setFrameRounded(true);
frame->setBackgroundRole(DPalette::ItemBackground);

auto *layout = new QVBoxLayout(frame);
layout->addWidget(new QLabel("内容区域"));
```

## 3. 常见错误与避坑

### 错误 1：使用废弃的 DBaseExpand

```cpp
// ❌ 错误：DBaseExpand 已废弃
auto *expand = new DBaseExpand(this);

// ✅ 正确：使用 DDrawer
auto *drawer = new DDrawer(this);
```

### 错误 2：使用废弃的 DExpandGroup

```cpp
// ❌ 错误：DExpandGroup 已废弃
auto *group = new DExpandGroup(this);

// ✅ 正确：使用 DDrawerGroup
auto *group = new DDrawerGroup(this);
```

## 4. 相关文档

- [index.md](index.md) - 控件选择决策树
- [container.md](container.md) - 容器/分组控件
