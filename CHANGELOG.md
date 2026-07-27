# 维护日志 CHANGELOG

> LLM Wiki 操作记录，按时间倒序。每次 ingest/lint 追加一条。

## 2026-07-26 · ingest 新增（陶哲轩 Terence Tao 个人思想演进深度调研）

**操作**:新增 `01-people/terence_tao_analysis.md`。

- 调研对象:陶哲轩,UCLA 杰出教授(菲尔兹奖 2006、Green-Tao 定理/压缩感知/随机矩阵)、IPAM Director of Special Projects、PCAST 成员;非 AI 从业者,而是顶尖数学家对 AI 介入数学的观察者/实践者
- 2 subagent 并行搜集(sonnet 学术事实 + opus 思想演进),发现 Tao 自维护 tao-web 金矿(Claude 起草、本人审阅的 AI 观点 living summary + 2026-07-23 逐字访谈),Tavily 耗尽后 r.jina.ai/WebFetch/DDG 兜底
- 思想演进为骨架主干(七阶段):2014"编译错误"预言 -> 2023"2026 共同作者"预言+概率核+比较优势 -> 2024"平庸但不无能的研究生" -> 2025 验证过滤器+IMO 金牌拐点 -> 2025-12 Erdős #1026 被 Aristotle+Lean 自主解 -> 2026-03 ChatGPT Pro 共同贡献对偶证明(预言兑现)+"ready for primetime" -> 2026-04 "job description changing"+proof abundance 三段论 -> 2026-07 coding agent 五条件论
- 10 条核心命题,承重墙="验证是让不可靠工具有用的唯一过滤器";数学哲学底色(理解为本/实验为法/协作为体/比较优势/工具可上移)是 AI 立场的底座
- 关键订正(两 subagent 交叉验证):Erdős #1026(非 #126);Jacobian 反例由 Claude Fable 5 找到;IPAM ready for primetime 是 2026-03-04~06
- 学术:560 篇论文+19 本书;Fields/Breakthrough/MacArthur;2026 Companion of the Order of Australia;PCAST 2021
- 关联:[[demis_hassabis_analysis]]、[[sergey_levine_analysis]]、[[ilya_sutskever_analysis]]

## 2026-07-26 · ingest 新增（Sergey Levine 个人思想演进深度调研）

**操作**:新增 `01-people/sergey_levine_analysis.md`。

- 调研对象:Sergey Levine,UC Berkeley 副教授(Harvey E. Wagner 讲席)+ Physical Intelligence 联合创始人/首席科学家,深度 RL 用于机器人控制先驱
- 2 subagent 并行搜集(sonnet 学术事实 + opus 思想演进纵深),主 agent 复用 Pi 调研已抓的 Dwarkesh/LinkedIn/TechCrunch 三场原话,Tavily 耗尽后 r.jina.ai/WebFetch/DDG 兜底
- 思想演进为骨架主干(六时期收束):PhD 的 GPS -> 2016 端到端"像素到力矩" -> 2018 SAC 最大熵 -> 2018-21 离线 RL(CQL/AWAC/IQL/D4RL,最重要学术贡献) -> 2022-24 RT-X/DROID 大规模数据转向 -> 2024 VLA/π0"阿波罗计划"
- 8 条贯穿哲学命题 + 1 元命题("通用性=改进方式的通用性",把整条学术线统一);近一年推进:VLA 必须叠 RL / 瓶颈上移到中间层推理(标注>遥操) / 通用性元定义
- 学术:research.com D-Index 153、引用 ~9.8 万、世界 CS 第 33;PECASE 2025(Biden 宣布);MAML/TRPO/SAC 等高引;学生含 Chelsea Finn/Haarnoja/Aviral Kumar 等
- 近 360 天两座主峰:Dwarkesh 2025-09-12 + Colossus 2026-03-31(原话经两份综述交叉印证,非逐字稿直取,已标注)
- 关联:[[physical_intelligence_analysis]]、[[demis_hassabis_analysis]]、[[ilya_sutskever_analysis]]

## 2026-07-26 · ingest 新增（Physical Intelligence π 机构与思想演进调研）

**操作**:新增 `01-people/physical_intelligence_analysis.md`。

