#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day06-Ex02 · 图状态:消息「追加不覆盖」的正式写法
=====================================================
题目:
    LangGraph 的 State 是 TypedDict,默认每个 key 「后写覆盖先写」。
    消息历史必须 append:用 Annotated[list, operator.add] 声明 reducer,
    节点返回新消息时框架自动拼接而不是覆盖——不写 reducer 的丢历史根源(day01 提过)。
"""
import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END


class ChatState(TypedDict):
    messages: Annotated[list, operator.add]     # reducer:追加不覆盖
    turn: int                                    # 无 reducer:默认覆盖(取最后写者)


def step_user(st: ChatState) -> dict:
    return {"messages": ["用户:hi"], "turn": 1}


def step_llm(st: ChatState) -> dict:
    return {"messages": ["模型:hello"], "turn": 2}


if __name__ == "__main__":
    g = StateGraph(ChatState)
    g.add_node("user", step_user)
    g.add_node("llm", step_llm)
    g.add_edge(START, "user")
    g.add_edge("user", "llm")
    g.add_edge("llm", END)
    app = g.compile()

    final = app.invoke({"messages": [], "turn": 0})
    print("最终状态:", final)
    assert final["messages"] == ["用户:hi", "模型:hello"], "消息必须追加不覆盖"
    assert final["turn"] == 2, "无 reducer 的 key 为 last-writer-wins"
    print("messages 追加成功;turn 覆盖成功 —— reducer 与覆盖两种语义都验证")
    print("\nPASS: ex02 State reducer 语义(append 消息 + 覆盖标量)")