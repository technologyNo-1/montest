#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day07-Ex03 · 检索式客服 agent 完整图:契约 + 并发 + 重试 + 循环终止 + 断点续跑 + HITL
================================================================================
结项要求 4 & 5:
  4) 用图(State + Node + 条件边)组织流程,循环必须有终止条件
  5) checkpointer 存状态,同 thread 断点可续跑;并含人机协作挂起点(HITL)
集成 ex01(契约)+ ex02(并发/重试)为一个可调用的检索式客服 agent。
"""
import asyncio
import operator
from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command

from store_lib import TOOL_SCHEMAS, run_tool, fake_llm_toolcall, retrieve

MAX_ROUNDS = 3


class AgentState(TypedDict):
    q: str
    round: int
    tool_raw: str
    valid: bool
    action: str
    params_json: str
    sources: list
    confirmed: bool
    answer: str
    turns: Annotated[list, operator.add]     # 消息历史(追加不覆盖)


def blank_state(q: str) -> AgentState:
    return {"q": q, "round": 0, "tool_raw": "", "valid": False, "action": "",
            "params_json": "", "sources": [], "confirmed": False,
            "answer": "", "turns": []}


# ---- 节点 ----
def parse(st: AgentState) -> dict:
    r = st["round"] + 1
    raw = fake_llm_toolcall(st["q"], r)        # 离线"模型"输出工具调用(可能脏)
    return {"round": r, "tool_raw": raw,
            "turns": [f"模型/输出工具调用: {raw}"]}


def validate(st: AgentState) -> dict:
    try:
        action, params = run_tool(st["tool_raw"])   # Pydantic 契约拦截非法参数
        return {"valid": True, "action": action,
                "params_json": params.model_dump_json(),
                "turns": [f"工具契约/校验通过 → {action}"]}
    except Exception as e:                          # JSONDecodeError/ValidationError/FatalError
        return {"valid": False, "action": "", "params_json": "",
                "turns": [f"工具契约/拦截: {type(e).__name__}"]}


def route_validate(st: AgentState) -> str:
    if st["valid"]:
        return "retrieve"
    if st["round"] >= MAX_ROUNDS:                   # ← 循环终止:条件边的第二道闸
        return "answer"
    return "parse"                                  # 把错误回注,让模型重解析


async def do_retrieve(st: AgentState) -> dict:
    params = TOOL_SCHEMAS[st["action"]].model_validate_json(st["params_json"])
    rows = await retrieve(st["action"], params)     # 并发双源 + 重试 + 隔离
    return {"sources": rows, "turns": [f"工具/并发双源: {' | '.join(rows)}"]}


def ask_confirm(st: AgentState) -> dict:
    ans = interrupt(f"客服: 已查到——{('；'.join(st['sources']))}。确认成交请回 y,否则回 n。")
    return {"confirmed": str(ans).lower().startswith("y"),
            "turns": [f"用户/确认: {ans}"]}


def answer(st: AgentState) -> dict:
    if not st["valid"]:
        return {"answer": "抱歉,我未能理解您的请求(工具参数校验连续失败)。请换个问法。",
                "turns": ["客服/兜底回答"]}
    if st["confirmed"]:
        return {"answer": f"已确认成交: {('；'.join(st['sources']))}。感谢惠顾!",
                "turns": ["客服/成交"]}
    return {"answer": f"已记录需求: {('；'.join(st['sources']))}。回复 y 可立即下单。",
            "turns": ["客服/待确认"]}


# ---- 图 ----
def build():
    g = StateGraph(AgentState)
    g.add_node("parse", parse)
    g.add_node("validate", validate)
    g.add_node("retrieve", do_retrieve)
    g.add_node("confirm", ask_confirm)
    g.add_node("answer", answer)

    g.add_edge(START, "parse")
    g.add_edge("parse", "validate")
    g.add_conditional_edges("validate", route_validate,
                            {"parse": "parse", "retrieve": "retrieve", "answer": "answer"})
    g.add_edge("retrieve", "confirm")
    g.add_edge("confirm", "answer")
    g.add_edge("answer", END)
    return g.compile(checkpointer=MemorySaver())     # 断点续跑的基础


async def main() -> None:
    # 场景A · 干净查询 + 用户确认成交
    print("== 场景A · 干净查询 + HITL 确认 ==")
    appA = build(); cfgA = {"configurable": {"thread_id": "tA"}}
    first = await appA.ainvoke(blank_state("cpu 有货吗"), cfgA)
    print("  第一次 invoke 停在 HITL:", str(first["__interrupt__"][0].value))
    final_a = await appA.ainvoke(Command(resume="y"), cfgA)
    for t in final_a["turns"]:
        print("   ·", t)
    print("  最终回答:", final_a["answer"])
    assert final_a["confirmed"] and "成交" in final_a["answer"]

    # 场景B · 模型第一轮脏输出 → 契约拦截 → 重解析修好 → 检索 → 待确认
    print("\n== 场景B · 脏输出被拦截后重试修好 ==")
    appB = build(); cfgB = {"configurable": {"thread_id": "tB"}}
    first_b = await appB.ainvoke(blank_state("帮我查下显卡"), cfgB)
    final_b = await appB.ainvoke(Command(resume="n"), cfgB)
    print("  轮数:", final_b["round"], "| 校验节点备注:",
          [t for t in final_b["turns"] if "拦截" in t or "通过" in t])
    print("  最终回答:", final_b["answer"])
    assert final_b["valid"] and "记录需求" in final_b["answer"]

    # 断点续跑 · 同 thread(tB) 压下一条新咨询,历史状态保留
    print("\n== 断点续跑:同 thread(tB)新咨询,历史保留 ==")
    second = await appB.ainvoke(blank_state("价格多少"), cfgB)
    turns_after = second["turns"]
    assert any("query_price" in t for t in turns_after)
    print("  历史 turns 累计:", len(turns_after), "条 | 含 query_price:",
          any("query_price" in t for t in turns_after))
    st = appB.get_state(cfgB).values
    print("  当前持久化状态摘要: q=", st["q"], "| 消息数=", len(st["turns"]))


if __name__ == "__main__":
    asyncio.run(main())
    print("\nPASS: ex03 结项 agent(契约/并发/重试/循环终止/断点续跑/HITL)全部跑通")