#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day01-Ex05 · 模型边界最小闭环:返回 → 校验 → 重试 → 路由
=====================================================
题目:
    模拟一个"模型节点"(离线):它根据输入返回一段夹着 JSON 的文本。
    你的任务:提取 JSON → Pydantic 校验 → 失败回注错误并重试(最多 2 次)→ 成功后路由。
    全程离线、确定性 mock——这也是 day07 eval 的雏形。

先自己写,再运行。

要点(总纲 S1/S8):
    - Agent 闭环里「决策层」的输出永远是字符串;契约负责把它变合法,决定权在你手里。
    - 把"模型边界"和"确定逻辑"分层:模型只返回文本,校验/路由是确定逻辑 → 可单测。
"""
import json
import re
from pydantic import BaseModel, Field, ValidationError


class Route(BaseModel):
    action: str = Field(pattern="^(search|summarize|stop)$", description="下一步动作")
    query: str = Field(default="", description="若 action=search 时的关键词")


class FakeLLM:
    """离线模型节点:前 fail_until 次输出「模型幻觉」,之后恢复正常。"""

    def __init__(self, fail_until: int = 0) -> None:
        self.call = 0
        self.fail_until = fail_until

    def respond(self, user: str) -> str:
        self.call += 1
        if self.call <= self.fail_until:
            return '没问题我来办 -> {"action":"dance","query":"x"}'   # 常见幻觉:动作不在枚举
        return '好的,{"action":"search","query":"' + user + '"}'


def extract_json(text: str) -> dict:
    """从模型文本里抠出第一个 {...} 并解析成 dict。"""
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("未找到 JSON")
    return json.loads(m.group(0))


def run_agent(user: str, llm: FakeLLM, max_retries: int = 2) -> str:
    for attempt in range(max_retries + 1):
        raw = llm.respond(user)
        try:
            data = extract_json(raw)
            r = Route.model_validate(data)
        except (ValueError, json.JSONDecodeError, ValidationError) as e:
            print(f"  第{attempt + 1}次失败: {type(e).__name__}: {e}")
            continue
        if r.action == "search":
            return f"search('{r.query}')"
        return f"noop({r.action})"
    return "fallback: 默认 summarize"


def demo() -> None:
    print("模型稳定        :", run_agent("python agents", FakeLLM(fail_until=0)))
    print("先脏后修好      :", run_agent("httpx vs requests", FakeLLM(fail_until=1)))
    print("连续脏(耗光重试) :", run_agent("langgraph", FakeLLM(fail_until=99)))


if __name__ == "__main__":
    demo()
    print("\nPASS: ex05 模型边界最小闭环(校验→重试→路由→兜底)全跑通")