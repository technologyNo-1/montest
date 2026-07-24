---
title: "Gavin Uberti 思想演进与 Etched/Sohu 近360天调研"
type: people-analysis
date: 2026-07-23
tags: [Gavin Uberti, Etched, Sohu, ASIC, Transformer, 推理芯片, 算力经济, AI硬件, scaling law, MoE, 全栈]
status: active
source: "3 subagent 并行搜集(Tavily 配额耗尽后 Jina/Brave/DDG 兜底)+ 主 agent 一次性整合"
---

# Gavin Uberti 思想演进与 Etched/Sohu 近360天调研

> **一句话主线**:Gavin Uberti 以"**把 Transformer 烧进硅片**"为终生赌注,从哈佛辍学创立 Etched(2022),押注"专业化 ASIC 必然取代通用 GPU";思想主线高度一致(**规模→超智、推理算力将远超训练、专业化必然、全栈垂直整合是护城河**),最显著的**演进**在架构赌注--从 2024"只跑 Transformer、被取代即作废"的极端单架构,到 2026 主动扩展 MoE+Mamba/SSM + LVI/CSM 全栈,产品从"芯片"升级为"Gigawatt 级 frontier inference cluster"。
> **整理日期**:2026-07-23(当日恰为 Etched Series C $300M、估值 $10.3B、Sequoia 领投公告日)
> **信源层级**:L0 一手(Etched 官方博客《Making the Biggest Bet in AI》经 Wayback 全文获取、官网 /progress、globenewswire 新闻稿)> L1 权威二手(TechCrunch/Bloomberg/SiliconANGLE/MIT TR/Colossus ILTB 章节)> L2 一般(wafer.substack/seti_park/百科)。Tavily 本会话配额耗尽,X 原推反爬未直取(经二手引述),Colossus ILTB Ep.480 transcript 在登录墙后(仅获章节标题);Dwarkesh 档案确认 Gavin 未上过。未核实项见文末。

---

## 一、背景生平(从简)

- **教育**:哈佛大学,同时修 CS 与数学的学士/硕士课程;**2023-03 辍学**创办 Etched。出生约 2001-2002(源间不一致,未精确核实)。
- **早期经历**:ChatGPT 发布前为开源编译器 **Apache TVM** 写 matmul(矩阵乘)内核;此前 **ex-OctoML、ex-Xnor.ai**(后者被苹果约 $2 亿收购)。
- **联合创始人**:三人均哈佛辍学生--CEO **Gavin Uberti**、CTO **Chris Zhu**、COO **Robert Wachen**,加前 Cypress Semiconductor CTO **Mark Ross**。三人同入选 **Thiel Fellowship**;Uberti 入选 **MIT TR35 2025**(23 岁)。
- **创立缘起(2022)**:"In 2022, we made a bet that transformers would take over the world."--当时 ChatGPT 未发、图像用 U-Net、自动驾驶用 CNN,押注 Transformer 是逆共识赌注。

---

## 二、主要成就与机构演进(早期从简,重点主要成就 + 最近)

### 2.1 机构演进时间线

| 时点 | 事件 |
|---|---|
| 2022 | Etched 创立(哈佛辍学生三人组),押注 Transformer |
| 2023-03/04 | Uberti 辍学;种子轮 ~$5.36M,估值 $34M(2023 末濒临断粮,30 页 memo 四处碰壁) |
| 2024-06-25 | **发布 Sohu + $120M Series A**(Primary Venture + Positive Sum 领投),团队 ~35 人 |
| 2024-10/11 | 与 Decart 发布 **Oasis**(首个可玩 AI 生成游戏,实时类 Minecraft) |
| 2025-09 | Uberti 入选 **MIT TR35 2025** |
| 2025-12 | **$500M Series B,$5B 估值**,Stripes 领投,Thiel 参投 |
| 2026-04 | wafer.substack《Peak FLOPS》深度质疑(20× 仅高 batch+短 context 成立) |
| 2026-06-30 | **走出隐身**:A0 流片成功(TSMC N4P,首版即成)、累计 $800M 融资、>$1B 客户合同、400+ 团队、台湾工厂 + 圣何塞 2MW 数据中心 |
| 2026-07-23 | **$300M Series C,$10.3B 估值,Sequoia 领投**(a16z/SK Hynix/Jane Street/Diffusion Capital 参投),7 个月估值翻倍,自称"Sequoia 领投 Series C 史上最高估值" |

