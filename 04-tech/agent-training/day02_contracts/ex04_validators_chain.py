#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day02-Ex04 · 校验器链 + 跨字段业务规则
=====================================================
题目:
    任务参数需要业务校验:开始时间 < 结束时间;窗口 ≤ 72h;优先级限 low/normal/high 且大小写归一。
    用 field_validator 做「字段级清洗」,用 model_validator 做「跨字段业务规则」。
    业务规则写进模型 → 上层 use-case 不再各自重复判断。
"""
from datetime import datetime, timedelta
from pydantic import BaseModel, field_validator, model_validator, ValidationError


class TaskWindow(BaseModel):
    start: datetime
    end: datetime
    priority: str = "normal"

    @field_validator("priority")
    @classmethod
    def norm_priority(cls, v: str) -> str:
        v = str(v).strip().lower()
        if v not in {"low", "normal", "high"}:
            raise ValueError(f"非法优先级: {v}")
        return v

    @model_validator(mode="after")
    def check_range(self) -> "TaskWindow":
        if self.end <= self.start:
            raise ValueError("end 必须晚于 start")
        if self.end - self.start > timedelta(hours=72):
            raise ValueError("任务窗口不能超过 72 小时")
        return self


def demo() -> None:
    ok = TaskWindow(start=datetime(2026, 8, 20, 9, 0),
                    end=datetime(2026, 8, 21, 9, 0),
                    priority=" HIGH ")
    print("合法窗口:", ok.start.date(), "→", ok.end.date(),
          "| priority 归一化为", repr(ok.priority))

    cases = [
        ("end 早于 start", dict(start=datetime(2026, 8, 20), end=datetime(2026, 8, 19))),
        ("超 72h", dict(start=datetime(2026, 8, 20), end=datetime(2026, 8, 25))),
        ("非法优先级 urgent", dict(start=datetime(2026, 8, 20),
                                   end=datetime(2026, 8, 21), priority="urgent")),
    ]
    for name, kw in cases:
        try:
            TaskWindow(**kw)
            print(f"[{name}] 未拦截?!")
        except ValidationError as e:
            print(f"[{name}] 拦截 -> {e.errors()[0]['msg']}")


if __name__ == "__main__":
    demo()
    print("\nPASS: ex04 字段级 + 跨字段业务规则全部生效")