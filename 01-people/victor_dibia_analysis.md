# Victor Dibia 深度调研：从 LIDA 到 Microsoft Agent Framework，一位 Agent 平台架构师的思想演进

> 调研日期：2026-07-18
> 覆盖窗口：2025-07 至 2026-07（360 天）+ 完整背景履历
> 调研方法：4 个子 Agent 并行抓取（curl 静态抓取为主，WebSearch 在当前环境不可用）
> 信源：victordibia.com、newsletter.victordibia.com（Substack "Designing with AI"）、Google Scholar、arXiv、GitHub、Microsoft devblogs、QCon/AI.Engineer 演讲 PDF

---

## 0. 核心结论前置

**一句话定位**：Victor Dibia 是微软 Core AI 的 Principal Research Software Engineer，AutoGen / Microsoft Agent Framework 的核心开发者，《Designing Multi-Agent Systems》一书作者。他的独特性在于**用 HCI/UX 视角做 agent 基础设施**--在满世界讲"怎么调 prompt、怎么加 agent"时，他讲"用户怎么知道 agent 能做什么、怎么追溯、怎么叫停、怎么知道这次委派值不值"。

**贯穿始终的 DNA**：以 HCI 敏感性构建"增强人类"的开源工具，几乎每个项目都是"GitHub 库 + live demo + 博文 + 论文"四件套。基底技术在变（RNN → LLM → 多 agent），但"人因 + 开发者工具 + 开源 + 可交互 demo"的方法论 14 年没变。

**关于"编码消失论"的核实结论（重要）**：
本次调研的触发点是一段观点——"3-5 年内编码可能基本消失：agents 替代大部分软件工程执行，人们戴带摄像头的眼镜让 agent 理解完整工作上下文，开完会回到桌前 agent 已经把任务实现了"。

**核实结果：在 Victor Dibia 的 8 篇 newsletter 全文（覆盖全部反思/编码类高价值文章）中，针对 glasses / camera / 3-5 year / disappear / end of coding / back at desk / obsolete 等关键词 grep，均无命中。** 且该表述与他 newsletter 一贯的**审慎/反思语调不一致**——他在 newsletter 中反复强调工程纪律、安全、agentic noise、能动性丧失、成瘾式依赖，从不做"编码将消失"的激进预测。

判断：
- 若该观点确属他，**极可能出自播客/访谈的口头表述**（newsletter 是书面、审慎的；口头可能更放松），但 curl-only 约束下无法抓取播客（X/Twitter @vykthur、LinkedIn、YouTube 视频正文均需登录或无文字）。
- 亦**不排除为转述/误植**——即他人观点被误记到他头上。
- 他真正说过、方向相关但更审慎的版本见 §5（如"AI writes the code, AI reviews the code, and the human pays $25 to be removed from the loop"）。
- **如需最终证实**，建议用登录态浏览器查 @vykthur 的 X 时间线、或 Latent Space / Practical AI / AI.Engineer 等播客的嘉宾列表。

---

## 1. 背景履历

### 教育
- **City University of Hong Kong（2012–2016）**：Information Systems 博士，方向 Quantitative User Behaviour / HCI。香港研究资助局 **HKPFS 学者奖**。博士论文研究**软件众包竞赛中的开发者贡献行为**——影响参与的因素、激励对参与行为的影响、问题求解过程。这是他"理解人类行为"方法论的源头。
- **Carnegie Mellon University, Information Networking Institute（2009–2011）**：Information Networking 硕士。

### 职业时间线
| 时间 | 机构 | 角色 | 关键产出 |
|---|---|---|---|
| 早期 | 西非创业公司 / AIT(希腊) / MIT Global Startup Labs | 创始人/研究员/技术负责人 | — |
| 2016.04–2019.01 | IBM Research, Yorktown Heights | Research Staff Member | **Data2Vis**（首个神经网络自动可视化，IEEE CG&A Best Paper）、**TJBot**（开源 DIY AI 套件）、**HandTrack.js**（浏览器内手势追踪） |
| 2019.01–2021.09 | Cloudera Fast Forward Labs | Principal Research Engineer | **NeuralQA**（BERT 问答）、Applied ML Prototypes（AMPs）成客户接入标准 |
| 2021.10–2025.05 | Microsoft Research – AI Frontiers Lab | Principal Research SWE | **AutoGen** 核心开发（52K★, 5.9M 下载）、**AutoGen Studio** 创建者、**Magentic-One** 共同作者、**LIDA** 创建者（ACL 2023，被 Excel/Fabric/PowerBI 采用）、改进 GitHub Copilot 离线评测 |
| 2025.05–至今 | Microsoft Core AI | Research & Engineering Lead | **Agent Optimization Service**（Azure 服务数十万客户）、主导 **SK + AutoGen 合并为 Microsoft Agent Framework**、**DevUI**（470K 下载，Ignite 2025 六场 session） |

