"""模拟面试题生成器 - 复用 Interview/ 的 simulate prompt"""

from pathlib import Path
from datetime import datetime
import json

from . import call_llm, load_prompt, DATA_DIR

# Interview/ 项目的 prompt 路径（复用）
INTERVIEW_PROMPTS = Path("../Interview/prompts/simulate_interview.md")


def load_jd_text(jd_id: str) -> str:
    """Load JD by identifier (e.g. 'd-embedded-rail-safety')"""
    # 尝试 jd/{id}.md 或 jd/{id}-*.md
    jd_dir = Path("../Interview/jd/")
    for f in [f"{jd_id}.md", f"{jd_id}-*.md"]:
        matches = list(jd_dir.glob(f))
        if matches:
            return matches[0].read_text(encoding="utf-8")[:5000]
    raise FileNotFoundError(f"JD not found: {jd_id}")


def load_resume() -> str:
    """Load resume_data.md"""
    p = Path("../Interview/resume_data.md")
    if p.exists():
        return p.read_text(encoding="utf-8")[:8000]
    return "（未找到 resume_data.md）"


def generate_questions(jd_id: str, n: int = 5) -> str:
    """Generate N interview questions based on JD + resume

    Args:
        jd_id: JD identifier (e.g. 'd-embedded-rail-safety')
        n: number of questions

    Returns:
        markdown 格式的题目列表（含参考答案提示）
    """
    jd_text = load_jd_text(jd_id)
    resume = load_resume()

    # 直接复用 Interview/ 的 simulate prompt 作为 system
    system_prompt = load_prompt("interview_pack.md") if (Path(__file__).resolve().parent.parent / "prompts" / "interview_pack.md").exists() else (
        "你是一名资深面试官。基于候选人简历和 JD 出模拟面试题。"
    )

    user_prompt = f"""基于以下信息出 {n} 道模拟面试题（按 JD 高频关键词）：

## 候选人简历（source_data）
{resume}

## 目标 JD
{jd_text}

## 要求
1. 每题用 1 行（不超 50 字，直接问）
2. 标"考察维度"（技术深度 / 表达 / 量化 / 案例 / 反思）
3. 标"难度档"（1-10）
4. 标"必须基于候选人简历真实项目"（避免编造）
5. 标"预期命中率"（候选人有多大把握答到 8+ 分）

## 输出格式

### Q1: [题目]
- 考察: ...
- 难度: N/10
- 基于: [候选人简历哪个项目]
- 命中率: N%

### Q2: ...

(共 {n} 题)
"""

    result = call_llm(system_prompt, user_prompt, max_tokens=2000)

    # 记录题目
    _log_questions(jd_id, result)
    return result


def _log_questions(jd_id: str, questions: str) -> None:
    """记录模拟面试题历史"""
    questions_file = DATA_DIR / "questions.json"
    if questions_file.exists():
        data = json.loads(questions_file.read_text(encoding="utf-8"))
    else:
        data = {"history": []}

    data["history"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "jd": jd_id,
        "questions": questions,
    })
    data["history"] = data["history"][-20:]  # 保留最近 20 条

    questions_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate mock interview questions")
    parser.add_argument("jd", help="JD identifier")
    parser.add_argument("-n", "--num", type=int, default=5)
    args = parser.parse_args()

    questions = generate_questions(args.jd, args.num)
    print(questions)


if __name__ == "__main__":
    main()