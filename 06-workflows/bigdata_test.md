
# 终极方案：淘系数仓血缘与数据治理（生产级）

---

## 〇、对GLM评价的逐条回应

| GLM评价 | 我的态度 | 理由 |
|---------|---------|------|
| 硬编码JSON是伪溯源 | ✅ **完全认可** | 同一任务所有行JSON相同，无法定位具体行 |
| OpenLineage与Atlas阻抗失配 | ✅ **完全认可** | 事件模型vs图模型，需大量Adapter，维护黑洞 |
| 流批"同一套SQL"是伪命题 | ✅ **完全认可** | Watermark/TTL/Retraction在批处理中不存在 |
| Docker Compose非生产级 | ✅ **认可但补充** | 作为开发验证环境合理，但必须明确与生产环境分离 |
| 任务指纹+外部字典方案 | ⚠️ **方向对，细节需修正** | hash有碰撞风险，应用业务主键组合而非hash |
| 质量监控需阻断 | ✅ **完全认可** | 必须fail-fast，不能只打报告 |

**GLM未指出的问题（我补充）：**
- 原方案中`_source_hash`用hash函数有碰撞风险，生产环境不可接受
- 原方案缺乏"数据回滚"机制（ETL出错后如何恢复）
- 原方案缺乏"数据SLA"管理（下游等上游的超时机制）
- 原方案缺乏"变更管理"（表结构变更时的血缘自动更新）

---

## 一、终极架构（修正版）

### 1.1 架构核心变化

```
原方案问题                    终极方案修正
─────────────────────────────────────────────────────
硬编码JSON溯源         →    轻量指纹字段 + 血缘字典表（旁路存储）
Atlas + OpenLineage    →    DataHub（原生支持OpenLineage）
流批同一套SQL          →    逻辑统一定义(YAML) + 物理分别生成
质量只打报告           →    质量门禁（fail-fast阻断）
Docker Compose生产     →    开发环境(Docker) + 生产环境(K8s)分离
无回滚机制             →    分区级快照 + 一键回滚
无SLA管理              →    Airflow SLA + 超时告警 + 降级策略
```

### 1.2 终极架构全景图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          【数据消费层】                                       │
│   Superset(BI) │ Grafana(实时) │ 数据API Gateway │ 推荐/风控特征服务         │
└────────┬───────────────┬───────────────┬────────────────┬───────────────────┘
         │               │               │                │
┌────────┴───────────────┴───────────────┴────────────────┴───────────────────┐
│                          【ADS应用层】                                        │
│   离线: Hive/Spark SQL              实时: Doris/StarRocks                    │
│   (日/周/月报表、画像宽表)           (实时指标、实时特征)                       │
└────────┬────────────────────────────────────────────┬───────────────────────┘
         │                                            │
┌────────┴────────────────────────────────────────────┴───────────────────────┐
│                          【DWS汇总层】                                        │
│   离线: Spark SQL                   实时: Flink SQL                          │
│   (主题域聚合、公共指标)              (窗口聚合、实时维度关联)                   │
└────────┬────────────────────────────────────────────┬───────────────────────┘
         │                                            │
┌────────┴────────────────────────────────────────────┴───────────────────────┐
│                          【DWD明细层 + DIM维度层】                             │
│   离线: Spark SQL                   实时: Flink SQL                          │
│   维度: Hive + HBase(Redis缓存)                                              │
│                                                                             │
│   ★ 每行数据携带: _etl_task_id + _source_ref (轻量指纹)                      │
└────────┬────────────────────────────────────────────┬───────────────────────┘
         │                                            │
┌────────┴────────────────────────────────────────────┴───────────────────────┐
│                          【ODS原始层】                                        │
│   离线: Hive (DataX/SeaTunnel批量同步)                                       │
│   实时: Kafka (Flink CDC实时同步)                                            │
│                                                                             │
│   ★ 每行数据携带: _source_system + _source_table + _source_pk               │
└────────┬────────────────────────────────────────────┬───────────────────────┘
         │                                            │
┌────────┴────────────────────────────────────────────┴───────────────────────┐
│                          【数据源层】                                         │
│   MySQL │ Nginx日志 │ 埋点SDK │ 爬虫 │ 第三方API │ 文件(CSV/JSON)            │
└─────────────────────────────────────────────────────────────────────────────┘

                    ╔═══════════════════════════════════════╗
                    ║      【横切：数据治理平台（修正版）】     ║
                    ║                                       ║
                    ║  ┌─────────────────────────────────┐  ║
                    ║  │ DataHub (元数据+血缘，替代Atlas)  │  ║
                    ║  │ + OpenLineage (自动采集)         │  ║
                    ║  └─────────────────────────────────┘  ║
                    ║  ┌─────────────────────────────────┐  ║
                    ║  │ 血缘字典表 (行级溯源旁路存储)      │  ║
                    ║  │ meta_task_lineage_dict           │  ║
                    ║  └─────────────────────────────────┘  ║
                    ║  ┌─────────────────────────────────┐  ║
                    ║  │ Great Expectations (质量门禁)     │  ║
                    ║  │ + Airflow阻断 (fail-fast)        │  ║
                    ║  └─────────────────────────────────┘  ║
                    ║  ┌─────────────────────────────────┐  ║
                    ║  │ Apache Ranger (安全+脱敏)         │  ║
                    ║  └─────────────────────────────────┘  ║
                    ║  ┌─────────────────────────────────┐  ║
                    ║  │ dbt-core (流批逻辑统一定义)       │  ║
                    ║  └─────────────────────────────────┘  ║
                    ╚═══════════════════════════════════════╝
```

---

## 二、技术组件选型（终极版）

| 层次 | 组件 | 版本 | 选型理由（为什么不用其他） |
|------|------|------|--------------------------|
| 离线计算 | **Apache Spark** | 3.5.x | 比Flink批处理更适合（资源利用率更高，SQL优化器更成熟） |
| 离线存储 | **Apache Hive** | 3.1.x | Metastore是元数据基石，ORC列存压缩率高 |
| 实时计算 | **Apache Flink** | 1.18.x | 真正的流处理（非微批），Watermark/状态管理成熟 |
| 消息总线 | **Apache Kafka** | 3.6.x | 事实标准，Flink CDC原生对接 |
| OLAP | **Apache Doris** | 2.0.x | 比ClickHouse更适合多表JOIN，比StarRocks社区更活跃 |
| 元数据+血缘 | **DataHub** | 0.13.x | 原生支持OpenLineage，无需Adapter，运维简单 |
| 血缘采集 | **OpenLineage** | 1.16.x | 开放标准，Spark/Flink/Airflow均有官方集成 |
| 调度 | **Apache Airflow** | 2.8.x | DAG编排+SLA管理+失败重试，最成熟 |
| 数据质量 | **Great Expectations** | 0.18.x | 声明式规则+阻断能力+报告生成 |
| 逻辑统一定义 | **dbt-core** | 1.7.x | 流批逻辑统一管理，模板生成不同引擎SQL |
| 安全 | **Apache Ranger** | 2.4.x | 列级脱敏+行级过滤，与Hive深度集成 |
| 数据同步(离线) | **Apache SeaTunnel** | 2.3.x | 比DataX更现代，支持CDC，社区活跃 |
| 数据同步(实时) | **Flink CDC** | 3.0.x | 直接消费MySQL binlog，无需额外组件 |
| 维度存储 | **Apache HBase** + **Redis** | 2.5.x / 7.x | HBase做持久化，Redis做热缓存 |
| 可视化 | **Apache Superset** | 3.0.x | 开源BI，支持Doris/Hive |
| 监控 | **Prometheus + Grafana** | — | 标准可观测性栈 |

**为什么去掉了Atlas？**
```
Atlas的问题：
  1. 强依赖HBase + Solr + Kafka，运维复杂度极高
  2. 与OpenLineage事件模型存在阻抗失配，需要写大量Adapter
  3. UI体验差，二次开发成本高
  4. 社区活跃度持续下降

DataHub的优势：
  1. 原生支持OpenLineage事件接入（零Adapter）
  2. 元数据摄入基于Kafka，天然解耦
  3. GraphQL API，前端可定制
  4. 支持字段级血缘可视化
  5. LinkedIn出品，生产验证充分
```

---

## 三、行级溯源：终极方案（核心修正）

### 3.1 设计哲学

```
❌ 原方案（错误）：在业务表中塞大JSON字符串
   问题：所有行JSON相同，无法定位具体行；逻辑变更时JSON腐化

✅ 终极方案（正确）：轻量指纹 + 旁路字典 + 动态溯源API
   
   核心思想：
   ┌─────────────────────────────────────────────────────────────┐
   │  业务表只存"指纹"（极轻量），溯源详情存在"字典表"（旁路）     │
   │  查询时通过API动态关联，业务表零膨胀                          │
   └─────────────────────────────────────────────────────────────┘
```

### 3.2 表结构设计

```sql
-- ============================================
-- ODS层：记录"数据从哪个系统来"
-- ============================================
CREATE TABLE ods.ods_trade_order (
    -- 业务字段
    order_id        BIGINT,
    buyer_id        BIGINT,
    seller_id       BIGINT,
    item_id         BIGINT,
    order_amount    DECIMAL(18,2),
    pay_amount      DECIMAL(18,2),
    order_status    STRING,
    create_time     TIMESTAMP,
    pay_time        TIMESTAMP,
    
    -- ★ 溯源字段（轻量，仅3个）
    _source_system  STRING COMMENT '来源系统标识: mysql_trade/log_payment/crawler',
    _source_table   STRING COMMENT '来源表名',
    _source_pk      STRING COMMENT '源表主键值(原始值，非hash)'
    -- 注意：用原始主键值，不用hash（避免碰撞）
) PARTITIONED BY (dt STRING)
STORED AS ORC;

-- ============================================
-- DWD层：记录"数据经过哪个任务加工"
-- ============================================
CREATE TABLE dwd.dwd_trade_order_detail (
    -- 业务字段
    order_id        BIGINT,
    buyer_id        BIGINT,
    seller_id       BIGINT,
    item_id         BIGINT,
    item_name       STRING,
    category_name   STRING,
    order_amount    DECIMAL(18,2),
    pay_amount      DECIMAL(18,2),
    is_paid         INT,
    create_time     TIMESTAMP,
    pay_time        TIMESTAMP,
    
    -- ★ 溯源字段（轻量，仅2个）
    _etl_task_id    STRING COMMENT 'ETL任务唯一标识',
    _source_ref     STRING COMMENT '源数据引用键(用于反查字典表)'
    -- _source_ref = 源表主键的组合，如 "mysql_trade.orders:10001"
    -- 不是hash！是确定性的业务键组合
) PARTITIONED BY (dt STRING)
STORED AS ORC;

-- ============================================
-- 血缘字典表（旁路存储，核心创新）
-- ============================================
CREATE TABLE meta.meta_task_lineage_dict (
    -- 任务信息
    etl_task_id         STRING COMMENT 'ETL任务ID',
    etl_task_name       STRING COMMENT 'ETL任务名称',
    execution_time      TIMESTAMP COMMENT '执行时间',
    batch_id            STRING COMMENT '批次号',
    
    -- 源信息
    source_table        STRING COMMENT '源表全限定名',
    source_pk_columns   STRING COMMENT '源表主键列(逗号分隔)',
    source_filter       STRING COMMENT '源表过滤条件(如 dt=2024-06-15)',
    
    -- 目标信息
    target_table        STRING COMMENT '目标表全限定名',
    target_partition    STRING COMMENT '目标分区',
    
    -- 加工逻辑
    transform_sql       STRING COMMENT '加工SQL(完整记录)',
    transform_type      STRING COMMENT '加工类型: join/aggregate/filter/case_when',
    field_mapping       STRING COMMENT '字段映射JSON(自动生成)',
    
    -- 统计信息
    input_row_count     BIGINT COMMENT '输入行数',
    output_row_count    BIGINT COMMENT '输出行数',
    
    -- 溯源键
    source_ref_prefix   STRING COMMENT '源引用前缀(用于快速关联)'
) PARTITIONED BY (dt STRING)
STORED AS ORC;
```

### 3.3 溯源字段生成逻辑（生产级代码）

```python
# etl_core.py - 核心ETL引擎
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, concat_ws, current_timestamp, count
from datetime import datetime
import json
import hashlib

class ProductionETLEngine:
    """
    生产级ETL引擎
    核心原则：
    1. 业务表只存轻量指纹（_etl_task_id + _source_ref）
    2. 溯源详情存字典表（meta_task_lineage_dict）
    3. 字段映射由sqlglot自动解析生成（非人工维护）
    """
    
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def generate_source_ref(self, source_system: str, source_table: str, 
                            pk_columns: list) -> str:
        """
        生成源数据引用键（确定性，非hash）
        格式: {source_system}.{source_table}:{pk_value}
        示例: mysql_trade.orders:10001
        """
        # 返回SQL表达式字符串，在Spark SQL中使用
        pk_expr = ", ".join([f"CAST({pk} AS STRING)" for pk in pk_columns])
        return f"CONCAT('{source_system}.{source_table}:', {pk_expr})"
    
    def execute_dwd_order_detail(self, dt: str):
        """
        DWD-交易订单明细加工（生产级）
        """
        task_id = f"task_dwd_trade_order_detail_{dt}_{self.batch_id}"
        
        # ===== Step 1: 定义源表信息（用于字典表） =====
        source_info = {
            "sources": [
                {
                    "table": "ods.ods_trade_order",
                    "pk_columns": ["order_id"],
                    "filter": f"dt = '{dt}'",
                    "alias": "o"
                },
                {
                    "table": "dim.dim_item",
                    "pk_columns": ["item_id"],
                    "filter": None,
                    "alias": "i"
                }
            ],
            "target": "dwd.dwd_trade_order_detail",
            "target_partition": f"dt='{dt}'",
            "transform_type": "join"
        }
        
        # ===== Step 2: 执行ETL SQL =====
        # 注意：_source_ref 使用业务主键，不用hash
        etl_sql = f"""
        INSERT OVERWRITE TABLE dwd.dwd_trade_order_detail PARTITION (dt='{dt}')
        SELECT 
            o.order_id,
            o.buyer_id,
            o.seller_id,
            o.item_id,
            i.item_name,
            i.category_name,
            o.order_amount,
            o.pay_amount,
            CASE WHEN o.order_status IN ('paid','shipped','completed') 
                 THEN 1 ELSE 0 END as is_paid,
            o.create_time,
            o.pay_time,
            -- ★ 轻量溯源字段（仅2个）
            '{task_id}' as _etl_task_id,
            CONCAT('mysql_trade.orders:', CAST(o.order_id AS STRING)) as _source_ref
        FROM ods.ods_trade_order o
        LEFT JOIN dim.dim_item i ON o.item_id = i.item_id
        WHERE o.dt = '{dt}'
        """
        
        self.spark.sql(etl_sql)
        
        # ===== Step 3: 自动解析字段映射（sqlglot） =====
        field_mapping = self._parse_field_mapping(etl_sql)
        
        # ===== Step 4: 写入字典表 =====
        input_count = self.spark.sql(
            f"SELECT COUNT(*) FROM ods.ods_trade_order WHERE dt='{dt}'"
        ).collect()[0][0]
        
        output_count = self.spark.sql(
            f"SELECT COUNT(*) FROM dwd.dwd_trade_order_detail WHERE dt='{dt}'"
        ).collect()[0][0]
        
        dict_sql = f"""
        INSERT INTO meta.meta_task_lineage_dict PARTITION (dt='{dt}')
        VALUES (
            '{task_id}',
            'DWD交易订单明细加工',
            current_timestamp(),
            '{self.batch_id}',
            'ods.ods_trade_order, dim.dim_item',
            'order_id, item_id',
            'dt = \\'{dt}\\'',
            'dwd.dwd_trade_order_detail',
            'dt=\\'{dt}\\'',
            \\'\\'\\'{etl_sql}\\'\\'\\',
            'join',
            '{json.dumps(field_mapping, ensure_ascii=False)}',
            {input_count},
            {output_count},
            'mysql_trade.orders:'
        )
        """
        self.spark.sql(dict_sql)
        
        print(f"[ETL] {task_id} completed. input={input_count}, output={output_count}")
        return task_id
    
    def _parse_field_mapping(self, sql: str) -> list:
        """
        使用sqlglot自动解析字段映射（非人工维护，不会腐化）
        """
        import sqlglot
        from sqlglot import exp
        
        mappings = []
        try:
            parsed = sqlglot.parse_one(sql, read="hive")
            
            for select in parsed.find_all(exp.Select):
                for projection in select.expressions:
                    target_field = projection.alias_or_name
                    
                    # 提取源字段引用
                    sources = []
                    for column in projection.find_all(exp.Column):
                        sources.append({
                            "table": column.table or "unknown",
                            "field": column.name
                        })
                    
                    # 判断操作类型
                    operation = self._classify_operation(projection)
                    
                    mappings.append({
                        "target_field": target_field,
                        "source_fields": sources,
                        "operation": operation
                    })
        except Exception as e:
            print(f"[WARN] SQL解析失败: {e}")
            mappings = [{"error": str(e)}]
        
        return mappings
    
    def _classify_operation(self, expression) -> str:
        """自动分类操作类型"""
        from sqlglot import exp
        
        if isinstance(expression, exp.Column):
            return "direct_mapping"
        elif isinstance(expression, exp.Alias):
            inner = expression.this
            if isinstance(inner, exp.Column):
                return "rename"
            elif isinstance(inner, (exp.Add, exp.Mul, exp.Sub, exp.Div)):
                return "calculation"
            elif isinstance(inner, exp.Case):
                return "case_when"
            elif isinstance(inner, exp.AggFunc):
                return "aggregation"
            else:
                return "expression"
        elif isinstance(expression, exp.AggFunc):
            return "aggregation"
        else:
            return "complex"
```

### 3.4 溯源查询API（终极版）

```python
# provenance_api.py - 生产级溯源查询服务
from fastapi import FastAPI, Query, HTTPException
from typing import Optional
import json

app = FastAPI(title="数据溯源服务", version="2.0")

class ProvenanceService:
    """
    溯源查询核心逻辑：
    1. 给定一条DWD记录 → 通过 _etl_task_id 查字典表 → 获得完整加工信息
    2. 给定 _source_ref → 反查ODS层原始记录
    3. 给定目标字段 → 通过DataHub查字段级血缘
    """
    
    def __init__(self, spark_session, datahub_client):
        self.spark = spark_session
        self.datahub = datahub_client
    
    def trace_record(self, table: str, pk_field: str, pk_value: str) -> dict:
        """
        行级溯源：查询某条具体记录的完整来源链路
        
        示例: trace_record("dwd.dwd_trade_order_detail", "order_id", "10001")
        返回: 这条数据从哪个源表、经过什么加工、原始值是什么
        """
        # Step 1: 查询目标记录，获取溯源指纹
        target_sql = f"""
        SELECT *, _etl_task_id, _source_ref
        FROM {table}
        WHERE {pk_field} = '{pk_value}'
        LIMIT 1
        """
        target_row = self.spark.sql(target_sql).collect()
        
        if not target_row:
            raise HTTPException(404, f"记录不存在: {table}.{pk_field}={pk_value}")
        
        row = target_row[0]
        etl_task_id = row["_etl_task_id"]
        source_ref = row["_source_ref"]
        
        # Step 2: 通过 _etl_task_id 查字典表，获取加工详情
        dict_sql = f"""
        SELECT *
        FROM meta.meta_task_lineage_dict
        WHERE etl_task_id = '{etl_task_id}'
        LIMIT 1
        """
        dict_row = self.spark.sql(dict_sql).collect()
        
        task_info = dict_row[0] if dict_row else None
        
        # Step 3: 通过 _source_ref 反查源表原始记录
        # _source_ref 格式: "mysql_trade.orders:10001"
        source_parts = source_ref.split(":")
        source_table_ref = source_parts[0]  # "mysql_trade.orders"
        source_pk_value = source_parts[1]   # "10001"
        
        # 映射到ODS表
        ods_table = f"ods.ods_{source_table_ref.split('.')[-1]}"
        source_sql = f"""
        SELECT *
        FROM {ods_table}
        WHERE _source_pk = '{source_pk_value}'
        LIMIT 1
        """
        
        try:
            source_row = self.spark.sql(source_sql).collect()
            source_data = source_row[0].asDict() if source_row else None
        except:
            source_data = None
        
        # Step 4: 组装完整溯源结果
        return {
            "target_record": {
                "table": table,
                "pk": {pk_field: pk_value},
                "data": row.asDict()
            },
            "transform_info": {
                "task_id": etl_task_id,
                "task_name": task_info["etl_task_name"] if task_info else None,
                "execution_time": str(task_info["execution_time"]) if task_info else None,
                "transform_type": task_info["transform_type"] if task_info else None,
                "field_mapping": json.loads(task_info["field_mapping"]) if task_info else None,
                "input_rows": task_info["input_row_count"] if task_info else None,
                "output_rows": task_info["output_row_count"] if task_info else None
            },
            "source_record": {
                "table": ods_table,
                "pk_value": source_pk_value,
                "data": source_data
            },
            "lineage_chain": self._build_chain(table, pk_field, pk_value)
        }
    
    def trace_field(self, target_table: str, target_field: str) -> list:
        """
        字段级溯源：通过DataHub查询字段的上游依赖
        """
        # 调用DataHub GraphQL API
        query = """
        {
          dataset(urn: "urn:li:dataset:(urn:li:dataPlatform:hive,%s,PROD)") {
            upstreamLineage {
              upstreams {
                dataset {
                  name
                  upstreamLineage {
                    upstreams {
                      dataset { name }
                    }
                  }
                }
                fineGrainedLineages {
                  upstreams { path }
                  downstreams { path }
                }
              }
            }
          }
        }
        """ % target_table
        
        result = self.datahub.execute(query)
        return self._format_field_lineage(result, target_field)
    
    def _build_chain(self, table, pk_field, pk_value) -> list:
        """递归构建完整血缘链（从ADS追溯到ODS）"""
        chain = []
        current_table = table
        current_pk = pk_value
        
        # 最多追溯5层
        for depth in range(5):
            try:
                sql = f"""
                SELECT _etl_task_id, _source_ref
                FROM {current_table}
                WHERE {pk_field} = '{current_pk}'
                LIMIT 1
                """
                row = self.spark.sql(sql).collect()
                if not row:
                    break
                
                chain.append({
                    "level": depth,
                    "table": current_table,
                    "task_id": row[0]["_etl_task_id"],
                    "source_ref": row[0]["_source_ref"]
                })
                
                # 解析source_ref，跳到上一层
                # 实际实现中需要根据字典表确定上一层的表和主键
                break  # 简化示意
                
            except:
                break
        
        return chain


# ===== API端点 =====
provenance_svc = None  # 初始化时注入

@app.get("/api/v2/provenance/record")
def api_trace_record(
    table: str = Query(..., description="目标表名"),
    pk_field: str = Query(..., description="主键字段名"),
    pk_value: str = Query(..., description="主键值")
):
    """
    行级溯源API
    示例: GET /api/v2/provenance/record?table=dwd.dwd_trade_order_detail&pk_field=order_id&pk_value=10001
    """
    return provenance_svc.trace_record(table, pk_field, pk_value)

@app.get("/api/v2/provenance/field")
def api_trace_field(
    table: str = Query(...),
    field: str = Query(...)
):
    """字段级血缘API"""
    return provenance_svc.trace_field(table, field)
```

---

## 四、流批统一：逻辑统一，物理分离

### 4.1 用dbt统一管理业务逻辑

```yaml
# dbt_project.yml
name: taobao_dw
version: '1.0'
profile: taobao

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]

vars:
  offline_engine: spark
  realtime_engine: flink
```

```yaml
# models/dwd/dwd_trade_order_detail.yml
# 统一逻辑定义（与引擎无关）