### 身份与荣誉
IEEE Senior member；Google Developer Expert in ML；Google Certified Professional（Data Engineer、Cloud Architect）。
**Google Scholar**：总引用 1643，h-index 15，i10-index 21。
**Best Paper**：IEEE CG&A（2020，Data2Vis）、IEEE VIS Honorable Mention（2018）、AAAI Best Technical Demo（2018）。
**专利**：7 项授权 + 2 项在审（含 LIDA 自动可视化、数据健康评估、代码生成评测等）。
**著作**：《Designing Multi-Agent Systems》Amazon Generative AI 类 #1 New Release。

> 履历来源：https://victordibia.com/cv/

---

## 2. 思想演进脉络（7 阶段）

演进逻辑总纲：**HCI/众包（理解人）→ 数据可视化自动化（Data2Vis→LIDA）→ LLM agent（AutoGen）→ 多 agent 平台 + 人本 agent UX**。LIDA（2022.08）是枢纽——他亲手把 LIDA 的"LLM 驱动可视化管线"单 agent 模式扩展为多个协作 agent，转向不是断裂而是放大。

### 阶段一（2012–2016）PhD：HCI、众包、可穿戴
- 核心关切：理解人类行为。博士论文研究众包竞赛开发者贡献；Foqus（2014，ASSETS）用智能手表 + 正念辅助 ADHD。
- **源头**：后续所有 agent 工作都保留了对用户行为与可访问性的关注。

### 阶段二（2016–2019）IBM Research：自动可视化 + 浏览器内 ML + 创客套件
- **Data2Vis**（seq2seq RNN 自动生成可视化）——"自动化分析师"线索的起点；**TJBot**（民主化 AI 创客套件）；**HandTrack.js**（TF.js 浏览器内实时手势追踪）。
- **转折点**：从"研究人类行为"转向"用 ML 工具增强人类"，数据可视化成为连接 HCI 与 ML 的桥梁。

### 阶段三（2019–2021）Cloudera FFL：应用 ML 工程化、NLP
- NeuralQA（EMNLP 2020）、SignVer、Anomagram/ConvNet Playground（交互式 ML 教学工具）。
- **模式确立**：构建"可用开源库 + 交互 demo"来教开发者——开发者工具心智在此固化。

### 阶段四（2021–2023）MSR：LLM 登场，LIDA 是转折枢纽
- 2021.10 加入 MSR AI Frontiers。**LIDA（2022.08）**：用 LLM 自动生成语法无关的可视化与信息图（ACL 2023）。
- **关键转折**：他在 agentux.pdf 第 1 页明确标注"How I got into Agents .. August 2022 | LIDA"——LIDA 用 LLM 替换 Data2Vis 的 RNN，让 LLM 驱动"目标生成 → 可视化执行 → 信息图 → 评测"全流程，本质已是一个单 agent 系统。从"自动化单一任务"到"LLM 编排多步骤/工具"是自然延伸。
- 同期改进 GitHub Copilot 评测（ACL 2023）——代码场景的人机对齐。

### 阶段五（2023–2024）多 agent 转向：AutoGen + Studio + Magentic-One
- 2023.09 AutoGen（他标注的 agent 起点）。核心开发，主导 v0.4 的 async-first 设计。
- AutoGen Studio（2024.03，EMNLP 2024）：无代码构建/调试多 agent；Magentic-One（2024.11）：通用多 agent 参考架构。
- **思想结晶**——workflow vs agent 之分开始成形。

### 阶段六（2024–2025）整合期：书 + UX 原则 + 框架统一
- 「10 Reasons Your Multi-Agent Workflows Fail」（QCon 2024.11）——失败实践分类法。
- **UX Design Principles for Semi-Autonomous MAS**（AI.Engineer 2025.06）：4 条 UX 原则。
- 书《Designing Multi-Agent Systems》2025.11 交付：15 章、395 页、picoagents 从零构建。
- Interactive Debugging & Steering of MAS（CHI 2025）、Magentic-UI（人在环中）、AI Fatigue（CACM，反思 AI 高速发展的人性代价）。
- **核心关切转向**：人在环中、可靠性、何时**不该**用 MAS、AI 节奏对人性的冲击。

