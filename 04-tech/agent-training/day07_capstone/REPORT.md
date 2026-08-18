# 结项报告 · 离线检索式客服 agent

> 日期:2026-08-19 | 对应《Agent 开发工程化总纲》第七部分
> 运行:`uv run --with langgraph python3 run_checklist.py` 全 PASS = 毕业。

## 一、架构(一张图画清楚)

```
                     ┌──────────────────────── 图(StateGraph) ─────────────────────────┐
 START → parse ──→ validate ──┬──(合法)────────→ retrieve ──→ confirm ──→ answer → END
   │       │          │       │               (并发双源+重试)  (HITL interrupt)
   │       └─ 离线模型 ┘       ├──(非法 & 轮数未满)→ parse  ←──────(重解析,错误回注)
   │                           └──(非法 & 轮数已满)→ answer ──(有界兜底,绝不死循环)
   q=输入                       State:Turns(历史)/action/params/sources/confirmed/answer
每个节点只返回【增量】;框架按 reducer(Turns 追加,标量覆盖)合并进 State。
checkpointer=MemorySaver → 状态跨 invoke 持久化 → 同 thread 可断点续跑,可 HITL 中断。
```

## 二、六项结项要求 → 落到哪行代码

| # | 要求 | 落地 |
|---|---|---|
| 1 | Pydantic 工具参数,非法拦截 | `store_lib.StocksQuery/PriceQuery` + `run_tool()`;`ex01` |
| 2 | asyncio 并发检索 2 源,单点失败不炸 | `store_lib.retrieve()` = `asyncio.gather(..., return_exceptions=True)`;`ex02` scene A |
| 3 | 异常分类 + 网络类指数退避重试 | `RetryableError / FatalError`;`call_with_retry()`(base*2^n + wait_for);`ex02` scene B/C |
| 4 | 图流程 + 循环必须有终止 | `route_validate()` 双终止**:命中→retrieve / 轮数≥MAX→answer(兜底)**;`ex03` |
| 5 | checkpointer 断点续跑 + HITL 挂起点 | `interrupt()` 停在 confirm;`Command(resume=)` 续跑;同 thread 二段会话;`ex03` |
| 6 | 3 条离线 eval 断言 | `run_checklist` 项 6:干净查询 / 脏输出拦截重试 / 有界兜底 三断言 |

## 三、设计取舍(为什么这么做)

1. **全程离线 mock,0 token**:把「模型边界」隔离在 `fake_llm_toolcall` 一处,其它全是确定逻辑——这本身就是总纲 S8 的三层切分实践。模型换成真的,图/契约/重试/持久化一行不用改。
2. **脏输出放进第一轮而非测试**:让"契约拦截 → 回注 → 重解析修好"成为真实跑过的路径,而不是纸面说法。
3. **两条终止路径都写**:命中终止 + 轮数上限兜底。框架不替你挡死循环,**条件边的终止条件是你的事**(总纲 1.3 反直觉点)。
4. **HITL 用 `interrupt()` 而非"等待轮询"**:图真正停在挂起点,状态被 checkpointer 封存;用户随时 `resume`,期间别的会话照常跑——这是 durable execution 的正解(总纲第六部分趋势 1)。

## 四、踩坑 / 复盘(学习中真实出现,已修复)

- **浅拷贝共享内层**(day02 ex02 内存):状态快照会互相污染 → 深拷贝或 `model_copy(deep=True)`。
- **`gather` 默认一错全炸**(day03 ex02):并发里一个源 404 会连坐吞掉其余成功结果 → `return_exceptions=True` 或逐个隔离。
- **async 装饰器作用域踩坑**(day04 ex06):`throttle` 里 `return wrapper` 写错层级 → `deco` 返回 None → 函数被装饰成 None。教训:**装饰器三层(工厂→装饰器→wrapper)的 return 层级要逐个核**。
- **图里「无 reducer 的 key 默认覆盖」**:消息存 list 时必须 `Annotated[list, operator.add]`,否则节点二次返回就把历史冲掉(day01/06 同一根因).

## 五、如何接到真 LLM / 真数据(三步)

1. `fake_llm_toolcall` → 真模型:`model.with_structured_output(ToolCallModel)` 拿到结构化工具调用,或 `result.tool_calls`;保留 run_tool 的校验当最后一层拦网。
2. `source_*` → 真 API:函数体换成 `httpx.AsyncClient` 请求 + `call_with_retry` 兜底;注意 `async with httpx.AsyncClient()` 管好连接池。
3. 挂观测:每个节点埋 token/延迟/tool-error 计数(这就是数据集);把本次 3 条 eval 断言扩成回归集,接真模型后每周回归。

## 六、毕业一句

> 做完这 7 天,你对 agent 不再背 API,而是有一个可迁移的思想模型:**契约管状态、异步管 IO、函数组合管控制流、异常管不确定性、图管组织、checkpointer 管记忆。** 框架怎么换代,地基都在。