- 调研对象:Physical Intelligence (π),"机器人领域的 OpenAI",2024-03 创立,通用机器人 VLA 基础模型
- 2 subagent 并行搜集(sonnet 事实型 + opus 思想演进),Tavily 耗尽后 r.jina.ai/WebFetch/DDG 兜底
- 主线:思想演进为骨架主干——π0(可学会)→π0.5(可泛化)→π*0.6(RL 攻可部署)→π0.7(组合泛化,GPT-3 时刻);商业上抵抗过早商业化、做机器人 API 层,反向区隔 Skild/Figure/Tesla
- 4 场深度访谈逐字稿原话引述(Dwarkesh×Levine / Sequoia×Hausman+Springenberg / Finn AI Startup School / LinkedIn×Levine)
- 融资四轮:种子 $70M → A $400M@$2.4B → B $600M@$5.6B → C ~$1B@$11B(在谈)
- 信源差异已取多数派(成立年份/创始人名单/各轮领投方),存疑项列文末 §5
- 关联:[[demis_hassabis_analysis]]、[[gavin_uberti_analysis]]、[[李飞飞_空间智能与世界模型_2026思科AI峰会观点总结]]

## 2026-07-25 · ingest 新增（CXMT HBM 全产业链深度调研,国产替代视角）

**操作**:新增 `02-industry/cxmt_hbm_investment_deep_research_2026-07-25.md`。

- 基于权威方法论框架(12维度+6步+三角验证+可证伪),4 Agent 并行调研(主体/工艺瓶颈/供应商/需求CAGR机构观点)
- CXMT 特殊性:追赶者+出口管制,投资逻辑=国产替代(非全球供应链,与海力士HBM4E根本不同)
- 主线结论:最值得投资=国产上游设备/材料商(非CXMT本身,因商业悖论:IPO不投HBM、HBM短期不赚钱)
- 三视角收敛:拓荆科技(混合键合+PECVD+订单+54%,唯一三视角交集)+华海诚科GMC(中期弹性)+设备四强(短期确定性)
- 扩产周期最长+溢价最强上游=键合设备(拓荆Dione 300国产突破)
- 关键修正:上次CXMT HBM3 parity不准确,实际落后2-3年(整体3-4年)
- 关联:[[semiconductor_2026_report]]、[[hbm4e_investment_deep_research_2026-07-25]]

## 2026-07-25 · ingest 新增（HBM4E 全产业链深度调研 v2,权威方法论）

**操作**:新增 `02-industry/hbm4e_investment_deep_research_2026-07-25.md`。

- 基于权威方法论框架(Gartner/IDC/麦肯锡/SemiAnalysis/Porter 提炼)12 维度 + 6 步顺序 + 三角验证 + 可证伪
- 4 Agent 并行调研(主体/工艺瓶颈/供应商全景/需求TAM+CAGR+机构观点),主动跟踪状态(吸取上次 Agent 丢失教训)
- 主线结论:最值得投资 = 先进封装设备链(CoWoS/HB/Besi)+ 检测/量测(KLA/Camtek/Onto),三视角(瓶颈/CAGR/议价权)收敛 + 机构共识(Atlas Peak 价值迁移)
- 关键证伪:球粉 CAGR 4-8%(非 35-50%+)、2026 末供过于求被证伪(实际短缺到 2027-28)、先发优势被追平
- 数据来源:SemiAnalysis/Atlas Peak/TrendForce/TechInsights/公司财报,三角验证 + 等级标注
- 关联:[[semiconductor_2026_report]]

## 2026-07-25 · 删除（HBM4E 调研报告,质量不及格物理删除）

**操作**:物理删除 `02-industry/hbm4e_supplier_deep_research_2026-07-25.md`,同步移除 `_index.md`/`INDEX.md` 条目。

- 原因:任务完全不及格--D1-D4 Agent 丢失、按权威方法论缺 6 维度(市场边界/周期定位/需求TAM/成本/财务验证/政策地缘)、数据单源无三角验证、无可证伪设计、违反下手顺序(直接钻供应商跳过需求分析)
- 方法论框架已建立(12 维度+6 步顺序+三角验证,从 Gartner/IDC/麦肯锡/SemiAnalysis/Porter 提炼),待存 06-workflows 后按此重做
- 教训:动手具体产业前,先建立有依据的调研方法论;Agent 派出后要主动跟踪状态,不能假设"还在跑"

## 2026-07-25 · 重做（HBM4E 全产业链深度调研,D1-D7 + R1-R6）

**操作**:覆盖重写 `02-industry/hbm4e_supplier_deep_research_2026-07-25.md`。

- 原版只覆盖供应商 + 最受益细分(不及格),重做为全维度:技术路线 / 垄断根基 / 工艺 / 瓶颈 / 供应商 / 情景 / CAGR + R1-R6 递归推理
- 核心发现(反直觉):TC Bonder 权威 CAGR 仅 13% < HBM 整体 26.8%,设备类被单价稀释,耗材(球粉)+ 测试类弹性更优
- 数据来源:2 Agent 并行调研(D1-D4 / D6-D7)+ 主 agent 深度推理;交错式(先假设键合最受益 -> 权威 CAGR 证伪 -> 修正为耗材/测试)
- 诚实标注:良率/瓶颈/多数细分权威 CAGR 在付费报告,推断 CAGR 标注非权威
- 关联:[[semiconductor_2026_report]]

