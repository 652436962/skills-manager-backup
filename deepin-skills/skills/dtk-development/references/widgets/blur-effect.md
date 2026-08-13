# DBlurEffectWidget 模糊效果

## 1. 概述与适用场景

`DBlurEffectWidget`（dtkwidget）提供窗口模糊效果。常用于实现半透明毛玻璃背景的面板、弹出框和工具窗口。

**适用场景：**
- 面板/弹出框的毛玻璃背景
- 工具窗口的模糊效果
- 叠加层的半透明效果

## 2. 枚举

### 2.1 BlendMode（混合模式）

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | `InWindowBlend` | 窗口内混合，模糊窗口自身下方内容 |
| 1 | `BehindWindowBlend` | 窗口后混合，模糊窗口后方桌面内容 |
| 2 | `InWidgetBlend` | 控件内混合，模糊父控件内容 |

### 2.2 BlurMode（模糊模式）

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | `GaussianBlur` | 高斯模糊 |

### 2.3 MaskColorType（遮罩颜色类型）

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | `DarkColor` | 深色遮罩 |
| 1 | `LightColor` | 浅色遮罩 |
| 2 | `AutoColor` | 自动跟随主题 |
| 3 | `CustomColor` | 自定义颜色 |

## 3. 核心 API

### 3.1 基本用法

```cpp
#include <DBlurEffectWidget>

auto *blurWidget = new DBlurEffectWidget(this);
blurWidget->setBlendMode(DBlurEffectWidget::BehindWindowBlend);
blurWidget->setRadius(30);
blurWidget->setMaskColor(DBlurEffectWidget::AutoColor);
blurWidget->setBlurRectXRadius(8);
blurWidget->setBlurRectYRadius(8);
blurWidget->resize(300, 200);
```

### 3.2 BehindWindowBlend

模糊窗口后方桌面内容，最常用模式：

```cpp
auto *blur = new DBlurEffectWidget(this);
blur->setBlendMode(DBlurEffectWidget::BehindWindowBlend);
blur->setRadius(35);
blur->setMaskColor(DBlurEffectWidget::AutoColor);
blur->setBlurEnabled(true);
```

### 3.3 InWindowBlend

模糊窗口自身下方的控件内容：

```cpp
auto *blur = new DBlurEffectWidget(parentWidget);
blur->setBlendMode(DBlurEffectWidget::InWindowBlend);
blur->setRadius(20);
blur->setMaskAlpha(102);
```

> `radius` 属性仅在 `InWindowBlend` 模式下有效。

### 3.4 遮罩颜色

```cpp
// 自动跟随主题
blurWidget->setMaskColor(DBlurEffectWidget::AutoColor);

// 自定义颜色
blurWidget->setMaskColor(QColor(0, 0, 0, 80));

// 设置遮罩透明度
blurWidget->setMaskAlpha(102);
```

> maskColor 的 alpha 通道：若 `DPlatformWindowHandle::hasBlurWindow()` 为 true 则固定 102，否则固定 204。

### 3.5 自定义遮罩路径

```cpp
QPainterPath path;
path.addRoundedRect(rect, 8, 8);
blurWidget->setMaskPath(path);
```

### 3.6 全屏模糊

```cpp
blurWidget->setFull(true);
```

### 3.7 禁用/启用模糊

```cpp
blurWidget->setBlurEnabled(false); // 临时禁用
blurWidget->setBlurEnabled(true);  // 重新启用
```

## 4. 属性一览

| 属性 | 类型 | 说明 |
|------|------|------|
| `radius` | `int` | 模糊半径（仅 InWindowBlend） |
| `mode` | `BlurMode` | 模糊模式 |
| `blendMode` | `BlendMode` | 混合模式 |
| `blurRectXRadius` | `int` | 模糊区域 X 圆角 |
| `blurRectYRadius` | `int` | 模糊区域 Y 圆角 |
| `maskColor` | `QColor` | 遮罩颜色 |
| `maskAlpha` | `quint8` | 遮罩透明度 |
| `full` | `bool` | 是否全屏模糊 |
| `blurEnabled` | `bool` | 是否启用模糊 |

## 5. DBlurEffectGroup 共享模糊

多个 `DBlurEffectWidget` 共享同一个模糊源图像：

```cpp
auto *group = new DBlurEffectGroup();
group->setSourceImage(backgroundImage, 35);

group->addWidget(blurWidget1, QPoint(0, 0));
group->addWidget(blurWidget2, QPoint(100, 0));

group->removeWidget(blurWidget1);
```

## 6. 信号

| 信号 | 参数 | 说明 |
|------|------|------|
| `radiusChanged` | `int` | 半径变化 |
| `modeChanged` | `BlurMode` | 模糊模式变化 |
| `blendModeChanged` | `BlendMode` | 混合模式变化 |
| `maskColorChanged` | `QColor` | 遮罩颜色变化 |
| `maskAlphaChanged` | `quint8` | 遮罩透明度变化 |
| `fullChanged` | `bool` | 全屏状态变化 |
| `blurEnabledChanged` | `bool` | 模糊启用状态变化 |
| `blurSourceImageDirtied` | 无 | 模糊源图像脏 |

## 7. 常见错误与避坑

### 错误 1：radius 在 BehindWindowBlend 下无效

```cpp
// ❌ 错误：BehindWindowBlend 模式下 radius 无效
blur->setBlendMode(DBlurEffectWidget::BehindWindowBlend);
blur->setRadius(50); // 不生效

// ✅ 正确：radius 仅在 InWindowBlend 下生效
blur->setBlendMode(DBlurEffectWidget::InWindowBlend);
blur->setRadius(50);
```

### 错误 2：忘记设置圆角

```cpp
// ❌ 错误：模糊区域为矩形
blur->setBlendMode(DBlurEffectWidget::BehindWindowBlend);

// ✅ 正确：设置圆角
blur->setBlurRectXRadius(8);
blur->setBlurRectYRadius(8);
```

## 8. 相关文档

- [window.md](window.md) - 窗口规范
- [../utilities/window-manager.md](../utilities/window-manager.md) - 窗口管理助手
- [../platform-abstraction.md](../platform-abstraction.md) - 平台抽象层