### 2.2 融资

| 轮次 | 时间 | 金额 | 估值 |
|---|---|---|---|
| 种子 | 2023-03 | $5.36M | $34M |
| A | 2024-06 | $120M | 未披露 |
| B | 2025-12 | $500M | $5B |
| (未官宣第四轮) | 2026H1 | ~$175M(推算) | - |
| C | 2026-07-23 | $300M | $10.3B |

累计约 **$1.1B**。投资人阵容:L0 机构(Stripes/Sequoia/a16z/Primary/Jane Street/HRT/Jump/Two Sigma/Ribbit/Radical/VentureTech Alliance/SK Hynix)+ AI 名人(**Karpathy、Hinton、Fei-Fei Li、Druckenmiller、Arthur Mensch、Scott Wu、Noam Brown、Peter Thiel**)+ 天使(GitHub CEO Dohmke、Kyle Vogt、Charlie Cheever、Amjad Masad、Dylan Field)。

### 2.3 Sohu 芯片(产品要点)

- **定位**:Transformer 专用 ASIC 推理芯片,裁掉无关硬件专攻矩阵运算;TSMC **N4P**,die ~800mm²(接近可制造极限)。
- **性能(自报,未独立核验)**:8-Sohu 服务器 Llama 70B **>500,000 tokens/sec**,替代 **160 张 H100**;比 Blackwell GB200 "快且便宜一个数量级";**>90% FLOPS 利用率**(GPU ~30%)。
- **2026 双突破**:**LVI(低电压推理)**--数学块电压低于常规一半,万亿参数稀疏 MoE 80%+ Peak FLOPs 不降频(攻 prefill 算力/热墙);**CSM(集群级内存)**--HBM/SRAM 混合 + 专有低延迟高带宽互连(攻 decode 带宽)。
- **量产**:2026 夏首批机架出货履约 $1B 合同,目标 2027 GW 级。

---

## 三、近 360 天事件与思想铺垫(2025-07-27 至 2026-07-23)

> 本节合并窗口内访谈、社交媒体、重大事件,作为 §4 思想演进的铺垫。窗口内 Gavin 公开发声**高度集中于 2026-06-30 出隐身当天**(此前 11 个月近乎隐身期)。

### 3.1 窗口内访谈(高度集中)

