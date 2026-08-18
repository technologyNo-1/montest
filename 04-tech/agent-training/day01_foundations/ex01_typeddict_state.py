#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day01-Ex01 · Agent 状态与 reducer:消息「追加不覆盖」
=====================================================
题目:
    给一个"检索 agent"定义状态。每次节点返回新消息时,必须把新消息【追加】到历史,
    而不是【覆盖】整段对话。请用 TypedDict + 手写 reducer 完成,并对照"没写 reducer"的坑。

先自己写,再运行。

要点(总纲 S6 / Python.md §3):
    - TypedDict 只在类型层面描述 dict,【运行时不校验】——写错 key 悄悄丢数据。
    - reducer = 合并策略函数:状态里同一 key 返回新值时,「覆盖还是追加」由它说了算。
    - LangGraph 的 add_messages 就是这个思路;这里不依赖框架,徒手实现一次它的语义。
"""
from typing import TypedDict, Annotated, NotRequired


class RetrievalState(TypedDict):
    """检索 agent 的图状态。Annotated 第二个参数是 reducer 的占位(教学简化)。"""
    messages: Annotated[list, "reducer=append_messages"]
    query: str
    hits: NotRequired[list[dict]]
    retries: int


def append_messages(current: list, incoming) -> list:
    """合并策略:把节点返回的新消息追加到历史末尾(不覆盖)。"""
    cur = list(current) if current else []
    if isinstance(incoming, list):
        return cur + list(incoming)
    return cur + [incoming]


# ---- 模拟「图的节点结果合并半步」:有 reducer 的 key 走 reducer,否则覆盖 ----
def apply_node(state: RetrievalState, partial: dict) -> RetrievalState:
    merged = dict(state)
    for k, v in partial.items():
        if k == "messages":
            merged["messages"] = append_messages(state.get("messages"), v)
        else:
            merged[k] = v          # 无 reducer 的 key 直接覆盖
    return merged


def demo() -> None:
    state: RetrievalState = {"messages": [], "query": "", "retries": 0}

    state = apply_node(state, {"query": "python asyncio 是什么",
                               "messages": ["用户:python asyncio 是什么"]})
    state = apply_node(state, {"messages": ["模型:asyncio 是 Python 的异步库…"]})
    state = apply_node(state, {"messages": ["工具:命中 3 条文档"]})

    assert len(state["messages"]) == 3, "消息必须追加,不能覆盖"
    print("追加后的历史:")
    for m in state["messages"]:
        print("  ·", m)

    # ---- 反面:没有 reducer 的写法(新手丢历史的根源) ----
    naive = {"messages": []}
    step = lambda s, partial: {**s, **partial}           # 直接覆盖
    naive = step(naive, {"messages": ["用户:问题"]})
    naive = step(naive, {"messages": ["模型:回答"]})
    print("\n反面(直接覆盖)只剩 1 条:", naive["messages"])
    assert len(naive["messages"]) == 1


if __name__ == "__main__":
    demo()
    print("\nPASS: ex01 状态 + reducer 追加语义正确")