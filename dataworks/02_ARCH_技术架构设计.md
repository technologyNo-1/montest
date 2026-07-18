# AI DataWorks — 技术架构设计文档

## 一、整体架构

### 1.1 架构分层

```
┌──────────────────────────────────────────────────────────────────┐
│                        交互层 (Interaction Layer)                 │
│  Web Chat UI │ Slack Bot │ 飞书 Bot │ API Gateway │ JDBC Proxy  │
└──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────┐
│                     智能体编排层 (Agent Orchestration)             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐ │
│  │ 意图路由器  │  │ 对话管理器  │  │ 任务规划器  │  │ 追问推荐器  │ │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────┐
│                     语义理解层 (Semantic Layer)    ★ 核心层       │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐ │
│  │ LLM 意图解析│  │ 语义映射引擎│  │ 时间解析器  │  │ 实体链接器  │ │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘ │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐ │
│  │ 指标注册中心│  │ 维度目录   │  │ Schema 路由 │  │ 权限解析器  │ │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────┐
│                     查询编译层 (Query Compiler)                    │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐ │
│  │ SQL 编译器  │  │ 查询优化器  │  │ 方言适配器  │  │ 多源联邦器  │ │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────┐
│                     验证 & 安全层 (Verification Layer)             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐ │
│  │ SQL 校验器  │  │ 结果验证器  │  │ 权限执行器  │  │ 置信度引擎  │ │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────┐
│                     执行层 (Execution Layer)                       │
│  ClickHouse │ StarRocks │ Hive │ MySQL │ Presto/Trino │ 缓存层   │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 技术选型

| 组件 | 选型 | 理由 |
|------|------|------|
| **后端框架** | Python FastAPI + asyncio | 异步高性能，生态成熟 |
| **LLM 网关** | LiteLLM + 自建 Router | 多模型统一接入，自动 fallback |
| **语义存储** | PostgreSQL + Apache Atlas | 结构化元数据 + 数据血缘 |
| **向量数据库** | Milvus | Schema/Query 相似检索 |
| **语义层引擎** | MetricFlow (dbt) + 自建 | 指标定义标准化 |
| **SQL 引擎** | sqlglot (解析/转换/方言) | Python 原生，支持 20+ 方言 |
| **查询引擎** | ClickHouse / StarRocks | OLAP 高性能 |
| **前端** | React + TypeScript + ECharts | 交互式分析体验 |
| **任务编排** | Temporal | 长任务、重试、可观测 |
| **消息队列** | Kafka | 异步事件驱动 |
| **监控** | Prometheus + Grafana | 全链路可观测 |

---

## 二、语义层设计（AI-ready Data Layer）

> 这是整个平台最重要的基础层，决定了自然语言分析的能力上限。
> 行业数据表明：**没有语义层，直接 NL2SQL 的业务准确率不足 50%。**

### 2.1 语义模型定义

#### 2.1.1 指标定义（Metric）

```yaml
# metrics/gmv.yaml
metric:
  name: gmv                                    # 唯一标识
  display_name: "总交易额(GMV)"
  aliases: ["GMV", "总成交额", "总销售额", "交易总额"]
  description: "用户实际支付完成的订单总金额，不含退款"
  type: SUM                                    # 聚合类型
  measure:                                     # 物理度量
    table: dws_trade_order_daily_1d
    column: payment_amount
    filter: "order_status = 'paid' AND is_refund = 0"
  dimensions:                                  # 可用维度
    - time: dt                                # 时间维度
    - region                                # 地区维度
    - channel                               # 渠道维度
    - platform                              # 平台维度
    - category                              # 品类维度
  unit: "元"
  precision: 2
  owner: "交易域"
  sla: "T+1 上午 8:00"
  history_queries:                            # 历史查询示例（用于 Few-shot）
    - "昨天的 GMV 是多少？"
    - "近 7 天各渠道的 GMV 趋势"
  verified: true
  last_verified_at: "2026-07-01"