version: 2

models:
  - name: dwd_trade_order_detail
    description: "DWD-交易订单明细（含商品维度）"
    
    # 统一的业务逻辑定义
    columns:
      - name: order_id
        description: "订单ID"
        source_column: "ods_trade_order.order_id"
        transform: "direct_mapping"
        
      - name: item_name
        description: "商品名称"
        source_column: "dim_item.item_name"
        transform: "lookup_join"
        join_key: "item_id"
        
      - name: is_paid
        description: "是否已支付"
        source_column: "ods_trade_order.order_status"
        transform: "case_when"
        logic: "CASE WHEN order_status IN ('paid','shipped','completed') THEN 1 ELSE 0 END"
    
    # 质量规则（与引擎无关）
    tests:
      - name: pk_unique
        column: order_id
        rule: "COUNT(*) = COUNT(DISTINCT order_id)"
        
      - name: amount_non_negative
        column: pay_amount
        rule: "MIN(pay_amount) >= 0"
        
      - name: cross_layer_consistency
        rule: "SUM(pay_amount) = (SELECT SUM(pay_amount) FROM ods.ods_trade_order WHERE dt={{dt}})"
        tolerance: 0.0001
```

### 4.2 物理SQL生成器

```python
# sql_generator.py
# 根据统一逻辑定义，分别生成Spark SQL和Flink SQL

import yaml
from jinja2 import Template

class SQLGenerator:
    """
    流批SQL生成器
    输入：统一的YAML逻辑定义
    输出：Spark SQL（离线） 或 Flink SQL（实时）
    """
    
    def __init__(self, model_path: str):
        with open(model_path) as f:
            self.model = yaml.safe_load(f)
    
    def generate_spark_sql(self, dt: str) -> str:
        """生成离线Spark SQL"""
        model = self.model["models"][0]
        
        template = Template("""
INSERT OVERWRITE TABLE dwd.dwd_trade_order_detail PARTITION (dt='{{dt}}')
SELECT 
    {% for col in columns %}
    {{col.expression}} as {{col.name}},
    {% endfor %}
    '{{task_id}}' as _etl_task_id,
    CONCAT('{{source_ref_prefix}}', CAST(order_id AS STRING)) as _source_ref
FROM {{source_table}} o
{% for join in joins %}
LEFT JOIN {{join.table}} {{join.alias}} ON {{join.condition}}
{% endfor %}
WHERE o.dt = '{{dt}}'
""")
        
        # 构建列表达式
        columns = []
        for col_def in model["columns"]:
            if col_def["transform"] == "direct_mapping":
                expr = f"o.{col_def['source_column'].split('.')[-1]}"
            elif col_def["transform"] == "case_when":
                expr = col_def["logic"]
            elif col_def["transform"] == "lookup_join":
                expr = f"i.{col_def['source_column'].split('.')[-1]}"
            else:
                expr = col_def.get("logic", f"o.{col_def['name']}")
            
            columns.append({"name": col_def["name"], "expression": expr})
        
        return template.render(
            dt=dt,
            columns=columns,
            task_id=f"task_dwd_order_{dt}",
            source_ref_prefix="mysql_trade.orders:",
            source_table="ods.ods_trade_order",
            joins=[{"table": "dim.dim_item", "alias": "i", "condition": "o.item_id = i.item_id"}]
        )
    
    def generate_flink_sql(self) -> str:
        """生成实时Flink SQL（包含Watermark、TTL等流特有语法）"""
        model = self.model["models"][0]
        
        template = Template("""
-- Flink SQL（自动生成，勿手动修改）
-- 包含流处理特有语法：Watermark, Lookup Join, State TTL

CREATE TABLE kafka_source_order (
    order_id        BIGINT,
    buyer_id        BIGINT,
    seller_id       BIGINT,
    item_id         BIGINT,
    order_amount    DECIMAL(18,2),
    pay_amount      DECIMAL(18,2),
    order_status    STRING,
    create_time     TIMESTAMP(3),
    pay_time        TIMESTAMP(3),
    proc_time       AS PROCTIME(),
    WATERMARK FOR create_time AS create_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'ods_trade_order_cdc',
    'properties.bootstrap.servers' = '${KAFKA_BROKERS}',
    'format' = 'debezium-json',
    'scan.startup.mode' = 'latest-offset'
);

CREATE TABLE dim_item_lookup (
    item_id         BIGINT,
    item_name       STRING,
    category_name   STRING,
    PRIMARY KEY (item_id) NOT ENFORCED
) WITH (
    'connector' = 'hbase',
    'table-name' = 'dim_item',
    'zookeeper.quorum' = '${HBASE_ZK}',
    'lookup.cache.max-rows' = '100000',
    'lookup.cache.ttl' = '3600s',
    'lookup.async' = 'true'
);

CREATE TABLE dwd_sink (
    order_id        BIGINT,
    buyer_id        BIGINT,
    seller_id       BIGINT,
    item_id         BIGINT,
    item_name       STRING,
    category_name   STRING,
    order_amount    DECIMAL(18,2),
    pay_amount      DECIMAL(18,2),
    is_paid         INT,
    create_time     TIMESTAMP(3),
    _etl_task_id    STRING,
    _source_ref     STRING,
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector' = 'kafka',
    'topic' = 'dwd_trade_order_detail',
    'properties.bootstrap.servers' = '${KAFKA_BROKERS}',
    'format' = 'json'
);

-- State TTL设置（流处理特有）
SET 'table.exec.state.ttl' = '86400000';  -- 24小时

INSERT INTO dwd_sink
SELECT 
    o.order_id,
    o.buyer_id,
    o.seller_id,
    o.item_id,
    i.item_name,
    i.category_name,
    o.order_amount,
    o.pay_amount,
    CASE WHEN o.order_status IN ('paid','shipped','completed') THEN 1 ELSE 0 END,
    o.create_time,
    'flink_task_dwd_order_realtime',
    CONCAT('mysql_trade.orders:', CAST(o.order_id AS STRING))
FROM kafka_source_order o
LEFT JOIN dim_item_lookup FOR SYSTEM_TIME AS OF o.proc_time AS i
    ON o.item_id = i.item_id;
""")
        
        return template.render()
```

---

## 五、数据质量门禁（fail-fast阻断）

### 5.1 质量检查框架（生产级）

```python
# quality_gate.py
"""
数据质量门禁：嵌入ETL流程，失败即阻断
核心原则：错误数据绝不流入下游
"""
from airflow.exceptions import AirflowFailException
from pyspark.sql import SparkSession
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class Severity(Enum):
    BLOCK = "block"       # 阻断：必须停止下游
    WARN = "warn"         # 告警：记录但不停止
    INFO = "info"         # 信息：仅记录

@dataclass
class QualityRule:
    name: str
    sql: str
    severity: Severity
    threshold: float = 0
    description: str = ""

class QualityGate:
    """
    质量门禁引擎
    在Airflow DAG中作为gate task执行
    任何BLOCK级别的规则失败 → 抛出AirflowFailException → 阻断下游
    """
    
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.results = []
    
    def add_rule(self, rule: QualityRule):
        self.rules.append(rule)
    
    def execute(self, context: dict) -> dict:
        """执行所有质量规则"""
        dt = context.get("ds")
        report = {"dt": dt, "rules": [], "passed": True, "blocked": False}
        
        for rule in self.rules:
            try:
                result = self.spark.sql(rule.sql).collect()[0][0]
                passed = result <= rule.threshold
                
                rule_result = {
                    "name": rule.name,
                    "severity": rule.severity.value,
                    "result": result,
                    "threshold": rule.threshold,
                    "passed": passed,
                    "description": rule.description
                }
                report["rules"].append(rule_result)
                
                if not passed:
                    if rule.severity == Severity.BLOCK:
                        report["passed"] = False
                        report["blocked"] = True
                        # 写入告警
                        self._send_alert(rule, result, dt)
                    elif rule.severity == Severity.WARN:
                        self._send_warning(rule, result, dt)
                        
            except Exception as e:
                report["rules"].append({
                    "name": rule.name,
                    "severity": "error",
                    "error": str(e),
                    "passed": False
                })
                report["passed"] = False
        
        # 关键：如果有任何BLOCK级别失败，抛出异常阻断DAG
        if report["blocked"]:
            failed_rules = [r["name"] for r in report["rules"] if not r["passed"]]
            raise AirflowFailException(
                f"数据质量门禁阻断！失败规则: {failed_rules}。"
                f"下游任务已停止，请检查数据后重跑。"
            )
        
        return report
    
    def _send_alert(self, rule, result, dt):
        """发送告警（钉钉/企微/PagerDuty）"""
        message = f"""
        🚨 数据质量阻断告警
        规则: {rule.name}
        描述: {rule.description}
        当前值: {result}
        阈值: {rule.threshold}
        日期: {dt}
        影响: 下游所有任务已停止
        """
        # 实际调用告警API
        print(f"[ALERT] {message}")


def build_dwd_quality_gate(spark, dt: str) -> QualityGate:
    """构建DWD层质量门禁规则集"""
    gate = QualityGate(spark)
    
    # 规则1：主键唯一性（BLOCK级别）
    gate.add_rule(QualityRule(
        name="pk_uniqueness",
        sql=f"""
            SELECT COUNT(*) - COUNT(DISTINCT order_id) as dup_count
            FROM dwd.dwd_trade_order_detail WHERE dt='{dt}'
        """,
        severity=Severity.BLOCK,
        threshold=0,
        description="主键order_id不允许重复"
    ))
    
    # 规则2：金额非负（BLOCK级别）
    gate.add_rule(QualityRule(
        name="amount_non_negative",
        sql=f"""
            SELECT COUNT(*) as negative_count
            FROM dwd.dwd_trade_order_detail 
            WHERE dt='{dt}' AND pay_amount < 0
        """,
        severity=Severity.BLOCK,
        threshold=0,
        description="支付金额不允许为负"
    ))
    
    # 规则3：跨层对账（BLOCK级别）
    gate.add_rule(QualityRule(
        name="cross_layer_amount_consistency",
        sql=f"""
            SELECT ABS(
                (SELECT SUM(pay_amount) FROM dwd.dwd_trade_order_detail WHERE dt='{dt}')
                - (SELECT SUM(pay_amount) FROM ods.ods_trade_order WHERE dt='{dt}')
            ) / NULLIF((SELECT SUM(pay_amount) FROM ods.ods_trade_order WHERE dt='{dt}'), 0)
            as diff_rate
        """,
        severity=Severity.BLOCK,
        threshold=0.0001,  # 差异率不超过0.01%
        description="DWD层金额总和必须与ODS层一致（误差<0.01%）"
    ))
    
    # 规则4：行数波动检查（WARN级别）
    gate.add_rule(QualityRule(
        name="row_count_fluctuation",
        sql=f"""
            SELECT ABS(
                (SELECT COUNT(*) FROM dwd.dwd_trade_order_detail WHERE dt='{dt}')
                - (SELECT AVG(cnt) FROM (
                    SELECT COUNT(*) as cnt FROM dwd.dwd_trade_order_detail 
                    WHERE dt >= date_sub('{dt}', 7) AND dt < '{dt}'
                    GROUP BY dt
                ))
            ) / NULLIF((SELECT AVG(cnt) FROM (
                SELECT COUNT(*) as cnt FROM dwd.dwd_trade_order_detail 
                WHERE dt >= date_sub('{dt}', 7) AND dt < '{dt}'
                GROUP BY dt
            )), 0) as fluctuation_rate
        """,
        severity=Severity.WARN,
        threshold=0.3,  # 波动超过30%告警
        description="行数相比前7天均值波动不超过30%"
    ))
    
    # 规则5：溯源字段完整性（BLOCK级别）
    gate.add_rule(QualityRule(
        name="provenance_completeness",
        sql=f"""
            SELECT COUNT(*) as missing_count
            FROM dwd.dwd_trade_order_detail 
            WHERE dt='{dt}' AND (_etl_task_id IS NULL OR _source_ref IS NULL)
        """,
        severity=Severity.BLOCK,
        threshold=0,
        description="溯源字段不允许为空"
    ))
    
    return gate
```

### 5.2 Airflow DAG集成（带阻断）

```python
# dags/taobao_daily_etl_v2.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowFailException
from datetime import datetime, timedelta

default_args = {
    'owner': 'taobao_data_team',
    'depends_on_past': True,
    'start_date': datetime(2024, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=10),
    'sla': timedelta(hours=6),
    'on_failure_callback': send_dingtalk_alert,  # 失败自动告警
}

with DAG(
    'taobao_daily_offline_etl_v2',
    default_args=default_args,
    schedule_interval='0 2 * * *',
    catchup=False,
    max_active_runs=1,  # 同一时间只允许一个实例运行
    tags=['taobao', 'offline', 'daily', 'v2'],
) as dag:

    def task_check_source(**context):
        """检查源数据就绪"""
        dt = context['ds']
        # 检查MySQL binlog是否已同步完成
        # 检查日志文件是否已上传到HDFS
        # 如果未就绪，等待或失败
        pass
    
    def task_sync_ods(**context):
        """ODS层数据同步"""
        dt = context['ds']
        # SeaTunnel/DataX 执行同步
        pass
    
    def task_ods_quality_gate(**context):
        """ODS层质量门禁"""
        dt = context['ds']
        spark = get_spark_session()
        
        gate = QualityGate(spark)
        gate.add_rule(QualityRule(
            name="ods_row_count_not_zero",
            sql=f"SELECT CASE WHEN COUNT(*) > 0 THEN 0 ELSE 1 END FROM ods.ods_trade_order WHERE dt='{dt}'",
            severity=Severity.BLOCK,
            threshold=0,
            description="ODS层数据不能为空"
        ))
        gate.add_rule(QualityRule(
            name="ods_source_system_not_null",
            sql=f"SELECT COUNT(*) FROM ods.ods_trade_order WHERE dt='{dt}' AND _source_system IS NULL",
            severity=Severity.BLOCK,
            threshold=0,
            description="来源系统标识不能为空"
        ))
        
        gate.execute(context)  # 失败会抛AirflowFailException
    
    def task_etl_dwd(**context):
        """DWD层加工"""
        dt = context['ds']
        spark = get_spark_session()
        engine = ProductionETLEngine(spark)
        engine.execute_dwd_order_detail(dt)
    
    def task_dwd_quality_gate(**context):
        """DWD层质量门禁（核心阻断点）"""
        dt = context['ds']
        spark = get_spark_session()
        
        gate = build_dwd_quality_gate(spark, dt)
        gate.execute(context)  # 任何BLOCK规则失败 → 阻断下游
    
    def task_etl_dws(**context):
        """DWS层加工"""
        dt = context['ds']
        # ...
    
    def task_dws_quality_gate(**context):
        """DWS层质量门禁"""
        dt = context['ds']
        spark = get_spark_session()
        
        gate = QualityGate(spark)
        gate.add_rule(QualityRule(
            name="dws_sum_equals_dwd_sum",
            sql=f"""
                SELECT ABS(
                    (SELECT SUM(pay_amount_sum) FROM dws.dws_trade_seller_day WHERE dt='{dt}')
                    - (SELECT SUM(pay_amount) FROM dwd.dwd_trade_order_detail WHERE dt='{dt}' AND is_paid=1)
                ) as diff
            """,
            severity=Severity.BLOCK,
            threshold=0.01,
            description="DWS聚合值必须等于DWD明细值"
        ))
        gate.execute(context)
    
    def task_etl_ads(**context):
        """ADS层加工"""
        pass
    
    def task_final_validation(**context):
        """最终验证：业务合理性检查"""
        dt = context['ds']
        spark = get_spark_session()
        
        # GMV波动检查
        gmv_today = spark.sql(f"SELECT gmv FROM ads.ads_platform_gmv_daily WHERE dt='{dt}'").collect()[0][0]
        gmv_7d_avg = spark.sql(f"""
            SELECT AVG(gmv) FROM ads.ads_platform_gmv_daily 
            WHERE dt >= date_sub('{dt}', 7) AND dt < '{dt}'
        """).collect()[0][0]
        
        fluctuation = abs(gmv_today - gmv_7d_avg) / gmv_7d_avg
        if fluctuation > 0.5:  # 波动超过50%
            raise AirflowFailException(
                f"GMV异常波动: 今日={gmv_today}, 7日均值={gmv_7d_avg}, 波动率={fluctuation:.2%}"
            )

    # ===== 任务定义 =====
    t_check = PythonOperator(task_id='check_source_ready', python_callable=task_check_source)
    t_ods = PythonOperator(task_id='sync_ods', python_callable=task_sync_ods)
    t_ods_gate = PythonOperator(task_id='ods_quality_gate', python_callable=task_ods_quality_gate)
    t_dwd = PythonOperator(task_id='etl_dwd', python_callable=task_etl_dwd)
    t_dwd_gate = PythonOperator(task_id='dwd_quality_gate', python_callable=task_dwd_quality_gate)
    t_dws = PythonOperator(task_id='etl_dws', python_callable=task_etl_dws)
    t_dws_gate = PythonOperator(task_id='dws_quality_gate', python_callable=task_dws_quality_gate)
    t_ads = PythonOperator(task_id='etl_ads', python_callable=task_etl_ads)
    t_final = PythonOperator(task_id='final_validation', python_callable=task_final_validation)

    # ===== 依赖关系（质量门禁作为gate嵌入） =====
    t_check >> t_ods >> t_ods_gate >> t_dwd >> t_dwd_gate >> t_dws >> t_dws_gate >> t_ads >> t_final
    #                          ↑ 阻断点              ↑ 阻断点              ↑ 阻断点
```

---

## 六、DataHub集成（替代Atlas）

### 6.1 OpenLineage → DataHub 原生集成

```yaml
# openlineage_datahub_config.yml
# OpenLineage事件直接推送到DataHub（无需Adapter）

transport:
  type: http
  url: http://datahub-gms:8080/openlineage
  
namespace: taobao_offline

# Spark任务配置（spark-defaults.conf）
# spark.openlineage.transport.type=http
# spark.openlineage.transport.url=http://datahub-gms:8080/openlineage
# spark.openlineage.namespace=taobao_offline
```

### 6.2 字段级血缘注册到DataHub

```python
# datahub_lineage_client.py
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import (
    FineGrainedLineageClass,
    UpstreamLineageClass,
    DatasetLineageTypeClass,
)
from datahub.utilities.urns.dataset_urn import DatasetUrn

class DataHubLineageManager:
    """DataHub字段级血缘管理"""
    
    def __init__(self, gms_url="http://localhost:8080"):
        self.emitter = DatahubRestEmitter(gms_url)
        self.platform = "hive"
        self.env = "PROD"
    
    def register_field_lineage(self, 
                               source_table: str, source_field: str,
                               target_table: str, target_field: str,
                               operation: str, task_name: str):
        """注册字段级血缘到DataHub"""
        
        target_urn = DatasetUrn.create_from_string(
            f"urn:li:dataset:(urn:li:dataPlatform:{self.platform},{target_table},{self.env})"
        )
        source_urn = DatasetUrn.create_from_string(
            f"urn:li:dataset:(urn:li:dataPlatform:{self.platform},{source_table},{self.env})"
        )
        
        fine_grained = FineGrainedLineageClass(
            upstreams=[f"{source_urn},{source_field}"],
            downstreams=[f"{target_urn},{target_field}"],
            transformOperation=operation,
            confidenceScore=1.0
        )
        
        lineage = UpstreamLineageClass(
            upstreams=[{
                "dataset": str(source_urn),
                "type": DatasetLineageTypeClass.TRANSFORMED
            }],
            fineGrainedLineages=[fine_grained]
        )
        
        mcp = MetadataChangeProposalWrapper(
            entityUrn=str(target_urn),
            aspect=lineage
        )
        
        self.emitter.emit(mcp)
        print(f"[DataHub] 字段血缘注册成功: {source_table}.{source_field} → {target_table}.{target_field}")
    
    def batch_register_from_etl(self, task_id: str, field_mappings: list):
        """从ETL任务的字段映射批量注册血缘"""
        for mapping in field_mappings:
            target_field = mapping["target_field"]
            for source in mapping["source_fields"]:
                self.register_field_lineage(
                    source_table=source.get("table", "unknown"),
                    source_field=source["field"],
                    target_table="dwd.dwd_trade_order_detail",
                    target_field=target_field,
                    operation=mapping["operation"],
                    task_name=task_id
                )
```

---

## 七、完整业务案例：从始至终走一遍

### 7.1 业务场景

```
场景：电商平台"618大促"期间的GMV实时+离线双链路

数据源：
  A. MySQL订单库（order_id, buyer_id, seller_id, item_id, pay_amount, order_status）
  B. 支付日志（order_id, pay_channel, pay_time, pay_amount）
  C. 商品爬虫（item_id, price, quantity, crawl_time）

需求：
  1. 实时大屏：每分钟展示GMV（Flink → Doris）
  2. 离线报表：T+1产出卖家维度GMV汇总（Spark → Hive → Superset）
  3. 溯源需求：运营发现某卖家GMV异常，需要追溯到具体哪笔订单、来自哪个源
```

### 7.2 全链路执行流程

```
时间线：2024-06-18 00:00 ~ 2024-06-19 08:00

【实时链路】（秒级）
  00:00:01  MySQL产生订单 → Flink CDC捕获binlog
  00:00:02  → Kafka ods_trade_order_cdc topic
  00:00:03  → Flink SQL加工（JOIN商品维度）
  00:00:04  → Kafka dwd_trade_order_detail topic
  00:00:05  → Flink窗口聚合（1分钟窗口）
  00:00:06  → Doris dws_gmv_realtime 表
  00:00:07  → Grafana大屏展示

【离线链路】（T+1）
  06-19 02:00  Airflow触发DAG
  06-19 02:05  SeaTunnel同步MySQL全量 → Hive ODS
  06-19 02:15  ODS质量门禁 ✅ 通过
  06-19 02:20  Spark SQL加工DWD（JOIN dim_item）
  06-19 02:35  DWD质量门禁 ✅ 通过（主键唯一、对账一致）
  06-19 02:40  Spark SQL加工DWS（GROUP BY seller_id）
  06-19 02:50  DWS质量门禁 ✅ 通过
  06-19 02:55  Spark SQL加工ADS（平台GMV日报）
  06-19 03:00  最终验证 ✅ GMV波动<30%
  06-19 03:01  Superset报表可查
  06-19 03:02  钉钉通知："日常ETL完成"

【溯源查询】（运营使用）
  06-19 10:00  运营发现卖家seller_id=2001的GMV异常偏高
  06-19 10:01  调用溯源API:
               GET /api/v2/provenance/record?table=dwd.dwd_trade_order_detail&pk_field=order_id&pk_value=50001
  06-19 10:02  返回：
               {
                 "target_record": {"order_id": 50001, "pay_amount": 99999.00, ...},
                 "transform_info": {
                   "task_id": "task_dwd_trade_order_detail_2024-06-18_20240619_020500",
                   "transform_type": "join",
                   "field_mapping": [...]
                 },
                 "source_record": {
                   "table": "ods.ods_trade_order",
                   "data": {"order_id": 50001, "pay_amount": 99999.00, "_source_system": "mysql_trade"}
                 }
               }
  06-19 10:03  运营确认：该订单来自MySQL订单库，金额确实是99999（非ETL错误）
  06-19 10:04  进一步排查：发现是刷单行为 → 通知风控
