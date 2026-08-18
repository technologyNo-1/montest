#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
day07 公用库:工具契约 / 异常分类 / 离线数据源 / 并发检索 / 重试助手。
ex01/ex02/ex03/run_checklist.py 复用本文件。全部离线、确定性可断言。
"""
from __future__ import annotations

import asyncio
import json
from pydantic import BaseModel, Field, ValidationError


# ============ 1. 工具参数契约(结项要求 1) ============
class StockQuery(BaseModel):
    product: str = Field(min_length=1, max_length=40, description="商品名")
    region: str = Field(default="cn", pattern="^(cn|global)$", description="仓区(枚举)")


class PriceQuery(BaseModel):
    sku: str = Field(min_length=1, max_length=16, description="商品 SKU")


TOOL_SCHEMAS: dict[str, type[BaseModel]] = {
    "query_stock": StockQuery,
    "query_price": PriceQuery,
}


def run_tool(raw: str) -> tuple[str, BaseModel]:
    """校验模型输出的工具调用 JSON;参数非法直接抛(ValidationError / FatalError)。"""
    data = json.loads(raw)                     # JSON 解析失败 → JSONDecodeError
    action = data.get("action")
    if action not in TOOL_SCHEMAS:
        raise FatalError(f"未知工具: {action}")
    return action, TOOL_SCHEMAS[action].model_validate(data)   # 非法参数 → ValidationError


# ============ 2. 异常分类(结项要求 3) ============
class RetryableError(Exception):
    """网络抖动 / 503 / 超时 → 可重试。"""


class FatalError(Exception):
    """参数非法 / 业务拒绝 → 不可重试,立即上报。"""


# ============ 3. 离线数据源(带可注入抖动开关) ============
STOCK = {"gtx": 12, "rtx": 3, "cpu": 99}
PRICE = {"gtx": 4999, "rtx": 6999, "cpu": 1999}
_FAIL: dict[str, int] = {}


def set_fail_source(name: str, times: int) -> None:
    """测试用:让某数据源先抖 times 次(模拟 503)。"""
    _FAIL[name] = times


async def _maybe_flaky(name: str) -> None:
    if _FAIL.get(name, 0) > 0:
        _FAIL[name] -= 1
        raise RuntimeError(f"{name} 503 抖动")


async def source_inventory(product: str) -> str:
    await _maybe_flaky("inventory")
    await asyncio.sleep(0.10)
    if product not in STOCK:
        raise FatalError(f"无此商品: {product}")
    return f"总仓库存 {product} = {STOCK[product]} 件"


async def source_warehouse(product: str) -> str:
    await _maybe_flaky("warehouse")
    await asyncio.sleep(0.12)
    return f"华东仓 {product} ≈ {STOCK.get(product, 0) - 1} 件"


async def source_price_hk(sku: str) -> str:
    await asyncio.sleep(0.12)
    if sku not in PRICE:
        raise FatalError(f"无此价格: {sku}")
    return f"{sku} 港币价 ≈ ¥{PRICE[sku] + 300}"


# ============ 4. 重试助手:可重试退避,不可重试直抛(结项要求 3) ============
async def call_with_retry(coro_factory, *, max_retries: int = 3,
                          base_delay: float = 0.02, timeout: float = 5.0) -> str:
    last: Exception | None = None
    for attempt in range(max_retries):
        try:
            return await asyncio.wait_for(coro_factory(), timeout)
        except FatalError:
            raise                                  # 不可重试:立即抛
        except (RetryableError, RuntimeError, TimeoutError) as e:
            last = e
            await asyncio.sleep(base_delay * (2 ** attempt))   # 指数退避
    raise RetryableError(f"重试 {max_retries} 次仍失败: {last}")


# ============ 5. 并发检索两个数据源,单个失败不炸(结项要求 2) ============
def source_pairs(action: str, params: BaseModel):
    if action == "query_stock":
        return [lambda: source_inventory(params.product),
                lambda: source_warehouse(params.product)]
    return [lambda: source_price_hk(params.sku)]


async def retrieve(action: str, params: BaseModel) -> list[str]:
    """并发 gather 双源;单个失败(重试耗尽)被隔离为结果,不拖垮整体。"""
    coros = source_pairs(action, params)
    res = await asyncio.gather(*(call_with_retry(c) for c in coros),
                               return_exceptions=True)
    return [r if isinstance(r, str) else f"({type(r).__name__}) 该源重试后仍失败,已隔离"
            for r in res]


# ============ 6. 离线'模型'节点:按关键词输出工具调用(可故意脏一次) ============
def fake_llm_toolcall(q: str, round_no: int) -> str:
    if "价" in q or "多少" in q:
        return '{"action":"query_price","sku":"gtx"}'
    if "库存" in q or "货" in q or "cpu" in q.lower():
        return '{"action":"query_stock","product":"cpu","region":"cn"}'
    if "显卡" in q:
        # 第一轮故意脏输出(把 123 当 product)→ 第二轮模型"修好" → 演示拦截后重试
        return '{"action":"query_stock","product":123}' if round_no < 2 \
            else '{"action":"query_stock","product":"rtx","region":"cn"}'
    return '{"action":"what"}'      # 听不懂 → 未知工具 → 抛 FatalError → 有界兜底