# 数仓里用 SparkSQL 还是手写 RDD 算子？—— 字节大数据架构师 2026 落地实践

> **核心结论：能用 SQL 的必须用 SQL，需要手写的场景有且仅有四类。在字节跳动的数仓体系里，SparkSQL（含 DataFrame DSL）占比 >90%，手写 RDD 的场景 <3%，其余是 PySpark UDF / Java UDAF 等混合模式。下面拆开讲。**

---

## 一、先纠正一个常见误区

**这个讨论在 2026 年不应该是"SparkSQL vs RDD"，而应该是"SparkSQL vs DataFrame API vs RDD"。**

RDD（Resilient Distributed Dataset）是 Spark 1.x 时代的底层抽象。如今我们真正讨论的"手写算子"，绝大多数场景指的是 **DataFrame / Dataset API**（即类型安全的、带 Schema 的编程接口），而不是裸 RDD。纯 RDD 编程在数仓场景中已经极少出现——除非你还在维护 2018 年以前的老作业。

| 抽象层级 | 序列化 | Catalyst 优化器 | Tungsten 全阶段代码生成 | 适用场景 |
|---------|--------|----------------|----------------------|---------|
| **SparkSQL** | Encoder（堆外） | ✅ 完整参与 | ✅ | 标准 SQL 语义的 ETL / 聚合 / 窗口 / Join |
| **DataFrame API** | Encoder（堆外） | ✅ 完整参与 | ✅ | SQL 难以表达的复杂逻辑，但不涉及自定义类型 |
| **Dataset API** | Encoder（堆外） | ✅ 部分 | ✅ 部分 | 需强类型 + Lambda 但保持优化的场景 |
| **RDD** | Java/Kryo（堆内） | ❌ 完全不参与 | ❌ 完全不参与 | 非结构化数据、自定义分区、迭代计算 |

**RDD 的最大代价不是写法啰嗦，而是它完全绕过了 Catalyst 优化器和 Tungsten 执行引擎。** 同样的逻辑，RDD 版本通常是 SQL/DataFrame 版本的 3~10 倍慢，且 GC 压力更大。

---

## 二、SparkSQL 压倒性占比的原因——不是政治正确，是工程经济

### 2.1 Catalyst 优化器的价值被严重低估

很多人以为 SQL 优化器只做"谓词下推""列裁剪"这些教科书上的事。但在字节 PB 级数仓里，Catalyst 真正值钱的是：

- **Cost-Based Optimizer（CBO）**：基于 Hive 统计信息自动选择 Join 顺序。一个 8 表 Join，人肉排顺序几乎不可能最优，CBO 在 95% 的情况下比人肉排得更好。
- **动态分区裁剪（DPP）**：Spark 3.0+ 在 Broadcast Hash Join 时自动将过滤条件推到事实表扫描侧。手写 RDD 你做不做？做——500 行代码起；不做——多扫 10x 数据。
- **自适应查询执行（AQE）**：运行时自动合并小分区、切换 Join 策略、处理数据倾斜。手写 RDD 时这些全是你自己的事。

### 2.2 可维护性 = 成本

数仓的特点是一个模型被几十个下游引用、一个作业跑了两年突然要改逻辑。SQL 的可读性和可维护性碾压手写代码——这不是偏好，是现实：

- 新人接手一个 SQL ETL 作业：读 30 分钟，改 10 分钟
- 新人接手一个手写 RDD 作业：读 2 天，改 1 天，修 bug 3 天

### 2.3 数据治理的硬需求

字节的数仓治理平台会自动解析 SQL 血缘（表级 + 字段级），构建全链路依赖图。手写 RDD 的血缘解析靠静态分析几乎不可能——你的 DataFrame 经过了 map/flatMap/filter 之后，字段从哪来到哪去，平台根本不知道。这意味着：

- 影响分析失效
- 数据质量监控无法自动挂载
- 成本治理看不到字段级热度

---

## 三、必须手写算子（DataFrame/Dataset/RDD）的四类场景

好，核心问题来了。**以下四类场景，SQL 要么完全做不到，要么做出来是个灾难。**

### 场景一：Session 窗口 / 复杂事件序列匹配（CEP）

**为什么 SQL 不够：**

标准 SQL 窗口函数只能处理固定范围的 ROWS/RANGE BETWEEN。但数仓里大量的需求是：
- 用户 Session 切割（两次行为间隔 > 30 min 切一个新 Session）
- 漏斗分析中的严格时序匹配（A 事件 → 1 小时内 B 事件 → 再 1 小时内 C 事件）
- 归因分析中的多触点归因（时间衰减模型）

