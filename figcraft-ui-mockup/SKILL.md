---
name: figcraft-ui-mockup
description: 用 FigCraft（figcraft-cli）把软件界面、截图或源码还原成可编辑的 .figcraft 设计稿。触发词：用 FigCraft 画界面、把 UI 画出来、还原这个界面/截图、生成 .figcraft、界面设计稿、figcraft。内置强制结构：一屏一个 Page、共用外壳做成组件实例、禁止把多屏塞进同一页。
---

# FigCraft 界面还原

把一款软件（或几张截图）画成 FigCraft 设计稿：Python 生成脚本 → figcraft-cli 执行 → 导出 PNG 自检 → 交付 .figcraft + PNG + 脚本。

## 0. 三条硬约束（开工前先默读，违反就是返工）

1. **一屏一个 Page。**
   一个屏幕 = 一个 Page = 一个 `SCR-<屏幕名>` 顶层 frame。
   **禁止**把两个画板用 y 偏移并排放进同一页（`y=0` 和 `y=880` 那种），也禁止一页里放多屏。
2. **共用外壳只做一份。**
   顶栏、侧栏、标题栏、状态栏、按钮、导航选中态 → 全部放在 `组件` 页做成 component，每屏放一个 instance。
   **禁止**逐屏复制粘贴同一批图层（两屏复制一遍顶栏 = 200 个重复节点 + 改文案漏改）。
3. **内容层挂在 0,0 全屏透明 frame 上。**
   屏幕 frame 的子层顺序：外壳实例 → `内容` 容器（`x=0,y=0,w=屏宽,h=屏高, fill=none`）→ 具体内容。
   内容坐标直接写屏幕绝对坐标，不做相对换算，这样从截图量出来的坐标能直接抄。

## 1. 准备：先有事实，再画

| 来源 | 要取什么 |
|---|---|
| Qt Widgets 源码（`mainwindow.cpp`） | `resize()` 窗口尺寸、每个控件的绝对坐标与尺寸、标题栏文案、QSS 配色、字号 |
| QML / kiosk | root 的 `width/height`、颜色常量、导航项数组、字号 |
| 截图 | 直接用像素量比例（先确定基准宽度，再按比例折算） |
| 项目总结文档 | 页面清单、功能点、示例数据（IP、版本号、内核串） |

**不要凭感觉编尺寸**——窗口宽高、栏宽、行高都要有出处；数值、日志、IP 这类示例数据可以编，但要在交付时说明。

工具入口（无 MCP 时直接驱动 CLI）：

```bash
/usr/bin/figcraft-cli commands          # 列全部命令
/usr/bin/figcraft-cli run x.json --out x.figcraft
/usr/bin/figcraft-cli info x.figcraft --json
/usr/bin/figcraft-cli export x.figcraft -o png --page "系统概览" --scale 2
```

## 2. 脚本骨架（照这个顺序写）

```python
import sys
sys.path.insert(0, "<本 skill 目录>/assets")
import figbase as F
from figbase import (rect, frame, text, vec, rtext, est_width, CUR)

# ---- 1) 组件页：复用文档自带空白页，改名「组件」（不这么做会多出一个空 Page）
F.begin()

def draw_topbar(p):                     # 组件内只放一个文本子层（见 §6）
    ...
TOP  = F.make_component("Chrome / 顶栏", 1280, 64, draw_topbar)
SIDE = F.make_component("Chrome / 侧栏", 208, 736, draw_sidebar, fill="#101821")

# ---- 2) 每屏一个 Page
P1 = F.page("系统概览", "P1")
C1 = F.screen(P1, "系统概览", 1280, 800,
              parts=[(TOP, 0, 0, "顶栏"), (SIDE, 0, 64, "侧栏")])
CUR[0] = C1                             # 之后的图元默认落在内容容器里
text("系统概览", 236, 88, 23, "#EEF4FA", "Bold")

P2 = F.page("NPU YOLO", "P2")
C2 = F.screen(P2, "NPU YOLO", 1280, 800,
              parts=[(TOP, 0, 0, "顶栏"), (SIDE, 0, 64, "侧栏"),
                     (NAV_NPU, 12, 404, "导航选中态")])
CUR[0] = C2
...

# ---- 3) 落地 + 自检
js = F.dump("boardlab.json")
print(F.run(js, "boardlab-ui.figcraft")[0])      # True = 全部步骤 ok
print(F.audit("boardlab-ui.figcraft"))           # 页数 / 每页 SCR 数 / 缺字体
```

