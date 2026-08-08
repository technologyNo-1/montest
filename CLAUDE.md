# CLAUDE.md - 本 Vault 的维护规则（LLM Wiki Schema v2）

> 本文件是 Claude Code 在本 vault 工作的指令手册。任何在 `/Users/wyf/Desktop/code/document` 启动的 claude 会话会自动读取。
> 模式：**Karpathy LLM Wiki** -「人选材料，LLM 维护」。
> **v2 核心转变（2026-08-08）**：从「LLM 手写结构」到「**LLM 维护元数据与链接，结构自动生成**」——用 properties + Bases + MOC 三件套，让索引/看板/网络自动长出来。详见 [[vault_research_workflow_rebuild_2026-08-08]]。

## 1. Vault 定位

wyf 的个人知识库，存放 AI/大数据领域的调研、人物思想、行业报告、技术实践、求职职业、工作方法论、投资调研。目标：可被 Claude Code 读写、Obsidian 可视化、定期复盘自我进化的**持久知识网络**——越用越密的积累，而非一次性问答。

## 2. 分类逻辑（10 类，`01-`~`09-` + Clippings + 存档）

| 目录 | frontmatter `type` | 内容 |
|---|---|---|
| `01-people/` | `people-analysis` | 人物思想深度调研 |
| `02-industry/` | `industry-report` | 行业趋势/公司报告 |
| `03-ai-token/` | `ai-token` | AI Token/算力经济（`research/` `delivery/` `data/`） |
| `04-tech/` | `tech-practice` | 技术实践（`dataworks/` 数仓、`interviews/` 面试、散篇） |
| `05-career/` | `career` | 求职/职业/岗位 |
| `06-workflows/` | `workflow` | 工作方式/方法论 |
| `07-paper/` | `paper-summary` | 论文总结（`paper_summaries.md` 单文件追加） |
| `08-book/` | `book` | 书籍/读书笔记 |
| `09-invest/` | `invest-research` | 投资调研（公司/标的/产业链投资视角） |
| `Clippings/` | `clipping` | 网页剪藏原料库（被调研文档引用，不进知识网络主干） |
| `10-claude-QA/` | （无 type） | 对话存档（全局指令归档，**不计入 lint 孤儿/合规**） |

新文档入库按内容归类，存疑读首段判断；跨类主题按主旨归一类，用 tags + MOC 跨类关联。

## 3. 文件命名规范

- 小写英文+下划线为主；中文人物名/主题可保留中文
- 人物调研：`<英文名>_analysis.md` 或 `<中文名>_<主题>.md`
- 不用空格，用下划线；日期后缀 `_YYYY-MM-DD`
- **Clippings 规范化**：剪藏文件名去空格/特殊字符/零宽字符，转 `<主题>_clipping.md`；原标题作 `aliases` 便于搜索
- MOC 文件：`MOC-<主题>.md`（顶层主题入口）

## 4. frontmatter 标准（每个内容文档必须有）

```yaml
---
title: 标题
type: people-analysis   # 见 §2，单一值，不带行内注释
date: 2026-08-08        # 文档日期/整理日期
tags: [人物名, 主题, 技术]
status: active          # active | stale | draft
source: 原始来源或生成方式
confidence: A1          # Admiralty 信源置信度，调研文档必填；纯方法论/笔记可省
aliases: [别名]         # 便于 wikilink 与搜索，可省
---
```

**Admiralty 置信度（信源可靠度 A-F × 信息可信度 1-6，双字符）**：
- `A1` 一手直接/高度可信（原文、财报、本人访谈、代码）
- `A2` 一手/可能可信
- `B1` 权威二手/交叉印证（Nature/Quanta/SemiAnalysis）
- `B2`/`B3` 权威二手/单源或存疑
- `C1` 一般/未交叉（百科、聚合、SEO 内容）

**硬规则**：
- `type`/`status` 字段值**不带行内注释**（旧版 `type: people-analysis  # 见 §2` 是脏值，禁止）
- 每次 ingest 强制补全 frontmatter；lint 校验合规率 → 100%
- 不删人写正文，frontmatter 缺失只补不改

## 5. 链接规范

- **文档间引用用 wikilink**：`[[文件名]]` 或 `[[文件名|显示文本]]`。Obsidian 原生，移动不失效。
- **不用相对路径** `../xxx.md`。
- **MOC（Map of Content）**：跨类主题入口。顶层 MOC：`[[MOC-人物思想]]` `[[MOC-算力与半导体]]` `[[MOC-AI-Agent]]` `[[MOC-调研方法论]]` `[[MOC-投资与金融]]`。入库时检查并建链到相关 MOC，**目标出链 5-8/篇**。
- `INDEX.md` = "MOC of MOC" 总入口，只列 MOC + 维护页，不手抄全部文档。
- 概念/人物交叉链接汇聚在 MOC 与 `INDEX.md`。
- 引用源文件给 `文件路径:行号`。
- **维护页箭头字符**：统一用 Unicode `→`（U+2192）、`←`（U+2190），非 ASCII `->`/`<-`；Edit 时从原文复制字符，新增行对齐。

## 6. 三个核心操作（升级：自动生成优先）

