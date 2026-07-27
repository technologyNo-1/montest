---
title: "陶哲轩(Terence Tao)思想演进与近360天调研"
type: people-analysis
date: 2026-07-26
tags: [Terence Tao, 陶哲轩, UCLA, 菲尔兹奖, Green-Tao, 压缩感知, Lean, 证明助手, AI for Math, ChatGPT, ICM 2026, PCAST]
status: active
source: "2 subagent 并行搜集(sonnet 学术事实 + opus 思想演进)+ 主 agent 一次性整合"
---

# 陶哲轩(Terence Tao)思想演进与"AI for Math 拐点"近360天调研

> **一句话主线**:陶哲轩是当代最伟大数学家之一(菲尔兹奖 2006,Green-Tao 定理/压缩感知/随机矩阵圆定律,560 篇论文)。本文主线不是数学成就,而是**一个顶尖数学家对 AI 介入数学的态度演变**--不是一次性转向,而是**随技术能力曲线逐级解锁**:2014 预言"用形式语言写论文、软件抛编译错误"-> 2023 预言"2026 AI 将成为可信共同作者"-> 2025-07 IMO 金牌拐点 -> 2026-03 ChatGPT Pro 在其论文中贡献对偶证明(预言公开兑现) -> 2026-04 "job description is changing"+proof abundance 三段论。贯穿承重墙是"**验证是让不可靠工具有用的唯一过滤器**";底色是数学哲学(理解为本/实验为法/协作为体/比较优势/工具可上移),故拥抱 AI 是其思想的自洽延伸而非妥协;同时反复强调 **engage over hostility、拒绝一维叙事、预报谦卑**(2023 的预报信心已"gone")。
> **整理日期**:2026-07-26
> **信源层级**:L0 一手(Tao 自维护 **teorth.github.io/tao-web** 的 AI 观点 living summary + 2026-07-23 逐字访谈,由 Claude 起草、Tao 本人审阅修正;博客 terrytao.wordpress.com 原文;arXiv 论文)> L1 权威二手(Nature/Quanta/The Atlantic/IEEE Spectrum/Scientific American)> L2 一般(播客笔记 podcastnotes/podmarized、媒体)。**tao-web living summary 是本次最大金矿**,结构化为 Part I-V、Tao 审阅过所有引用;Dwarkesh/Lex 笔记为转述,已注明。未取得一手:Tao 对 IMO 2025 金牌的直接引语(一贯立场已述);Nature 正文部分付费(由 tao-web 交叉印证)。

---

## 一、背景生平(从简)

- **出生**:1975-07-17 澳大利亚阿德莱德(现 51 岁),澳+美双重国籍。父亲 Billy Tao(陶象國,上海出生儿科医生,1969 港大 MBBS),母亲 Grace Leong(梁蕙蘭,港大数学/物理一等荣誉,曾任中学教师);1972 年自港移民澳洲。妻子 Laura Tao(NASA JPL 电气工程师),2 孩子。会粤语不会写中文。
- **神童线**:跳 5 个年级,9 岁旁听大学数学;8 岁 SAT 数学 760(SMPY 史上仅 3 名 8 岁儿童达 700+);IMO 10 岁首赛,**1986 铜/1987 银/1988 金,三类奖牌均史上最年轻**;1985(10 岁)与 Paul Erdős 合影(**Erdős number = 2**);14 岁 RSI 暑期项目。
- **教育**:Flinders University BSc+MSc(1991,16 岁,导师 Garth Gaudry);Fulbright 赴普林斯顿,**PhD 1996(21 岁,导师 Elias M. Stein 调和分析泰斗)**,论文《Three Regularity Results in Harmonic Analysis》。
- **UCLA**:1996 加入,1999(24 岁)正教授(UCLA 史上最年轻);现 **Distinguished Professor + James and Carol Collins 讲席教授**;2025-07-01 兼任 **IPAM(Institute for Pure and Applied Mathematics)Director of Special Projects**。
- **师承与底色**:启蒙于超常教育 + Erdős 交集 -> Princeton 师从 Stein(调和分析)-> UCLA 跨领域发散。这条线解释了他"狐狸而非刺猬"(博识多领域、找连接)的研究风格。

---

## 二、主要成就

