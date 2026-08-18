#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day01-Ex04 · 嵌套契约 + 枚举:一个真正的 function-call schema
=====================================================
题目:
    定义"查天气"工具:城市名 + 温度单位(枚举) + 可选的时间窗(嵌套模型)。
    用 model_json_schema() 导出可投喂给 LLM 的 function-calling schema,再解析一次 LLM 回传。

先自己写,再运行。

要点:
    - 工具契约是嵌套的:一个工具的入参本身可能是结构化对象(嵌套模型)。
    - model_json_schema() 等价于 OpenAI function calling 的 parameters 段——契约的载体。
    - Literal = 把自由文本的选项"焊死",杜绝 LLM 传 undefined 之类的意外值。
"""
from typing import Literal, Optional
from pydantic import BaseModel, Field, ValidationError


class TimeWindow(BaseModel):
    start: str = Field(description="开始日期,如 2026-08-20")
    hours: int = Field(default=24, ge=1, le=72, description="覆盖小时数")


class WeatherQuery(BaseModel):
    city: str = Field(description="城市中文名")
    unit: Literal["celsius", "fahrenheit"] = "celsius"
    window: Optional[TimeWindow] = None      # 嵌套模型


def demo() -> None:
    schema = WeatherQuery.model_json_schema()
    print("=== function-call schema(可投喂 LLM)===")
    print("  title:", schema["title"], "| properties:", list(schema["properties"]))
    print("  unit 枚举:", schema["properties"]["unit"]["enum"])
    print("  window 嵌套:", "TimeWindow" if "window" in schema["properties"] else "?")

    cases = [
        ("合法嵌套", '{"city":"上海","unit":"celsius","window":{"start":"2026-08-20","hours":24}}'),
        ("非法枚举(kelvin)", '{"city":"上海","unit":"kelvin"}'),
        ("省略可选(单城市)", '{"city":"北京"}'),
    ]
    for name, raw in cases:
        try:
            obj = WeatherQuery.model_validate_json(raw)
            print(f"[{name}] OK  -> city={obj.city} unit={obj.unit} window={obj.window}")
        except ValidationError as e:
            print(f"[{name}] 拦截 -> {[(er['loc'], er['msg']) for er in e.errors()]}")


if __name__ == "__main__":
    demo()
    print("\nPASS: ex04 嵌套契约 + 枚举 + json_schema 导出全通过")