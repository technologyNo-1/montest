---
title: "Claude 记忆全流程:官方设计·多 agent 调优·生产级理念(结合本地)"
type: workflow
date: 2026-07-23
tags: [memory, claude-code, context-engineering, multi-agent, 知识管理, obsidian, 方法论, CoALA]
status: active
source: "Claude 官方文档 + Anthropic engineering blog + arxiv 论文 + 落地项目 docs 调研(3 subagent 并行搜集原始信息,主 agent 一次性整合)"
---

# Claude 记忆全流程:官方设计·多 agent 调优·生产级理念(结合本地)

> **一句话主线**:Claude 的"记忆"本质是 **context engineering**--在有限 context window 里治理"哪些 token 该出现",而非无限堆积事实。所有官方机制(200 行限额、just-in-time 召回、/doctor 裁剪)和业界方案(CoALA 四分法、MemGPT 虚拟内存、Letta Context Constitution)都指向同一理念:**记忆不是"存",而是"治理"**。
> **本文与旧版的区别**:旧版 `claude_memory_全流程_2026-07-22` 跳过官方源头、直接讲本地实测,是经验主义;本版**从官方设计出发**(docs.claude.com / platform.claude.com / Anthropic engineering blog),经**多 agent 调优**与**论文/落地项目**拓展,落到**生产级理念**,最后才**结合本地泛化**。旧版已删,git 历史可回溯。
> **整理日期**:2026-07-23
> **信源层级**:L0 官方一手(docs.claude.com / platform.claude.com / code.claude.com / anthrop.com news & engineering / support.anthropic.com)> L1 论文(arxiv,经一手摘要核实)> L2 项目官方 docs。Tavily MCP 本会话配额耗尽,subagent 改用官方站 `.md` 端点 + arxiv + Jina Reader 直取;Cursor docs 为 SPA 未提取正文,已如实标注。

---

## 〇、三层记忆先听懂

| 层 | 性质 | 对应官方概念 | 本地映射 |
|---|---|---|---|
| **working** | 当前会话 context(window 内) | context window + 活跃 memory | 当前对话 + MEMORY.md 前 200 行 |
| **long-term** | 跨会话持久(窗口外) | auto memory / CLAUDE.md / memory tool/stores | auto-memory + CLAUDE.md + vault |
| **external** | 外部知识/工具通道 | MCP / RAG / 外部 store | obsidian-vault / tavily / mysql / macos MCP |

记住这个分层,下面所有细节都是"这三层怎么治理"的展开。

---

## 一、Claude 官方 memory 设计(权威源头)

### 1.1 双系统:CLAUDE.md(人写)+ auto memory(Claude 自写)

Claude Code 有两套互补记忆,**都每会话加载,都当作 context 注入而非强制配置**:

- **CLAUDE.md**:用户写的持久指令(规矩)。
- **auto memory**:Claude 基于用户纠正/偏好自己记的笔记(事实)。

