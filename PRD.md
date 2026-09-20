# Personal Career Coach — PRD

> **一句话**：基于我的 3 个并行目标（A 档 IT Support 保底 / B 档数据工程 主投 / C 档 LLM 算法 / D 档嵌入式铁路），自动生成每日 4 小时学习计划 + 模拟面试题 + 进度追踪。

> **核心哲学**：每个工作日剩余 4 小时，CISSP + 研究生 双线备考，最稀缺的是**注意力**，不是信息。
> Personal Career Coach 不是"万能学习助手"——它是**调度员**。

---

## 🎯 用户

我自己（蒋汶睿）：
- 3 年 IT 运维（克诺尔 IT Analyst + 微创 IT 技术支持）
- 微软系技术栈 + PMP + CISSP（预计 2026-09 拿证）+ ITILv5 + 雅思 6.0
- 2026 秋拟入学南京理工大学非全日制 AI 研究生
- 4 个意向岗位（A/B/C/D 档）+ 0 投递状态

---

## 📥 输入

```yaml
today:
  remaining_hours: 4         # 今晚剩余时间
  energy_level: "medium"     # high / medium / low
  date: "2026-09-19"
current_target: "D 档嵌入式铁路面试准备"
recent_activity:
  - { date: "2026-09-18", action: "完成 D 档问题 bilingual", hours: 2 }
  - { date: "2026-09-17", action: "读 EN 50126 标准", hours: 1.5 }
context:
  resume_data_path: "../Interview/resume_data.md"
  jd_dir: "../Interview/jd/"
  existing_projects: ["mother_care", "ai_knowledge_cockpit", "Friday_Translator", ...]
```

---

## 📤 输出

### 1. 4 小时精确计划（按小时分段）

```yaml
plan:
  - time: "19:00-19:45"
    action: "读 EN 50128 标准第 4 章（软件需求）"
    source: "../Interview/jd/d-embedded-rail-safety.md"
    why: "JD 要求 EN 50126/128/129，你目前只读了 50126"
  - time: "19:45-20:30"
    action: "模拟面试：EN 50128 vs IEC 61508 区别"
    type: "tech_question"
    expected_score: "需要 3 维评分 ≥ 8"
  - break: "20:30-20:45"
  - time: "20:45-21:30"
    action: "更新 resume_data.md §5 加 D 档项目"
  - time: "21:30-22:00"
    action: "tracker.md 加 D 档投递行"
```

### 2. 推荐复习 source（自动聚合）

从以下来源按 JD 关键词匹配：
- `resume_data.md`（候选人的真实项目）
- `jd/<current_jd>.md`（目标 JD）
- `mother_care/KB/`、`ai_knowledge_cockpit/KB/`（已积累知识）
- 用户最近 7 天 GitHub commit（实际做了什么）

### 3. 模拟面试题（自动从 source 生成）

```yaml
mock_questions:
  - id: "EN50128-V-V-model"
    question: "描述你做过的最复杂的 V&V 活动"
    dimensions: [技术深度, 表达清晰, 量化结果, 案例匹配, 反思深度]
    expected_8_plus: true
    based_on: "resume §4.1 克诺尔 ISO 27001 IT module audit (可类比 V&V 文档要求)"
```

### 4. 进度追踪

- 每日完成率（按 4 小时）
- 周报 + 月报
- 同侪对比（可选，匿名）

---

## 🏗 架构（v1.0 MVP）

```
career-coach/
├── README.md                 # 本 PRD
├── app/
│   ├── main.py               # FastAPI 入口
│   ├── coach.py              # CareerCoach agent（核心）
│   ├── planner.py            # 4 小时计划生成
│   ├── question_gen.py       # 模拟面试题生成（基于 JD + 简历）
│   ├── source_aggregator.py  # 从 resume_data + jd/ + KB/ 聚合
│   └── progress.py           # 进度追踪
├── prompts/
│   ├── planner.md            # 4 小时计划 prompt
│   ├── question_gen.md       # 模拟面试题 prompt（复用 Interview/ 的 simulate）
│   └── source_aggregator.md  # source 聚合 prompt
├── data/
│   ├── progress.json         # 每日完成率
│   ├── questions.json        # 历史模拟面试题
│   └── sources.json          # source 索引
├── tests/
│   └── test_planner.py       # planner 单测
├── pyproject.toml
└── .env.example              # LLM_API_KEY etc.
```

### 技术选型

- **Python 3.11+** · **FastAPI** · **SQLite**（轻量、个人用）
- **LLM**：DeepSeek-V3（默认） / OpenAI 兼容
- **数据源**：
  - 静态：resume_data.md + jd/ + mother_care/KB
  - 动态：最近 git log + KB search
- **零外部依赖**（除 LLM API）
- **个人用**，不部署

---

## 🚫 反模式

- **🚨 禁止"万能学习助手"**：不做通用知识问答，专注"调度"
- **🚨 禁止付费课推荐**：用户策略定向，不推 Coursera/极客时间
- **🚨 禁止"每天 8 小时学"**：用户在职 + 双线备考，**每天 4 小时封顶**
- **🚨 禁止编造**：模拟面试题必须基于 source_data 真实项目，不编
- **🚨 禁止"21 天速成"**：用户 3 年经验 + CISSP/研究生双线，速成不现实

---

## 🎯 v1.0 验收标准（1-2 周）

- [ ] `python main.py plan` 输入今日剩余时间 → 输出 4 小时精确计划
- [ ] `python main.py question D` → 输出 5 个模拟面试题（基于 D 档 JD）
- [ ] `python main.py progress week` → 输出本周进度 + 周报
- [ ] 单测覆盖核心逻辑
- [ ] 真实跑 3 天无 bug

## 🚀 v2.0（3-4 周）

- 集成 mother_care KB 搜索（复用 FAISS + BGE embedding）
- 集成 ai_knowledge_cockpit KB
- IM 提醒（钉钉 Stream）
- 进度可视化（Web dashboard）

## 🌟 v3.0（5-6 周）

- 自适应难度（C 模式）
- 同侪对比（匿名）
- ML 模型预测"今天该不该学 X"