#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day03-Ex03 · 单个失败不炸全局:任务级隔离
=====================================================
题目:
    3 个并行子任务,其中一个注定失败。要求:成功的 2 个正常收结果、失败的那个单独处理,
    整个调用不抛异常——这是 agent 并发调"多数据源检索"时的生产级底线。
"""
import asyncio


async def fetch(name: str, fail: bool = False) -> str:
    await asyncio.sleep(0.1)
    if fail:
        raise ValueError(f"{name} 404")
    return f"{name} 数据"


async def main() -> None:
    names = ["源0", "源1", "源2"]
    tasks = [asyncio.create_task(fetch(n, fail=(n == "源1"))) for n in names]

    results = {}
    for name, t in zip(names, tasks):
        try:
            results[name] = await t
        except ValueError as e:
            results[name] = f"FAILED({e}) 已隔离"     # 只记失败,不连累别的

    print("隔离后结果:", results)
    ok = sum(1 for v in results.values() if not v.startswith("FAILED"))
    assert ok == 2, "成功的 2 个必须完整返回"
    print(f"成功 {ok}/3,失败单点已隔离 → 主流程不受影响")


if __name__ == "__main__":
    asyncio.run(main())
    print("\nPASS: ex03 任务级隔离(单点失败不炸全局)")