### 2.1 学术(重点)--跨领域高产

| 领域 | 贡献 | 影响 |
|---|---|---|
| 解析数论 | **Green-Tao 定理**(2004,与 Ben Green):素数中存在任意长等差数列 | 最著名成果;transference principle 推广 Szemerédi 定理 |
| 压缩感知 | 与 **Emmanuel Candès**、Romberg 奠基;RIP;Dantzig selector;矩阵补全 | **MRI 扫描加速 ~10 倍**(Tao 自述);2020 Princess of Asturias 奖 |
| 随机矩阵 | **圆定律**证明(2010,与 Van Vu)+ universality + four moment theorem(2011) | 解决长期猜想 |
| 调和分析 | restriction 定理、双线性 restriction、wave maps 全局适定性 | 2002 Bôcher 奖、2003 Clay Research 奖 |
| PDE | 色散 PDE 适定性;**2016 构造 Navier-Stokes 变体有限时 blowup** | 千禧问题相关,否定一类"正向解答"路径 |
| 解析数论 | Erdős 偏差问题(2015,熵估计);de Bruijn-Newman 常数非负(2018,黎曼假设方向);Collatz 概率性进展(2019) | 多项主流媒体报道 |
| Erdős 问题 | 2024-2025 解决 #121/#442/#135/#685/#69/#1102 | 持续推进 |

**论文影响力**:560 篇论文 + 19 本书;Erdős number=2;Clarivate Highly Cited Researcher;合作者 68+ 位(2015)。**主要合作者**:Ben Green(最长期)、Van Vu、Emmanuel Candès、Tamar Ziegler、Jean Bourgain、Kaisa Matomäki、Maksym Radziwiłł;与 DeepMind 的 Adam Wagner、Bogdan Georgiev(AlphaEvolve)。

### 2.2 奖项与荣誉(30+ 项)

**顶级三大**:**Fields Medal(2006,31 岁,首位澳大利亚人/首位 UCLA 教师)**;**Breakthrough Prize in Mathematics(2014 首届,自认不够资格,要求分奖金未果,后设学生奖学金)**;**MacArthur Fellowship(2006)**。其他:2000 Salem、2002 Bôcher、2003 Clay Research、2007 FRS、2008 Waterman、2010 King Faisal/Nemmers、2012 Crafoord、2014 Royal Medal、2020 Princess of Asturias(与 Candès)、2021 IEEE Jack S. Kilby、**2026 Companion of the Order of Australia**。学会会员:FRS/AAAS/NAS Foreign member/AMS fellow。

### 2.3 商业--基本无,但与 AI 公司有结构化关系

- **不被任何 AI 公司直接付薪**,但获赠 premium frontier model 访问权。
- 与 **Google DeepMind** 合作(AlphaEvolve 项目,2025-01 起);曾协助组织 **OpenAI 赞助**的会议;其 IPAM special project 研究生由 **Math Inc.** 捐款资助。
- **联合创立 AI 非营利 SAIR Foundation**(sair.foundation),以此为载体为"AI for math/science"筹款。

### 2.4 社会工程--公共知识分子角色(这是他与纯数学家的区别)

- **PCAST 成员**(2021 Biden 任命,总统科技顾问委员会 30 人之一)--政策建言通道。
- **IPAM Director of Special Projects**(2025-07 起):主管"Empowering Research with Usable AI Tools"方向。
- **博客 "What's new"**(terrytao.wordpress.com,2007 起):全球最具影响力数学博客,含论文/综述/开放问题/职业建议/教学讲义;近年大量 coding-agent 可视化 applet。
- **Mastodon**(@tao@mathstodon.xyz)极活跃,AI 观点 living summary 即基于 ~70 条帖子提炼。
- **teorth.github.io/tao-web**:本人论文/书籍/工具站,含 AI 观点 living summary(由 AI 协助维护、本人审阅)。
- **科普与媒体发声**:Nature/Quanta/The Atlantic/Scientific American/IEEE Spectrum 频繁发声;NYT 称"同代最优秀数学家"。
- **社区规范**:公开背书 **Leiden Declaration**(leidendeclaration.ai,2026-06-02,负责任 AI 与形式化规范);建 erdosproblems.com + GitHub wiki 追踪 AI 对 Erdős 问题的贡献(促使 AI 公司误导性声明减少)。
- **教育倡导**:"AI diet"认知饮食类比(EMS Lecture 2026-06)。
- **政策发声**:2025-08-18 撰文批评 Trump 削减 NSF 经费(两笔被暂停,含 UCLA 研究 + IPAM)。

