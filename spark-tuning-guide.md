# Spark 大规模指标计算：问题发现、排查、解决与性能调优最佳实践

> 以字节跳动典型场景为例：每天 PB 级数据、数千个 Spark Job、计算数百个业务指标（DAU、留存、LTV、漏斗转化等）。

---

## 一、常见问题分类与发现方式

### 1.1 数据倾斜（Top 1 问题）

**现象识别：**
- Spark UI 中某个 Stage 有 1-2 个 Task 远超其他 Task 的执行时间（几百 ms vs 几十分钟）
- Shuffle Read/Write 严重不均衡
- OOM 集中在个别 Executor

**根因：**
```scala
// 典型场景：按 user_id group by，但大 V 数据量是普通用户的万倍
df.groupBy("user_id").agg(sum("play_duration"))
// 或 join 时热点 key
largeDF.join(smallDF, Seq("hot_key"))  // hot_key 分布极度不均
```

**排查方法：**
```bash
# 1. Spark UI → Stages → 查看 Task 时间分布，找长尾 Task
# 2. 抽样查看 key 分布
```

```sql
-- 3. 直接查询 key 分布
SELECT key, COUNT(*) as cnt
FROM table
GROUP BY key
ORDER BY cnt DESC
LIMIT 100;
```

**解决方案（按优先级）：**
1. **两阶段聚合（加盐去盐）** — 最常用
2. **Broadcast Join** — 小表 < 10GB（可调大 `spark.sql.autoBroadcastJoinThreshold`）
3. **Split-Join** — 将倾斜 key 单独处理再 union
4. **Skew Join Hint** — Spark 3.x 原生支持

### 1.2 Shuffle 膨胀

**现象识别：**
- Shuffle Write 远大于输入数据量
- Stage 间数据量暴涨
- 磁盘 I/O 成为瓶颈

**根因：**
- 多表 join 产生笛卡尔积或大量重复
- `groupBy` + `collect_list` 导致单 key 数据过大
- 未做提前过滤或去重

**排查方法：**
```bash
# Spark UI → SQL/DataFrame Tab → 查看每个算子输入输出行数
# 重点关注 Join 和 Aggregate 节点的输出膨胀比
```

### 1.3 OOM 与 GC 过载

**现象识别：**
```
Container killed by YARN for exceeding memory limits.
java.lang.OutOfMemoryError: Java heap space
java.lang.OutOfMemoryError: GC overhead limit exceeded
```

**排查方法：**
```bash
# 1. 检查 GC 日志
-XX:+PrintGCDetails -XX:+PrintGCDateStamps

# 2. 分析 Executor 内存分布
# Spark UI → Executors → Storage Memory / Execution Memory

# 3. dump heap（极端情况）
-XX:+HeapDumpOnOutOfMemoryError
```

### 1.4 小文件问题

**现象识别：**
- 输出目录有数万甚至数十万个文件
- 下游读取极慢（每个文件一个 Task）
- HDFS NameNode 压力大

**排查：**
```bash
hdfs dfs -ls /path/to/output | wc -l
hdfs dfs -count /path/to/output
```

### 1.5 动态资源分配与 Executor 调度问题

**现象：**
- YARN 集群资源充足但 Job 排队
- Executor 频繁申请和释放
- Container 抢占导致 Task 失败重试

---

## 二、实战性能调优最佳实践

### 2.1 内存管理（核心）

```bash
# === 最关键的几个参数 ===

# 1. YARN 模式下，给 Executor 留足 overhead
spark.executor.memory=16g           # JVM heap
spark.executor.memoryOverhead=4g    # off-heap（默认 max(384m, 0.1*memory) 往往不够）
# 总 container 内存 = 16g + 4g = 20g

# 2. 合理分配堆内 Memory Region
spark.memory.fraction=0.6           # 60% 用于 execution + storage，40% 用于用户对象
spark.memory.storageFraction=0.5   # storage 和 execution 各占一半

# 3. 堆外内存（排序/shuffle 时使用，避免 GC）
spark.memory.offHeap.enabled=true
spark.memory.offHeap.size=2g

# 4. GC 调优：大数据场景用 G1GC
spark.executor.extraJavaOptions=-XX:+UseG1GC -XX:InitiatingHeapOccupancyPercent=35 -XX:ConcGCThreads=4
```

