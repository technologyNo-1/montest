# AI DataWorks — 核心代码架构设计

## 一、项目结构

```
dataworks/
├── apps/                           # 应用层
│   ├── api/                        # FastAPI 主服务
│   │   ├── main.py                 # 应用入口
│   │   ├── routers/                # API 路由
│   │   │   ├── chat.py             # 对话接口
│   │   │   ├── metrics.py          # 指标管理
│   │   │   ├── semantic.py         # 语义层管理
│   │   │   └── admin.py            # 管理后台
│   │   ├── middleware/             # 中间件
│   │   │   ├── auth.py             # 认证
│   │   │   ├── rate_limit.py       # 限流
│   │   │   └── audit.py            # 审计
│   │   └── schemas/                # Pydantic 模型
│   │       ├── chat.py
│   │       ├── query.py
│   │       └── response.py
│   │
│   └── worker/                     # 后台 Worker (Temporal)
│       ├── workflows/              # 工作流定义
│       │   ├── query_workflow.py   # 查询执行工作流
│       │   └── sync_workflow.py    # 元数据同步工作流
│       └── activities/             # 活动定义
│           ├── semantic_activities.py
│           ├── sql_activities.py
│           └── verification_activities.py
│
├── core/                           # 核心引擎
│   ├── intent/                     # 意图解析
│   │   ├── parser.py               # LLM 意图解析器
│   │   ├── router.py               # 意图路由器
│   │   └── entity_linker.py        # 实体链接
│   │
│   ├── semantic/                   # 语义层 ★
│   │   ├── engine.py               # 语义映射引擎
│   │   ├── metric_registry.py      # 指标注册中心
│   │   ├── dimension_catalog.py    # 维度目录
│   │   ├── glossary.py             # 术语词典
│   │   ├── schema_router.py        # Schema 路由
│   │   └── time_resolver.py        # 时间解析
│   │
│   ├── compiler/                   # SQL 编译
│   │   ├── compiler.py             # 主编译器 (IR → SQL)
│   │   ├── optimizer.py            # 查询优化
│   │   ├── dialect.py              # 方言适配 (ClickHouse/Hive/...)
│   │   └── ir.py                   # 中间表示 (IR) 定义
│   │
│   ├── verification/               # 验证引擎 ★
│   │   ├── sql_validator.py        # SQL 安全校验
│   │   ├── result_validator.py     # 结果合理性校验
│   │   ├── confidence.py           # 置信度评分
│   │   ├── reconciliation.py       # 对账引擎
│   │   └── explainer.py            # SQL 结果解释器
│   │
│   ├── execution/                  # 查询执行
│   │   ├── executor.py             # 查询执行器
│   │   ├── connection_pool.py      # 连接池管理
│   │   └── cache.py                # 结果缓存
│   │
│   └── security/                   # 安全
│       ├── permission.py           # 权限执行器
│       ├── masking.py              # 数据脱敏
│       └── auditor.py              # SQL 审计
│
├── llm/                            # LLM 集成
│   ├── gateway.py                  # 多模型网关 (LiteLLM)
│   ├── prompts/                    # Prompt 模板
│   │   ├── intent_parsing.j2       # 意图解析
│   │   ├── schema_linking.j2       # Schema 路由
│   │   ├── time_resolution.j2      # 时间解析
│   │   ├── result_explanation.j2   # 结果解释
│   │   └── follow_up.j2            # 追问推荐
│   └── embeddings.py               # Embedding 服务
│
├── infrastructure/                 # 基础设施
│   ├── db/                         # 数据库
│   │   ├── postgres.py             # PostgreSQL 连接
│   │   ├── clickhouse.py           # ClickHouse 连接
│   │   └── milvus.py               # Milvus 向量库
│   ├── cache/                      # 缓存
│   │   └── redis.py                # Redis
│   ├── queue/                      # 消息队列
│   │   └── kafka.py                # Kafka
│   └── monitoring/                 # 监控
│       ├── metrics.py              # Prometheus 指标
│       └── tracing.py              # OpenTelemetry 追踪
│
├── config/                         # 配置
│   ├── settings.py                 # 全局配置
│   ├── semantic/                   # 语义层配置
│   │   ├── metrics/                # 指标 YAML 定义
│   │   │   ├── gmv.yaml
│   │   │   ├── dau.yaml
│   │   │   └── conversion_rate.yaml
│   │   ├── dimensions/             # 维度 YAML 定义
│   │   │   ├── region.yaml
│   │   │   ├── channel.yaml
│   │   │   └── time.yaml
│   │   ├── glossary.yaml           # 术语词典
│   │   └── data_models.yaml        # 数据模型注册
│   └── prompts/                    # Prompt 配置
│
├── tests/                          # 测试
│   ├── unit/
│   │   ├── test_metric_registry.py
│   │   ├── test_time_resolver.py
│   │   ├── test_sql_compiler.py
│   │   └── test_sql_validator.py
│   ├── integration/
│   │   ├── test_query_pipeline.py
│   │   ├── test_semantic_engine.py
│   │   └── test_permission.py
│   ├── e2e/
│   │   ├── test_chat_flow.py
│   │   └── test_analytics_flow.py
│   └── fixtures/
│       ├── semantic_data.py
│       └── query_cases.py
│
├── docs/                           # 文档
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── Makefile
└── README.md
```

