#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day06-Ex01 · 最小图:看清 StatsGraph 的骨头
=====================================================
题目:
    搭一个只有单个节点的图:START → bump(把 n+1)→ END。理解四块骨架:
      State(数据) / Node(逻辑) / Edge(连线) / Compiled app(可调用)。
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class Ctx(TypedDict):
    n: int


def bump(st: Ctx) -> dict:
    return {"n": st["n"] + 1}               # 节点只返回增量,框架负责合并进 State


if __name__ == "__main__":
    # 1. 建图
    g = StateGraph(Ctx)
    # 2. 加节点
    g.add_node("bump", bump)
    # 3. 连线:入口 → 节点 → 出口
    g.add_edge(START, "bump")
    g.add_edge("bump", END)
    # 4. 编译后才是可调用对象
    app = g.compile()

    final = app.invoke({"n": 0})
    print("invoke 结果:", final)
    assert final == {"n": 1}, "节点返回值应合并进 State"

    # 结构可视化:看图上有什么
    print("编译后可用方式: invoke / stream(逐步) —— 图把流程变成数据。")
    print("\nPASS: ex01 最小图跑通(State/Node/Edge/compile 四件套)")