## 2026-07-25 · ingest 新增（SK海力士 HBM4E 核心供应商深度调研）

**操作**：新增行业调研入库 `02-industry/`。

- 新增 `hbm4e_supplier_deep_research_2026-07-25.md`:SK海力士 HBM4E 全行业核心供应商深度调研(材料 9 环节 + 设备/制造/IP 8 环节),含激进扩产到 2030 最受益细分推理
- 核心:最受益细分 = 键合设备环节(TC Bonder Hanmi/ASMPT 扩产期爆发 -> hybrid bonding Besi 2030 前后接棒),胜在"海力士不自研键合机"无自研替代风险;材料端 Namics 独家协议到期是最大变量(华海诚科潜在二供);华海增收不增利(营收 +38% / 净利 -39%)
- 数据来源:2 个 Agent 并行调研(Tavily 超额,WebFetch + DDG 兜底)+ 主 agent 深度推理整合;交错式(先推理假设 Besi 垄断 -> 验证修正为 Hanmi 主导 TC Bonder)
- 索引:更新 `02-industry/_index.md`(7->8 篇)、`INDEX.md` 算力/半导体交叉入口
- 关联:[[semiconductor_2026_report]](HBM 宏观市场)

## 2026-07-24 · ingest 新增（中金 AI 金融时刻投资思考维度）

**操作**：新增行业分析入库 `02-industry/`。

- 新增 `中金AI金融时刻_美股A股投资思考维度_2026-07-24.md`:基于中金《AI的金融时刻--AI融资追踪(1)》(2026-07-23)报告框架,结合美股/A股环境,给出 7 个投资思考维度(融资结构/现金流循环/利润率×折旧敏感性/风险传导/时间轴/泡沫判断/产业链位置)
- 核心:AI capex 从现金流驱动转向债务扩张,3.5万亿外部融资缺口、1万亿收入回本门槛、"收入前置风险后置";投资思考核心是"投资能否收回"而非"能否建成"
- 美股映射:云厂商/芯片/银行/Neocloud/私募;A股映射:算力硬件链(卖铲人)/券商/银行(应用侧)/AI应用,突出中美差异(A股无 hyperscaler、融资链不完整、硬件链受美股 capex 周期传导)
- 数据来源:主 agent 基于中金报告(已存 Clippings)分析,未联网搜集
- 索引:更新 `02-industry/_index.md`(6->7 篇)、`INDEX.md` 新增「AI 金融/融资周期」交叉入口
- 关联:[[gavin_uberti_analysis]](ASIC 资产寿命)、[[jensen_huang_thoughts_analysis]]、[[semiconductor_2026_report]]、03-ai-token

## 2026-07-23 · ingest 新增（Gavin Uberti / Etched）

**操作**：新增人物思想调研入库 `01-people/`。

- 新增 `gavin_uberti_analysis.md`:Gavin Uberti(Etched CEO)背景、主要成就(Etched 机构演进/Sohu Transformer 专用 ASIC/融资累计 ~$1.1B/$10.3B 估值 Series C)、个人/机构/产品思想演进(为什么 ASIC 而非 GPU、scaling 判断、推理算力经济、模型架构演进[从极端单架构到 MoE+Mamba]、AGI/竞争格局、机构战略从芯片到 GW 级集群)、近 360 天访谈(ILTB Ep.480/Bloomberg)+ 重大事件时间轴
- 切入点:2026-06-30 出隐身(A0 流片成功 + $1B 合同)+ 2026-07-23 Series C $10.3B(Sequoia 领投,当日公告)
- 主线:思想主线高度一致(规模->超智、推理算力远超训练、专业化必然、全栈护城河);最显著演进在架构赌注(2024 极端单架构 -> 2026 主动扩展 MoE+Mamba + LVI/CSM 全栈,产品从芯片升级为 GW 级 inference cluster)
- 数据来源:3 subagent 并行搜集(Tavily 配额耗尽后 Jina/Brave/DDG 兜底)+ 主 agent 一次性整合(非 Workflow)
- 信源限制:Tavily 耗尽、X 反爬、Colossus transcript 登录墙、Dwarkesh 确认未上过;8 档点名播客窗口内无专属访谈,均如实标注;未核实项见文末附 B
- 更新 `01-people/_index.md`(22->23 篇)、`INDEX.md`(算力/半导体交叉入口 +[[gavin_uberti_analysis]])
- 关联:[[feedback-people-analysis-structure]](思想演进为重点)、[[feedback-research-workflow-paused]](本次未用 Workflow)

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