---

## 二、核心模块代码实现

### 2.1 语义映射引擎 (core/semantic/engine.py)

```python
"""
语义映射引擎 —— 将 LLM 解析出的结构化意图映射为物理表、字段和 JOIN 路径。

这是整个系统正确性的核心保证层。
LLM 只负责意图理解，本引擎负责确定性映射——不存在幻觉。
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum

from core.semantic.metric_registry import MetricRegistry
from core.semantic.dimension_catalog import DimensionCatalog
from core.semantic.glossary import Glossary
from core.semantic.schema_router import SchemaRouter


class AggregationType(Enum):
    SUM = "SUM"
    COUNT = "COUNT"
    COUNT_DISTINCT = "COUNT_DISTINCT"
    AVG = "AVG"
    MAX = "MAX"
    MIN = "MIN"
    RATIO = "RATIO"               # 需要两个指标相除
    CUSTOM = "CUSTOM"             # 自定义计算表达式


@dataclass
class ParsedIntent:
    """LLM 解析后的结构化意图"""
    metrics: List[str]            # ["gmv", "conversion_rate"]
    dimensions: List[str]         # ["region", "platform"]
    filters: Dict[str, any]       # {"region": "北京", "platform": "iOS"}
    time_range: tuple             # ("2026-06-22", "2026-06-28")
    granularity: str              # "daily" | "weekly" | "monthly" | "summary"
    order_by: Optional[str]       # "gmv DESC"
    limit: Optional[int]          # 10
    query_type: str               # "aggregation" | "detail" | "trend" | "compare"


@dataclass
class PhysicalQuery:
    """物理查询计划 —— 完全不依赖 LLM 的确定性输出"""
    main_table: str               # "dws_trade_order_daily_1d"
    select_columns: List[dict]    # [{"expr": "SUM(payment_amount)", "alias": "gmv"}]
    joins: List[dict]             # [{"table": "dim_region", "on": "...", "type": "LEFT"}]
    where_clauses: List[str]      # ["region_name = '北京'", "dt BETWEEN ..."]
    group_by: List[str]           # ["region_name"]
    order_by: Optional[str]
    limit: Optional[int]
    metadata: dict                # 置信度、权限、来源追踪等


class SemanticEngine:
    """
    语义映射引擎：Intent → PhysicalQuery
    
    工作流程：
    1. 将 LLM 解析的意图指标名解析为注册中心中的 Metric 定义
    2. 解析维度名到 Dimension 定义
    3. 计算 JOIN 路径（多表 JOIN 时取最优路径）
    4. 构建 PhysicalQuery（完全不依赖 LLM）
    """
    
    def __init__(
        self,
        metric_registry: MetricRegistry,
        dimension_catalog: DimensionCatalog,
        glossary: Glossary,
        schema_router: SchemaRouter,
    ):
        self.metrics = metric_registry
        self.dimensions = dimension_catalog
        self.glossary = glossary
        self.schema = schema_router
    
    def resolve(self, intent: ParsedIntent) -> PhysicalQuery:
        """核心方法：将意图解析为物理查询计划"""
        
        resolved_metrics = []
        for m in intent.metrics:
            metric_def = self.metrics.get(m)
            if not metric_def:
                raise SemanticError(
                    f"未找到指标 '{m}'。您是否指的是："
                    f"{self.metrics.suggest_similar(m)}？"
                )
            resolved_metrics.append(metric_def)
        
        resolved_dimensions = []
        for d in intent.dimensions:
            dim_def = self.dimensions.get(d)
            if not dim_def:
                raise SemanticError(
                    f"未找到维度 '{d}'。可用维度："
                    f"{self.dimensions.list_available_for(resolved_metrics)}"
                )
            resolved_dimensions.append(dim_def)
        
        # Step 3: 计算 SELECT 表达式
        select_exprs = []
        for metric in resolved_metrics:
            select_exprs.append({
                "expr": self._build_aggregation_expr(metric),
                "alias": metric.name,
                "display_name": metric.display_name,
            })
        
        # Step 4: 计算 JOIN 路径
        # 多个维度来自不同维度表时，需要规划最优 JOIN 顺序
        join_plan = self._plan_joins(resolved_metrics, resolved_dimensions)
        
        # Step 5: 构建过滤条件
        where = self._build_where(intent.filters, intent.time_range, resolved_metrics)
        
        # Step 6: 组装 PhysicalQuery
        return PhysicalQuery(
            main_table=resolved_metrics[0].measure.table,
            select_columns=select_exprs,
            joins=join_plan,
            where_clauses=where,
            group_by=self._build_group_by(resolved_dimensions, intent.granularity),
            order_by=intent.order_by,
            limit=intent.limit,
            metadata={
                "confidence": self._calculate_confidence(
                    resolved_metrics, resolved_dimensions, intent
                ),
                "required_permissions": self._gather_permissions(
                    resolved_metrics, resolved_dimensions
                ),
                "trace": {
                    "metrics_resolved": [m.name for m in resolved_metrics],
                    "dimensions_resolved": [d.name for d in resolved_dimensions],
                    "tables_touched": [t for t in self._collect_tables(join_plan)],
                },
            },
        )
    
    def _plan_joins(
        self, metrics: List, dimensions: List
    ) -> List[dict]:
        """规划最优 JOIN 路径"""
        # 1. 收集所有涉及的表
        tables = set()
        for m in metrics:
            tables.add(m.measure.table)
        
        dimension_tables = {}
        for d in dimensions:
            for level in d.hierarchy:
                tables.add(level.get("table"))
                dimension_tables[d.name] = level.get("table")
        
        # 2. 使用维度定义的 join_path 构建 JOIN
        joins = []
        seen_tables = {metrics[0].measure.table}
        
        for d in dimensions:
            join_path = d.join_path
            if join_path["to_table"] not in seen_tables:
                joins.append({
                    "table": join_path["to_table"],
                    "alias": f"_{d.name}",
                    "on": f"{join_path['from_table']}.{join_path['from_column']} "
                          f"= _{d.name}.{join_path['to_column']}",
                    "type": join_path.get("join_type", "LEFT"),
                })
                seen_tables.add(join_path["to_table"])
        
        return joins
    
    def _build_aggregation_expr(self, metric) -> str:
        """构建聚合表达式"""
        agg = metric.type.value
        col = f"{metric.measure.table}.{metric.measure.column}"
        
        if metric.type == AggregationType.COUNT_DISTINCT:
            return f"COUNT(DISTINCT {col})"
        elif metric.type == AggregationType.RATIO:
            num = metric.measure.numerator
            den = metric.measure.denominator
            return f"SAFE_DIVIDE({agg}({num}), {agg}({den}))"
        else:
            return f"{agg}({col})"
    
    def _build_where(
        self, filters: dict, time_range: tuple, metrics: List
    ) -> List[str]:
        """构建 WHERE 子句"""
        where = []
        
        # 时间范围
        start, end = time_range
        where.append(f"dt BETWEEN '{start}' AND '{end}'")
        
        # 指标定义中的默认过滤条件
        for m in metrics:
            if m.measure.filter:
                where.append(m.measure.filter)
        
        # 用户指定的维度过滤
        for dim_name, value in filters.items():
            dim = self.dimensions.get(dim_name)
            filter_col = dim.hierarchy[0]["column"]
            if isinstance(value, list):
                values = ", ".join(f"'{v}'" for v in value)
                where.append(f"{filter_col} IN ({values})")
            else:
                where.append(f"{filter_col} = '{value}'")
        
        return where
    
    def _build_group_by(self, dimensions: List, granularity: str) -> List[str]:
        """构建 GROUP BY"""
        group_cols = []
        for d in dimensions:
            # 按最细粒度维度分组
            group_cols.append(d.hierarchy[-1]["column"])
        
        # 如果是趋势查询，加上时间粒度
        if granularity in ("daily", "weekly", "monthly"):
            group_cols.insert(0, "dt")
        
        return group_cols
    
    def _calculate_confidence(self, metrics, dimensions, intent) -> float:
        """
        计算当前解析的置信度
        
        影响因子：
        - 指标是否完全匹配（精确匹配 vs 模糊匹配）
        - 维度是否有效 JOIN（小基数高置信 → 大基数低置信）
        - 过滤条件是否明确（'北京' 明确 → '大城市' 模糊）
        - 时间范围是否精确（'2026-06-22' 精确 → '最近一阵' 模糊）
        
        返回 0.0 ~ 1.0
        """
        score = 1.0
        
        # 指标匹配度
        for m in metrics:
            if not m.verified:
                score -= 0.05
        
        # 维度基数惩罚——高基数字段更易出错
        for d in dimensions:
            if d.cardinality and d.cardinality > 10000:
                score -= 0.02
        
        # 过滤条件模糊度
        for value in intent.filters.values():
            if isinstance(value, str) and len(value) <= 2 and not value.isdigit():
                score -= 0.05  # 模糊缩写
        
        return max(0.0, min(1.0, score))
    
    def _gather_permissions(self, metrics, dimensions) -> List[str]:
        """收集查询所需权限"""
        perms = set()
        for m in metrics:
            perms.add(f"metric:{m.name}:read")
        for d in dimensions:
            perms.add(f"dim:{d.name}:read")
        return sorted(perms)
    
    def _collect_tables(self, joins: List[dict]) -> set:
        """收集所有涉及的表"""
        tables = set()
        for j in joins:
            tables.add(j["table"])
        return tables


class SemanticError(Exception):
    """语义解析错误 — 可理解、可修复的错误"""
    def __init__(self, message: str, suggestions: list = None):
        self.message = message
        self.suggestions = suggestions or []
        super().__init__(message)
```