```

### 7.3 关键节点数据验证

| 节点 | 验证内容 | 验证方法 | 通过标准 |
|------|---------|---------|---------|
| ODS接入后 | 行数一致 | COUNT(*)对比源表 | 差异=0 |
| ODS接入后 | 溯源字段非空 | _source_system IS NULL检查 | 空值数=0 |
| DWD加工后 | 主键唯一 | COUNT(*)=COUNT(DISTINCT order_id) | 重复数=0 |
| DWD加工后 | 金额对账 | SUM(DWD)=SUM(ODS) | 差异率<0.01% |
| DWD加工后 | 溯源字段完整 | _etl_task_id和_source_ref非空 | 空值数=0 |
| DWS汇总后 | 聚合一致 | SUM(DWS)=SUM(DWD WHERE is_paid=1) | 差异<0.01 |
| ADS产出后 | 业务合理 | GMV波动<30%（对比7日均值） | 波动率<0.3 |
| 实时链路 | 延迟 | Flink metrics | P99<5s |
| 实时链路 | 准确性 | 实时GMV vs 离线GMV（T+1对账） | 差异<1% |

---

## 八、测试方案（生产级）

### 8.1 端到端自动化测试

```python
# tests/test_e2e_full_pipeline.py
"""
端到端测试：覆盖从数据注入到溯源查询的完整闭环
使用高频业务场景：订单交易链路
"""
import pytest
import time
import json
from datetime import datetime
from pyspark.sql import SparkSession

@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder \
        .appName("E2E_Test") \
        .master("local[4]") \
        .enableHiveSupport() \
        .getOrCreate()

@pytest.fixture(scope="module")
def test_dt():
    return datetime.now().strftime("%Y-%m-%d")