> 官方原话:"Both are loaded at the start of every conversation. Claude treats them as context, not enforced configuration."([code.claude.com/en/docs/memory](https://code.claude.com/docs/en/memory))

**设计哲学**:要硬性阻断动作,**不能靠 CLAUDE.md**(它只是 context、不保证合规),而要用 **PreToolUse hook**。这是和"把规矩写进 CLAUDE.md 就万事大吉"直觉相反的关键点。

### 1.2 CLAUDE.md 分层加载:拼接,不覆盖

按 scope 从宽到窄加载,**所有发现的文件拼接进 context,而非互相覆盖**;目录树从 cwd 向上遍历,子目录里的 CLAUDE.md **不在启动时加载**,而是读该子目录文件时按需加载。

| 层 | 路径 | 说明 |
|---|---|---|
| Managed policy | `/Library/Application Support/ClaudeCode/CLAUDE.md`(mac) | IT/DevOps 管,**不可被排除**,组织基线 |
| User | `~/.claude/CLAUDE.md` | 全局个人 |
| Project | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 随版本控制共享 |
| Local | `./CLAUDE.local.md` | 个人、加 .gitignore |

辅助:`/memory` 列出各 scope 文件并开关 auto memory;`/init` 分析代码库自动生成起始 CLAUDE.md;`@path/to/import` 导入额外文件(递归深度 4 跳,相对路径相对包含文件解析);`/context` 查看本会话**实际加载**了什么。

> 官方原话:"All discovered files are concatenated into context rather than overriding each other... Within each directory, CLAUDE.local.md is appended after CLAUDE.md, so your personal notes are the last thing Claude reads."

### 1.3 auto memory:索引全量 + 正文按需(just-in-time)

存储:`~/.claude/projects/<project>/memory/`,`<project>` 由 git 仓库派生,**同一 repo 的所有 worktree 和子目录共享一个 memory 目录**;机器本地、不跨机器。

recall 机制(核心):

- **MEMORY.md 是索引**,每会话开始**只加载前 200 行或 25KB(取先到者)**;超出部分下次加载被丢弃。
- **topic 文件**(如 `debugging.md`、`api-conventions.md`)**不在启动时加载**,Claude 用标准文件工具按需读取。
- 写带 YAML frontmatter 的 memory 时,Claude Code 记 `modified` 字段(ISO 8601);**绝不为无 frontmatter 的文件添加 frontmatter**;frontmatter 与 HTML 注释在加载前剥离,不计入限额。

> 官方原话:"The first 200 lines of MEMORY.md, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start."

**设计哲学**:这是 just-in-context 的典范--索引全量进上下文(让 Claude 知道"有什么"),正文按需读(用到才取)。和 MemGPT 的"主存 vs 外存"、LangGraph 的"thread state vs store"是同一思想。

### 1.4 Claude.ai 消费级 memory(2025-09 发布)

2025-09-11 发布(Team/Enterprise),10-23 扩展到 Pro/Max。**project-scoped**:每个 project 有独立 memory 空间和专用 project summary;memory 构建为一组**按类别组织的独立条目**,实时读写(非固定每日计划);"搜索过往对话"用 RAG,以 tool call 形式出现。控制:Pause memory(保留但不新建)/ Reset memory(永久删除,不可撤销);Incognito chat 不存 memory。

### 1.5 API 侧两套机制

- **Memory tool(GA,Messages API)**:客户端实现的文件式记忆。配置 `{"type": "memory_20250818", "name": "memory"}`(name 必须为 `memory`,无需 input schema)。Claude 在 `/memories` 目录下 create/view/str_replace/insert/delete/rename,**客户端侧执行**(Claude 只请求文件操作,应用返回 tool_result)。支持 just-in-time 召回。Claude 4+ 可用。**自动注入 MEMORY PROTOCOL**(见 §2.3)。
- **Memory stores(Beta,Managed Agents)**:workspace 级、为 Claude 优化的文本集合;attach 到 session 时挂载进 sandbox。限制:单条 100kB(~25k tokens)、单 store 2000 条、单会话最多 8 store;**结构化为多个小而聚焦的文件,而非少数大文件**。冲突解决用 `content_sha256` 乐观并发;每次改动生成不可变 **memory version**(审计 + 时间点恢复)。

### 1.6 官方最佳实践:什么该记、什么不该记

**Include / Exclude 对照表**(直接可照做):

| 该记(Include) | 不该记(Exclude) |
|---|---|
| Claude 猜不到的 Bash 命令 | Claude 读代码就能推断的 |
| 与默认不同的代码风格规则 | 标准语言约定 |
| 测试指令与首选 test runner | 详细 API 文档(改为链接) |
| 仓库礼仪(分支/PR 约定) | 频繁变动的信息 |
| 项目特定架构决策 | 长解释/教程 |
| 开发环境怪癖(必需 env var) | 逐文件代码库描述 |
| 常见 gotcha/非显然行为 | "write clean code" 之类自明实践 |

**何时往 CLAUDE.md 加**:Claude 第二次犯同样错;code review 抓到 Claude 本应知道的点;你打了和上次一样的纠正;新队友需要同样 context 才能上手。

**怎么写好**:Size(单文件 <200 行)、Structure(markdown 标题+列表)、Specificity(具体到可验证,如 "Use 2-space indentation" 而非 "Format code properly")、Consistency(定期移除过时/冲突)。

> 官方原话:"For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"

**怎么管理 auto memory**:Claude 不每次都存,基于"对未来对话是否有用"决定;MEMORY.md 接近限额时精简(每条一行、细节移 topic 文件、合并/丢弃 stale);`/doctor` 提议裁剪--删掉 Claude 能从代码推断的(目录布局、依赖列表、架构概览),保留 pitfalls、rationale、与工具默认不同的约定。

### 1.7 memory 与 context window 的关系

- **context 非指令**:CLAUDE.md 作为"系统提示之后的 user message"投递,无严格合规保证;要硬阻断用 PreToolUse hook。
- **just-in-time 召回**:不全量塞;memory tool 明确"agent records what it learns in memory files and reads them back on demand"。
- **compaction 后存活表**(关键):

| compaction 后 | 状态 |
|---|---|
| System prompt / output style | 不变 |
| Project-root CLAUDE.md + unscoped rules | 从磁盘重新注入 |
| Auto memory | 从磁盘重新注入 |
| **path-scoped rules(`paths:` frontmatter)** | **丢失**,直到再读匹配文件 |
| **子目录 nested CLAUDE.md** | **丢失**,直到读该子目录文件 |
| Invoked skill bodies | 重新注入(每 skill 上限 5000 token,总 25000) |

> 官方原话:"Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills... The context window is the most important resource to manage."

**§1 观点提炼**:官方把记忆定位为"被治理的 context"而非"知识库"--所以才有 200 行限额、/doctor 裁剪、just-in-time、compaction 存活表。记忆越多 ≠ 越好;**最小高信号 token 集**才是目标。

---

## 二、复杂 agent 架构下的 memory 使用与调优

### 2.1 多 agent 记忆流转:隔离 + 浓缩回传

orchestrator-worker 模式:lead 分析 query、制定策略、**把计划存入 memory 持久化**(因 context 超 200k 会被截断),并行 spawn 专门 subagent;subagent 各自用搜索工具迭代探索,**返回 1,000-2,000 token 的浓缩摘要**(可能消耗数万 token 探索,但只回传精华);lead 综合后返回用户。

**两个关键设计**:

1. **subagent 产物落文件系统,只回传轻量引用**--避免大输出在对话历史里反复复制(防"传话游戏")。
2. **context 接近上限时 spawn 全新 subagent(clean context)**,靠 careful handoff + 外部 memory 保持连续性。

> 官方原话:"Each subagent might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)... the detailed search context remains isolated within sub-agents, while the lead agent focuses on synthesizing and analyzing the results."

### 2.2 context engineering:context 是有限资源

- **context rot**:context 越长,模型准确召回能力越下降(所有模型都有);context 是边际收益递减的有限资源。
- **attention budget**:transformer 中每个 token 关注所有其他 token,n 个 token 产生 n² 关系;长 context 把注意力"拉稀"。
- **核心原则**:"finding the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome"。
- **何时塞进 context vs 外部记忆**:知识库 <200k tokens(约 500 页)直接全塞(配 prompt caching);超出用 RAG / 外部记忆。
- **just-in-time**:agent 只持轻量标识符(文件路径、stored query、链接),运行时用工具动态载入。Claude Code 对大库写 targeted query、存结果、用 head/tail 分析,从不全量载入。
- **compaction 调参**:先最大化 recall(摘要别漏关键),再提升 precision(去冗余);最低成本的压缩是"清理历史深处的 tool 原始结果"。
- **按任务选技术**:compaction(多轮来回)/ note-taking(有里程碑的迭代开发)/ multi-agent(并行探索研究)。

> token 经济现实:"agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats."--多 agent 本质是"花足够 token 解决问题",只对高价值任务划算。

### 2.3 memory 调优策略

- **structured note-taking(agentic memory)**:agent 定期把笔记写到 context 外的 memory,需要时拉回(如 Claude Code to-do list、自定义 NOTES.md)。
- **MEMORY PROTOCOL**(memory tool 自动注入系统提示):**开工前先 view memory 目录**;边做边记;**假设随时会被中断**(未记录即丢失)。
- **去重 / 防尸体 / 防膨胀**:保持 memory up-to-date、连贯、有组织;可重命名或删除不再相关的文件;**非必要不新建文件**;单条 100kB、单 store 2000 条;**结构化为多个小而聚焦的文件**。
- **冲突解决**:`content_sha256` 乐观并发--更新时传 hash 前置条件,不匹配则重新读取重试。
- **遗忘 / 清理**:定期清理长期未访问的 memory;跟踪文件大小、防过大、支持分页。
- **召回相关性**:传统 RAG 切分会破坏上下文;**Contextual Embeddings + Contextual BM25** 把检索失败率降 49%(加 reranking 降 67%);BM25 抓精确匹配(错误码、ID),embedding 抓语义。
- **安全**:处理不可信输入时用 `read_only`(防 prompt injection 写恶意内容进 store);所有操作限制在 `/memories` 目录,校验路径防目录穿越。

### 2.4 生产级调优经验(Anthropic 自家踩坑)

- **模型分档**:Opus lead + Sonnet subagent 比单 Opus 在内部研究 eval 高 **90.2%**。
- **按复杂度缩放 effort**:简单查事实 1 agent + 3-10 次工具调用;直接对比 2-4 subagent 各 10-15 次;复杂研究 >10 subagent 且分工明确。早期踩坑:简单 query 就 spawn 50 个 subagent、无止境搜不存在的源。
- **委托质量**:每个 subagent 需 objective + output format + 工具/来源指引 + 清晰任务边界;否则重复劳动、留空、漏信息。
- **工具描述即成败**:坏描述把 agent 引向歧途;自建 tool-testing agent 反复用 flawed MCP 工具并重写描述,使后续 agent 任务完成时间降 **40%**。
- **并行化**:lead 并行起 3-5 subagent + subagent 并行用 3+ 工具,复杂 query 研究时间降 **90%**。
- **长程 harness**(关键,解决"one-shot 倾向"与"误判完成"两类失败):
  - **initializer agent**(首会话专用):建 `init.sh`、`claude-progress.txt`、feature list、初始 git commit。
  - **coding agent**(后续):读 progress + git 历史快速上手,**一次只做一个 feature**,结束前 git commit(描述性 message)+ 写 progress 摘要;可用 git 回滚坏改动。
  - **状态文件用 JSON 而非 Markdown**(模型更不容易误改/覆盖 JSON);用强措辞禁止删改测试。

### 2.5 subagent 的 memory 边界

- **每个 subagent 独立 context window + 独立 system prompt + 独立工具/权限**;看不到主对话历史、已 invoke 的 skills、已读文件(fork 例外)。
- **主对话的 auto memory 不加载进 subagent**(fork 例外);subagent 可通过 frontmatter `memory` 字段拥有自己独立的 memory 目录:
  - `user` -> `~/.claude/agent-memory/<name>/`
  - `project` -> `.claude/agent-memory/<name>/`(可经版本控制共享,**推荐默认**)
  - `local` -> `.claude/agent-memory-local/<name>/`(项目级但不应入库)
- **内置 Explore/Plan subagent 故意跳过 CLAUDE.md 和父会话 git status**(保持快速廉价);其他 subagent 加载两者。
- subagent 限定单会话内;并行独立会话用 background agents;会话间通信用 agent teams。

**§2 观点提炼**:多 agent 的记忆问题**不是"共享一个大记忆",而是"更聪明的隔离与浓缩"**--subagent 在自己 context 里烧 token,只把精华回传;主 agent 与 subagent 的 memory 边界要清晰,否则就是传话游戏。长程任务靠"状态文件 + git commit + 增量推进",不靠"一个 agent one-shot 到底"。

---

## 三、论文与落地项目的 memory 设计理念(拓展)

### 3.1 记忆分类共识:CoALA 四分法(被广泛采纳)

CoALA(Cognitive Architectures for Language Agents,[arxiv 2309.02427](https://arxiv.org/abs/2309.02427))从认知科学给出被后续广泛引用的框架:

| 类型 | 内容 | 本地对应 |
|---|---|---|
| **working** | 当前上下文 | 会话 context |
| **semantic** | 事实/知识 | vault 调研文档 |
| **episodic** | 经历/过往动作 | auto-memory 的 feedback/project |
| **procedural** | 指令/系统 prompt/skills | CLAUDE.md / skills |

action space 区分**内部记忆操作**(读写反思记忆、检索)与**外部环境操作**(工具调用)。LangGraph 官方文档明确引用 CoALA 作为 memory 类型划分依据。

### 3.2 记忆操作四件套:write / read / reflect / forget

- **write**:写入/提取(Mem0 的 extract/consolidate)
- **read**:检索(recency×importance×relevance 等)
- **reflect**:反思/合成(Generative Agents 的 reflection、Letta 的 dreaming)
- **forget**:淘汰/截断(LlamaIndex 的 priority 截断、compaction)

**只写不整是反模式**--没有 reflect 与 forget 的记忆会膨胀、漂移、召回打架。

### 3.3 检索策略:三因子 → 图 → 时序

- **三因子加权**(Generative Agents,[arxiv 2304.03442](https://arxiv.org/abs/2304.03442)):recency(近期)× importance(LLM 打分)× relevance(语义相似度)。消融证明 observation/planning/reflection 三组件缺一不可。
- **分层搬运**(MemGPT,[arxiv 2310.08560](https://arxiv.org/abs/2310.08560)):把 LLM context 类比 OS 内存,main context(主存)与 archival memory(外存)间搬运页面;LLM 即 OS,自己管理内存分层。
- **图结构 + 时间感知**(Zep/A-MEM/GraphRAG):Zep([arxiv 2501.13956](https://arxiv.org/abs/2501.13956))的 Graphiti 是时序知识图谱,事实变化不丢旧值,cross-session 综合最强(+18.5% accuracy、-90% latency);A-MEM([arxiv 2502.12110](https://arxiv.org/abs/2502.12110))用 Zettelkasten 思想做 agent 式自组织记忆,新记忆触发历史记忆更新;GraphRAG([arxiv 2404.16130](https://arxiv.org/abs/2404.16130))用图索引解决"全局性问题"(QFS 而非检索)。

### 3.4 演进方向:从被动存取到 agent 式自组织

- **Reflexion**([arxiv 2303.11366](https://arxiv.org/abs/2303.11366)):不更新权重,改用语言反馈做"强化";反思文本存 episodic memory buffer,HumanEval 91% pass@1。
- **Mem0**([arxiv 2504.19413](https://arxiv.org/abs/2504.19413)):可扩展 memory-centric 架构,LLM-as-Judge 比 OpenAI 高 26%,p95 延迟降 91%、token 成本省 90%+;提供图记忆变体。
- **Letta(MemGPT 产品化)**:靠主动管理自身上下文学习(在 token 空间建立 identity/memory/continuity 的持久表征)而非更新权重。核心 **Context Constitution**:决定放什么、什么顺序、什么粒度、留多久。**MemFS**(git 版本化 memory 文件系统)+ **Dreaming**(后台 subagent 回顾对话、合并经验、更新记忆)+ `/doctor`(审计漂移/重复/token 占用)。

### 3.5 落地 coding agent 的 memory 设计对比

| 项目 | memory 机制 | 核心理念 |
|---|---|---|
| **Claude Code** | CLAUDE.md(分层)+ auto memory(just-in-time)+ `.claude/rules/`(path-scoped) | 双系统:人写规矩 + AI 写事实,都是 context |
| **Cline** | Memory Bank 6 文件(brief/productContext/activeContext/systemPatterns/techContext/progress) | "记忆会话间完全重置,完美文档是唯一续作依据,每次任务必读全部" |
| **Codex CLI** | AGENTS.md 链(global→project→override,每目录至多一文件,32KiB 上限) | 从 git root 向下拼接,越近 cwd 越优先 |
| **Windsurf** | Memories(workspace 级,按相关性检索)+ Rules(global+workspace)+ system-level rules(企业不可删) | 自动生成 + 手写规则 + 组织基线三层 |
| **Aider** | `CONVENTIONS.md` read-only + prompt caching | 最简:read-only 文件 + chat history |
| **Devin** | Knowledge(semantic)+ Playbooks(procedural) | 语义记忆 + 过程记忆分离 |
| **Cursor** | Rules + Skills + Subagents + Hooks | 旧"Memories"被 Rules 体系取代(正文 SPA 未提取,待人工核验) |

**共识**:生产 coding agent 普遍收敛到"**组织基线 + 项目共享(版本控制)+ 个人本地(gitignore)**"三层规则。

### 3.6 通用 agent 框架的 memory 模块

| 框架 | 短期 | 长期 | 差异化 |
|---|---|---|---|
| **LangGraph** | thread state + checkpointer | namespace store | semantic 分 Profile(单文档)vs Collection(原子事实集合,recall 更高) |
| **LlamaIndex** | FIFO 消息队列(token_limit 控制) | Memory Block(Static/FactExtraction/Vector) | block priority 截断,priority=0 永不裁剪 |
| **CrewAI** | crew 共享 | 层级 scope(类文件系统) | 复合打分(similarity×recency×importance)+ consolidation(相似度 0.85 阈值)+ MemorySlice 只读跨分支 |
| **AutoGen** | model_context | Memory 协议(add/query/update_context) | 最薄,RAG 注入式 |

**§3 观点提炼**:所有正经方案都收敛到 **CoALA 四分法 + 检索打分 + 四操作**;真正的差异化在"长期记忆怎么组织与演化"--单 profile vs 原子事实集合 vs 图 vs 时序 KG。演进方向是从"被动存取"到"agent 式自组织 + 后台反思"。

---

## 四、多 agent 生产级 memory 设计理念与最佳实践

### 4.1 共享记忆 vs 私有记忆

- **CrewAI** 给出最显式模型:`MemoryScope`(子树=私有上下文,如 researcher 只看 `/agent/researcher`)与 `MemorySlice`(跨分支组合,**只读 slice**--agent 读多个分支但不可写共享区,读-写 slice 需显式指定写哪个 scope)。典型模式:researcher 私有 findings + writer 读共享 crew memory。
- **Cline Agent Teams**:共享 task board + inter-agent mailbox(点对点消息)+ mission log(活动历史),team state 持久化于 `~/.cline/data/teams/[team-name]/`,可跨会话 resume。
- **Claude Code**:subagent 各自维护自己的 auto memory(per-subagent persistent memory)。
- **Letta**:一个 agent、多个独立 message thread、**共享同一 MemFS 记忆**;同一 agent+记忆可跨机器、跨终端/桌面/Web/IM 通道迁移。

### 4.2 持久化与一致性(生产级分水岭)

- **持久化形态多样**:git 版本化文件系统(Letta MemFS,可 diff/回滚/同步)、DB checkpoint(LangGraph)、namespace store、时序知识图谱(Zep Graphiti)、memory 层服务(Mem0)。
- **一致性/演化机制**:CrewAI consolidation(相似度阈值 + LLM 决定 keep/update/合并);Letta **dreaming**(后台 subagent 回顾对话→合并经验→更新记忆,在 N 条消息后或 compaction 时触发)+ `/doctor` 审计漂移/重复/token 占用;Zep 用时序边维护"历史关系"(事实可随时间变化而不丢旧值);API memory stores 的 `content_sha256` 乐观并发 + 不可变 version。

### 4.3 生产级架构理念(综合)

1. **记忆作为独立层/服务**:Mem0(可调用 memory 层)、Zep(memory layer service)、Letta(harness + MemFS)--趋势是把记忆从应用逻辑中剥离成可独立运维、可观测、可演化的层。
2. **Context Constitution**(Letta):记忆本质是"治理上下文窗口"--决定放什么、什么顺序、什么粒度、留多久;agent 靠管理上下文学习而非改权重。
3. **企业三层规则**:Windsurf system-level rules(不可被终端用户改)、Claude Code managed policy、Codex AGENTS.md global→project→override 链、Devin enterprise playbooks--生产系统普遍需要"组织基线 + 团队/项目覆盖 + 个人本地"三层。
4. **时间维度是生产刚需**:Zep 强调 RAG 只能静态检索,企业要 cross-session 综合 + 时序推理;时序 KG 是 2025 年的明确方向。

### 4.4 memory vs RAG vs fine-tuning(工程取舍)

| 机制 | 改什么 | 频率 | 适用场景 |
|---|---|---|---|
| **memory** | 状态/偏好/经历 | 运行时,高频演化 | 长期多会话一致性、个性化、agent 自我改进 |
| **RAG** | 接外部静态知识 | 按需检索 | 静态文档语料、全局性问题(GraphRAG) |
| **fine-tuning** | 能力/风格(权重) | 低频 | 固化领域深知识/风格,变化频率低,有训练数据 |

**行业方向(2023-2026)明确倾向"上下文/记忆管理"替代微调**:Letta(learn by managing context, not updating weights)、Reflexion(reinforce not by updating weights, but through linguistic feedback)、Mem0(structured memory 比 full-context 省成本、比微调灵活)。**能用 memory/RAG 解决的别上微调**--schema 频繁变更场景尤其如此(本库 nl2sql 的"LLM+schema 上下文"优于微调即是此实践)。

**§4 观点提炼**:生产级的分水岭是**"记忆能否被独立运维、可观测、可演化"**--业余的只写不整,生产的有审计、有反思、有时序、有冲突解决。共享 vs 私有、时序不覆盖旧值、后台反思,是三个最关键的生产设计。

---

## 五、结合本地环境(泛化建议)

### 5.1 本地三层映射 CoALA 四分法

| CoALA 类型 | 本地载体 | 现状 |
|---|---|---|
| working | 当前会话 context + MEMORY.md 前 200 行 | 自然遵守 |
| semantic | vault(8 类调研文档) | 厚 |
| episodic | auto-memory 的 feedback/project 条目 | 厚(home 20 条 + vault 4 条) |
| procedural | CLAUDE.md + skills | **偏薄**(vault CLAUDE.md 有,全局无) |

**诊断**:本地记忆偏科--semantic/episodic 厚,procedural 薄。可补全局 `~/.claude/CLAUDE.md` 或更多 skills 沉淀跨项目工作规矩。

### 5.2 本地机制印证官方设计

- **MEMORY.md 前 200 行/25KB** = 官方 just-in-time(本机已自然遵守,home MEMORY.md 20 行未触限)。
- **auto-memory 按启动目录隔离** = 官方 per-repo 机制(home 启动→`-Users-wyf/memory/`;vault 启动→`-Users-wyf-Desktop-code-document/memory/`,互不可见)。**治理选择**:通用偏好集中 home + 项目状态写进对应项目目录(见旧版 §4.2,机制仍成立)。
- **两套 wikilink 不互通** = auto-memory 的 `[[name]]` 与 vault 的 `[[文件名]]` 是两个独立网络,跨层只能用路径引用。
- **vault 的 ingest/lint 闭环** = 官方"write/reflect/forget"的本地版(lint = reflect + forget)。

### 5.3 4 个 MCP 在记忆体系中的角色

| MCP | 记忆类型 | 角色 |
|---|---|---|
| obsidian-vault | semantic | vault 物理通道(长期知识库) |
| tavily | working | 即用即弃的工作记忆(搜索结果) |
| mysql-local | semantic(结构化) | 只读结构化长期记忆 |
| macos-mcp | (感知/执行) | 非记忆本身,是感知/执行通道 |

**原则**:能持久化的(vault/mysql)当长期记忆用;即用即弃的(tavily)当工作记忆,不落盘除非提炼成 vault;本机操作(macos)操作过的东西若有价值再落 vault/auto-memory。

### 5.4 泛化建议(可落地)

1. **补"反思/审计"闭环**:定期 lint vault = Letta dreaming 的本地版;auto-memory 定期查重/清尸体(官方 `/doctor` 精神)--本机已用 SUPERSEDED 横幅纠偏 `long-task-execution-time-feedback`,即此实践。
2. **多 agent 边界意识**:subagent **不继承主对话 auto memory**(官方明确)--所以调研 subagent 各自独立,主 agent 亲自整合(本次重做即如此,3 subagent 搜集 + 主 agent 一次性整合,避免 Demis 式"6-agent 并行后整合失败、重点被生平淹没")。subagent 只回传结构化摘要,不回传全文。
3. **生产三层规则本地化**:本机已有 user(无)+ project(vault CLAUDE.md)+ local(无);若团队协作可加 managed policy 做组织基线(不可被排除)。
4. **记忆均衡审视**:按 CoALA 四分法看本地是否偏科--procedural 偏薄,可补;auto-memory 多 feedback/project,确保每条带 Why/How(官方"具体到可验证"精神)。
5. **context engineering 意识**:CLAUDE.md <200 行(官方硬指标);auto-memory MEMORY.md 精简(每条一行 + topic 文件);调研文档也要 just-in-time(索引全量、正文按需)--vault 的 INDEX/_index 设计即是。
6. **能用 memory/RAG 别上微调**:本库 nl2sql 已是"LLM+schema 上下文"优于微调的实践,与行业方向一致。
7. **长程任务用 initializer + coding agent 模式**:状态文件用 JSON 优于 MD(模型更不易误改),git commit 做检查点,一次一个 feature--可借鉴到 vault 的多会话调研。

---

## 六、速查与红线

**核心公式**:记忆 = 被治理的 context(不是知识库);四分法 working/semantic/episodic/procedural;四操作 write/read/reflect/forget;检索 recency×importance×relevance。

**多 agent**:隔离 + 浓缩回传(1-2k token 摘要),不共享大记忆;subagent 不继承主对话 auto memory(fork 例外);产物落文件系统只回传引用;长程任务靠状态文件 + git commit + 增量推进。

**生产三层**:组织基线(managed,不可改)+ 项目共享(版本控制)+ 个人本地(gitignore)。

**取舍**:memory(状态/偏好)/ RAG(静态知识)/ fine-tuning(能力/风格);能不上微调就不上。

**官方限额**:CLAUDE.md 单文件 <200 行;MEMORY.md 前 200 行/25KB;memory store 单条 100kB、单 store 2000 条、单会话 8 store;结构化为多小文件。

**红线**:不存密钥/token;不记 repo 已有(代码结构/git history/CLAUDE.md 已写);不记一次性临时上下文;recall 是背景非指令(引用前验证文件/函数/flag 是否还在);feedback/project 必带 Why/How;要硬阻断动作用 PreToolUse hook 而非 CLAUDE.md。

---

## 附 A:信源清单

**L0 官方一手**
- Claude Code memory(分层/auto memory/@导入//memory//init): https://code.claude.com/docs/en/memory
- Claude Code context window(compaction 存活表): https://code.claude.com/docs/en/context-window
- Claude Code best practices(Include/Exclude 表): https://code.claude.com/docs/en/best-practices
- Claude Code subagents(memory 字段/隔离): https://docs.claude.com/en/docs/claude-code/subagents
- API memory tool(GA/MEMORY PROTOCOL/安全): https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool
- API memory stores(Beta/版本审计): https://platform.claude.com/docs/en/managed-agents/memory
- Anthropic multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic effective context engineering: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic effective harnesses for long-running agents: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic building effective agents: https://www.anthropic.com/engineering/building-effective-agents
- Anthropic contextual retrieval: https://www.anthropic.com/engineering/contextual-retrieval
- Bringing memory to Claude(2025-09-11): https://www.anthropic.com/news/memory
- Claude.ai memory 帮助中心: https://support.anthropic.com/en/articles/11817273

**L1 论文(arxiv)**
- MemGPT 2310.08560 · Generative Agents 2304.03442 · Reflexion 2303.11366 · CoALA 2309.02427 · A-MEM 2502.12110 · Mem0 2504.19413 · Zep 2501.13956 · GraphRAG 2404.16130 · Memory Survey 2404.13501

**L2 项目 docs**
- Cline Memory Bank / Agent Teams · Codex AGENTS.md · Windsurf Cascade Memories · Aider conventions · Devin Knowledge/Playbooks · Cursor docs(SPA 正文未提取)· Letta memory/MemFS/Context Constitution · LangGraph/LlamaIndex/AutoGen/CrewAI memory

**未核实(如实标注)**
- Cursor `.cursor/rules/*.mdc` frontmatter 与"Auto/Agent-Requested/Always"三类规则:官方 docs 为 SPA 无法机器提取,Web Archive 临时封禁,未做一手核实,建议人工在 docs.cursor.com 验证。
- Devin 内部短期会话记忆机制:闭源,未公开文档,仅 Knowledge/Playbooks API 可见。
- `#` 快速记忆快捷键语法:官方 memory/cli-reference/interactive-mode/common-workflows 页面均未见专门记载,官方仅以"ask Claude to remember something"描述。

---

## 附 B:本文 self-check

- ✅ 从官方源头出发(§1 全部官方一手,带原话引述),非直接本地实测
- ✅ 复杂 agent 架构下使用与调优(§2 context engineering + 多 agent 流转 + 生产经验 + subagent 边界)
- ✅ 论文与落地项目拓展(§3 CoALA 四分法 + 9 篇论文 + 7 个 coding agent + 4 个框架对比)
- ✅ 多 agent 生产级设计理念(§4 共享/私有 + 持久化一致性 + 架构理念 + memory/RAG/微调取舍)
- ✅ 结合本地泛化(§5 CoALA 映射 + 机制印证 + 4 MCP 角色 + 7 条可落地建议)
- ✅ 遵循 vault frontmatter 规范,落盘 06-workflows,配套更新 `_index.md`/`INDEX.md`/`CHANGELOG.md`
