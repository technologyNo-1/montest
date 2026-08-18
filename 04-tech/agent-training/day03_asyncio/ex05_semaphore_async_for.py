#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day03-Ex05 · 限流(Semaphore)+ async for:10 个请求撞进 3 条并发车道
=====================================================
题目:
    有 10 个待处理的切片,LLM 并发上限 3。用 asyncio.Semaphore(3) 限流压制并发度,
    再用 async for 流式消费一个异步生成器——两个都要跑通。
"""
import asyncio


async def embed(slice_id: int, sem: asyncio.Semaphore) -> int:
    async with sem:                       # 占用一个并发车位
        await asyncio.sleep(0.1)
        return slice_id


async def embed_stream(items: list[int], sem: asyncio.Semaphore):
    """异步生成器:边算边 yield(流式透传,day04 的主角)。"""
    for it in items:
        async with sem:
            await asyncio.sleep(0.05)
            yield it * 2


async def main() -> None:
    sem = asyncio.Semaphore(3)

    # ① 限流并发批:10 个任务只占 3 条车道 → 总耗时 ≈ 4 波 × 0.1s
    t0 = asyncio.get_running_loop().time()
    results = await asyncio.gather(*(embed(i, sem) for i in range(10)))
    dt = asyncio.get_running_loop().time() - t0
    print(f"① 10 任务限流 3:耗时 {dt:.2f}s(串行需 ~1.0s;裸并发 ~0.1s),结果 {len(results)} 条")

    # ② async for 流式消费
    got = [v async for v in embed_stream([1, 2, 3, 4], sem)]
    print("② async for 流式: ", got)

    assert 0.1 < dt < 1.0, "限流后耗时应介于裸并发与串行之间"
    assert got == [2, 4, 6, 8]


if __name__ == "__main__":
    asyncio.run(main())
    print("\nPASS: ex05 Semaphore 限流保并发度 + async for 流式消费")