---

## 三、近 360 天事件与思想铺垫(2025-08 至 2026-07)

> 本节合并窗口内访谈、博客、社媒、论文、重大事件,作为 §4 思想演进的铺垫。窗口内 Tao 公开发声**密度极高**--七阶段态度演变在一年内完成最后三阶段(自主证明 -> 共同作者 -> 职业再定义)。

### 3.1 窗口内事件(合并时间轴,精选)

| 日期 | 事件 | 思想节点 |
|---|---|---|
| 2025-08-11/18 | IPAM 任 Director of Special Projects(07-01 起);撰文批 Trump 削 NSF 经费 | 以 IPAM 为载体推 AI 工具;政策发声 |
| 2025-10~11 | Mastodon:负责任"vibe coding"解 Erdős #707;AlphaEvolve 论文(arXiv 2511.02864,67 题 23 改进) | AI 进日常研究流程 |
| 2025-12-08 | 博客《The story of Erdős problem #1026》 | **Aristotle + Lean 自主解决**(Boris Alexeev),Tao 评论"proof not particularly novel" |
| 2025-12-14 | Mastodon:"Artificial General **Cleverness**, not general intelligence" | AI 是"随机生成有时聪明、常有用的输出"的工具,非 AGI |
| 2026-01-16 | GPT-5.2 Pro 自主解一道 Erdős 开问题 | Tao 称里程碑但"速度≠难度" |
| 2026-02-10 | IPAM "AI for Science: Kickoff"主旨演讲(YouTube zJvuaRVc8Bg) | 综述形式化/LLM/协作平台;SAIR 联合主办 |
| 2026-02-24 | The Atlantic《The Edge of Mathematics》 | "几乎正好赶上 2026 时间表" |
| **2026-03-04~06** | **IPAM×OpenAI 会议**"Accelerating Math and Theoretical Physics with AI" | **"AI ready for primetime""saves more time than it wastes"** |
| 2026-03-22 | **Dwarkesh Podcast**(《Kepler, Newton, and the true nature of mathematical discovery》) | "simultaneously amazing and disappointing";deductive overhang;1-2% 真实成功率 |
| 2026-03-23 | arXiv《Local Bernstein theory, Lebesgue constants》(2603.21453) | **致谢 ChatGPT Pro 贡献对偶证明**--AI 成共同贡献者 |
| 2026-03-29 | Klowden-Tao 长文《Mathematical methods and human thought in the age of AI》(arXiv 2603.26524,29 节) | human-centered 论;red team 建议 |
| 2026-04-13 | Quanta《The AI Revolution in Math Has Arrived》 | 系统梳理 2025-07 IMO 拐点后研究数学 AI 应用 |
| 2026-04-22/27 | Mastodon 三段论 + Nature《'The job description is changing'》 | **generation/verification/digestion 三段论**;"five stages of grief";"rethink fundamental questions" |
| 2026-05-30 | OpenAI Forum YouTube《How AI Is Changing Mathematics》(与 Mark Chen) | 实验成本下降 |
| 2026-05-31 | "AI could split math work by role" | 数学研究的劳动分工/工业化 |
| 2026-06-02 | 公开背书 Leiden Declaration | 社区负责任 AI 规范 |
| 2026-06 | IEEE Spectrum《big mathematics》;Quanta profile《How Terry Tao Became an Evangelist for AI in Math》;EMS Lecture《AI diet》 | "AI or real people";认知饮食;"grades better, stupider" |
| **2026-07-16** | 博客《Two more apps...》 | **LLM 适用五条件论**(非关键/独立/确定性/不替代核心技能/不与人竞争) |
| 2026-07-21 | 博客《A digestion of the Jacobian conjecture counterexample》 | **Claude Fable 5 找到 1939 年 Jacobian 猜想反例**(3 变量,Jacobian 恒为 -2 却三对一);公开 ChatGPT 对话作"消化"示范 |
| 2026-07-23 | tao-web 逐字访谈(AI 助手提问、Tao 逐字答) | disclosure、math 是 AI 安全上限、Thurston/音乐类比、预报谦卑、embrace complexity |
| 2026-07-24 | **ICM 2026 公开讲座《Mathematics in the age of AI》** | 把上述论点汇成一讲(slides 已公开) |
| 2026-07-26 | lifeboat 发布《Terence Tao on AI summary》 | living summary 转载 |