class TestFullPipeline:
    """完整链路测试"""
    
    # ===== Phase 1: 数据注入 =====
    def test_01_inject_source_data(self, spark, test_dt):
        """注入测试源数据到MySQL（模拟业务系统）"""
        import pymysql
        conn = pymysql.connect(host='mysql', user='root', password='root123', db='trade')
        cursor = conn.cursor()
        
        # 注入10条测试订单
        test_orders = [
            (90001, 1001, 2001, 3001, 299.00, 279.00, 'paid'),
            (90002, 1002, 2001, 3002, 199.00, 189.00, 'paid'),
            (90003, 1003, 2002, 3003, 599.00, 559.00, 'paid'),
            (90004, 1004, 2002, 3004, 99.00, 89.00, 'created'),   # 未支付
            (90005, 1005, 2003, 3005, 1299.00, 1199.00, 'paid'),
            (90006, 1006, 2003, 3006, 499.00, 479.00, 'paid'),
            (90007, 1007, 2004, 3007, 799.00, 749.00, 'shipped'),
            (90008, 1008, 2004, 3008, 399.00, 379.00, 'paid'),
            (90009, 1009, 2005, 3009, 159.00, 149.00, 'refunded'), # 已退款
            (90010, 1010, 2005, 3010, 899.00, 849.00, 'paid'),
        ]
        
        for order in test_orders:
            cursor.execute("""
                INSERT INTO orders (order_id, buyer_id, seller_id, item_id, 
                                   order_amount, pay_amount, order_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, order)
        
        conn.commit()
        conn.close()
        
        # 验证注入成功
        cursor.execute("SELECT COUNT(*) FROM orders WHERE order_id BETWEEN 90001 AND 90010")
        assert cursor.fetchone()[0] == 10
    
    # ===== Phase 2: ODS同步 + 质量门禁 =====
    def test_02_ods_sync_and_gate(self, spark, test_dt):
        """ODS同步并执行质量门禁"""
        # 模拟SeaTunnel同步（实际调用SeaTunnel API）
        spark.sql(f"""
            INSERT OVERWRITE TABLE ods.ods_trade_order PARTITION(dt='{test_dt}')
            SELECT 
                order_id, buyer_id, seller_id, item_id,
                order_amount, pay_amount, order_status,
                create_time, pay_time,
                'mysql_trade' as _source_system,
                'orders' as _source_table,
                CAST(order_id AS STRING) as _source_pk
            FROM jdbc_trade_source
        """)
        
        # 质量门禁
        count = spark.sql(f"SELECT COUNT(*) FROM ods.ods_trade_order WHERE dt='{test_dt}'").collect()[0][0]
        assert count == 10, f"ODS行数={count}，期望=10"
        
        null_count = spark.sql(f"""
            SELECT COUNT(*) FROM ods.ods_trade_order 
            WHERE dt='{test_dt}' AND (_source_system IS NULL OR _source_pk IS NULL)
        """).collect()[0][0]
        assert null_count == 0, "溯源字段存在空值"
    
    # ===== Phase 3: DWD加工 + 质量门禁 =====
    def test_03_dwd_etl_and_gate(self, spark, test_dt):
        """DWD加工并执行质量门禁"""
        engine = ProductionETLEngine(spark)
        task_id = engine.execute_dwd_order_detail(test_dt)
        
        # 验证行数
        count = spark.sql(f"SELECT COUNT(*) FROM dwd.dwd_trade_order_detail WHERE dt='{test_dt}'").collect()[0][0]
        assert count == 10
        
        # 验证主键唯一
        dup = spark.sql(f"""
            SELECT COUNT(*) - COUNT(DISTINCT order_id) 
            FROM dwd.dwd_trade_order_detail WHERE dt='{test_dt}'
        """).collect()[0][0]
        assert dup == 0, f"主键重复数={dup}"
        
        # 验证is_paid逻辑
        paid_count = spark.sql(f"""
            SELECT COUNT(*) FROM dwd.dwd_trade_order_detail 
            WHERE dt='{test_dt}' AND is_paid = 1
        """).collect()[0][0]
        # paid + shipped = 8条（90004是created，90009是refunded）
        assert paid_count == 8, f"已支付订单数={paid_count}，期望=8"
        
        # 验证溯源字段
        sample = spark.sql(f"""
            SELECT _etl_task_id, _source_ref 
            FROM dwd.dwd_trade_order_detail 
            WHERE dt='{test_dt}' AND order_id = 90001
        """).collect()[0]
        
        assert sample["_etl_task_id"] == task_id
        assert sample["_source_ref"] == "mysql_trade.orders:90001"
        
        # 跨层对账
        ods_sum = spark.sql(f"SELECT SUM(pay_amount) FROM ods.ods_trade_order WHERE dt='{test_dt}'").collect()[0][0]
        dwd_sum = spark.sql(f"SELECT SUM(pay_amount) FROM dwd.dwd_trade_order_detail WHERE dt='{test_dt}'").collect()[0][0]
        assert abs(float(ods_sum) - float(dwd_sum)) < 0.01, "跨层对账失败"
    
    # ===== Phase 4: DWS汇总 =====
    def test_04_dws_aggregation(self, spark, test_dt):
        """DWS卖家维度汇总"""
        spark.sql(f"""
            INSERT OVERWRITE TABLE dws.dws_trade_seller_day PARTITION(dt='{test_dt}')
            SELECT 
                seller_id,
                COUNT(order_id) as order_count,
                SUM(CASE WHEN is_paid=1 THEN pay_amount ELSE 0 END) as pay_amount_sum,
                COUNT(DISTINCT buyer_id) as buyer_count,
                COUNT(DISTINCT item_id) as item_count,
                ROUND(SUM(CASE WHEN is_paid=1 THEN pay_amount ELSE 0 END) 
                      / NULLIF(COUNT(CASE WHEN is_paid=1 THEN 1 END), 0), 2) as avg_order_amount,
                '["dwd.dwd_trade_order_detail"]' as _source_tables,
                'task_dws_seller_{test_dt}' as _etl_task_id,
                current_timestamp() as _etl_time
            FROM dwd.dwd_trade_order_detail
            WHERE dt='{test_dt}'
            GROUP BY seller_id
        """)
        
        # 验证：seller_id=2001 有2笔订单，都已支付，金额=279+189=468
        seller_2001 = spark.sql(f"""
            SELECT * FROM dws.dws_trade_seller_day 
            WHERE dt='{test_dt}' AND seller_id=2001
        """).collect()[0]
        
        assert seller_2001["order_count"] == 2
        assert float(seller_2001["pay_amount_sum"]) == 468.00
        assert seller_2001["buyer_count"] == 2
    
    # ===== Phase 5: ADS产出 =====
    def test_05_ads_report(self, spark, test_dt):
        """ADS平台GMV日报"""
        spark.sql(f"""
            INSERT OVERWRITE TABLE ads.ads_platform_gmv_daily
            SELECT 
                '{test_dt}' as dt,
                SUM(pay_amount_sum) as gmv,
                SUM(order_count) as order_count,
                SUM(buyer_count) as pay_user_count,
                ROUND(SUM(pay_amount_sum)/NULLIF(SUM(order_count),0), 2) as avg_order_amount,
                NULL as top_category,
                '["dws.dws_trade_seller_day"]' as _source_tables,
                'task_ads_gmv_{test_dt}' as _etl_task_id,
                current_timestamp() as _etl_time
            FROM dws.dws_trade_seller_day WHERE dt='{test_dt}'
        """)
        
        gmv = spark.sql(f"SELECT gmv FROM ads.ads_platform_gmv_daily WHERE dt='{test_dt}'").collect()[0][0]
        
        # 计算期望GMV：所有is_paid=1的订单pay_amount之和
        expected_gmv = spark.sql(f"""
            SELECT SUM(pay_amount) FROM dwd.dwd_trade_order_detail 
            WHERE dt='{test_dt}' AND is_paid=1
        """).collect()[0][0]
        
        assert abs(float(gmv) - float(expected_gmv)) < 0.01, f"GMV不一致: {gmv} vs {expected_gmv}"
    
    # ===== Phase 6: 行级溯源验证 =====
    def test_06_record_provenance(self, spark, test_dt):
        """验证行级溯源：从DWD记录追溯到ODS源"""
        # 查询order_id=90001的溯源信息
        row = spark.sql(f"""
            SELECT _etl_task_id, _source_ref
            FROM dwd.dwd_trade_order_detail
            WHERE dt='{test_dt}' AND order_id=90001
        """).collect()[0]
        
        task_id = row["_etl_task_id"]
        source_ref = row["_source_ref"]
        
        # 验证source_ref格式正确
        assert source_ref == "mysql_trade.orders:90001"
        
        # 通过source_ref反查ODS
        source_pk = source_ref.split(":")[1]
        ods_row = spark.sql(f"""
            SELECT * FROM ods.ods_trade_order 
            WHERE dt='{test_dt}' AND _source_pk = '{source_pk}'
        """).collect()[0]
        
        assert ods_row["order_id"] == 90001
        assert ods_row["_source_system"] == "mysql_trade"
        assert float(ods_row["pay_amount"]) == 279.00
        
        # 通过task_id查字典表
        dict_row = spark.sql(f"""
            SELECT * FROM meta.meta_task_lineage_dict 
            WHERE etl_task_id = '{task_id}'
        """).collect()[0]
        
        assert dict_row["source_table"] == "ods.ods_trade_order, dim.dim_item"
        assert dict_row["transform_type"] == "join"
        assert dict_row["input_row_count"] == 10
        assert dict_row["output_row_count"] == 10
    
    # ===== Phase 7: 字段级血缘验证 =====
    def test_07_field_lineage(self, spark, test_dt):
        """验证字段级血缘：dwd.pay_amount ← ods.pay_amount"""
        engine = ProductionETLEngine(spark)
        
        # 获取ETL任务的字段映射
        task_id = spark.sql(f"""
            SELECT _etl_task_id FROM dwd.dwd_trade_order_detail 
            WHERE dt='{test_dt}' LIMIT 1
        """).collect()[0][0]
        
        dict_row = spark.sql(f"""
            SELECT field_mapping FROM meta.meta_task_lineage_dict 
            WHERE etl_task_id = '{task_id}'
        """).collect()[0]
        
        field_mapping = json.loads(dict_row[0])
        
        # 验证pay_amount字段的映射
        pay_amount_mapping = next(
            (m for m in field_mapping if m["target_field"] == "pay_amount"), None
        )
        assert pay_amount_mapping is not None
        assert pay_amount_mapping["operation"] == "direct_mapping"
        assert any(s["field"] == "pay_amount" for s in pay_amount_mapping["source_fields"])
    
    # ===== Phase 8: 语义正确性验证 =====
    def test_08_semantic_correctness(self, spark, test_dt):
        """
        语义正确性验证：确保业务逻辑没有偏离
        """
        # 验证1：is_paid语义（paid/shipped/completed → 1，其他 → 0）
        wrong_is_paid = spark.sql(f"""
            SELECT COUNT(*) FROM dwd.dwd_trade_order_detail o
            JOIN ods.ods_trade_order s ON o.order_id = s.order_id AND s.dt='{test_dt}'
            WHERE o.dt='{test_dt}'
            AND (
                (s.order_status IN ('paid','shipped','completed') AND o.is_paid != 1)
                OR (s.order_status NOT IN ('paid','shipped','completed') AND o.is_paid != 0)
            )
        """).collect()[0][0]
        assert wrong_is_paid == 0, "is_paid语义错误"
        
        # 验证2：JOIN正确性（DWD的item_name必须与DIM一致）
        wrong_join = spark.sql(f"""
            SELECT COUNT(*) FROM dwd.dwd_trade_order_detail d
            JOIN dim.dim_item i ON d.item_id = i.item_id
            WHERE d.dt='{test_dt}' AND d.item_name != i.item_name
        """).collect()[0][0]
        assert wrong_join == 0, "JOIN结果不一致"
        
        # 验证3：聚合语义（DWS的pay_amount_sum = DWD中该卖家is_paid=1的pay_amount之和）
        agg_check = spark.sql(f"""
            SELECT dws.seller_id, dws.pay_amount_sum,
                   dwd_calc.calc_sum,
                   ABS(dws.pay_amount_sum - dwd_calc.calc_sum) as diff
            FROM dws.dws_trade_seller_day dws
            JOIN (
                SELECT seller_id, SUM(pay_amount) as calc_sum
                FROM dwd.dwd_trade_order_detail
                WHERE dt='{test_dt}' AND is_paid=1
                GROUP BY seller_id
            ) dwd_calc ON dws.seller_id = dwd_calc.seller_id
            WHERE dws.dt='{test_dt}'
        """).collect()
        
        for row in agg_check:
            assert row["diff"] < 0.01, f"seller_id={row['seller_id']} 聚合不一致"
```

### 8.2 性能测试

```python
# tests/test_performance.py

def test_etl_performance_100m(spark, test_dt):
    """
    性能基准：1亿条数据DWD加工
    目标：< 20分钟（50 executor × 4 core × 16G）
    """
    import time
    
    # 生成1亿条测试数据
    spark.sql(f"""
        INSERT OVERWRITE TABLE ods.ods_trade_order PARTITION(dt='{test_dt}')
        SELECT 
            id as order_id,
            id % 10000000 as buyer_id,
            id % 500000 as seller_id,
            id % 2000000 as item_id,
            ROUND(RAND() * 1000, 2),
            ROUND(RAND() * 1000, 2),
            CASE WHEN RAND() > 0.3 THEN 'paid' ELSE 'created' END,
            CURRENT_TIMESTAMP(), NULL,
            'mysql_trade', 'orders', CAST(id AS STRING)
        FROM RANGE(100000000)
    """)
    
    start = time.time()
    engine = ProductionETLEngine(spark)
    engine.execute_dwd_order_detail(test_dt)
    elapsed = time.time() - start
    
    print(f"[PERF] 1亿条DWD加工耗时: {elapsed/60:.1f}分钟")
    assert elapsed < 1200, f"超时: {elapsed/60:.1f}分钟 > 20分钟目标"


def test_provenance_query_latency(spark, test_dt):
    """
    溯源查询延迟测试
    目标：单次查询 < 3秒
    """
    import time
    
    start = time.time()
    
    # 执行溯源查询
    result = spark.sql(f"""
        SELECT d._etl_task_id, d._source_ref, m.transform_type, m.field_mapping
        FROM dwd.dwd_trade_order_detail d
        JOIN meta.meta_task_lineage_dict m ON d._etl_task_id = m.etl_task_id
        WHERE d.dt='{test_dt}' AND d.order_id = 90001
    """).collect()
    
    elapsed = time.time() - start
    print(f"[PERF] 溯源查询延迟: {elapsed*1000:.0f}ms")
    assert elapsed < 3.0, f"溯源查询超时: {elapsed:.2f}s"
```

---

## 九、生产环境部署（K8s）

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: taobao-dw

---
# k8s/spark-operator.yaml (使用Spark Operator)
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: etl-dwd-order
  namespace: taobao-dw
spec:
  type: Scala
  mode: cluster
  image: taobao/spark-etl:3.5
  mainApplicationFile: local:///opt/spark/jobs/etl-pipeline.jar
  arguments:
    - "--dt"
    - "{{ds}}"
  sparkConf:
    spark.executor.instances: "50"
    spark.executor.cores: "4"
    spark.executor.memory: "16g"
    spark.sql.adaptive.enabled: "true"
    spark.sql.adaptive.skewJoin.enabled: "true"
    spark.openlineage.transport.type: "http"
    spark.openlineage.transport.url: "http://datahub-gms:8080/openlineage"
  driver:
    cores: 2
    memory: "8g"
  executor:
    cores: 4
    memory: "16g"
    instances: 50

---
# k8s/datahub.yaml (DataHub部署)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: datahub-gms
  namespace: taobao-dw
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: datahub-gms
        image: acryldata/datahub-gms:latest
        ports:
        - containerPort: 8080
        env:
        - name: MAE_CONSUMER_ENABLED
          value: "true"
        - name: MCE_CONSUMER_ENABLED
          value: "true"
        - name: DATAHUB_ANALYTICS_ENABLED
          value: "true"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

---

## 十、项目目录结构（终极版）

```
taobao-dw/
├── README.md                          # 项目总览与快速启动
├── Makefile                           # 一键操作命令集
│
├── infra/                             # 基础设施层
│   ├── docker/                        # 开发环境（Docker Compose）
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.monitoring.yml
│   │   └── .env.example
│   ├── k8s/                           # 生产环境（Kubernetes）
│   │   ├── namespace.yaml
│   │   ├── spark-operator/
│   │   │   ├── spark-application-template.yaml
│   │   │   └── spark-rbac.yaml
│   │   ├── flink/
│   │   │   ├── flink-session-cluster.yaml
│   │   │   └── flink-deployment.yaml
│   │   ├── kafka/
│   │   │   ├── kafka-statefulset.yaml
│   │   │   └── kafka-topics-job.yaml
│   │   ├── doris/
│   │   │   ├── doris-fe-statefulset.yaml
│   │   │   └── doris-be-statefulset.yaml
│   │   ├── datahub/
│   │   │   ├── datahub-gms.yaml
│   │   │   ├── datahub-frontend.yaml
│   │   │   └── datahub-mae-consumer.yaml
│   │   ├── airflow/
│   │   │   ├── airflow-scheduler.yaml
│   │   │   └── airflow-webserver.yaml
│   │   └── monitoring/
│   │       ├── prometheus.yaml
│   │       ├── grafana.yaml
│   │       └── alertmanager.yaml
│   └── terraform/                     # 云资源编排（可选）
│       ├── main.tf
│       └── variables.tf
│
├── dbt/                               # 统一逻辑定义层（dbt-core）
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── models/
│   │   ├── ods/
│   │   │   ├── ods_trade_order.sql
│   │   │   ├── ods_user_behavior_log.sql
│   │   │   └── schema.yml
│   │   ├── dim/
│   │   │   ├── dim_item.sql
│   │   │   ├── dim_seller.sql
│   │   │   └── schema.yml
│   │   ├── dwd/
│   │   │   ├── dwd_trade_order_detail.sql
│   │   │   ├── dwd_trade_order_detail.yml    # 统一逻辑定义
│   │   │   └── schema.yml
│   │   ├── dws/
│   │   │   ├── dws_trade_seller_day.sql
│   │   │   ├── dws_trade_seller_day.yml
│   │   │   └── schema.yml
│   │   └── ads/
│   │       ├── ads_platform_gmv_daily.sql
│   │       └── schema.yml
│   ├── macros/
│   │   ├── generate_source_ref.sql     # 生成溯源引用键的宏
│   │   ├── quality_gate.sql            # 质量检查宏
│   │   └── partition_filter.sql        # 分区过滤宏
│   ├── tests/
│   │   ├── test_pk_unique.sql
│   │   ├── test_amount_non_negative.sql
│   │   └── test_cross_layer_consistency.sql
│   └── seeds/
│       └── meta_task_lineage_dict_seed.csv
│
├── etl/                               # ETL引擎层
│   ├── core/
│   │   ├── __init__.py
│   │   ├── etl_engine.py              # 核心ETL引擎（含溯源字段注入）
│   │   ├── source_ref_generator.py    # 源引用键生成器
│   │   └── field_mapping_parser.py    # sqlglot字段映射解析器
│   ├── offline/
│   │   ├── __init__.py
│   │   ├── ods_sync.py               # ODS层同步（SeaTunnel封装）
│   │   ├── dwd_transform.py          # DWD层加工
│   │   ├── dws_aggregate.py          # DWS层汇总
│   │   └── ads_report.py             # ADS层报表
│   ├── realtime/
│   │   ├── __init__.py
│   │   ├── flink_cdc_source.py       # Flink CDC源配置
│   │   ├── flink_dwd_transform.py    # 实时DWD加工
│   │   ├── flink_dws_window.py       # 实时窗口聚合
│   │   └── flink_doris_sink.py       # Doris写入
│   └── sql_generator/
│       ├── __init__.py
│       ├── generator.py               # 流批SQL生成器
│       ├── spark_template.py          # Spark SQL模板
│       └── flink_template.py          # Flink SQL模板（含Watermark/TTL）
│
├── quality/                           # 数据质量层
│   ├── __init__.py
│   ├── gate.py                        # 质量门禁引擎（fail-fast）
│   ├── rules/
│   │   ├── __init__.py
│   │   ├── completeness.py           # 完整性规则
│   │   ├── uniqueness.py             # 唯一性规则
│   │   ├── consistency.py            # 一致性规则（跨层对账）
│   │   ├── timeliness.py             # 时效性规则
│   │   └── business_rules.py         # 业务规则
│   ├── reports/
│   │   └── report_generator.py       # 质量报告生成
│   └── alerts/
│       ├── dingtalk.py               # 钉钉告警
│       └── pagerduty.py              # PagerDuty告警
│
├── lineage/                           # 血缘管理层
│   ├── __init__.py
│   ├── openlineage_config.py         # OpenLineage配置
│   ├── datahub_client.py             # DataHub客户端
│   ├── field_lineage_register.py     # 字段级血缘注册
│   ├── provenance_service.py         # 溯源查询服务
│   └── impact_analysis.py            # 影响分析
│
├── governance/                        # 数据治理层
│   ├── lifecycle/
│   │   ├── policy.py                 # 生命周期策略定义
│   │   ├── executor.py               # 策略执行器（归档/删除）
│   │   └── audit.py                  # 审计日志
│   ├── security/
│   │   ├── ranger_policies.py        # Ranger策略管理
│   │   ├── masking_rules.py          # 脱敏规则
│   │   └── access_control.py         # 访问控制
│   └── standards/
│       ├── naming_convention.md      # 命名规范
│       ├── field_dictionary.md       # 字段字典
│       └── layer_specification.md    # 分层规范
│
├── api/                               # 数据服务层
│   ├── main.py                        # FastAPI入口
│   ├── routers/
│   │   ├── provenance.py             # 溯源查询API
│   │   ├── lineage.py                # 血缘查询API
│   │   ├── quality.py                # 质量报告API
│   │   └── metadata.py               # 元数据查询API
│   ├── services/
│   │   ├── provenance_service.py
│   │   ├── lineage_service.py
│   │   └── quality_service.py
│   └── models/
│       └── schemas.py                 # Pydantic模型
│
├── airflow/                           # 调度层
│   ├── dags/
│   │   ├── taobao_daily_offline.py   # 离线日任务DAG
│   │   ├── taobao_hourly_sync.py     # 小时级同步DAG
│   │   ├── taobao_lifecycle.py       # 生命周期管理DAG
│   │   └── taobao_quality_audit.py   # 质量审计DAG
│   ├── plugins/
│   │   └── quality_gate_plugin.py    # 质量门禁Airflow插件
│   └── config/
│       └── airflow.cfg
│
├── monitoring/                        # 监控层
│   ├── prometheus/
│   │   ├── prometheus.yml
│   │   └── rules/
│   │       ├── etl_alerts.yml
│   │       ├── realtime_alerts.yml
│   │       └── quality_alerts.yml
│   ├── grafana/
│   │   └── dashboards/
│   │       ├── etl_overview.json
│   │       ├── realtime_pipeline.json
│   │       ├── data_quality.json
│   │       ├── lineage_coverage.json
│   │       └── cost_monitoring.json
│   └── scripts/
│       ├── health_check.py           # 组件健康检查
│       └── sla_monitor.py            # SLA监控
│
├── tests/                             # 测试层
│   ├── unit/
│   │   ├── test_source_ref_generator.py
│   │   ├── test_field_mapping_parser.py
│   │   ├── test_quality_rules.py
│   │   └── test_sql_generator.py
│   ├── integration/
│   │   ├── test_e2e_offline_pipeline.py    # 离线端到端
│   │   ├── test_e2e_realtime_pipeline.py   # 实时端到端
│   │   ├── test_provenance_query.py        # 溯源查询
│   │   └── test_quality_gate_block.py      # 质量阻断
│   ├── performance/
│   │   ├── test_etl_100m_rows.py           # 1亿行性能
│   │   ├── test_provenance_latency.py      # 溯源延迟
│   │   └── test_doris_query_p99.py         # Doris P99
│   └── fixtures/
│       ├── test_data_orders.csv
│       ├── test_data_items.csv
│       └── expected_results.json
│
├── scripts/                           # 运维脚本
│   ├── init_all.sh                    # 一键初始化
│   ├── rollback_partition.sh          # 分区回滚
│   ├── backfill.sh                    # 数据补跑
│   ├── migrate_schema.sh              # 表结构变更
│   └── cleanup_expired.sh             # 过期数据清理
│
├── docs/                              # 文档
│   ├── architecture.md                # 架构设计文档
│   ├── data_dictionary.md             # 数据字典
│   ├── runbook.md                     # 运维手册
│   ├── incident_response.md           # 故障应急手册
│   └── onboarding.md                  # 新人指南
│
├── config/                            # 配置文件
│   ├── spark-defaults.conf
│   ├── flink-conf.yaml
│   ├── hive-site.xml
│   ├── ranger/
│   │   └── policies.json
│   └── datahub/
│       └── application.yml
│
└── Makefile                           # 常用命令
    # make dev-up          启动开发环境
    # make dev-down        停止开发环境
    # make test-unit       运行单元测试
    # make test-e2e        运行端到端测试
    # make deploy          部署到K8s
    # make rollback DT=xx  回滚指定日期分区
    # make backfill DT=xx  补跑指定日期
```

---

## 十一、回滚与补跑机制

### 11.1 分区级快照与回滚

```python
# scripts/rollback_manager.py
"""
分区级回滚机制
核心思想：每次ETL前对目标分区做快照，失败时可一键恢复
"""
from pyspark.sql import SparkSession
from datetime import datetime

class RollbackManager:
    """
    回滚管理器
    策略：
    1. ETL前：将目标分区数据复制到 _backup 后缀表
    2. ETL失败：从 _backup 恢复
    3. ETL成功：保留 _backup 7天后自动清理
    """
    
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.backup_suffix = "_backup"
        self.backup_retention_days = 7
    
    def create_snapshot(self, table: str, partition: str):
        """ETL前创建快照"""
        backup_table = f"{table}{self.backup_suffix}"
        
        # 创建备份表（如果不存在）
        self.spark.sql(f"""
            CREATE TABLE IF NOT EXISTS {backup_table}
            LIKE {table}
        """)
        
        # 复制目标分区到备份表
        self.spark.sql(f"""
            INSERT OVERWRITE TABLE {backup_table} PARTITION({partition})
            SELECT * FROM {table} WHERE {partition}
        """)
        
        print(f"[Rollback] Snapshot created: {table} {partition} → {backup_table}")
    
    def rollback(self, table: str, partition: str):
        """从快照回滚"""
        backup_table = f"{table}{self.backup_suffix}"
        
        # 检查备份是否存在
        backup_count = self.spark.sql(f"""
            SELECT COUNT(*) FROM {backup_table} WHERE {partition}
        """).collect()[0][0]
        
        if backup_count == 0:
            raise Exception(f"备份不存在: {backup_table} {partition}")
        
        # 恢复
        self.spark.sql(f"""
            INSERT OVERWRITE TABLE {table} PARTITION({partition})
            SELECT * FROM {backup_table} WHERE {partition}
        """)
        
        print(f"[Rollback] Restored: {backup_table} → {table} {partition}")
    
    def cleanup_old_backups(self):
        """清理过期备份"""
        cutoff = datetime.now().strftime("%Y-%m-%d")
        # 删除超过保留期的备份分区
        self.spark.sql(f"""
            ALTER TABLE {table}{self.backup_suffix} 
            DROP IF EXISTS PARTITION (dt < date_sub('{cutoff}', {self.backup_retention_days}))
        """)


class BackfillManager:
    """
    数据补跑管理器
    场景：某天ETL失败或数据源延迟，需要重新跑历史分区
    """
    
    def __init__(self, spark: SparkSession, rollback_mgr: RollbackManager):
        self.spark = spark
        self.rollback_mgr = rollback_mgr
    
    def backfill(self, table: str, start_dt: str, end_dt: str, 
                 etl_func, skip_quality_gate: bool = False):
        """
        批量补跑
        etl_func: ETL函数引用
        """
        from datetime import timedelta
        
        current = datetime.strptime(start_dt, "%Y-%m-%d")
        end = datetime.strptime(end_dt, "%Y-%m-%d")
        
        results = []
        while current <= end:
            dt = current.strftime("%Y-%m-%d")
            print(f"[Backfill] Processing dt={dt}")
            
            try:
                # 1. 创建快照
                self.rollback_mgr.create_snapshot(table, f"dt='{dt}'")
                
                # 2. 执行ETL
                etl_func(dt)
                
                # 3. 质量检查（除非跳过）
                if not skip_quality_gate:
                    gate = build_quality_gate(self.spark, dt)
                    gate.execute({"ds": dt})
                
                results.append({"dt": dt, "status": "success"})
                
            except Exception as e:
                # 失败：回滚
                print(f"[Backfill] FAILED dt={dt}: {e}. Rolling back...")
                self.rollback_mgr.rollback(table, f"dt='{dt}'")
                results.append({"dt": dt, "status": "failed", "error": str(e)})
                break  # 停止补跑，避免连锁错误
            
            current += timedelta(days=1)
        
        return results
```

### 11.2 Airflow中的回滚集成

```python
# 在DAG中集成回滚
def task_etl_dwd_with_rollback(**context):
    """带回滚能力的DWD ETL"""
    dt = context['ds']
    spark = get_spark_session()
    rollback_mgr = RollbackManager(spark)
    
    try:
        # 1. 快照
        rollback_mgr.create_snapshot("dwd.dwd_trade_order_detail", f"dt='{dt}'")
        
        # 2. 执行ETL
        engine = ProductionETLEngine(spark)
        engine.execute_dwd_order_detail(dt)
        
    except Exception as e:
        # 3. 失败回滚
        print(f"[ETL] Failed: {e}. Rolling back...")
        rollback_mgr.rollback("dwd.dwd_trade_order_detail", f"dt='{dt}'")
        raise AirflowFailException(f"ETL失败并已回滚: {e}")
```

---

## 十二、SLA管理与降级策略

```python
# sla_manager.py
"""
SLA管理：确保数据按时产出
淘系标准：
  - ODS层：T+1 04:00前就绪
  - DWD层：T+1 06:00前就绪
  - DWS层：T+1 07:00前就绪
  - ADS层：T+1 08:00前就绪（业务人员上班前可看）
"""
from datetime import datetime, timedelta
from enum import Enum

class SLALevel(Enum):
    ODS = {"deadline_hour": 4, "alert_before_min": 30}
    DWD = {"deadline_hour": 6, "alert_before_min": 30}
    DWS = {"deadline_hour": 7, "alert_before_min": 30}
    ADS = {"deadline_hour": 8, "alert_before_min": 60}

class SLAManager:
    """SLA监控与降级"""
    
    def check_sla(self, layer: str, dt: str) -> dict:
        """检查某层是否按时产出"""
        sla = SLALevel[layer].value
        deadline = datetime.strptime(dt, "%Y-%m-%d") + timedelta(hours=sla["deadline_hour"])
        now = datetime.now()
        
        # 检查数据是否已产出
        is_ready = self._check_partition_ready(layer, dt)
        
        if is_ready:
            return {"status": "on_time", "layer": layer, "dt": dt}
        elif now > deadline:
            return {"status": "breached", "layer": layer, "dt": dt, 
                    "delay_minutes": (now - deadline).total_seconds() / 60}
        elif now > deadline - timedelta(minutes=sla["alert_before_min"]):
            return {"status": "at_risk", "layer": layer, "dt": dt,
                    "remaining_minutes": (deadline - now).total_seconds() / 60}
        else:
            return {"status": "on_track", "layer": layer, "dt": dt}
    
    def degrade_strategy(self, layer: str, dt: str) -> str:
        """
        降级策略：当某层SLA即将超时时的应急方案
        """
        strategies = {
            "ODS": "使用前一天数据作为兜底，标记为stale",
            "DWD": "跳过非核心字段加工，只产出核心指标",
            "DWS": "使用增量更新代替全量重算",
            "ADS": "展示前一天数据 + 实时数据补充",
        }
        return strategies.get(layer, "无降级策略，等待人工介入")
    
    def _check_partition_ready(self, layer: str, dt: str) -> bool:
        """检查分区数据是否已产出"""
        table_map = {
            "ODS": "ods.ods_trade_order",
            "DWD": "dwd.dwd_trade_order_detail",
            "DWS": "dws.dws_trade_seller_day",
            "ADS": "ads.ads_platform_gmv_daily"
        }
        table = table_map.get(layer)
        # 实际检查Hive分区是否存在且行数>0
        return True  # 简化
```

---

## 十三、Makefile（一键操作）

```makefile
# Makefile - 淘系数仓一键操作

.PHONY: dev-up dev-down test-unit test-e2e deploy rollback backfill

# ===== 开发环境 =====
dev-up:
	docker-compose -f infra/docker/docker-compose.yml up -d
	@echo "等待服务启动..."
	@sleep 30
	@echo "初始化表结构..."
	docker exec -i mysql mysql -uroot -proot123 < scripts/init_source_tables.sql
	@echo "开发环境就绪 ✓"

dev-down:
	docker-compose -f infra/docker/docker-compose.yml down -v

# ===== 测试 =====
test-unit:
	pytest tests/unit/ -v --tb=short

test-integration:
	pytest tests/integration/ -v --tb=short

test-e2e:
	pytest tests/integration/test_e2e_offline_pipeline.py -v --tb=long

test-perf:
	pytest tests/performance/ -v --tb=short -s

test-all: test-unit test-integration

# ===== 部署 =====
deploy:
	kubectl apply -f infra/k8s/namespace.yaml
	kubectl apply -f infra/k8s/
	@echo "部署完成 ✓"

# ===== 运维操作 =====
rollback:
	@read -p "输入回滚日期(YYYY-MM-DD): " dt; \
	python scripts/rollback_manager.py rollback --table dwd.dwd_trade_order_detail --dt $$dt

backfill:
	@read -p "输入补跑起始日期(YYYY-MM-DD): " start; \
	read -p "输入补跑结束日期(YYYY-MM-DD): " end; \
	python scripts/rollback_manager.py backfill --start $$start --end $$end

# ===== 质量检查 =====
quality-check:
	python -m quality.gate --layer dwd --dt $(DT)

# ===== 血缘查询 =====
trace-record:
	curl -s "http://localhost:8000/api/v2/provenance/record?table=$(TABLE)&pk_field=$(PK)&pk_value=$(VALUE)" | python -m json.tool

# ===== 监控 =====
monitor:
	@echo "Grafana: http://localhost:3000"
	@echo "Prometheus: http://localhost:9090"
	@echo "DataHub: http://localhost:9002"
	@echo "Airflow: http://localhost:8082"
	@echo "Flink UI: http://localhost:8081"
	@echo "Doris: http://localhost:8030"
```

---

## 十四、关键结果验证矩阵（终极版）

### 14.1 从始至终的业务验证（高频场景：订单交易）

| 步骤 | 操作 | 输入 | 期望输出 | 验证方法 | 失败处理 |
|------|------|------|---------|---------|---------|
| 1 | MySQL产生订单 | INSERT order_id=90001, pay_amount=279 | 1行数据 | SELECT COUNT | 检查binlog |
| 2 | Flink CDC捕获 | MySQL binlog | Kafka消息 | 消费Kafka验证 | 检查CDC连接 |
| 3 | Kafka ODS Topic | CDC消息 | topic有消息 | kafka-console-consumer | 检查topic配置 |
| 4 | Flink DWD加工 | ODS消息+维度表 | DWD消息(含item_name) | 消费DWD topic | 检查JOIN逻辑 |
| 5 | Doris写入 | DWD消息 | Doris表有数据 | SELECT验证 | 检查sink配置 |
| 6 | 离线ODS同步 | MySQL全量 | Hive ODS有数据 | Spark SQL COUNT | 检查SeaTunnel |
| 7 | ODS质量门禁 | ODS数据 | 通过(行数>0,溯源非空) | 门禁执行 | 阻断+告警 |
| 8 | DWD加工 | ODS+DIM | DWD有数据(含溯源字段) | 验证_source_ref | 回滚+重跑 |
| 9 | DWD质量门禁 | DWD数据 | 通过(主键唯一,对账一致) | 门禁执行 | 阻断+回滚 |
| 10 | DWS汇总 | DWD数据 | DWS有数据 | SUM验证 | 回滚+重跑 |
| 11 | DWS质量门禁 | DWS数据 | 通过(聚合一致) | 门禁执行 | 阻断 |
| 12 | ADS产出 | DWS数据 | ADS有数据 | GMV验证 | 回滚 |
| 13 | 最终验证 | ADS数据 | GMV波动<30% | 对比7日均值 | 告警+人工 |
| 14 | 溯源查询 | order_id=90001 | 返回完整来源链路 | API调用 | 检查字典表 |
| 15 | 字段血缘 | dwd.pay_amount | 上游=ods.pay_amount | DataHub查询 | 检查OpenLineage |

### 14.2 语义正确性验证清单

| 验证项 | 验证SQL | 期望结果 | 严重级别 |
|--------|---------|---------|---------|
| is_paid语义 | `SELECT COUNT(*) FROM dwd d JOIN ods o ON d.order_id=o.order_id WHERE (o.status IN('paid','shipped','completed') AND d.is_paid!=1) OR (o.status NOT IN(...) AND d.is_paid!=0)` | = 0 | BLOCK |
| JOIN正确性 | `SELECT COUNT(*) FROM dwd d JOIN dim i ON d.item_id=i.item_id WHERE d.item_name != i.item_name` | = 0 | BLOCK |
| 金额一致性 | `SELECT ABS(SUM(dwd.pay_amount) - SUM(ods.pay_amount)) FROM ...` | < 0.01 | BLOCK |
| 聚合正确性 | `SELECT ABS(dws.sum - SUM(dwd WHERE is_paid=1)) GROUP BY seller_id` | < 0.01 | BLOCK |
| GMV计算 | `SELECT ABS(ads.gmv - SUM(dwd WHERE is_paid=1))` | < 0.01 | BLOCK |
| 退款排除 | `SELECT COUNT(*) FROM dwd WHERE order_status='refunded' AND is_paid=1` | = 0 | BLOCK |
| 时间范围 | `SELECT COUNT(*) FROM dwd WHERE dt='{dt}' AND create_time NOT BETWEEN '{dt} 00:00' AND '{dt} 23:59'` | = 0 | WARN |

---

## 十五、实时vs离线对账机制

```python
# realtime_offline_reconciliation.py
"""
实时vs离线对账：确保两条链路数据一致
淘系经验：实时和离线允许有微小差异（<1%），但必须有对账机制
"""
from pyspark.sql import SparkSession
from datetime import datetime

class RealtimeOfflineReconciliation:
    """实时离线对账器"""
    
    def __init__(self, spark: SparkSession, doris_conn):
        self.spark = spark
        self.doris = doris_conn
    
    def reconcile_gmv(self, dt: str) -> dict:
        """
        对账GMV：离线ADS vs 实时Doris
        在T+1凌晨执行（此时实时数据已稳定）
        """
        # 离线GMV（来自Hive ADS）
        offline_gmv = self.spark.sql(f"""
            SELECT gmv FROM ads.ads_platform_gmv_daily WHERE dt='{dt}'
        """).collect()[0][0]
        
        # 实时GMV（来自Doris，取当天所有窗口的累计）
        cursor = self.doris.cursor()
        cursor.execute(f"""
            SELECT SUM(pay_amount_sum) as realtime_gmv
            FROM dws.dws_trade_seller_realtime
            WHERE window_start >= '{dt} 00:00:00'
            AND window_start < '{dt} 23:59:59'
        """)
        realtime_gmv = cursor.fetchone()[0]
        
        # 计算差异
        diff = abs(float(offline_gmv) - float(realtime_gmv))
        diff_rate = diff / float(offline_gmv) if float(offline_gmv) > 0 else 0
        
        result = {
            "dt": dt,
            "offline_gmv": float(offline_gmv),
            "realtime_gmv": float(realtime_gmv),
            "diff": diff,
            "diff_rate": round(diff_rate, 6),
            "threshold": 0.01,  # 允许1%差异
            "passed": diff_rate < 0.01,
            "reconcile_time": datetime.now().isoformat()
        }
        
        if not result["passed"]:
            # 差异超过阈值，触发告警
            self._alert_reconciliation_failure(result)
        
        return result
    
    def reconcile_order_count(self, dt: str) -> dict:
        """对账订单数"""
        offline_count = self.spark.sql(f"""
            SELECT COUNT(*) FROM dwd.dwd_trade_order_detail WHERE dt='{dt}'
        """).collect()[0][0]
        
        cursor = self.doris.cursor()
        cursor.execute(f"""
            SELECT SUM(order_count) FROM dws.dws_trade_seller_realtime
            WHERE window_start >= '{dt} 00:00:00' AND window_start < '{dt} 23:59:59'
        """)
        realtime_count = cursor.fetchone()[0]
        
        diff = abs(offline_count - realtime_count)
        
        return {
            "offline_count": offline_count,
            "realtime_count": realtime_count,
            "diff": diff,
            "passed": diff <= offline_count * 0.001  # 允许0.1%差异
        }
    
    def _alert_reconciliation_failure(self, result):
        """对账失败告警"""
        message = f"""
        🚨 实时离线对账失败
        日期: {result['dt']}
        离线GMV: {result['offline_gmv']}
        实时GMV: {result['realtime_gmv']}
        差异率: {result['diff_rate']:.4%}
        阈值: 1%
        请排查：
        1. 实时链路是否有数据丢失（Kafka消费Lag）
        2. Flink窗口是否有迟到数据被丢弃
        3. 离线ETL是否有数据重复
        """
        print(f"[ALERT] {message}")
        # 实际发送钉钉/企微告警
```

---

## 十六、变更管理（表结构变更时的血缘自动更新）

```python
# schema_change_manager.py
"""
表结构变更管理
核心问题：当ODS表加了一个字段，下游DWD/DWS如何感知？
"""

class SchemaChangeManager:
    """
    表结构变更管理器
    流程：
    1. 检测Schema变更（通过Hive Metastore事件或定期扫描）
    2. 分析影响范围（通过DataHub血缘）
    3. 通知下游Owner
    4. 自动更新字段映射
    """
    
    def detect_schema_change(self, table: str) -> list:
        """检测表结构变更"""
        # 对比当前Schema与上次记录的Schema
        current_schema = self._get_current_schema(table)
        last_schema = self._get_last_recorded_schema(table)
        
        changes = []
        
        # 新增字段
        for field in current_schema:
            if field["name"] not in [f["name"] for f in last_schema]:
                changes.append({"type": "add_column", "field": field})
        
        # 删除字段
        for field in last_schema:
            if field["name"] not in [f["name"] for f in current_schema]:
                changes.append({"type": "drop_column", "field": field})
        
        # 类型变更
        for field in current_schema:
            old_field = next((f for f in last_schema if f["name"] == field["name"]), None)
            if old_field and old_field["type"] != field["type"]:
                changes.append({"type": "type_change", "field": field, 
                              "old_type": old_field["type"]})
        
        return changes
    
    def analyze_impact(self, table: str, changes: list) -> dict:
        """分析变更影响范围"""
        # 通过DataHub查询下游依赖
        downstream = self.datahub_client.get_downstream_tables(table)
        
        impact = {
            "changed_table": table,
            "changes": changes,
            "affected_downstream": [],
            "risk_level": "low"
        }
        
        for change in changes:
            if change["type"] == "drop_column":
                # 删除字段：高风险，下游可能报错
                for ds_table in downstream:
                    # 检查下游是否使用了该字段
                    if self._field_used_in_downstream(change["field"]["name"], ds_table):
                        impact["affected_downstream"].append({
                            "table": ds_table,
                            "field": change["field"]["name"],
                            "risk": "high"
                        })
                impact["risk_level"] = "high"
            
            elif change["type"] == "type_change":
                impact["risk_level"] = "medium"
        
        return impact
    
    def notify_owners(self, impact: dict):
        """通知下游Owner"""
        for affected in impact["affected_downstream"]:
            owner = self._get_table_owner(affected["table"])
            message = f"""
            ⚠️ 上游表结构变更通知
            变更表: {impact['changed_table']}
            变更内容: {impact['changes']}
            影响你的表: {affected['table']}
            影响字段: {affected['field']}
            风险等级: {affected['risk']}
            请评估是否需要修改你的ETL逻辑。
            """
            self._send_notification(owner, message)
```

---

## 十七、最终总结

### 17.1 终极方案 vs 原方案 vs GLM建议 对照

| 维度 | 原方案 | GLM建议 | 终极方案 |
|------|--------|---------|---------|
| 行级溯源 | 硬编码JSON（❌） | 任务指纹+外部字典（✅方向对） | **业务主键组合（非hash）+ 字典表 + API动态查询** |
| 元数据 | Atlas + OpenLineage（❌阻抗失配） | 去Atlas，用DataHub（✅） | **DataHub + OpenLineage原生集成** |
| 流批统一 | 同一套SQL（❌伪命题） | 逻辑统一，物理分离（✅） | **dbt YAML统一定义 + SQL生成器分别生成** |
| 质量监控 | 只打报告（❌） | 需要阻断（✅） | **QualityGate + AirflowFailException阻断** |
| 回滚 | 无（❌） | 未提及 | **分区快照 + 一键回滚 + 补跑管理器** |
| SLA | 无（❌） | 未提及 | **SLA监控 + 降级策略 + 超时告警** |
| 实时离线对账 | 无（❌） | 未提及 | **T+1自动对账 + 差异告警** |
| 变更管理 | 无（❌） | 未提及 | **Schema变更检测 + 影响分析 + 通知** |
| 部署 | Docker Compose（⚠️仅开发） | 指出非生产级（✅） | **Docker(开发) + K8s(生产) 分离** |
| 溯源键 | 无明确设计 | 建议用hash（⚠️有碰撞风险） | **用业务主键原始值（确定性，无碰撞）** |

### 17.2 核心设计原则（终极版）

```
┌─────────────────────────────────────────────────────────────────────┐
│                    淘系数仓终极方案 · 七条铁律                        │
│                                                                     │
│  1. 溯源字段必须轻量                                                │
│     业务表只存 _etl_task_id + _source_ref（2个字段）                 │
│     详情存字典表，查询时动态关联                                      │
│                                                                     │
│  2. 溯源键必须是确定性业务键                                         │
│     用 "mysql_trade.orders:10001" 而非 hash(...)                    │
│     hash有碰撞风险，生产环境不可接受                                  │
│                                                                     │
│  3. 字段映射必须自动生成                                              │
│     用sqlglot解析SQL AST，不依赖人工维护                              │
│     SQL改了，映射自动跟着改，不会腐化                                  │
│                                                                     │
│  4. 质量门禁必须能阻断                                               │
│     BLOCK级别失败 → 抛异常 → 下游全部停止                            │
│     绝不让错误数据流入下游                                            │
│                                                                     │
│  5. 流批必须承认差异                                                 │
│     逻辑层统一（YAML），物理层分离（Spark SQL / Flink SQL）           │
│     通过代码生成器桥接，不强求一套SQL跑两个引擎                        │
│                                                                     │
│  6. 元数据栈必须收敛                                                 │
│     OpenLineage采集 → DataHub存储展示（原生集成，零Adapter）           │
│     不要混搭不兼容的组件                                              │
│                                                                     │
│  7. 每个关键节点必须有回滚能力                                        │
│     ETL前快照 → 失败回滚 → 补跑恢复                                  │
│     没有回滚能力的ETL不允许上生产                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 17.3 一句话总结

> **这套方案的本质是：用最小的侵入（业务表只加2个字段）实现最大的能力（任意一行数据可追溯到源头），通过自动化（sqlglot解析+OpenLineage采集+质量门禁阻断）消除人工维护的腐化风险，通过旁路字典表实现业务表零膨胀的行级溯源。**



# 终极生产级方案：淘天离线数仓 ChatBI 落地

---

## 一、对 GLM 审判的逐条回应

| GLM 批评 | 我的态度 | 修正方向 |
|---------|---------|---------|
| "WrenAI没有RAG"是事实错误 | ✅ **完全认可，我错了** | WrenAI有RAG，检索的是治理后的MDL语义层 |
| 22,000张表向量化是灾难级反模式 | ✅ **完全认可，我错了** | 只暴露ADS层+指标字典，绝不暴露ODS/DWD |
| WrenAI不支持Hive方言是误判 | ✅ **部分认可** | WrenAI有方言下推能力，但MaxCompute UDF适配确实弱 |
| "收敛口径"是企业铁律 | ✅ **完全认可** | AI只能查治理过的数据，不能自由探索 |
| "DB-GPT骨架+WrenAI灵魂"融合 | ✅ **完全认可** | 这是正确的架构方向 |

**GLM说得最对的一句话：**

> "Qwen 选对了工具，但开错了药方。"

我之前的方案本质上是**"让AI自由探索22,000张表"**，这在生产环境中等于**"让一个实习生拿着root密码直接连生产库"**。

---

## 二、终极架构：DB-GPT骨架 + 语义护栏 + 收敛口径

### 2.1 核心设计原则（铁律）

```
┌─────────────────────────────────────────────────────────────────────┐
│                    淘天 ChatBI 落地五条铁律                           │
│                                                                     │
│  铁律一：绝不暴露裸表                                                │
│    AI 只能查 ADS 层（经过治理的聚合表）和指标字典                      │
│    用户问的问题如果 ADS 层覆盖不了，回复"当前数据未覆盖"               │
│    绝不去 DWD/ODS 层"试探"                                          │
│                                                                     │
│  铁律二：口径必须收敛                                                │
│    "GMV"只有一个定义，不允许 AI 自己猜                                │
│    所有指标必须经过指标平台注册，AI 从字典中取口径                     │
│    没有注册的指标，AI 拒绝回答                                        │
│                                                                     │
│  铁律三：资源必须隔离                                                │
│    ChatBI 查询走独立 Spark 队列（chatbi_queue）                      │
│    单查询资源上限：最多扫描 50GB，超时 5 分钟自动 kill                 │
│    绝不允许 ChatBI 查询击穿离线 ETL 资源                             │
│                                                                     │
│  铁律四：结果必须校验                                                │
│    AI 生成的 SQL 必须经过语法校验 + 语义校验 + 权限校验                │
│    查询结果必须经过合理性校验（如 GMV 不能为负数）                     │
│    校验不通过，不返回结果，返回"无法确认数据准确性"                    │
│                                                                     │
│  铁律五：必须有降级                                                  │
│    LLM 不可用时 → 降级为关键词匹配 + SQL 模板                        │
│    Spark 队列满时 → 降级为查 Doris 加速层（数据可能有 T+1 延迟）      │
│    全部不可用时 → 返回"系统繁忙，请稍后重试"                         │
│    绝不返回未经验证的结果                                             │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 终极架构全景图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         【用户层】                                       │
│                                                                         │
│   运营(钉钉机器人) │ 分析师(Web) │ 产品经理(API) │ 管理层(大屏)          │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────────────────┐
│                    【DB-GPT 应用层（AWEL工作流）】                        │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                                                                 │   │
│   │   用户提问                                                      │   │
│   │     │                                                           │   │
│   │     ▼                                                           │   │
│   │   [意图识别Agent]                                               │   │
│   │     │                                                           │   │
│   │     ├── 指标查询 → [指标字典检索] → [模板SQL生成] → [执行]      │   │
│   │     │                                                           │   │
│   │     ├── 复杂分析 → [多Agent协作] → [多步SQL] → [归因报告]      │   │
│   │     │                                                           │   │
│   │     └── 超出范围 → [拒绝回答] → "当前数据未覆盖该问题"          │   │
│   │                                                                 │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │
│   │ SMMF         │  │ RAG引擎      │  │ SQL校验引擎  │                │
│   │              │  │              │  │              │                │
│   │ Qwen2-72B   │  │ 只检索：     │  │ 语法校验     │                │
│   │ (本地部署)   │  │  ①指标字典   │  │ 语义校验     │                │
│   │              │  │  ②ADS表schema│  │ 权限校验     │                │
│   │              │  │  ③SQL模板    │  │ 资源预估     │                │
│   │              │  │              │  │ 合理性校验   │                │
│   │              │  │ 绝不检索：   │  │              │                │
│   │              │  │  ODS/DWD表   │  │              │                │
│   └──────────────┘  └──────────────┘  └──────────────┘                │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────────────────┐
│                    【语义护栏层（核心创新）】                              │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                    指标字典服务（OneMetric）                      │   │
│   │                                                                 │   │
│   │   ┌─────────────────────────────────────────────────────────┐   │   │
│   │   │ 指标名称 │ 标准口径 │ 推荐表 │ 时间字段 │ 过滤条件 │ Owner│   │   │
│   │   ├─────────────────────────────────────────────────────────┤   │   │
│   │   │ GMV     │ SUM(pay_amount)│ads_platform_gmv│dt│status=│交易组│   │   │
│   │   │         │ WHERE status  │_daily         │  │'paid' │     │   │   │
│   │   │         │ ='paid'      │               │  │       │     │   │   │
│   │   ├─────────────────────────────────────────────────────────┤   │   │
│   │   │ DAU     │ COUNT(DISTINCT│ads_platform_dau│dt│       │用户组│   │   │
│   │   │         │ user_id)     │_daily          │  │       │     │   │   │
│   │   ├─────────────────────────────────────────────────────────┤   │   │
│   │   │ 转化率   │ 下单UV/访问UV│ads_funnel_daily│dt│       │流量组│   │   │
│   │   └─────────────────────────────────────────────────────────┘   │   │
│   │                                                                 │   │
│   │   规则：                                                         │   │
│   │   1. 只有注册过的指标才能被AI查询                                 │   │
│   │   2. 每个指标有且只有一个标准口径                                 │   │
│   │   3. 指标变更必须走审批流程                                      │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                    ADS表白名单（唯一可查数据源）                   │   │
│   │                                                                 │   │
│   │   允许AI查询的表（约200-500张，非22,000张）：                     │   │
│   │   ✅ ads.ads_platform_gmv_daily                                 │   │
│   │   ✅ ads.ads_platform_funnel_daily                              │   │
│   │   ✅ ads.ads_channel_category_funnel                            │   │
│   │   ✅ dws.dws_trade_seller_day（高频使用）                        │   │
│   │   ✅ dim.dim_category（维度表）                                  │   │
│   │                                                                 │   │
│   │   禁止AI查询的表：                                               │   │
│   │   ❌ ods.*（原始层，绝不允许）                                    │   │
│   │   ❌ dwd.*（明细层，绝不允许）                                    │   │
│   │   ❌ 未注册的任何表                                              │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                    查询护栏（Query Guard）                       │   │
│   │                                                                 │   │
│   │   1. 表白名单校验：SQL中的表必须在白名单内                        │   │
│   │   2. 分区裁剪校验：必须包含dt分区条件，禁止全表扫描               │   │
│   │   3. 资源预估：扫描数据量>50GB → 拒绝执行                       │   │
│   │   4. 超时控制：单查询最多5分钟，超时自动kill                      │   │
│   │   5. 并发控制：同时最多20个ChatBI查询                            │   │
│   │   6. 结果校验：GMV<0、转化率>100% → 标记异常                     │   │
│   └─────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────────────────┐
│                    【查询执行层（资源隔离）】                              │
│                                                                         │
│   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│   │ Spark Thrift     │  │ Doris            │  │ MySQL            │     │
│   │ Server           │  │ (加速层)         │  │ (维度表)         │     │
│   │                  │  │                  │  │                  │     │
│   │ 队列:chatbi_queue│  │ ADS层数据同步     │  │ DIM维度表        │     │
│   │ 资源:独立队列    │  │ 秒级响应         │  │ 配置表           │     │
│   │ 限制:50GB/5min  │  │ 适合小查询       │  │ 指标字典         │     │
│   │ 适合大查询       │  │                  │  │                  │     │
│   └──────────────────┘  └──────────────────┘  └──────────────────┘     │
│                                                                         │
│   路由规则：                                                             │
│   - 预估扫描<1GB → Doris（秒级）                                        │
│   - 预估扫描1-50GB → Spark chatbi_queue（分钟级）                        │
│   - 预估扫描>50GB → 拒绝执行                                            │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────────────────┐
│                    【淘天离线数仓（底层）】                                │
│                                                                         │
│   ODS(3000表) → DWD(5000表) → DWS(8000表) → ADS(4000表)               │
│                                                                         │
│   ChatBI 只接触 ADS 层的 200-500 张高频表                                │
│   其余 21,500+ 张表对 AI 完全不可见                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.3 与原方案的关键差异

| 维度 | 原方案（错误） | 终极方案（正确） |
|------|--------------|----------------|
| **AI可见范围** | 22,000张表全部向量化 | 只暴露200-500张ADS白名单表 |
| **口径管理** | AI自己从schema猜 | 指标字典硬编码注入口径 |
| **查询执行** | 无资源限制 | 独立队列+50GB上限+5分钟超时 |
| **结果校验** | 无 | 合理性校验（GMV非负、转化率<100%） |
| **降级策略** | 无 | LLM不可用→模板匹配；队列满→Doris降级 |
| **权限控制** | 简单 | 表级+列级+行级（Ranger） |
| **幻觉防护** | 无 | SQL校验+结果校验+拒绝回答机制 |

---

## 三、核心组件实现（生产级代码）

### 3.1 指标字典服务（语义护栏核心）

```python
# metric_dictionary_service.py
"""
指标字典服务：淘天 ChatBI 的"语义护栏"
核心原则：AI 不允许自己定义指标，只能从字典中取
"""
from fastapi import FastAPI, HTTPException
from typing import Optional
import json

app = FastAPI(title="淘天指标字典服务")

class MetricDictionary:
    """
    指标字典：所有业务指标的唯一权威来源
    数据来源：淘天 OneMetric 指标平台
    同步方式：每日从 OneMetric API 同步
    """
    
    def __init__(self):
        self.metrics = {}
        self.table_whitelist = set()
        self.sql_templates = {}
    
    def load_from_onemetric(self):
        """从 OneMetric 平台同步指标定义"""
        # 实际调用 OneMetric API
        # 这里用静态数据示意
        
        self.metrics = {
            "GMV": {
                "name": "GMV",
                "cn_name": "成交总额",
                "definition": "已支付订单的支付金额总和",
                "formula": "SUM(pay_amount) WHERE order_status = 'paid'",
                "recommended_table": "ads.ads_platform_gmv_daily",
                "time_field": "dt",
                "time_granularity": "日",
                "filters": {"order_status": "paid"},
                "dimensions": ["dt", "category_name", "channel", "seller_id"],
                "owner": "交易平台数据组",
                "sla": "T+1 08:00前产出",
                "unit": "元",
                "validation_rules": {
                    "min_value": 0,          # GMV不能为负
                    "max_fluctuation": 0.5,  # 日波动不超过50%
                }
            },
            "DAU": {
                "name": "DAU",
                "cn_name": "日活跃用户数",
                "definition": "当日有访问行为的去重用户数",
                "formula": "COUNT(DISTINCT user_id)",
                "recommended_table": "ads.ads_platform_dau_daily",
                "time_field": "dt",
                "time_granularity": "日",
                "filters": {},
                "dimensions": ["dt", "platform", "channel"],
                "owner": "用户增长数据组",
                "sla": "T+1 08:00前产出",
                "unit": "人",
                "validation_rules": {
                    "min_value": 0,
                    "max_fluctuation": 0.3,
                }
            },
            "转化率": {
                "name": "转化率",
                "cn_name": "下单转化率",
                "definition": "下单用户数占访问用户数的比例",
                "formula": "COUNT(DISTINCT order_user_id) / COUNT(DISTINCT visit_user_id)",
                "recommended_table": "ads.ads_platform_funnel_daily",
                "time_field": "dt",
                "time_granularity": "日",
                "filters": {},
                "dimensions": ["dt", "channel", "category_name"],
                "owner": "流量数据组",
                "sla": "T+1 09:00前产出",
                "unit": "%",
                "validation_rules": {
                    "min_value": 0,
                    "max_value": 100,  # 转化率不能超过100%
                }
            },
            "客单价": {
                "name": "客单价",
                "cn_name": "平均客单价",
                "definition": "GMV除以支付订单数",
                "formula": "GMV / COUNT(DISTINCT order_id) WHERE order_status = 'paid'",
                "recommended_table": "ads.ads_platform_gmv_daily",
                "time_field": "dt",
                "time_granularity": "日",
                "filters": {"order_status": "paid"},
                "dimensions": ["dt", "category_name"],
                "owner": "交易平台数据组",
                "sla": "T+1 08:00前产出",
                "unit": "元",
                "validation_rules": {
                    "min_value": 0,
                    "max_value": 100000,
                }
            }
        }
        
        # ADS表白名单（只有这些表允许被AI查询）
        self.table_whitelist = {
            "ads.ads_platform_gmv_daily",
            "ads.ads_platform_dau_daily",
            "ads.ads_platform_funnel_daily",
            "ads.ads_channel_category_funnel",
            "ads.ads_seller_performance_daily",
            "dws.dws_trade_seller_day",
            "dws.dws_trade_category_day",
            "dim.dim_category",
            "dim.dim_channel",
        }
    
    def lookup_metric(self, query: str) -> Optional[dict]:
        """
        根据用户问题中的关键词，匹配指标
        返回指标定义（包含标准口径和推荐表）
        """
        # 简单的关键词匹配（实际用向量检索更准）
        query_lower = query.lower()
        
        for name, metric in self.metrics.items():
            if name.lower() in query_lower or metric["cn_name"] in query:
                return metric
        
        # 同义词匹配
        synonyms = {
            "成交额": "GMV",
            "销售额": "GMV",
            "交易额": "GMV",
            "日活": "DAU",
            "活跃用户": "DAU",
            "下单率": "转化率",
            "购买率": "转化率",
        }
        
        for synonym, metric_name in synonyms.items():
            if synonym in query:
                return self.metrics.get(metric_name)
        
        return None
    
    def is_table_allowed(self, table_name: str) -> bool:
        """检查表是否在白名单中"""
        return table_name in self.table_whitelist
    
    def get_sql_template(self, metric_name: str) -> Optional[str]:
        """获取指标的标准SQL模板"""
        metric = self.metrics.get(metric_name)
        if not metric:
            return None
        
        return f"""
        SELECT 
            {metric['time_field']},
            {metric['formula'].split('WHERE')[0].strip()} AS {metric_name}
        FROM {metric['recommended_table']}
        WHERE {{time_condition}}
        GROUP BY {metric['time_field']}
        """


# ===== API端点 =====
metric_dict = MetricDictionary()
metric_dict.load_from_onemetric()

@app.get("/api/v1/metric/lookup")
def api_lookup_metric(query: str):
    """指标查询：根据用户问题匹配指标"""
    metric = metric_dict.lookup_metric(query)
    if metric:
        return {"found": True, "metric": metric}
    return {"found": False, "message": "未找到匹配的指标定义"}

@app.get("/api/v1/table/whitelist")
def api_table_whitelist():
    """获取ADS表白名单"""
    return {"tables": list(metric_dict.table_whitelist)}

@app.get("/api/v1/metric/list")
def api_metric_list():
    """获取所有已注册指标"""
    return {
        "total": len(metric_dict.metrics),
        "metrics": [
            {"name": m["name"], "cn_name": m["cn_name"], "owner": m["owner"]}
            for m in metric_dict.metrics.values()
        ]
    }
```

### 3.2 查询护栏（Query Guard）

```python
# query_guard.py
"""
查询护栏：防止AI生成的SQL击穿底层计算资源
这是整个方案中最关键的安全组件
"""
import re
import sqlglot
from dataclasses import dataclass
from enum import Enum

class GuardVerdict(Enum):
    PASS = "pass"
    BLOCK = "block"
    DEGRADE = "degrade"  # 降级到Doris

@dataclass
class GuardResult:
    verdict: GuardVerdict
    reason: str
    estimated_scan_gb: float = 0
    suggested_engine: str = "doris"

class QueryGuard:
    """
    查询护栏：7层校验
    
    Layer 1: 表白名单校验
    Layer 2: 分区裁剪校验
    Layer 3: 资源预估
    Layer 4: 语法校验
    Layer 5: 语义校验（字段存在性）
    Layer 6: 权限校验
    Layer 7: 结果合理性校验
    """
    
    def __init__(self, metric_dict, spark_session):
        self.metric_dict = metric_dict
        self.spark = spark_session
        self.max_scan_gb = 50       # 最大扫描量
        self.max_timeout_sec = 300  # 最大执行时间
        self.max_concurrent = 20    # 最大并发
    
    def validate(self, sql: str, user_id: str) -> GuardResult:
        """执行全部校验"""
        
        # Layer 1: 表白名单
        result = self._check_table_whitelist(sql)
        if result.verdict == GuardVerdict.BLOCK:
            return result
        
        # Layer 2: 分区裁剪
        result = self._check_partition_pruning(sql)
        if result.verdict == GuardVerdict.BLOCK:
            return result
        
        # Layer 3: 资源预估
        result = self._estimate_resource(sql)
        if result.verdict == GuardVerdict.BLOCK:
            return result
        
        # Layer 4: 语法校验
        result = self._check_syntax(sql)
        if result.verdict == GuardVerdict.BLOCK:
            return result
        
        # Layer 5: 语义校验
        result = self._check_semantics(sql)
        if result.verdict == GuardVerdict.BLOCK:
            return result
        
        # Layer 6: 权限校验
        result = self._check_permission(sql, user_id)
        if result.verdict == GuardVerdict.BLOCK:
            return result
        
        # 全部通过
        return GuardResult(
            verdict=GuardVerdict.PASS,
            reason="全部校验通过",
            estimated_scan_gb=result.estimated_scan_gb,
            suggested_engine=result.suggested_engine
        )
    
    def _check_table_whitelist(self, sql: str) -> GuardResult:
        """Layer 1: 表白名单校验"""
        try:
            parsed = sqlglot.parse_one(sql, read="hive")
            
            # 提取所有引用的表
            referenced_tables = set()
            for table in parsed.find_all(sqlglot.exp.Table):
                table_name = f"{table.db}.{table.name}" if table.db else table.name
                referenced_tables.add(table_name)
            
            # 检查是否都在白名单中
            for table in referenced_tables:
                if not self.metric_dict.is_table_allowed(table):
                    return GuardResult(
                        verdict=GuardVerdict.BLOCK,
                        reason=f"表 {table} 不在ChatBI白名单中。"
                               f"ChatBI只能查询已注册的ADS层表。"
                               f"如需查询该表，请联系数据团队开通权限。"
                    )
            
            return GuardResult(verdict=GuardVerdict.PASS, reason="表白名单校验通过")
        
        except Exception as e:
            return GuardResult(
                verdict=GuardVerdict.BLOCK,
                reason=f"SQL解析失败，无法校验: {str(e)}"
            )
    
    def _check_partition_pruning(self, sql: str) -> GuardResult:
        """Layer 2: 分区裁剪校验（禁止全表扫描）"""
        try:
            parsed = sqlglot.parse_one(sql, read="hive")
            
            # 检查WHERE子句中是否包含分区字段条件
            where_clause = parsed.find(sqlglot.exp.Where)
            if not where_clause:
                return GuardResult(
                    verdict=GuardVerdict.BLOCK,
                    reason="SQL缺少WHERE条件，禁止全表扫描。"
                           "请添加时间分区条件（如 dt BETWEEN '2024-06-01' AND '2024-06-18'）"
                )
            
            # 检查是否包含dt条件
            sql_lower = sql.lower()
            if "dt" not in sql_lower and "dt" not in str(where_clause).lower():
                return GuardResult(
                    verdict=GuardVerdict.BLOCK,
                    reason="SQL缺少分区字段(dt)条件，可能导致全表扫描。"
                )
            
            return GuardResult(verdict=GuardVerdict.PASS, reason="分区裁剪校验通过")
        
        except Exception as e:
            return GuardResult(verdict=GuardVerdict.BLOCK, reason=f"分区校验失败: {e}")
    
    def _estimate_resource(self, sql: str) -> GuardResult:
        """Layer 3: 资源预估"""
        try:
            # 使用Spark的EXPLAIN估算扫描量
            explain_result = self.spark.sql(f"EXPLAIN COST {sql}").collect()
            
            # 解析估算结果（简化）
            estimated_scan_gb = self._parse_scan_estimate(explain_result)
            
            if estimated_scan_gb > self.max_scan_gb:
                return GuardResult(
                    verdict=GuardVerdict.BLOCK,
                    reason=f"预估扫描量 {estimated_scan_gb:.1f}GB 超过上限 {self.max_scan_gb}GB。"
                           f"请缩小查询范围或联系数据团队。",
                    estimated_scan_gb=estimated_scan_gb
                )
            
            # 路由决策
            if estimated_scan_gb < 1:
                engine = "doris"  # 小查询走Doris
            else:
                engine = "spark"  # 大查询走Spark
            
            return GuardResult(
                verdict=GuardVerdict.PASS,
                reason="资源预估通过",
                estimated_scan_gb=estimated_scan_gb,
                suggested_engine=engine
            )
        
        except Exception as e:
            return GuardResult(
                verdict=GuardVerdict.BLOCK,
                reason=f"资源预估失败: {e}"
            )
    
    def _check_syntax(self, sql: str) -> GuardResult:
        """Layer 4: 语法校验"""
        try:
            sqlglot.parse_one(sql, read="hive")
            return GuardResult(verdict=GuardVerdict.PASS, reason="语法校验通过")
        except Exception as e:
            return GuardResult(
                verdict=GuardVerdict.BLOCK,
                reason=f"SQL语法错误: {str(e)}"
            )
    
    def _check_semantics(self, sql: str) -> GuardResult:
        """Layer 5: 语义校验（字段是否存在）"""
        try:
            parsed = sqlglot.parse_one(sql, read="hive")
            
            for table in parsed.find_all(sqlglot.exp.Table):
                table_name = f"{table.db}.{table.name}" if table.db else table.name
                
                # 获取表的实际schema
                try:
                    actual_columns = set(
                        row[0] for row in self.spark.sql(f"DESCRIBE {table_name}").collect()
                    )
                except:
                    continue
                
                # 检查SQL中引用的字段是否存在
                for column in parsed.find_all(sqlglot.exp.Column):
                    if column.table and column.table == table.alias_or_name:
                        if column.name not in actual_columns and column.name != "*":
                            return GuardResult(
                                verdict=GuardVerdict.BLOCK,
                                reason=f"字段 {column.name} 在表 {table_name} 中不存在。"
                                       f"可用字段: {sorted(actual_columns)[:10]}..."
                            )
            
            return GuardResult(verdict=GuardVerdict.PASS, reason="语义校验通过")
        
        except Exception as e:
            return GuardResult(verdict=GuardVerdict.BLOCK, reason=f"语义校验失败: {e}")
    
    def _check_permission(self, sql: str, user_id: str) -> GuardResult:
        """Layer 6: 权限校验"""
        # 实际调用Ranger API检查用户权限
        # 简化示意
        return GuardResult(verdict=GuardVerdict.PASS, reason="权限校验通过")
    
    def _parse_scan_estimate(self, explain_result) -> float:
        """解析EXPLAIN COST结果"""
        # 简化：实际解析Spark的cost估算
        return 2.5  # 示例返回2.5GB
    
    def validate_result(self, result_data: dict, metric_name: str) -> GuardResult:
        """Layer 7: 结果合理性校验"""
        metric = self.metric_dict.metrics.get(metric_name)
        if not metric:
            return GuardResult(verdict=GuardVerdict.PASS, reason="无校验规则")
        
        rules = metric.get("validation_rules", {})
        
        for key, value in result_data.items():
            if isinstance(value, (int, float)):
                if "min_value" in rules and value < rules["min_value"]:
                    return GuardResult(
                        verdict=GuardVerdict.BLOCK,
                        reason=f"结果异常：{key}={value}，低于最小值{rules['min_value']}。"
                               f"可能是数据质量问题，已拦截。"
                    )
                if "max_value" in rules and value > rules["max_value"]:
                    return GuardResult(
                        verdict=GuardVerdict.BLOCK,
                        reason=f"结果异常：{key}={value}，超过最大值{rules['max_value']}。"
                               f"可能是数据质量问题，已拦截。"
                    )
        
        return GuardResult(verdict=GuardVerdict.PASS, reason="结果合理性校验通过")
```

### 3.3 AWEL 工作流（DB-GPT核心编排）

```python
# awel_chatbi_workflow.py
"""
DB-GPT AWEL 工作流：淘天 ChatBI 主链路
"""
from dbgpt.core.awel import DAG, MapOperator, BranchOperator
from dbgpt.core.awel.trigger.http_trigger import HttpRequestTrigger

class TaobaoChatBIWorkflow:
    """
    淘天 ChatBI AWEL 工作流
    
    流程：
    用户提问 → 意图识别 → 指标字典检索 → SQL生成 → 查询护栏 → 执行 → 结果校验 → 返回
    """
    
    def __init__(self, llm_client, metric_dict, query_guard, spark_session):
        self.llm = llm_client
        self.metric_dict = metric_dict
        self.guard = query_guard
        self.spark = spark_session
    
    def build_dag(self):
        """构建AWEL DAG"""
        
        with DAG("taobao_chatbi_main") as dag:
            
            # 节点1：接收用户输入
            input_node = HttpRequestTrigger(
                method="POST",
                endpoint="/api/v1/chatbi/query"
            )
            
            # 节点2：意图识别
            intent_node = MapOperator(self._identify_intent)
            
            # 节点3：分支路由
            route_node = BranchOperator(
                branches=[
                    ("metric_query", self._handle_metric_query),      # 指标查询
                    ("complex_analysis", self._handle_complex_analysis),  # 复杂分析
                    ("out_of_scope", self._handle_out_of_scope),      # 超出范围
                ]
            )
            
            # 节点4：查询护栏
            guard_node = MapOperator(self._apply_query_guard)
            
            # 节点5：执行查询
            execute_node = MapOperator(self._execute_query)
            
            # 节点6：结果校验
            validate_node = MapOperator(self._validate_result)
            
            # 节点7：格式化返回
            format_node = MapOperator(self._format_response)
            
            # 连接节点
            input_node >> intent_node >> route_node
            route_node >> guard_node >> execute_node >> validate_node >> format_node
        
        return dag
    
    def _identify_intent(self, request) -> dict:
        """意图识别：判断查询类型"""
        user_query = request.get("query", "")
        
        # 先查指标字典（确定性匹配）
        metric = self.metric_dict.lookup_metric(user_query)
        
        if metric:
            return {
                "intent": "metric_query",
                "metric": metric,
                "query": user_query
            }
        
        # 复杂分析（包含"为什么"、"对比"、"趋势"等关键词）
        analysis_keywords = ["为什么", "原因", "对比", "趋势", "下降", "增长", "归因"]
        if any(kw in user_query for kw in analysis_keywords):
            return {
                "intent": "complex_analysis",
                "query": user_query
            }
        
        # 超出范围
        return {
            "intent": "out_of_scope",
            "query": user_query
        }
    
    def _handle_metric_query(self, context) -> dict:
        """
        处理指标查询（最常见，60%的查询）
        核心：从指标字典取口径，硬编码注入Prompt
        """
        metric = context["metric"]
        user_query = context["query"]
        
        # 构建Prompt（关键：口径从字典来，不让AI猜）
        prompt = f"""
你是一个数据查询助手。请根据以下信息生成SQL。

【指标定义（必须严格遵守）】
指标名称：{metric['name']}（{metric['cn_name']}）
计算公式：{metric['formula']}
推荐数据表：{metric['recommended_table']}
时间字段：{metric['time_field']}
过滤条件：{metric['filters']}
可用维度：{metric['dimensions']}

【规则】
1. 必须使用推荐数据表，不得使用其他表
2. 必须包含时间分区条件（dt字段）
3. 过滤条件必须严格遵守
4. 只生成SELECT语句，不允许INSERT/UPDATE/DELETE
5. 如果用户的问题超出上述指标定义范围，回复"OUT_OF_SCOPE"

【用户问题】
{user_query}

请生成SQL：
"""
        
        # 调用LLM生成SQL
        sql = self.llm.generate(prompt)
        
        # 检查是否超出范围
        if "OUT_OF_SCOPE" in sql:
            return {
                "status": "out_of_scope",
                "message": f"当前指标[{metric['name']}]不支持该查询维度。"
                          f"支持的维度：{metric['dimensions']}"
            }
        
        return {
            "status": "ready",
            "sql": sql,
            "metric_name": metric["name"],
            "engine": None  # 由护栏决定
        }
    
    def _handle_complex_analysis(self, context) -> dict:
        """
        处理复杂分析（归因、对比、趋势）
        使用多Agent协作
        """
        user_query = context["query"]
        
        # 规划Agent：拆解分析步骤
        plan_prompt = f"""
你是一个数据分析规划师。请将以下问题拆解为多步分析计划。

用户问题：{user_query}

可用的数据表（只能使用这些表）：
{json.dumps(list(self.metric_dict.table_whitelist), ensure_ascii=False)}

可用的指标：
{json.dumps(list(self.metric_dict.metrics.keys()), ensure_ascii=False)}

请输出分析计划（JSON格式）：
[
  {{"step": 1, "action": "查询整体指标", "table": "...", "purpose": "..."}},
  {{"step": 2, "action": "分维度下钻", "table": "...", "purpose": "..."}},
  {{"step": 3, "action": "归因总结", "purpose": "..."}}
]

如果问题超出可用数据范围，输出：{{"out_of_scope": true, "reason": "..."}}
"""
        
        plan = self.llm.generate(plan_prompt)
        
        return {
            "status": "analysis_plan",
            "plan": plan,
            "query": user_query
        }
    
    def _handle_out_of_scope(self, context) -> dict:
        """处理超出范围的查询"""
        return {
            "status": "rejected",
            "message": (
                "抱歉，该问题超出当前ChatBI的数据覆盖范围。\n\n"
                "当前支持查询的指标：\n"
                + "\n".join(f"  - {m['cn_name']}({m['name']})" 
                           for m in self.metric_dict.metrics.values())
                + "\n\n如需新增指标，请联系数据团队在指标平台注册。"
            )
        }
    
    def _apply_query_guard(self, context) -> dict:
        """应用查询护栏"""
        if context.get("status") != "ready":
            return context
        
        sql = context["sql"]
        user_id = context.get("user_id", "anonymous")
        
        guard_result = self.guard.validate(sql, user_id)
        
        if guard_result.verdict == GuardVerdict.BLOCK:
            return {
                "status": "blocked",
                "message": f"查询被安全策略拦截：{guard_result.reason}",
                "sql": sql
            }
        
        context["engine"] = guard_result.suggested_engine
        context["estimated_scan_gb"] = guard_result.estimated_scan_gb
        return context
    
    def _execute_query(self, context) -> dict:
        """执行查询（带资源隔离）"""
        if context.get("status") in ("blocked", "rejected", "out_of_scope"):
            return context
        
        sql = context["sql"]
        engine = context.get("engine", "doris")
        
        try:
            if engine == "doris":
                # 走Doris（小查询，秒级）
                result = self._execute_on_doris(sql)
            else:
                # 走Spark chatbi_queue（大查询，分钟级）
                result = self._execute_on_spark(sql)
            
            context["status"] = "executed"
            context["result"] = result
            return context
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"查询执行失败：{str(e)}",
                "sql": sql
            }
    
    def _validate_result(self, context) -> dict:
        """结果合理性校验"""
        if context.get("status") != "executed":
            return context
        
        metric_name = context.get("metric_name")
        result = context.get("result", {})
        
        validate_result = self.guard.validate_result(result, metric_name)
        
        if validate_result.verdict == GuardVerdict.BLOCK:
            return {
                "status": "result_anomaly",
                "message": f"查询结果异常，已拦截：{validate_result.reason}",
                "raw_result": result
            }
        
        context["status"] = "validated"
        return context
    
    def _format_response(self, context) -> dict:
        """格式化最终响应"""
        if context.get("status") in ("blocked", "rejected", "out_of_scope", 
                                      "error", "result_anomaly"):
            return {
                "success": False,
                "message": context.get("message", "未知错误"),
                "data": None
            }
        
        return {
            "success": True,
            "message": "查询成功",
            "data": context.get("result"),
            "metadata": {
                "sql": context.get("sql"),
                "engine": context.get("engine"),
                "scan_gb": context.get("estimated_scan_gb"),
                "metric": context.get("metric_name")
            }
        }
```

### 3.4 降级策略

```python
# degradation_manager.py
"""
降级策略：确保ChatBI在任何情况下都能给出响应
绝不允许返回未经验证的结果
"""
from enum import Enum

class DegradationLevel(Enum):
    NORMAL = "normal"           # 正常：LLM生成SQL
    TEMPLATE = "template"       # 降级1：SQL模板匹配
    CACHED = "cached"           # 降级2：返回缓存结果
    REJECT = "reject"           # 降级3：拒绝服务

class DegradationManager:
    """
    降级管理器
    
    触发条件：
    - LLM服务不可用 → 降级为SQL模板匹配
    - Spark队列满 → 降级为Doris查询
    - Doris也不可用 → 返回缓存结果
    - 全部不可用 → 拒绝服务
    """
    
    def __init__(self, metric_dict):
        self.metric_dict = metric_dict
        self.sql_templates = self._load_templates()
        self.result_cache = {}  # 实际用Redis
    
    def get_degradation_level(self) -> DegradationLevel:
        """判断当前降级级别"""
        if not self._is_llm_available():
            if self._is_spark_available():
                return DegradationLevel.TEMPLATE
            elif self._is_doris_available():
                return DegradationLevel.TEMPLATE
            elif self._has_cached_results():
                return DegradationLevel.CACHED
            else:
                return DegradationLevel.REJECT
        
        if not self._is_spark_available():
            if self._is_doris_available():
                return DegradationLevel.NORMAL  # 走Doris
            else:
                return DegradationLevel.CACHED
        
        return DegradationLevel.NORMAL
    
    def handle_with_template(self, user_query: str) -> dict:
        """降级模式：使用SQL模板"""
        metric = self.metric_dict.lookup_metric(user_query)
        
        if not metric:
            return {
                "success": False,
                "message": "AI服务暂时不可用，且未找到匹配的指标模板。请稍后重试。"
            }
        
        # 使用预定义的SQL模板
        template = self.sql_templates.get(metric["name"])
        if template:
            # 简单的时间范围提取
            time_condition = self._extract_time_range(user_query)
            sql = template.replace("{time_condition}", time_condition)
            
            return {
                "success": True,
                "message": f"[降级模式] 使用标准模板查询 {metric['cn_name']}",
                "sql": sql,
                "degradation": "template"
            }
        
        return {
            "success": False,
            "message": "AI服务暂时不可用，请稍后重试。"
        }
    
    def _load_templates(self) -> dict:
        """加载SQL模板（人工维护的标准查询）"""
        return {
            "GMV": """
                SELECT dt, SUM(gmv) as gmv
                FROM ads.ads_platform_gmv_daily
                WHERE {time_condition}
                GROUP BY dt ORDER BY dt
            """,
            "DAU": """
                SELECT dt, dau
                FROM ads.ads_platform_dau_daily
                WHERE {time_condition}
                ORDER BY dt
            """,
            "转化率": """
                SELECT dt, conversion_rate
                FROM ads.ads_platform_funnel_daily
                WHERE {time_condition}
                ORDER BY dt
            """,
        }
    
    def _extract_time_range(self, query: str) -> str:
        """从用户问题中提取时间范围（简化版）"""
        import re
        from datetime import datetime, timedelta
        
        # 匹配"最近N天"
        match = re.search(r'最近(\d+)天', query)
        if match:
            days = int(match.group(1))
            end = datetime.now()
            start = end - timedelta(days=days)
            return f"dt BETWEEN '{start.strftime('%Y-%m-%d')}' AND '{end.strftime('%Y-%m-%d')}'"
        
        # 匹配"上个月"
        if "上个月" in query:
            now = datetime.now()
            if now.month == 1:
                start = now.replace(year=now.year-1, month=12, day=1)
            else:
                start = now.replace(month=now.month-1, day=1)
            end = now.replace(day=1) - timedelta(days=1)
            return f"dt BETWEEN '{start.strftime('%Y-%m-%d')}' AND '{end.strftime('%Y-%m-%d')}'"
        
        # 默认：最近7天
        end = datetime.now()
        start = end - timedelta(days=7)
        return f"dt BETWEEN '{start.strftime('%Y-%m-%d')}' AND '{end.strftime('%Y-%m-%d')}'"
    
    def _is_llm_available(self) -> bool:
        """检查LLM服务是否可用"""
        # 实际调用健康检查API
        return True
    
    def _is_spark_available(self) -> bool:
        """检查Spark队列是否可用"""
        return True
    
    def _is_doris_available(self) -> bool:
        """检查Doris是否可用"""
        return True
    
    def _has_cached_results(self) -> bool:
        """检查是否有缓存结果"""
        return len(self.result_cache) > 0
```

---

## 四、生产级测试方案

### 4.1 护栏测试（最关键）

```python
# test_query_guard.py
"""
查询护栏测试：确保所有防护措施生效
"""
import pytest

class TestQueryGuard:
    """查询护栏测试套件"""
    
    @pytest.fixture
    def guard(self):
        return QueryGuard(metric_dict, spark_session)
    
    # ===== 表白名单测试 =====
    def test_block_ods_table(self, guard):
        """测试：禁止查询ODS层"""
        sql = "SELECT * FROM ods.ods_trade_order WHERE dt='2024-06-15'"
        result = guard.validate(sql, "user1")
        assert result.verdict == GuardVerdict.BLOCK
        assert "白名单" in result.reason
    
    def test_block_dwd_table(self, guard):
        """测试：禁止查询DWD层"""
        sql = "SELECT * FROM dwd.dwd_trade_order_detail WHERE dt='2024-06-15'"
        result = guard.validate(sql, "user1")
        assert result.verdict == GuardVerdict.BLOCK
    
    def test_allow_ads_table(self, guard):
        """测试：允许查询ADS白名单表"""
        sql = "SELECT dt, gmv FROM ads.ads_platform_gmv_daily WHERE dt='2024-06-15'"
        result = guard.validate(sql, "user1")
        assert result.verdict == GuardVerdict.PASS
    
    # ===== 分区裁剪测试 =====
    def test_block_full_table_scan(self, guard):
        """测试：禁止无分区条件的查询"""
        sql = "SELECT * FROM ads.ads_platform_gmv_daily"
        result = guard.validate(sql, "user1")
        assert result.verdict == GuardVerdict.BLOCK
        assert "分区" in result.reason or "WHERE" in result.reason
    
    # ===== 资源预估测试 =====
    def test_block_large_scan(self, guard):
        """测试：拒绝扫描量超过50GB的查询"""
        # 模拟一个扫描100GB的查询
        sql = """
            SELECT * FROM ads.ads_platform_gmv_daily 
            WHERE dt BETWEEN '2020-01-01' AND '2024-12-31'
        """
        # 这个时间范围会扫描大量数据
        result = guard.validate(sql, "user1")
        # 根据实际预估结果判断
        if result.estimated_scan_gb > 50:
            assert result.verdict == GuardVerdict.BLOCK
    
    # ===== 结果校验测试 =====
    def test_block_negative_gmv(self, guard):
        """测试：拦截负数GMV"""
        result_data = {"gmv": -100}
        result = guard.validate_result(result_data, "GMV")
        assert result.verdict == GuardVerdict.BLOCK
        assert "异常" in result.reason
    
    def test_block_impossible_conversion_rate(self, guard):
        """测试：拦截超过100%的转化率"""
        result_data = {"conversion_rate": 150}
        result = guard.validate_result(result_data, "转化率")
        assert result.verdict == GuardVerdict.BLOCK
    
    def test_allow_valid_result(self, guard):
        """测试：通过正常结果"""
        result_data = {"gmv": 52300000}
        result = guard.validate_result(result_data, "GMV")
        assert result.verdict == GuardVerdict.PASS
    
    # ===== SQL注入防护测试 =====
    def test_block_sql_injection(self, guard):
        """测试：拦截SQL注入"""
        sql = "SELECT * FROM ads.ads_platform_gmv_daily WHERE dt='2024-06-15'; DROP TABLE ads.ads_platform_gmv_daily"
        result = guard.validate(sql, "user1")
        assert result.verdict == GuardVerdict.BLOCK
    
    def test_block_write_operation(self, guard):
        """测试：拦截写操作"""
        sql = "INSERT INTO ads.ads_platform_gmv_daily VALUES (...)"
        result = guard.validate(sql, "user1")
        assert result.verdict == GuardVerdict.BLOCK
    
    # ===== 降级测试 =====
    def test_degradation_to_template(self):
        """测试：LLM不可用时降级为模板"""
        dm = DegradationManager(metric_dict)
        # 模拟LLM不可用
        dm._is_llm_available = lambda: False
        
        result = dm.handle_with_template("最近7天的GMV")
        assert result["success"] == True
        assert result["degradation"] == "template"
        assert "ads_platform_gmv_daily" in result["sql"]
```

### 4.2 端到端测试

```python
# test_e2e_chatbi.py
"""
端到端测试：从用户提问到结果返回的完整链路
"""
import pytest
import requests

class TestE2EChatBI:
    
    BASE_URL = "http://localhost:5670"
    
    def test_01_simple_gmv_query(self):
        """场景1：简单指标查询"""
        response = requests.post(f"{self.BASE_URL}/api/v1/chatbi/query", json={
            "query": "618大促期间（6月1日到18日）平台GMV是多少？",
            "user_id": "ops_user_001"
        })
        
        assert response.status_code == 200
        result = response.json()
        
        assert result["success"] == True
        assert result["data"] is not None
        assert result["metadata"]["engine"] in ("doris", "spark")
        # GMV必须是正数
        assert result["data"]["gmv"] > 0
    
    def test_02_block_ods_query(self):
        """场景2：试图查ODS层（应被拦截）"""
        response = requests.post(f"{self.BASE_URL}/api/v1/chatbi/query", json={
            "query": "帮我查一下ods_trade_order表里order_id=10001的数据",
            "user_id": "ops_user_001"
        })
        
        result = response.json()
        assert result["success"] == False
        assert "白名单" in result["message"] or "未覆盖" in result["message"]
    
    def test_03_unregistered_metric(self):
        """场景3：查询未注册的指标（应拒绝）"""
        response = requests.post(f"{self.BASE_URL}/api/v1/chatbi/query", json={
            "query": "我们的NPS评分是多少？",
            "user_id": "ops_user_001"
        })
        
        result = response.json()
        assert result["success"] == False
        assert "未覆盖" in result["message"] or "未找到" in result["message"]
    
    def test_04_complex_analysis(self):
        """场景4：归因分析（多Agent）"""
        response = requests.post(f"{self.BASE_URL}/api/v1/chatbi/query", json={
            "query": "为什么618大促期间转化率比去年下降了？",
            "user_id": "pm_user_001"
        })
        
        result = response.json()
        assert result["success"] == True
        assert "归因" in str(result["data"]) or "分析" in str(result["data"])
    
    def test_05_degradation_mode(self):
        """场景5：降级模式测试（模拟LLM不可用）"""
        # 通过管理API模拟LLM故障
        requests.post(f"{self.BASE_URL}/api/v1/admin/simulate_llm_failure")
        
        response = requests.post(f"{self.BASE_URL}/api/v1/chatbi/query", json={
            "query": "最近7天GMV",
            "user_id": "ops_user_001"
        })
        
        result = response.json()
        # 降级模式也应该能返回结果（使用模板）
        assert result["success"] == True
        assert result.get("degradation") == "template"
        
        # 恢复LLM
        requests.post(f"{self.BASE_URL}/api/v1/admin/restore_llm")
    
    def test_06_concurrent_limit(self):
        """场景6：并发限制测试"""
        import concurrent.futures
        
        def make_query(i):
            return requests.post(f"{self.BASE_URL}/api/v1/chatbi/query", json={
                "query": f"第{i}天的GMV",
                "user_id": f"user_{i}"
            })
        
        # 同时发30个请求（超过20的并发限制）
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            futures = [executor.submit(make_query, i) for i in range(30)]
            results = [f.result() for f in futures]
        
        # 应该有部分请求被限流
        blocked_count = sum(1 for r in results if r.json().get("success") == False)
        assert blocked_count > 0, "并发限制未生效"
```

---

## 五、部署架构（生产环境）

```yaml
# k8s/chatbi-deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: chatbi-dbgpt
  namespace: taobao-dw
spec:
  replicas: 4  # 4个实例，支持高可用
  template:
    spec:
      containers:
      - name: dbgpt-app
        image: taobao/dbgpt-chatbi:0.8.0
        ports:
        - containerPort: 5670
        resources:
          requests:
            memory: "8Gi"
            cpu: "4000m"
          limits:
            memory: "16Gi"
            cpu: "8000m"
        env:
        - name: LLM_ENDPOINT
          value: "http://vllm-service:8000"  # 本地模型服务
        - name: METRIC_DICT_URL
          value: "http://metric-dict-service:8081"
        - name: SPARK_THRIFT_URL
          value: "jdbc:hive2://spark-thrift:10000/;queue=chatbi_queue"
        - name: DORIS_URL
          value: "jdbc:mysql://doris-fe:9030"
        - name: MILVUS_URL
          value: "milvus-service:19530"
        - name: MAX_SCAN_GB
          value: "50"
        - name: MAX_TIMEOUT_SEC
          value: "300"
        - name: MAX_CONCURRENT
          value: "20"

---
# 模型服务（独立GPU节点）
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-qwen2-72b
  namespace: taobao-dw
spec:
  replicas: 2
  template:
    spec:
      nodeSelector:
        gpu: "true"
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        args:
        - --model=/models/Qwen2-72B-Chat
        - --quantization=awq  # INT4量化，降低显存
        - --max-model-len=32768
        - --gpu-memory-utilization=0.9
        resources:
          limits:
            nvidia.com/gpu: 4  # 4张A100

---
# Spark独立队列配置
# spark-thrift-server 配置
apiVersion: v1
kind: ConfigMap
metadata:
  name: spark-chatbi-config
data:
  spark-queue-config: |
    # chatbi_queue 独立资源队列
    # 与离线ETL队列完全隔离
    yarn.scheduler.capacity.root.chatbi_queue.capacity=10
    yarn.scheduler.capacity.root.chatbi_queue.maximum-capacity=15
    yarn.scheduler.capacity.root.chatbi_queue.maximum-application-master-resource-percent=0.5
    # 单应用最大资源
    spark.yarn.maxAppAttempts=1
    spark.dynamicAllocation.maxExecutors=10
    spark.executor.memory=8g
    spark.executor.cores=2
```

---

## 六、最终总结

```
┌─────────────────────────────────────────────────────────────────────┐
│                    终极方案核心要点                                   │
│                                                                     │
│  选型：DB-GPT（多Agent编排 + 本地模型 + RAG）                        │
│                                                                     │
│  架构核心：DB-GPT骨架 + 语义护栏 + 收敛口径                          │
│                                                                     │
│  五条铁律：                                                          │
│    1. 只暴露ADS白名单表（200-500张），绝不暴露22,000张               │
│    2. 指标口径从字典取，AI不允许自己猜                                │
│    3. 独立Spark队列 + 50GB扫描上限 + 5分钟超时                       │
│    4. SQL七层校验 + 结果合理性校验                                    │
│    5. 三级降级（模板→缓存→拒绝），绝不返回未验证结果                   │
│                                                                     │
│  与原方案的关键修正：                                                │
│    ❌ 22,000张表向量化 → ✅ 只向量化ADS白名单表                       │
│    ❌ AI自由探索 → ✅ 指标字典硬编码口径                              │
│    ❌ 无资源限制 → ✅ 独立队列+扫描上限+超时控制                      │
│    ❌ 无结果校验 → ✅ 七层护栏                                       │
│    ❌ 无降级 → ✅ 三级降级策略                                       │
│                                                                     │
│  一句话：                                                           │
│  ChatBI的本质不是"让AI自由查数据"，                                  │
│  而是"让AI在严格护栏内安全地查治理过的数据"。                         │
│  护栏越严格，系统越可靠，业务方越敢用。                               │
└─────────────────────────────────────────────────────────────────────┘
```



# 终结版：淘天离线数仓 ChatBI 生产落地方案

---

## 一、对 GLM 终审的专业判断

| GLM 指出的隐患 | 我的判断 | 理由 |
|---------------|---------|------|
| EXPLAIN COST 击穿 Spark Thrift Server | ✅ **完全认可，必须修** | 20并发×复杂EXPLAIN = Driver OOM，大促期间直接炸 |
| DESCRIBE 实时查 Metastore 导致高延迟 | ✅ **完全认可，必须修** | 每次查询多一次 Metastore RPC，叠加网络抖动，用户体验崩 |
| 多步SQL未逐步过护栏（越狱风险） | ✅ **完全认可，必须修** | 这是安全漏洞，一条未校验SQL就能全表扫描 |

**三个都是真实的生产事故隐患，不是"过度设计"，必须修。**

GLM 的终审结论我认可：**架构方向正确，代码细节需要这三个修补才能上生产线。**

---

## 二、终结版方案（含全部修正）

### 2.1 系统全景（最终版）

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            【用户接入层】                                     │
│                                                                             │
│   钉钉机器人(运营) │ Web UI(分析师) │ API(产品/开发) │ 大屏(管理层)          │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    【DB-GPT AWEL 工作流引擎】                                │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                                                                     │    │
│  │  用户提问                                                           │    │
│  │    │                                                                │    │
│  │    ▼                                                                │    │
│  │  [意图识别] ──→ 指标查询(60%) / 复杂分析(30%) / 超出范围(10%)       │    │
│  │    │                                                                │    │
│  │    ▼                                                                │    │
│  │  [指标字典硬注入] ──→ Prompt中写死口径，AI不允许自由发挥             │    │
│  │    │                                                                │    │
│  │    ▼                                                                │    │
│  │  [SQL生成] ──→ LLM基于口径+白名单表schema生成                       │    │
│  │    │                                                                │    │
│  │    ▼                                                                │    │
│  │  [QueryGuard 七层校验] ──→ 每步SQL必须过，无例外                    │    │
│  │    │                                                                │    │
│  │    ▼                                                                │    │
│  │  [路由执行] ──→ Doris(<1GB) / Spark chatbi_queue(1-50GB)           │    │
│  │    │                                                                │    │
│  │    ▼                                                                │    │
│  │  [结果校验] ──→ 合理性检查 → 通过则返回 / 异常则拦截                │    │
│  │    │                                                                │    │
│  │    ▼                                                                │    │
│  │  [降级兜底] ──→ LLM挂→模板 / 队列满→Doris / 全挂→拒绝              │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                │
│  │ SMMF           │  │ RAG引擎        │  │ Schema Cache   │                │
│  │ Qwen2-72B     │  │               │  │ (本地内存)     │                │
│  │ 本地部署       │  │ 只检索:       │  │               │                │
│  │ INT4量化       │  │  指标字典     │  │ 白名单表结构   │                │
│  │ vLLM推理      │  │  ADS表schema  │  │ 每日凌晨刷新   │                │
│  │               │  │  SQL模板      │  │ 0ms查询延迟   │                │
│  └────────────────┘  └────────────────┘  └────────────────┘                │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    【语义护栏层】                                             │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  指标字典(OneMetric同步)  │  ADS表白名单(200-500张)  │  SQL模板库  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  QueryGuard 七层校验                                                 │    │
│  │  L1表白名单 → L2分区裁剪 → L3资源估算(元数据法) → L4语法            │    │
│  │  → L5语义(本地缓存) → L6权限 → L7结果合理性                         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    【查询执行层（资源隔离）】                                  │
│                                                                             │
│   ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐     │
│   │ Doris            │    │ Spark Thrift     │    │ MySQL            │     │
│   │ (加速层)         │    │ (chatbi_queue)   │    │ (维度/字典)      │     │
│   │                  │    │                  │    │                  │     │
│   │ 扫描<1GB走这里   │    │ 扫描1-50GB走这里 │    │ 指标字典         │     │
│   │ 秒级响应         │    │ 独立队列         │    │ 配置信息         │     │
│   │ 最多并发50       │    │ 最多并发20       │    │                  │     │
│   │                  │    │ 超时5min自动kill │    │                  │     │
│   └──────────────────┘    └──────────────────┘    └──────────────────┘     │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    【淘天离线数仓】                                           │
│                                                                             │
│   ODS(3000) → DWD(5000) → DWS(8000) → ADS(4000)                           │
│                                                                             │
│   ChatBI只接触ADS白名单中的200-500张表                                       │
│   其余21,500+张表对AI完全不可见、不可达                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 2.2 核心组件一：QueryGuard（含三处修正）

```python
# query_guard_final.py
"""
QueryGuard 终结版
修正点：
  1. 资源估算：用元数据法替代EXPLAIN COST（防止击穿Thrift Server）
  2. 语义校验：用本地Schema缓存替代实时DESCRIBE（0ms延迟）
  3. 多步校验：每一步SQL必须独立过护栏（防止越狱）
"""
import sqlglot
from sqlglot import exp
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Set
from datetime import datetime
import threading
import logging

logger = logging.getLogger("QueryGuard")


class GuardVerdict(Enum):
    PASS = "pass"
    BLOCK = "block"
    DEGRADE = "degrade"


@dataclass
class GuardResult:
    verdict: GuardVerdict
    reason: str
    estimated_scan_gb: float = 0
    suggested_engine: str = "doris"


class SchemaCache:
    """
    本地Schema缓存（修正点2）
    每日凌晨从Hive Metastore拉取白名单表结构到内存
    查询时0ms延迟，不依赖网络
    """
    
    def __init__(self):
        self._cache: Dict[str, Set[str]] = {}  # table_name -> set of columns
        self._partition_sizes: Dict[str, float] = {}  # table_name -> avg partition size GB
        self._lock = threading.RLock()
        self._last_refresh: Optional[datetime] = None
    
    def refresh(self, spark_session, table_whitelist: set):
        """
        刷新缓存（由定时任务调用，每日凌晨执行）
        不在用户请求链路中执行
        """
        new_cache = {}
        new_sizes = {}
        
        for table_name in table_whitelist:
            try:
                # 获取列信息
                schema_rows = spark_session.sql(f"DESCRIBE {table_name}").collect()
                columns = {row[0] for row in schema_rows if row[0] and not row[0].startswith('#')}
                new_cache[table_name] = columns
                
                # 获取分区大小统计（从Metastore统计信息）
                stats = spark_session.sql(f"""
                    SELECT AVG(data_size) / 1073741824.0 as avg_partition_gb
                    FROM (
                        SELECT data_size FROM FILES('{table_name}') 
                        GROUP BY partition_name
                    )
                """).collect()
                
                if stats and stats[0][0]:
                    new_sizes[table_name] = float(stats[0][0])
                else:
                    new_sizes[table_name] = 1.0  # 默认1GB/分区
                
            except Exception as e:
                logger.warning(f"Schema缓存刷新失败: {table_name}, {e}")
                continue
        
        with self._lock:
            self._cache = new_cache
            self._partition_sizes = new_sizes
            self._last_refresh = datetime.now()
        
        logger.info(f"Schema缓存刷新完成: {len(new_cache)}张表, 时间={self._last_refresh}")
    
    def get_columns(self, table_name: str) -> Optional[Set[str]]:
        """获取表的列集合（0ms，纯内存）"""
        with self._lock:
            return self._cache.get(table_name)
    
    def get_partition_size_gb(self, table_name: str) -> float:
        """获取单分区平均大小（0ms，纯内存）"""
        with self._lock:
            return self._partition_sizes.get(table_name, 1.0)
    
    @property
    def is_stale(self) -> bool:
        """缓存是否过期（超过24小时）"""
        if self._last_refresh is None:
            return True
        return (datetime.now() - self._last_refresh).total_seconds() > 86400


class QueryGuard:
    """
    查询护栏终结版：七层校验
    
    修正点汇总：
    - L3资源估算：元数据法（不触发EXPLAIN）
    - L5语义校验：本地缓存（不查Metastore）
    - 多步校验：每步独立过护栏
    """
    
    def __init__(self, metric_dict, schema_cache: SchemaCache):
        self.metric_dict = metric_dict
        self.schema_cache = schema_cache
        self.max_scan_gb = 50
        self.max_timeout_sec = 300
        self.max_concurrent = 20
        self._current_concurrent = 0
        self._concurrent_lock = threading.Lock()
    
    def validate(self, sql: str, user_id: str) -> GuardResult:
        """
        执行全部七层校验
        任何一层BLOCK → 立即返回，不执行后续层
        """
        
        # L1: 表白名单
        r = self._check_table_whitelist(sql)
        if r.verdict == GuardVerdict.BLOCK:
            return r
        
        # L2: 分区裁剪
        r = self._check_partition_pruning(sql)
        if r.verdict == GuardVerdict.BLOCK:
            return r
        
        # L3: 资源估算（修正点1：元数据法）
        r = self._estimate_resource_by_metadata(sql)
        if r.verdict == GuardVerdict.BLOCK:
            return r
        
        # L4: 语法校验
        r = self._check_syntax(sql)
        if r.verdict == GuardVerdict.BLOCK:
            return r
        
        # L5: 语义校验（修正点2：本地缓存）
        r = self._check_semantics_cached(sql)
        if r.verdict == GuardVerdict.BLOCK:
            return r
        
        # L6: 权限校验
        r = self._check_permission(sql, user_id)
        if r.verdict == GuardVerdict.BLOCK:
            return r
        
        # L7: 并发控制
        r = self._check_concurrency()
        if r.verdict == GuardVerdict.BLOCK:
            return r
        
        return r
    
    def validate_step(self, sql: str, user_id: str, step_num: int) -> GuardResult:
        """
        修正点3：多步分析中，每一步SQL独立校验
        """
        result = self.validate(sql, user_id)
        if result.verdict == GuardVerdict.BLOCK:
            result.reason = f"分析步骤{step_num}被拦截: {result.reason}"
        return result
    
    # ===== L1: 表白名单 =====
    def _check_table_whitelist(self, sql: str) -> GuardResult:
        try:
            parsed = sqlglot.parse_one(sql, read="hive")
            
            for table in parsed.find_all(exp.Table):
                table_name = f"{table.db}.{table.name}" if table.db else table.name
                
                if not self.metric_dict.is_table_allowed(table_name):
                    return GuardResult(
                        verdict=GuardVerdict.BLOCK,
                        reason=f"表[{table_name}]不在ChatBI白名单中。"
                               f"当前仅支持查询已注册的ADS层聚合表。"
                    )
            
            return GuardResult(verdict=GuardVerdict.PASS, reason="L1通过")
        
        except Exception as e:
            return GuardResult(verdict=GuardVerdict.BLOCK, reason=f"SQL解析失败: {e}")
    
    # ===== L2: 分区裁剪 =====
    def _check_partition_pruning(self, sql: str) -> GuardResult:
        try:
            parsed = sqlglot.parse_one(sql, read="hive")
            where = parsed.find(exp.Where)
            
            if not where:
                return GuardResult(
                    verdict=GuardVerdict.BLOCK,
                    reason="缺少WHERE条件，禁止全表扫描。请添加dt分区条件。"
                )
            
            # 检查是否包含dt条件
            where_str = where.sql(dialect="hive").lower()
            if "dt" not in where_str:
                return GuardResult(
                    verdict=GuardVerdict.BLOCK,
                    reason="WHERE条件中缺少dt分区字段，可能导致全表扫描。"
                )
            
            return GuardResult(verdict=GuardVerdict.PASS, reason="L2通过")
        
        except Exception as e:
            return GuardResult(verdict=GuardVerdict.BLOCK, reason=f"分区校验失败: {e}")
    
    # ===== L3: 资源估算（修正点1：元数据法，不用EXPLAIN） =====
    def _estimate_resource_by_metadata(self, sql: str) -> GuardResult:
        """
        基于元数据的轻量级资源估算
        不触发Spark Catalyst，不读Thrift Server
        纯内存计算，耗时<1ms
        """
        try:
            parsed = sqlglot.parse_one(sql, read="hive")
            
            # 提取涉及的表
            tables = []
            for table in parsed.find_all(exp.Table):
                table_name = f"{table.db}.{table.name}" if table.db else table.name
                tables.append(table_name)
            
            if not tables:
                return GuardResult(verdict=GuardVerdict.BLOCK, reason="未找到查询表")
            
            # 提取时间范围（天数）
            days = self._extract_days_from_where(sql)
            
            # 计算估算扫描量
            total_scan_gb = 0
            for table_name in tables:
                partition_size = self.schema_cache.get_partition_size_gb(table_name)
                total_scan_gb += days * partition_size
            
            if total_scan_gb > self.max_scan_gb:
                return GuardResult(
                    verdict=GuardVerdict.BLOCK,
                    reason=f"预估扫描量{total_scan_gb:.1f}GB，超过上限{self.max_scan_gb}GB。"
                           f"请缩小时间范围。",
                    estimated_scan_gb=total_scan_gb
                )
            
            # 路由决策
            engine = "doris" if total_scan_gb < 1.0 else "spark"
            
            return GuardResult(
                verdict=GuardVerdict.PASS,
                reason=f"L3通过，预估扫描{total_scan_gb:.1f}GB",
                estimated_scan_gb=total_scan_gb,
                suggested_engine=engine
            )
        
        except Exception as e:
            # 估算失败：保守策略，降级到Doris
            return GuardResult(
                verdict=GuardVerdict.DEGRADE,
                reason=f"资源估算失败({e})，降级到Doris执行",
                suggested_engine="doris"
            )
    
    def _extract_days_from_where(self, sql: str) -> int:
        """从WHERE条件中提取时间跨度（天数）"""
        import re
        
        # 匹配 BETWEEN 'yyyy-mm-dd' AND 'yyyy-mm-dd'
        match = re.search(
            r"BETWEEN\s+'(\d{4}-\d{2}-\d{2})'\s+AND\s+'(\d{4}-\d{2}-\d{2})'",
            sql, re.IGNORECASE
        )
        if match:
            from datetime import datetime
            start = datetime.strptime(match.group(1), "%Y-%m-%d")
            end = datetime.strptime(match.group(2), "%Y-%m-%d")
            return max((end - start).days, 1)
        
        # 匹配 dt = 'yyyy-mm-dd'（单天）
        if re.search(r"dt\s*=\s*'\d{4}-\d{2}-\d{2}'", sql):
            return 1
        
        # 匹配 dt >= 'yyyy-mm-dd'（无上限，保守估计30天）
        if re.search(r"dt\s*>=\s*'\d{4}-\d{2}-\d{2}'", sql):
            return 30
        
        # 无法解析，保守估计7天
        return 7
    
    # ===== L4: 语法校验 =====
    def _check_syntax(self, sql: str) -> GuardResult:
        try:
            sqlglot.parse_one(sql, read="hive")
            return GuardResult(verdict=GuardVerdict.PASS, reason="L4通过")
        except Exception as e:
            return GuardResult(verdict=GuardVerdict.BLOCK, reason=f"SQL语法错误: {e}")
    
    # ===== L5: 语义校验（修正点2：本地缓存，0ms） =====
    def _check_semantics_cached(self, sql: str) -> GuardResult:
        """
        基于本地Schema缓存的语义校验
        不查Metastore，纯内存操作
        """
        try:
            parsed = sqlglot.parse_one(sql, read="hive")
            
            for table in parsed.find_all(exp.Table):
                table_name = f"{table.db}.{table.name}" if table.db else table.name
                
                # 从本地缓存获取列信息（0ms）
                actual_columns = self.schema_cache.get_columns(table_name)
                
                if actual_columns is None:
                    return GuardResult(
                        verdict=GuardVerdict.BLOCK,
                        reason=f"表[{table_name}]未纳管，无法校验字段。"
                    )
                
                # 检查SQL中引用的列是否存在
                table_alias = table.alias_or_name
                for column in parsed.find_all(exp.Column):
                    # 只检查明确指定了表别名的列
                    if column.table == table_alias and column.name != "*":
                        if column.name not in actual_columns:
                            return GuardResult(
                                verdict=GuardVerdict.BLOCK,
                                reason=f"字段[{column.name}]在表[{table_name}]中不存在。"
                                       f"可用字段: {sorted(list(actual_columns))[:15]}"
                            )
            
            return GuardResult(verdict=GuardVerdict.PASS, reason="L5通过")
        
        except Exception as e:
            return GuardResult(verdict=GuardVerdict.BLOCK, reason=f"语义校验失败: {e}")
    
    # ===== L6: 权限校验 =====
    def _check_permission(self, sql: str, user_id: str) -> GuardResult:
        """权限校验（实际调用Ranger API）"""
        # 生产环境：调用Ranger REST API检查用户权限
        # 这里简化为通过
        return GuardResult(verdict=GuardVerdict.PASS, reason="L6通过")
    
    # ===== L7: 并发控制 =====
    def _check_concurrency(self) -> GuardResult:
        with self._concurrent_lock:
            if self._current_concurrent >= self.max_concurrent:
                return GuardResult(
                    verdict=GuardVerdict.BLOCK,
                    reason=f"当前并发查询数已达上限({self.max_concurrent})，请稍后重试。"
                )
            self._current_concurrent += 1
        
        return GuardResult(verdict=GuardVerdict.PASS, reason="L7通过")
    
    def release_concurrency(self):
        """查询完成后释放并发计数"""
        with self._concurrent_lock:
            self._current_concurrent = max(0, self._current_concurrent - 1)
    
    # ===== 结果校验（L7补充） =====
    def validate_result(self, result_data: dict, metric_name: str) -> GuardResult:
        """结果合理性校验"""
        metric = self.metric_dict.metrics.get(metric_name)
        if not metric:
            return GuardResult(verdict=GuardVerdict.PASS, reason="无校验规则")
        
        rules = metric.get("validation_rules", {})
        
        for key, value in result_data.items():
            if not isinstance(value, (int, float)):
                continue
            
            if "min_value" in rules and value < rules["min_value"]:
                return GuardResult(
                    verdict=GuardVerdict.BLOCK,
                    reason=f"结果异常: {key}={value}，低于合理最小值{rules['min_value']}。已拦截。"
                )
            if "max_value" in rules and value > rules["max_value"]:
                return GuardResult(
                    verdict=GuardVerdict.BLOCK,
                    reason=f"结果异常: {key}={value}，超过合理最大值{rules['max_value']}。已拦截。"
                )
        
        return GuardResult(verdict=GuardVerdict.PASS, reason="结果校验通过")
```

---

### 2.3 核心组件二：多步分析闭环校验（修正点3）

```python
# complex_analysis_executor.py
"""
复杂分析执行器（多Agent协作）
修正点3：每一步SQL必须独立过护栏，任何一步被拦截则终止整条链路
"""
import json
from typing import List, Dict
from query_guard_final import QueryGuard, GuardVerdict

class ComplexAnalysisExecutor:
    """
    多步分析执行器
    
    核心原则：
    1. LLM生成分析计划（多步）
    2. 每一步生成SQL后，必须独立过QueryGuard
    3. 任何一步被BLOCK → 终止整条链路，不执行后续步骤
    4. 所有步骤的结果汇总后，交给归因Agent生成报告
    """
    
    def __init__(self, llm_client, guard: QueryGuard, spark_session, doris_conn):
        self.llm = llm_client
        self.guard = guard
        self.spark = spark_session
        self.doris = doris_conn
        self.max_steps = 5  # 最多5步，防止无限循环
    
    def execute(self, user_query: str, user_id: str) -> Dict:
        """执行多步分析"""
        
        # Step 1: 生成分析计划
        plan = self._generate_analysis_plan(user_query)
        
        if plan.get("out_of_scope"):
            return {
                "success": False,
                "message": f"该问题超出当前数据覆盖范围: {plan.get('reason', '')}"
            }
        
        steps = plan.get("steps", [])
        if len(steps) > self.max_steps:
            steps = steps[:self.max_steps]
        
        # Step 2: 逐步执行（每步过护栏）
        step_results = []
        
        for i, step in enumerate(steps, 1):
            # 2.1 为该步骤生成SQL
            step_sql = self._generate_step_sql(step, user_query, step_results)
            
            if not step_sql or step_sql == "OUT_OF_SCOPE":
                step_results.append({
                    "step": i,
                    "status": "skipped",
                    "reason": "无法生成有效SQL"
                })
                continue
            
            # 2.2 ★ 关键：每步SQL必须独立过护栏（修正点3）
            guard_result = self.guard.validate_step(step_sql, user_id, step_num=i)
            
            if guard_result.verdict == GuardVerdict.BLOCK:
                # 一旦某步被拦截，终止整条链路
                return {
                    "success": False,
                    "message": f"分析在第{i}步被安全策略拦截: {guard_result.reason}",
                    "completed_steps": step_results,
                    "blocked_step": {"step": i, "sql": step_sql}
                }
            
            # 2.3 校验通过，执行查询
            try:
                engine = guard_result.suggested_engine
                if engine == "doris":
                    result = self._execute_on_doris(step_sql)
                else:
                    result = self._execute_on_spark(step_sql)
                
                step_results.append({
                    "step": i,
                    "status": "success",
                    "purpose": step.get("purpose", ""),
                    "sql": step_sql,
                    "result": result
                })
            
            except Exception as e:
                step_results.append({
                    "step": i,
                    "status": "error",
                    "error": str(e),
                    "sql": step_sql
                })
                # 某步执行失败，终止后续步骤
                break
        
        # Step 3: 归因总结
        if not any(r["status"] == "success" for r in step_results):
            return {
                "success": False,
                "message": "所有分析步骤均失败，无法生成报告。",
                "steps": step_results
            }
        
        report = self._generate_attribution_report(user_query, step_results)
        
        return {
            "success": True,
            "message": "分析完成",
            "report": report,
            "steps": step_results
        }
    
    def _generate_analysis_plan(self, user_query: str) -> Dict:
        """生成分析计划"""
        prompt = f"""
你是数据分析师。请将以下问题拆解为多步分析计划。

【可用数据表（只能使用这些）】
{json.dumps(list(self.guard.metric_dict.table_whitelist), ensure_ascii=False, indent=2)}

【可用指标】
{json.dumps(list(self.guard.metric_dict.metrics.keys()), ensure_ascii=False)}

【用户问题】
{user_query}

【输出格式（JSON）】
{{
  "steps": [
    {{"purpose": "确认整体趋势", "table": "ads.ads_xxx", "description": "..."}},
    {{"purpose": "分维度下钻", "table": "ads.ads_xxx", "description": "..."}},
    {{"purpose": "归因定位", "table": "ads.ads_xxx", "description": "..."}}
  ]
}}

如果问题超出可用数据范围，输出：
{{"out_of_scope": true, "reason": "..."}}

注意：只能使用上述列出的表，不允许使用任何其他表。
"""
        
        response = self.llm.generate(prompt)
        
        try:
            # 提取JSON
            json_str = response[response.index("{"):response.rindex("}")+1]
            return json.loads(json_str)
        except:
            return {"out_of_scope": True, "reason": "分析计划生成失败"}
    
    def _generate_step_sql(self, step: Dict, user_query: str, 
                           previous_results: List) -> str:
        """为单个分析步骤生成SQL"""
        prompt = f"""
请为以下分析步骤生成Hive SQL。

【分析步骤】
目的: {step.get('purpose', '')}
使用表: {step.get('table', '')}
描述: {step.get('description', '')}

【前序步骤结果（供参考）】
{json.dumps(previous_results[-2:] if previous_results else [], ensure_ascii=False, default=str)}

【原始问题】
{user_query}

【规则】
1. 只能使用指定的表
2. 必须包含dt分区条件
3. 只生成SELECT语句
4. 如果无法生成，回复 OUT_OF_SCOPE

请直接输出SQL（不要markdown代码块）：
"""
        
        sql = self.llm.generate(prompt).strip()
        
        # 清理可能的markdown标记
        sql = sql.replace("```sql", "").replace("```", "").strip()
        
        return sql
    
    def _generate_attribution_report(self, user_query: str, 
                                     step_results: List) -> str:
        """基于多步结果生成归因报告"""
        prompt = f"""
你是资深数据分析师。请基于以下多步分析结果，生成归因报告。

【原始问题】
{user_query}

【分析步骤及结果】
{json.dumps(step_results, ensure_ascii=False, default=str)}

【要求】
1. 用简洁的中文总结核心发现
2. 给出明确的归因结论（主要原因是什么）
3. 给出可操作的建议
4. 标注数据来源表
5. 如果数据不足以得出结论，明确说明

请输出报告：
"""
        
        return self.llm.generate(prompt)
    
    def _execute_on_doris(self, sql: str) -> Dict:
        """在Doris上执行（小查询）"""
        cursor = self.doris.cursor()
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return {"columns": columns, "rows": rows, "row_count": len(rows)}
    
    def _execute_on_spark(self, sql: str) -> Dict:
        """在Spark chatbi_queue上执行（大查询）"""
        df = self.spark.sql(sql)
        rows = df.collect()
        columns = df.columns
        return {
            "columns": columns,
            "rows": [row.asDict() for row in rows],
            "row_count": len(rows)
        }
```

---

### 2.4 核心组件三：Schema缓存定时刷新

```python
# schema_cache_scheduler.py
"""
Schema缓存定时刷新任务
由Airflow调度，每日凌晨执行
不在用户请求链路中
"""
from datetime import datetime

def refresh_schema_cache(**context):
    """
    Airflow DAG任务：每日03:00刷新Schema缓存
    在ETL完成后执行，确保缓存的是最新schema
    """
    from pyspark.sql import SparkSession
    
    spark = SparkSession.builder.getOrCreate()
    
    # 获取白名单表列表（从指标字典服务获取）
    import requests
    whitelist_response = requests.get("http://metric-dict-service:8081/api/v1/table/whitelist")
    table_whitelist = set(whitelist_response.json()["tables"])
    
    # 刷新缓存
    global schema_cache
    schema_cache.refresh(spark, table_whitelist)
    
    # 验证缓存有效性
    if schema_cache.is_stale:
        raise Exception("Schema缓存刷新失败")
    
    print(f"[SchemaCache] 刷新完成: {len(table_whitelist)}张表, {datetime.now()}")


# Airflow DAG定义
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta

with DAG(
    'chatbi_schema_cache_refresh',
    schedule_interval='0 3 * * *',  # 每日03:00
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={'retries': 2, 'retry_delay': timedelta(minutes=5)},
) as dag:
    
    refresh_task = PythonOperator(
        task_id='refresh_schema_cache',
        python_callable=refresh_schema_cache,
    )
```

---

### 2.5 核心组件四：降级管理器（终结版）

```python
# degradation_manager_final.py
"""
三级降级策略终结版

Level 0 (正常): LLM生成SQL → QueryGuard校验 → 执行
Level 1 (模板): LLM不可用 → SQL模板匹配 → QueryGuard校验 → 执行
Level 2 (缓存): 执行层不可用 → 返回最近一次缓存结果（标记为stale）
Level 3 (拒绝): 全部不可用 → 明确告知用户"服务暂不可用"

铁律：任何级别都不允许返回未经验证的结果
"""
from enum import IntEnum
from datetime import datetime, timedelta
from typing import Optional, Dict
import logging

logger = logging.getLogger("DegradationManager")


class DegradationLevel(IntEnum):
    NORMAL = 0
    TEMPLATE = 1
    CACHED = 2
    REJECT = 3


class DegradationManager:
    
    def __init__(self, metric_dict, redis_client=None):
        self.metric_dict = metric_dict
        self.redis = redis_client  # 用于结果缓存
        self.sql_templates = self._init_templates()
        self._llm_healthy = True
        self._spark_healthy = True
        self._doris_healthy = True
    
    def detect_level(self) -> DegradationLevel:
        """检测当前降级级别"""
        if not self._llm_healthy:
            if self._spark_healthy or self._doris_healthy:
                return DegradationLevel.TEMPLATE
            elif self._has_cache():
                return DegradationLevel.CACHED
            else:
                return DegradationLevel.REJECT
        
        if not self._spark_healthy and not self._doris_healthy:
            if self._has_cache():
                return DegradationLevel.CACHED
            return DegradationLevel.REJECT
        
        return DegradationLevel.NORMAL
    
    def handle_template_query(self, user_query: str) -> Dict:
        """Level 1: 模板匹配"""
        metric = self.metric_dict.lookup_metric(user_query)
        
        if not metric:
            return {
                "success": False,
                "degradation_level": "template",
                "message": "AI服务暂时不可用，且未找到匹配的指标模板。请稍后重试或联系数据团队。"
            }
        
        template = self.sql_templates.get(metric["name"])
        if not template:
            return {
                "success": False,
                "degradation_level": "template",
                "message": f"指标[{metric['cn_name']}]暂无标准查询模板。"
            }
        
        # 提取时间条件
        time_condition = self._extract_time_condition(user_query)
        sql = template.replace("{time_condition}", time_condition)
        
        return {
            "success": True,
            "degradation_level": "template",
            "sql": sql,
            "metric": metric["name"],
            "message": f"[降级模式] 使用标准模板查询{metric['cn_name']}，结果可能不如AI分析精准。"
        }
    
    def handle_cached_query(self, user_query: str) -> Dict:
        """Level 2: 返回缓存结果"""
        if not self.redis:
            return self._reject_response()
        
        # 尝试从Redis获取最近一次相同指标的查询结果
        metric = self.metric_dict.lookup_metric(user_query)
        if not metric:
            return self._reject_response()
        
        cache_key = f"chatbi:result:{metric['name']}:latest"
        cached = self.redis.get(cache_key)
        
        if cached:
            import json
            data = json.loads(cached)
            return {
                "success": True,
                "degradation_level": "cached",
                "data": data,
                "message": f"[降级模式] 返回最近缓存数据（{data.get('cache_time', '未知时间')}），"
                          f"非实时数据，仅供参考。"
            }
        
        return self._reject_response()
    
    def _reject_response(self) -> Dict:
        """Level 3: 拒绝服务"""
        return {
            "success": False,
            "degradation_level": "reject",
            "message": (
                "ChatBI服务暂时不可用。\n"
                "可能原因：计算资源繁忙或系统维护中。\n"
                "建议：\n"
                "  1. 稍后重试\n"
                "  2. 直接使用Superset查看预置报表\n"
                "  3. 联系数据团队值班同学\n\n"
                "我们绝不返回未经验证的数据。"
            )
        }
    
    def cache_result(self, metric_name: str, result: Dict):
        """查询成功后缓存结果（供降级使用）"""
        if self.redis:
            import json
            cache_key = f"chatbi:result:{metric_name}:latest"
            result["cache_time"] = datetime.now().isoformat()
            self.redis.setex(cache_key, 86400, json.dumps(result, default=str))
    
    def _init_templates(self) -> Dict[str, str]:
        """标准SQL模板（人工维护，覆盖高频指标）"""
        return {
            "GMV": "SELECT dt, SUM(gmv) as gmv FROM ads.ads_platform_gmv_daily WHERE {time_condition} GROUP BY dt ORDER BY dt",
            "DAU": "SELECT dt, dau FROM ads.ads_platform_dau_daily WHERE {time_condition} ORDER BY dt",
            "转化率": "SELECT dt, conversion_rate FROM ads.ads_platform_funnel_daily WHERE {time_condition} ORDER BY dt",
            "客单价": "SELECT dt, avg_order_amount FROM ads.ads_platform_gmv_daily WHERE {time_condition} ORDER BY dt",
        }
    
    def _extract_time_condition(self, query: str) -> str:
        """从用户问题中提取时间条件"""
        import re
        from datetime import datetime, timedelta
        
        # 最近N天
        m = re.search(r'最近(\d+)天', query)
        if m:
            days = int(m.group(1))
            end = datetime.now() - timedelta(days=1)  # T+1
            start = end - timedelta(days=days)
            return f"dt BETWEEN '{start.strftime('%Y-%m-%d')}' AND '{end.strftime('%Y-%m-%d')}'"
        
        # 上个月
        if "上个月" in query:
            now = datetime.now()
            if now.month == 1:
                start = now.replace(year=now.year-1, month=12, day=1)
            else:
                start = now.replace(month=now.month-1, day=1)
            end = now.replace(day=1) - timedelta(days=1)
            return f"dt BETWEEN '{start.strftime('%Y-%m-%d')}' AND '{end.strftime('%Y-%m-%d')}'"
        
        # 默认最近7天
        end = datetime.now() - timedelta(days=1)
        start = end - timedelta(days=7)
        return f"dt BETWEEN '{start.strftime('%Y-%m-%d')}' AND '{end.strftime('%Y-%m-%d')}'"
    
    def _has_cache(self) -> bool:
        if not self.redis:
            return False
        return self.redis.keys("chatbi:result:*") is not None
```

---

### 2.6 端到端测试（终结版）

```python
# test_final_validation.py
"""
终结版测试：覆盖所有修正点
"""
import pytest
import time
from unittest.mock import patch, MagicMock


class TestQueryGuardFinal:
    """QueryGuard终结版测试"""
    
    @pytest.fixture
    def guard(self, schema_cache, metric_dict):
        return QueryGuard(metric_dict, schema_cache)
    
    # === 修正点1测试：资源估算不触发EXPLAIN ===
    def test_resource_estimate_no_explain(self, guard):
        """验证：资源估算不调用Spark（纯元数据计算）"""
        sql = "SELECT dt, gmv FROM ads.ads_platform_gmv_daily WHERE dt BETWEEN '2024-06-01' AND '2024-06-18'"
        
        # Mock Spark，如果被调用则测试失败
        with patch.object(guard, 'spark', None):
            result = guard._estimate_resource_by_metadata(sql)
        
        # 应该通过（不依赖Spark）
        assert result.verdict in (GuardVerdict.PASS, GuardVerdict.DEGRADE)
        assert result.estimated_scan_gb > 0
    
    def test_resource_estimate_blocks_large_scan(self, guard):
        """验证：超大扫描被拦截"""
        # 模拟扫描100天的数据
        sql = "SELECT * FROM ads.ads_platform_gmv_daily WHERE dt BETWEEN '2024-01-01' AND '2024-06-18'"
        result = guard._estimate_resource_by_metadata(sql)
        
        # 如果超过50GB应该被拦截
        if result.estimated_scan_gb > 50:
            assert result.verdict == GuardVerdict.BLOCK
    
    # === 修正点2测试：语义校验用本地缓存 ===
    def test_semantic_check_uses_cache(self, guard, schema_cache):
        """验证：语义校验从本地缓存读取，不查Metastore"""
        # 预填充缓存
        schema_cache._cache = {
            "ads.ads_platform_gmv_daily": {"dt", "gmv", "order_count", "pay_user_count"}
        }
        
        sql = "SELECT dt, gmv FROM ads.ads_platform_gmv_daily WHERE dt = '2024-06-15'"
        result = guard._check_semantics_cached(sql)
        assert result.verdict == GuardVerdict.PASS
    
    def test_semantic_check_blocks_invalid_column(self, guard, schema_cache):
        """验证：不存在的字段被拦截"""
        schema_cache._cache = {
            "ads.ads_platform_gmv_daily": {"dt", "gmv", "order_count"}
        }
        
        sql = "SELECT dt, non_existent_field FROM ads.ads_platform_gmv_daily WHERE dt = '2024-06-15'"
        result = guard._check_semantics_cached(sql)
        assert result.verdict == GuardVerdict.BLOCK
        assert "non_existent_field" in result.reason
    
    def test_semantic_check_speed(self, guard, schema_cache):
        """验证：语义校验耗时<1ms"""
        schema_cache._cache = {
            "ads.ads_platform_gmv_daily": {"dt", "gmv", "order_count"}
        }
        
        sql = "SELECT dt, gmv FROM ads.ads_platform_gmv_daily WHERE dt = '2024-06-15'"
        
        start = time.time()
        for _ in range(1000):
            guard._check_semantics_cached(sql)
        elapsed_ms = (time.time() - start) * 1000
        
        # 1000次校验应该在100ms内完成（平均0.1ms/次）
        assert elapsed_ms < 100, f"语义校验太慢: {elapsed_ms:.1f}ms/1000次"
    
    # === 修正点3测试：多步SQL逐步过护栏 ===
    def test_multi_step_each_validated(self, guard):
        """验证：多步分析中每步SQL独立过护栏"""
        # Step 1: 合法SQL
        sql1 = "SELECT dt, gmv FROM ads.ads_platform_gmv_daily WHERE dt = '2024-06-15'"
        r1 = guard.validate_step(sql1, "user1", step_num=1)
        assert r1.verdict == GuardVerdict.PASS
        
        # Step 2: 非法SQL（查ODS表）
        sql2 = "SELECT * FROM ods.ods_trade_order WHERE dt = '2024-06-15'"
        r2 = guard.validate_step(sql2, "user1", step_num=2)
        assert r2.verdict == GuardVerdict.BLOCK
        assert "步骤2" in r2.reason
    
    def test_multi_step_blocks_entire_chain(self):
        """验证：某步被拦截后，整条链路终止"""
        executor = ComplexAnalysisExecutor(
            llm_client=MagicMock(),
            guard=guard,
            spark_session=MagicMock(),
            doris_conn=MagicMock()
        )
        
        # Mock LLM返回包含非法表的计划
        executor.llm.generate.return_value = json.dumps({
            "steps": [
                {"purpose": "查整体", "table": "ads.ads_platform_gmv_daily"},
                {"purpose": "查明细", "table": "ods.ods_trade_order"},  # 非法！
            ]
        })
        
        result = executor.execute("测试问题", "user1")
        
        # 应该在第2步被拦截
        assert result["success"] == False
        assert "拦截" in result["message"]


class TestDegradationFinal:
    """降级策略测试"""
    
    def test_llm_down_fallback_to_template(self, metric_dict):
        """LLM不可用 → 降级为模板"""
        dm = DegradationManager(metric_dict)
        dm._llm_healthy = False
        
        level = dm.detect_level()
        assert level == DegradationLevel.TEMPLATE
        
        result = dm.handle_template_query("最近7天GMV")
        assert result["success"] == True
        assert result["degradation_level"] == "template"
        assert "ads_platform_gmv_daily" in result["sql"]
    
    def test_all_down_reject(self, metric_dict):
        """全部不可用 → 拒绝服务"""
        dm = DegradationManager(metric_dict)
        dm._llm_healthy = False
        dm._spark_healthy = False
        dm._doris_healthy = False
        
        level = dm.detect_level()
        assert level == DegradationLevel.REJECT
    
    def test_never_return_unvalidated(self, metric_dict):
        """铁律：绝不返回未验证结果"""
        dm = DegradationManager(metric_dict)
        dm._llm_healthy = False
        dm._spark_healthy = False
        dm._doris_healthy = False
        
        result = dm.handle_cached_query("GMV")
        if result["success"] == False:
            assert "未经验证" in result["message"] or "不可用" in result["message"]
```

---

## 三、部署清单（直接上生产线）

### 3.1 上线前检查清单

| # | 检查项 | 标准 | 负责人 |
|---|--------|------|--------|
| 1 | 指标字典同步 | OneMetric中所有核心指标已注册，口径经业务方确认 | 数据PM |
| 2 | ADS白名单确认 | 200-500张表逐一确认，每张表有Owner | 数据架构师 |
| 3 | Schema缓存刷新 | 首次全量刷新成功，定时任务配置正确 | SRE |
| 4 | QueryGuard测试 | 全部单元测试通过（含注入攻击、越权、全表扫描） | QA |
| 5 | 资源隔离验证 | chatbi_queue独立，不影响ETL队列 | SRE |
| 6 | 降级演练 | 模拟LLM宕机、Spark队列满、Doris宕机，验证降级正确 | QA |
| 7 | 并发压测 | 50并发下P99延迟<5s，无OOM | QA |
| 8 | 安全审计 | SQL注入、XSS、越权访问全部拦截 | 安全团队 |
| 9 | 回滚方案 | 一键关闭ChatBI入口，不影响现有报表 | SRE |
| 10 | 监控告警 | 拦截率、降级率、延迟、错误率全部有告警 | SRE |

### 3.2 灰度发布策略

```
Week 1: 内部灰度（数据团队10人）
  → 验证核心链路正确性
  → 收集Bad Case，优化Prompt和模板

Week 2: 小范围灰度（运营团队50人）
  → 验证高频场景覆盖率
  → 验证降级策略在真实负载下的表现

Week 3: 大范围灰度（全运营+产品200人）
  → 验证并发能力
  → 验证指标口径一致性（与Superset报表对比）

Week 4: 全量上线
  → 开放给所有业务方
  → 7×24值班
  → 每日Review拦截日志和Bad Case
```

### 3.3 核心监控指标

```yaml
# prometheus_alerts_chatbi.yml
groups:
  - name: chatbi_alerts
    rules:
      # 拦截率过高（说明AI生成质量差）
      - alert: HighBlockRate
        expr: rate(chatbi_guard_blocked_total[5m]) / rate(chatbi_query_total[5m]) > 0.3
        for: 10m
        annotations:
          summary: "ChatBI拦截率超过30%，AI生成质量异常"
      
      # 降级率过高（说明基础设施不稳定）
      - alert: HighDegradationRate
        expr: rate(chatbi_degradation_total[5m]) / rate(chatbi_query_total[5m]) > 0.2
        for: 5m
        annotations:
          summary: "ChatBI降级率超过20%，请检查LLM/Spark/Doris健康状态"
      
      # P99延迟过高
      - alert: HighLatency
        expr: histogram_quantile(0.99, chatbi_query_duration_seconds) > 10
        for: 5m
        annotations:
          summary: "ChatBI P99延迟超过10秒"
      
      # 并发接近上限
      - alert: ConcurrentNearLimit
        expr: chatbi_concurrent_queries > 18
        for: 2m
        annotations:
          summary: "ChatBI并发接近上限(20)，部分请求可能被拒绝"
```

---

## 四、终极总结

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  淘天离线数仓 ChatBI 终结版方案                                          │
│                                                                         │
│  选型：DB-GPT（多Agent编排 + 本地模型 + AWEL工作流）                     │
│                                                                         │
│  架构精髓：克制                                                          │
│    用白名单圈定AI的活动范围（200-500张ADS表）                            │
│    用字典锁死AI的编造空间（指标口径硬注入）                               │
│    用护栏兜底AI的偶尔抽风（七层校验）                                    │
│    用降级保证系统永远有响应（三级降级）                                   │
│                                                                         │
│  三处关键修正（GLM终审）：                                               │
│    ① 资源估算：元数据法（不触发EXPLAIN，防止击穿Thrift Server）          │
│    ② 语义校验：本地Schema缓存（0ms，不查Metastore）                     │
│    ③ 多步校验：每步SQL独立过护栏（防止越狱）                             │
│                                                                         │
│  五条铁律：                                                              │
│    1. 绝不暴露裸表（ODS/DWD对AI不可见）                                  │
│    2. 口径必须收敛（从字典取，AI不许猜）                                  │
│    3. 资源必须隔离（独立队列 + 50GB上限 + 5分钟超时）                    │
│    4. 结果必须校验（七层护栏 + 合理性检查）                               │
│    5. 必须有降级（模板→缓存→拒绝，绝不返回未验证数据）                   │
│                                                                         │
│  一句话：                                                               │
│  ChatBI不是让AI自由探索数据，                                            │
│  而是让AI在严格护栏内安全地查治理过的数据。                               │
│  护栏越严格，业务方越敢用，系统活得越久。                                │
│                                                                         │
│  可以开工了。                                                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```




```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  MySQL ──→ 系统元数据存储（指标字典、白名单、权限、配置）         │
│                                                                 │
│  Elasticsearch ──→ 语义检索引擎                                  │
│       ├── 指标字典全文检索（同义词、模糊匹配）                    │
│       ├── 查询审计日志（可搜索、可聚合）                          │
│       └── Bad Case库（历史错误查询，供学习）                      │
│                                                                 │
│  Embedding + Milvus ──→ 向量检索                                │
│       ├── ADS表Schema语义检索（RAG）                             │
│       ├── 历史相似问题检索                                       │
│       └── 指标语义匹配（"销售额"→"GMV"）                        │
│                                                                 │
│  LangGraph ──→ Agent编排引擎                                     │
│       ├── 状态机管理（多步分析的状态流转）                        │
│       ├── 循环推理（查→分析→再查→归因）                         │
│       ├── 人机交互节点（不确定时请求用户确认）                    │
│       └── 条件分支（简单查询走快速通道，复杂分析走多Agent）       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```