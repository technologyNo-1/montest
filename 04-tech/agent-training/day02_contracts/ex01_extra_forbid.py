#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day02-Ex01 · Pydantic 严格模式:extra="forbid" + 自定义校验器
=====================================================
题目:
    day01 默认容忍多余字段(ignore)。但生产里"多出来"的字段往往意味着模型胡编或版本错配,
    你想直接拒绝。定义 SearchParams(model_config=ConfigDict(extra="forbid")):
      ① 多余的字段直接抛 ValidationError
      ② 用 field_validator 把 query 首尾空格去掉、空白则拒绝。
"""
from pydantic import BaseModel, Field, ConfigDict, field_validator, ValidationError


class SearchParams(BaseModel):
    model_config = ConfigDict(extra="forbid")          # 拒绝未被声明的字段
    query: str
    top_n: int = Field(default=3, ge=1, le=10)

    @field_validator("query")
    @classmethod
    def strip_query(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("query 不能是纯空白")
        return v


def demo() -> None:
    # ① 多出的 "debug" 字段 → 直接拒绝(对比 day01 的默认忽略)
    try:
        SearchParams.model_validate_json('{"query":"a","top_n":1,"debug":true}')
    except ValidationError as e:
        print("多余字段被拦截:", e.errors()[0]["msg"])

    # ② 空格被清理 + 合法通过
    ok = SearchParams(query="  python agent  ", top_n=5)
    print("query 已 strip:", repr(ok.query))

    # 空白 query 被拦
    try:
        SearchParams(query="   ")
    except ValidationError as e:
        print("空白 query 被拦:", e.errors()[0]["msg"])


if __name__ == "__main__":
    demo()
    print("\nPASS: ex01 extra=forbid + field_validator 生效")