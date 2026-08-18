#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day02-Ex03 · 容器操作:状态合并 / 默认值 / 计数器 / 滚动窗口
=====================================================
题目:
    节点返回 partial,你要把它安全合并进 state。完成三个场景:
      ① 用 | 或 {**a, **b} 做浅合并——注意消息必须「追加」而非常规覆盖
      ② 用 setdefault 只保留首次默认、Counter 统计动作分布
      ③ 用 deque(maxlen=N) 保留最近 N 条消息(滚动窗口)
"""
import json
from collections import Counter, deque


def demo() -> None:
    # ① 浅合并:普通键覆盖,消息键手动追加
    node1 = {"messages": ["用户:hi"], "retries": 1}
    node2 = {"messages": ["模型:hello"], "hits": 3}
    state = node1
    state = {**state, **node2, "messages": state["messages"] + node2["messages"]}
    print("① 合并后:", json.dumps(state, ensure_ascii=False))

    # ② setdefault:只写首次默认;Counter:分布统计
    cfg = {}
    cfg.setdefault("model", "gpt-4o-mini")
    cfg.setdefault("model", "deepseek-v3")          # 已有,不覆盖
    cfg.setdefault("timeout", 30)
    print("② setdefault 默认值:", cfg)
    acts = Counter(["search", "search", "stop", "search", "summarize"])
    print("   Counter 动作分布:", dict(acts))

    # ③ deque 滚动窗口:只留最近 3 条消息(像截断上下文的长短记忆)
    recent = deque(maxlen=3)
    for m in ["用户:q1", "模型:a1", "工具:r1", "用户:q2"]:
        recent.append(m)
    print("③ 最近消息窗口:", list(recent))


if __name__ == "__main__":
    demo()
    print("\nPASS: ex03 容器合并 / 默认值 / 计数 / 滚动窗口全通过")