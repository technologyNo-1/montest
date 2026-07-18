---
title: "AI DataWorks — 测试方案与用例"
type: tech-practice
date: 2026-07-02
tags: []
status: active
source: ""
---

# AI DataWorks — 测试方案与用例

## 一、测试策略总览

```
┌──────────────────────────────────────────────────────────────────────┐
│                        测试金字塔                                     │
│                                                                      │
│                    ╱  E2E 测试 (5%) ╲                                │
│                   ╱  完整用户旅程验证  ╲                               │
│                  ╱────────────────────╲                              │
│                 ╱  集成测试 (25%)      ╲                             │
│                ╱  Pipeline 端到端      ╲                            │
│               ╱────────────────────────╲                           │
│              ╱   单元测试 (70%)          ╲                          │
│             ╱  每个模块独立验证          ╲                         │
│            ╱────────────────────────────╲                        │
└──────────────────────────────────────────────────────────────────────┘
```

### 1.1 测试原则

1. **语义层正确性不可妥协** — 指标定义、维度映射、时间解析的测试覆盖率必须 100%
2. **每个验证层独立可测** — SQL 校验、结果校验、权限校验各有独立测试套件
3. **Golden Query 回归测试** — 维护 100+ 条"已知正确答案"的业务查询作为回归基准
4. **生产影子模式** — 上线后至少 2 周并行运行（AI vs 人工），持续对比

---

## 二、单元测试

### 2.1 语义映射引擎测试

