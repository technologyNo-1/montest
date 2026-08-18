# Day 05 · 异常分类 / 上下文管理 / 序列化 / 工程

> 对应总纲:第四部分 L1「异常+上下文管理」、L2「序列化/配置、模块与依赖」;第三部分 7/10/11/12 章。
> 过关标准:**with 管好资源** + **状态可序列化往返**。

```bash
uv run --with pydantic python3 ex01_exception_taxonomy.py
```

## 领题

| 文件 | 题目 | 核心概念 |
|---|---|---|
| `ex01_exception_taxonomy.py` | 把失败分成「可重试 / 不可重试」两族并分派 | 自定义异常 + 捕获顺序 |
| `ex02_context_manager_with.py` | `with` 管好文件/HTTP/会话,**炸了也清理** | with / @contextmanager / `__exit__` |
| `ex03_serialization_roundtrip.py` | 状态 dict→JSON→dict 往返(set/datetime 坑的解法) | 序列化 / Pydantic 往返 |
| `ex04_project_structure.py` | `__name__ == "__main__"` 惯用法 + import 边界 | 模块工程化 / uv 提示 |

## 先想清楚(反思)

1. **错误也是数据,要分门别类**:网络抖动/限流 → 可重试;参数非法/业务拒绝 → 不可重试。混为一谈 = 该重试的不重试、不该重试的反复烧钱。
2. `with` 是"资源生命周期"的收口:**分配 → 使用 → 必然清理**。文件句柄、HTTP client、DB 会话不 with,泄漏是迟早的事。
3. **checkpointer 之所以能断点续跑,全靠"状态可序列化、可重建"**(总纲 S6/S2)。而 `set`/`datetime` 天然不是 JSON 类型——转换规则要预先约定好,别等序列化那天才发现炸。
4. `__name__ == "__main__"` 分界让同一份代码既能被 import 复用、又能直接跑——本训练所有脚本都遵守它,你写 agent 也要遵守。