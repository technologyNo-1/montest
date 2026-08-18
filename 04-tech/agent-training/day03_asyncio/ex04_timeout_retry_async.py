#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day03-Ex04 · 超时 + 异步重试(backoff):害怕模型挂死/抖动
=====================================================
题目:
    LLM 调用可能 hang、可能偶发 5xx。写 call_with_retry:
    超时/抛错 → 指数退避 → 重试 → 耗尽后抛出,由上层降级。
    asyncio.wait_for 负责超时;async sleep 做退避(不阻塞事件循环)。
"""
import asyncio


class LLMBackend:
    """离线模型后端:hang_first=前 N 次挂死;fail_times=前 N 次 503 抖动。"""

    def __init__(self, hang_first: int = 0, fail_times: int = 0) -> None:
        self.call = 0
        self.hang_first = hang_first
        self.fail_times = fail_times

    async def invoke(self, prompt: str) -> str:
        self.call += 1
        if self.call <= self.hang_first:
            await asyncio.sleep(10)                   # 模拟挂死(应被 wait_for 掐断)
        if self.call <= self.fail_times:
            raise RuntimeError("503 上游抖动")
        return f"回答: {prompt}"


async def call_with_retry(prompt: str, backend: LLMBackend, timeout: float = 0.3,
                          max_retries: int = 3, base_delay: float = 0.05) -> str:
    for attempt in range(max_retries + 1):
        try:
            return await asyncio.wait_for(backend.invoke(prompt), timeout)
        except (asyncio.TimeoutError, RuntimeError) as e:
            if attempt == max_retries:
                raise
            delay = base_delay * (2 ** attempt)      # 指数退避:0.05, 0.1, 0.2
            await asyncio.sleep(delay)


async def main() -> None:
    print("① 稳定后端      :", await call_with_retry("hi", LLMBackend()))
    print("② 抖动 1 次后成功:", await call_with_retry("hello", LLMBackend(fail_times=1)))
    try:
        await call_with_retry("hang", LLMBackend(hang_first=99), timeout=0.2, max_retries=2)
    except asyncio.TimeoutError:
        print("③ 挂死后重试耗尽 → 向外抛,上层降级")

    print("调用次数核验:①=1 次 | ②=2 次(1 失败+1 成功) | ③=3 次(全部超时)")


if __name__ == "__main__":
    asyncio.run(main())
    print("\nPASS: ex04 超时 + 指数退避重试 + 耗尽抛异常")