### 2.2 Shuffle 优化

```bash
# 1. 使用基于排序的 shuffle（默认就是 sort shuffle）
spark.sql.shuffle.partitions=2000   # 根据数据量设置，单 partition 目标 128MB-256MB

# 2. 开启 bypass（无聚合场景，跳过 sort，类似 hash shuffle）
spark.shuffle.sort.bypassMergeThreshold=400

# 3. 压缩
spark.shuffle.compress=true
spark.io.compression.codec=zstd     # zstd > lz4 > snappy（压缩比），lz4 > snappy > zstd（速度）

# 4. Shuffle 服务（动态资源分配必备）
spark.shuffle.service.enabled=true
spark.dynamicAllocation.enabled=true
```

### 2.3 Join 策略优化

```bash
# 1. Broadcast Join 阈值（字节场景常调到 512MB-1GB）
spark.sql.autoBroadcastJoinThreshold=536870912  # 512MB

# 2. 强制 Broadcast Hint
/*+ BROADCAST(small_table) */

# 3. Sort Merge Join → Broadcast Join 转换条件
# 小表 < broadcast 阈值，且能被广播（非广播端没有 hint 限制时）

# 4. 消除无用 Join
# AQE 在 Spark 3.x 可以自动检测并消除
spark.sql.adaptive.enabled=true
```

### 2.4 AQE（Adaptive Query Execution）— Spark 3.x 核心

```bash
# AQE 三大能力
spark.sql.adaptive.enabled=true

# ① 动态合并小分区（coalesce）
spark.sql.adaptive.coalescePartitions.enabled=true
spark.sql.adaptive.coalescePartitions.minPartitionSize=1MB
spark.sql.adaptive.coalescePartitions.initialPartitionNum=2000

# ② 动态切换 Join 策略（SortMerge → Broadcast）
spark.sql.adaptive.localShuffleReader.enabled=true

# ③ 动态处理倾斜 Join
spark.sql.adaptive.skewJoin.enabled=true
spark.sql.adaptive.skewJoin.skewedPartitionFactor=5   # partition 超过中位数 5 倍视为倾斜
spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes=256MB
```

### 2.5 数据读写优化

```scala
// === 列式存储 + 分区裁剪 ===
df.write
  .mode(SaveMode.Overwrite)
  .partitionBy("dt", "hour")       // 按日期+小时分区
  .bucketBy(256, "user_id")        // 分桶，加速后续 join
  .sortBy("user_id")
  .format("parquet")               // 或 ORC
  .option("compression", "zstd")
  .save(path)

// === 小文件合并 ===
// 方法 1: repartition（数据量可控时）
df.repartition(200).write.parquet(path)

// 方法 2: coalesce（减少分区时，避免 shuffle）
df.coalesce(200).write.parquet(path)

// 方法 3: AQE 自动合并（推荐）
spark.sql.adaptive.coalescePartitions.enabled=true

// 方法 4: 定时合并任务（Hive）
// INSERT OVERWRITE TABLE target SELECT * FROM target;
```

### 2.6 序列化优化

```bash
# 使用 Kryo 序列化（比 Java 序列化快 10x）
spark.serializer=org.apache.spark.serializer.KryoSerializer
spark.kryo.registrationRequired=false  # 生产可以先 false，调优后改为 true
spark.kryoserializer.buffer.max=1024m  # 大数据场景加大 buffer
```

### 2.7 推测执行与失败重试

