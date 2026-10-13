#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成个人网站的 og:image 分享缩略图（1200x630）。
设计基调刻意对齐 portfolio-site/index.html 的设计 token：
  --void #08090b / --surface #0e1013 / --ink #f2f1ec / --ink-2 #b7bac2
  --muted #787d88 / --line rgba(242,241,236,.10) / --amber #f0a92b
右侧几何母题呼应首屏 identity 卡的 SVG 拓扑图（中心节点 + 模块环）。
"""
from PIL import Image, ImageDraw, ImageFont
import re, pathlib

# 项目数直接读 index.html，避免手写数字与站点文案漂移（曾出现过 OG 图 31 / 站点 35）
_here = pathlib.Path(__file__).parent
_m = re.search(r'(\d+)\s*个开源项目', (_here / "index.html").read_text(encoding="utf-8"))
NPROJ = _m.group(1) if _m else "?"

W, H = 1200, 630
VOID = (8, 9, 11)
INK = (242, 241, 236)
INK2 = (183, 186, 194)
MUTED = (120, 125, 136)
FAINT = (74, 78, 87)
AMBER = (240, 169, 43)
AMBER_2 = (255, 197, 92)
AZURE = (61, 99, 240)
TEAL = (24, 168, 155)

CJK = "/System/Library/Fonts/Hiragino Sans GB.ttc"
MONO = "/System/Library/Fonts/SFNSMono.ttf"


def F(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), VOID)
d = ImageDraw.Draw(img, "RGBA")

# ── 背景细网格（技术感，克制）────────────────────────────────
for x in range(0, W, 40):
    d.line([(x, 0), (x, H)], fill=(255, 255, 255, 6), width=1)
for y in range(0, H, 40):
    d.line([(0, y), (W, y)], fill=(255, 255, 255, 6), width=1)

# ── 右上几何母题：中心节点 + 模块环 ──────────────────────────
cx, cy = 1015, 315
for r, a in ((86, 26), (140, 18), (196, 12)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=AMBER + (a,), width=1)

import math
mods = [
    (86, -90, AMBER), (86, 30, TEAL), (140, 165, AZURE), (140, -20, AMBER),
    (140, 80, TEAL), (196, 205, FAINT), (196, 120, AZURE),
]
for r, ang, col in mods:
    a = math.radians(ang)
    x, y = cx + r * math.cos(a), cy + r * math.sin(a)
    d.line([(cx, cy), (x, y)], fill=(255, 255, 255, 16), width=1)
    s = 7
    d.rectangle([x - s, y - s, x + s, y + s], outline=col + (200,), width=2)

# 中心：琥珀实心 + 外环
d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=AMBER + (170,), width=1)
d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=AMBER + (235,))

# ── 左侧琥珀信号竖条 ────────────────────────────────────────
d.rectangle([0, 0, 7, H], fill=AMBER)

# ── 文本区 ──────────────────────────────────────────────────
L = 76

f_kick = F(MONO, 17)
d.text((L, 84), "JIANG WENRUI · JARVIS / PERSONAL SITE", font=f_kick, fill=MUTED)

# 姓名 —— 琥珀下划线强调「严谨」
f_name = F(CJK, 84, 0)
d.text((L - 4, 128), "蒋汶睿", font=f_name, fill=INK)
nw = d.textlength("蒋汶睿", font=f_name)
d.rectangle([L, 232, L + nw - 8, 236], fill=AMBER)

# 方向
f_role = F(MONO, 23)
d.text((L, 264), "IT  /  SECURITY COMPLIANCE  /  DEVSECOPS", font=f_role, fill=AMBER_2)

# 主标语
f_head = F(CJK, 46, 0)
d.text((L, 330), "把企业级 IT 的严谨，", font=f_head, fill=INK)
d.text((L, 392), "带进 AI 工程。", font=f_head, fill=INK)

# 分隔线
d.line([(L, 476), (L + 640, 476)], fill=(242, 241, 236, 26), width=1)

# 数据条
f_stat = F(CJK, 24, 0)
x = L
for txt, col in (("4 年企业级 IT 交付", INK2), (f"{NPROJ} 个开源项目", INK2)):
    d.text((x, 508), txt, font=f_stat, fill=col)
    x += d.textlength(txt, font=f_stat)
    if txt.startswith("4"):
        d.ellipse([x + 26, 517, x + 33, 524], fill=AMBER)
        x += 46

f_foot = F(MONO, 18)
d.text((L, 566), "SECURITY  ·  IDENTITY  ·  DATA ENGINEERING  ·  AI APPLICATION",
       font=f_foot, fill=FAINT)

out = "/Users/jiangwenrui/Downloads/mass/30-career-coach/portfolio-site/assets/og-image.png"
img.save(out, "PNG", optimize=True)
print("已生成:", out, img.size)