### ingest - 新文档入库
1. 判断分类，放入对应目录
2. 补全 frontmatter（§4），含 confidence/aliases
3. **建链到相关 MOC**（检查已有 MOC，无则新建待审批）；目标 5-8 出链/篇
4. **Bases 自动索引**：无需手写 _index 条目，.base 视图按 type 自动收录
5. 在 `INDEX.md` 的 MOC 入口补交叉链接（仅 MOC 级，不逐条）
6. 追加 `CHANGELOG.md` 一行
7. `git add -A && git commit`

### query - 查询
用户问 vault 内容时：先用 Grep/Read/Bases 检索，给 **grounded 答案**（基于本库，不杜撰），引用源文件路径。涉及多文件交叉综合。

### lint - 检查维护 / 复盘（查询驱动，不手扫）
用户说「复盘 vault」「lint」「整理一下」时执行：
1. **frontmatter 合规率**：查无 type/status 的文档
2. **孤儿**：Dataview `FROM "" WHERE length(file.inlinks)=0`（排除 _index/MOC/Clippings/10-claude-QA）
3. **stale**：`status: stale` 或长期未更新，提示复核
4. **坏链**：失效 wikilink
5. **密度**：出链 <3/篇 的文档补链
6. 更新 MOC 与 `INDEX.md`
7. 追加 `CHANGELOG.md`
8. `git commit`

## 7. 调研 pipeline（分块容错 + claim 级校验）

详见 [[vault_research_workflow_rebuild_2026-08-08]]。核心：

1. **定承重墙骨架**（主 agent，先于抓取）——三类骨架：
   - 人物 = 思想演进主干（架构化、多预算）+ 背景从简 + 事实订正收文末
   - 行业 = 价值链 → 五力 → 供需/竞争 → 国产替代/卡点 → 演进判断
   - 技术 = 问题 → 方案 → 实现 → 落地效果 → 踩坑 → 可复用结论
2. **分块并行抓取**（每块一个 subagent）：lead agent 发「目标+边界+输出格式+不准碰 X」明确指令防重复；产物落文件只回传引用；思想演进多预算，背景/商业从简。
3. **claim 级校验**：关键 claim 标 Admiralty 置信度，事实/推断显式区分，事实订正全收文末一节。
4. **satisficing 阈值**：设渴望水位达阈即停；复杂度分级（事实查找 1 agent / 复杂研究多 agent）。
5. **ingest**：走 §6 清单。

**搜索后端（通用规则，不限场景）**：
- WebSearch 工具本环境空——不用
- Tavily MCP 易耗尽——可先试找 URL，耗尽即切免 key 路径，**不退回"基于知识"**
- 免 key 兜底（默认）：r.jina.ai 抓取（`curl -s "https://r.jina.ai/<url>" -H "Accept: text/markdown"`）、WebFetch 工具、DDG html 搜索（`https://duckduckgo.com/html/?q=...`）
- s.jina.ai 需 key——别用
- 所有路径失败才退回"基于知识"并明确标注

**调研 Workflow 状态**：默认不启动多 agent Workflow；用单 agent 精研或先对齐骨架再动手。恢复 Workflow 需用户明确 opt-in。

## 8. Obsidian 维护三件套（结构自动生成）

1. **properties（数据）**：类型化 frontmatter，一切自动化地基。官方："Bases are only as good as your properties"。合规率必须近 100%。
2. **Bases（视图）**：每类建 `.base` 视图（按 type/status/tags 自动生成活索引+看板），替代手写 _index.md。AI 只写 .base 纯文本，不手抄条目。孤儿检测用 Dataview 查询。
3. **MOC/wikilink（网络）**：LYT 模式，入库时建链到 MOC，目标 5-8/篇。MOC 替代静态 INDEX，移动不失效。

## 9. 安全规则

- **不删除人写的原创正文**；废弃用 `status: stale` 标记，不物理删
- 重大改动前先 `git commit`；可 `git checkout` 回滚
- **不在 vault 存** API key / 密码 / token
- LLM 维护页（`CLAUDE.md` / `INDEX.md` / `MOC-*.md` / `_index.md` / `CHANGELOG.md`）可自由改；人的调研文档**只补 frontmatter 与 wikilink，不改正文**
- 每次操作后 `git commit`，保持历史可追溯
- 批量改 frontmatter/链接前先 `git commit` 保护

## 10. Obsidian 协同

- `/.obsidian/` 是配置，不手动改（已 .gitignore 部分排除）
- 优先 wikilink、frontmatter、tags、Bases（原生能力）
- 保持 frontmatter 规范，便于 Bases/Dataview 查询
- 图谱视图依赖 wikilink，多建交叉链接让网络可视化
- 已装 kepano 官方 skills（defuddle/json-canvas/obsidian-bases/obsidian-cli/obsidian-markdown）

## 11. 自我进化闭环

```
新增文档 → ingest(补frontmatter+建MOC链) → Bases自动索引 → Dataview lint(查询驱动)
   ↑                                                                    ↓
   └────────── 定期复盘（用户触发）←── CHANGELOG 记录 ←──────────────────┘
```

知识在 wikilink + MOC 网络中沉淀，结构自动生成，lint 查询驱动修复。vault 核心价值=越用越密的持久知识网络。
