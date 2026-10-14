# 个人网站 · 交接说明

> 本文件**不属于**部署产物，刻意放在 `portfolio-site/` 外面，避免被一起发布到公网。

## 给新 session 的开场白（可直接粘贴）

```
接手个人网站项目。工作目录 ~/Downloads/mass/30-career-coach。

先读项目根目录的 PORTFOLIO-SITE.md，里面有完整部署方式、结构说明和待办。

【已完成】建站时误把南京理工大学写成「在读 / 攻读」，违反既定红线（备考中的
学历不得写「在读/就读」）。三处已于 2026-10-13 从 30-career-coach 目录成功发布，
URL 不变，线上已验证：grep -c '在读' / '攻读' / '就读' 均为 0。

现在没有阻塞项，直接看下面「待办」里的 1~3。
```

## 改动日志

| 日期 | 内容 | 验证 |
|---|---|---|
| 2026-10-13 | 南京理工大学表述 `在读/攻读` → `备考`（L854 / L1732 / L1771），原地更新 node `450481916682970` | 线上 `在读`/`攻读`/`就读` 计数均为 0 |
| 2026-10-13 | 修复死链 `40-mother_care` → `mother-care`（原来靠 301 重定向） | 35 个仓库链接逐一 HTTP 实测 |
| 2026-10-13 | 补 `robots.txt`（全站禁止索引）、`canonical` / `og:url` / `og:site_name` / `og:locale` / `twitter:card` | robots 200 + `Disallow: /` |
| 2026-10-13 | 生成并挂上 `assets/og-image.png`（1200×630）+ `og:image:*` | 200 / 57,693B / image/png |
| 2026-10-13 | 6 个项目建 public 仓库并推送；卡片 29 → 35，文案 31 → 35 | 线上 35 张卡片、`35 个开源项目` × 3、零死链 |
| 2026-10-13 | 署名加英文名 Jarvis（9 处 + og:image 重绘） | 桌面/移动两套断点实测 |
| 2026-10-13 | **主域名迁到 GitHub Pages**：`awuawuheiyohei.github.io/career-coach`；旧 mcode 地址保留并同步 | 新址 200 / HTTPS+HSTS / 资源全通；canonical 等 4 处已指向新址 |

## 线上地址

| 项 | 值 | 状态 |
|---|---|---|
| **主 URL** | https://awuawuheiyohei.github.io/career-coach/ | **主**，canonical 指向这里 |
| 备用 URL | https://06a9sk88n7fwg.space.mcode.cn | 保留，内容与主站同步（旧链接不失效） |
| Drive node ID | `450481916682970` | mcode 侧部署用 |
| GitHub 仓库 | `awuawuheiyohei/30-career-coach`（public） | Pages 源码 |
| 源码目录 | `mass/30-career-coach/portfolio-site/` | **唯一源**，两个托管都从这里出 |

**两处托管并存的原因**：`space.mcode.cn` 的子域是平台分配的随机哈希（`06a9sk88n7fwg`），
`website_deploy` 只有 `path`/`project_name`/`source_path`/`node_id` 四个参数，**改不了域名**。
GitHub Pages 免费、域名固定可控（`awuawuheiyohei` 就是本人 handle）、自动 HTTPS + HSTS。

**Pages 走 Actions 而非 "Deploy from branch"**：Pages 的 source path 只接受 `/` 或 `/docs`，
指不到 `portfolio-site/`，所以 `.github/workflows/deploy-pages.yml` 在 checkout 后
把 `portfolio-site/` 整份复制到 `_site/` 再 `upload-pages-artifact`。
**好处是 `portfolio-site/` 保持唯一源**——改了它，push 即两边同时更新，不用维护两份。

`robots.txt` 已于 2026-10-13 补上并全站禁止索引（用户决定：只通过主动分享的链接访问）。

## 怎么改（重要）

源码在 `portfolio-site/index.html`，是**单文件全内联**的：CSS、JS、8 张 SVG 插图都在里面，
没有任何外部依赖（无 CDN、无字体外链、无图片文件）。

改完后**原地更新**，URL 不变：

```python
website_deploy(
    path="<绝对路径>/portfolio-site",       # 必须是含 index.html 的目录
    source_path="<绝对路径>/portfolio-site", # 源码根目录
    project_name="蒋汶睿-个人网站",
    node_id="450481916682970",               # 少了这个就变成新站点，会多一个 URL
)
```

**必须带 `node_id`**，否则会发布成第二个站点。

## 页面结构

