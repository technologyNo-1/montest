# Day 02 · Pydantic 进阶 + 容器/状态安全

> 对应总纲:第四部分 L1「数据容器操作」;第三部分 5 章(容器/深浅拷贝)。
> 过关标准:**嵌套模型 + extra=forbid + 深浅拷贝不踩坑**。

```bash
uv run --with pydantic python3 ex01_extra_forbid.py
```

## 领题

| 文件 | 题目 | 核心概念 |
|---|---|---|
| `ex01_extra_forbid.py` | 生产环境拒绝"多出来"的字段 + 参数清洗 | extra="forbid" + field_validator |
| `ex02_shallow_deep_copy.py` | 状态快照被"共享内层"污染的 bug 根因与修复 | 浅拷贝 vs deepcopy / model_copy |
| `ex03_dict_merge_state.py` | 节点返回 partial 如何安全合并进 state | `state\|node` / setdefault / Counter / deque |
| `ex04_validators_chain.py` | 跨字段业务规则(区间、上限、枚举归一) | field_validator + model_validator |

## 先想清楚(反思)

1. **`extra` 三态**:`ignore`(默认,容忍多字段)、`forbid`(拒绝,防模型胡编)、`allow`(保留到 `model_extra`)。话题从"校验"变成"**信任边界**"——你给 LLM 多大自由度?
2. **浅拷贝只复制一层**——内层 list/dict 仍在共享。Agent 并行分支、持久化快照时,共享即污染。
3. **校验器两个维度**:字段级(`field_validator` 单字段清洗/约束)+ 跨字段(`model_validator` 业务规则)。业务规则写进模型,就不必散落在 use-case 里各写一遍。