### 2.2 SQL 编译器 (core/compiler/compiler.py)

```python
"""
SQL 编译器 —— 将 PhysicalQuery 编译为可执行的 SQL 语句。

确定性编译：相同输入必定产生相同 SQL。完全不使用 LLM。
"""

import sqlglot
from sqlglot import exp, errors
from typing import Optional
from dataclasses import dataclass

from core.compiler.ir import PhysicalQuery, Dialect
from core.compiler.optimizer import QueryOptimizer


class SQLCompiler:
    """
    PhysicalQuery → SQL String
    
    设计原则：
    1. 确定性：相同输入 → 相同输出，永不依赖概率模型
    2. 安全性：内置 LIMIT、禁止 DML、只读模式
    3. 方言适配：根据目标引擎（ClickHouse / Hive / StarRocks）生成方言 SQL
    """
    
    def __init__(self, dialect: Dialect = Dialect.CLICKHOUSE):
        self.dialect = dialect
        self.optimizer = QueryOptimizer()
    
    def compile(self, pq: PhysicalQuery) -> str:
        """主编译方法"""
        
        # 1. 构建 SELECT 子句
        select = self._compile_select(pq.select_columns)
        
        # 2. 构建 FROM 子句
        from_clause = self._compile_from(pq.main_table)
        
        # 3. 构建 JOIN 子句
        joins = self._compile_joins(pq.joins)
        
        # 4. 构建 WHERE 子句
        where = self._compile_where(pq.where_clauses)
        
        # 5. 构建 GROUP BY
        group_by = self._compile_group_by(pq.group_by)
        
        # 6. 构建 ORDER BY
        order_by = self._compile_order_by(pq.order_by)
        
        # 7. 构建 LIMIT（强制安全限制）
        limit = self._compile_limit(pq.limit)
        
        # 8. 组装 SQL
        sql = self._assemble(select, from_clause, joins, where, group_by, order_by, limit)
        
        # 9. SQL 方言转换 & 优化
        sql = self._to_dialect(sql)
        sql = self.optimizer.optimize(sql)
        
        # 10. 最终验证（使用 sqlglot 解析验证语法）
        self._validate_syntax(sql)
        
        return sql
    
    def _compile_select(self, columns: list) -> str:
        exprs = []
        for col in columns:
            exprs.append(f"  {col['expr']} AS {col['alias']}")
        return ",\n".join(exprs)
    
    def _compile_from(self, main_table: str) -> str:
        return f"FROM {main_table}"
    
    def _compile_joins(self, joins: list) -> str:
        lines = []
        for j in joins:
            lines.append(
                f"{j['type']} JOIN {j['table']} AS {j['alias']} "
                f"ON {j['on']}"
            )
        return "\n".join(lines)
    
    def _compile_where(self, clauses: list) -> str:
        if not clauses:
            return ""
        return "WHERE " + "\n  AND ".join(clauses)
    
    def _compile_group_by(self, columns: list) -> str:
        if not columns:
            return ""
        return "GROUP BY " + ", ".join(columns)
    
    def _compile_order_by(self, order: Optional[str]) -> str:
        if not order:
            return ""
        return f"ORDER BY {order}"
    
    def _compile_limit(self, limit: Optional[int]) -> str:
        # 强制上限：未指定 LIMIT 时默认 1000，最大不超过 50000
        if limit is None:
            limit = 1000
        return f"LIMIT {min(limit, 50000)}"
    
    def _assemble(self, *parts) -> str:
        sql = "SELECT\n"
        for part in parts:
            if part:
                sql += part + "\n"
        return sql.strip()
    
    def _to_dialect(self, sql: str) -> str:
        """将标准 SQL 转换为目标引擎方言"""
        try:
            parsed = sqlglot.parse_one(sql)
            return parsed.sql(dialect=self.dialect.value)
        except errors.ParseError:
            # 如果 sqlglot 无法解析，返回原始 SQL
            return sql
    
    def _validate_syntax(self, sql: str):
        """语法校验——无法解析则抛出异常"""
        try:
            sqlglot.parse_one(sql, dialect=self.dialect.value)
        except errors.ParseError as e:
            raise SQLCompileError(f"SQL 语法错误: {e}")


class SQLCompileError(Exception):
    pass
```