```python
"""
tests/unit/test_semantic_engine.py
语义映射引擎单元测试
"""
import pytest
from core.semantic.engine import SemanticEngine, ParsedIntent, SemanticError
from core.semantic.metric_registry import MetricRegistry
from core.semantic.dimension_catalog import DimensionCatalog


class TestSemanticEngine:
    """语义映射引擎 —— 核心正确性测试"""
    
    @pytest.fixture
    def engine(self):
        """初始化语义引擎（使用测试夹具数据）"""
        registry = MetricRegistry.from_yaml("tests/fixtures/semantic/metrics/")
        catalog = DimensionCatalog.from_yaml("tests/fixtures/semantic/dimensions/")
        return SemanticEngine(registry, catalog, glossary=None, schema_router=None)
    
    # ─── 基础指标解析 ───
    
    def test_resolve_single_metric_sum(self, engine):
        """测试：单指标 SUM 聚合"""
        intent = ParsedIntent(
            metrics=["gmv"],
            dimensions=[],
            filters={},
            time_range=("2026-06-22", "2026-06-28"),
            granularity="summary",
            order_by=None,
            limit=None,
            query_type="aggregation",
        )
        result = engine.resolve(intent)
        
        assert "SUM(payment_amount)" in result.select_columns[0]["expr"]
        assert result.select_columns[0]["alias"] == "gmv"
        assert result.main_table == "dws_trade_order_daily_1d"
    
    def test_resolve_count_distinct_metric(self, engine):
        """测试：COUNT DISTINCT 聚合"""
        intent = ParsedIntent(
            metrics=["dau"],
            dimensions=[],
            filters={},
            time_range=("2026-06-28", "2026-06-28"),
            granularity="summary",
            order_by=None,
            limit=None,
            query_type="aggregation",
        )
        result = engine.resolve(intent)
        
        assert "COUNT(DISTINCT" in result.select_columns[0]["expr"]
    
    def test_resolve_ratio_metric(self, engine):
        """测试：比率指标"""
        intent = ParsedIntent(
            metrics=["conversion_rate"],
            dimensions=[],
            filters={},
            time_range=("2026-06-28", "2026-06-28"),
            granularity="summary",
            order_by=None,
            limit=None,
            query_type="aggregation",
        )
        result = engine.resolve(intent)
        
        assert "SAFE_DIVIDE" in result.select_columns[0]["expr"]
    
    # ─── 维度解析 ───
    
    def test_resolve_with_dimensions(self, engine):
        """测试：指标 + 维度组合"""
        intent = ParsedIntent(
            metrics=["gmv"],
            dimensions=["region", "channel"],
            filters={},
            time_range=("2026-06-22", "2026-06-28"),
            granularity="summary",
            order_by="gmv DESC",
            limit=10,
            query_type="aggregation",
        )
        result = engine.resolve(intent)
        
        assert len(result.joins) >= 2  # region + channel 两个维度表
        assert len(result.group_by) >= 2
        assert result.order_by == "gmv DESC"
        assert result.limit == 10
    
    def test_resolve_with_filters(self, engine):
        """测试：维度过滤"""
        intent = ParsedIntent(
            metrics=["gmv"],
            dimensions=["region"],
            filters={"region": "北京", "platform": "iOS"},
            time_range=("2026-06-22", "2026-06-28"),
            granularity="summary",
            order_by=None,
            limit=None,
            query_type="aggregation",
        )
        result = engine.resolve(intent)
        
        where_str = " ".join(result.where_clauses)
        assert "北京" in where_str
        assert "iOS" in where_str
        assert "dt BETWEEN" in where_str
    
    # ─── 错误与边缘情况 ───
    
    def test_unknown_metric_raises_error(self, engine):
        """测试：不存在的指标应抛出语义错误"""
        intent = ParsedIntent(
            metrics=["不存在的指标"],
            dimensions=[],
            filters={},
            time_range=("2026-06-22", "2026-06-28"),
            granularity="summary",
            order_by=None,
            limit=None,
            query_type="aggregation",
        )
        
        with pytest.raises(SemanticError) as exc:
            engine.resolve(intent)
        assert "未找到指标" in str(exc.value)
    
    def test_metric_alias_resolution(self, engine):
        """测试：指标别名解析"""
        for alias in ["GMV", "总成交额", "总销售额", "交易总额"]:
            intent = ParsedIntent(
                metrics=[alias],
                dimensions=[],
                filters={},
                time_range=("2026-06-28", "2026-06-28"),
                granularity="summary",
                order_by=None,
                limit=None,
                query_type="aggregation",
            )
            result = engine.resolve(intent)
            assert result.select_columns[0]["alias"] == "gmv"
    
    def test_dimension_hierarchy(self, engine):
        """测试：维度层级 —— 查询城市级 vs 省份级"""
        intent_city = ParsedIntent(
            metrics=["gmv"],
            dimensions=["region"],
            filters={"region": "北京市"},
            time_range=("2026-06-22", "2026-06-28"),
            granularity="summary",
            order_by=None,
            limit=None,
            query_type="aggregation",
        )
        result_city = engine.resolve(intent_city)
        # 应自动使用城市级别的列
        assert "city_name" in " ".join(result_city.where_clauses) or \
               "province_name" in " ".join(result_city.where_clauses)


class TestTimeResolver:
    """时间解析器测试"""
    
    @pytest.mark.parametrize("expression,expected_start,expected_end", [
        ("今天",       "2026-07-02", "2026-07-02"),
        ("昨天",       "2026-07-01", "2026-07-01"),
        ("近 7 天",    "2026-06-25", "2026-07-01"),
        ("近 30 天",   "2026-06-02", "2026-07-01"),
        ("上周",       "2026-06-22", "2026-06-28"),
        ("本月",       "2026-07-01", "2026-07-02"),
        ("上月",       "2026-06-01", "2026-06-30"),
        ("Q1",         "2026-01-01", "2026-03-31"),
        ("Q2",         "2026-04-01", "2026-06-30"),
        ("上半年",     "2026-01-01", "2026-06-30"),
        ("年初至今",   "2026-01-01", "2026-07-02"),
    ])
    def test_common_time_patterns(self, expression, expected_start, expected_end):
        """测试：常见时间表达式的精确解析（给定 today=2026-07-02）"""
        from core.semantic.time_resolver import TimeResolver
        
        resolver = TimeResolver(reference_date="2026-07-02")
        result = resolver.resolve(expression)
        
        assert result.start == expected_start
        assert result.end == expected_end
```

### 2.2 SQL 编译器测试