```bash
# 推测执行：慢 Task 在其他节点重跑（解决机器性能不均）
spark.speculation=true
spark.speculation.interval=100ms        # 检查频率
spark.speculation.multiplier=3          # 超过中位数 3 倍的 Task 触发推测
spark.speculation.quantile=0.9          # 取 90 分位的 Task 时间作为基准

# 注意：写入外部存储（如 Kafka/MySQL）时关闭推测执行，防止重复写入
```

### 2.8 SQL/DataFrame 层面优化

**算子选择优先级：**
```
reduceByKey > groupByKey           # 带 map 端预聚合
DataFrame/SQL > RDD                # Catalyst 优化器 + Tungsten 全阶段代码生成
broadcast join > sort merge join   # 小表场景
map-side filter > shuffle 后 filter # 尽早裁剪数据
```

**具体示例：**

```scala
// ❌ 差：先 groupBy 再 filter
df.groupBy("user_id", "page_id")
  .agg(count("*").as("pv"))
  .filter($"pv" > 10)

// ✅ 好：子查询先聚合再过滤（逻辑无变化，但利用 AQE）
df.groupBy("user_id", "page_id")
  .agg(count("*").as("pv"))
  .filter($"pv" > 10)
// 两者逻辑相同，确保 spark.sql.adaptive.enabled=true
// 实际优化：增加 local 预聚合减少 shuffle 量

// ❌ 差：UDF 在 Java/Scala 中处理
val myUDF = udf((s: String) => complexLogic(s))
df.withColumn("result", myUDF($"col"))

// ✅ 好：尽可能用内置函数（Catalyst 能优化）
df.withColumn("result",
  when($"col".isNull, "default")
    .otherwise(regexp_replace($"col", "pattern", "replacement"))
)
```

---

## 三、字节场景的特殊实践

### 3.1 多指标 Pipeline 化

```
ODS → DWD（清洗）→ DWS（轻度聚合）→ ADS（指标层）
每个层级逐步减少数据量，避免在原始数据上多次扫表
```

### 3.2 实时 + 离线 Lambda 架构

```
Kafka → Flink（实时计算分钟级指标）
              ↓
HDFS → Spark（T+1 离线校正）→ 最终指标 = 实时 + 离线修正
```

### 3.3 诊断工具箱

```bash
# 1. 快速诊断脚本
spark-submit --conf "spark.extraListeners=com.example.DiagnosticsListener" \
  --conf "spark.sql.adaptive.enabled=true" \
  --conf "spark.eventLog.enabled=true" \
  --conf "spark.eventLog.dir=hdfs:///spark-history" \
  your-job.jar

# 2. 事后分析
# Spark History Server → 查看：
#   - Job Duration（有哪些 Stage 是瓶颈）
#   - Stage → Summary Metrics（Task 时间分布）
#   - Stage → Aggregated Metrics by Executor（Executor 间负载是否均衡）
#   - SQL Tab → 每个算子的输入/输出行数
#   - Executors Tab → GC Time / Shuffle Read/Write

# 3. Metrics 监控（Prometheus + Grafana）
# 关键指标：
#   - executor.gc.time.percent
#   - executor.shuffle.records_written
#   - executor.shuffle.spill.disk
#   - executor.running_tasks vs executor.cores
```

---

## 四、调优顺序（经验法则）

```
第1步：AQE 全开（投入产出比最高，零代码改动）
第2步：内存参数调优（memoryOverhead, G1GC, memory.fraction）
第3步：Shuffle 分区数调优（2000 → 根据数据量计算最优值）
第4步：Join 策略优化（Broadcast Hint, 数据倾斜处理）
第5步：数据存储优化（分区、分桶、文件格式、压缩）
第6步：代码层面优化（算子选择、提前过滤、避免 UDF）
第7步：硬件层面（SSD、万兆网卡、NUMA 绑定）
```

---

如果你有具体场景（比如某个指标计算特别慢、某个 Job 经常 OOM），可以告诉我详细信息，我可以给出针对性的排查和优化方案。