`F.screen()` 已经封装好：切页 → 建 `SCR-<名>` frame → 依次粘贴外壳实例 → 建 `内容` 容器并返回引用。

## 3. 命名规范

| 前缀 | 用途 | 例 |
|---|---|---|
| `SCR-<屏幕名>` | 屏幕 frame（与 Page 同名） | `SCR-BoardLab · 系统概览` |
| `Chrome / *` | 全局外壳组件 | `Chrome / 顶栏` |
| `Nav / 选中 · <项>` | 导航高亮态组件 | `Nav / 选中 · NPU` |
| `Button / <风格>` | 按钮组件 | `Button / Qt 默认` |
| `卡片 / *` | 内容面板 | `卡片 / 设备状态` |
| `磁贴-*` / `按钮-*` | 实例 | `磁贴-按键检测` |
| `内容` | 屏幕内容容器 | — |

## 4. 导出与自检（**必做，不能跳**）

```bash
# 逐页导出；不带 --page 只会导出当前页，多屏会漏图
/usr/bin/figcraft-cli export x.figcraft -o png --page "系统概览" --scale 2
/usr/bin/figcraft-cli export x.figcraft -o png --page "NPU YOLO" --scale 2
```

然后**看图**，不要只看命令返回码：

1. 用 Read 打开导出的 PNG，确认布局没有塌、文本没被裁掉。
2. 细节看不清就裁剪放大：

```python
from PIL import Image
im = Image.open("png/SCR-系统概览.png")     # 2x 图，坐标记得乘 2
im.crop((0, 0, 1300, 400)).save("c.png")
```

3. 跑 `F.audit()`：页数应为「屏数 + 1」，每页恰好 1 个 `SCR-`，`missingFonts` 为空。

**常见返工点**：元素消失（parent 没给，挂到页面上去了）、文本错位（该右对齐却用了左对齐）、文字超框（没估宽）、组件实例里文案没改（子层混了非文本层）。

## 5. 交付

```
<project>/
├── gen_<name>.py            # 可改参数重生成的脚本
├── <name>.json              # 生成的 CLI 脚本（调试用）
├── <name>.figcraft          # 设计稿，可直接用 FigCraft 打开
└── png/<name>@2x.png        # 每屏一张预览
```

收尾时说明：哪些数据来自源码、哪些是编造的示例值；哪些面板刻意没做成组件及原因。

## 6. 必踩的坑（细节见 references/figcraft-cli.md）

- **只有 frame 能装子图层**。矩形当容器会报 `can't contain layers`，要用 `node.create` + `type:"frame"`（基座里的 `frame()`）。
- **`parent` 省略 = 挂到页面上**，导出单页时就会“消失”。基座用 `CUR[0]` 兜底，但仍建议显式传。
- **渐变写 `fills:[{...}]`**，写 `fill` 无效。
- **组件内只留一个文本子层**。`instance(label=...)` 靠 `select.children` 一次性选中所有子层，混进矩形就报 `node N is not text`。所以按钮的底色/描边要画在组件根 frame 上。
- **`edit.paste` 的 x/y 是页面绝对坐标**，不是父级相对坐标。
- **`page.select` 只认 `{id}` / `{index}`**，不认 name。
- **数字写法**：脚本里 `page.select` 用 `{"id": {...}}`；`$ref` 只能引用步骤的 `id` 字段，取数组元素（`ids[0]`）会报错——想改实例内容就走「paste 后实例被选中 → `select.children` → `node.set`」。

## 参考文件

- `assets/figbase.py` — 基座：图元、组件、实例、屏幕骨架、run/export/audit
- `references/figcraft-cli.md` — 命令与脚本语法速查 + 踩坑记录
- `references/layout-recipes.md` — 深色 kiosk / 浅色 Qt 两套配色与面板尺寸配方、图标 path 库
- `examples/demo_two_screens.py` — 最小两屏示例，跑通即代表基座可用
