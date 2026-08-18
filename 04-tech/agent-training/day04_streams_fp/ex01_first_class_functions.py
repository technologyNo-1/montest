#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day04-Ex01 · 一等函数:函数是数据 → 工具注册表的雏形
=====================================================
题目:
    把"工具"抽象成 dict(name, fn)。用 partial 预设参数、map 批量应用、
    函数工厂按需生成——这就是【函数即数据】,agent 工具注册的底层机制。
"""
from functools import partial


def search(query: str, top_n: int = 3) -> str:
    return f"search('{query}', top_n={top_n}) 命中 3 条"


def summarize(text: str) -> str:
    return f"summarize('{text[:20]}…')"


def double(x: int) -> int:
    return x * 2


def demo() -> None:
    # ① partial 预设参数 → 统一调度表
    tools = {"search": partial(search, top_n=5), "summarize": summarize}
    print("工具表调度:", tools["search"]("python agent"), "|", tools["summarize"]("一篇长文档的内容…"))

    # ② map 批量应用
    print("map(double):", list(map(double, [1, 2, 3])))

    # ③ 函数作为返回值:工厂
    def make_multiplier(k: int):
        return lambda x: x * k
    print("函数工厂 ×3:", make_multiplier(3)(7))


if __name__ == "__main__":
    demo()
    print("\nPASS: ex01 函数即数据(工具表 / map / 工厂)")