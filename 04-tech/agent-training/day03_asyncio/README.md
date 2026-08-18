# Day 03 · 异步原理 + 并发 / 限流 / 超时

> 对应总纲:第四部分 L0「asyncio」;第三部分 13 章(理解即可→异步优先)。
> 过关标准:**并发 3 个调用 + 单个失败不炸全局**。

```bash
uv run python3 ex01_async_await_basics.py
```

> 本日全部纯标准库,不需要 pydantic:直接 `python3` 即可。

## 领题

| 文件 | 题目 | 核心概念 |
|---|---|---|
| `ex01_async_await_basics.py` | 同步串行 vs 异步并发的耗时对比 | async/await + 事件循环 |
| `ex02_gather_concurrency.py` | 一行并发 + **默认一错全炸**的行为 | asyncio.gather |
| `ex03_failure_isolation.py` | 3 个任务一个失败,成功的不陪葬 | create_task + 逐个隔离 |
| `ex04_timeout_retry_async.py` | 模型挂死/抖动:超时 + 指数退避重试 | wait_for + backoff |
| `ex05_semaphore_async_for.py` | 10 个请求限流到 3 条并发车道 + 流式消费 | Semaphore + async for |

## 先想清楚(反思)

1. **Agent 是 I/O 密集,不是计算密集**(总纲 1.3 / S4)——等待网络/模型返回占大头,**异步是默认项不是优化项**;同步写 = 把 GPU 和钱包浪费在排队上。
2. `asyncio.gather` 默认**一个子任务抛错,整个 gather 抛错、其余结果全丢**。要让"单个失败不炸全局",得用 `return_exceptions=True` 或逐个 `await` 隔离。
3. **超时 = 给不确定性上保险**:模型可能挂死,`asyncio.wait_for` 掐断 + 指数退避重试是生产基线。
4. **限流 = 钱包保护**:`Semaphore` 把并发度压到预算内,再多的任务也只占 N 个车位。