```

#### 2.1.2 维度定义（Dimension）

```yaml
# dimensions/region.yaml
dimension:
  name: region
  display_name: "地区"
  aliases: ["区域", "大区", "省份", "城市", "地域"]
  type: categorical                          # categorical | temporal | numeric
  hierarchy:                                 # 维度层级
    - level: country
      table: dim_region
      column: country_name
    - level: province
      table: dim_region
      column: province_name
    - level: city
      table: dim_region
      column: city_name
  join_path:                                 # JOIN 路径
    - from_table: dws_trade_order_daily_1d
      from_column: region_id
      to_table: dim_region
      to_column: region_id
      join_type: LEFT
  allowed_operators: ["=", "IN", "IS NOT NULL"]
  cardinality: 350                           # 维度基数（用于优化）
```

#### 2.1.3 术语词典（Business Glossary）

```yaml
# glossary.yaml
terms:
  - term: "大促"
    definition: "平台级营销活动"
    time_mapping: "参照 dim_promotion_calendar 表"
    sql_filter: "dt IN (SELECT dt FROM dim_promotion_calendar WHERE promo_type = 'big_promo')"
    
  - term: "高价值用户"
    definition: "近 90 天累计消费 >= 10,000 元的用户"
    sql_filter: "user_lifetime_value >= 10000"
    
  - term: "转化率"
    definition: "下单用户数 / 访问用户数 * 100%"
    metric_ref: "conversion_rate"
    
  - term: "周活"
    definition: "Weekly Active Users，近 7 天至少活跃 1 次的去重用户数"
    metric_ref: "wau"
```

### 2.2 Schema 路由（Schema Linking）

当数仓有 500+ 张表时，无法全部塞入 LLM Context。Schema 路由解决了这个问题：

```
用户 Query: "北京 iOS 用户的 GMV"
    │
    ▼
┌─────────────────────────────────────────────────┐
│ Stage 1: BM25 关键词粗筛（低延迟）                │
│   "gmv" → 候选表: [trade_order_daily,            │
│                    trade_order_hourly, ...]      │
│   召回 top-30 张表                                │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│ Stage 2: 语义向量精排（高精度）                    │
│   将 Query + 候选表 Schema + 历史查询 向量化       │
│   通过 Milvus 余弦相似度排序                      │
│   返回 Top-5 张最相关表 + 字段                     │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│ Stage 3: LLM 关系推理                             │
│   小模型（7B）推理这 5 张表之间的 JOIN 关系        │
│   → 输出: 主表: trade_order_daily                 │
│           JOIN: dim_region ON region_id           │
│           JOIN: dim_platform ON platform_id       │
└─────────────────────────────────────────────────┘
```

### 2.3 时间表达式解析

**双引擎机制**：规则引擎处理常规时间，LLM 兜底模糊时间。

```python
# 规则引擎覆盖（确定性，零延迟）
TIME_PATTERNS = {
    "今天": lambda: (today(), today()),
    "昨天": lambda: (yesterday(), yesterday()),
    "本周": lambda: (this_week_start(), today()),
    "上周": lambda: (last_week_start(), last_week_end()),
    "本月": lambda: (this_month_start(), today()),
    "上月": lambda: (last_month_start(), last_month_end()),
    "近 7 天": lambda: (days_ago(7), yesterday()),
    "近 30 天": lambda: (days_ago(30), yesterday()),
    "Q1": lambda y=this_year(): (f"{y}-01-01", f"{y}-03-31"),
    "Q2": lambda y=this_year(): (f"{y}-04-01", f"{y}-06-30"),
    "Q3": lambda y=this_year(): (f"{y}-07-01", f"{y}-09-30"),
    "Q4": lambda y=this_year(): (f"{y}-10-01", f"{y}-12-31"),
    "上半年": lambda y=this_year(): (f"{y}-01-01", f"{y}-06-30"),
    "下半年": lambda y=this_year(): (f"{y}-07-01", f"{y}-12-31"),
    "年初至今": lambda: (this_year_start(), today()),
}

# LLM 兜底（处理"大促期间""双十一当月"等模糊表达）
def resolve_fuzzy_time(expression: str) -> TimeRange:
    """模糊时间 -> 精确日期范围"""
    # 1. 先尝试规则引擎
    if result := TIME_PATTERNS.get(expression):
        return TimeRange(*result())
    
    # 2. LLM 推理 + 查 dim_time 表验证
    candidate = llm_resolve_time(expression)
    return validate_against_dim_time(candidate)
```
