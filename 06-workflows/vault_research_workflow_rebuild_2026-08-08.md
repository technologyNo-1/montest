---
title: "Vault 调研工作流重构:从手写结构到自动生成"
type: workflow
date: 2026-08-08
tags: [vault, obsidian, 调研方法论, MOC, Bases, frontmatter, 重构, 知识管理]
status: active
source: "Obsidian 官方文档(Bases/Properties)+ LYT MOC + Admiralty 信源分级 + Anthropic 多 agent 调研 + 本地体检数据综合"
aliases: [vault重构, 调研工作流重构]
---

# Vault 调研工作流重构:从手写结构到自动生成

> **一句话**:旧工作流(5.0/10)的病根是"结构靠 LLM 手写",规模过 100 篇即崩;重构为"properties + Bases + MOC 三件套让结构自动生成,LLM 只维护元数据与链接",新计划 8.5/10。主杠杆=结构自动生成 + 调研分块容错。

---

## 一、现状体检(2026-08-08,数据驱动)

| 指标 | 现状 | 健康线 | 诊断 |
|---|---|---|---|
| 文档规模 | 123 md | - | 适中 |
| frontmatter 合规率 | 56%(79/141) | >95% | 严重不达标,近半无元数据 |
| 脏 frontmatter | 2 条模板注释被当值 | 0 | 批量打底出错 |
| wikilink 密度 | 1.6/篇 | 5-8/篇 | 网络稀疏 |
| 孤儿率 | 41%(51/123) | <15% | 大量无入链 |
| 06-workflows 孤儿率 | 78%(19篇15孤儿) | - | 重灾区 |
| 09-invest/10-claude-QA/Clippings | 100%/100%/92% 孤儿 | - | 游离体系外 |
| 规则 vs 实际 | CLAUDE.md 定义 8 类,实际 9+ 类 | 一致 | 脱节 |
| lint 执行 | INDEX 自挂 4 项 todo 未做 | 定期清 | 空转 |
| status 梯度 | 71 active / 0 stale | 有梯度 | stale 从未执行 |

**断裂铁证**:`01-people/` 6 篇新文档(BanghuaZhu/Christopher_Manning/Einstein/IlyaSutskever_SafeSuperintelligence/Moonshot_Academy/Woosuk_Inferact)是未走 ingest 的裸文件。

---

## 二、旧工作流打分(5.0/10)

### 过程

| 环节 | 分 | 评 |
|---|---|---|
| ingest 框架 | 6/10 | 三操作方向对,但步骤靠人工记忆未固化,6 篇漏走流程 |
| 调研执行 | 5/10 | 早期 6-agent Workflow ROI 低(Demis);后期 2-subagent+骨架先行改善(terence_tao 高质);但反复重做(HBM4E/claude_memory) |
| 搜索后端 | 4/10 | 反复撞墙后才沉淀规则,且没提升为通用规则,主 agent 没用上 |
| 链接网络 | 3/10 | 1.6/篇、41% 孤儿,概念地图没建起来 |
| 元数据治理 | 3/10 | 56% 合规+脏值+无梯度 |
| 记忆反馈闭环 | 8/10 | 6 条精准 memory 有效驱动改进,最健康 |
| CHANGELOG | 8/10 | 详细留痕 |

### 结果

| 产出 | 分 | 评 |
|---|---|---|
| 人物调研 | 7/10 | 最新高质,早期不及格,方差大 |
| 行业调研 | 6/10 | 有方法论框架,但删了重做 |
| 知识网络密度 | 3/10 | 远低于健康线 |
| 可复用性 | 4/10 | 一次性长文,缺原子化洞察 |
| 维护负担 | 4/10 | 手写 _index/INDEX 重且易漏 |

### 根因

1. **结构靠手写而非自动生成**:索引全靠 LLM 手抄,新增没走流程即成孤儿。properties+Bases 能让结构自动长出,但没用。
2. **元数据是地基却最薄弱**:56% 合规+脏值,任何自动化都建不起来。
3. **链接网络从未真正建立**:1.6/篇,LYT MOC 未实施。
4. **调研一次性成文、缺分块容错**:先抓再整合,失败整篇报废。
5. **规则与实际脱节**:CLAUDE.md 停在 8 类,实际 9+ 类。

