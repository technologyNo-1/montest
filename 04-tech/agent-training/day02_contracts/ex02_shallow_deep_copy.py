#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day02-Ex02 · 深浅拷贝:状态快照被"共享内层"污染的坑
=====================================================
题目:
    你的 agent 把 state["messages"] 打两份快照给两个并行分支,期望互不影响。
    但浅拷贝只复制外层、内层 list 仍共享——一个分支改写,另一份也变。
    用 copy.deepcopy(Python 层面) 与 Pydantic 的 model_copy(deep=True) 正确防护。

先想清楚:并行分支、persistence 快照、CLI 回滚,全是深拷贝的高频场景;图的状态外置更敏感。
"""
import copy
from typing import TypedDict
from pydantic import BaseModel


class State(TypedDict):
    messages: list
    budget: int


def buggy() -> None:
    """踩坑现场:dict.copy() 浅拷贝,内层 messages 共享。"""
    state: State = {"messages": [{"role": "user", "text": "hi"}], "budget": 10}
    branch = state.copy()                                  # 浅拷贝
    branch["messages"].append({"role": "assistant", "text": "hello"})
    print("原始 state 消息数:", len(state["messages"]), "← 被分支污染了!")


def safe() -> None:
    """修复:copy.deepcopy 深拷贝,整棵树独立。"""
    state: State = {"messages": [{"role": "user", "text": "hi"}], "budget": 10}
    branch = copy.deepcopy(state)
    branch["messages"].append({"role": "assistant", "text": "hello"})
    assert len(state["messages"]) == 1 and len(branch["messages"]) == 2
    print("deepcopy 后: 原始", len(state["messages"]), "| 分支", len(branch["messages"]), "互不影响")


# ---------- Pydantic 侧:model_copy(deep=True) ----------
class Msg(BaseModel):
    role: str
    text: str


class Session(BaseModel):
    messages: list[Msg]
    budget: int = 0


def pydantic_variant() -> None:
    s = Session(messages=[Msg(role="user", text="hi")])
    snap = s.model_copy(deep=True)                        # 深度复制
    snap.messages.append(Msg(role="assistant", text="hello"))
    print("Pydantic model_copy(deep=True): 原件", len(s.messages), "| 快照", len(snap.messages))


if __name__ == "__main__":
    print("== 踩坑 ==")
    buggy()
    print("== 修复 ==")
    safe()
    print("== Pydantic 版 ==")
    pydantic_variant()
    print("\nPASS: ex02 深浅拷贝语义正确,状态快照被隔离")