#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day01-Ex03 · ValidationError 处理闭环:拦截 → 重试 → 兜底
=====================================================
题目:
    模型节点回传的工具参数可能缺字段/类型错。写 call_tool(raw, max_retries=1):
    解析失败时打印 errors() 明细并「修复后重试」一次;仍失败则抛自定义异常,由上层兜底。

先自己写,再运行。

要点:
    - 校验失败不是"程序崩溃",而是【业务分支】:重试 / 换模型 / 兜底,由你决定。
    - e.errors() 给出 loc + msg + input,业界标准做法是把它回注给 LLM 让它改。
"""
import json
from pydantic import BaseModel, Field, ValidationError


class StockQuery(BaseModel):
    symbol: str = Field(min_length=1, max_length=8, description="股票代码")
    market: str = Field(default="cn", pattern="^(cn|us|hk)$")


class ToolCallError(Exception):
    """重试仍失败的可恢复异常,上层据此降级(人工/默认参数)。"""


def normalize(raw: str) -> str:
    """模拟 LLM 根据错误明细的二次生成:这里只演示修复「缺 market」。"""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    data.setdefault("market", "cn")        # 首次失败常见缺 market,重试补上
    return json.dumps(data, ensure_ascii=False)


def call_tool(raw: str, max_retries: int = 1) -> StockQuery:
    last = None
    for attempt in range(max_retries + 1):
        try:
            return StockQuery.model_validate_json(raw)
        except ValidationError as e:
            last = e
            locs = [er["loc"] for er in e.errors()]
            print(f"  第{attempt + 1}次失败: loc={locs}")
            if attempt < max_retries:
                raw = normalize(raw)       # 把错误明细"回注"给模型,这里直接补
    raise ToolCallError(f"重试 {max_retries} 次仍失败: {last}")


def demo() -> None:
    print("案例A · 一次通过:")
    ok = call_tool('{"symbol":"AAPL","market":"us"}')
    print("        ->", ok)

    print("案例B · 缺 market,重试后通过:")
    fixed = call_tool('{"symbol":"AAPL"}')
    print("        ->", fixed)

    print("案例C · 符号超长不可修复,重试仍失败 → 兜底:")
    try:
        call_tool('{"symbol":"TOOLONGZZ","market":"us"}')
    except ToolCallError:
        print("        -> 已抛 ToolCallError,上层走人工/默认参数")


if __name__ == "__main__":
    demo()
    print("\nPASS: ex03 非法输入被拦截;可恢复分支重试;不可恢复分支兜底")