**核心病根**:"手写结构"模式不可持续,规模过 100 篇即崩。

---

## 三、新架构(结构自动生成)

**理念转变**:从"LLM 手写结构"到"**LLM 维护元数据与链接,结构自动生成**"。三件套:
- **properties(数据)**:类型化 frontmatter,一切自动化地基。官方:"Bases are only as good as your properties"。
- **Bases(视图)**:按 type/status/tags 自动生成活索引+看板,替代手写 _index.md。
- **MOC/wikilink(网络)**:入库时建链到 MOC,目标 5-8/篇,LYT 模式。

### 3.1 知识分类:目录(粗分)+ MOC(主题)双轨
- 目录保留作物理归位,降为粗分类,不再要求每类手写 _index.md。
- 顶层 MOC 跨类汇聚:`[[MOC-人物思想]]` `[[MOC-算力与半导体]]` `[[MOC-AI-Agent]]` `[[MOC-调研方法论]]` `[[MOC-投资与金融]]`。
- INDEX.md 升级为"MOC of MOC"总入口。
- 游离目录归位:09-invest 纳入(type: invest-research);Clippings 建索引+文件名规范化为"原料库"(type: clipping);10-claude-QA 标记为对话存档(不计孤儿)。

### 3.2 frontmatter 标准(强制+类型化)
```yaml
title / type / date / tags / status / source
confidence: A1|A2|B1|B2|C1   # Admiralty 信源置信度,调研文档必填
aliases: [别名]              # 便于 wikilink 与搜索
```
- type 扩展:people-analysis | industry-report | ai-token | tech-practice | career | workflow | paper-summary | book | invest-research | clipping
- 每次 ingest 强制补全,lint 校验合规率->100%,删脏值。
- **Admiralty Code**(信源可靠度 A-F × 信息可信度 1-6,两轴独立):A1=一手直接/高度可信,B3=权威二手/可能,C1=一般/未交叉。

### 3.3 调研 pipeline(分块容错 + claim 级校验)
1. **定承重墙骨架**(主 agent,先于抓取):三类骨架
   - 人物 = 思想演进主干(架构化、多预算) + 背景从简 + 事实订正收文末
   - 行业 = 价值链定位 -> 五力 -> 供需/竞争 -> 国产替代/卡点 -> 演进判断
   - 技术 = 问题 -> 方案选型 -> 实现/架构 -> 落地效果(可量化) -> 踩坑 -> 可复用结论
2. **分块并行抓取**(每块一个 subagent):lead agent 发"目标+边界+输出格式+不准碰 X"明确指令防重复;产物落文件只回传引用(避免传话游戏)。思想演进多预算,背景/商业从简。
3. **claim 级校验**:关键 claim 标 Admiralty 双字符置信度 [A1]/[B3],事实/推断显式区分,事实订正全收文末一节(不散布正文)。
4. **satisficing 阈值**:设渴望水位达阈即停,按复杂度分级(事实查找 1 agent × 3-10 调用;直接对比 2-4 subagent × 10-15;复杂研究 10+ subagent)。
5. **ingest 入库**:走固化 checklist(归类 -> frontmatter -> MOC 建链 -> Bases 自动索引 -> CHANGELOG -> commit)。
- **搜索后端(通用规则)**:默认 r.jina.ai + DDG + WebFetch,不用 WebSearch(本环境空),Tavily 省用(耗尽即切免 key 路径),所有路径失败才退回"基于知识"并标注。

### 3.4 Obsidian 维护(自动化)
- **properties**:强制合规,自动化地基。
- **Bases**:每类 `.base` 视图替代手写 _index.md,自动生成活索引+看板。AI 只写 .base 纯文本。
- **MOC/wikilink**:入库时检查并建链到相关 MOC,目标 5-8/篇。
- **lint 查询化**:孤儿/stale/坏链/合规率全用 Bases/Dataview 查询自动发现,lint 只做确认+修复。孤儿检测 Dataview:`FROM "" WHERE length(file.inlinks)=0`。