这些可以用 SQL 写——但会变成嵌套 3-4 层子查询 + 大量 `LAG/LEAD` + 自关联的怪物。一个 Session 切割逻辑用 SQL 写出 150 行，跑一次 40 分钟；用 DataFrame API + `flatMapGroupsWithState` 写出 60 行，跑 8 分钟。

```scala
// 典型的 Session 切割 —— SQL 极难表达
val sessionized = events
  .groupByKey(_.userId)
  .flatMapGroupsWithState(OutputMode.Append, GroupStateTimeout.EventTimeTimeout) {
    case (userId, events, state) =>
      // 自定义 Session 状态机逻辑
      Sessionizer.cut(events.toSeq, gapThreshold = 30.minutes)
  }
```

**判定标准：** 当你发现 SQL 里出现了 3 层以上的嵌套窗口函数，或者你在用 SQL 模拟状态机——停下来，切 DataFrame API。

### 场景二：自定义分区策略 & 数据倾斜治理

**为什么 SQL 不够：**

SQL 的分发策略只有 HASH / BROADCAST / RANGE 三种。但真实场景中：

- **两阶段聚合（盐值化）**：面对热点 Key，需要加随机前缀打散 → 局部聚合 → 去前缀 → 全局聚合。SQL 能做但极其丑陋（CONCAT + SUBSTR + MOD 满天飞），且 Optimizer 可能会把你的手动两阶段"优化"回一阶段。
- **自定义 Partitioner**：比如根据 Key 的 Hash 范围 + 业务规则做 Range-Lookup 分区。
- **异构数据源 Join 的 Distribute By 控制**：控制哪些数据 Co-locate 到同一 Executor 以减少 Shuffle。

```scala
// 盐值化两阶段聚合 —— 用 SQL 很难保证不被 Optimizer 破坏
val salted = skewedDF
  .withColumn("salt", lit(ceil(rand() * 10)))  // 加 0-9 随机盐
  .groupBy("salt", "hot_key")
  .agg(sum("value").as("partial_sum"))
  .groupBy("hot_key")
  .agg(sum("partial_sum").as("total_sum"))
```

**判定标准：** 如果你的倾斜治理逻辑依赖特定的物理执行计划（不能被 Optimizer 改变），手写 DataFrame API + 关闭部分 AQE 规则。

### 场景三：非结构化 / 半结构化数据解析 + 复杂 UDF 链

**为什么 SQL 不够：**

- **嵌套 Protobuf / Thrift 解析**：数仓经常需要消费在线系统的二进制日志（埋点、交易流水）。解析这些需要 Schema Registry 查找 + 版本兼容逻辑 + 递归展开。SQL 的 `from_json` / `from_protobuf` 只能处理简单的、Schema 固定的情况。
- **复杂 IP 解析**：IP → 国家/省/市/运营商/经纬度，需要加载几十 MB 的 IP 库做二分查找。SQL UDF 能做，但 UDF 初始化、广播变量的管理用 DataFrame `mapPartitions` 更干净。
- **模型推理嵌入**：在 ETL 中做简单的规则模型打分或小模型推理（如敏感词过滤、垃圾内容识别）。

```scala
// mapPartitions 模式：每个 Partition 初始化一次解析器
df.mapPartitions { partition =>
  val ipParser = new IPParser(broadcastIPLib.value)  // 每个分区初始化一次
  val protoParser = new ProtoParser(schemaRegistryClient)
  partition.map { row =>
    // 解析埋点
    val event = protoParser.parse(row.getAs[Array[Byte]]("payload"))
    val ipInfo = ipParser.lookup(event.clientIp)
    (event.eventId, ipInfo.province, ipInfo.city)
  }
}
```

**判定标准：** 你的逻辑需要在每个 Executor / Partition 级别管理有状态资源（连接池、模型对象、大字典），或者需要解析的数据格式 SQL 原生不支持。

### 场景四：迭代计算 & 图计算

**为什么 SQL 不够：**

SQL 的本质是一次性声明式查询，而以下场景需要迭代：

- **漏斗/路径分析的递归回溯**：用户在转化前的完整行为序列，多轮往前回溯
- **PageRank / Label Propagation** 等图算法：数仓里做用户社区发现、欺诈团伙识别
- **RFM 分层**：基于用户的累计消费行为迭代更新分群

Spark 提供了 GraphX（基于 RDD）和 GraphFrames（基于 DataFrame），但在纯数仓场景中，这些东西通常不直接上场——更多时候是 **DataFrame + 循环控制** 的伪迭代方案：

```scala
// 伪迭代：漏斗回溯
var current = factTable.filter($"event" === "purchase")
for (step <- List("add_cart", "view_item", "search", "landing")) {
  current = current.join(
    factTable.filter($"event" === step),
    Seq("user_id"),
    "left_semi"
  ).select($"user_id", factTable("ts").as(s"${step}_ts"))
}
```