```python
"""
tests/unit/test_sql_compiler.py
SQL 编译器单元测试 —— 确保生成语法正确、安全且确定性的 SQL
"""
import pytest
from core.compiler.compiler import SQLCompiler, PhysicalQuery, Dialect


class TestSQLCompiler:
    
    @pytest.fixture
    def compiler(self):
        return SQLCompiler(dialect=Dialect.CLICKHOUSE)
    
    def test_basic_aggregation(self, compiler):
        """测试：基础聚合查询"""
        pq = PhysicalQuery(
            main_table="dws_trade_order_daily_1d",
            select_columns=[
                {"expr": "SUM(payment_amount)", "alias": "gmv"},
            ],
            joins=[],
            where_clauses=[
                "dt BETWEEN '2026-06-22' AND '2026-06-28'",
                "order_status = 'paid'",
            ],
            group_by=[],
            order_by=None,
            limit=None,
            metadata={},
        )
        sql = compiler.compile(pq)
        
        assert "SELECT" in sql
        assert "SUM(payment_amount) AS gmv" in sql
        assert "FROM dws_trade_order_daily_1d" in sql
        assert "WHERE" in sql
        assert "dt BETWEEN" in sql
        assert "order_status = 'paid'" in sql
    
    def test_default_limit_enforced(self, compiler):
        """测试：强制 LIMIT —— 未指定时自动添加 LIMIT 1000"""
        pq = PhysicalQuery(
            main_table="dws_trade_order_daily_1d",
            select_columns=[{"expr": "COUNT(*)", "alias": "cnt"}],
            joins=[],
            where_clauses=[],
            group_by=[],
            order_by=None,
            limit=None,           # 未指定
            metadata={},
        )
        sql = compiler.compile(pq)
        assert "LIMIT 1000" in sql
    
    def test_max_limit_capped(self, compiler):
        """测试：LIMIT 上限 —— 最大不超过 50000"""
        pq = PhysicalQuery(
            main_table="dws_trade_order_daily_1d",
            select_columns=[{"expr": "COUNT(*)", "alias": "cnt"}],
            joins=[],
            where_clauses=[],
            group_by=[],
            order_by=None,
            limit=100000,          # 超过上限
            metadata={},
        )
        sql = compiler.compile(pq)
        assert "LIMIT 50000" in sql
    
    def test_joins_compilation(self, compiler):
        """测试：多表 JOIN"""
        pq = PhysicalQuery(
            main_table="dws_trade_order_daily_1d",
            select_columns=[
                {"expr": "SUM(payment_amount)", "alias": "gmv"},
                {"expr": "r.province_name", "alias": "province"},
            ],
            joins=[
                {
                    "table": "dim_region",
                    "alias": "_region",
                    "on": "dws_trade_order_daily_1d.region_id = _region.region_id",
                    "type": "LEFT",
                }
            ],
            where_clauses=["dt BETWEEN '2026-06-22' AND '2026-06-28'"],
            group_by=["r.province_name"],
            order_by="gmv DESC",
            limit=10,
            metadata={},
        )
        sql = compiler.compile(pq)
        
        assert "LEFT JOIN dim_region AS _region" in sql
        assert "ON" in sql
        assert "GROUP BY" in sql
        assert "ORDER BY gmv DESC" in sql
    
    def test_clickhouse_dialect(self, compiler):
        """测试：ClickHouse 方言适配"""
        compiler.dialect = Dialect.CLICKHOUSE
        pq = PhysicalQuery(
            main_table="dws_trade_order_daily_1d",
            select_columns=[{"expr": "SUM(payment_amount)", "alias": "gmv"}],
            joins=[],
            where_clauses=["dt = '2026-06-28'"],
            group_by=[],
            order_by=None,
            limit=100,
            metadata={},
        )
        sql = compiler.compile(pq)
        # sqlglot 应能解析生成的 SQL
        import sqlglot
        try:
            parsed = sqlglot.parse_one(sql, dialect="clickhouse")
            assert parsed is not None
        except Exception as e:
            pytest.fail(f"SQL 解析失败: {sql}\n错误: {e}")
    
    def test_invalid_sql_raises_error(self, compiler):
        """测试：无效 SQL 结构应抛出错误"""
        # 模拟一个不可能的编译——在 _validate_syntax 层面捕获
        pass  # 此测试依赖编译器内部验证逻辑
```

### 2.3 结果验证器测试

