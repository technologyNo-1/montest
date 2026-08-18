#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day05-Ex01 · 异常分类学:错误也是数据,分门别类才能决策
=====================================================
题目:
    agent 的失败要分两类:
      - 可重试:网络抖动 / 5xx / 限流 → 退避重试
      - 不可重试:参数非法 / 业务拒绝 → 立即上报,别白烧重试的钱
    写 dispatcher:可重试的退避重试,max_retries 后抛出;不可重试的当场抛出。
"""
import time


class AgentError(Exception):
    """agent 全家族异常基类。"""


class RetryableError(AgentError):
    """可重试:网络抖动、上游 5xx、限流 429。"""


class FatalError(AgentError):
    """不可重试:参数非法、业务拒绝。"""


def risky_call(code: int) -> str:
    if code == 429:
        raise RetryableError("限流 429,稍后再试")
    if code == 503:
        raise RetryableError("上游抖动 503")
    if code == 400:
        raise FatalError("参数非法 400")
    return "ok"


def dispatch(code: int, max_retries: int = 2) -> str:
    """按异常类型决策:可重试→退避;不可重试→直接炸。"""
    for attempt in range(max_retries):
        try:
            return risky_call(code)
        except RetryableError:
            delay = (attempt + 1) * 0.02
            print(f"  可重试,第 {attempt + 1} 次退避 {delay:.2f}s …")
            time.sleep(delay)
    raise RetryableError("重试耗尽,仍不可用")


def demo() -> None:
    cases = [(200, "成功"), (400, "不可重试"), (429, "可重试但耗尽")]
    for code, label in cases:
        try:
            print(f"[{label}] ->", dispatch(code, max_retries=2))
        except FatalError as e:
            print(f"[{label}] -> FatalError: {e}(当场上报,不重试)")
        except RetryableError as e:
            print(f"[{label}] -> RetryableError: {e}(重试 2 轮后向上抛)")


if __name__ == "__main__":
    demo()
    print("\nPASS: ex01 异常分类 + 按类型分派(可重试退避 / 不可重试上报)")