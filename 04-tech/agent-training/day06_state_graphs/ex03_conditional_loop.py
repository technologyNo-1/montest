#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day06-Ex03 · 条件路由 + 循环终止:让图自己决定下一步
=====================================================
题目:
    一个"竭力改进"节点:每次尝试提升答案质量。用 add_conditional_edges 让节点
    自己决定下一步;但条件函数必须给【终止条件】——轮数上限(MAX_ROUNDS)。
    跑通后验证:恰好跑 MAX_ROUNDS 次就停,绝不死循环。
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class St(TypedDict):
    attempts: int
    last: str


MAX_ROUNDS = 5


def work(st: St) -> dict:
    n = st["attempts"] + 1
    return {"attempts": n, "last": f"第 {n} 次打磨"}


def route(st: St) -> str:
    if st["attempts"] >= MAX_ROUNDS:
        return "end"                    # ← 终止条件:轮数到顶
    return "work"


if __name__ == "__main__":
    g = StateGraph(St)
    g.add_node("work", work)
    g.add_edge(START, "work")
    g.add_conditional_edges("work", route, {"work": "work", "end": END})
    app = g.compile()

    final = app.invoke({"attempts": 0, "last": ""})
    print("最终:", final)
    assert final["attempts"] == MAX_ROUNDS, "必须在轮数上限处终止"
    assert final["last"] == f"第 {MAX_ROUNDS} 次打磨"
    print(f"循环恰好跑了 {MAX_ROUNDS} 轮后终止 —— 条件边 + 上限 = 防死循环")
    print("\nPASS: ex03 条件路由 + 循环终止(轮数上限)")