### 3.2 近一年思想推进(综合)

近 360 天,Tao 的思想沿三条线显著推进:

1. **从"预言"到"兑现"到"自我重新定义职业"**--2025 年下半年还停在"验证过滤器 + 自主解小问题"框架;2026-03 两事件(IPAM "ready for primetime" + ChatGPT Pro 共同贡献对偶证明)公开兑现 2023 预言;随即在 2026-04 Nature 与 IEEE Spectrum 跃升到"job description is changing / big mathematics / proof abundance"的职业再定义层。**进展节奏加快,但感受是悖论式**--"simultaneously amazing and disappointing"。
2. **从"何时用 AI"到"何时不用 AI"的可操作清单化**--上半年是"概率核/比较优势/可接受失败率"宏观原则;下半年(2026-07 五条件 + 2026-04 red-team 课堂展示守则)落地为微观操作守则,并公开自己的 ChatGPT 对话作示范。越来越强调"only rely on AI where you can red-team it yourself"与"keep some friction"。
3. **从"技术评估"到"人本主义 + 社会契约"**--近一年越来越多谈 digestion、taste、human understanding、音乐类比、认知饮食不平等、Leiden Declaration、engage-over-hostility、math 作为"AI 安全使用上限"。**反复强调三点**:验证必须跟上自动化否则 proof abundance 变 proof indigestion;不能把框架话语权让给科技公司("if we don't ask these questions ourselves, they will get answered for us by a technology company");拒绝一维叙事(embrace the complexity)。

**预报谦卑**是近一年最明显的自我修正:2023 那份预测三年的"relative certainty"已"gone",世界"far more unpredictable","I'm not sure anyone is capable of any reliable forecasting beyond a year at best"。

---

## 四、思想演进(主干)

### 4.1 七阶段:从"编译错误预言"到"职业再定义"

#### 阶段 0｜底色早铺好(2014-2022):形式化与"编译错误"预言

Tao 对 AI 的拥抱并非突变,而是建立在对**实验数学、形式化、大规模协作**的一贯信念上。早在 2014 年座谈中,他就预言数学家终将"不是用 LaTeX 写论文,而是用某种语言,由智能软件转成形式语言",每当软件"不理解你如何推出这一步"时就"抛出一个编译错误"(2014 panel,Quanta 2026-06 复引)。2022 年首次接触 ChatGPT 印象是"流利但空洞"(fluent but hollow)。

#### 阶段 1｜2023 定调:"2026 共同作者"预言 + 概率核 + 比较优势

2023 是坐标系确立年。Microsoft AI Anthology(2023-06)《Embracing change and resetting expectations》给出此后三年组织一切的预测:"**2026-level AI … will be a trustworthy co-author in mathematical research**"--前提是结合形式验证器、搜索与符号包;真正任务是"safely, wisely, and equitably"驾驭过渡。

同年 Mastodon 奠定两个反复使用的框架:
- **概率核**(2023-03-05):AI 工具不像确定性函数,而像"给定输入产生集中于理想答案附近、但携带微妙 plausible 误差的随机输出的概率核",应交互使用而非"按一次就走"。
- **比较优势**(2023-04-23,援引李嘉图):"AI is very good at converting billions of pieces of data into one good answer. **Humans are good at taking 10 observations and making really inspired guesses**."

**与前阶段差异**:几乎无"成果"可指,立场是预测性+框架性的。

#### 阶段 2｜2024 下半年:早期实验的失望与发现--"平庸但不无能的研究生"

2024-09 测试 OpenAI 早期 o1 模型做难题,给出广为流传的判语:"**a mediocre, but not completely incompetent [research assistant]**--像在指导一个平庸但不完全无能的研究生。"同期印象:"coherent English … but there was very little depth"。但已看到形式化协作的革命:"**you don't need to trust the people you're working with, because the program gives you this 100 percent guarantee**"--使"factory-production-type, industrial-scale mathematics … like a modern supply chain"成为可能。

