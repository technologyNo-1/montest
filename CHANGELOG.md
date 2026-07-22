# 维护日志 CHANGELOG

> LLM Wiki 操作记录，按时间倒序。每次 ingest/lint 追加一条。

## 2026-07-23 · 重做（Claude 记忆全流程,从官方源头出发）

**操作**：删除旧版 `claude_memory_全流程_2026-07-22.md`,重做并入库 `06-workflows/`。

- 新文档：`claude_memory_全流程_2026-07-23.md`(替换旧版)
- 重做理由：旧版跳过官方源头、直接本地实测,是经验主义;用户评"做得很差劲",要求先查 Claude 官网 memory 设计与最佳实践、再结合本地泛化
- 新版结构(从权威源头出发,主 agent 一次性整合,非 Workflow):
  1. Claude 官方 memory 设计(CLAUDE.md 分层拼接/auto memory just-in-time 前 200 行·25KB/Claude.ai 消费级/API memory tool+stores/官方 Include·Exclude 最佳实践/context 与 compaction 存活表)
  2. 复杂 agent 架构下使用与调优(orchestrator-worker 隔离+浓缩回传/context engineering·context rot/MEMORY PROTOCOL/长程 harness initializer+coding agent/subagent memory 边界)
  3. 论文与落地项目(CoALA 四分法/MemGPT/Generative Agents/Reflexion/A-MEM/Mem0/Zep/GraphRAG/Letta;7 个 coding agent + 4 个框架对比)
  4. 多 agent 生产级设计理念(共享 vs 私有/持久化一致性·dreaming/记忆即独立层/企业三层规则/memory vs RAG vs fine-tuning 取舍)
  5. 结合本地泛化(CoALA 映射诊断偏科/机制印证/4 MCP 角色/7 条可落地建议)
- 数据来源:3 subagent 并行搜集原始信息(Tavily 配额耗尽后改官方站 .md 端点 + arxiv + Jina Reader),主 agent(opus)一次性整合
- 信源:全部 L0 官方一手 + L1 arxiv + L2 项目 docs;Cursor/Devin/# 快捷键等未核实点如实标注
- 索引:更新 `06-workflows/_index.md`、`INDEX.md`(替换旧引用)
- 关联 auto-memory:`feedback-claude-memory-doc-approach`(重做法反馈)、`feedback-research-workflow-paused`(本次未用 Workflow)

## 2026-07-22 · ingest 新增（Demis Hassabis）

**操作**：新增人物思想调研入库 `01-people/`。

- 新增 `demis_hassabis_analysis.md`：Demis Hassabis 背景生平与学术成就（象棋神童/游戏设计/剑桥双第一/UCL 认知神经科学/DeepMind 创立/AlphaGo/AlphaFold/2024 诺奖）、商业/社会工程与机构演进（Google 收购/AlphaFold 开源/Isomorphic Labs/Google DeepMind 合并/Gemini/AI 安全治理）、个人/机构/产品思想演进（游戏AI->RL->世界模型->规划->agent->AGI；谨慎乐观+10倍安全投入；信息本体论与诺奖猜想；AGI 时间线从"几十年"前移至"奇点山脚"）、近 360 天播客与商业访谈（60 Minutes/达沃斯/I/O 2026 等）思想总结 + 故事叙述手法、近 360 天社交媒体（2026-07-14 FINRA 式前沿 AI 监管框架 X 长文、Platform 37 署名博文）思想总结 + 叙述手法、近 360 天重大事件双轴时间轴的系统化梳理
- 切入点：2024 诺奖 + 2026 Mallaby 传记《The Infinity Machine》+ 近 360 天 AGI 时间线前移与 FINRA 监管框架
- 事实订正：象棋 13 岁达 master（非 8 岁）、Black & White 原作（非续作）、封爵 2024-03-28（非新年荣誉）
- 数据来源：Workflow（6 agent 并行调研 + 主 agent 一次性整合）经 Tavily MCP + curl + Wikipedia API（Tavily 套餐中途耗尽后兜底）；约 700 行
- 信源限制：Tavily 套餐额度中途耗尽、X 反爬、部分 JS 站点未一手渲染，均已在文档 §0/§9 诚实标注
- 更新 `01-people/_index.md`（21->22 篇）、`INDEX.md`（研究者/科学家人物网络 + AGI 时间线/AI for Science 概念交叉）

## 2026-07-22 · ingest 新增（Claude 记忆全流程）⛔ 已被 2026-07-23 重做替换（文件已删,见上）

**操作**：新增工作方法论文档入库 `06-workflows/`。