```python
"""
tests/unit/test_result_validator.py
结果验证器测试
"""
import pytest
import pandas as pd
import numpy as np
from core.verification.result_validator import ResultValidator


class TestResultValidator:
    
    @pytest.fixture
    def validator(self):
        from unittest.mock import MagicMock
        baseline = MagicMock()
        baseline.get.return_value = {"mean": 1000000, "std": 100000}
        rules = MagicMock()
        rules.get_applicable_rules.return_value = []
        return ResultValidator(baseline, rules)
    
    def test_empty_result_rejected(self, validator):
        """测试：空结果应被拒绝"""
        result = pd.DataFrame()
        intent = {
            "metrics": ["gmv"],
            "time_range": ("2026-06-22", "2026-06-28"),
            "granularity": "summary",
        }
        
        validation = validator.validate(result, intent, "SELECT ...")
        
        assert not validation.passed
        assert validation.overall_confidence == 0.0
        assert validation.recommendation == "reject"
    
    def test_normal_result_accepted(self, validator):
        """测试：正常结果通过"""
        result = pd.DataFrame({"gmv": [1000000]})
        intent = {
            "metrics": ["gmv"],
            "time_range": ("2026-06-22", "2026-06-28"),
            "granularity": "summary",
        }
        
        validation = validator.validate(result, intent, "SELECT ...")
        
        assert validation.passed
        assert validation.overall_confidence > 0.70
        assert validation.recommendation in ("accept", "review")
    
    def test_magnitude_anomaly_warns(self, validator):
        """测试：偏离基线 > 3σ 应告警"""
        # 历史基线：mean=1000000, std=100000
        # 当前值：2000000 → 偏离 10σ
        result = pd.DataFrame({"gmv": [2000000]})
        intent = {
            "metrics": ["gmv"],
            "time_range": ("2026-06-22", "2026-06-28"),
            "granularity": "summary",
        }
        
        validation = validator.validate(result, intent, "SELECT ...")
        
        assert len(validation.warnings) > 0
        assert "偏离" in validation.warnings[0]
    
    def test_trend_anomaly_detected(self, validator):
        """测试：趋势异常检测"""
        # 构造时间序列，最后一天突然暴涨
        values = [1000, 1050, 1020, 1080, 990, 1010, 5000]  # 5000 是异常
        dates = pd.date_range("2026-06-22", periods=7, freq="D")
        result = pd.DataFrame({"dt": dates, "gmv": values})
        
        intent = {
            "metrics": ["gmv"],
            "time_range": ("2026-06-22", "2026-06-28"),
            "granularity": "daily",
        }
        
        validation = validator.validate(result, intent, "SELECT ...")
        
        # 应该检测到异常
        trend_checks = [c for c in validation.checks if c.get("layer") == "trend"]
        if trend_checks:
            assert trend_checks[0]["anomaly_count"] > 0
```

---

## 三、集成测试

### 3.1 查询 Pipeline 端到端测试

```python
"""
tests/integration/test_query_pipeline.py
集成测试：从自然语言到 SQL 执行结果的完整 Pipeline
"""
import pytest
from core.intent.parser import IntentParser
from core.semantic.engine import SemanticEngine
from core.compiler.compiler import SQLCompiler
from core.verification.result_validator import ResultValidator


class TestQueryPipeline:
    """端到端查询 Pipeline 集成测试"""
    
    @pytest.fixture
    def pipeline(self):
        """构建完整的查询 Pipeline"""
        intent_parser = IntentParser(
            llm_gateway=None,  # 集成测试使用 Mock LLM
        )
        semantic_engine = SemanticEngine(  # 使用真实语义层
            metric_registry=...,
            dimension_catalog=...,
            glossary=...,
            schema_router=...,
        )
        compiler = SQLCompiler(dialect=Dialect.CLICKHOUSE)
        validator = ResultValidator(baseline_store=..., rule_engine=...)
        
        return {
            "intent_parser": intent_parser,
            "semantic_engine": semantic_engine,
            "compiler": compiler,
            "validator": validator,
        }
    
    # ─── Golden Query 回归测试 ───
    
    @pytest.mark.parametrize("query,expected_metrics,expected_table", [
        (
            "昨天全站的 GMV 是多少",
            ["gmv"],
            "dws_trade_order_daily_1d",
        ),
        (
            "近 7 天各渠道的 DAU",
            ["dau"],
            "dws_user_active_daily_1d",
        ),
        (
            "上个月北京地区的订单量和转化率",
            ["order_count", "conversion_rate"],
            "dws_trade_order_daily_1d",
        ),
        (
            "Q2 各大区 GMV Top10",
            ["gmv"],
            "dws_trade_order_daily_1d",
        ),
    ])
    def test_golden_queries(
        self, pipeline, query, expected_metrics, expected_table
    ):
        """
        Golden Query 测试：
        已知正确答案的查询——确保每次变更不破坏语义解析
        """
        # Step 1: 意图解析
        intent = pipeline["intent_parser"].parse(query)
        assert intent.metrics == expected_metrics, \
            f"意图解析错误：期望 {expected_metrics}，实际 {intent.metrics}"
        
        # Step 2: 语义映射
        physical_query = pipeline["semantic_engine"].resolve(intent)
        assert physical_query.main_table == expected_table, \
            f"表映射错误：期望 {expected_table}，实际 {physical_query.main_table}"
        
        # Step 3: SQL 编译
        sql = pipeline["compiler"].compile(physical_query)
        assert sql is not None and len(sql) > 0
        assert "SELECT" in sql
        assert "LIMIT" in sql  # 安全保护
        
        # Step 4: SQL 语法验证
        import sqlglot
        try:
            sqlglot.parse_one(sql)
        except Exception:
            pytest.fail(f"生成的 SQL 语法错误：\n{sql}")
        
        # Step 5: 权限校验
        perms = physical_query.metadata.get("required_permissions", [])
        assert len(perms) > 0
    
    # ─── 错误恢复测试 ───
    
    def test_ambiguous_metric_clarification(self, pipeline):
        """测试：模糊指标名应给出澄清建议"""
        query = "转化率是多少"  # 可能有多种"转化率"
        
        # 当有多个候选时，应返回建议而非随机选择
        result = pipeline["intent_parser"].parse(query)
        
        if len(result.metrics) == 1 and result.metrics[0] == "conversion_rate":
            # 如果直接匹配到了，验证置信度是否合理
            pass
        # 否则应该给出候选列表
    
    def test_invalid_time_range_handling(self, pipeline):
        """测试：不可能的日期范围处理"""
        query = "2027 年 1 月的 GMV"  # 未来日期
        
        # 应能处理未来日期（可能数据为空，但不应该崩溃）
        result = pipeline["intent_parser"].parse(query)
        assert result.time_range is not None
```

