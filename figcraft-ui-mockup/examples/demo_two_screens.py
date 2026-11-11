#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最小可跑的两屏示例：验证 figbase 的组件/实例/每屏一 Page 约定。

    python3 demo_two_screens.py            # 生成 demo.json + demo.figcraft + png/
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "assets"))
import figbase as F
from figbase import (rect, frame, text, page, screen, make_component,
                     instance, CUR)

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 640
NAV = [("概览", "grid"), ("设备", "cpu"), ("日志", "list")]

# ------------------------------------------------ 1) 组件页（先建，供后面复制）
F.begin()          # 复用默认首页并改名「组件」，避免多出一个空 Page


def draw_topbar(p):
    rect(0, 0, W, 56, p, "#151B23", name="背景")
    rect(0, 55, W, 1, p, "#232C38", name="下边线")
    rect(16, 14, 28, 28, p, radius=8, name="Logo")
    text("示例控制台", 56, 14, 15, "#E9EFF6", "Medium", parent=p)
    text("Demo Console", 56, 34, 9.5, "#5D6A79", parent=p)


TOP = make_component("Chrome / 顶栏", W, 56, draw_topbar, fill=None)


def draw_side(p):
    rect(0, 0, 180, H - 56, p, "#111820", name="背景")
    y = 18
    for label, _ic in NAV:
        text(label, 24, y, 12.5, "#94A2B1", parent=p)
        y += 40
    rect(179, 0, 1, H - 56, p, "#1D2733", name="右边线")


SIDE = make_component("Chrome / 侧栏", 180, H - 56, draw_side)


def draw_btn(p):
    # 组件内只放一个文本子层，底色/描边在根 frame 上（见 make_component 参数）
    text("按钮", 0, 8, 11.5, "#C7D3E1", "Medium", align="center", w=88, parent=p)


BTN = make_component("Button / 默认", 88, 32, draw_btn, radius=7,
                     stroke="#2B3745", grad={"type": "linearGradient",
                                             "stops": ["#1E2A38", "#16202B"],
                                             "from": [0, 0], "to": [0, 1]})

# ------------------------------------------------ 2) 每屏一个 Page
P1 = page("系统概览", "P1")
C1 = screen(P1, "系统概览", W, H, fill="#0E131A",
            parts=[(TOP, 0, 0, "顶栏"), (SIDE, 0, 56, "侧栏")])
CUR[0] = C1
text("系统概览", 204, 84, 20, "#EEF4FA", "Bold")
instance(BTN, C1, 204, 120, label="刷新", name="按钮-刷新")
frame(204, 176, 780, 120, "卡片 / 设备状态", "#151D26", radius=12,
      stroke="#212C38", asname="card1")

P2 = page("设备信息", "P2")
C2 = screen(P2, "设备信息", W, H, fill="#0E131A",
            parts=[(TOP, 0, 0, "顶栏"), (SIDE, 0, 56, "侧栏")])
CUR[0] = C2
text("设备信息", 204, 84, 20, "#EEF4FA", "Bold")
instance(BTN, C2, 204, 120, label="导出", name="按钮-导出")
frame(204, 176, 780, 120, "卡片 / 硬件", "#151D26", radius=12,
      stroke="#212C38", asname="card2")

# ------------------------------------------------ 3) 落地与校验
if __name__ == "__main__":
    js = F.dump(os.path.join(OUT, "demo.json"))
    ok, bad = F.run(js, os.path.join(OUT, "demo.figcraft"))
    print("run:", "OK" if ok else "FAILED")
    for b in bad[:5]:
        print("  ", b)
    ok2, rep = F.audit(os.path.join(OUT, "demo.figcraft"))
    print(rep)
    print("audit:", "OK" if ok2 else "FAILED")
