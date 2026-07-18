# AI DataWorks — 部署运维与使用注意事项

## 一、部署架构

### 1.1 生产环境拓扑

```
┌─────────────────────────────────────────────────────────────────────┐
│                          负载均衡 (Nginx/ALB)                        │
│                         HTTPS:443 → API:8000                        │
└─────────────────────────────────────────────────────────────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            ▼                       ▼                       ▼
┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐
│   API Server 1    │   │   API Server 2    │   │   API Server 3    │
│   FastAPI:8000    │   │   FastAPI:8000    │   │   FastAPI:8000    │
│   4 CPU / 8 GB    │   │   4 CPU / 8 GB    │   │   4 CPU / 8 GB    │
└───────────────────┘   └───────────────────┘   └───────────────────┘
            │                       │                       │
            └───────────────────────┼───────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│  PostgreSQL   │         │    Redis      │         │   Milvus      │
│  语义层存储    │         │  查询缓存      │         │  向量检索      │
│  16C/64G/1TB  │         │  8C/32G/64G  │         │  8C/32G/512G │
└───────────────┘         └───────────────┘         └───────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         数据查询引擎集群                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │ ClickHouse   │  │  StarRocks   │  │    Hive      │               │
│  │ (实时分析)    │  │ (高并发 OLAP) │  │ (离线批处理)  │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Docker Compose 开发部署

```yaml
# docker-compose.yml
version: "3.9"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://dataworks:xxx@postgres:5432/dataworks
      - REDIS_URL=redis://redis:6379/0
      - CLICKHOUSE_URL=clickhouse://clickhouse:9000
      - MILVUS_HOST=milvus
      - LLM_API_KEY=${DEEPSEEK_API_KEY}
      - LLM_BASE_URL=${LLM_BASE_URL:-https://api.deepseek.com}
    depends_on:
      - postgres
      - redis
      - milvus
    volumes:
      - ./config/semantic:/app/config/semantic  # 语义层定义热加载
    restart: unless-stopped

  worker:
    build: .
    command: temporal-worker
    environment:
      - TEMPORAL_HOST=temporal:7233
    depends_on:
      - temporal
    restart: unless-stopped

  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: dataworks
      POSTGRES_USER: dataworks
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pg_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  milvus:
    image: milvusdb/milvus:v2.4.0
    ports:
      - "19530:19530"
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
    depends_on:
      - etcd
      - minio
    volumes:
      - milvus_data:/var/lib/milvus

  temporal:
    image: temporalio/auto-setup:1.22
    ports:
      - "7233:7233"
    environment:
      - DB=postgres12
      - DB_PORT=5432
      - POSTGRES_USER=temporal
      - POSTGRES_PWD=${TEMPORAL_PASSWORD}
      - POSTGRES_SEEDS=postgres
    depends_on:
      - postgres

volumes:
  pg_data:
  redis_data:
  milvus_data:
```

---

## 二、语义层治理规范

### 2.1 指标注册审查清单

每条指标定义合入前必须通过以下检查：

- [ ] **命名唯一性**：指标名在全域唯一，不与已有指标冲突
- [ ] **别名完备性**：至少列出 3 个以上业务常用别名
- [ ] **描述清晰性**：用业务语言写清计算口径，非技术人员可理解
- [ ] **物理映射正确**：`table.column` 在目标数据库中确实存在
- [ ] **过滤条件声明**：`order_status = 'paid'` 等默认过滤明确写出
- [ ] **维度关联**：列出该指标可与哪些维度组合查询
- [ ] **Owner 明确**：指定维护团队/个人
- [ ] **SLA 标注**：数据产出时间（T+1 8:00 等）
- [ ] **示例查询**：至少提供 1 个常见查询示例
- [ ] **口径变更记录**：若修改计算口径，保留历史版本的变更说明

### 2.2 维度定义规范

- [ ] **层级完备**：有层级的维度（如地区：国家→省→市）必须标注完整层级
- [ ] **JOIN 路径正确**：from_table.from_column → to_table.to_column 能被实际执行
- [ ] **基数标注**：标注维度基数（实际值），帮助优化器选择策略
- [ ] **允许的操作符**：声明 `=`, `IN`, `LIKE` 等可用操作符

### 2.3 术语词典维护

新业务术语加入流程：

```
业务方提交术语定义 → 数据架构师审核 → 技术验证 → 合入术语词典 → 通知相关方
```

---

## 三、安全配置

### 3.1 权限模型

```yaml
# 权限模型：RBAC + 数据级权限
roles:
  admin:
    - can_manage_metrics
    - can_manage_dimensions
    - can_manage_users
    - can_view_audit_log
    - can_override_permission  # 超级管理员可越权查看（记录审计日志）
  
  data_analyst:
    - can_query_data
    - can_create_chart
    - can_save_report
    - can_view_lineage
    - data_scope: team_level    # 只能看自己团队的数据
  
  business_user:
    - can_query_data
    - can_create_chart
    - data_scope: self_level    # 只能看自己有权限的数据
  
  viewer:
    - can_view_dashboard
    - can_export_report
    - data_scope: public_only   # 只能看公开数据
```

### 3.2 SQL 安全规则

```python
# core/security/auditor.py 核心规则
SECURITY_RULES = [
    # 规则1：禁止 DML / DDL 操作
    {
        "name": "ban_write_operations",
        "check": lambda sql: not any(
            kw in sql.upper()
            for kw in ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER",
                       "CREATE", "TRUNCATE", "GRANT", "REVOKE"]
        ),
        "action": "reject",
        "message": "仅允许只读查询（SELECT）",
    },
    
    # 规则2：强制 LIMIT 检查
    {
        "name": "force_limit",
        "check": lambda sql: "LIMIT" in sql.upper(),
        "action": "auto_fix",   # 自动添加 LIMIT 1000
    },
    
    # 规则3：敏感表访问控制
    {
        "name": "sensitive_table_access",
        "check": lambda sql, user: not any(
            table in sql for table in user.restricted_tables
        ),
        "action": "reject",
        "message": "您没有访问该数据表的权限",
    },
    
    # 规则4：行级安全 —— 自动注入 org_id 过滤
    {
        "name": "row_level_security",
        "check": lambda sql, user: True,
        "action": "auto_inject",  # WHERE org_id = user.org_id
        "inject": lambda sql, user: inject_org_filter(sql, user.org_id),
    },
    
    # 规则5：超时保护
    {
        "name": "query_timeout",
        "check": lambda sql: "SETTINGS max_execution_time" not in sql,
        "action": "auto_inject",
        "inject": lambda sql: sql + "\nSETTINGS max_execution_time = 300",
    },
]
```

### 3.3 数据脱敏

```python
# 自动脱敏规则
MASKING_RULES = [
    {
        "column_pattern": r".*phone.*",
        "mask": lambda v: v[:3] + "****" + v[-4:] if v else v,
    },
    {
        "column_pattern": r".*id_card.*|.*身份证.*",
        "mask": lambda v: v[:3] + "****" + v[-4:] if v else v,
    },
    {
        "column_pattern": r".*bank_account.*|.*银行卡.*",
        "mask": lambda v: "****" + v[-4:] if v else v,
    },
    {
        "column_pattern": r".*email.*",
        "mask": lambda v: v.split("@")[0][:2] + "***@" + v.split("@")[1] if v else v,
    },
]
```

---

## 四、使用注意事项

### 4.1 语义层建设的"先做后跑"原则

| 阶段 | 做什么 | 为什么不跳过 |
|------|--------|-------------|
| **Phase 1: 核心指标** | 定义 Top 20 高频指标（GMV、DAU、订单量…） | 覆盖 80% 日常查询 |
| **Phase 2: 常用维度** | 时间、地区、渠道、平台、品类 | 支撑多维分析 |
| **Phase 3: 高级指标** | 转化率、复购率、LTV、留存率 | 支撑深度分析 |
| **Phase 4: 术语词典** | 业务黑话映射 | 降低 LLM 理解偏差 |

**关键数据**：语义层覆盖率达到 80% 时，AI 查询准确率才能稳定 > 90%。

### 4.2 使用中的"三个不"

1. **不要在未验证语义层之前用于生产决策** — 每个指标和维度必须先通过一致性检查（表存在、列存在、JOIN 路径正确）
2. **不要跳过置信度判断** — 当系统标记 `recommendation: "review"` 时，请人工复核；标记 `"reject"` 时，一定不要使用该结果
3. **不要在语义层不覆盖的领域期待准确回答** — 语义层没覆盖的表/字段，AI 会自行"猜测"，幻觉风险极高

### 4.3 常见失败模式与应对

| 失败模式 | 原因 | 应对 |
|---------|------|------|
| "查询结果看起来不对" | 指标口径理解偏差 | 在语义层中增加更详细的指标描述 |
| "这个维度怎么查不了" | 维度未注册 JOIN 路径 | 在维度定义中补全 join_path |
| "时间范围总是不对" | 模糊时间未正确解析 | 使用精确日期，或在术语词典中增加时间映射 |
| "数据量和 BI 报表不一致" | 分区/快照时间不同 | 检查指标 SLA 标注是否正确 |
| "查询太慢了" | 大表全表扫描 | 在语义层增加分区字段、设置时间范围强制要求 |

### 4.4 迭代优化循环

```
用户反馈 → Bad Case 收集 → 根因分析 → 语义层增强 → 回归测试 → 上线验证
   ↑                                                                    ↓
   └──────────────────── 持续改进闭环 ──────────────────────────────────┘
