---
name: devboard-pinout
description: 为开发板生成「HTML + SVG + data 属性」交互式引脚图。当用户想为某块开发板/核心板创建可点击查看元件与引脚详情的可视化页面（如"给XX板做个引脚图"、"板卡资源查询页"、"交互式引脚图"）时使用。工作流：收集官方引脚资料 → 复制模板 → 绘制 SVG 板卡 → 为每个元件添加带 data-* 属性的元件分组 → 校验数据与官方引脚表一致 → 本地预览。
---

# 交互式引脚图生成

## Overview

用单个静态 HTML 文件呈现开发板板卡：**纯 SVG 手绘板卡与元件**（渐变 + 阴影 + 高光模拟立体，不嵌入图片），每个元件通过 `data-*` 属性携带名称/分类/引脚/冲突信息，点击即可查看详情。零依赖、无后端，数据全部内联在 HTML 中，新增元件只需追加一个 `<g class="part">`。支持正面/反面双视图切换。

## 工作流程

### Step 1: 收集板卡资料（确定权威数据源）

在动手前先定位以下资料，引脚数据必须以官方资料为准：

1. 官方原理图 / 引脚分配表 / 数据手册（最高优先级）
2. 板卡实物照片或官方渲染图（用于绘制 SVG 布局）
3. 社区整理的引脚表（仅作参考，需与官方交叉核对）

若项目内已有该板卡的 README 或文档，优先读取其中的引脚分配章节。

### Step 2: 复制模板到目标目录

```bash
cp .codebuddy/skills/devboard-pinout/assets/pinout-template.html <板卡目录>/<板卡名>_board.html
```

命名规范：`<板卡名>_board.html`，如 `chitu_board.html`、`esp32s3_board.html`。

### Step 3: 替换占位符

替换模板中的占位符（可用 `replace_all`）：

| 占位符 | 说明 | 示例 |
|---|---|---|
| `__TITLE__` | 浏览器标签页标题 | `赤菟 CH32V307 开发板 · 交互式引脚图` |
| `__BOARD_NAME__` | 板卡名 | `赤菟` |
| `__CHIP__` | 主控芯片型号 | `CH32V307` |

### Step 4: 绘制 SVG 板卡（手绘立体效果）

**全部用 SVG 手绘，不嵌入照片/图片**。参照板卡实物照片的布局与质感，用渐变、阴影、高光等绘制技巧表现立体感（详见 data-spec.md 第 9 节）：

1. 调整板框 `rect` 的位置、尺寸、圆角以匹配实际板卡长宽比；用厚度层（偏移 3px 的暗色 rect）+ 顶部环境光制造板身厚度感。
2. 保留 `defs`：发光滤镜、`pcbGrad` 板身渐变、`metalGrad` 金属渐变、`chipGrad` 芯片渐变、`btnGrad` 按钮凸起渐变、`shadow`/`softShadow` 投影滤镜。
3. 按元件在板上的**实际相对位置**绘制，尽量保持布局相似；每个元件用 2~3 层图形模拟立体：底层深色阴影、主体渐变、顶部高光。
   - 芯片：深色主体 + 顶部金属引脚 + 左上白色高光椭圆 + 型号文字
   - 金属屏蔽罩（Wi-Fi 模组）：金属渐变 + 顶部亮条 + 侧边暗部 + 激光雕刻文字
   - 按键：凹槽底座 + 径向渐变凸起 + 顶部高光椭圆
   - 接口/排针：白色塑料底座 + 顶部亮条 + 深色金属针脚
   - LED：发光圆点 + 同色半透明光晕
4. 图形配色建议：元件底色 `fill` 用深色（`#14161a` 系），描边 `stroke` 用该分类的默认颜色（见 data-spec.md 第 3 节）。
5. **交互热点**：每个 `<g class="part">` 内含 `.hit` 透明交互区 + `.outline` 高亮描边（hover/选中时显示），视觉图形本身设 `pointer-events="none"` 避免干扰命中。
6. **多面视图（可选）**：正反面元件分开的板卡，拆为 `<g id="face-front" class="face">` 与 `<g id="face-back" class="face" style="display:none">` 两个视图组（板框/defs/安装孔放组外共用），切换按钮与 JS 已内置，无需改脚本；单面板卡忽略此项。

### Step 5: 为每个元件添加 `<g class="part">`

按 `references/data-spec.md` 的规范，为每个板载元件添加：

```html
<g class="part" data-category="mcu" data-name="CH32V307VCT6"
   data-desc="青稞 V4F 内核, 144MHz, 256KB Flash + 64KB SRAM"
   data-pins="LQFP100, 全部 GPIO 可复用" data-conflict="部分外设引脚冲突, 详见各模块">
  <rect x="230" y="280" width="120" height="120" rx="3" fill="#0d0d10" stroke="#8a8a8a" stroke-width="1.8"/>
  <text x="290" y="320" text-anchor="middle" fill="#aaa" font-size="11" font-weight="600">CH32V307</text>
</g>
```

要点：

- `data-category` 必须是规范中的 10 个枚举值之一；需要新分类时按 data-spec.md 第 4 节**同步修改三处**（CSS 变量、categoryLabel 映射、图例）。
- `data-conflict` 无冲突时写 `无`。
- 新增元件**不要修改 `<script>` 部分**，脚本自动适配。
- 板卡上没有的分类，可删除对应 CSS 变量与图例项。

### Step 6: 校验

1. 每个元件都有完整的 `data-category` / `data-name` / `data-desc`。
2. 逐条将 `data-pins` 与官方引脚表比对，发现不一致以官方为准修正（这是最容易出错、也最重要的一步）。
3. 复用的引脚（I2C 总线、SDIO/DVP 冲突等）在相关元件的 `data-conflict` 中互相标注。
4. 运行 `grep -o 'data-category="[^"]*"' <板卡名>_board.html | sort | uniq -c` 检查分类分布，确认没有拼写错误的分类值。

### Step 7: 本地预览

```bash
cd <板卡目录> && python3 -m http.server 8900
```

浏览器访问 `http://localhost:8900/<板卡名>_board.html`，逐个点击元件验证详情渲染。

### Step 8:（可选）整理进项目 README

将元件明细（元件/分类/功能/引脚/冲突）整理为表格，写入该板卡的 `example/README.md`，并在表格前注明"新增元件只需在 HTML 中追加 `<g class="part">` 带完整 data 属性即可自动接入"，保持 HTML 与 README 数据一致。

## Resources

- `assets/pinout-template.html` —— 通用模板：完整交互框架（CSS + SVG 骨架 + JS）+ 两个示例元件，复制后替换占位符即可开工。
- `references/data-spec.md` —— 属性规范：data-* 属性表、10 类枚举、新增分类三步同步、数据来源与校验要求、完整元件示例。
- 参考实现：`CH32V307/chitu_board.html`（赤菟 CH32V307，21 元件）+ `CH32V307/example/README.md` 明细表。
