# Personal Career Coach

> 基于我的 3 个并行目标（A 档 IT Support 保底 / B 档数据工程 主投 / C 档 LLM 算法 / D 档嵌入式铁路），
> 自动生成**每日 4 小时精确计划** + **模拟面试题** + **进度追踪**。

不是"万能学习助手"——是**调度员**。

详见 [PRD.md](./PRD.md)。

---

## 🚀 快速开始

```bash
# 1. 准备 .env
cp .env.example .env
# 编辑 .env 填 LLM_API_KEY=...

# 2. 激活 venv（如有）
source .venv/bin/activate

# 3. 跑计划
python -m app.main plan --hours 4 --target "D 档嵌入式面试" --energy medium

# 4. 跑模拟面试题
python -m app.main question d-embedded-rail-safety -n 5

# 5. 看进度
python -m app.main progress --week
```

---

## 📁 项目结构

```
career-coach/
├── README.md                 # 本文件
├── PRD.md                    # 需求文档
├── pyproject.toml            # Python 配置
├── .env.example              # 环境变量模板
├── .gitignore
├── app/
│   ├── __init__.py           # LLM 调用公共函数（call_llm + strip_thinking）
│   ├── main.py               # CLI 入口（plan / question / progress）
│   ├── planner.py            # 4 小时计划生成
│   ├── question_gen.py       # 模拟面试题生成
│   └── progress.py           # 进度追踪 + 周报
├── prompts/
│   └── planner.md            # planner prompt 模板
├── data/                     # 进度数据（gitignore）
└── tests/
```

---

## 🎯 核心原则

- **调度员，不是万能学习助手**：不做通用知识问答，专注"今天这 4 小时怎么用"
- **基于事实**：所有计划必须基于候选人简历 + JD + 最近活动，**禁止编造**
- **4 小时封顶**：在职 + 双线备考（CISSP + 研究生），时间最稀缺
- **可执行**：每个时间块要给具体动作 + 验收标准
- **可衡量**：每块含 5 维评分（技术 / 表达 / 量化 / 案例 / 反思）

---

## 🛠 命令

### `plan` — 今日 4 小时计划

```bash
python -m app.main plan \
  --hours 4 \
  --target "D 档嵌入式面试" \
  --energy medium  # high / medium / low
```

### `question` — 模拟面试题

```bash
python -m app.main question d-embedded-rail-safety -n 5
```

复用 Interview/ 项目的 `prompts/interview_pack.md`（关键词映射）。

### `progress` — 进度追踪

```bash
python -m app.main progress           # 总览
python -m app.main progress --today  # 今日
python -m app.main progress --week   # 周报
```

---

## 📊 进度数据（data/progress.json）

```json
{
  "recent_activity": [
    {"date": "2026-09-19", "action": "plan: D 档嵌入式", "hours": 4}
  ],
  "stats": {}
}
```

---

## 🔗 与 Interview/ 项目的整合

- **复用**：JD 文件（`../Interview/jd/`）、简历源（`../Interview/resume_data.md`）、prompt 模板
- **互补**：Career Coach 是"调度"，Interview 是"生成报告"，不重复
- **同步**：未来可在 Dashboard 加 Career Coach tab

---

## 🚀 Roadmap

- [x] v0.1 MVP（1-2 周）：plan / question / progress 三件套
- [x] **端到端验证 2026-09-19**：planner.generate_plan 真实调用 LLM，1056 字符输出，含诚实 disclaimer（D 档 gap 警告 + B/C 档更现实建议）
- [ ] v0.2：集成 mother_care KB 搜索
- [ ] v0.3：IM 提醒（钉钉 Stream）
- [ ] v1.0：Web dashboard + 同侪对比