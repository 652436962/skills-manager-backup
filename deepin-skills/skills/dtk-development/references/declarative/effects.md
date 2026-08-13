# QML 效果组件

## 1. 概述

dtkdeclarative 提供多种视觉效果组件：

| 组件 | 用途 |
|------|------|
| `InWindowBlur` / `BehindWindowBlur` | 模糊效果 |
| `GlowEffect` | 辉光效果 |
| `ColorOverlay` / `OpacityMask` | 颜色叠加（位于 `private/` 子目录） |
| `WaterProgressBar` | 水波纹进度 |

## 2. 模糊效果

```qml
import org.deepin.dtk 1.0

Item {
    InWindowBlur {
        anchors.fill: parent
        radius: 20
    }
}
```

## 3. 相关文档

- [index.md](index.md) - QML 控件选择
