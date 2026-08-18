#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day06-Ex05 · 并行扇出 + 汇合合并:一图两源
=====================================================
题目:
    两个数据源并行检索,结果在 merge 节点汇合。要点:
      ① 同一时刻两个分支并行(异步 IO 层面是并发)
      ② merge 用 reducer(operator.add)收集两路结果,再统一加工
      ③ 多 agent 协作 / 多源检索,靠的就是这个「扇出-汇合」骨架
"""
import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END


class St(TypedDict):
    reviews: Annotated[list, operator.add]      # 两路结果都 append 进来


def src_a(st: St) -> dict:
    return {"reviews": ["A 源:命中 3 条"]}


def src_b(st: St) -> dict:
    return {"reviews": ["B 源:命中 5 条"]}


def merge(st: St) -> dict:
    combined = " | ".join(st["reviews"])
    return {"reviews": [f"合并置顶: {combined}"]}


if __name__ == "__main__":
    g = StateGraph(St)
    g.add_node("src_a", src_a)
    g.add_node("src_b", src_b)
    g.add_node("merge", merge)
    g.add_edge(START, "src_a")        # 入口一路扇出
    g.add_edge(START, "src_b")
    g.add_edge("src_a", "merge")      # 两路汇合
    g.add_edge("src_b", "merge")
    g.add_edge("merge", END)
    app = g.compile()

    final = app.invoke({"reviews": []})
    print("最终 reviews:", final["reviews"])
    assert len(final["reviews"]) == 3, "两路结果 + 合并置顶"
    print("并行扇出-汇合成功:两路独立结果被 reducer 收集,再合并加工")
    print("\nPASS: ex05 并行分支 + 汇合(扇出/合并骨架)")