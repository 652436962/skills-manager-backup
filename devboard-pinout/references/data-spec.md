# 交互式引脚图 · data-* 属性规范

本文档定义「HTML + SVG + data 属性」交互式引脚图的数据规范，配合 `assets/pinout-template.html` 使用。页面无需数据库或后端，全部信息通过每个 SVG 元件 `<g class="part">` 上的 `data-*` 属性承载，脚本自动读取渲染。

## 1. 工作模式

- 每个板载元件 = 一个 `<g class="part">` 元素，内部用 SVG 图形（rect/circle/path/text）绘制外观。
- 元件信息全部写在 `data-*` 属性上，**新增元件只需追加一个带完整 data 属性的 `<g class="part">`，无需改动任何脚本**。
- 交互行为（悬停高亮、点击详情、冲突标红、原始属性回显）由模板内固定脚本提供。

## 2. data-* 属性表

| 属性 | 必填 | 说明 | 示例 |
|---|---|---|---|
| `data-category` | 是 | 元件分类，取值必须是第 3 节枚举之一 | `mcu` |
| `data-name` | 是 | 元件名称（型号/名称） | `CH32V307VCT6` |
| `data-desc` | 是 | 功能描述，包含型号与关键参数 | `青稞 V4F 内核, 144MHz, 256KB Flash + 64KB SRAM` |
| `data-pins` | 建议 | 相关引脚清单，逗号分隔，格式 `功能(PIN)` | `UART7_TX(PC2), UART7_RX(PC3), AT=PA7` |
| `data-conflict` | 建议 | 引脚冲突说明；**无冲突必须写 `无`**（否则会被脚本误判为冲突） | `与以太网模块共用部分 I2S/I2C 引脚` |

> `data-conflict` 缺省或值为 `无` 时，面板不显示红色"冲突"标签。多引脚并列时建议遵循「单引脚组用逗号、键值用 `=`」的写法，保持 `data-pins` 中英文半角逗号分隔。

## 3. 分类枚举（10 类默认）

| category | 中文 | CSS 变量 | 默认颜色 |
|---|---|---|---|
| `mcu` | 主控 | `--cat-mcu` | `#8a8a8a` |
| `display` | 显示 | `--cat-display` | `#5a9fd4` |
| `sensor` | 传感器 | `--cat-sensor` | `#5ad49f` |
| `wireless` | 无线 | `--cat-wireless` | `#d4c85a` |
| `storage` | 存储 | `--cat-storage` | `#d49f5a` |
| `audio` | 音频 | `--cat-audio` | `#d45a8a` |
| `input` | 按键 | `--cat-input` | `#9aa0aa` |
| `debug` | 调试 | `--cat-debug` | `#d45a5a` |
| `interface` | 接口 | `--cat-interface` | `#5ab4d4` |
| `camera` | 摄像头 | `--cat-camera` | `#b45ad4` |

## 4. 新增分类（三步同步）

若某板卡需要默认 10 类之外的分类，必须**同步修改三处**，否则图例/标签/颜色会不一致：

1. **CSS**：`:root` 中新增 `--cat-新分类: 颜色值;`
2. **JS**：`categoryLabel()` 映射表中新增 `新分类:'中文名'`
3. **图例**：底部 `.legend` 中新增 `<span><i style="background:var(--cat-新分类)"></i>中文名</span>`

之后元件即可使用 `data-category="新分类"`。

## 5. 数据来源与校验（重要）

引脚数据的准确性是页面价值所在，必须遵守：

1. **以官方资料为准**：优先使用官方原理图、引脚分配表、数据手册；其次才是社区资料与实物丝印。
2. **冲突标注**：同一引脚被多个外设复用（如 I2C 总线、SDIO 与 DVP 共用数据线）时，必须在**每个相关元件**的 `data-conflict` 中互相标注，且措辞一致。
3. **交叉核对**：绘制完成后，将每个元件的 `data-pins` 与官方引脚表逐条比对；发现不一致时以官方资料为准并修正。
4. **示例校验命令**（任选）：
   ```bash
   # 统计元件数与分类分布
   grep -o 'data-category="[^"]*"' <板卡>_board.html | sort | uniq -c
   # 找出缺少 data-name 的元件
   grep -c 'class="part"' <板卡>_board.html
   ```
5. **预览**：`python3 -m http.server 8900` 后浏览器访问对应 HTML。

## 6. 一个完整元件示例

```html
<g class="part" data-category="wireless" data-name="BLE 模组" data-desc="蓝牙串口透传, 主从一体"
   data-pins="UART7_TX(PC2), UART7_RX(PC3), AT=PA7, SLEEP=PC13" data-conflict="无">
  <rect x="235" y="30" width="80" height="52" rx="4" fill="#141a14" stroke="#d4c85a" stroke-width="1.6"/>
  <text x="275" y="50" text-anchor="middle" fill="#d4c85a" font-size="9" font-weight="600">BLE</text>
</g>
```

## 7. 多面视图切换（正面/反面）

板卡正反面元件分开（如屏幕在正面、接口/芯片在背面）时，拆分为多个 `<g class="face">` 视图组：

