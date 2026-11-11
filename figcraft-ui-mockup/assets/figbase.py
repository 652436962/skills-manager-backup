#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""figbase —— 用 Python 写 figcraft-cli 脚本的基座。

把枯燥的 ``{"command": ..., "params": ...}`` 包装成 rect/text/vec/component/instance，
并把本项目的**结构规范**固化成函数签名：

  * 一屏一个 Page（``page()`` + ``screen()``）
  * 屏幕 frame 命名 ``SCR-<屏幕名>``，页名与屏幕名相同
  * 共用外壳放 `组件` 页，做成 component，每屏只放一个 instance
  * 内容层挂在 0,0 全屏透明 frame 上，坐标直接写屏幕绝对坐标

典型脚本：

    from figbase import *
    import figbase

    P1 = page("系统概览", "P1")
    C  = screen(P1, "系统概览", 1280, 800, parts=[("顶栏实例", TOP, 0, 0)])
    text("系统概览", 236, 88, 23, "#EEF4FA", "Bold")
    figbase.dump("out.json")
    figbase.run("out.json", "out.figcraft")
"""

import json
import subprocess

# ------------------------------------------------------------------ 全局状态
S = []          # 步骤列表
_c = [0]        # 自动 id 计数
CUR = [None]    # 当前默认父级（None = 页面）
CLI = "/usr/bin/figcraft-cli"

UI = "Noto Sans CJK SC"
MONO = "Noto Sans Mono CJK SC"

# 深色底（板端 kiosk / 工业风），浅色主题请在脚本里自行覆盖
BG     = "#0E131A"
PANEL  = "#151D26"
LINE   = "#212C38"
TXT    = "#E9EFF6"
TXT2   = "#8A97A6"
TXT3   = "#5D6A79"
ACCENT = "#2DD4BF"


def aid(prefix="e"):
    _c[0] += 1
    return "%s%d" % (prefix, _c[0])


# ------------------------------------------------------------------ 基础图元
def rect(x, y, w, h, parent=None, fill=None, radius=0, stroke=None, sw=1,
         name=None, asname=None, opacity=None, grad=None, is_frame=False):
    """矩形。is_frame=True 时是 frame（唯一能装子图层的容器）。"""
    props = {"cornerRadius": radius}
    if grad:
        props["fills"] = [grad]          # 渐变必须放 fills，放 fill 无效
    else:
        props["fill"] = fill if fill else "none"
    if stroke:
        props["stroke"] = stroke
        props["strokeWeight"] = sw
        props["strokeAlign"] = "inside"
    if opacity is not None:
        props["opacity"] = opacity
    if parent is None:
        parent = CUR[0]
    p = {"x": x, "y": y, "width": w, "height": h, "props": props}
    if name or asname:
        p["name"] = name or asname
    if parent:
        p["parent"] = parent
    if is_frame:
        p["type"] = "frame"
        cmd = {"command": "node.create", "params": p}
    else:
        cmd = {"command": "shape.rectangle", "params": p}
    if asname:
        cmd["as"] = asname
    S.append(cmd)
    return {"$ref": asname} if asname else None


def frame(x, y, w, h, name, fill=None, radius=0, stroke=None, asname=None,
          parent=None, sw=1, grad=None):
    return rect(x, y, w, h, parent, fill, radius, stroke, sw=sw, name=name,
                asname=asname, grad=grad, is_frame=True)


def text(t, x, y, size=12, color=TXT, weight="Regular", family=UI,
         parent=None, ls=None, align=None, w=None, asname=None, name=None):
    """文本。给了 w 就走自动高度 + 指定宽度，align 生效。"""
    props = {"fontSize": size, "fontFamily": family, "fontStyle": weight, "fill": color}
    if ls is not None:
        props["letterSpacing"] = ls
    if align:
        props["textAlign"] = align
    if parent is None:
        parent = CUR[0]
    p = {"text": t, "x": x, "y": y, "props": props}
    if w:
        p["width"] = w
        props["textAutoResize"] = "height"
        props["textAlignVertical"] = "top"
    if name:
        p["name"] = name
    if parent:
        p["parent"] = parent
    cmd = {"command": "text.create", "params": p}
    if asname:
        cmd["as"] = asname
    S.append(cmd)
    return {"$ref": asname} if asname else None


def vec(path, x, y, size=16, parent=None, stroke=None, sw=1.4, fill=None, name=None):
    """矢量图标：24×24 viewBox 的 SVG path 字符串。"""
    props = {"stroke": stroke or ACCENT, "strokeWeight": sw, "strokeCap": "round",
             "strokeJoin": "round", "fill": fill if fill else "none"}
    if parent is None:
        parent = CUR[0]
    p = {"path": path, "x": x, "y": y, "width": size, "height": size, "props": props}
    if name:
        p["name"] = name
    if parent:
        p["parent"] = parent
    S.append({"command": "vector.create", "params": p})


# ------------------------------------------------------------------ 文本度量
def est_width(t, size, mono=False):
    """粗估文本宽度：CJK 按 1chars，西文按 0.52（等宽 0.60）。右对齐必用。"""
    w = 0.0
    for ch in t:
        w += (1.0 if ord(ch) > 0x2E80 else (0.60 if mono else 0.52)) * size
    return w


def rtext(t, rx, y, size=9.5, color=None, weight="Regular", family=UI, parent=None):
    """右对齐文本：给右边界 rx，自动算宽度。"""
    w = est_width(t, size, mono=(family == MONO)) * 1.08 + 4
    text(t, rx - w, y, size, color or TXT3, weight, family, parent,
         align="right", w=w)


# ------------------------------------------------------------------ 页面
def begin(components_page="组件"):
    """复用文档自带的空白首页，改名成组件页，避免多出一个空 Page。"""
    S.append({"command": "page.select", "params": {"index": 0}})
    S.append({"command": "page.rename", "params": {"name": components_page}})
    return {"index": 0}


def page(name, asname=None):
    cmd = {"command": "page.add", "params": {"name": name}}
    if asname:
        cmd["as"] = asname
    S.append(cmd)
    return {"$ref": asname} if asname else None


def go_page(ref):
    """切页：只接受 {id} 或 {index}，不接受 name。"""
    S.append({"command": "page.select", "params": {"id": ref}})


# ------------------------------------------------------------------ 组件 / 实例
def make_component(comp_name, w, h, draw, x=0, y=0, fill=None, radius=0,
                   stroke=None, sw=1, grad=None):
    """在**当前页**（应为 `组件` 页）建一个主组件，返回可复制的引用。

    外壳的底色/描边/圆角直接画在组件根 frame 上（fill / grad / stroke），
    draw(ref) 里**只放一个文本子层**——因为 instance(label=...) 走的是
    `select.children`，子层里混进矩形就会报 `node N is not text`。
    """
    asn = "C-" + comp_name
    CUR[0] = None                     # 必须重置，否则组件会嵌进上一个组件
    frame(x, y, w, h, comp_name, fill, radius, stroke, sw=sw, grad=grad,
          asname=asn)
    ref = {"$ref": asn}
    CUR[0] = ref
    draw(ref)
    S.append({"command": "component.create", "params": {"ids": [ref]},
              "as": asn + "#main"})
    return {"$ref": asn + "#main"}


def instance(comp, parent, x, y, label=None, name=None):
    """把主组件复制粘贴成实例。注意：paste 的 x/y 是**页面绝对坐标**。"""
    S.append({"command": "edit.copy", "params": {"ids": [comp]}})
    S.append({"command": "edit.paste", "params": {"parent": parent, "x": x, "y": y}})
    if name:
        S.append({"command": "object.rename", "params": {"name": name}})
    if label is not None:
        S.append({"command": "select.children", "params": {}})
        S.append({"command": "node.set", "params": {"characters": label}})
    S.append({"command": "select.none", "params": {}})


# ------------------------------------------------------------------ 屏幕骨架
def screen(pg_ref, name, w=1280, h=800, fill=None, parts=(), content=True):
    """建一屏：切页 → SCR-<name> frame → 放外壳实例 → 建 `内容` 容器。

    parts: [(组件引用, x, y, 实例名), ...]，坐标为屏幕内绝对坐标。
    content=True 时返回 0,0 全屏透明 frame 作为后续内容的父级。
    """
    go_page(pg_ref)
    CUR[0] = None
    asn = "SCR-" + name
    frame(0, 0, w, h, asn, fill or BG, asname=asn)
    scr = {"$ref": asn}
    CUR[0] = scr
    for item in parts:
        comp, px, py = item[0], item[1], item[2]
        iname = item[3] if len(item) > 3 else None
        instance(comp, scr, px, py, name=iname)
    if not content:
        return scr
    frame(0, 0, w, h, "内容", None, asname=asn + "-content")
    return {"$ref": asn + "-content"}


# ------------------------------------------------------------------ 执行 / 校验
def dump(path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(S, f, ensure_ascii=False, indent=1)
    return path


def run(json_path, fig_path, cli=None, quiet=True):
    """跑脚本并检查是否有失败步骤；返回 (ok, 失败输出)。"""
    cli = cli or CLI
    proc = subprocess.run([cli, "run", json_path, "--out", fig_path],
                          capture_output=True, text=True)
    bad = [ln for ln in proc.stdout.splitlines() if '"ok":true' not in ln and ln.strip()]
    ok = proc.returncode == 0 and not bad
    if not ok and not quiet:
        print("[figcraft] 失败步骤:\n" + "\n".join(bad[:10]))
    return ok, bad


def export(fig_path, out_dir, page_name=None, scale=2, cli=None):
    cli = cli or CLI
    cmd = [cli, "export", fig_path, "-o", out_dir, "--scale", str(scale)]
    if page_name:
        cmd += ["--page", page_name]
    return subprocess.run(cmd, capture_output=True, text=True)


def info(fig_path, cli=None, as_json=True):
    cli = cli or CLI
    cmd = [cli, "info", fig_path] + (["--json"] if as_json else [])
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    if not as_json:
        return out
    try:
        return json.loads(out)
    except ValueError:
        return {"pages": [], "missingFonts": [], "raw": out}


def audit(fig_path):
    """校验结构：返回 (ok, 报告文本)。硬约束同页多屏、缺字体都在这里抓。"""
    d = info(fig_path)
    pages = d.get("pages", [])
    lines, ok = [], True
    scr_pages = 0
    for p in pages:
        name = p.get("name", "?")
        frames = p.get("frames", [])
        tops = [f for f in frames if f.get("type") in ("FRAME", "COMPONENT")]
        scr = [f for f in tops if str(f.get("name", "")).startswith("SCR-")]
        if name == "组件" or name.lower() in ("components", "_components"):
            lines.append("  组件页：%d 个主组件" % len(
                [f for f in tops if f.get("type") == "COMPONENT"]))
            continue
        scr_pages += 1
        lines.append('  页「%s」：%d 个顶层 frame（%d 个 SCR-）' % (name, len(tops), len(scr)))
        if len(scr) != 1:
            ok = False
            lines.append("    ✗ 违反「一屏一个 Page」：该页有 %d 个屏幕画板" % len(scr))
        others = [f for f in tops if not str(f.get("name", "")).startswith("SCR-")]
        if others:
            lines.append("    注意：非 SCR- 顶层 frame %s" % [f.get("name") for f in others])
    missing = d.get("missingFonts") or []
    if missing:
        lines.append("  ✗ 缺字体：%s" % ", ".join(map(str, missing)))
        ok = False
    lines.insert(0, "屏数 %d / 页面 %d / 节点 %d" % (scr_pages, len(pages), d.get("nodes", 0)))
    return ok, "\n".join(lines)
