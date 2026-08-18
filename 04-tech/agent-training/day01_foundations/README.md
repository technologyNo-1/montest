# Day 01 · 类型与契约(TypedDict + Pydantic 核心)

> 对应总纲:第四部分 L0「类型系统 + Pydantic」;第三部分 2/5/6 章的杠杆点。
> 过关标准:**能徒手写出"带校验的工具参数模型"并捕获 ValidationError**。
> 运行方式:进本目录后,每个脚本:

```bash
uv run --with pydantic python3 ex01_typeddict_state.py
```

> 每题都「先自己写 → 再运行 → 对照答案」;卡超 40 分钟标 `!` 次日重来。

## 领题

| 文件 | 题目 | 核心概念 |
|---|---|---|
| `ex01_typeddict_state.py` | 给"检索 agent"定义状态;用 reducer 让消息**追加不覆盖** | TypedDict + Annotated/reducer |
| `ex02_pydantic_tool_schema.py` | 给搜索工具定义带描述的参数模型,解析 LLM 的**脏 JSON** | BaseModel + Field |
| `ex03_validation_guard.py` | LLM 回传缺字段/类型错,如何**拦截→重试→兜底**? | ValidationError 处理闭环 |
| `ex04_nested_contract.py` | 把天气查询参数**嵌套**成工具契约,导出 function-call schema | 嵌套模型 + Literal + json_schema |
| `ex05_llm_boundary_loop.py` | 模拟「模型节点」返回 → 校验 → 失败重试 → 路由,最小闭环 | 不确定边界收口 |

## 先想清楚这几句话(反思题)

1. **Agent 的控制流由大模型在运行时决定**,所以 LLM 输出必须先过「契约」再进逻辑——这就是类型系统 + Pydantic 是 L0 的原因。
2. **TypedDict 只做类型提示,运行时不校验**;Pydantic 才做运行时校验。两者分工:状态描述用 TypedDict,工具/输出契约用 Pydantic。
3. **校验失败不是崩溃,是业务分支**——重试、换模型、兜底,由你写。