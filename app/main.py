#!/usr/bin/env python3
"""
main.py — Personal Career Coach CLI

用法：
  python main.py plan --hours 4 --target "D 档嵌入式" --energy medium
  python main.py question D   # 自动从 jd/d-embedded-rail-safety.md 出 5 道题
  python main.py progress     # 查看本周进度
"""
import argparse
import sys
from pathlib import Path

# 加载 .env
env_file = Path(__file__).resolve().parent.parent / ".env"
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        import os
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def cmd_plan(args):
    from . import planner
    plan = planner.generate_plan(args.hours, args.target, args.energy)
    print(plan)


def cmd_question(args):
    from . import question_gen
    questions = question_gen.generate_questions(args.jd, n=args.n)
    print(questions)


def cmd_progress(args):
    from . import progress as prog
    if args.week:
        print(prog.week_report())
    elif args.today:
        print(prog.today_status())
    else:
        print(prog.overview())


def main():
    parser = argparse.ArgumentParser(description="Personal Career Coach")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_plan = sub.add_parser("plan", help="生成今日 4 小时计划")
    p_plan.add_argument("--hours", type=float, default=4.0, help="剩余时间")
    p_plan.add_argument("--target", default="求职准备", help="当前目标")
    p_plan.add_argument("--energy", default="medium", choices=["high", "medium", "low"])

    p_q = sub.add_parser("question", help="基于 JD 生成模拟面试题")
    p_q.add_argument("jd", help="JD 标识（如 d-embedded-rail-safety）")
    p_q.add_argument("-n", "--num", type=int, default=5, help="题目数")

    p_prog = sub.add_parser("progress", help="查看进度")
    p_prog.add_argument("--week", action="store_true", help="周报")
    p_prog.add_argument("--today", action="store_true", help="今日状态")

    args = parser.parse_args()

    if args.cmd == "plan":
        cmd_plan(args)
    elif args.cmd == "question":
        cmd_question(args)
    elif args.cmd == "progress":
        cmd_progress(args)


if __name__ == "__main__":
    main()