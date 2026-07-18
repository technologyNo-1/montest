# LLM 关键数据信息源索引

> 整理目的：知道去哪里看什么数据、反映什么信息。去噪，只保留可执行 URL。
> 更新日期：2026-07-06

---

## 目录

- [A. 模型能力对比评测（Benchmarks）](#a-模型能力对比评测benchmarks)
- [B. Token 用量与地区数据](#b-token-用量与地区数据)
- [C. API 定价与速度对比](#c-api-定价与速度对比)
- [D. 行业报告与宏观数据](#d-行业报告与宏观数据)
- [E. 中国市场专用](#e-中国市场专用)
- [F. 快速决策速查表](#f-快速决策速查表)

---

## A. 模型能力对比评测（Benchmarks）

### A1. LMArena（原 LMSYS Chatbot Arena）⭐ 最核心

| 项目 | 内容 |
|------|------|
| **网址** | https://lmarena.ai |
| **Leaderboard** | https://lmarena.ai/leaderboard/text |
| **看什么** | Elo 评分排名（盲选人类偏好投票），10 个专项 Arena（文本/视觉/代码/文档/搜索/文生图/图编辑/文生视频/图生视频/视频编辑） |
| **反映什么** | **用户实际偏好**——不是 benchmark 分数，而是人类更喜欢哪个模型的回答，最接近"好用"的定义；Style-Controlled Elo 可矫正长度偏好偏差 |
| **更新频率** | 实时 |

### A2. Artificial Analysis ⭐ 最全面

| 项目 | 内容 |
|------|------|
| **网址** | https://artificialanalysis.ai |
| **看什么** | Intelligence Index v4.1（10 项评估复合分）· 每百万 token 价格 · 输出速度（tok/s）· 首 token 延迟 · 上下文窗口 · 100+ 模型对比 |
| **反映什么** | **性价比三维图**——智能度 × 价格 × 速度，适合做 API 选型决策；v4.1 侧重 agentic 工作负载（250 轮轨迹、真实工具调用） |
| **更新频率** | 实时（定价/延迟），定期更新 Intelligence Index |

### A3. LiveBench

| 项目 | 内容 |
|------|------|
| **网址** | https://livebench.ai |
| **GitHub** | https://github.com/LiveBench/LiveBench |
| **看什么** | 每次发布全新生题目的无污染评测：推理/编码/Agentic 编码/数学/数据分析/语言/指令遵循 |
| **反映什么** | **防刷榜评测**——题目每 6 月全量更新，模型不可能在训练数据中见过，比固定 benchmark 更能暴露真实能力 |
| **更新频率** | 版本化发布（如 LiveBench-2026-01-08） |

### A4. Scale AI SEAL

| 项目 | 内容 |
|------|------|
| **网址** | https://scale.com/leaderboard |
| **看什么** | 50+ 模型的专家设计评测：SWE-bench Pro（1865 题抗污染软件任务）· HLE · EnigmaEval · 安全/欺骗检测 · Remote Labor Index |
| **反映什么** | **工业级能力+SaaS 安全**——不只是能力，还包括 alignability、deception detection；SEAL Showdown 有 232K 用户偏好投票跨 100+ 国家/70+ 语言做人口学切分 |
| **更新频率** | 持续更新，年度 Awards（12月） |

### A5. Vellum LLM Leaderboard

| 项目 | 内容 |
|------|------|
| **网址** | https://www.vellum.ai/llm-leaderboard |
| **看什么** | GPQA Diamond · AIME 2025 · SWE-bench Verified · HLE · ARC-AGI 2 · MMLU（50+ 模型） |
| **反映什么** | **前沿硬能力聚焦**——不追全面，只追寻最难推理/编码/AGI 测试题，适合追踪"谁能解最难题" |
| **更新频率** | 定期（最新：2026.06） |

### A6. LLM Stats

| 项目 | 内容 |
|------|------|
| **网址** | https://llm-stats.com |
| **看什么** | 300+ 模型：复合分（GPQA Diamond + SWE-bench Verified + coding-arena）· 实时速度 · 价格 · 延迟 · 上下文窗口 |
| **反映什么** | **最广覆盖**——如果你需要对比某个小众模型，这是最可能覆盖到的 |
| **更新频率** | 实时 / 近实时 |

### A7. Stanford HELM（维护模式）

| 项目 | 内容 |
|------|------|
| **网址** | https://crfm-helm.readthedocs.io/en/latest/ |
| **看什么** | 42 场景 × 7 维指标（准确度/校准/鲁棒性/公平/偏见/毒性/效率） |
| **反映什么** | **学术级多维评测**——虽然 2026.06 已进入维护模式，但历史数据在 fairness/bias/toxicity 维度仍是最全面的 |
| **更新频率** | 停止更新 |

### A8. SWE-bench（编码专用）

| 项目 | 内容 |
|------|------|
| **网址** | https://www.swebench.com |
| **看什么** | 真实 GitHub Issue 解决率；Verified 子集 = 500 人工验证题 |
| **反映什么** | **编码 Agent 的真实能力**——能做真实软件工程任务吗？当前最活跃的 coding benchmark |
| **更新频率** | 定期 |

### A9. AutoBench（抗刷榜专用）

| 项目 | 内容 |
|------|------|
| **网址** | https://autobench.org |
| **看什么** | 多 LLM 互评 + 不断变化的题目 + 并排对比质量/价格/延迟 |
| **反映什么** | **防游戏化评测**——87% 与 Artificial Analysis 相关，77%+ 与 LM Arena 相关 |
| **更新频率** | 定期 |

### A10. Vectara Hallucination Leaderboard

| 项目 | 内容 |
|------|------|
| **网址** | https://github.com/vectara/hallucination-leaderboard |
| **看什么** | 各模型的**幻觉率**（按模型列出） |
| **反映什么** | **安全第一指标**——哪个模型在摘要任务中最少乱编 |
| **更新频率** | 新模型发布时更新 |

---

## B. Token 用量与地区数据

### B1. Cloudflare Radar ⭐ 最直接

| 项目 | 内容 |
|------|------|
| **网址** | https://radar.cloudflare.com |
| **看什么** | 全球互联网流量趋势 → 筛选 "AI" 或 "AI-related domains"；按国家/地区的流量分布 |
| **反映什么** | **AI API 流量的地理分布代理指标**——Cloudflare 承载了大量 AI API 请求（Workers AI 等），可以间接看出哪些地区调用量大；也看 `ai.cloudflare.com` 的流量变化 |
| **更新频率** | 实时 / 每日 |

### B2. OpenRouter 公开排名

| 项目 | 内容 |
|------|------|
| **网址** | https://openrouter.ai |
| **看什么** | 模型用量排名（按请求量/token 量排序）· 价格对比 · 趋势变化 · 跨模型测试 |
| **反映什么** | **实际 API 消费市场份额**——OpenRouter 是最大的 LLM API 聚合器之一，哪个模型被调用最多反映了真实开发者选择；也可以看哪些模型"正在上升" |
| **更新频率** | 实时 |

### B3. Stanford HAI AI Index Report ⭐ 最权威

| 项目 | 内容 |
|------|------|
| **网址** | https://aiindex.stanford.edu |
| **看什么** | 年度 AI 全景数据：LLM 训练成本演变 · 各国 AI 论文/专利数 · AI 使用地区分布 · 各行业采用率 · 政策/法规数据 · 模型能力进化 |
| **反映什么** | **最全面的宏观数据**——如果你只能读一份年度报告，就读这个。按国家的时间序列数据是理解地区 AI 发展差距最可靠的来源 |
| **更新频率** | 年更（最新：2026 版） |

### B4. State of AI Report

| 项目 | 内容 |
|------|------|
| **网址** | https://www.stateof.ai |
| **看什么** | AI 产业年度深度：研究突破 · 产业格局 · 政策 · 安全 · 预测 |
| **反映什么** | **VC/产业视角趋势**——Air Street Capital 出品（Nathan Benaich），权威性与 Stanford 互补，更偏产业和投资 |
| **更新频率** | 年更（通常在 10 月） |

### B5. Stack Overflow Developer Survey

| 项目 | 内容 |
|------|------|
| **网址** | https://survey.stackoverflow.co |
| **看什么** | 全球开发者 AI 工具使用率 · 按地区的 AI 工具采用 · 对 AI 的态度 · 最常用 AI 工具排名 |
| **反映什么** | **开发者人群的 AI 采用格局**——ChatGPT/Copilot/Claude 等工具的地区渗透率，用于理解不同市场的成熟度 |
| **更新频率** | 年更（通常在 6 月） |

### B6. GitHub Octoverse

| 项目 | 内容 |
|------|------|
| **网址** | https://octoverse.github.com |
| **看什么** | 全球开发者增长数据 · AI 相关项目增长 · 最流行语言/框架 · 按地区的贡献量 |
| **反映什么** | **AI 开发活动的地区分布**——哪些国家在 GitHub 上做 AI 项目？印度/美国/中国/巴西等地 AI 仓库增速 |
| **更新频率** | 年更（通常在 10-11 月） |

### B7. Gartner AI Forecast

| 项目 | 内容 |
|------|------|
| **网址** | https://www.gartner.com/en/information-technology/insights/ai |
| **看什么** | AI 市场总规模预测 · 各细分（LLM/MLOps/AI Chip）支出 · 企业采用率 · 按地区的 IT 支出分解 |
| **反映什么** | **企业支出的地区分解**——传统权威，但需要付费/注册获取详细报告；免费摘要也有参考价值 |
| **更新频率** | 持续（报告分散在各季度） |

### B8. OpenAI Signals Data Portal ⭐⭐

| 项目 | 内容 |
|------|------|
| **网址** | https://openai.com/signals/data/ |
| **看什么** | 各国人均 ChatGPT 消息量（覆盖 >5M 人口国家）· 53 个使用类别 · 工作 vs 非工作使用 · 美国州级数据 · 年龄/性别/计划类型人口统计 |
| **反映什么** | **ChatGPT 消费的最佳单一数据源**——新加坡 ~75% 网民用过 ChatGPT，美国 ~29%。数据覆盖 2024.07-2026.03 |
| **更新频率** | 定期更新 · CC-BY 4.0 开源 · CSV 可下载 |

### B9. Anthropic Economic Index ⭐⭐

| 项目 | 内容 |
|------|------|
| **网址** | https://huggingface.co/datasets/Anthropic/EconomicIndex |
| **看什么** | Claude.ai 对话按国家/州/职业分类的使用量 · 任务复杂度 · 协作模式 · 工作 vs 个人使用 · 时间节省估算 |
| **反映什么** | **最细粒度的 AI 使用地理分布**——三级地理层级（国家/州/全球），最低阈值 200 次对话/国家。适合与 OpenAI Signals 对比做交叉验证 |
| **更新频率** | 定期发布（2025.02 / 03 / 09 / 2026.01 / 03）· CC-BY 4.0 · CSV/Parquet 可下载 |

### B10. OpenRouter + a16z "State of AI" Report

| 项目 | 内容 |
|------|------|
| **网址** | https://openrouter.ai/data |
| **看什么** | 100 万亿 token 实证研究——按供应商的市场份额：Google 29.7% · Anthropic 23.8% · DeepSeek 20.0% · Qwen 10.4% · OpenAI 4.7% |
| **反映什么** | **开发者 API 消费的 ground truth**——中国开源模型从 1.2% 飙升至 ~30% 周份额。推理模型采用率 >50%。编程 ~50% 查询量 |
| **更新频率** | 研究发布（2025.12），底层数据实时更新 |

### B11. Hugging Face / MIT "Economies of Open Intelligence"

| 项目 | 内容 |
|------|------|
| **网址** | https://huggingface.co/spaces/mmpr/open-model-evolution |
| **看什么** | 851K 模型 · 2.2B 下载量（2020.06-2025.08）· 按国家下载份额：中国 17.1% · 美国 15.8% · 国际/匿名 23.8%|
| **反映什么** | **开源模型消费的地面真相**——中国首次超过美国在开源模型下载量。2024-2025 63% 的新 fine-tune 基于中国基础模型 |
| **更新频率** | 研究论文（2025.11）+ 在线仪表盘 |

### B12. Cloudflare Radar AI Insights（深度入口）

| 项目 | 内容 |
|------|------|
| **网址** | https://radar.cloudflare.com/ai-insights |
| **看什么** | AI bot 爬虫流量（按目的/内容类型/行业）· Workers AI 模型流行度（按模型×任务维度）· robots.txt 分析 · 1.1.1.1 DNS 查询反映的生成式 AI 服务流行度 |
| **反映什么** | 比主 Radar 页面更细致的 AI 专用视图——可以看到哪个模型在 Workers AI 上推理请求量最大 |
| **API** | REST API：`location[]`（ISO alpha-2）和 `continent[]` 过滤 |

### B13. Backblaze Network Stats（基础设施视角）

| 项目 | 内容 |
|------|------|
| **网址** | https://www.backblaze.com/blog/ |
| **看什么** | Neocloud + 超大规模云厂商的 AI 流量份额（25.5% Q1 2026）· 地理热力图 · 每 IP 比特数（"大象流"代理指标）|
| **反映什么** | **AI 计算负载的物理分布**——罕见的基础设施层面视角。AI 流量呈突发特征（100G/400G 极端峰值）。加州 · Ashburn-Reston (VA) · 芬兰 · 巴西 · 法国 · 加拿大是 AI 计算热点 |
| **更新频率** | 季度 |

### B14. Datadog State of AI Engineering

| 项目 | 内容 |
|------|------|
| **网址** | https://www.datadoghq.com/resources/state-of-ai-engineering/ |
| **看什么** | 多模型舰队管理 · 模型采用/淘汰率 · Agent 框架采用 · Prompt 缓存利用率——来自 1,000+ 客户 |
| **反映什么** | **企业对多模型的真实选择**——揭示"隐藏 token 成本"（缓存利用不足造成的浪费），比单个供应商数据更中立的工程视角 |
| **更新频率** | 年度 |

### B15. New Relic AI Unwrapped

| 项目 | 内容 |
|------|------|
| **网址** | https://newrelic.com/resources/report/ai-unwrapped-2025-impact-report |
| **看什么** | 85,000 客户账户的 LLM token 消费——ChatGPT 占 86% 所有 LLM tokens · Llama 第二 · 92% QoQ 增长在独特 LLM 数 · Python +45% |
| **反映什么** | **最大的企业级 LLM 消费数据集之一**——OpenAI 在企业的压倒性份额（但注意：这是 2025 年数据，反映 ChatGPT API 早期采用阶段）|
| **更新频率** | 年度（首版 2025.06）|

### B16. World Bank "ChatGPT Adoption by Country"

| 项目 | 内容 |
|------|------|
| **网址** | https://documents1.worldbank.org/curated/en/099856110152535288/pdf/ |
| **看什么** | 按收入水平分层的 ChatGPT 渗透率：高收入 24% · 中上收入 5.8% · 中下收入 4.7% · 低收入 0.7% · 各国互联网用户中的访问比例 |
| **反映什么** | **全球 AI 采用鸿沟的严谨学术测量**——收入水平是最强预测变量 |
| **更新频率** | 一次性（数据截至 2025.04）|

### B17. CSH / Science 论文: "Who is using AI to code?"

| 项目 | 内容 |
|------|------|
| **网址** | https://www.eurekalert.org/news-releases/1112957 |
| **看什么** | 3,000 万次 commit × ~16 万开发者 → AI 生成 Python 代码的国别份额：美国 29% · 法国 24% · 德国 23% · 印度 20% · 俄罗斯 15% · 中国 12% |
| **反映什么** | **最严谨的同行评审 AI 编码采用国别测量**——美国全年 $9.6-$14.4B 经济价值 |
| **更新频率** | 一次性（Science, 2026.01）|

### B18. Similarweb AI Rankings

| 项目 | 内容 |
|------|------|
| **网址** | https://www.similarweb.com/top-apps/ai/ |
| **看什么** | ChatGPT、Claude、Gemini、DeepSeek 等各 AI 产品的网站流量/月活用户/按国家分布 |
| **反映什么** | **C 端 AI 产品市场份额**——不直接等于 token 量，但和 API 调用格局高度相关；按国家的流量数据是地区偏好的最好代理 |
| **更新频率** | 月度 |

---

## C. API 定价与速度对比

### C1. Artificial Analysis

| 项目 | 内容 |
|------|------|
| **网址** | https://artificialanalysis.ai |
| **看什么** | 已在 A2 列出。补充：**Price vs Speed vs Quality 三维散点图**——选择"哪个模型性价比最高"的最佳工具 |
| **更新频率** | 实时 |

### C2. OpenRouter

| 项目 | 内容 |
|------|------|
| **网址** | https://openrouter.ai |
| **看什么** | 已在 B2 列出。补充：**实时 API 定价比较** + **直接在线选模型测试** + **token 用量排行（哪些模型增长最快）** |

### C3. LiteLLM Cost Tracker

| 项目 | 内容 |
|------|------|
| **网址** | https://github.com/BerriAI/litellm |
| **看什么** | GitHub README 中的定价对比表 + `/docs` 中的模型价格追踪 |
| **反映什么** | **最全的开源定价清单**——所有主要模型的 token 价格都在一个表里，开发者选模型时经常引用 |

### C4. TokenCalculator

| 项目 | 内容 |
|------|------|
| **网址** | https://tokencalculator.com/llm-benchmarks |
| **看什么** | 16 模型精炼对比表（MATH/GSM8K/HumanEval/SWE-bench） |
| **反映什么** | 快速快照——不想浏览复杂排行榜时用 |

---

## D. 行业报告与宏观数据

### D1. Stanford HAI AI Index ⭐

| 项目 | 内容 |
|------|------|
| **网址** | https://aiindex.stanford.edu |
| **核心数据章节** | Chapter 3（技术性能）· Chapter 4（LLM 负责任 AI）· Chapter 6（政策与治理）· Chapter 7（R&D 投入地区分布） |
| **反映什么** | 见 B3。最全面的年度快照。关键数据点：各国私人 AI 投资额 · 各国 AI 论文数 · 训练成本演变 |

### D2. State of AI Report ⭐

| 项目 | 内容 |
|------|------|
| **网址** | https://www.stateof.ai |
| **核心数据** | 研究趋势（每月 arXiv 论文数）· 产业格局（LLM API 市场份额估算）· 安全事件时间轴 · 地缘政治 AI 竞赛数据 |
| **反映什么** | 见 B4。与 Stanford 互补——更偏产业和前沿趋势 |

### D3. Fed Cohen (CB Insights)

| 项目 | 内容 |
|------|------|
| **网址** | https://www.cbinsights.com/research/ai-trends/ |
| **看什么** | AI 独角兽/投融资数据 · 按轮次/国家/细分 · 季度融资金额排名 · IPO 退出数据 |
| **反映什么** | **资本市场对 AI 的押注方向**——哪些赛道（Foundation Model/Agent/Infra/垂直应用）融钱最多、哪国吸金 |
| **更新频率** | 持续（付费，但有免费摘要） |

### D4. PitchBook AI Dashboard

| 项目 | 内容 |
|------|------|
| **网址** | https://pitchbook.com/news/reports?themes=ai |
| **看什么** | AIGC/ML 投融资数据 · 估值倍数 · 退出统计 · PE/VC 流入量 |
| **反映什么** | 和 CB Insights 类似，但侧重点稍不同——PitchBook 更偏 PE/后期，CB Insights 更偏早期创投 |

### D5. McKinsey State of AI

| 项目 | 内容 |
|------|------|
| **网址** | https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai |
| **看什么** | 企业 AI 采用率 · 各行业 → 用例 → ROI 数据 · 按地区分解 |
| **反映什么** | **企业端实际落地情况**——不是开发者社区采用，是大企业真正在花钱用什么 |
| **更新频率** | 年更 |

---

## E. 中国市场专用

### E1. SuperCLUE ⭐

| 项目 | 内容 |
|------|------|
| **网址** | https://www.superclueai.com |
| **看什么** | 中文 LLM 综合排行榜：语言理解 · 推理 · 数学 · 编码 · 指令遵循 · Agent 能力 · 安全对齐 |
| **反映什么** | **中文能力最权威的排名**——国际模型 vs 中国模型的中文 head-to-head；关键洞察：Top 4 国际模型（Claude/Gemini/GPT-5.x）＋开源中国模型成本效率 ~3x 于同等国际模型 |
| **更新频率** | 年度报告 + 定期快报 |

### E2. FlagEval (BAAI/智源)

| 项目 | 内容 |
|------|------|
| **网址** | https://flageval.baai.ac.cn |
| **看什么** | 语言/多模态/代码/数学/安全/价值观对齐 多维评测；独立安全和价值观排行榜；开源中文 LLM HF Leaderboard |
| **反映什么** | **最系统的价值观和安全对齐评估**——去理解中国 LLM 在什么维度被定义为"安全/对齐"，以及开源中国模型对标国际的差距 |
| **更新频率** | 定期 |

### E3. OpenCompass (上海 AI Lab)

| 项目 | 内容 |
|------|------|
| **网址** | https://rank.opencompass.org.cn |
| **看什么** | CompassRank（5 维综合评测）· CompassAcademic（学术榜 ~2 周更新）· CompassBench（指令遵循/Agent）· 多模态榜 |
| **反映什么** | **更新最快的中文评测之一**——如果你需要跟踪最新的中国模型能力变化，这个比 SuperCLUE 更频繁 |
| **更新频率** | ~2 周 |

### E4. C-Eval

| 项目 | 内容 |
|------|------|
| **网址** | https://cevalbenchmark.com |
| **看什么** | 52 学科中文评测（STEM/社科/人文） |
| **反映什么** | 中文知识覆盖——但 2025.07 已停止维护排行榜 |
| **更新频率** | 停更 |

---

## F. 快速决策速查表

### 我想知道…

| 问题 | 去哪里 | 看什么 |
|------|--------|--------|
| 哪个模型最好用？ | https://lmarena.ai | Elo 排名 |
| 哪个模型性价比最高？ | https://artificialanalysis.ai | Quality×Price×Speed 三维图 |
| 哪个模型编码最强？ | https://www.swebench.com + https://scale.com/leaderboard | SWE-bench + SWE-bench Pro |
| 哪个模型中文最好？ | https://www.superclueai.com | SuperCLUE 中文综合榜 |
| 谁幻觉最少？ | https://github.com/vectara/hallucination-leaderboard | 幻觉率排行 |
| 排行榜被刷了吗？ | https://livebench.ai + https://autobench.org | 防污染评测 |
| ChatGPT 各国家用的人多少？ | https://openai.com/signals/data/ | 人均消息量 + 使用类别 |
| Claude 各国家用的人多少？ | https://huggingface.co/datasets/Anthropic/EconomicIndex | 按职业/国家使用量 |
| 哪个 API 用量最大？ | https://openrouter.ai/rankings + https://openrouter.ai/data | 模型 token 排名 + 100T token 实证研究 |
| 开源模型哪个国家下得最多？ | https://huggingface.co/spaces/mmpr/open-model-evolution | 国家下载份额 |
| AI 流量地理分布？ | https://radar.cloudflare.com/ai-insights + https://www.backblaze.com/blog/ | AI 推理请求分布 + 计算负载热力图 |
| 全球 AI 研发投入地区分布？ | https://aiindex.stanford.edu（Ch.7）| 各国私人投资额 + 论文数 |
| 企业在真正用什么模型？ | https://newrelic.com/resources/report/ai-unwrapped-2025-impact-report + https://www.datadoghq.com/resources/state-of-ai-engineering/ | 企业 token 消费模型分布 |
| 开发者用什么 AI 工具？ | https://survey.stackoverflow.co | 开发者调查 AI 使用率 |
| 哪里 AI 代码最活跃？ | https://octoverse.github.com | GitHub AI 仓库 + 地区增长 |
| 企业落地了什么 AI？ | https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai | 行业 × 用例 × ROI |
| AI 赛道融了多少钱？ | https://www.cbinsights.com/research/ai-trends/ | VC 融资额 + 独角兽 |
| API 价格对比？ | https://openrouter.ai + https://artificialanalysis.ai | 实时定价 + 速度 |
| 完整的模型/定价清单？ | https://github.com/BerriAI/litellm | LiteLLM 定价表 |
| 中国模型价值观/安全？ | https://flageval.baai.ac.cn | FlagEval 安全榜 |

---

> 📌 **使用建议**：
> - **日常跟踪**：LMArena + Artificial Analysis + OpenRouter 三个网站
> - **地区 token 用量**：尚无单一完美数据源。用 **OpenAI Signals + Anthropic Economic Index + Cloudflare Radar AI + OpenRouter 排名 + HuggingFace 下载数据** 五角交叉验证
> - **每周/月深度**：加 LiveBench + SuperCLUE + Datadog State of AI
> - **每季度/年宏观**：Stanford AI Index + State of AI Report + McKinsey State of AI
> - **地区数据的最佳三角验证组合**：OpenAI Signals（C 端） + Anthropic Economic Index（C 端） + OpenRouter（API 端） + HuggingFace（开源端） + Cloudflare Radar（基础设施端）
> - **注意盲区**：AWS Bedrock / Azure AI / GCP Vertex AI 不公开任何地区性 token 消费数据——这是最大的信息缺口
