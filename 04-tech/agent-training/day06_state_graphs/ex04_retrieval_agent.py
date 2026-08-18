#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day06-Ex04 · ⛳ 过关题:检索 agent 图,含两种循环终止路径
=====================================================
题目:
    画并跑通"检索 agent"图:用户提问 → 检索(可能是空的)→ 判断 →
    有命中/到上限 → 回答;否则 → 再查一次。要求:
      ① 循环有终止条件(命中 或 轮数上限,两条路都能停)
      ② 全部节点离线 mock,确定性可断言
    过关标准:不看答案能画出 State/Node/条件边,并说清为什么要轮数上限。
"""
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END


MAX_ROUNDS = 3


class AgentState(TypedDict):
    query: str
    messages: Annotated[list, operator.add]     # 消息历史
    iter_count: int                              # 检索轮数
    hits: list                                   # 命中的切片


def make_fake_store(hit_at: "int | None"):
    """离线语料:只在第 hit_at 轮返回命中;None=永远不命中。"""

    def retrieve(st: AgentState) -> dict:
        n = st["iter_count"] + 1
        found = hit_at is not None and n >= hit_at
        hit = f"<切片{n}> asyncio 是 python 异步库" if found else None
        return {
            "iter_count": n,
            "hits": [hit] if hit else [],
            "messages": [f"工具/检索第 {n} 轮{'命中' if hit else '无结果'}"],
        }

    return retrieve


def answer(st: AgentState) -> dict:
    top = st["hits"][0] if st["hits"] else "无"
    return {"messages": [f"模型/基于检索({top})生成回答"]}


def route(st: AgentState) -> str:
    # 终止条件两条路:① 有命中 ② 轮数到上限 —— 缺一都会死循环
    if st["hits"]:
        return "answer"
    if st["iter_count"] >= MAX_ROUNDS:
        return "answer"
    return "retrieve"


def build(hit_at: "int | None"):
    g = StateGraph(AgentState)
    g.add_node("retrieve", make_fake_store(hit_at))
    g.add_node("answer", answer)
    g.add_edge(START, "retrieve")
    g.add_conditional_edges("retrieve", route, {"retrieve": "retrieve", "answer": "answer"})
    g.add_edge("answer", END)
    return g.compile()


def run(hit_at, label):
    app = build(hit_at)
    final = app.invoke({"query": "asyncio", "messages": ["用户:asyncio 是什么"],
                        "iter_count": 0, "hits": []})
    print(f"[{label}] 轮数={final['iter_count']} 消息={len(final['messages'])} 条")
    for m in final["messages"]:
        print("   ·", m)
    assert final["iter_count"] == MAX_ROUNDS, "两条终止路径都必须以检索 → 回答收束"
    assert final["messages"][-1].startswith("模型/"), "最后一条必须是模型回答"
    return final


if __name__ == "__main__":
    print("== 图结构 ==")
    print("   START → retrieve ──(route:命中?→answer / 轮数到顶→answer / 否则→retrieve)── answer → END")
    f = run(3, "第 3 轮命中(按命中终止)")
    f2 = run(None, "永不命中(按轮数上限终止)")
    print("\n两条终止路径都收束于 iter_count=3 —— 循环终止由『条件边』保证,框架本身不管")
    print("\nPASS: ex04 检索 agent 图(命中 / 上限 双终止)")