- 文档：`claude_memory_全流程_2026-07-22.md`
- 内容：Claude Code 三层记忆体系（auto-memory / CLAUDE.md / vault）的创建·管理·治理全流程，结合本机实测（20 条 auto-memory、vault 8 类、4 个 MCP、obsidian skills、auto-memory 按启动目录隔离机制）
- 索引：更新 `06-workflows/_index.md`（3 篇增至 4 篇）；`INDEX.md` 新增「记忆 / 知识管理」交叉入口
- 关联 auto-memory：`personal-knowledge-vault` / `vault-auto-fix-format` / `claude-code-session-hygiene` / `change-impact-rollback-workflow`

## 2026-07-21 · 升级（深层相似性 A -> B 档）

**操作**：将 `deep_similarity_training_2026-07-21.md` 从 A 档浅扫升级为 B 档中度整合。

- 实践维度（训练/测试/loop/方案/能力差异）补实验/数据/理论支撑：Gick & Holyoak 迁移率数据（基线~10%->提示后~70%、自发迁移~10-20%）、Chi 专家新手分类、Gentner & Namy 对比学习、生成效应（Slamecka & Graf）、测试效应（Roediger & Karpicke 2006）、形成性评估（Black & Wiliam 1998）、RAT 信度（~0.8）、刻意练习 + 分散练习周期支撑
- 契合 [[large-research-workflow-patterns]] 三档深度方法论：B 档 = 浅扫 + 实践维度补实验数据（用户"不需要深度"时默认）；"不需要深度"≠"只要结论"

## 2026-07-21 · ingest 新增（深层相似性）

**操作**：新增认知/学习方法论文档入库 `06-workflows/`。

- 新增 `deep_similarity_training_2026-07-21.md`：深层相似性(结构映射/类比推理)全维度浅扫--理论(Gentner/Holyoak/Hofstadter) + 经典实验(Gick & Holyoak 辐射问题 / Chi 专家新手分类) + 训练方法 + 测试评分系统 + 反馈优化 Loop + 8-12 周可执行训练方案
- 调研模式：初版广度浅扫(每维度核心观点 + 依据,未深度挖掘),按 [[large-research-workflow-patterns]] 两阶段方法论;用户确认不需要二版深挖
- 更新 `06-workflows/_index.md`(2 -> 3 篇)、`INDEX.md`(新增"认知/学习方法"概念交叉)

## 2026-07-21 · ingest 追加（OpenClaw 补充 Loop engineering）

**操作**：为 `04-tech/openclaw_deep_research_2026-07-21.md` 追加第二十章 Loop engineering。

- 追加维度：Loop engineering（agent loop 工程化：Pi 嵌入式 loop / 五步控制流 / 终止与恢复 / failover 回退链 / HITL 与审计 / 与 Claude Code·Aider·OpenHands·SWE-agent 对比）
- 数据来源：第 5 个 Workflow（1 agent）经 curl 直取 arxiv 2603.27517 + DeepWiki 代码级知识库；文档增至 20 章
- 更新 `04-tech/_index.md`（维度数 19 -> 20）

## 2026-07-21 · ingest 追加（OpenClaw 补充 8 维度）

**操作**：为 `04-tech/openclaw_deep_research_2026-07-21.md` 追加 8 个维度（十二~十九章）。

- 追加维度：网关设置 / 长程任务 / 主动推送 / 容器化 / 本地部署 / token 消耗 / computer use 工程化 / Hermes agent 核心技术对比
- 数据来源：第 4 个 Workflow（8 agent 并行）经 Tavily + curl 直取官方 `docs/gateway/` 源码文档与 arxiv 安全论文；文档增至 290K 字符 / 496 信源 / 19 章
- 更新 `04-tech/_index.md`（维度数 11 -> 19）

## 2026-07-21 · ingest 新增（OpenClaw）

**操作**：新增技术调研入库 `04-tech/`。

- 新增 `openclaw_deep_research_2026-07-21.md`：OpenClaw 全维度技术调研（11 维度）——设计理念与哲学 / 架构体系 / 核心解决方案 / PR审核合并自动化架构 / 安全争议与生态 / Context 处理 / 智能体编排 / 安全边界 / Memory 系统 / Build Skills / 自我迭代
- 切入点：OpenClaw 是 2026 年 GitHub 历史增长最快的开源自托管 AI agent 框架（Peter Steinberger 创立，峰值 383K stars），其 harness engineering 范式与供应链安全治理教训值得沉淀
- 数据来源：3 个 Workflow 并行深挖（5+3+3 维度）经 Tavily MCP 检索 arxiv 安全论文 2603.27517 / 官方仓库 / awesome-openclaw 生态；163K 字符 / 343 信源
- 更新 `04-tech/_index.md`（散篇）、`INDEX.md`（AI Agent 概念交叉 + Peter Steinberger 关联 OpenClaw 创始人）