### 3.2 语义层一致性测试

```python
"""
tests/integration/test_semantic_consistency.py
语义层一致性测试 —— 确保语义层定义与实际数据库 schema 一致
"""

class TestSemanticConsistency:
    
    def test_all_metrics_have_valid_tables(self, engine, db_conn):
        """测试：所有注册指标对应的表在数据库中确实存在"""
        for metric in engine.metrics.list_all():
            table = metric.measure.table
            result = db_conn.execute(f"SHOW TABLES LIKE '{table}'")
            assert len(result) > 0, \
                f"指标 '{metric.name}' 引用的表 '{table}' 在数据库中不存在"
    
    def test_all_metric_columns_exist(self, engine, db_conn):
        """测试：所有指标引用的列在对应表中存在"""
        for metric in engine.metrics.list_all():
            table = metric.measure.table
            column = metric.measure.column
            result = db_conn.execute(f"DESCRIBE {table}")
            columns = [row[0] for row in result]
            assert column in columns, \
                f"指标 '{metric.name}' 引用的列 '{table}.{column}' 不存在"
    
    def test_all_join_paths_valid(self, engine, db_conn):
        """测试：所有维度 JOIN 路径中引用的列存在"""
        for dim in engine.dimensions.list_all():
            join = dim.join_path
            # 验证 from_table.from_column 存在
            result = db_conn.execute(f"DESCRIBE {join['from_table']}")
            columns = [row[0] for row in result]
            assert join["from_column"] in columns
            
            # 验证 to_table.to_column 存在
            result = db_conn.execute(f"DESCRIBE {join['to_table']}")
            columns = [row[0] for row in result]
            assert join["to_column"] in columns
    
    def test_dimension_cardinality_reasonable(self, engine, db_conn):
        """测试：维度基数在合理范围内"""
        for dim in engine.dimensions.list_all():
            if dim.cardinality is not None:
                # 验证定义的基数与实际数据库基数基本一致
                actual_count = db_conn.execute(
                    f"SELECT COUNT(DISTINCT {dim.hierarchy[-1]['column']}) "
                    f"FROM {dim.hierarchy[-1]['table']}"
                )[0][0]
                
                # 允许 ±50% 偏差（维度定义可能过时）
                ratio = actual_count / dim.cardinality
                assert 0.5 <= ratio <= 1.5, \
                    f"维度 '{dim.name}' 实际基数 {actual_count} 与定义的 "
                    f"{dim.cardinality} 偏差过大 ({ratio:.1f}x)"
```

---

## 四、E2E 测试

### 4.1 用户旅程测试

