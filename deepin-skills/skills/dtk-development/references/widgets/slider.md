# DSlider 滑动条

## 1. 概述与适用场景

`DSlider`（dtkwidget）提供 DTK 风格的滑动条。在 QSlider 基础上增加了图标和刻度标签功能。

**适用场景：**
- 数值范围选择
- 音量/亮度调节
- 需要图标装饰的滑动条

## 2. 枚举

### SliderIcons

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | `LeftIcon` | 左侧图标 |
| 1 | `RightIcon` | 右侧图标 |

## 3. 核心 API

### 3.1 基本用法

```cpp
#include <DSlider>

auto *slider = new DSlider(Qt::Horizontal, this);
slider->setMinimum(0);
slider->setMaximum(100);
slider->setValue(50);

connect(slider, &DSlider::valueChanged, [](int value) {
    qInfo() << "Value:" << value;
});
```

### 3.2 设置图标

```cpp
// 设置左右图标（如音量图标）
slider->setLeftIcon(QIcon::fromTheme("audio-volume-low"));
slider->setRightIcon(QIcon::fromTheme("audio-volume-high"));

// 监听图标点击
connect(slider, &DSlider::iconClicked, [](DSlider::SliderIcons icon, bool checked) {
    if (icon == DSlider::LeftIcon) { /* 点击了左图标 */ }
});

// 设置图标大小
slider->setIconSize(QSize(24, 24));
```

### 3.3 设置刻度标签

```cpp
// 设置刻度标签
slider->setAboveTicks({"低", "中", "高"});
slider->setBelowTicks({"0", "50", "100"});
slider->setLeftTicks({"0", "25", "50", "75", "100"});
slider->setRightTicks({"低", "中", "高"});

// 设置标记位置
slider->setMarkPositions({0, 25, 50, 75, 100});
```

### 3.4 其他设置

```cpp
// 获取内部 QSlider
QSlider *qslider = slider->slider();

// 设置分页步长
slider->setPageStep(10);

// 禁用鼠标滚轮
slider->setMouseWheelEnabled(false);

// 设置提示值
slider->setTipValue("50%");

// 控制滑块可见性
slider->setHandleVisible(false);

// 跨样式启用
slider->setEnabledAcrossStyle(true);
```

## 4. 信号

| 信号 | 参数 | 说明 |
|------|------|------|
| `valueChanged` | `int` | 值变化 |
| `sliderPressed` | 无 | 滑块按下 |
| `sliderMoved` | `int` | 滑块移动 |
| `sliderReleased` | 无 | 滑块释放 |
| `rangeChanged` | `int min, int max` | 范围变化 |
| `actionTriggered` | `int` | 动作触发 |
| `iconClicked` | `SliderIcons, bool` | 图标点击 |

## 5. 相关文档

- [input.md](input.md) - 输入控件
- [progress.md](progress.md) - 进度控件