| 日期 | 场合 | 核心主题 |
|---|---|---|
| 2026-06-30 | **Colossus / Invest Like the Best Ep.480**(Patrick O'Shaughnessy,Gavin + Wachen)《The Future of AI Hardware》 | LVI+CSM 双赌注、"find-a-way" 文化、推理成最大市场、speed wins、垂直整合、Gen 2 千瓦级、"机器不像人那样思考"、"一年算力压缩进一个月"、万亿美元数据中心 |
| 2026-06-30 | **Bloomberg Tech**(Ed Ludlow) | 出隐身、$800M 融资、行业从训练转向推理、挑战 Nvidia |

> **用户点名的 8 档播客(Dwarkesh/20VC/No Priors/NLW/Latent Space/Acquired/Lenny/Semianalysis)窗口内均未发现 Gavin 专属访谈**--Dwarkesh sitemap 175 期确认无 Etched/Uberti 条目,如实标注。Gavin 历史长访谈为 2023-12 ILTB EP.356、2024 TechCrunch Found、2025-03 Pioneers of AI(均窗口外)。

### 3.2 窗口内重大事件时间轴(按月)

| 月份 | 事件 | 思想节点 |
|---|---|---|
| 2025-09 | MIT TR35 入选 | "2022 押注 transformer 是冒险但正确的赌注";比特币 ASIC 类比 |
| 2025-12 | $500M B 轮 $5B(悄然) | (未公开声明)对应 ILTB 追述的 2023 近破产→"find-a-way" 逆袭 |
| 2026-03 | **NVIDIA GTC Vera Rubin**(R100,推理 5× Blackwell,token 成本 1/10) | Gavin 未直接回应;Etched 定位锚点:"通用 GPU 再快也输给硬连线 transformer" |
| 2026-04 | wafer.substack 技术质疑(20× 仅高 batch 成立;3 专利;首席架构师 Saptadeep Pal 前 Auradine 比特币 ASIC;风险=混合 attention-SSM 侵蚀优势) | Gavin 立场(6 月强化):Sohu 是"吞吐机而非延迟机",throughput-first 路线(区别 Groq/d-Matrix 低延迟 SRAM 路线) |
| 2026-05 | Cerebras IPO($5.5B/~$38B);2026-06 Groq $650M、OpenAI 自研芯片(Broadcom) | 推理芯片赛道升温,多家自研印证"专用化"趋势 |
| **2026-06-30** | **出隐身**($800M/$1B/A0 硅/LVI+CSM) | "frontier AI 将成最具经济意义的技术之一,但可持续服务它的基础设施并不存在";"production is the product"(Wachen) |
| **2026-07-23** | **Series C $10.3B**(Sequoia 领投) | Wachen:"系统可跑任意模型,含 MoE 与非 transformer 的 Mamba"--**从"只跑 transformer"退守为"专用硅 + 多模型系统"** |

### 3.3 社交媒体

- **2026-06-30 Etched 官方 X 出隐身长推串**:LVI/CSM/$800M/$1B/2027 千瓦级纲领宣言(原推反爬未直取,经 seti_park 分析串 + TechCrunch 引述确证)。
- **2026-07-05 @seti_park X 分析串**:拆解 Etched pitch,指其书面版早三年由 Uberti+Zhu 署名。
- **@blip_tm 持续质疑**(TechCrunch 引为"持续质疑"代表,即便流片成功后仍存疑)。
- **比特币挖矿 ASIC 类比**(Gavin 标志性叙事,窗口内 ILTB + wafer 均引述)。

---

## 四、个人/机构/产品思想演进(重点)

> Gavin 思想主线高度一致;最显著的演进在**架构赌注**。本节用其直接原话架构化梳理。

### 4.1 为什么 ASIC 而非 GPU:专业化必然 + 面积经济性

核心论点:GPU 已撞墙(只变大不变强),专业化是唯一出路,面积经济性第一性原理。

- **GPU 批评**:"Santa Clara's dirty little secret is that GPUs haven't gotten better, they've gotten bigger. The compute (TFLOPS) per area of the chip has been nearly flat for four years... With Moore's law slowing, the only way to improve performance is to specialize."
- **面积经济性**:"only 3.3% of the transistors on an H100 GPU are used for matrix multiplication!... specializing on transformers lets you fit far more compute.";"Sohu boasts over 90% FLOPS utilization (compared to ~30% on a GPU with TRT-LLM)."
- **规模阈值**:"When models cost $1B+ to train and $10B+ for inference, specialized chips are inevitable. At this scale, a 1% improvement would justify a $50-100M custom chip project."
- **Bitcoin ASIC 类比(反复使用)**:"Bitcoin used to be mined on GPUs, but the moment that the first ASICs came out, they were better than GPUs by an order of magnitude... With billions of dollars on the line, the same will happen for AI."
- **客户倒逼**:"our future customers won't be able to afford not to switch to Sohu."

### 4.2 对 scaling law 的判断:规模→超智,推理算力远超训练

- **规模即超智**:"Scale is all you need for superintelligence... Scale is the only trick that's continued to work for decades... We are living in the largest infrastructure buildout of all time."
- **规模演进量化**:"Meta used 50,000x more compute to train Llama 400B (2024 SoTA) than OpenAI used on GPT-2 (2019)."
- **推理 vs 训练(关键)**:"models cost $1B+ to train and $10B+ for inference"--推理开销约训练 10 倍量级,是其押注推理硬件的底层依据。
- **数据墙即推理算力**:"the data problem is actually an inference compute problem."(并称 Zuckerberg/Amodei/Hassabis 似乎同意)
- **基础设施极限**:"Scaling the next 1,000x will be very expensive. The next-generation data centers will cost more than the GDP of a small nation."

### 4.3 推理/算力经济:推理是最大市场,专用算力必然

- **推理市场爆发**:"People don't realize how big of a market inference is going to be... those are going to have to get deployed to 8,000,000,000 people across the globe.";"models grow to many trillions of parameters and token demand scales to quadrillions per month."
- **推理非内存瓶颈**:"LLM inputs are compute-bound, and LLM outputs are memory-bound. When we combine input and output tokens with continuous batching, the workload becomes very compute bound."--论证专用**算力**(非带宽)的必要性。
- **需求未被满足**:"even if we do keep making GPUs bigger, at a rate of 2.5x every two years, it will take a decade to make video generation real-time."
- **LVI/CSM 经济性**:GPU 约 50% 理论算力就过热;Etched 与 TSMC 协同设计晶体管更低电压运行,80%+ Peak FLOPs 不降频;CSM 使"faster tokens per second without a corresponding cost increase"。

### 4.4 模型架构演进:从极端单架构赌注到主动扩展(张力最大,确实演进)

这是 Gavin 思想中**前后张力最大、且确实发生演进**的一节:

- **2024 极端赌注**:"If transformers are replaced by SSMs, RWKV, or any new architecture, our chips will be useless. But if we're right, Sohu will change the world."
- **硬件彩票论(护城河)**:"the models that win are the ones that can run the fastest and cheapest on hardware... Transformers have a huge moat... As models scale from $1B to $10B to $100B training runs, the risk of testing new architectures skyrockets."
- **架构收敛论**:"since GPT-2, state-of-the-art model architectures have remained nearly identical... The only major difference is scale."
- **早期兜底承诺(预示后期转向)**:"Transformer killers will need to run on GPUs faster than transformers run on Sohu. If that happens, we'll build an ASIC for that too!"
- **2026 演进结果(重大调整)**:系统现能跑"any AI model, including MoE models like DeepSeek and Qwen... as well as non-transformer designs like Mamba (state-space model)."--从"只跑 Transformer"实质放宽到 MoE + SSM。官网:"push the entire pareto curve on frontier models, including many-trillion-parameter MoEs, long context, and agentic workloads."--MoE 已成一等公民优化对象。

> **演进实质**:未等到 Transformer 被取代,已主动扩展可服务架构面,兑现早期"若新架构胜出也会为其做 ASIC"的兜底承诺。

### 4.5 AGI/未来判断 + 竞争格局

- **AGI 路径**:"Scale is all you need for superintelligence"--算力是核心载体;ILTB 章节 "Why Machines Don't Think Like People"、"The Trillion-Dollar Data Center"、billions of agents 并发构想。未找到 Gavin 给出明确 AGI 年份的原话(未核实)。
- **领先窗口(2024)**:"we have more than an 18-month head start on them."
- **Ferrari 类比(护城河,2026)**:"speed still commands a premium, in the same way a Ferrari commands one over a Toyota despite both being cars";更持久优势是"the willingness to build the whole stack - chip through production line - rather than just the silicon."
- **全栈定位**:"We are building rack scale inference hardware. That means chips, boards, platforms, racks, clusters, as well as software, and importantly, the production lines to build those things at scale."
- **人才壁垒**:约一半平台团队来自 Nvidia;硬件 VP 此前掌管 HGX/DGX(Hopper/Blackwell 周期大部分收入来源);出隐身是为招人而非获客。

### 4.6 机构/产品战略演进(核心:从芯片到 GW 级集群)

清晰存在一条从"极端架构赌注"到"全栈推理集群"的演进线:

- **2022 立约** → **2024-06 Sohu 发布**(transformer ASIC,只跑 transformer,1 服务器替代 160 H100) → **2026-06 出隐身**(A0 流片成功,LVI+CSM,定位升级为"rack-scale / frontier inference clusters",GW 级量产) → **2026-07 Series C**($10.3B,支持 MoE+Mamba)。
- **战略转向核心**:从 2024"只跑 Transformer、被取代即作废"极端单架构押注,演化为 2026"frontier inference clusters + LVI/CSM 全栈协同设计",且明确支持 MoE + Mamba/SSM。TechCrunch 指出公司"仍在对抗其产品只跑特定 LLM 的 perception";Wachen 强调"systems can run any AI model"。
- **叙事退守**:在 NVIDIA Vera Rubin 压力 + 持续质疑下,叙事从"颠覆 GPU"转向"推理经济性 + 系统级交付 + 客户亲测验证"(Karpathy/Noam Brown/Hinton 均试过硬件)。

---

## 五、观点提炼与争议

**主线(高度一致)**:规模→超智、推理算力将远超训练(约 10×)、专业化 ASIC 必然(面积经济性 + Bitcoin 类比)、全栈垂直整合是护城河。

**最显著演进**:架构赌注从极端单架构(2024"被取代即作废")→ 主动扩展 MoE+Mamba(2026),产品从"芯片"→"GW 级 frontier inference cluster",兑现早期兜底承诺。叙事从"颠覆 GPU"退守为"推理经济性 + 系统交付"。

**争议与风险**:
1. **20× 宣称**:wafer.substack 拆解--20× 仅在高 batch + 短 context 成立,低 batch/长 context 不成立;无独立 benchmark(访问仅限投资人/早期客户,办公室内私演示)。
2. **3.3% 矩阵乘晶体管论证**:被 zach.be/wafer 质疑过度简化。
3. **架构风险**:混合 attention-SSM 架构若成主流,专用 transformer 硅优势被侵蚀(Gavin 已以支持 Mamba 部分对冲)。
4. **NVIDIA 反击**:Vera Rubin(R100,推理 5× Blackwell)直接抬升通用 GPU 推理门槛,挤压 Etched 定位。
5. **生产/交付**:截至 2026-07 仍未大规模出货,实际确认营收未披露(仅 $1B 签约合同口径)。
6. **赛道拥挤**:Cerebras(IPO)、Groq($650M)、OpenAI 自研(Broadcom)、Google Frozen v2--"模型烧进硅片"已去神秘化。

**类比定位(自述)**:比特币矿机革命--早期 GPU 挖矿,后被专用 ASIC 取代,Gavin 押注 AI 推理将重演。

---

## 附 A:信源清单

**L0 一手**
- Etched 官方博客《Making the Biggest Bet in AI》2024-06-25(经 Wayback 全文): https://www.etched.com/blog-posts/etched-is-making-the-biggest-bet-in-ai
- Etched 官网 /progress(LVI/CSM/A0/量产): https://www.etched.com/progress
- globenewswire 出隐身新闻稿(2026-06-30): https://www.globenewswire.com/news-release/2026/06/30/3319922/...

**L1 权威二手**
- TechCrunch 2024-06-25(Sohu 发布+$120M A): https://techcrunch.com/2024/06/25/etched-is-building-an-ai-chip-that-only-runs-transformer-models/
- TechCrunch 2026-07-23($10.3B C 轮): https://techcrunch.com/2026/07/23/ai-chip-startup-etched-defies-skeptics-hits-10-3b-valuation-from-big-name-investors/
- TechCrunch Found 播客 2024-08-20(Gavin 原话): https://techcrunch.com/podcast/etched-founder-gavin-uberti-thinks-his-company-stands-on-the-shoulders-of-giants/
- Colossus ILTB Ep.480《The Future of AI Hardware》2026-06-30(章节标题,transcript 登录墙后): https://colossus.com/episode/the-future-of-ai-hardware/
- Bloomberg 2026-06-30(Ed Ludlow/Dina Bass);SiliconANGLE 2024-06-25;Data Center Dynamics 2026-01-19(引 Bloomberg B 轮);MIT TR35: https://www.technologyreview.com/innovator/gavin-uberti/
- tbpndigest 2026-06-30(Gavin 出隐身采访原话): https://www.tbpndigest.com/story/2026-06-30/etched-raises-landmark-round-...

**L2 一般**
- wafer.substack《Peak FLOPS》2026-04(技术质疑): https://wafer.substack.com/p/breaking-down-etcheds-sohu
- seti_park X 分析串 2026-07-05;yespress.io 汇总页;百度百科(部分未核)

## 附 B:未核实项(如实标注)

- Gavin 精确出生年份(约 2001-2002,源间不一致);IMO 冠军(仅百度百科,英文未印证);Jane Street 累计投资 >$1 亿(仅百度百科);第四轮未官宣融资金额/领投;实际确认营收(公司仅披露签约口径);AGI 明确时间线引述(未找到);Colossus ILTB Ep.480 完整 transcript(登录墙后);X 原推(反爬未直取)。

## 附 C:self-check

- ✅ 按 [[feedback-people-analysis-structure]]:背景(§1)从简、成就(§2)早期从简重点最近、近360天+时间轴(§3)合并为思想演进铺垫、思想演进(§4)重点架构化带原话
- ✅ 思想演进为主干,背景/商业为枝叶;事实核实与未核实项集中文末,不散布正文
- ✅ 有观点有重点(§5 主线 + 演进 + 争议);frontmatter 规范,落盘 01-people,更新 _index/INDEX/CHANGELOG
