# Chameleon 风格：QWidget 与 QML 共用概览

## 1. 概述与适用场景

Chameleon 是 DTK 的统一视觉风格，同时支持 QWidget 和 QML 两套 UI 技术栈。

**适用场景：**
- 理解 DTK 控件绘制机制
- 自定义控件时复用 DTK 风格元素
- 理解 QWidget 和 QML 风格差异

**相关接口：**
- QWidget: `DStyle` / `ChameleonStyle` / `DStyleHelper`
- QML: `org.deepin.dtk` 控件 / `ColorSelector`

## 2. Chameleon 是什么

Chameleon（变色龙）是 DTK 为两套 Qt UI 技术栈提供的统一视觉风格名称。DTK 同时实现了两个独立插件：

| 技术栈 | 插件类型 | 实现项目 | 主要职责 |
|---|---|---|---|
| QWidget | Qt `QStylePlugin` | `dde-qtintegration/styleplugins/chameleon/` | 通过 `DStyle`/`ChameleonStyle` 绘制 QWidget，计算尺寸、子区域和命中区域 |
| QML | Qt Quick Controls 2 Style 插件 | `dtkdeclarative/chameleon/` | 把 Qt Quick Controls 的控件类型映射到 DTK QML 控件实现 |

二者名称和设计语言相同，但不是同一份绘制代码，也不能相互替代。QWidget 使用 `QPainter` 和 `QStyleOption`；QML 使用 Qt Quick 的 Item、属性绑定、状态和场景图。

```text
                         DTK 主题与设计语义
                    palette / DPalette / DCI / 字体
                              │
              ┌───────────────┴────────────────┐
              │                                │
    QWidget Chameleon                  QML Chameleon
    QStylePlugin                       Qt Quick Controls 2 Style
    DStyle → ChameleonStyle            *.qml → org.deepin.dtk 控件
              │                                │
         QWidget 应用                       QML 应用
```

## 3. 两套实现共用什么

两套插件共同遵循 DTK 的视觉语义：

- 使用主题调色板，而不是在应用中硬编码亮色和暗色；
- 以 normal、hover、pressed、checked、disabled、focus 等状态选择背景和前景；
- 使用 DTK 的圆角、间距、字体和图标规范；
- DCI 图标可按 Light/Dark 主题和 Normal/Hover/Pressed/Disabled 模式切换；
- 主题或 palette 更新后，控件应重新解析颜色并刷新。

“共用”指设计语义、颜色体系、图标资源和用户体验保持一致，不表示 QWidget 与 QML 共用同一个插件 ABI 或同一个 paint 函数。

## 3. 动态指定风格并进行对比调试

调试风格问题时，优先在启动命令中临时指定插件。这样不需要修改代码，也能用同一份程序快速比较 Chameleon 与 Qt 内置风格。

### 3.1 QWidget

Qt 的通用 `-style` 参数可在本次运行中指定 `QStyle`：

```bash
./my-widget-app -style chameleon
./my-widget-app -style fusion
```

也可以通过环境变量覆盖本次进程的 QWidget 风格：

```bash
QT_STYLE_OVERRIDE=chameleon ./my-widget-app
QT_STYLE_OVERRIDE=fusion ./my-widget-app
```

代码中仍可使用 `QApplication::setStyle("chameleon")`，但应在创建普通控件前调用。对比调试更推荐命令行或环境变量，因为不会把诊断设置提交到业务代码。

可以输出实际加载结果和可用键名：

```cpp
qInfo() << "current style:" << QApplication::style()->objectName();
qInfo() << "available styles:" << QStyleFactory::keys();
```

### 3.2 QML / Qt Quick Controls 2

QML 风格可通过环境变量动态指定：

```bash
QT_QUICK_CONTROLS_STYLE=Chameleon ./my-qml-app
QT_QUICK_CONTROLS_STYLE=Basic ./my-qml-app
QT_QUICK_CONTROLS_STYLE=Fusion ./my-qml-app
```

Qt Quick Controls 也支持启动参数，可用于临时对比：

```bash
./my-qml-app -style Chameleon
./my-qml-app -style Basic
```

