#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day03-Ex01 · async/await 基础:事件循环让 IO 等待变成并发
=====================================================
题目:
    模拟"调用 LLM"(0.3s)两次。分别用【同步串行】和【asyncio 并发】跑,对比总耗时。
    理解:agent 为什么"异步是默认项,不是优化项"(总纲 1.3 / S4)。
"""
import asyncio
import time


def fake_llm(name: str, delay: float) -> str:
    time.sleep(delay)                 # 同步版:真阻塞当前线程
    return f"{name} done"


async def a_fake_llm(name: str, delay: float) -> str:
    await asyncio.sleep(delay)        # 异步版:让出控制权,去干别的
    return f"{name} done"


def sync_version(n: int = 3) -> float:
    t0 = time.perf_counter()
    for i in range(n):
        fake_llm(f"llm-{i}", 0.3)
    return time.perf_counter() - t0


async def async_version(n: int = 3) -> float:
    t0 = time.perf_counter()
    await asyncio.gather(*(a_fake_llm(f"llm-{i}", 0.3) for i in range(n)))
    return time.perf_counter() - t0


async def main() -> None:
    s = sync_version()
    a = await async_version()
    print(f"同步串行 3 次: {s:.2f}s")
    print(f"异步并发 3 次: {a:.2f}s(约等于单次)")
    assert a < s, "并发必须显著快于串行"
    print(f"提速 {s / a:.1f}x —— agent 天生 I/O 密集,瓶颈在等待")


if __name__ == "__main__":
    asyncio.run(main())
    print("\nPASS: ex01 async/await 基础 + 并发提速验证")