### 2.3 验证引擎 (core/verification/result_validator.py)

```python
"""
结果验证引擎 —— 多维度校验查询结果的合理性

验证维度：
1. 空值校验：关键指标不应为空
2. 量级校验：结果值与历史基线的量级一致性
3. 趋势校验：环比/同比变化是否在合理范围
4. 模式校验：维度分布是否合理（若适用）
5. 交叉校验：多个指标之间的逻辑关系自洽性

返回置信度评分，低于阈值时自动拒绝或标记需人工复核。
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import numpy as np


@dataclass
class ValidationResult:
    passed: bool
    overall_confidence: float          # 0.0 ~ 1.0
    checks: List[dict]                 # 各项检查详情
    warnings: List[str]                # 告警信息
    recommendation: str                # "accept" | "review" | "reject"


class ResultValidator:
    """
    结果验证器
    
    采用多层漏斗模型：
    Layer 1: 空值校验（快速失败）
    Layer 2: 量级校验（与历史基线对比）
    Layer 3: 趋势校验（统计异常检测）
    Layer 4: 业务规则校验（可配置）
    """
    
    def __init__(self, baseline_store, rule_engine):
        self.baseline = baseline_store     # 历史基线数据
        self.rules = rule_engine            # 业务规则引擎
    
    def validate(
        self, 
        result: dict, 
        intent: dict, 
        sql: str
    ) -> ValidationResult:
        """
        主验证入口
        
        Args:
            result: 查询结果 DataFrame
            intent: 原始意图
            sql: 执行的 SQL
        
        Returns:
            ValidationResult
        """
        checks = []
        warnings = []
        
        # Layer 1: 空值校验
        empty_check = self._check_emptiness(result, intent)
        checks.append(empty_check)
        if not empty_check["passed"]:
            return ValidationResult(
                passed=False,
                overall_confidence=0.0,
                checks=checks,
                warnings=["查询结果为空，请检查过滤条件是否过于严格或时间范围是否正确"],
                recommendation="reject",
            )
        
        # Layer 2: 量级校验（与近 7 天历史基线对比）
        magnitude_check = self._check_magnitude(result, intent)
        checks.append(magnitude_check)
        if not magnitude_check["passed"]:
            warnings.append(magnitude_check["message"])
        
        # Layer 3: 趋势校验（异常值检测）
        trend_check = self._check_trend(result, intent)
        checks.append(trend_check)
        if not trend_check["passed"]:
            warnings.append(trend_check["message"])
        
        # Layer 4: 业务规则校验
        for rule in self.rules.get_applicable_rules(intent):
            rule_check = rule.validate(result)
            checks.append(rule_check)
            if not rule_check["passed"]:
                warnings.append(rule_check["message"])
        
        # 综合置信度
        confidence = self._aggregate_confidence(checks)
        
        # 推荐决策
        if confidence >= 0.90:
            recommendation = "accept"
        elif confidence >= 0.70:
            recommendation = "review"
        else:
            recommendation = "reject"
        
        return ValidationResult(
            passed=confidence >= 0.70,
            overall_confidence=confidence,
            checks=checks,
            warnings=warnings,
            recommendation=recommendation,
        )
    
    def _check_emptiness(self, result, intent) -> dict:
        """空值校验"""
        row_count = len(result) if hasattr(result, '__len__') else result.shape[0]
        passed = row_count > 0
        return {
            "layer": "emptiness",
            "passed": passed,
            "detail": f"返回 {row_count} 行",
        }
    
    def _check_magnitude(self, result, intent) -> dict:
        """
        量级校验
        
        对比逻辑：
        1. 从 baseline_store 获取同指标、同时段的近 7 天历史均值
        2. 若当前值偏离历史均值超过 3σ（标准差），标记告警
        """
        metric_name = intent["metrics"][0]
        time_range = intent["time_range"]
        
        # 获取历史基线
        baseline = self.baseline.get(metric_name, time_range)
        if baseline is None:
            return {"layer": "magnitude", "passed": True, "detail": "无历史基线，跳过"}
        
        current_value = self._extract_metric_value(result, metric_name)
        historical_mean = baseline["mean"]
        historical_std = baseline["std"] or 1
        
        deviation = abs(current_value - historical_mean) / historical_std
        
        passed = deviation <= 3.0
        return {
            "layer": "magnitude",
            "passed": passed,
            "current_value": current_value,
            "historical_mean": historical_mean,
            "deviation_sigma": round(deviation, 2),
            "detail": f"当前值偏离基线 {deviation:.1f}σ",
            "message": (
                ""
                if passed
                else f"{metric_name} 当前值 {current_value} 偏离近 7 天均值 {historical_mean}，"
                     f"偏离 {deviation:.1f} 倍标准差，建议人工复核"
            ),
        }
    
    def _check_trend(self, result, intent) -> dict:
        """
        趋势校验
        
        使用简单但有效的 Z-Score 异常检测：
        - 时间序列数据按日展开，计算每日 Z-Score
        - 若某日 |Z-Score| > 3，标记告警
        """
        # 如果只有汇总值，跳过趋势校验
        if intent.get("granularity") == "summary":
            return {"layer": "trend", "passed": True, "detail": "汇总查询，跳过趋势校验"}
        
        # 提取时序数据
        values = self._extract_time_series(result)
        if len(values) < 3:
            return {"layer": "trend", "passed": True, "detail": "数据点不足，跳过趋势校验"}
        
        # Z-Score 计算
        mean = np.mean(values)
        std = np.std(values) or 1
        z_scores = [(v - mean) / std for v in values]
        anomalies = [i for i, z in enumerate(z_scores) if abs(z) > 3]
        
        passed = len(anomalies) == 0
        return {
            "layer": "trend",
            "passed": passed,
            "anomaly_count": len(anomalies),
            "detail": f"检测到 {len(anomalies)} 个异常点" if anomalies else "趋势正常",
            "message": (
                ""
                if passed
                else f"检测到 {len(anomalies)} 个异常数据点，请确认数据是否正确"
            ),
        }
    
    def _aggregate_confidence(self, checks: List[dict]) -> float:
        """综合各项检查，计算最终置信度"""
        weights = {
            "emptiness": 0.30,
            "magnitude": 0.25,
            "trend": 0.20,
            "business_rule": 0.25,
        }
        score = 0.0
        for check in checks:
            layer = check.get("layer", "business_rule")
            weight = weights.get(layer, 0.1)
            if check["passed"]:
                score += weight
        return score
```