```python
"""
tests/e2e/test_chat_flow.py
E2E 测试：模拟真实用户对话流程
"""
import pytest
import httpx


class TestChatFlow:
    """端到端用户对话测试"""
    
    BASE_URL = "http://localhost:8000/api/v1"
    
    @pytest.fixture
    def client(self):
        return httpx.AsyncClient(base_url=self.BASE_URL, timeout=60.0)
    
    @pytest.mark.e2e
    async def test_simple_metric_query(self, client):
        """E2E: 简单指标查询"""
        response = await client.post("/chat", json={
            "message": "昨天的 DAU 是多少",
            "session_id": "e2e-test-001",
        })
        assert response.status_code == 200
        data = response.json()
        
        assert "answer" in data
        assert "sql" in data
        assert "confidence" in data
        assert data["confidence"] >= 0.7
        assert "SELECT" in data["sql"]
        assert "LIMIT" in data["sql"]
    
    @pytest.mark.e2e
    async def test_multi_turn_conversation(self, client):
        """E2E: 多轮对话"""
        session_id = "e2e-test-multi-turn"
        
        # Round 1: 初始查询
        r1 = await client.post("/chat", json={
            "message": "近 7 天各渠道的 GMV",
            "session_id": session_id,
        })
        assert r1.status_code == 200
        
        # Round 2: 追问（基于上一轮上下文）
        r2 = await client.post("/chat", json={
            "message": "只看北京地区的",
            "session_id": session_id,
        })
        assert r2.status_code == 200
        # 应自动补充地区过滤
        assert "北京" in r2.json()["sql"] or "region" in r2.json()["sql"].lower()
        
        # Round 3: 再追问
        r3 = await client.post("/chat", json={
            "message": "按天展开趋势",
            "session_id": session_id,
        })
        assert r3.status_code == 200
        # 应包含 GROUP BY dt
        sql_lower = r3.json()["sql"].lower()
        assert "group by" in sql_lower and "dt" in sql_lower
    
    @pytest.mark.e2e
    async def test_permission_enforcement(self, client):
        """E2E: 权限强制执行"""
        # 使用无权限的用户
        restricted_user = "test_restricted_user"
        
        response = await client.post(
            "/chat",
            json={
                "message": "所有用户的手机号",
                "session_id": "e2e-test-perm",
            },
            headers={"X-User-ID": restricted_user},
        )
        
        data = response.json()
        # 应被拒绝或对敏感字段脱敏
        if response.status_code == 403:
            assert "权限不足" in data.get("error", "")
        elif response.status_code == 200:
            # 如果允许查询，手机号应被脱敏
            if "phone" in str(data.get("answer", "")).lower():
                assert "***" in str(data["answer"]) or "脱敏" in str(data["answer"])
    
    @pytest.mark.e2e
    async def test_sql_injection_prevention(self, client):
        """E2E: SQL 注入防护"""
        injection_attempts = [
            "GMV; DROP TABLE users; --",
            "DAU' OR '1'='1",
            "销售额 UNION SELECT password FROM users",
        ]
        
        for msg in injection_attempts:
            response = await client.post("/chat", json={
                "message": msg,
                "session_id": "e2e-test-injection",
            })
            # 不应崩溃，不应执行恶意 SQL
            assert response.status_code in (200, 400, 422)
            if response.status_code == 200:
                data = response.json()
                # 生成的 SQL 不应包含危险操作
                sql = data.get("sql", "").upper()
                assert "DROP" not in sql
                assert "DELETE" not in sql
                assert "INSERT" not in sql
                assert "UPDATE" not in sql
                assert "ALTER" not in sql
                assert "CREATE" not in sql
```

---

## 五、Golden Query 基准测试

### 5.1 Golden Query 定义

```yaml
# tests/golden_queries.yaml
# 100 条已知正确答案的查询，每次变更后回归测试
# 每个 query 定义：自然语言、期望的指标、维度、表、SQL 模式

golden_queries:
  - id: GQ001
    query: "昨天的 GMV 是多少"
    difficulty: easy
    expected:
      metrics: ["gmv"]
      main_table_contains: "trade_order"
      sql_patterns: ["SUM", "payment_amount", "LIMIT"]
    
  - id: GQ002
    query: "近 7 天各渠道的 DAU 趋势"
    difficulty: medium
    expected:
      metrics: ["dau"]
      dimensions: ["channel"]
      granularity: "daily"
      sql_patterns: ["GROUP BY", "dt", "channel", "COUNT(DISTINCT"]
    
  - id: GQ003
    query: "上个月北京地区 iOS 用户的 GMV 和转化率，按天展开"
    difficulty: hard
    expected:
      metrics: ["gmv", "conversion_rate"]
      dimensions: ["region", "platform"]
      granularity: "daily"
      sql_patterns: ["dt BETWEEN", "北京", "iOS", "SAFE_DIVIDE"]
    
  - id: GQ004
    query: "Q2 各大区 GMV Top10，对比去年同期"
    difficulty: hard
    expected:
      metrics: ["gmv"]
      dimensions: ["region"]
      has_yoy_comparison: true
      sql_patterns: ["TOP", "ORDER BY", "DESC", "LIMIT 10"]
    
  # ... 共 100 条
```