代码方式为 `QQuickStyle::setStyle("Chameleon")`。必须在加载 QML、创建第一个 Qt Quick Controls 控件之前调用；风格一旦完成初始化，就不适合在同一进程中切换。需要对比时应分别启动进程。

### 3.3 插件未加载时

先打开 Qt 插件诊断：

```bash
QT_DEBUG_PLUGINS=1 ./my-widget-app -style chameleon
QT_DEBUG_PLUGINS=1 QT_QUICK_CONTROLS_STYLE=Chameleon ./my-qml-app
```

重点检查：

- QWidget：输出中是否扫描到包含 Chameleon 的 Qt `styles` 插件目录；
- QML：QML import path 中是否存在 Chameleon 模块和 `qmldir`；
- 应用使用的 Qt 主版本、架构和构建配置是否与插件一致；
- 对比测试时是否被代码中的 `setStyle()` 或其他启动脚本再次覆盖。

### 3.4 修改 palette 不生效时的对比方法

如果应用已经调用 `setPalette()` 或 `DPaletteHelper::setPalette()`，但控件背景、前景或状态色没有变化，可用同一程序临时切换到非 Chameleon 风格：

```bash
# QWidget：保持业务代码和 palette 设置不变，只替换风格
./my-widget-app -style chameleon
./my-widget-app -style fusion
```

如果 palette 在 Fusion 等风格下生效、在 Chameleon 下不生效，通常说明该控件的 Chameleon 绘制分支没有读取这个 palette role、使用了另一个 `DPalette::ColorType`，或者被 DCI/专用绘制逻辑覆盖。此时应对照 `chameleonstyle.cpp` 中对应的 `drawPrimitive()`、`drawControl()` 或 `drawComplexControl()` 分支确认实际颜色来源，而不是继续在应用层重复设置同一角色。

反之，如果切换到 Fusion 后仍不生效，应优先检查：palette 是否设置到了真正参与绘制的内部控件、是否被 model/delegate 或 Style Sheet 覆盖，以及 Active/Inactive/Disabled 颜色组是否正确。

QML 也可以保持 palette 绑定不变，分别以 `QT_QUICK_CONTROLS_STYLE=Chameleon` 和 `QT_QUICK_CONTROLS_STYLE=Basic` 启动两个进程对比。由于两种风格的控件实现可能读取不同属性，对比结果用于定位问题层级，不代表所有 palette role 必须在不同风格中产生完全相同的视觉效果。

若测试未安装的本地构建，可临时设置精确的 `QT_PLUGIN_PATH` 或 `QML2_IMPORT_PATH`。不要把整个系统目录永久加入这些变量，否则可能加载到另一 Qt 版本的插件。

## 4. QWidget Chameleon

### 4.1 实现结构

```text
QCommonStyle
└── DStyle                         dtkwidget
    └── ChameleonStyle             dde-qtintegration

QStylePlugin
└── ChameleonStylePlugin
    └── create("chameleon") → ChameleonStyle
```

`ChameleonStylePlugin` 的键名为小写 `chameleon`，安装在 Qt styles 插件目录。Deepin 平台主题把它作为 QWidget 首选风格，`DApplication` 在需要时也会主动选择该风格。

`DStyle` 提供 DTK 扩展元素、度量、标准图标和状态画刷；`ChameleonStyle` 实现 `drawPrimitive()`、`drawControl()`、`drawComplexControl()`、布局、命中测试、动画以及 widget polish。

### 4.2 详细文档

Widget 控件的背景、前景、hover/pressed/checked 状态组合以及图标、文字、箭头等绘制区域，统一放在：

- [Widget ChameleonStyle 控件绘制指南](../widgets/style.md)

## 5. QML Chameleon

### 5.1 插件结构

`dtkdeclarative/chameleon/` 是 Qt Quick Controls 2 style 模块。它包含插件类 `QtQuickControls2ChameleonStylePlugin`、`qmldir` 和一组与 Qt Quick Controls 同名的 QML 文件，例如：

