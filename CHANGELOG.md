# 维护日志 CHANGELOG

> LLM Wiki 操作记录，按时间倒序。每次 ingest/lint 追加一条。

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
