#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day07-Ex01 · 工具层:带校验的工具参数模型 + 非法输入拦截
=====================================================
结项要求 1:Pydantic 定义工具参数(查库存/查价格),非法输入被拦截。
本脚本独立展示工具契约与分发;图集成见 ex03。
"""
from store_lib import StockQuery, PriceQuery, TOOL_SCHEMAS, run_tool
from pydantic import ValidationError


def demo() -> None:
    print("== 合法工具调用 ==")
    ok = StockQuery(product="cpu", region="cn")
    print("   StockQuery 合法:", ok.model_dump_json())

    print("== 非法参数被拦截(ValidationError)==")
    for bad in [{"product": 123}, {"product": "x", "region": "eu"}, {}]:
        try:
            StockQuery.model_validate(bad)
            print("   未拦截?!", bad)
        except ValidationError as e:
            print("   拦截:", bad, "→", e.errors()[0]["msg"])

    print("== run_tool 分发:未知工具 / 脏 JSON ==")
    for raw in ['{"action":"query_stock","product":"cpu","region":"cn"}',
                '{"action":"hack_delete_all"}',
                '{"action":"query_price","sku":"gtx"}']:
        try:
            action, params = run_tool(raw)
            print(f"   {raw} → {action}({params.model_dump_json()})")
        except Exception as e:                      # FatalError / ValidationError
            print(f"   {raw} → {type(e).__name__}: {e}")

    print("\n工具注册表:", list(TOOL_SCHEMAS))


if __name__ == "__main__":
    demo()
    print("\nPASS: ex01 工具契约 + 非法拦截 + 分发")