**与前阶段差异**:从"预言"转向"实测",形式化协作从设想变实战(Polynomial Freiman-Ruzsa,33 页论文、约 20 人三周完成)。

#### 阶段 3｜2025 上半年:验证过滤器成承重思想 + IMO 拐点

Simons 座谈(2025-02)与 *Notices of the AMS*《Machine-Assisted Proof》(2025-01)确立他全部 AI 写作中 load-bearing 的思想:"**the most promising uses of AI come from combining them with more traditional and reliable verification methods, in order to filter out hallucinations that would otherwise render the AI output useless**." 他把传统研究比作"低流量净水龙头",AI 是"高体积不可饮用消防水管",整个游戏就是**造过滤器**。

**IMO 拐点**:2024-07 AlphaProof + AlphaGeometry 2 解 IMO 4/6、银牌(差 1 分金牌);**2025-07 Google Gemini Deep Think 解 5/6、35/42 达金牌**(IMO 主席 Dolinar 称证明"astonishing … clear, precise … easy to follow",第 6 题 0 分)。从银到金的跨越是社区公认拐点。Tao 对竞赛成绩始终谨慎:成功率先量级依赖算力、辅助与报告方式,呼吁标准化预披露基准。

**与前阶段差异**:思想从"AI 能帮忙"上升为"验证才是让 AI 有用的关键";IMO 金牌让"AI 解题"从演示变公认里程碑。

#### 阶段 4｜2025 年末:自主证明里程碑--Erdős #1026 被 Aristotle + Lean 自主解决

2025-12-07,Boris Alexeev 在对 Erdős 问题库系统扫描中,用 AI 工具 **Aristotle** 让其**自主解决** Erdős 问题 #1026(证 c(k²)=1/k),并直接输出 **Lean** 形式化证明(化为矩形装箱问题)。Tao 2025-12-08 博客:"**was able to get this tool to autonomously solve this conjecture c(k²)=1/k in the proof assistant language Lean**… the proof turned out to not be particularly novel." 同月提出"artificial general **cleverness**, not general intelligence"区分:当前工具是"stochastic generators of sometimes-clever, often-useful outputs"。对真实成功率泼冷水:"only a point or two",集中在易端,"no evidence the median problem is in reach"。

**与前阶段差异**:AI 从"辅助"跨入"自主产出可验证证明";但 Tao 同时泼冷水。

#### 阶段 5｜2026-03:AI 成共同作者--ChatGPT Pro 贡献对偶证明 + "ready for primetime"

**(a) IPAM "ready for primetime"(2026-03-04~06)**:OpenAI × UCLA IPAM 会议宣判当前模型已"ready for primetime",因数学与理论物理中 AI 现在"**saves more time than it wastes**"。改变判断的是"the gradual widening of the tasks he can hand over"--文献检索、写代码、作图、跑计算、测试思路。一次原本数小时数周的文献检索,现在一个 prompt 几分钟返回"useful map"。

**(b) ChatGPT Pro 成共同贡献者(2026-03-23)**:论文《Local Bernstein theory, and lower bounds for Lebesgue constants》(arXiv:2603.21453)明确致谢 ChatGPT Pro。Tao 博客原话:"I decided to try my luck giving it to ChatGPT Pro, which recognized it as an L¹ approximation problem and gave me a **duality-based proof** (based ultimately on the Fourier expansion of the square wave)." 以及"this latter argument was provided to me by ChatGPT, as I was not previously aware of the Nevanlinna two-constant theorem." 价值定位:"their main value for me was in quickly confirming that the approach I had in mind was numerically plausible, and in recognizing the right technique to solve one part." 这一步正好兑现 2023 预言;他对 The Atlantic 说该预言"almost exactly [on] schedule",AI 贡献已"on par with the contribution … a junior human co-author"。

**Dwarkesh(2026-03-22)** 给出最精炼的矛盾感受:"**The progress is simultaneously amazing and disappointing. It is a very strange feeling to see these tools in action.**"

**与前阶段差异**:AI 从"自主解小问题"升级为**在一线研究论文中贡献关键证明思路**;预言被公开验证,但感受是悖论式。