### 阶段七（2025–至今）Core AI：平台化整合
- 主导 SK + AutoGen 合并为 Microsoft Agent Framework；Agent Optimization Service；DevUI。
- **核心关切**：规模化生产级 agent 基础设施与开发者体验。

---

## 3. 产品思想体系（8 条核心理念）

### ① Workflow vs Agent 的判断（设计第 0 原则）
- **Workflow** = 确定性步骤 + 撒点 LLM 调用，可靠、可投产，但需预知精确解。
- **Agent/MAS** = LLM 驱动控制流，适合精确解未知的场景，以可靠性换自主性。
- "Know when to use a multi-agent approach!"是第 0 原则。任务复杂度四维 checklist：**Planning**（可分解到目标态）/ **Diverse Perspectives**（可映射不同领域专长）/ **Extensive Context**（每步需处理大量上下文）/ **Adaptive Solution**（动态环境、行动后才知道解）。
- 原文："most 'agents' in production are mostly workflows - a set of deterministic steps designed by an engineer with a few LLM calls sprinkled in... Multi-Agent Systems where LLMs drive control flow of execution, are suited to problem spaces where the exact solution is unknown."
- 出处：https://newsletter.victordibia.com/p/4-ux-design-principles-for-multi

### ② 构建流程：5 阶段、eval 驱动、agent 最后做
顺序：Goal definition → Baseline（非 agent 基线）→ **Tools（花最多时间）** → **Eval testbed** → Agent（最后）。
- "This comes last, not first!"——反对一上来就写 Agent 类。
- "I often see developers start the agent development process by immediately attempting to code up an Agent class... This is often a mistake."
- "about 70% of effort should be split between step 3 and 4 - across building your tools and tuning your evaluation harness."
- "Your agent is only as good as the tools you give it!"
- "Academic benchmarks, while helpful, are NOT your task."——必须针对自己任务建评测。
- **picoagents 的设计意图**：书的 Part II 带你从零构建 agent 框架，揭示 execution loop（model call → tool execution → model call，直到返回文本）。目的是**去黑箱化**——"Same Pattern, Different Frameworks"，同一执行循环在 MAF / Google ADK / LangGraph 下本质相同，先理解再选用框架。
- 出处：https://victordibia.com/pdf/victordibia_agentux.pdf

### ③ Agent anatomy：model + tools + memory，execution loop 是通用内核
- Agent = "an entity that can reason, act, communicate, and adapt to solve problems"。
- 三组件：model（推理）、tools（行动）、memory（短期对话历史 + 长期持久存储）。
- "an agent takes multiple steps (model call → tool execution → model call) within a single run. The loop continues until the model returns a text response instead of tool calls."
- 出处：https://victordibia.com/blog/agent-execution-loop/

### ④ AutoGen Studio：无代码/低代码原型化 MAS
降低门槛：rapidly build, test, share multi-agent solutions。源于维护 AutoGen 时观察开发者原型困难。设计意图：先原型，再毕业到代码。

### ⑤ Agent Framework（合并 AutoGen + Semantic Kernel 的逻辑）
- AutoGen（agent 编排、多 agent 对话）与 Semantic Kernel（规划、插件、企业集成）原本重叠/分叉 → 统一为一个框架，提供"stronger developer experience and better integration with Microsoft Foundry Agent Service"。
- 一个框架替代两个竞争框架，减少开发者困惑、合并工程力量。
- **DevUI**：chat interface + thread management + event tracing（展示 tool calls 与执行流）——把可观测性内建进开发闭环。

### ⑥ 半自主 MAS 的 4 条 UX 设计原则（他区别于纯工程视角的核心）
底层 MAS 三属性决定 UX 必须审慎：**Autonomy**（能做很多事）/ **Action**（有副作用）/ **Duration**（长时任务）。
- **Capability Discovery**：帮用户理解 agent 能做什么；逐项列能力、传达可靠性、基于上下文主动建议。
- **Observability & Provenance**：用户可观察/追踪 agent 行为；活动日志可视化、调试与溯源（提示：用 async generators）。
- **Interruptibility**：可暂停/恢复/取消；持久化 agent 与应用状态；提供反馈控制。
- **Cost-Aware Delegation**：传达 agent 行动成本；让用户决定 agent 何时行动；必要时委托回人类。
- 出处：https://victordibia.com/pdf/victordibia_agentux.pdf

### ⑦ 人在环中是一等公民
- Magentic-UI、Interactive Debugging & Steering（CHI 2025）——agent 必须可驾驭，不能 fire-and-forget。
- "Multiple agents collaborating, with autonomy increases the surface for errors and reliability issues. Like any other tool, they should be selected when they are the right tool for the job."

