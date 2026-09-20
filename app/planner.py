"""4-hour daily plan generator"""

from pathlib import Path
from datetime import datetime
from . import call_llm, load_prompt, DATA_DIR


def load_user_context() -> str:
    """Load user context (resume + recent JD + recent activity)"""
    parts = []

    # 1. resume_data.md
    resume = Path("../Interview/resume_data.md")
    if resume.exists():
        parts.append(f"## 候选人简历（source_data）\n{resume.read_text(encoding='utf-8')[:8000]}")
    else:
        parts.append("## 候选人简历\n（未找到 ../Interview/resume_data.md）")

    # 2. current JD (if specified)
    jd_dir = Path("../Interview/jd/")
    if jd_dir.exists():
        jds = sorted(jd_dir.glob("*.md"))
        parts.append(f"## 候选人 JD 文件\n{', '.join(j.stem for j in jds)}")

    # 3. recent progress
    progress = DATA_DIR / "progress.json"
    if progress.exists():
        import json
        data = json.loads(progress.read_text(encoding="utf-8"))
        recent = data.get("recent_activity", [])[:7]  # 最近 7 天
        parts.append(f"## 最近 7 天活动\n{chr(10).join(f'- {a}' for a in recent)}")

    return "\n\n".join(parts)


def generate_plan(remaining_hours: float, current_target: str,
                  energy_level: str = "medium") -> str:
    """生成 4 小时精确计划

    Args:
        remaining_hours: 今日剩余时间（如 4.0）
        current_target: 当前目标（如 "D 档嵌入式铁路面试准备"）
        energy_level: high / medium / low

    Returns:
        markdown 格式的计划
    """
    template = load_prompt("planner.md")
    user_context = load_user_context()

    user_prompt = (template
        .replace("{{REMAINING_HOURS}}", str(remaining_hours))
        .replace("{{CURRENT_TARGET}}", current_target)
        .replace("{{ENERGY_LEVEL}}", energy_level)
        .replace("{{USER_CONTEXT}}", user_context)
        .replace("{{DATE}}", datetime.now().strftime("%Y-%m-%d")))

    result = call_llm(template, user_prompt)

    # 记录进度
    _log_plan(remaining_hours, current_target, result)
    return result


def _log_plan(remaining_hours: float, current_target: str, plan: str) -> None:
    """记录今日计划"""
    import json
    progress_file = DATA_DIR / "progress.json"
    if progress_file.exists():
        data = json.loads(progress_file.read_text(encoding="utf-8"))
    else:
        data = {"recent_activity": [], "stats": {}}

    data["recent_activity"].insert(0, {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "action": f"plan: {current_target}",
        "hours": remaining_hours,
    })
    data["recent_activity"] = data["recent_activity"][:30]  # 保留最近 30 条

    progress_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate 4-hour daily plan")
    parser.add_argument("--hours", type=float, default=4.0, help="今日剩余时间（小时）")
    parser.add_argument("--target", default="求职准备", help="当前目标")
    parser.add_argument("--energy", default="medium", choices=["high", "medium", "low"])
    args = parser.parse_args()

    plan = generate_plan(args.hours, args.target, args.energy)
    print(plan)


if __name__ == "__main__":
    main()