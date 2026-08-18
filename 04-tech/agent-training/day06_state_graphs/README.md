# Day 06 · 状态机 / 图设计(LangGraph,离线确定性节点)

> 对应总纲:第四部分 L1;第三部分 14 章(菜单循环 → 图);Python.md LangGraph 各节。
> 过关标准:⛳ **画并跑通"检索 agent"图,含循环终止**(ex04)。
> 运行方式:本日用真实 LangGraph(节点全部离线 mock,不花一分 token):

```bash
uv run --with langgraph python3 ex01_graph_basics.py
```

> 冒烟通过:`uv run --with langgraph python3 -c "from langgraph.graph import StateGraph"`(首次装 ~35 包,uv 缓存后即秒开)。

## 领题

| 文件 | 题目 | 核心概念 |
|---|---|---|
| `ex01_graph_basics.py` | 最小图:一个节点,看清 StatsGraph 的骨头 | Node / Edge / START / END |
| `ex02_state_schema.py` | 消息「追加不覆盖」在真框架里怎么写 | `Annotated[list, operator.add]` reducer |
| `ex03_conditional_loop.py` | 让图**自己决定下一步**,循环必须有终止 | 条件边 + 轮数上限 |
| `ex04_retrieval_agent.py` | ⛳ 检索 agent 图:检索 → 判断 → 回答,两种终止路径 | 过关题 / 循环终止 |
| `ex05_parallel_join.py` | 一把扇出 2 个数据源,汇合合并 | 并行分支 + reduce 汇合 |

## 先想清楚(反思)

1. **图 = 状态显式化、外置化**(总纲 S2/S6):状态放 `State`,节点返回增量,框架按 reducer 合并。这使中断续跑、并行、HITL、跨调用持久化成为可能——函数调用栈做不到。
2. **控制权交给节点**:流程不是写死的 if/else,而是**条件边在运行时根据 State 决定去哪**。条件边一定要有**终止条件**(轮数上限/成功标志)——不然就是无底洞。
3. LangGraph 与我们 day01–05 手写的机制**一一对应**:State=TypedDict、reducer=合并策略、conditional edges=运行时路由。框架只是把你已经理解的东西拼装好。