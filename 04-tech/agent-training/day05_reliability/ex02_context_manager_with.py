#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day05-Ex02 · with 管好资源:文件 / 会话 / 自写上下文管理器
=====================================================
题目:
    ① 文件读写必须 with(防句柄泄漏)
    ② 用 @contextmanager 实现自动开关的「LLM 客户端会话」
    ③ 手写 __enter__ / __exit__ 类:进入分配、**中途抛异常也必然清理**
"""
import os
import contextlib


def part1() -> None:
    """文件句柄:with 保证 close。"""
    path = "/tmp/d05_demo.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write("hello agent\n")
    with open(path, encoding="utf-8") as f:
        print("  文件内容:", f.read().strip())


@contextlib.contextmanager
def llm_session(model: str = "gpt-4o-mini"):
    """上下文管理器:进入连接,退出必然关闭(哪怕 yield 中途抛异常)。"""
    print(f"  连接 {model} …")
    try:
        yield f"{model}-session"          # with 块内拿到的值
    finally:
        print(f"  关闭 {model} 连接(finally 保证)")


class TempFile:
    """自写上下文管理器:分配(建文件)→ 使用 → 必然清理(删文件)。"""

    def __init__(self, path: str) -> None:
        self.path = path

    def __enter__(self) -> str:
        open(self.path, "w").close()
        print(f"  分配 {self.path}")
        return self.path

    def __exit__(self, exc_type, exc, tb) -> bool:
        os.remove(self.path)                                   # 无论成败都清理
        print(f"  清理 {self.path}(异常={exc_type.__name__ if exc_type else '无'})")
        return False                                           # False = 不吞异常,继续传播


def demo() -> None:
    part1()

    with llm_session() as s:
        print("  会话:", s)

    try:
        with TempFile("/tmp/d05_tmp.txt") as p:
            print("  进入", p, "→ 制造一个异常:")
            raise ValueError("走到一半炸了")
    except ValueError as e:
        print("  捕获 ValueError:", e, "(上下文已在异常传播前清理完毕)")


if __name__ == "__main__":
    demo()
    print("\nPASS: ex02 with / @contextmanager / 自写上下文管理器 全通过")