```

**根因分类**：
- 语义层缺失（50%）→ 补指标/维度/术语定义
- LLM 理解偏差（20%）→ 优化 Prompt 或增强别名
- 时间解析错误（15%）→ 补时间模板或术语映射
- SQL 方言不兼容（10%）→ 增强方言适配器
- 数据质量问题（5%）→ 反馈数仓团队

---

## 五、SLA 与监控

### 5.1 服务 SLA

| 指标 | Target | 告警阈值 |
|------|--------|---------|
| API P99 延迟 | < 5s | > 10s |
| SQL 生成成功率 | > 95% | < 90% |
| 语义解析准确率 | > 92% | < 85% |
| 查询可用率 | > 99.5% | < 99% |
| LLM 调用成功率 | > 99.9% | < 99.5% |

### 5.2 核心监控指标

```python
# Prometheus 指标
ai_query_duration_seconds          # 查询总耗时
ai_query_semantic_resolution_seconds  # 语义解析耗时
ai_query_sql_compilation_seconds      # SQL 编译耗时
ai_query_llm_call_seconds             # LLM 调用耗时
ai_query_confidence_ratio             # 置信度分布
ai_query_error_total                  # 错误计数
ai_semantic_coverage_ratio            # 语义层覆盖率
ai_query_cost_dollars_total           # LLM 调用成本
```

### 5.3 告警规则

```yaml
alerts:
  - name: HighErrorRate
    expr: rate(ai_query_error_total[5m]) > 0.1
    severity: critical
    message: "AI 查询错误率超过 10%"
    
  - name: HighLatency
    expr: histogram_quantile(0.99, ai_query_duration_seconds) > 10
    severity: warning
    message: "P99 延迟超过 10s"
    
  - name: LowConfidence
    expr: avg(ai_query_confidence_ratio) < 0.7
    severity: warning
    message: "平均置信度低于 0.7"
    
  - name: LLMCostSpike
    expr: rate(ai_query_cost_dollars_total[1h]) > 100
    severity: warning
    message: "LLM 调用成本突增"
```

---

## 六、FAQ

**Q: 多租户环境下如何隔离数据？**
A: 通过 `org_id` 行级安全过滤 + 指标/维度权限控制。每个查询编译时自动注入 `WHERE org_id = current_user.org_id`。

**Q: 如何处理同一个指标在不同部门有不同口径？**
A: 支持命名空间隔离：`sales.gmv`（销售口径，含退款）vs `finance.gmv`（财务口径，不含税）。用户查询时根据其部门自动匹配。

**Q: SQL 方言差异怎么处理？**
A: sqlglot 支持 20+ 方言转换。编译器生成标准 SQL 后自动转目标方言。ClickHouse↔Hive↔StarRocks 之间有完整映射。

**Q: 系统如何避免"一本正经地胡说八道"？**
A: 三层防线：①语义层提供确定性映射（LLM 不参与 SQL 生成）②多级自动验证（语法/结果/趋势）③置信度评分 < 0.7 自动拒答并提示人工复核。

**Q: 语义层建设需要多久？**
A: 核心 20 个指标 + 6 个维度 ≈ 2-3 周即可覆盖 80% 日常查询。完整 100+ 指标建设约 3-6 个月。