### ⑧ 开源 + 交互 demo 作为产品/分发哲学
- 几乎每个项目都是"GitHub 库 + live demo + 博文 + 论文"四件套（Handtrack.js、LIDA、NeuralQA、SignVer、Peacasso、Anomagram、ConvNet Playground、BlenderLM、picoagents）。
- 分发矩阵：newsletter（1600→8800 订阅）、YouTube"Designing With ML"频道（16 教程、~100k 观看）、自建数字销售平台（<$2/月运维）——"教学即产品"。

---

## 4. 最近 360 天 Newsletter 思想总结（四条主线）

Newsletter 名为 "Designing with AI"（Substack），Issue 编号到 #66（2026-06-22），近期频率每月 2-4 篇。窗口内 21 篇，抓取 8 篇全文。可清晰分为四条主线：

### 主线 A：Claude Code 深度拆解系列
他从使用者走向逆向工程师，把 Claude Code 当研究对象拆解：
- **执行循环** → **自建 agent**（Building Your Own Claude Code from Scratch）→ **Skills**（从零实现，100 行 Python）→ **上下文工程**（管理上下文增长、防早停）→ **500K 行源码逆向**。
- 重磅文章《Inside Claude Code》（2026-04-06）：Claude Code TypeScript 源码 2026-03-31 随 npm 包泄露，**513,216 行、1,884 文件、42 工具、90 feature flag；agent loop 仅约 1%（~1,700 行），其余 99% 是维持其存活的 harness**。
  - Prompt 是最大隐性工程投入：约 60,000 token 分布在 37 个工具 prompt + 系统 prompt + 压缩 prompt；**每条规则都是一个被编码的生产故障模式**——大规模 prompt 工程是反应式的，从生产数据发现而非第一性原理推导。
  - 上下文管理是三级流水线（预算→微压缩→全压缩）；工具结果 >50k 字符落盘留 2KB 预览。
  - **38,000 行（7.5%）用于权限/安全**；BashTool 10% 执行逻辑、90% 安全设施。每个自动恢复路径都需断路器（缺失的重试上限曾让 1,279 个会话各跑 50+ 次压缩失败，日浪费约 25 万次 API 调用）。
  - 90 个 feature flag 揭示多 agent 协调、后台记忆整合、验证 agent；压缩 fork 继承全部工具纯粹为命中 prompt cache。

### 主线 B：编码 agent 的工程纪律与反思
这是他最"审慎"的一面，也是与"编码消失论"语调最相关但方向相反的部分：
- **《/upgrade ... or ...》**（2025-10-27）：工作流被根本性改变——从"代码匠人"变成"交响乐指挥"，在多个 VS Code 窗口间 babysit Claude。与成瘾类比：coding agent 让人工作超过预期时长，"免费"委派进度的诱惑让人无法移开视线（移开就丢上下文、积累债务）。**Jevons 悖论**："AI 生产力增益不买时间，只买更多工作"；资深开发者估算 50% 时间写需求、10-20% vibe coding、30-40% "vibe fixing"修 AI 产生的 bug。命名**"能动性丧失"（agency loss）为 AI 疲劳的新形态**。"代理反转 / 尾巴摇狗"：我们是用 AI 建项目，还是在按 AI 能做什么来选项目？
- **《Vibe Coding With Engineering Discipline》**（2025-12-19）：METR 研究显示自主任务长度每 7 个月翻倍，GPT-5-Codex 自主跑 7+ 小时；但团队仍卡壳。实践：把 agent 当需 onboarding 的新工程师（CLAUDE.md <300 行、分层）、Spec-Driven Development（GitHub Spec Kit）、测试驱动（亲自写并完全理解测试，防 agent 删测试来宣布完成）。
- **《Use Coding Agents to Build Your Product. Don't Make Them Your Product.》**（2026-02-18）：不要把通用 coding agent 当产品交付，但要用它们建产品。两大问题：**安全**（本地 agent 有效是因为在用户信任边界内；移到服务器后"用户"变攻击者。Meta 的"Rule of Two"：agent 至多满足{处理不可信输入、访问敏感系统、改变状态/对外通信}中两项）；**业务专属性**（通用模型付"认知税"，领域 agent 只需 3-5 工具、200-500 token prompt，对比通用 678 行 prompt+23 工具，4-10x overhead）。