#### 阶段 6｜2026-04~05:角色分化论--"job description is changing"

Nature(2026-04-27)Q&A:"**it's getting harder to deny that these tools can work**"--社区反应正经历"five stages of grief",denial 开始消退。最关键判断:"**AI is not just another technology like the word processor or the web browser. It really is forcing us to rethink fundamental questions - what is a mathematical proof? What is a paper? What is the purpose of our profession? If we don't ask these questions ourselves, then they will get answered for us by a technology company or decided by financial incentives. We have to get ahead of this.**"

**proof abundance / digestion 三段论**(Mastodon 2026-04-22/27):数学问题求解拆为 **generation、verification、digestion(理解、语境化、讲解)** 三段。历史上三者都难、digestion 是副产品;AI 与形式化把 generation(及 verification)远远甩在 digestion 前,造成"impedance mismatch"--数学从**证明稀缺**走向**证明过剩(proof abundance / proof indigestion)**。尖锐观察:现在生成**长**证明比**短**证明更容易,但生成变快**并未**带来数学进展变快。故声望应转向 verify 与 digest 的人。他据此**收窄了自己实时点评新证明的范围**。借 Douglas Adams 称之为从"Survival"(稀缺)经"Inquiry"走向"Sophistication"(过剩)的过渡。

**角色分化**(IEEE Spectrum 2026-06 "big mathematics"):数学家从"craftsperson … one toy at a time"走向"factories",类比软件工程从 lone hacker 到项目经理/QA/formalizer 分工;预言新职业(把机器丑陋证明改写成人类可读优雅证明)与"citizen mathematics"。

**与前阶段差异**:从"AI 帮我写论文"上升为**整个职业的自我重新定义**。

#### 阶段 7｜2026-07:coding agent 实践--LLM 适用条件论

2026-07-16 博客《Two more apps...》首次系统给出"**何时可放心让 LLM 全权代劳**"的五条有利条件(原话逐条):① **Not mission-critical**(小正误差率可接受);② **Stand-alone**(技术债有界);③ **End product is deterministic (and sandboxed)**(确定性语言、沙箱、运行时不调 LLM);④ **Not replacing primary skills**(愿意放弃保持 Javascript 水平,但仍手动写 Lean/Python);⑤ **Not competing with humans**(无既有人的努力被复制)。"I would however caution against unrestricted LLM use when one or more of the above five favorable situations is not in effect."

同月《A digestion of the Jacobian conjecture counterexample》(2026-07-21)公开自己与 ChatGPT 的对话作"消化"示范,在 Hacker News 665+ 分;2026-07-23 tao-web 逐字访谈补上所有模糊地带;2026-07-24 ICM 2026 讲座《Mathematics in the age of AI》汇成一讲。

**与前阶段差异**:从宏观角色论回到**微观操作守则**--五条适用条件 + red-team 原则,落地为可执行清单;开始公开自己的 AI 对话作示范。

### 4.2 核心思想命题(10 个,原话支撑)

1. **AI 擅长广度,人擅长深度(比较优势)**--"AI is very good at converting billions of pieces of data into one good answer. **Humans are good at taking 10 observations and making really inspired guesses**."(The Atlantic 2024-10;Mastodon 2023-04-23)

2. **AI 是 co-author 而非 oracle(信任层级 brainstorm > code > proof)**--"**useful assistants, but not peers**: less helpful as sources of deep original ideas than as tireless systems for scanning known methods, connecting a problem to the right literature, and reporting back."(OpenAI Academy 2026-03-06)

3. **【承重墙】验证是让不可靠工具有用的唯一过滤器**--"the most promising uses of AI come from combining them with more traditional and reliable verification methods, in order to **filter out hallucinations that would otherwise render the AI output useless**."(Simons/Notices 2025-01/02)"In almost any other application, the biggest Achilles heel of AI is that it makes unverifiable mistakes. **But in mathematics, almost uniquely, you can automatically check the output**."(Nature 2026-05)这是他判断"数学是 AI 成功最清晰的地方"的根因。

