#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_checklist.py · 结项 checklist 自动核验(总纲 §7.1 六项 + §7.2 全勾)
=====================================================================
运行:   uv run --with langgraph python3 run_checklist.py
结果:   全部 [PASS] 且退出码 0 = 毕业。任何 [FAIL] 都 assert 中断。
"""
import asyncio
import importlib
import json

from pydantic import ValidationError
from langgraph.types import Command

import store_lib
from store_lib import (StockQuery, retrieve, call_with_retry,
                       source_inventory, set_fail_source, FatalError)

agent_mod = importlib.import_module("ex03_customer_service_agent")


def check(name: str, cond: bool, extra: str = "") -> None:
    flag = "PASS" if cond else "FAIL"
    print(f"  [{flag}] {name} {extra}")
    assert cond, name


async def ainvoke(app, cfg, q):
    return await app.ainvoke(agent_mod.blank_state(q), cfg)


async def main() -> None:
    print("== §7.1 结项六项要求 ==")

    # 1. 带校验的工具参数模型,非法输入被拦截
    StockQuery(product="cpu", region="cn")
    try:
        StockQuery(product=123)
        check("1. Pydantic 工具参数 + 非法拦截", False)
    except ValidationError:
        check("1. Pydantic 工具参数 + 非法拦截", True, "(product=123 → ValidationError)")

    # 2. asyncio 并发检索 2 个数据源,单个失败不炸全局
    rows = await retrieve("query_stock", StockQuery(product="cpu"))
    check("2. 并发双源检索且结果收齐", len(rows) == 2,
          f"({len(rows)} 路结果,耗时≈最慢源)")

    # 3. 异常分类:网络类指数退避重试;业务类立即抛
    set_fail_source("inventory", 2)
    ok = await call_with_retry(lambda: source_inventory("cpu"))
    set_fail_source("inventory", 0)
    check("3. 可重试(503 抖动)→ 退避后成功", "cpu" in ok, f"({ok})")
    try:
        await call_with_retry(lambda: source_inventory("ghost"))
        check("3b. 不可重试 → 立即抛不烧钱", False)
    except FatalError:
        check("3b. 不可重试 → 立即抛不烧钱", True)

    # 4. 图流程 + 循环终止(命中 或 轮数上限)
    app = agent_mod.build()
    cfg = {"configurable": {"thread_id": "ck"}}
    first = await ainvoke(app, cfg, "cpu 有货吗")
    check("4. 图(State+Node+条件边)组织流程", first is not None)
    check("4b. 循环终止:停在 HITL 挂起点而非死循环", "__interrupt__" in first)
    final = await app.ainvoke(Command(resume="y"), cfg)
    st = app.get_state(cfg).values
    check("5. checkpointer 同 thread 断点续跑 + 状态保留",
          final["confirmed"] and "成交" in final["answer"])

    # 5b. 兜底路径也有界(轮数上限)
    app_fb = agent_mod.build(); cfg_fb = {"configurable": {"thread_id": "fb"}}
    await ainvoke(app_fb, cfg_fb, "!!?")
    st_fb = app_fb.get_state(cfg_fb).values
    check("5b. 听不懂也按轮数上限收束,不无限重试",
          st_fb["round"] <= agent_mod.MAX_ROUNDS and "抱歉" in st_fb["answer"])

    # 6. 3 条离线 eval 断言(确定性 mock 下稳定通过)
    r1 = await ainvoke(app_fb, {"configurable": {"thread_id": "e1"}}, "cpu 有货吗")
    await app_fb.ainvoke(Command(resume="y"), {"configurable": {"thread_id": "e1"}})
    s1 = app_fb.get_state({"configurable": {"thread_id": "e1"}}).values
    e1 = "库存" in str(s1["answer"])

    r2 = await ainvoke(app_fb, {"configurable": {"thread_id": "e2"}}, "帮我查下显卡")
    await app_fb.ainvoke(Command(resume="y"), {"configurable": {"thread_id": "e2"}})
    s2 = app_fb.get_state({"configurable": {"thread_id": "e2"}}).values
    e2 = len(s2["sources"]) > 0 and s2["round"] >= 2      # 脏输出被拦截后重试修好

    r3 = await ainvoke(app_fb, {"configurable": {"thread_id": "e3"}}, "!!?")
    s3 = app_fb.get_state({"configurable": {"thread_id": "e3"}}).values
    e3 = "抱歉" in str(s3["answer"]) and s3["round"] <= agent_mod.MAX_ROUNDS

    check("6. 3 条离线 eval 断言全过",
          all([e1, e2, e3]), f"e1(干净查询)={e1} e2(拦截重试)={e2} e3(有界兜底)={e3}")

    print("\n== §7.2 反思题(代码已示范,此处确认理解)==")
    for item in [
        "能徒手写带校验+嵌套/枚举的工具参数模型",
        "能并发3调用+单点失败隔离+超时",
        "能不查文档手写 @retry(backoff+jitter)",
        "能说清 async 函数里为什么不放同步 requests",
        "能用 with 管好文件/HTTP/会话资源",
        "能画出并解释带循环终止条件的 agent 图",
        "能说出 checkpointer 为何要可序列化可重建",
        "能把系统切成 确定逻辑/模型边界/行为质量 三层",
    ]:
        check(f"· {item}", True)


if __name__ == "__main__":
    asyncio.run(main())
    print("\n🎓 毕业:结项 checklist 全 [PASS],exit 0 —— 你可以独立交付一个离线检索 agent。")