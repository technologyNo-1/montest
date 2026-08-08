---
name: spark-etl-tuning
description: 用于诊断和优化运行在 YARN 上的离线批处理/ETL Spark 作业性能问题,支持自动化诊断(基于实际指标而非经验猜测)、按数据验证调优效果、处理多问题并存及多变业务场景。当用户提到 Spark 任务慢/超时、数据倾斜、OOM、GC 频繁、资源浪费、成本过高、Spark UI/History Server 指标分析、调优前后对比、参数配置等关键词时,必须使用本 skill,并优先调用 scripts/ 下的脚本而非仅凭经验给参数。
---

# Spark ETL 调优 Skill(YARN 环境,数据驱动闭环版)

本 skill 不是一份静态参数手册,而是一个**可执行的闭环流程**:采集指标 → 脚本自动诊断 → 给出针对性方案 → 应用后重新采集 → 脚本量化对比 → 判断是否固化为最佳实践或继续迭代。

## 核心工作流(严格按此顺序执行,不要跳步)

### 第 1 步:采集"优化前"指标
按 `references/metrics-collection.md` 的说明,帮用户把 Spark History Server / Spark UI / YARN 的数据整理成 `metrics.json`(schema 见该文档)。如果用户能提供 History Server 地址或直接的 UI 截图/数据,优先帮 TA 转换;如果什么都没有,先用 `assets/sample_metrics_before.json` 作为格式示例,让用户对照着填自己的数据。

### 第 2 步:运行自动诊断
```bash
python scripts/diagnose.py metrics_before.json
```
这一步**必须实际执行**,不要凭经验直接跳到给建议 —— 脚本会基于真实数值计算倾斜比、GC占比、spill比例等,输出按优先级排序的问题清单和证据。

### 第 3 步:处理多问题并存的场景
如果诊断结果不止一个问题,参考 `references/complex-scenarios.md` 第一节的优先级原则:先致命(container被杀)→ 再传染性根因(倾斜)→ 再表象(GC/spill)→ 最后效率优化(资源浪费)。**一次只改一类参数对应的问题**,避免多变量同时变化导致无法判断真正生效的原因。

### 第 4 步:识别是否属于特殊业务场景
如果用户的场景是增量ETL(数据量波动大)、深DAG链条、跨队列资源争抢、含Python UDF、准实时微批等,先看 `references/complex-scenarios.md` 第二节对应的场景说明 —— 这些场景下标准诊断结论需要结合场景特点调整解读方式(比如波动大的增量ETL不能直接比较两次绝对耗时)。

### 第 5 步:应用改动,采集"优化后"指标
用户在生产/测试环境应用建议的参数改动后,重新采集一份 `metrics_after.json`(格式相同)。

### 第 6 步:量化对比,判断是否达标
```bash
python scripts/compare_metrics.py metrics_before.json metrics_after.json
```
输出每个关键指标的前后对比和是否改善的标记。

### 第 7 步:固化或迭代
- 全部指标改善 → 按 `complex-scenarios.md` 第三节的建议,把配置固化为该场景的最佳实践,整理成简短的"问题-方案-效果"记录
- 部分指标未改善 → 回到第 2 步,用新的 metrics_after.json 重新诊断,判断是否引入了新问题,继续迭代

## 文件说明

```
spark-etl-tuning/
├── SKILL.md                          本文件,闭环流程总览
├── scripts/
│   ├── diagnose.py                   自动诊断:输入指标JSON,输出问题清单+证据+建议
│   └── compare_metrics.py            调优前后量化对比,判断是否达标
├── references/
│   ├── metrics-collection.md         如何获取diagnose.py需要的指标数据
│   └── complex-scenarios.md          多问题优先级原则 + 5种典型复杂业务场景
└── assets/
    ├── sample_metrics_before.json    示例数据(格式参考,已内置倾斜+GC+OOM问题)
    └── sample_metrics_after.json     示例数据(优化后,用于演示compare_metrics.py)
```

## 重要原则
- **不允许跳过脚本直接凭经验给参数** —— 除非用户明确说明无法提供任何指标数据,此时才退化为经验判断,并明确告知用户这是"未经数据验证的建议"。
- **每次只验证一个变量的改动**,不要一次性把5类参数全改了再看效果,否则无法归因。
- **资源效率优化排在稳定性问题之后**,任务还不稳定时不要为了省成本牺牲稳定性。
- **数据量波动大的场景不能直接比较绝对耗时**,参考 `complex-scenarios.md` 里的归一化对比建议。