> **注意：** 真正的图迭代（如 PageRank 跑 50 轮）应该在专门的图计算系统（如字节自研的 ByteGraph）或离线图计算框架中完成，而不是在数仓 Spark 作业里硬搞。数仓 Spark 作业里最多容忍 3-5 轮迭代。

**判定标准：** 你的逻辑需要"基于上一轮结果重新计算"，且轮次 > 2。

---

## 四、一个实用的决策框架

```
问题：这段逻辑用什么写？

├─ 是否涉及 Session 切割 / 事件序列匹配 / 状态机？      → DataFrame API（flatMapGroupsWithState）
├─ 是否涉及自定义分区 / 手动倾斜治理 / 物理计划控制？     → DataFrame API + 谨慎关闭 AQE 规则
├─ 是否涉及 Protobuf/Thrift 解析 / 大字典查找 / 模型推理？ → mapPartitions + 广播变量
├─ 是否涉及迭代计算（>2 轮）？                           → DataFrame + 循环控制（3-5轮内）
│                                                       → 超过 5 轮：切到专用图/迭代引擎
├─ 是否能用标准 SQL + 内建函数表达？                     → SparkSQL ✅
└─ 是否能用 SQL + 简单 UDF 表达？                        → SparkSQL + 注册 UDF ✅
```

---

## 五、字节数仓的实际演化路径（2019-2026）

这个问题的答案不是静态的——随着 Spark 版本演进，"必须手写"的范围在不断缩小：

| 时间 | Spark 版本 | 关键能力 | 对手写算子的影响 |
|------|-----------|---------|----------------|
| 2019 | 2.3 | SQL 窗口函数 | 减少 30% 手写窗口计算 |
| 2020 | 2.4 | 内置高阶函数（transform/filter/aggregate） | 减少数组/Map 处理的手写 |
| 2021 | 3.0 | AQE, DPP | 手写倾斜治理减少 50% |
| 2022 | 3.1 | ANSI SQL 增强 | 复杂 Join 条件手写减少 |
| 2023 | 3.3 | 更强大的 SQL UDF, ANSI interval | 时间计算手写减少 |
| 2024 | 3.4 | Scala UDF → Java UDF 性能对齐 | 更多逻辑往 UDF 迁移 |
| 2025-2026 | 4.0 Preview | Photon 原生引擎, SQL Scripting | Streaming SQL CEP 初具规模 |

**趋势很清楚：SQL 的能力边界在持续扩大，手写算子的场景在持续收缩。**

---

## 六、2026 年的最佳实践总结

1. **默认选 SparkSQL**。这是纪律，不是偏好。只有当你明确命中上述四类场景时才考虑手写。

2. **如果必须手写，按这个优先级选 API：**
   - DataFrame API（保留 Catalyst 优化） > Dataset API（保留部分优化） > RDD（放弃全部优化）
   - 不到万不得已不碰裸 RDD。即使在迭代计算场景中，也优先用 DataFrame + `mapPartitions`。

3. **UDF 是灰色地带。** 简单的标量 UDF（输入一行返回一行）用 SQL register 模式 OK。复杂的聚合 UDF（UDAF）必须手写且要注意序列化开销。Python UDF 在 Spark 3.x+ 中通过 Arrow 优化已经大幅提速，但对于毫秒级延迟敏感的作业仍然要选 Java/Scala UDF。

4. **代码 Review 检查项：**
   - 看到手写 RDD → 要求作者证明 SQL/DataFrame 无法实现
   - 看到 SQL 里 3 层嵌套窗口函数 → 建议切 DataFrame API
   - 看到 `map` / `flatMap` 而不是 `mapPartitions` → 建议改成批量模式

5. **平台侧应该做的事：**
   - 建设 SQL 代码模板库，把常见的 Session 切割、漏斗分析包装成 UDF/UDAF
   - 在 CI 中检测手写 RDD 的使用，自动触发 Review
   - 提供 DataFrame 工具类（通用盐值化、通用 IP 解析），降低手写成本

6. **对工程师的画像要求：**
   - 初级数仓工程师：只会 SQL，够了
   - 中级数仓工程师：SQL 为主，熟练使用 DataFrame API 处理边界场景
   - 高级/架构师：能精准判断"什么不该用 SQL"，并写出高质量的手写算子 + 完整的单元测试 + 性能验证

**最后一句话：2026 年的数仓 Spark 作业，如果你在写裸 RDD，要么你是万里挑一的硬核场景，要么你在犯一个昂贵的错误。**

---

> *本文基于字节跳动数据平台 2020-2026 年数仓实践经验总结，不代表公司官方立场。*