4. **证明助手(Lean)是 AI 进入数学的关键基础设施 + trustless 协作**--"**you don't need to trust the people you're working with, because the program gives you this 100 percent guarantee**" -> "factory-production-type, industrial-scale mathematics"(The Atlantic 2024-10);"maybe in the future, I won't even know if [my collaborators] are AI or real people."(IEEE Spectrum 2026-06)。他区分:Lean 是"a formal proof assistant rather than an automatic theorem prover"--形式化人已有的证明,"not all that useful in discovering new proofs";最佳实践是人写/审**定理陈述**、自动化处理**证明**。

5. **red team 优于 blue team**--造系统(blue team)受最弱链限制;找缺陷(red team)是累加的。故 AI 更安全地部署在 red-teaming(审查、测试、压力检查人类工作),而非超出 red team 验证能力的 blue-team 结构角色。他把自己用 AI 的方式概括为"AI on the red team"(Klowden-Tao,arXiv:2603.26524)。

6. **数学家 job description 在改变--角色分化 + big mathematics**--"The job description is changing"(Nature 2026-04-27);routine proofs/calculation 与扫描"quick wins"交给 AI,narrative-building 与判断新技术 promise 留给人;"we will still be driving"(近期人仍掌方向盘)。

7. **LLM 适合"非关键、独立、确定性、不替代核心技能、不与人竞争"任务**--五条件见阶段 7。精炼守则:"**if you would be unable to coherently present the output of the AI in a class presentation and be able to answer questions about it without further AI assistance, it should not be part of your workflow**."(博客评论 2026-04-18)即:只在自己能 red-team 其输出的地方依赖 AI。

8. **AI 让数学回到实验科学 + 从 case studies 到 population studies**--"These problems are like distant locations that you would hike to"--旅程让人"lay down trail markers";"AI tools are like taking a helicopter to drop you off at the site. You miss all the benefits of the journey itself."(The Atlantic 2026-02)但他正面提出:数学历来只对单题做"case studies",AI 使"**population studies**"--一次扫过数千问题--成为全新且互补的能力(IPAM 2026-02)。

9. **数学是关于 human understanding,不是定理配额--Thurston + 音乐类比**--"Thurston famously said that mathematics is not about fulfilling an abstract quota of definitions, theorems, and proofs, but that it is about understanding. (Nowadays I would amend the latter to '**human understanding**'…)" "we can electronically reproduce music with perfect fidelity… and yet we still value in-person concerts, because we value human connection. … [math] has actually always been human-centric at its core, and we now need to be more honest about it."(tao-web 逐字访谈 2026-07-23)他据此划出 AI 短期难越边界:**solving**(高可验证、AI 适合)与让一个全新想法被社区**认可、消化、觉得 exciting**("a far different game",AI 进展甚微)是两回事。

10. **对 AI 风险--反转科幻排序,警惕 dread-risk bias,engage 而非 boycott**--风险排序(从最不担心到最担心):"Autonomous AI malfunction ≪ Humans using AI incorrectly < Socioeconomic disruption < **Beneficial uses of AI shut down due to AI panic** < Malicious humans < Malicious humans assisted by AI"(博客评论 2023-06)。反对把期望值计算硬套到生存风险上(Pascal wager 类比)。"**it is still more effective to engage with them to move the cost-benefit balance sheet of the technology in a better direction, than to be uniformly hostile**."(tao-web 2026-07-23)收尾原话:"AI is a truly complex topic… it is very tempting to try to simplify it by having one-dimensional narratives such as 'AI good' or 'AI bad'. **But the topic is so much richer than that**… embrace the complexity and paradoxes."

### 4.3 数学研究哲学底色(AI 立场的底座)

理解 Tao 的 AI 立场,必须先看他对"数学是什么、数学家做什么"的一贯看法--这些底色在 AI 出现前已成型,正是它们让拥抱 AI 成为他思想的自洽延伸而非妥协:

