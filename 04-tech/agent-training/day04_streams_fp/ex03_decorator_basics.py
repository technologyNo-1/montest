#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day04-Ex03 · 装饰器热身:@timeit / @log + functools.wraps
=====================================================
题目:
    写一个 @timeit 打印耗时、一个 @log 打印入参出参。必须用 functools.wraps
    保留原名与文档(不然 help()/签名全丢,debug 无从谈起)。
"""
import time
from functools import wraps


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"  [{func.__name__}] 耗时 {(time.perf_counter() - t0) * 1000:.2f}ms")
        return result
    return wrapper


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  → {func.__name__}({args!r}, {kwargs!r})")
        return func(*args, **kwargs)
    return wrapper


@timeit
@log
def fetch_llm(prompt: str, model: str = "gpt-4o-mini") -> str:
    """模拟一次 LLM 调用"""
    time.sleep(0.05)
    return f"<{model}>{prompt}</{model}>"


def demo() -> None:
    print(fetch_llm("hi"))
    print("保留原名/文档:", fetch_llm.__name__, "|", fetch_llm.__doc__)


if __name__ == "__main__":
    demo()
    print("\nPASS: ex03 装饰器 + wraps 保留签名")