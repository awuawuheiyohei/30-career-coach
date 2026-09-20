"""进度追踪 + 周报"""

from pathlib import Path
from datetime import datetime, timedelta
import json

from . import DATA_DIR


def _load() -> dict:
    f = DATA_DIR / "progress.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    return {"recent_activity": [], "stats": {}}


def _save(data: dict) -> None:
    (DATA_DIR / "progress.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def overview() -> str:
    """总览：今日 + 本周 + 总计"""
    data = _load()
    recent = data.get("recent_activity", [])
    today = datetime.now().strftime("%Y-%m-%d")
    today_hours = sum(a.get("hours", 0) for a in recent if a.get("date") == today)

    week_start = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    week_hours = sum(a.get("hours", 0) for a in recent if a.get("date") >= week_start)

    total_hours = sum(a.get("hours", 0) for a in recent)

    md = f"""# 📊 Career Coach 进度总览

## 今日 ({today})
- 计划时间: {today_hours} 小时
- 目标: 4 小时/天
- 完成率: {today_hours / 4 * 100:.0f}%

## 本周 ({week_start} 至今)
- 总时长: {week_hours} 小时
- 平均每天: {week_hours / 7:.1f} 小时
- 目标: 4 小时/天 × 7 = 28 小时

## 累计
- 总记录: {len(recent)} 条活动
- 总时长: {total_hours} 小时

## 最近 10 条
"""
    for a in recent[:10]:
        md += f"- {a.get('date', '')} | {a.get('action', '')} | {a.get('hours', '')}h\n"

    return md


def today_status() -> str:
    """今日状态"""
    data = _load()
    today = datetime.now().strftime("%Y-%m-%d")
    recent = [a for a in data.get("recent_activity", []) if a.get("date") == today]

    if not recent:
        return f"# 今日 ({today})\n\n还没活动。建议：python main.py plan --hours 4 --target ..."
    return overview()


def week_report() -> str:
    """周报：活动 + 完成率"""
    data = _load()
    today = datetime.now()
    week_start = today - timedelta(days=7)
    week_start_str = week_start.strftime("%Y-%m-%d")

    recent = [a for a in data.get("recent_activity", []) if a.get("date") >= week_start_str]
    total_hours = sum(a.get("hours", 0) for a in recent)

    md = f"""# 📅 周报 ({week_start_str} - {today.strftime('%Y-%m-%d')})

## 统计
- 总时长: {total_hours} 小时
- 目标: 28 小时（4h × 7d）
- 完成率: {total_hours / 28 * 100:.0f}%

## 活动列表
"""
    for a in recent:
        md += f"- **{a.get('date', '')}** | {a.get('action', '')} | {a.get('hours', 0)}h\n"

    if not recent:
        md += "_本周还没活动_\n"

    return md


def main():
    import argparse
    parser = argparse.ArgumentParser(description="View progress")
    parser.add_argument("--week", action="store_true")
    parser.add_argument("--today", action="store_true")
    args = parser.parse_args()

    if args.today:
        print(today_status())
    elif args.week:
        print(week_report())
    else:
        print(overview())


if __name__ == "__main__":
    main()