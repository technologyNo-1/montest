#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day05-Ex03 · 状态可序列化往返:dict → JSON → dict
=====================================================
题目:
    checkpointer 持久化要求状态「可序列化、可重建」(总纲 S6)。完成:
      ① 简单 dict 往返
      ② Pydantic 模型 model_dump_json → model_validate_json 往返
      ③ 踩坑:set / datetime 不能直接 json.dumps → 给出约定好的转换方案
"""
import json
from datetime import datetime
from pydantic import BaseModel


def part1() -> None:
    state = {"messages": ["a", "b"], "retries": 1, "cwd": "/tmp"}
    back = json.loads(json.dumps(state, ensure_ascii=False))
    assert back == state
    print("① dict 往返 OK:", back)


class AgentState(BaseModel):
    messages: list[str]
    retries: int = 0
    last_seen: datetime | None = None


def part2() -> None:
    state = AgentState(messages=["a"], last_seen=datetime.now())
    s = state.model_dump_json()                  # 直接产出可存储的 JSON 字符串
    back = AgentState.model_validate_json(s)      # 重建回对象
    print("② Pydantic 往返 OK: messages=", back.model_dump()["messages"],
          "| last_seen 类型=", type(back.last_seen).__name__)


def part3() -> None:
    data = {"tags": {"x", "y"}, "created": datetime.now()}
    try:
        json.dumps(data)
    except TypeError as e:
        print("③ 坑:默认 json.dumps 不支持 set/datetime →", e)

    # 约定转换:set→sorted list;datetime→isoformat(业界标准约定)
    data2 = {"tags": sorted(data["tags"]), "created": data["created"].isoformat()}
    back = json.loads(json.dumps(data2))
    rebuilt = {"tags": set(back["tags"]), "created": datetime.fromisoformat(back["created"])}
    print("   约定转换后往返 OK:", back, "| 还原成 set/datetime:", type(rebuilt["tags"]).__name__, rebuilt["created"].date())


def demo() -> None:
    part1()
    part2()
    part3()


if __name__ == "__main__":
    demo()
    print("\nPASS: ex03 状态序列化往返(set/datetime 已有转换方案)")