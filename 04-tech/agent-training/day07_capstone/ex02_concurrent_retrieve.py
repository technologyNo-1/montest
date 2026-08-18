#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day07-Ex02 · 并发检索 + 异常分类 + 指数退避重试
=====================================================
结项要求 2 & 3:
  2) asyncio 并发检索 2 个数据源(离线用 sleep 模拟)
  3) 自定义异常区分可重试/不可重试,网络类错误指数退避重试
"""
import asyncio
from store_lib import (set_fail_source, source_inventory, source_warehouse,
                       call_with_retry, retrieve, StockQuery, FatalError)


async def scenario_a() -> None:
    """并发双源:总耗时≈最慢源(证明并发),结果两路都到。"""
    q = StockQuery(product="cpu", region="cn")
    t0 = asyncio.get_running_loop().time()
    rows = await retrieve("query_stock", q)
    dt = asyncio.get_running_loop().time() - t0
    print(f"  并发双源耗时 {dt:.2f}s(< 串行 0.22s):")
    for r in rows:
        print("   ·", r)
    assert len(rows) == 2


async def scenario_b() -> None:
    """网络抖动:库存源先抖 2 次,重试后成功(指数退避,可重试)。"""
    set_fail_source("inventory", 2)
    ok = await call_with_retry(lambda: source_inventory("cpu"))
    print("  抖动 2 次后重试成功:", ok)
    assert "cpu" in ok


async def scenario_c() -> None:
    """不可重试:商品不存在 → FatalError 立即抛,不重试不烧钱。"""
    try:
        await call_with_retry(lambda: source_inventory("nobody"))
    except FatalError as e:
        print("  不可重试立即上报:", e)


async def main() -> None:
    print("== A. 并发双源 ==");   await scenario_a()
    print("== B. 抖动重试 ==");   await scenario_b()
    print("== C. 不可重试 ==");   await scenario_c()


if __name__ == "__main__":
    asyncio.run(main())
    print("\nPASS: ex02 并发检索 + 异常分类 + 指数退避重试")