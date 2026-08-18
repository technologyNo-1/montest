#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day04-Ex04 · ⛳ 过关题:不查文档手写 @retry(backoff + jitter)
=====================================================
题目:
    写一个 @retry(max_attempts=4, base_delay=0.05, jitter=0.02) 装饰器:
      1. 函数抛指定异常 → 退避等待后重试
      2. 退避 = base_delay * 2^attempt + random.uniform(0, jitter)
      3. 重试耗尽后把最后一次异常往外抛
    过关标准:不看提示能徒手写出(这是 agent 可靠性的原子单元)。
"""
import time
import random
from functools import wraps


def retry(max_attempts: int = 4, base_delay: float = 0.05,
          jitter: float = 0.02, exc=Exception):
    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exc as e:
                    last = e
                    if attempt == max_attempts - 1:
                        break
                    delay = base_delay * (2 ** attempt) + random.uniform(0, jitter)
                    time.sleep(delay)
            raise last
        return wrapper
    return deco


class _FlakySvc:
    def __init__(self, fail_times: int) -> None:
        self.n = fail_times

    @retry(max_attempts=4, base_delay=0.02, exc=RuntimeError)
    def call(self) -> str:
        if self.n > 0:
            self.n -= 1
            raise RuntimeError("瞬时失败")
        return "ok,成功了"


def demo() -> None:
    print("失败 2 次后成功:", _FlakySvc(2).call())
    try:
        _FlakySvc(99).call()
    except RuntimeError as e:
        print("持续失败 → 重试耗尽后抛出:", e)


if __name__ == "__main__":
    demo()
    print("\nPASS: ex04 手写 @retry(backoff+jitter) 全链路")