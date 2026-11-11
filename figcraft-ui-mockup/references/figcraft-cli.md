# figcraft-cli 速查与踩坑

CLI：`/usr/bin/figcraft-cli`（无 MCP 工具时直接用它；有 `mcp__figcraft__*` 时优先用 MCP，语义一致）。

## 命令

```bash
figcraft-cli commands                            # 全部命令 + 参数签名
figcraft-cli run script.json --out x.figcraft    # 执行脚本，逐条返回 {"ok":true,...}
figcraft-cli run script.json --in x.figcraft     # 在已有文档上继续执行
figcraft-cli info x.figcraft                     # 节点/页面树
figcraft-cli info x.figcraft --json              # 程序可读（含 missingFonts）
figcraft-cli export x.figcraft -o 目录 --page "页名" --scale 2
figcraft-cli export x.figcraft -o 目录 --node "SCR-xxx" --scale 2
```

脚本是一个 JSON 数组，每项 `{"command": ..., "params": {...}, "as": "别名"}`：

- `as` 给这一步留名，后续用 `{"$ref": "别名"}` 引用（引用的是该步结果的 `id`）。
- 任一步失败 → `{"ok":false,...}`；默认整批回滚（`rolledBack: true`），不会留下半成品。
- 写脚本用 Python 生成 JSON（`json.dump`），别手写上百行 JSON。

## 常用命令

| 命令 | 参数 | 说明 |
|---|---|---|
| `page.add` | `{name}` | 新建页（名字以 `-` 开头会变成分隔条） |
| `page.select` | `{id}` 或 `{index}` | **不认 name** |
| `page.rename` | `{id?, name}` | 省略 id 改当前页 |
| `page.delete` | `{id?}` | 删除当前页 |
| `page.list` | `{}` | 列页 |
| `frame.create` | `{x,y,width,height,name,props}` | 建 frame（推荐用它，而不是 `node.create`） |
| `node.create` | `{type:"frame", x,y,width,height,props}` | 建任意节点 |
| `shape.rectangle` | `{x,y,width,height,parent,props}` | 矩形（**不能装子层**） |
| `text.create` | `{text,x,y,width?,parent,props}` | 文本 |
| `vector.create` | `{path,x,y,width,height,parent,props}` | 矢量图标，24×24 viewBox 的 path |
| `component.create` | `{ids:[...]}` | 把图层合并成主组件 |
| `edit.copy` / `edit.paste` | `{ids}` / `{parent,x,y}` | 复制组件 → 粘贴为实例；**x/y 是页面绝对坐标** |
| `edit.duplicate` | `{ids,dx,dy}` | 直接复制（返回 `{ids:[...]}`，取不到 ref，改用 copy+paste） |
| `select.children` / `select.none` | `{}` | 选中实例全部子层 / 清空选择 |
| `node.set` | `{ids?, characters?, x?, y?}` | 改文本内容或坐标 |
| `node.reparent` | `{ids, parent}` | 换父级 |
| `object.rename` | `{name}` | 给当前选中项改名 |

## 属性（props）

```jsonc
{
  "fill": "#151D26",                  // 纯色
  "fills": [{"type":"linearGradient", // 渐变只能写这里，写 fill 无效
             "stops":["#2DD4BF","#0E9488"],
             "from":[0,0], "to":[1,1]}],
  "stroke": "#212C38", "strokeWeight": 1, "strokeAlign": "inside",
  "cornerRadius": 14,
  "opacity": 0.85,
  "fontSize": 12.5, "fontFamily": "Noto Sans CJK SC",
  "fontStyle": "Regular | Medium | Bold",     // 是 fontStyle，不是 fontWeight
  "letterSpacing": 0.4, "textAlign": "left|center|right",
  "textAutoResize": "height", "textAlignVertical": "top"   // 给 width 时配套用
}
```

字体（本机已装）：`Noto Sans CJK SC`（正文/标题，Medium 当半粗）、`Noto Sans Mono CJK SC`（版本号、路径、数值）。

## 踩坑清单

1. **只有 frame / section / group 能包含子图层。** 矩形当容器 → `… can't contain layers`。
2. **`parent` 省略 = 挂到页面根。** 症状：单页导出时这部分“消失”。基座里 `CUR[0]` 是兜底父级，但显式传更稳。
3. **`$ref` 只能取步骤结果里的 `id`。** `{"$ref":"x","field":"ids[0]"}` → `result has no 'ids[0]'`。要拿 paste/duplicate 出来的实例，只能靠「粘贴后它自动被选中 → `select.children` / `node.set`」这条链。
4. **`edit.paste` 的 x/y 是页面坐标**，不是相对 parent 的坐标（实测 absoluteBounds 等于传入值）。
5. **`select.children` 一次选中所有子层。** 组件里有矩形 + 文本时，`node.set {characters}` 会报 `node N is not text`。所以：**按钮类组件把底色/描边/圆角画在根 frame 上，只留一个文本子层**。
6. **多文本面板别做组件。** KPI 卡、参数卡这种 4+ 个文本层 + 各自不同进度条的，实例覆盖机制表达不了，做成独立 frame + 规范命名即可（真要组件化留给人在 FigCraft 界面里做）。
7. **`make_component` 前必须重置当前父级**（基座里 `CUR[0]=None`），否则下一个组件 frame 会建进上一个组件里。
8. **导出要带 `--page`**，否则只导出当前页；文件名取的是 frame 名（`SCR-xxx.png`），带空格/点号也没关系。
9. **`export` 会把组件页也导成图**（`C-xxx.png`），只要屏幕图就按页导。
10. **2x 图坐标翻倍**：从截图裁剪定位时，图上的坐标是设计坐标 × scale。
11. **字体粗细靠 `fontStyle`**，写 `fontWeight: 600` 不生效。
12. **渐变方向**：`from`/`to` 用 0~1 的相对坐标，竖直渐变是 `from:[0,0] to:[0,1]`。