### 3.5 自动化闭环
```
人选材料 -> 主agent定承重墙骨架 -> 分块subagent并行抓取(r.jina.ai+DDG)
  -> claim级校验+Admiralty置信度 -> ingest(补frontmatter+建MOC链+CHANGELOG)
  -> Bases自动生成索引 -> Dataview定期lint(孤儿/stale/合规率) -> commit
持久知识库: 调研产物evergreen原子化, 后续调研增量更新而非重写
```

---

## 四、新计划打分(8.5/10)

| 维度 | 分 | 依据 |
|---|---|---|
| 理论依据 | 9/10 | Obsidian 官方 Bases/properties + LYT MOC + Admiralty + Anthropic 多 agent/claim 级校验 |
| 场景适配 | 9/10 | 直击三大病根 + 调研稳定性 |
| 可落地性 | 8/10 | Bases/properties/Dataview 均为 vault 已具备能力(Obsidian 1.12.7) |
| 容错性 | 8/10 | 调研分块+每块独立可保存,失败只重做单块 |
| 维护负担下降 | 9/10 | 手写 _index->Bases 自动;链接->MOC 规则化;lint->查询驱动 |
| 风险扣分 | -2 | Bases 仍 roadmap(kanban/API 未齐);批量改 frontmatter 需谨慎不损正文 |
| **综合** | **8.5/10** | 旧 5.0 -> 新 8.5 |

**最大杠杆**:把"手写结构"换成"properties+Bases+MOC 自动生成";把"调研一次性整合"换成"分块容错+claim 级校验"。

---

## 五、调研方法论权威依据

| 来源 | 核心贡献 | 应用 |
|---|---|---|
| [Obsidian Bases(官方)](https://help.obsidian.md/bases) | .base 视图按 properties 自动生成索引 | 替代手写 _index.md |
| [Obsidian Properties(官方)](https://help.obsidian.md/Editing+and+formatting/Properties) | 类型化 frontmatter | 自动化地基 |
| [LYT / Nick Milo](https://linkingyourthinking.com) | MOC middle-out,最契合 AI 协作 | 顶层 MOC 替代稀疏 INDEX |
| [dsebastien 8000 笔记](https://www.dsebastien.net/personal-knowledge-management-at-scale-analyzing-8-000-notes-and-64-000-links) | 8 出链/篇是密度健康线 | 建链目标 |
| [NATO Admiralty Code](https://en.wikipedia.org/wiki/Admiralty_code) | 信源 A-F × 可信度 1-6 双轴 | confidence 字段 |
| [Anthropic 多 agent 调研](https://www.anthropic.com/engineering/multi-agent-research-system) | orchestrator-worker,明确边界防重复,产物落文件只回传引用 | 调研 pipeline 分块 |
| [McKinsey 7 步](https://slideworks.io/resources/mckinsey-problem-solving-process) | 假设驱动+迭代+可证伪 | 行业调研骨架 |
| [claim-level 蕴含校验](https://futureagi.com/blog/llm-hallucination-deep-dive-2026) | 逐 claim NLI 打分,报每条幻觉率 | 事实校验 |
| [Satisficing(Simon)](https://en.wikipedia.org/wiki/Satisficing) | 渴望水位达阈即停 | ROI 控制 |
| [Evergreen notes(Andy Matuschak)](https://notes.andymatuschak.org/z5E5QawiXCMbtNtupvxeoEX) | 原子化、概念导向、密集链接、累积演进 | 可复用性 |

---

## 六、关联

- 旧反馈:[[feedback-people-analysis-structure]](思想演进重点)、[[feedback-research-workflow-paused]](暂停 Workflow)、[[feedback-search-backend-selection]](搜索后端通用规则)、[[feedback-research-obsidian-integration]](入库步骤固化)、[[feedback-research-pipeline-5min]](5min 架构)、[[feedback-claude-memory-doc-approach]](官方源头优先)
- 维护页:[[CLAUDE.md]](执行手册)、[[INDEX]](MOC of MOC)、[[CHANGELOG]]
- 同类方法论:[[claude_memory_全流程_2026-07-23]]、[[deep_similarity_training_2026-07-21]]、[[AI_Native_工作方式与时间分配_最佳实践]]
