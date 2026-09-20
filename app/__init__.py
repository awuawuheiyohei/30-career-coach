# Career Coach core agent

import os
import re
import sys
from pathlib import Path
from typing import Optional

import requests

# Project paths
ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# Default config (overridable via .env)
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "https://api.MiniMax.chat/v1")
LLM_MODEL = os.environ.get("LLM_MODEL", "MiniMax-M3")
LLM_TEMPERATURE = float(os.environ.get("LLM_TEMPERATURE", "0.3"))


def load_prompt(name: str) -> str:
    """Load prompt template from prompts/ directory"""
    path = PROMPTS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {path}")
    return path.read_text(encoding="utf-8")


def strip_thinking(content: str) -> str:
    """Strip LLM thinking blocks (标签 + 裸文本)"""
    # 1) 完整 <think> 块
    content = re.sub(r"<think>.*?</think>\s*", "", content, flags=re.DOTALL)
    # 2) 未闭合的 <think>
    content = re.sub(r"<think>.*$", "", content, flags=re.DOTALL)
    # 3) 裸文本 thinking markers
    thinking_markers = [
        r"^OK final structure:.*$",
        r"^OK let me (write|think).*$",
        r"^OK writing now.*$",
        r"^Actually[, ].*$",
        r"^Wait[, ].*$",
        r"^One more thought:.*$",
        r"^Let me (write|think|finalize|now).*$",
    ]
    for marker in thinking_markers:
        m = re.search(marker, content, flags=re.MULTILINE)
        if m:
            content = content[:m.start()].rstrip() + "\n"
            break
    return content.strip() + "\n"


def call_llm(system_prompt: str, user_prompt: str,
             api_key: str = None, base_url: str = None, model: str = None,
             temperature: float = None, max_tokens: int = 4000) -> str:
    """Call OpenAI-compatible chat completion API

    Returns:
        LLM response content (thinking stripped)
    """
    api_key = api_key or LLM_API_KEY
    if not api_key:
        raise ValueError("LLM_API_KEY 未配置。请在 .env 里设置 LLM_API_KEY=<你的 key>")

    base_url = base_url or LLM_BASE_URL
    model = model or LLM_MODEL
    temperature = temperature if temperature is not None else LLM_TEMPERATURE

    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=300)
    if resp.status_code != 200:
        raise RuntimeError(f"LLM 调用失败 ({resp.status_code}):\n{resp.text[:1000]}")

    content = resp.json()["choices"][0]["message"]["content"]
    return strip_thinking(content)