- **(a) 数学是关于 human understanding,不是定理配额**(见命题 9)--只要"理解"仍由人完成、被人珍视,工具代劳生成与验证并不威胁数学本质。这是他能平静接受 proof abundance 的根因。
- **(b) 数学本是实验科学 + 协作事业**--Lex Fridman #472(2025-06)强调实验数学兴起、理论与实验共生、"结构与随机"对偶;长期主持 Polymath 大规模协作、推动 Lean 形式化--"big mathematics"是这条路的延伸。他把数学共同体描述为"an incredibly super intelligent entity that no single human mathematician can come close to replicating"--AI 只是把集体智能再放大一层。
- **(c) "狐狸"而非"刺猬",比较优势驱动换领域**--自认"fox"(博识多领域、找连接),靠"irritation"学新领域;频繁换领域为把空间让给后来者(Thurston 自诫:自己过度成功会"杀死"领域)。这解释了他为何把 AI 工作专注在"long tail"。
- **(d) 对"困难问题"的态度:拆解、允许"作弊"暂时关掉困难维度**--主张 strategic problem simplification、视证明为有美感可优化的对象(受 Conway"extreme proofs"讲座影响)。
- **(e) 数学的"无理有效性"与普适性**--讨论 central limit theorem 等普适现象、2008 金融危机高斯假设失效的教训;这种"模型要配非数学的可靠性/稳健性追问"思维,延伸到他对 AI 的"数学只提供理论上限,法学/经济学/人文学科须为现实 messiness 打折扣"判断。
- **(f) 工具自动化一层,数学家就上移一层**--19 世纪数学家终生手解微分方程,如今 Wolfram Alpha 一秒完成;遗传学家曾用整个 PhD 测一个基因组,如今千美元几天。"**The field didn't die, it just moved to a different scale**."(Dwarkesh 2026-03)这是他能把 AI 看作"千年趋势最新一步"的历史底气。

**底色小结:理解为本、实验为法、协作为体、比较优势为节、工具为可上移的层。AI 在每一项上都是放大器而非颠覆者--这正是他立场既开放又清醒的根源。**

---

## 五、信源与未核实项

**一手源覆盖**:**teorth.github.io/tao-web**(Tao 自维护,AI 协助起草 + 本人审阅修正的 AI 观点 living summary,结构化 Part I-V;2026-07-23 逐字访谈;ICM 2026 slides)、博客 terrytao.wordpress.com 全部相关原文(2025-12-08 Erdős #1026、2026-03-23 Bernstein/Lebesgue、2026-03-29 Klowden-Tao、2026-07-16 coding agent 五条件、2026-07-21 Jacobian digestion)、arXiv 论文(2603.21453、2603.26524、2511.02864 AlphaEvolve)、Wikipedia、UCLA 主页、IPAM 官网、OpenAI Academy 博客(2026-03-06)。

**金矿说明**:tao-web living summary 由 Claude 据 Tao 公开写作整理、**Tao 本人审阅修正**,所有 Mastodon 引用经其脚注核验;本次原话引述以此站 + 博客原文为脊柱,Dwarkesh/Lex 笔记(podcastnotes/podmarized)为转述补充,已注明。

**关键订正**(两 subagent 独立交叉验证):① Erdős 问题实为 **#1026**(非 #126,博客 URL slug `erdos-problem-126` 具误导性,但 `<title>` 与正文均为 #1026);② Jacobian 猜想反例由 **Anthropic Claude Fable 5** 找到(数学家 Levent Alpöge 用 Fable 在 FIFA 世俱杯决赛期间发现,数小时内全球独立验证;猜想在 ≥3 维被证伪,2 维仍开放);③ IPAM "ready for primetime" 出自 2026-03-04~06 的 "Accelerating Math and Theoretical Physics with AI" 会议(非 2-10;2-10 是另一活动 "AI for Science: Kickoff")。

**未取得一手**:Tao 对 IMO 2025 金牌的直接引语(未找到;他一贯立场已述:"成功率先量级依赖算力/辅助/报告方式",呼吁标准化预披露基准);Nature 正文部分付费(由 tao-web living summary 交叉印证引用);精确 h-index 数值未在所抓信源查到(不补,只标注 Clarivate Highly Cited Researcher)。

**关联阅读**:[[demis_hassabis_analysis]](AI for Science/AlphaFold 对照--Tao 引"数学是 AI 安全使用上限"与 Demis 的科学 AI 路线互补)、[[李飞飞_空间智能与世界模型_2026思科AI峰会观点总结]](空间智能/具身)、[[sergey_levine_analysis]](研究者实践 AI 对照--Levine 创业、Tao 观察)、[[ilya_sutskever_analysis]](forecasting/规模--Tao 的预报谦卑对照)。
