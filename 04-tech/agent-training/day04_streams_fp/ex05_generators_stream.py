#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day04-Ex05 · 生成器:惰性 + 流式透传(管道)
=====================================================
题目:
    LLM 输出可能以分片到达(如 SSE)。用生成器实现"流式管道":
    上游产片 → 中游按块重组 → 下游消费,全程 O(1) 内存;再演示无限序列截断。
"""
def merge_chunks(chunks):
    """中游:把分片按 '|' 边界拼回完整块(边到边,不落全量)。"""
    buf = ""
    for c in chunks:
        buf += c
        while "|" in buf:
            piece, buf = buf.split("|", 1)
            yield piece
    # 末尾若残留无边界的碎片,这里选择丢弃(生产里可冲洗 buf)


def take(gen, n):
    for i, x in enumerate(gen):
        if i >= n:
            break
        yield x


def demo() -> None:
    # ① SSE 分片重组
    raw = ["ab|c", "d|ef|", "gh|i|"]
    pieces = list(merge_chunks(iter(raw)))
    print("流式重组(块):", pieces)
    assert pieces == ["ab", "cd", "ef", "gh", "i"]

    # ② 无限序列惰性消费:不构建 10 亿级列表
    evens = (x for x in range(10 ** 9) if x % 2 == 0)
    print("take 前 5 个偶数:", list(take(evens, 5)))

    # ③ 管道内存说明
    print("管道=边到边(惰性):生成器不预存全量,内存 O(1)")


if __name__ == "__main__":
    demo()
    print("\nPASS: ex05 生成器惰性 + 管道重组 + 无限序列截断")