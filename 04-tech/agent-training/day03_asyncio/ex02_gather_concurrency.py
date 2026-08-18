#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day03-Ex02 · asyncio.gather:一行并发 + 默认"一错全炸"
=====================================================
题目:
    并发调 3 个"模型节点"。展示:
      ① gather 并发:总耗时 ≈ 最慢单次(而不是三次之和)
      ② 默认 return_exceptions=False:一个子任务抛错 → 整个 gather 抛(其余结果全丢)
      ③ return_exceptions=True:错误以结果形式返回,不炸全局
"""
import asyncio


async def node(i: int, ok: bool = True) -> str:
    await asyncio.sleep(0.2)
    if not ok:
        raise RuntimeError(f"node-{i} 挂了")
    return f"node-{i} ok"


async def main() -> None:
    # ① 并发:总耗时 = 单次
    s = asyncio.get_running_loop().time()
    results = await asyncio.gather(node(0), node(1), node(2))
    dt = asyncio.get_running_loop().time() - s
    print("并发结果:", results, f"| 耗时 {dt:.2f}s(≈单次 0.2s)")

    # ② 默认:一个失败,全体陪葬
    try:
        await asyncio.gather(node(0), node(1, ok=False), node(2))
    except RuntimeError as e:
        print("默认行为:一个失败 → gather 整体抛:", e)

    # ③ return_exceptions=True:不抛,错误变成结果
    mixed = await asyncio.gather(node(0), node(1, ok=False), node(2),
                                 return_exceptions=True)
    shown = [type(r).__name__ if isinstance(r, BaseException) else r for r in mixed]
    print("return_exceptions=True:", shown)


if __name__ == "__main__":
    asyncio.run(main())
    print("\nPASS: ex02 gather 并发 + 默认炸全局 vs return_exceptions 对比")