| 板块 | 内容 |
|---|---|
| 首屏 bento | 身份 / 简介 / 数字卡 / 简历下载 / 能力速览 / 项目预览 / 索引 |
| 精选项目 | 4 个大插图叙事行：护栏 · 原件 · 留痕 · 授信 |
| **全部项目** | **35 张**密排卡片，按 4 组分类，每张链 GitHub 源码 |
| 能力与经验 | 4 张能力卡 + 工作经历时间线 + 教育 + 证书 |
| 关于我 | 四步方法闭环 |
| 联系方式 | 邮箱/手机点击复制（脱敏显示）+ 简历下载 |

设计基调：深色，琥珀 `#f0a92b` 作唯一信号色，四个项目各配低饱和强调色。
交互克制：仅 2px 悬停位移 + 一次性淡入上移，带 `prefers-reduced-motion` 降级。

## 数据来源与红线

内容全部取自 `mass/Interview/` 的简历底座，**不编造数字**。已确认的硬约束：

- CISSP：2026-09 通过，页面写「CISSP · 2026-09」
- 克诺尔 2024.02 **至今**（用户 2026-10-10 明确「还在职」）
- 项目只链 **PUBLIC** 仓库。账号现有 **35 个 public**（2026-10-13），与站点 35 张卡片一一对应；
  `25-Interview` / `26-LJ` / `24-Friday_Translator` / `dashboard5.0`(旧) / `NewlifeHuh` /
  `my-dataroom` 是 PRIVATE，不可链上去
- **项目数口径**：文案「35 个开源项目」必须与可点开的 public 仓库数一致。加卡片 = 加仓库，
  两边一起动，否则面试官点两下就对不上（2026-10-13 曾出现 31 vs 29 vs 35 的三方不一致）

## 待办

0. ~~**⚠️ 有一处已改好但未发布的修改，切目录后请先发一次**~~ —— **2026-10-13 已完成并验证**。
   建站时误把南京理工大学写成「在读 / 攻读」，违反用户既定红线
   （*不得写未入学的学历，备考中不得出现「在读/就读」*）。本地三处已改为「备考」
   （`identity-foot` / 教育经历 `<time>备考中</time>` / `about-small`），并已从
   `30-career-coach` 目录原地发布上线，URL 与 node ID 均未变。
   线上复验：`curl -s <URL> | grep -c '在读'` → `0`（`攻读`/`就读` 同为 0）。

1. **`mass/25-Interview/pdf_gen.py` 的排版修复未提交 git**。`bullet()` / `numbered()` 调
   `multi_cell` 没传 `align`，fpdf2 默认 `"J"`（两端对齐），中文可任意换行 + 行内大量
   `/ ` 空格会被拉成巨大空隙。已显式改成 `align="L"`（147 / 158 行），改动只在工作区。
2. **简历 PDF 与网页的克诺尔时间不一致**：PDF 写 `2024.02 - 2026.10`，网页写「至今」。
   用户选了「还在职」，所以网页没改；PDF 沿用了源文件写法。
3. ~~6 个真实项目还没 push GitHub~~ —— **2026-10-13 已完成**。6 个仓库全部建为 public 并推送，
   网站补了 6 张卡片，卡片数 29 → 35，文案「31 个开源项目」→「35 个开源项目」（3 处）。
   现分组：A 安全合规 18 / B DevOps 5 / C AI·LLM 7 / D 工具与记录 5 = 35，与 public 仓库数闭合。
   > 推送前做过体检：6 个仓库无硬编码密钥、无 `.env` 被跟踪、无身份证号、无手机号/个人邮箱。
   > 公开简历 PDF 只含 `jarvisxfriday@icloud.com`，**不含真实手机号**。

4. **GitHub 仓库名不带 `NN-` 归档序号**（本地目录才带）。已踩过的坑：站点曾链
   `40-mother_care`，而远端实际叫 `mother-care`，靠 301 重定向才能打开——已改成真实名字。
   新增卡片时，href 必须用 `gh api repos/awuawuheiyohei/<name> -q .name` 核对，不要照抄本地目录名。

5. **共享脚本**（改动站点后可直接复用）：
   - `portfolio-site/make_og_image.py` — 用站点设计 token 生成 1200×630 分享图
   - `portfolio-site/add_projects.py` — 插入卡片 + 全量重编号 + 同步分组计数与文案数字
     （占位符必须用**数字**如 `00`，用 `XX` 会被 `pcard-idx">\d+` 跳过，导致新卡片编号不上）