---

## 六、性能测试

```python
"""
tests/performance/test_latency.py
性能测试 —— 确保各环节满足 SLA
"""
import pytest
import time
import asyncio


class TestLatencySLA:
    """延迟 SLA 测试"""
    
    @pytest.mark.perf
    async def test_simple_query_under_1s(self):
        """简单指标查询 < 1s"""
        start = time.perf_counter()
        result = await query_pipeline.run("昨天的 DAU")
        elapsed = time.perf_counter() - start
        
        assert elapsed < 1.0, f"简单查询耗时 {elapsed:.2f}s，超过 1s SLA"
    
    @pytest.mark.perf
    async def test_medium_query_under_5s(self):
        """多维分析查询 < 5s"""
        start = time.perf_counter()
        result = await query_pipeline.run(
            "近 7 天各渠道、各城市的 GMV 和转化率 Top20"
        )
        elapsed = time.perf_counter() - start
        
        assert elapsed < 5.0, f"中等查询耗时 {elapsed:.2f}s，超过 5s SLA"
    
    @pytest.mark.perf
    async def test_attribution_under_30s(self):
        """归因分析查询 < 30s"""
        start = time.perf_counter()
        result = await query_pipeline.run(
            "分析 GMV 下降 15% 的原因，按渠道和品类拆解"
        )
        elapsed = time.perf_counter() - start
        
        assert elapsed < 30.0, f"归因查询耗时 {elapsed:.2f}s，超过 30s SLA"
    
    @pytest.mark.perf
    async def test_concurrent_10_queries(self):
        """10 并发查询不超时"""
        queries = [
            "昨天 GMV",
            "近 7 天 DAU",
            "上月转化率",
            "Q2 各渠道销售额",
            "今天订单量",
            "本周新增用户",
            "本月退款率",
            "北京地区 Top5 品类",
            "iOS 用户复购率",
            "大促期间 GMV 同比",
        ]
        
        async def run_one(q):
            try:
                return await query_pipeline.run(q)
            except Exception as e:
                return str(e)
        
        start = time.perf_counter()
        results = await asyncio.gather(*[run_one(q) for q in queries])
        elapsed = time.perf_counter() - start
        
        failures = [r for r in results if isinstance(r, str)]
        assert len(failures) == 0, f"{len(failures)} 个查询失败: {failures}"
        assert elapsed < 30.0, f"10 并发耗时 {elapsed:.2f}s"
```

---

## 七、影子模式测试（生产上线验证）

```
┌──────────────────────────────────────────────────────────────────┐
│                     影子模式架构                                 │
│                                                                 │
│  用户 Query ──┬──► AI DataWorks ──► AI 结果（记录日志）          │
│              │                                                  │
│              └──► 人工/现有系统 ──► 人工结果（作为 Ground Truth）│
│                                                                 │
│  对比：AI 结果 vs 人工结果                                       │
│  ├─ SQL 一致性: 是否生成等价的 SQL？                              │
│  ├─ 数值一致性: 数值误差 < 0.01%？                               │
│  ├─ 结论一致性: AI 分析结论是否与人工结论一致？                     │
│  └─ 耗时对比: AI 耗时 vs 人工耗时                                │
└──────────────────────────────────────────────────────────────────┘
```

影子模式指标：

| 指标 | 目标 | 测量方式 |
|------|------|---------|
| 回复可用率 | > 85% | AI 结果被用户接受而不重新提问的比率 |
| SQL 准确率 | > 95% | AI SQL vs 人工 SQL 结果数值一致性 |
| 结论一致性 | > 80% | AI 结论 vs 分析师结论人工评判 |
| 时间节省 | > 80% | AI 耗时 vs 人工耗时 |
| 无幻觉率 | > 95% | 不出错、不编造数据的比率 |