- 视图组外层用 `<g id="face-front" class="face">`（默认显示）、`<g id="face-back" class="face" style="display:none">`，组名规则为 `face-<视图名>`。
- 板框、`defs`、安装孔等共用元素放在视图组**外**。
- 切换按钮（`#btnFront` / `#btnBack`）与 JS `switchFace()` 逻辑在模板中已内置，无需修改。
- 元件归属按物理位置划分：正面的元件放 `face-front`，背面的放 `face-back`。
- 单面板卡可直接删除 `.face-switch` 按钮、`<g class="face">` 包裹层与 JS 中的切换段。

已落地示例：`ESP32-2432S0248R-PLUS/esp32_2432s0248r_plus_board.html`（正面：LCD + 触摸面板；反面：模组、TF、接口等 13 个元件）。

## 9. SVG 手绘立体效果规范

**纯 HTML/SVG 手绘，不嵌入照片**。参照实物照片的布局与质感，用渐变 + 阴影 + 高光模拟立体。

### 9.1 defs 必备滤镜与渐变

```html
<filter id="shadow" ...>      <!-- 大投影: 模组/卡座等大元件 -->
<filter id="softShadow" ...>  <!-- 小投影: 按钮/接口/芯片 -->
<linearGradient id="pcbGrad">    <!-- 板身: 上亮下暗 -->
<linearGradient id="metalGrad">  <!-- 金属: 亮→中灰→暗 -->
<linearGradient id="chipGrad">   <!-- 芯片: 深灰→黑 -->
<radialGradient id="btnGrad">    <!-- 按钮凸起: 左上亮右下暗 -->
<linearGradient id="glassGrad">  <!-- 屏幕玻璃反光: 对角渐隐 -->
```

### 9.2 板身立体（厚度感）

```html
<!-- ① 厚度层: 偏移 3px 的暗色 rect -->
<rect x="23" y="24" width="660" height="560" rx="18" fill="#0b0d11"/>
<!-- ② PCB 主面 -->
<rect x="20" y="20" width="660" height="560" rx="18" fill="url(#pcbGrad)" stroke="#3a3f4a" stroke-width="1.5"/>
<!-- ③ 顶部环境光 -->
<rect x="20" y="20" width="660" height="70" rx="18" fill="rgba(255,255,255,.045)"/>
```

### 9.3 各元件立体画法（2~3 层图形叠加）

| 元件类型 | 底层 | 主体 | 高光/细节 |
|---|---|---|---|
| 芯片 (IC) | 深色底座+阴影 | `chipGrad` + 顶排金属引脚 | 左上白色高光椭圆 + 型号文字 + 圆点标记 |
| 金属屏蔽罩 (Wi-Fi 模组) | 底部黑色投影 | `metalGrad` + 描边 | 顶部亮条 + 两侧暗部 + 激光雕刻文字 + 天线蛇形线 |
| 按键 | 凹槽底座(深色) | `btnGrad` 径向凸起 | 顶部高光椭圆 + 下方丝印名 |
| 白色接口/排针 | 底座+阴影 | 白底 `#dcdce0` | 顶部亮条 + 深色针脚竖条 |
| 金属接口 (USB-C/TF) | 底座+阴影 | `metalGrad` | 顶部亮条 + 深色插口 + 内部触点 |
| LED | 深色底 | 发光圆点 | 同色半透明光晕 + 引脚标注 |
| 屏幕 | 金属边框+阴影 | 玻璃渐变色 | 顶部亮条 + 文字 + 底部排线口 |

### 9.4 交互热点结构（手绘模式）

```html
<g class="part" data-category="mcu" data-name="ESP32-WROOM-32E"
   data-desc="..." data-pins="..." data-conflict="...">
  <!-- 视觉图形: 必须 pointer-events="none", 不挡点击 -->
  <rect x="480" y="120" width="178" height="218" rx="6" fill="url(#metalGrad)" ... pointer-events="none"/>
  ...
  <!-- 交互层: .hit 透明命中区 + .outline 高亮描边 -->
  <rect class="outline" x="480" y="120" width="178" height="218" rx="6" stroke="#8a8a8a"/>
  <rect class="hit" x="480" y="120" width="178" height="218" rx="6"/>
</g>
```

- `.hit` 平时透明，hover 时 `fill:rgba(255,255,255,.10)`、选中时 `.20`；`.outline` 平时 `opacity:0`，hover/选中显示分类色描边。
- 视觉图形一律 `pointer-events="none"`，只让 `.hit` 参与命中；`text` 同理。
- 拾取顺序：同一 face 内后画的在顶层，重叠时后画的优先被点中。

已落地示例：`ESP32-2432S0248R-PLUS/esp32_2432s0248r_plus_board.html`（反面 13 个元件全部 SVG 手绘立体 + 热点，正面 LCD 玻璃反光）。

## 8. 参考实现

- 已落地示例：`CH32V307/chitu_board.html`（赤菟 CH32V307 开发板，21 个元件）
- 元件明细表参考：`CH32V307/example/README.md` 的「1.3 交互式引脚图」章节