### 主线 C：微软生态
- **MCP for Software Engineers Part 1/2**（2025-07/08）→ **Microsoft Agent Framework = SK + AutoGen**（2025-10-01）→ **Agent Middleware**（2025-12-16）→ **Build 2026 全景**（2026-06-22）。
- Build 2026 文章自述他亲自参与 **Agent Optimization** 服务（公开预览）：从 eval 出发，自动搜索更优的 instructions/skills/tools/模型选择，返回排序后的 agent 候选；解决手工调优在数百生产 agent 上不可扩展的问题。

### 主线 D：思想性议题
- **《Is Scaling a Dead End?》**（2026-01-19）：回应 Sara Hooker《On Slow Death of Scaling》。认同 scaling 边际递减，但论证大规模不可避免——大基座模型是蒸馏/训练/验证未来高效小模型的关键基础设施。**"苦涩教训没死，它被摊销了。"** 小模型是大模型的衍生品（蒸馏需 teacher、合成数据需强生成器、RLHF 需强基座）。4 年间最高质量智能价格降了 400x。scaling 是设计特性，不是 bug。
- **《Agentic Noise》**（2026-03-30）：提出 **"agentic noise"概念**（出自其书第 13 章）：当 AI agent 加速双边平台一侧而另一侧仍为人速时，打破系统设计所依赖的假设。产销失衡实例：就业市场（AI 简历 vs AI 筛选，19% 误筛合格者，Mobley v. Workday 诉讼）、学术（NeurIPS 投稿 9.5k→23k；ICLR 2026 21% 审稿全 AI 生成）、社媒、出版、儿童内容"Elsagate 2.0"、GitHub OSS。**"信号失灵问题"**：人类用来导航内容的信号基础设施在源头被腐蚀。核心追问：**"AI 写论文又 AI 审稿，产出的是更好研究还是更高体量 churn？"** 本质是人类福祉与注意力问题。

---

## 5. 360 天重大事件时间轴

