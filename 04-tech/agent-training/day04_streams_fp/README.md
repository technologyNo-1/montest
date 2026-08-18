# Day 04 · 流式 / 生成器 / 一等函数 / 装饰器

> 对应总纲:第四部分 L1「一等函数/闭包/装饰器」「生成器/async 生成器」;第三部分 6/12 章。
> 过关标准:⛳ **不查文档手写 `@retry(backoff+jitter)` 装饰器**(ex04)。

```bash
uv run python3 ex01_first_class_functions.py
```

> 本日纯标准库,直接 `python3`。

## 领题

| 文件 | 题目 | 核心概念 |
|---|---|---|
| `ex01_first_class_functions.py` | 把"工具"抽象成 dict(fn,schema)——工具注册表的雏形 | 一等函数 / partial / map |
| `ex02_closures.py` | 节点捕获各自配置 + 避开 late-binding 坑 | 闭包 / nonlocal / LEGB |
| `ex03_decorator_basics.py` | 写 @timeit / @log 并保留函数签名 | 装饰器 / functools.wraps |
| `ex04_retry_decorator.py` | ⛳ 手写 `@retry(backoff + jitter)` | 装饰器 + 指数退避 |
| `ex05_generators_stream.py` | SSE 分片重组 + 无限序列截断 | yield / 惰性管道 |
| `ex06_async_generator_stream.py` | async 生成器 + 装饰器组合(SSE 雏形) | async for / 流式透传 |

## 先想清楚(反思)

1. **一等函数 = agent 组合的地基**:`@tool`/`@node` 本质就是"函数即数据 + 装饰器注册"——框架千变万化,底层就是这么三个机制。
2. **装饰器 = 横切关注点的收口**:重试、日志、限流、观测,不该写进业务函数内部,而是套在函数外。加分题:想清楚 `@wraps` 为什么必须。
3. **生成器 = O(1) 内存的流**:LLM/SSE 输出可以很大,"边到边"透传让内存不随负载线性涨。
4. **late-binding 坑**:在循环里建闭包/lambda,变量在"调用时"才解析 → 全取最后一个值。解决:默认参数即刻绑定。