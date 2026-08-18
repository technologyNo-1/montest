#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day01-Ex02 · 工具参数模型:把 LLM 的脏 JSON 变成合法结构
=====================================================
题目:
    给"搜索工具"定义参数模型:query 必填且带描述,top_n 默认 3 且限 1–10。
    模拟 LLM 回传 ① 合法 ② 多余字段 ③ 非法范围 三种 JSON,分别展示解析结果。

先自己写,再运行。

要点(总纲 S1 / Python.md §2):
    - LLM 输出是"概率字符串",Pydantic 把它降维成"合法结构"后才敢进逻辑。
    - description 是写给大模型看的 prompt;写模糊,模型就传错参数。
"""
from pydantic import BaseModel, Field, ValidationError


class SearchToolInput(BaseModel):
    """搜索引擎工具参数,给 LLM 读取的 schema。"""
    query: str = Field(description="搜索关键词,如 'python asyncio'")
    top_n: int = Field(default=3, description="返回结果数量,1–10", ge=1, le=10)


def parse_llm_output(raw: str) -> SearchToolInput:
    return SearchToolInput.model_validate_json(raw)   # 解析 + 校验一步到位


def demo() -> None:
    cases = [
        ("合法输入", '{"query":"python agent","top_n":5}'),
        ("多余字段(默认容忍忽略)", '{"query":"asyncio","top_n":2,"debug":true}'),
        ("top_n 越界(0 < ge=1)", '{"query":"asyncio","top_n":0}'),
        ("缺必填字段 query", '{"top_n":3}'),
    ]
    for name, raw in cases:
        try:
            obj = parse_llm_output(raw)
            print(f"[{name}] OK    -> query={obj.query!r} top_n={obj.top_n}  "
                  f"| dump_json={obj.model_dump_json()}")
        except ValidationError as e:
            first = e.errors()[0]
            print(f"[{name}] 拦截  -> loc={first['loc']} msg={first['msg']}")


if __name__ == "__main__":
    demo()
    print("\nPASS: ex02 工具参数模型解析 + 校验通过(非法输入抛 ValidationError)")