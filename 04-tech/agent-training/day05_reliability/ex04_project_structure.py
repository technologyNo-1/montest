#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day05-Ex04 · 工程化:__name__ 惯用法 + 模块边界(uv 提示)
=====================================================
题目:
    agent 项目不是单文件。关键习惯:
      ① 每个脚本用 `if __name__ == "__main__":` 分界——被 import 时不跑副作用,
         直接运行才跑 demo(本训练所有脚本都遵守,所以都能单独 `python3 x.py`)
      ② print(__name__) 理解当前命名空间
      ③ 真实项目推荐 uv:uv init + pyproject.toml 锁依赖,不污染系统 python
"""
import importlib


def main_demo() -> str:
    return f"当前命名空间 __name__ = {__name__}"


if __name__ == "__main__":
    print(main_demo())
    print("importlib 拿到的 __main__:", importlib.import_module("__main__").__name__)
    print("提示:多文件工程用 uv init + pyproject 锁依赖;本训练单文件,专注语义")
    print("\nPASS: ex04 __name__ 惯用法 + import 边界成立")