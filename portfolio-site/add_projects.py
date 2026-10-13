#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 6 个新公开仓库补进「全部项目」，并重排编号 / 分组计数 / 文案数字。
- 新卡片插入对应分组的末尾，随后全量重编号 01..N
- 分组计数 · NN 同步更新
- 「31 个开源项目」→「35 个开源项目」
- 挂上 og:image / og:image:width / og:image:height
"""
import re, pathlib

P = pathlib.Path(__file__).parent / "index.html"
s = P.read_text(encoding="utf-8")
orig_len = len(s)

def card(idx_placeholder, repo, title, desc, tech="Python"):
    return (
        '          <a class="pcard" href="https://github.com/awuawuheiyohei/{repo}" target="_blank" rel="noopener noreferrer">\n'
        '            <div class="pcard-top"><span class="pcard-idx">{idx}</span><span class="pcard-repo">{repo}</span></div>\n'
        '            <h3>{title}</h3>\n'
        '            <p>{desc}</p>\n'
        '            <div class="pcard-foot"><span>{tech}</span><span class="arrow" aria-hidden="true">↗</span></div>\n'
        '          </a>\n'
    ).format(idx=idx_placeholder, repo=repo, title=title, desc=desc, tech=tech)

# 索引先占位，最后统一重编号
NEW_C = [  # → C 组 AI / LLM 应用
    ("meeting-to-action", "会议转行动项", "Whisper 转写后自动产出纪要 / 待办 / 决策点 / 下次议题"),
    ("rss-reader",       "AI 聚合阅读", "自托管 RSS 聚合 + AI 多源总结 + 主题分类，数据本地不出网"),
    ("A",                "A 股分析助手", "akshare 取数 + 模型评分，每日两次自动出分析报告"),
]
NEW_D = [  # → D 组 工具与记录
    ("career-coach",         "个人职业教练", "按多目标生成每日精确计划 + 模拟面试题 + 进度追踪"),
    ("dashboard5.0-main",    "业主信息看板", "FastAPI + SQLite 看板，含三角色 RBAC 与全量审计日志"),
    ("insurance",            "少儿险条款对照", "意外险 / 医疗险条款并排对比，每字段可溯源官网原文"),
]

def insert_into_group(text, group_marker, cards):
    """在指定 <b>X</b> 分组的 pgrid 结束前插入卡片。"""
    m = re.search(re.escape(group_marker), text)
    if not m:
        raise SystemExit(f"未找到分组标记: {group_marker}")
    # 该分组 pgrid 的收尾：8 空格 </div> 紧跟 6 空格 </div>
    tail = text.find("\n        </div>\n      </div>", m.end())
    if tail == -1:
        raise SystemExit(f"未找到分组 {group_marker} 的收尾标记")
    block = "".join(card("00", r, t, d) for r, t, d in cards)
    return text[:tail + 1] + block + text[tail + 1:]

s = insert_into_group(s, '<b>C</b><span>AI / LLM 应用</span>', NEW_C)
s = insert_into_group(s, '<b>D</b><span>工具与记录</span>', NEW_D)

# ── 全量重编号 01..N ────────────────────────────────────────
idx = 0
def _renum(m):
    global idx
    idx += 1
    return f'pcard-idx">{idx:02d}'
s = re.sub(r'pcard-idx">\d+', _renum, s)
total = idx

# ── 分组计数同步 ────────────────────────────────────────────
def bump(group_tag, old, new):
    global s
    pat = re.compile(re.escape(group_tag) + r'(.*?)· ' + old + r'(<)', re.S)
    s, n = pat.subn(lambda m: group_tag + m.group(1) + f'· {new}' + m.group(2), s, count=1)
    if not n:
        raise SystemExit(f"分组计数未更新: {group_tag}")

bump('<b>C</b><span>AI / LLM 应用</span>', '04', f'{len(NEW_C) + 4:02d}')
bump('<b>D</b><span>工具与记录</span>',   '02', f'{len(NEW_D) + 2:02d}')

# ── 文案数字 ────────────────────────────────────────────────
n31 = s.count('31 个开源项目')
s = s.replace('31 个开源项目', '35 个开源项目')

# ── 挂 og:image ─────────────────────────────────────────────
if 'og:image' not in s:
    s = s.replace(
        '<meta property="og:locale" content="zh_CN" />',
        '<meta property="og:locale" content="zh_CN" />\n'
        '<meta property="og:image" content="https://06a9sk88n7fwg.space.mcode.cn/assets/og-image.png" />\n'
        '<meta property="og:image:width" content="1200" />\n'
        '<meta property="og:image:height" content="630" />\n'
        '<meta property="og:image:alt" content="蒋汶睿 — IT / 安全合规 / DevSecOps" />'
    )
    s = s.replace(
        '<meta name="twitter:card" content="summary" />',
        '<meta name="twitter:card" content="summary_large_image" />\n'
        '<meta name="twitter:image" content="https://06a9sk88n7fwg.space.mcode.cn/assets/og-image.png" />'
    )

P.write_text(s, encoding="utf-8")
print(f"✅ 卡片总数: {total}")
print(f"✅ 文案「31」→「35」共 {n31} 处")
print(f"✅ 字节数: {orig_len} → {len(s)}")