## 2026-07-19 · ingest 新增（伯南克）

**操作**：新增人物思想调研入库 `01-people/`。

- 新增 `ben_bernanke_thoughts_analysis.md`：本·伯南克背景与生平、学术思想演进（大萧条/金融加速器/储蓄过剩/诺奖工作）、政策产品思想演进（QE/前瞻指引/压力测试/最后贷款人/透明度/退场）、近 360 天播客与商业访谈思想总结、故事叙述手法、近 360 天重大事件双轴时间轴的系统化梳理
- 切入点：2026-07-09 伯南克被任命为 Anthropic Long-Term Benefit Trust（LTBT）成员，首次进入 AI 治理领域
- 数据来源：Workflow（6 agent 分头调研 + 1 agent 综合）经 Tavily MCP 检索中英文信源；648 行 / 111KB；7 agent / 928K tokens / 22 min
- 更新 `01-people/_index.md`（新增「宏观经济学家 / 政策学者」分组，20->21 篇）、`INDEX.md`（人物网络 + 宏观/货币与 AI 治理/劳动力市场概念交叉）

## 2026-07-19 · 新增 07-paper 分类

**操作**：新增论文总结分类，首篇论文入库。

- 新建 `07-paper/` 分类（type: `paper-summary`）：约定论文总结追加到 `07-paper/paper_summaries.md` 单文件，顶部索引同步
- 首篇收录：Anthropic《Labor Market Impacts of AI: A New Measure and Early Evidence》（Massenkoff & McCrory, 2026-03-05）中文总结
- 更新 `CLAUDE.md` §2（6→7 类）、`INDEX.md`（主题入口）、本日志
- 已存 memory：论文总结归 07-paper（以后自动）

## 2026-07-19 · ingest 新增

**操作**：新增 AI 预测/前沿安全部门调研入库 `01-people/`。

- 新增 `anthropic_openai_ai_forecasting_depts_analysis.md`：Anthropic 与 OpenAI 的 AI 预测/前沿安全部门（RSP/ASL、Preparedness、Superalignment 兴衰、Interpretability、Deliberative Alignment）背景、部门思想与产品思想演进、近 360 天播客访谈思想、故事叙述手法、重大事件双轴时间轴的系统化梳理
- 数据来源：Workflow（6 agent 分头调研 + 1 agent 综合）经 Tavily MCP 检索中英文信源；645 行 / 79KB
- 更新 `01-people/_index.md`（新增「AI 实验室 / 前沿安全部门」分组，19→20 篇）、`INDEX.md`（安全/治理 + AGI 时间线交叉链接）

## 2026-07-18 · 首次 vault 化整理

**操作**：将杂散文档目录重组为 Obsidian vault + LLM Wiki。

- 整体备份 `document` -> `document.bak.20260719-050444`
- `git init` + `.gitignore`（排除 `.DS_Store` / `.obsidian` 机器状态）
- 按 6 类重组 57 个内容文件：
  - `01-people/`（19）· `02-industry/`（6）· `03-ai-token/`（12）· `04-tech/`（12）· `05-career/`（6）· `06-workflows/`（2）
- 删除 0B 空文件 `ai_token_data_verification.md`（`token/` 内有同名实质文件）
- 修复 `README_agent3.md` 的 4 个失效 `../` 链接（文件已同目录）
- 写 LLM Wiki 维护层：`CLAUDE.md` / `INDEX.md` / `CHANGELOG.md` / `README.md` / 6×`_index.md`
- frontmatter 标准化：核心文档全量 + 其余脚本批量打底

**已完成**：
- ✅ 装 Obsidian 1.12.7（brew --cask）并指向 document vault
- ✅ 配 filesystem MCP server（`obsidian-vault`，写入 `~/.claude.json`，重启 CC 生效）
- ✅ 装 obsidian-skills（kepano 官方 5 skills：defuddle / json-canvas / obsidian-bases / obsidian-cli / obsidian-markdown）

## 2026-07-18 · 首次 lint

**检查结果**：
- frontmatter 覆盖率：54/54 内容文档 = 100%
- 坏链：无（`../` 与 `[[文件名]]` 仅为规则文本，非实际链接）
- 分类：6 类 57 内容文件归位
- git 提交：6 次

**待办（用户侧）**：
- [ ] 在 Obsidian GUI 点 "Trust author and enable plugins" 信任 document vault（生成 `.obsidian`）
- [ ] 重启 Claude Code 使 filesystem MCP（`obsidian-vault`）生效
- [ ] 后续说「复盘 vault」触发深度 lint（通读全库完善 INDEX 人物关系网）
