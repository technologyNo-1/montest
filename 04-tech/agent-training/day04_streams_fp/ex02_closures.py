#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day04-Ex02 · 闭包:节点捕获上下文 + 避开 late-binding 坑
=====================================================
题目:
    agent 节点需要"记住"自己的配置/计数。用闭包实现:
      ① 计数器 ② 每个节点绑定各自 max_rounds ③ 避坑:循环里建闭包全取最后一个值。
"""
def make_counter():
    n = 0
    def tick():
        nonlocal n            # 修改外层变量必须 nonlocal
        n += 1
        return n
    return tick


def make_node(name: str, max_rounds: int):
    def run(user: str) -> str:
        return f"{name} 处理 '{user}',上限 {max_rounds} 轮"
    return run


def late_binding_bug() -> list:
    """经典坑:lambda 里的 i 在【调用时】才解析 → 全是最后的值。"""
    fs = []
    for i in range(3):
        fs.append(lambda: i)
    return [f() for f in fs]          # [2, 2, 2]


def late_binding_fix() -> list:
    """修复:默认参数在【定义时】即刻绑定。"""
    fs = []
    for i in range(3):
        fs.append(lambda i=i: i)
    return [f() for f in fs]          # [0, 1, 2]


def demo() -> None:
    c = make_counter()
    print("闭包计数器:", c(), c(), c())

    n1, n2 = make_node("检索", 3), make_node("总结", 5)
    print("节点各自配置:", n1("q"), "|", n2("q"))

    print("late-binding 坑:", late_binding_bug(), "→ 修复:", late_binding_fix())


if __name__ == "__main__":
    demo()
    print("\nPASS: ex02 闭包捕获 + nonlocal + late-binding 避坑")