| 日期 | 事件 | 类别 | URL/出处 |
|---|---|---|---|
| 2025-07-02 | Newsletter《MCP for Software Engineers Part 1》 | 博文 | newsletter.victordibia.com |
| 2025-07-30 | **Magentic-UI 论文发表**（arXiv:2507.22358，窗口内唯一新论文） | 论文 | https://arxiv.org/abs/2507.22358 |
| 2025-10-01 | **Microsoft Agent Framework 首版 PyPI beta**（`1.0.0b251001`，合并 SK+AutoGen 起点） | 项目 | https://pypi.org/project/agent-framework/ |
| 2025-10-07 | devblog《Semantic Kernel and Microsoft Agent Framework》厘清二者关系 | 博文 | devblogs.microsoft.com/agent-framework/ |
| 2025-10-23 | MAF 企业级多 agent 编排博文 | 博文 | devblogs |
| 2025-10-27 | Newsletter《/upgrade ... or ...》（能动性丧失反思） | 博文 | newsletter.victordibia.com |
| 2025-11-14 | Newsletter《书出版：Two Years, 15 Chapters》 | 博文 | newsletter.victordibia.com |
| 2025（年内） | **书《Designing Multi-Agent Systems》出版**（Manning 解约后自出版，15 章 395 页 186 代码） | 书 | multiagentbook.com / Amazon B0G2BCQQJY |
| 2025-12-01 | MAF《Golden Triangle》博文 | 博文 | devblogs |
| 2025-12-09 | 博文《The Agent Execution Loop: Building an Agent From Scratch》 | 博文 | victordibia.com |
| 2025-12-19 | Newsletter《Vibe Coding With Engineering Discipline》 | 博文 | newsletter.victordibia.com |
| 2025-12-31 | 博文《2025 Year in Review》 | 博文 | victordibia.com |
| 2026-01-05 | Newsletter《The Arc of Agent Action: Code → Tools → Code》（SKILLS.md 不是新东西） | 博文 | newsletter |
| 2026-01-19 | Newsletter《Is Scaling a Dead End?》 | 博文 | newsletter |
| 2026-01 | 专利 US12518447B2 授权（LIDA 自动可视化） | 专利 | Google Patent |
| 2026-02-18 | Newsletter《Use Coding Agents to Build Your Product, Don't Make Them Your Product》 | 博文 | newsletter |
| 2026-02-19 | **MAF 迁移指南**（合并落地标志文档） | 项目 | devblogs |
| 2026-02-20 | MAF 1.0.0rc1（随后 rc2~rc6 至 3 月底） | 项目 | pypi |
| 2026-02-25 | Newsletter《Implementing Claude Code Skills from Scratch》 | 博文 | newsletter |
| 2026-03-11 | Newsletter《Context Engineering Strategies for your Agent》 | 博文 | newsletter |
| 2026-03-30 | Newsletter《Agentic Noise》 | 博文 | newsletter |
| 2026-04-01 | Newsletter《Building Your Own Claude Code from Scratch》 | 博文 | newsletter |
| **2026-04-02/03** | **Microsoft Agent Framework 1.0 GA**（PyPI 1.0.0 + devblog） | 项目 | devblogs |
| 2026-04-06 | Newsletter《Inside Claude Code》（513K 行源码逆向） | 博文 | newsletter |
| 2026-04-21 | Newsletter《How Good is Anthropic's Claude Design?》 | 博文 | newsletter |
| 2026-04-28 | MAF 支持 A2A v1（跨平台 agent 通信） | 项目 | devblogs |
| 2026-05-31 | MAF @ BUILD 2026 | 演讲 | devblogs |
| 2026-06-22 | Newsletter《Microsoft Build 2026: Top Announcements for Agent Developers》 | 博文 | newsletter |
| 2026-07-07 | Agent Skills for .NET 稳定版 | 项目 | devblogs |
| 2026-07-08 | **MAF 编排模式达 1.0**（sequential/concurrent/group chat/handoff/**magentic** 五种编排） | 项目 | devblogs |
| 2026-07-10 | MAF v1.11.0（GA 后约 3 个月发 11 个 minor） | 项目 | pypi |
| 2026-07-15 | Agent Skills for Python 稳定版 | 项目 | devblogs |

> MAF 节奏：2025-10-01 至 2026-07-10 共 **51 个 PyPI 发布**，典型 beta→rc→GA→快速 minor 节奏。

### 重点论文摘要
- **Magentic-UI: Towards Human-in-the-loop Agentic Systems**（arXiv:2507.22358，2025-07-30，窗口内核心）：Dibia 合著（Mozannar 等 20 人）。主张 human-in-the-loop agentic system 是可行路径——人类监督控制 + AI 效率。开源 Web 界面，支持 Web 浏览/代码执行/文件操作，可通过 MCP 扩展；提出 **6 种低成本人类介入机制**（co-planning、co-tasking、multi-tasking、action guards、long-term memory 等）。与 Agent UX 演讲的 HCI 视角一脉相承。
- **Magentic-One: A Generalist Multi-Agent System**（arXiv:2411.04468，2024-11-07，窗口外但关键）：主智能体 **Orchestrator** 负责规划/跟踪/重规划，调度专门 agent（浏览器、文件、Python）。在 GAIA/AssistantBench/WebArena 三个基准上取得与 SOTA 统计上具竞争力的表现。
- **AutoGen Studio**（arXiv:2408.15247，EMNLP 2024，Dibia 一作）：无代码多 agent 开发工具，4 条设计原则。
- **Concept Distillation**（arXiv:2408.09365，NAACL 2025）：用强模型为弱模型生成规则提升表现（Mistral-7B Multi-Arith +20%，Phi-3-mini HumanEval +34%）。**注：本次调研纠正了"该 ID 是 Magentic-One"的误传。**

---

## 6. 故事叙述风格（10 个手法）

他从两场演讲（QCon SF 2024 + AI.Engineer 2025）提炼出的特征手法：

1. **场景想象开场**：QCon 不从定义而从画面开场——"Imagine a scenario where computers could handle increasingly complex tasks on your behalf"，抛三个具象任务（下载邮件附件导入 Excel / 构建 Android app / 报税）贴标签，再归纳共性。**先共情再定义**。
2. **From-scratch 叙事（现场造物）**："Let's build something from scratch!"，用 BlenderLM 当场拆解构建。把听众拉进"构建者第一视角"。
3. **三段式议程结构**：先亮议程地图（Intro→Failure Modes→What you can do），听众始终知道自己在叙事哪一段。
4. **失败清单体 + 检查清单体**：QCon 标题"10 Reasons"即失败清单；Agent UX 用编号 takeaway（"0. Know when to use a multi-agent approach!"）和四维 checklist。结论收敛为可记忆的编号要点。
5. **执行循环拆解**：把 agent 抽象成最小循环"LLM Call → Process tool calls → Return Results"，工程流程拆 5 步把 Agent 放第 5 步标"This comes last, not first!"。用顺序反直觉制造记忆点。
6. **二元对比框架**：Workflow vs Autonomous MAS 对照表反复使用——一列"可靠但需预知解法"，一列"能探索但不可靠"。用对比而非定义传授"何时该用"。
7. **HCI/UX 视角切入**：当其他工程演讲讲"怎么调 prompt/怎么加 agent"，他讲"用户怎么知道 agent 能做什么、怎么追溯、怎么叫停、怎么知道委派值不值"。把 agent 当半自主人机协作系统而非纯算法。
8. **第三方权威锚定**：大量引用外部信源（Richard Socher 的 last mile problem、langchain 失败数据、YC 469% agent 初创增长、Forbes）。不靠自证，靠行业共识。
9. **金句锚点 + 谦虚免责**：每个 key slide 配一句可独立传播的口号，同时诚实标注边界："These principles are still early and non-exhaustive"、"remains challenging and somewhat unclear"。包装不过度。
10. **时间线自介建立可信度**：用"How I got into Agents"时间线（Aug 2022 LIDA → Sept 2023 AutoGen → AutoGen Studio）建立"我是一路造过来的"叙事权威，与 from-scratch 主题呼应。

---

## 7. 金句集（带出处）

1. "An agent is an entity that can reason, act, communicate, and adapt to solve tasks."（Agent = LLM + Tools）— QCon SF 2024 PDF
2. "Imagine a scenario where computers could handle increasingly complex tasks on your behalf." — QCon SF 2024 PDF
3. "Autonomous agents have the last mile problem."（引自 Richard Socher）— QCon SF 2024 PDF
4. "The future is agentic." — QCon SF 2024 PDF
5. "Your agent is only as good as the tools you give it!" — Agent UX PDF（AI.Engineer 2025）
6. "A workflow is a set of deterministic steps with sprinkles of LLM calls... reliable, production-ready... but require that we know the exact solution." — Agent UX PDF
7. "An autonomous multi-agent system is one where an LLM drives control flow... enabling software that takes actions, observes results and interactively explores the solution space." — Agent UX PDF
8. "Agents come last, not first." — Agent UX PDF
9. "Multiple agents collaborating, with autonomy, increases the surface for errors and reliability issues. Like any other tool, they should be selected when they are the right tool for the job." — Agent UX PDF
10. "Know when to use a multi-agent approach!"（第 0 原则） — Agent UX PDF
11. "Let's build something from scratch! A multi-agent system from scratch!" — Agent UX PDF
12. "about 70% of effort should be split between... building your tools and tuning your evaluation harness." — newsletter UX 帖
13. "Academic benchmarks, while helpful, are NOT your task." — Agent UX PDF
14. "We think we're using AI to build our projects faster. But increasingly, are we instead choosing projects based on what AI can help us build?" — Newsletter《/upgrade》
15. "AI writes the code, AI reviews the code, and the human pays $25 to be removed from the loop." — Newsletter《Agentic Noise》
16. "苦涩教训没死，它被摊销了。"（The bitter lesson isn't dead, it's been amortized.）— Newsletter《Is Scaling a Dead End?》
17. "most 'agents' in production are mostly workflows." — Newsletter UX 帖

> 金句出处 URL：
> - QCon/AI.Engineer 演讲：https://victordibia.com/pdf/victorqconsf2024.pdf 、https://victordibia.com/pdf/victordibia_agentux.pdf
> - Newsletter：https://newsletter.victordibia.com/p/4-ux-design-principles-for-multi 、/upgrade-or 、agentic-noise-how-ai-agents-can-break 、is-scaling-a-dead-end-why-model-scaling

---

## 8. 系统化梳理总结（综合认知）

把四路调研摄入后，可提炼出对 Victor Dibia 的三层系统认知：

### 第一层：他是"agent 时代的 HCI 布道者"
在 agent 圈普遍沉迷于"更多 agent、更大自主性"时，他始终拽着另一根绳——**agent 是半自主人机协作系统，必须为人设计**。这条线从他 PhD 的众包/可穿戴 HCI 研究，经 Data2Vis/LIDA 的"自动化分析师"，一路延伸到 Magentic-UI 的 6 种人类介入机制、4 条 UX 原则。**别人造更强的 agent，他造更可驾驭的 agent。**

### 第二层：他的产品哲学是"先理解再选用，先原型再投产"
两个反直觉主张贯穿其工作：
- **"Agents come last, not first"**——70% 精力在 tools 和 eval，agent 是最后一步。反对"一上来就写 Agent 类"。
- **"Know when to use a multi-agent approach"**——大多数生产中的"agent"其实是 workflow；MAS 只在精确解未知的场景才值得以可靠性换自主性。
这两条本质上是对行业"agent 通胀"（什么都叫 agent、什么都套多 agent）的纠偏。picoagents（从零造框架）和 Inside Claude Code（逆向 513K 行）是同一哲学的两面：**去黑箱化**——先搞懂执行循环这个通用内核，再谈框架选型。

### 第三层：他对 AI 编码的态度是"深刻乐观 + 强烈警惕"并存
这是与"编码消失论"最相关的一层。他不是技术悲观派，但也不是"编码要消失"的激进派：
- **乐观侧**：他亲手用 coding agent 建产品（Agent Framework、DevUI），拆解 Claude Code 源码赞赏其工程深度，承认 METR 自主任务长度每 7 月翻倍。
- **警惕侧**：他反复强调 vibe fixing（30-40% 时间修 AI 的 bug）、能动性丧失（从匠人变指挥者）、agentic noise（平台失衡）、成瘾式依赖、安全 Rule of Two、不要把通用 agent 当产品交付。
- **核心立场**：agent 会大幅改变编码工作形态，但**不等于编码消失**——它把人的工作从"写代码"推向"写需求 + 评测 + 纪律 + 系统设计"，且这个迁移需要工程纪律护航，否则就是 AI slop 和能动性丧失。

**这就解释了为什么"编码消失论"找不到出处**：那段话的激进预测（3-5 年消失 + 眼镜摄像头 + 开完会已实现）与他"深刻乐观 + 强烈警惕"的平衡立场不符。他更可能说的是类似"agent 自主任务时长在翻倍、编码工作形态在根本改变"这样的**趋势观察**，而非"编码消失"的**时间预测**。

### 一个贯穿性隐喻
如果要用他自己的语言概括他：他是在 agent 这辆越来越快的车上，**一边踩油门（造 AutoGen/MAF/Magentic）、一边反复检查刹车和方向盘（UX 原则、Interruptibility、Agentic Noise 警告）**的人。这种"建设者 + 警惕者"的双重身份，是他区别于同行最鲜明的标签。

---

## 9. 信源与缺口说明（方法论透明度）

### 已成功抓取（可信）
- victordibia.com 主页/CV/博客元数据
- newsletter.victordibia.com 全部 22 篇 archive 元数据 + 8 篇全文（含 2 篇付费墙截断）
- Google Scholar（引用 1643、h-15、论文列表）
- arXiv：2507.22358（Magentic-UI）、2411.04468（Magentic-One）、2408.15247（AutoGen Studio）、2408.09365（Concept Distillation）
- GitHub：microsoft/agent-framework、microsoft/autogen、victordibia profile README
- Microsoft devblogs（agent-framework 频道，2025-10 至 2026-07）
- PyPI（agent-framework 版本时间线）
- 两份演讲 PDF（QCon SF 2024、AI.Engineer 2025 Agent UX）——文本层提取，图形 slide 内容部分缺失
- QCon SF 会议页 abstract

### 未抓到 / 需登录态补取（缺口）
- **X/Twitter（@vykthur）时间线**：需登录，curl 抓不到。这是核实"编码消失论"若出自口头表述的最可能渠道。
- **LinkedIn（/in/dibiavictor/）**：需登录。
- **YouTube 视频正文/字幕**：那条 YouTube 链接经核实是 AI.dev + Cassandra Summit 2023 keynote 合集（非 QCon），且需登录。其他演讲视频字幕未取。
- **播客 appearance**：newsletter 正文未自述任何播客访谈；curl-only 约束下无法检索 Latent Space / Practical AI 等播客嘉宾列表。**这是本次调研最大的盲区**——若他有播客访谈，其口头表述（可能更放松、更激进）无法覆盖。
- **QCon PDF 中"10 个失败模式"具体条目**：纯图形 slide，文本层未保留，仅有 abstract 证明其存在。建议从演讲录像或书 Part III（10 大失败模式）补全。
- **书《Designing Multi-Agent Systems》具体出版日**：Google Books 页面 JS 渲染，API 返回空；Manning 原 URL 已 404。仅确认 2025 年内交付。

### 调研纪律
4 个子 Agent 并行，每个补抓轮次控制在 5 轮左右（newsletter 路 agent 为完成"编码消失论核实"硬性要求扩展到 9 轮）。所有结论可溯源至上述 URL。凡无法证实处（尤其"编码消失论"）均明确标注，不编造。

---

*文档生成：2026-07-18，由 4 个子 Agent 并行抓取 + 主 Agent 系统化梳理合成。如需补全缺口（尤其播客/口头表述核实），建议用登录态浏览器抓 @vykthur X 时间线与主流 AI 播客嘉宾页。*
