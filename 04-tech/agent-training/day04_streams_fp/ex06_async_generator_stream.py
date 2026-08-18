#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day04-Ex06 · async 生成器 + 装饰器组合:SSE 流式雏形
=====================================================
题目:
    FastAPI 的 SSE(Server-Sent Events)端点本质就是 async 生成器。写:
      ① 一个模拟 token 流的 async gen
      ② 一个 @stream_log 装饰器叠加观测
      ③ 一个 @throttle 装饰器做节流(防打爆消费端)
    async for 消费三者——【流式透传 + 横切关注点】的组合拳。
"""
import asyncio
from functools import wraps


async def token_stream(text: str, chunk: int = 4):
    for i in range(0, len(text), chunk):
        await asyncio.sleep(0.05)
        yield text[i:i + chunk]


def stream_log(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"  [stream] 开始: {func.__name__}")
        async for piece in func(*args, **kwargs):
            print(f"  [stream] 片段: {piece!r}")
            yield piece
    return wrapper


def throttle(limit: float):
    def deco(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async for piece in func(*args, **kwargs):
                await asyncio.sleep(limit)
                yield piece
        return wrapper
    return deco


@stream_log
async def annotated_stream():
    async for p in token_stream("你好世界这是一个流式输出"):
        yield p


@throttle(0.02)
async def slowed_stream():
    async for p in token_stream("abc"):
        yield p


async def main() -> None:
    print("== 带日志的流 ==")
    got = "".join([p async for p in annotated_stream()])
    print("拼回:", got)

    print("== 节流流 ==")
    print(list([p async for p in slowed_stream()]))


if __name__ == "__main__":
    asyncio.run(main())
    print("\nPASS: ex06 async 生成器 + 装饰器组合(SSE 雏形)")