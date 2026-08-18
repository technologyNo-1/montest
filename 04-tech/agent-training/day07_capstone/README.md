# Day 07 · 综合挑战 + 迷你结项

> 对应总纲:第七部分(结项标准)。目标:把 day01–06 全部能力集成成一个**离线可跑的检索式客服 agent**。
> 交付物:3 个主脚本 + 结项报告 + 毕业 checklist。
> 运行:`uv run --with langgraph python3 <file>.py`;**毕业命令 = `uv run --with langgraph python3 run_checklist.py`(全 PASS 即毕业)**。

## 领题

| 文件 | 结项要求 | 内容 |
|---|---|---|
| `store_lib.py` | —(公用地基) | 工具契约 / 异常分类 / 离线数据源 / 并发检索 / 退避重试 |
| `ex01_tools_pydantic.py` | 要求 1 | Pydantic 工具参数(查库存/查价格),非法输入被拦截 |
| `ex02_concurrent_retrieve.py` | 要求 2、3 | asyncio 并发双源 + 可重试/不可重试分类 + 指数退避 |
| `ex03_customer_service_agent.py` | 要求 4、5 | 图组织流程 + 循环终止 + checkpointer 断点续跑 + HITL 挂起点 |
| `run_checklist.py` | 要求 6 + §7.2 | 6 项结项要求 + 3 条离线 eval 断言,自动核验毕业 |
| `REPORT.md` | — | 结项报告:架构 / 取舍 / 复盘 / 如何接真 LLM |

## 接过关后再读一遍总纲第七部分

- 本目录 6 个 `.py` **全部离线、0 花费 token**;真实项目只需把 `fake_llm_toolcall` 换成真模型(`with_structured_output`),把 `source_*` 换成真 API,再挂监控即可上线。
- 毕业后每周跑一次 `run_checklist.py` 当回归测试;新踩的坑回填总纲 + 对应章笔记。