### 2.4 LLM 网关 (llm/gateway.py)

```python
"""
LLM 网关 —— 多模型统一接入、自动故障转移、Token 计数与成本控制
"""

import asyncio
import time
from dataclasses import dataclass, field
from typing import Optional, List, Dict, AsyncIterator
from enum import Enum

import litellm
from litellm import completion, acompletion


class ModelTier(Enum):
    """模型分层"""
    LIGHT = "light"       # 快速小模型 (3B-7B) — 意图路由、Schema 筛选
    STANDARD = "standard" # 标准模型 (70B) — 意图解析、时间理解
    HEAVY = "heavy"       # 最强模型 — 复杂归因分析、报告生成


@dataclass
class ModelConfig:
    model_id: str
    tier: ModelTier
    max_tokens: int
    cost_per_1k_input: float
    cost_per_1k_output: float
    rate_limit_rpm: int
    supports_json_mode: bool = True


# 模型注册表
MODEL_REGISTRY: Dict[str, ModelConfig] = {
    "deepseek-v4-flash": ModelConfig(
        model_id="deepseek/deepseek-v4-flash",
        tier=ModelTier.LIGHT,
        max_tokens=4096,
        cost_per_1k_input=0.00014,
        cost_per_1k_output=0.00028,
        rate_limit_rpm=500,
    ),
    "deepseek-v4-pro": ModelConfig(
        model_id="deepseek/deepseek-v4-pro",
        tier=ModelTier.STANDARD,
        max_tokens=8192,
        cost_per_1k_input=0.000435,
        cost_per_1k_output=0.00087,
        rate_limit_rpm=200,
    ),
    "claude-haiku-4-5": ModelConfig(
        model_id="claude-haiku-4-5-20251001",
        tier=ModelTier.LIGHT,
        max_tokens=4096,
        cost_per_1k_input=0.001,
        cost_per_1k_output=0.005,
        rate_limit_rpm=1000,
    ),
    "claude-sonnet-4-6": ModelConfig(
        model_id="claude-sonnet-4-6-20250701",
        tier=ModelTier.STANDARD,
        max_tokens=8192,
        cost_per_1k_input=0.003,
        cost_per_1k_output=0.015,
        rate_limit_rpm=400,
    ),
    "claude-opus-4-8": ModelConfig(
        model_id="claude-opus-4-8-20250601",
        tier=ModelTier.HEAVY,
        max_tokens=16384,
        cost_per_1k_input=0.015,
        cost_per_1k_output=0.075,
        rate_limit_rpm=100,
    ),
}


class LLMGateway:
    """
    LLM 网关
    
    核心能力：
    1. 多模型路由：根据任务复杂度和成本自动选择模型
    2. 故障转移：主模型不可用时自动切换到备用模型
    3. 限流保护：防止超出 API 限额
    4. 成本追踪：每次调用记录 Token 消耗和费用
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.default_model = config.get("default_model", "deepseek-v4-pro")
        self.light_model = config.get("light_model", "deepseek-v4-flash")
        self.heavy_model = config.get("heavy_model", "deepseek-v4-pro")
        self.max_retries = config.get("max_retries", 3)
        self.fallback_chain = config.get(
            "fallback_chain",
            ["deepseek-v4-pro", "deepseek-v4-flash"],
        )
        
        # 限流器
        self._rate_limiters = {}
        
        # 成本追踪
        self._total_cost = 0.0
        self._total_tokens = 0
    
    async def chat(
        self,
        messages: List[dict],
        model: Optional[str] = None,
        tier: Optional[ModelTier] = None,
        json_mode: bool = False,
        temperature: float = 0.1,   # 数据分析任务用低温度
        max_tokens: Optional[int] = None,
    ) -> dict:
        """
        发送 chat 请求
        
        自动选择模型：
        - 若指定 model，直接用指定模型
        - 若指定 tier，从该 tier 中选择
        - 否则使用 default_model
        """
        model_id = model or self._select_model_by_tier(tier)
        
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = await acompletion(
                    model=model_id,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens or 4096,
                    response_format={"type": "json_object"} if json_mode else None,
                )
                
                # 追踪成本
                self._track_cost(model_id, response)
                
                return response
                
            except litellm.RateLimitError:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # 指数退避
                    continue
                raise
                
            except (litellm.ServiceUnavailableError, litellm.APIError) as e:
                last_error = e
                # 尝试故障转移
                fallback = self._get_fallback(model_id, attempt)
                if fallback:
                    model_id = fallback
                    continue
                raise
        
        raise LLMError(f"所有重试和故障转移均失败: {last_error}")
    
    def _select_model_by_tier(self, tier: Optional[ModelTier]) -> str:
        if tier == ModelTier.LIGHT:
            return self.light_model
        elif tier == ModelTier.HEAVY:
            return self.heavy_model
        return self.default_model
    
    def _get_fallback(self, failed_model: str, attempt: int) -> Optional[str]:
        """获取故障转移模型"""
        try:
            return self.fallback_chain[attempt]
        except IndexError:
            return None
    
    def _track_cost(self, model_id: str, response):
        """追踪成本和 Token 消耗"""
        usage = response.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)
        
        model_cfg = MODEL_REGISTRY.get(model_id)
        if model_cfg:
            cost = (
                input_tokens * model_cfg.cost_per_1k_input / 1000
                + output_tokens * model_cfg.cost_per_1k_output / 1000
            )
            self._total_cost += cost
        self._total_tokens += input_tokens + output_tokens
    
    def get_usage_report(self) -> dict:
        return {
            "total_cost_usd": round(self._total_cost, 4),
            "total_tokens": self._total_tokens,
        }


class LLMError(Exception):
    pass
```