- `Button.qml`、`CheckBox.qml`、`RadioButton.qml`、`Switch.qml`；
- `TextField.qml`、`TextArea.qml`、`ComboBox.qml`、`SpinBox.qml`；
- `Slider.qml`、`ProgressBar.qml`、`ScrollBar.qml`；
- `Menu.qml`、`MenuItem.qml`、`Popup.qml`、`ToolTip.qml`；
- `ApplicationWindow.qml`、`Control.qml`、`Pane.qml`、`Frame.qml`。

这些文件不是把 QWidget 的 ChameleonStyle 包装到 QML。例如 `Button.qml` 直接实例化 `org.deepin.dtk` 模块中的 `D.Button`，`Control.qml` 直接实例化 `D.Control`。实际背景、contentItem、indicator、状态绑定和 palette 逻辑由 dtkdeclarative 的 DTK QML 控件实现。

### 5.2 模块名称与 Qt 版本差异

源码体现了两种构建路径：

- DTK5 路径安装到 `QtQuick/Controls.2/Chameleon`，`qmldir.in` 声明 `module QtQuick.Controls.Chameleon`；
- 非 DTK5 路径使用 `qt_add_qml_module()` 构建 URI 为 `Chameleon` 的模块；
- 启用 `QQuickStylePlugin` 私有接口时，插件的 `name()` 返回大小写敏感的 `Chameleon`。

因此不要把 QWidget 的键名 `chameleon` 与 QML 风格名 `Chameleon` 混淆。

### 5.3 启用方式

QML 应用应在加载第一个 Qt Quick Controls 之前选择风格，例如通过 Qt Quick Controls 支持的环境变量或 `QQuickStyle::setStyle("Chameleon")`。具体可用模块路径取决于 Qt/DTK 构建版本及安装位置。

选择 Chameleon 后，应用仍使用标准 Qt Quick Controls 类型，style 模块负责解析到对应的 QML 文件。直接使用 `org.deepin.dtk` 控件时，则已经进入 DTK QML 控件实现，不需要借助 QWidget 的 `QApplication::setStyle()`。

## 6. QML 样式数据定制

QML Chameleon 插件负责控件类型映射；DTK 控件内部还通过 `org.deepin.dtk.style` URI 的 `Style` 单例读取尺寸和状态调色板。默认数据由 `FlowStyle.qml` 提供，应用覆盖 `Style.qml` 的资源路径、示例及调试方法见 [QML Style 单例与应用级样式覆盖](../declarative/style.md)。

## 7. 不能混用的 API

| QWidget | QML |
|---|---|
| `QApplication::setStyle("chameleon")` | `QQuickStyle::setStyle("Chameleon")` |
| `QStyleOption::state` | QML 控件的 `hovered`、`pressed`、`checked`、`enabled`、`visualFocus` 等属性 |
| `QPalette` / `DPaletteHelper` | QML Palette、颜色选择器和属性绑定 |
| `drawControl()` / `QPainter` | `background`、`contentItem`、`indicator`、场景图节点 |
| `subControlRect()` | anchors、implicit size、padding/inset 和布局绑定 |

QML 页面不能调用 `QStyle::drawControl()` 获得 QML Chameleon 外观；QWidget 也不能导入 QML style 文件替代 `QStylePlugin`。

## 8. 排查顺序

1. 先确认应用是 QWidget 还是 Qt Quick Controls；
2. QWidget 检查 `QApplication::style()->objectName()`、Qt styles 插件目录和平台主题；
3. QML 检查风格是否在创建控件前设置、QML import path 中是否存在 Chameleon 模块；
4. 仅颜色不一致时，检查应用 palette、主题类型和控件局部 palette 覆盖；
5. 仅某一技术栈异常时，到对应插件源码排查，不要在另一套 Chameleon 实现中修复。

## 9. 相关文档

- [Widget ChameleonStyle 控件绘制指南](../widgets/style.md)
- [palette.md](palette.md) — DTK 语义色和 palette
- [theme-switch.md](theme-switch.md) — 主题切换
- [dci.md](dci.md) — DCI 图标主题与状态
- [QML 控件索引](../declarative/index.md)
