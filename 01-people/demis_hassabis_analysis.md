---
title: "Demis Hassabis 思想演进与近360天访谈/社交媒体调研"
type: people-analysis
date: 2026-07-22
tags: [Demis Hassabis, DeepMind, AGI, AlphaFold, 诺贝尔奖, AI for Science, AI安全, Gemini, Isomorphic Labs, 世界模型]
status: active
source: "Workflow 6 agent 并行调研（Tavily MCP + curl + Wikipedia API）经主 agent 一次性整合"
---

# Demis Hassabis 思想演进与近360天访谈/社交媒体调研

> **切入点**:Demis Hassabis(Google DeepMind CEO)的背景成就、思想演进,及近 360 天(2025-07-27 至 2026-07-22)在播客/商业访谈/社交媒体的思想与叙事。
> **整合范围**:背景生平与学术成就、商业/社会工程与机构演进、个人/机构/产品思想演进、近 360 天播客与商业访谈、近 360 天社交媒体、近 360 天重大事件双轴时间轴--六维分别调研后汇总摄入,系统化梳理。
> **整理日期**:2026-07-22
> **信源层级**:L0 一手(DeepMind/Google 官方博客、Isomorphic Labs 官网、Nobel 官方、London Gazette、UCL 仓库、CBS 60 Minutes 逐字稿、希腊总理府)> L1 权威二手(Nature/Science/Guardian/Reuters/FT/TechCrunch/MIT Tech Review/Ars Technica 等)> L2 一般(Wikipedia,交叉验证用)

---

## 〇、摘要与重要澄清(先读此节)

1. **一句话主线**:Demis Hassabis 以"先解决智能、再用它解决一切"为终生使命,从象棋神童与游戏设计师出发,经 UCL 认知神经科学博士训练(海马体/情景记忆),2010 年创立 DeepMind,接连攻克 AlphaGo、AlphaFold(因蛋白结构预测获 2024 诺贝尔化学奖),沿 **RL -> 世界模型 -> 规划/system 2 -> agent -> AGI** 路线推进;机构从独立研究实验室演进为 Google DeepMind 产品+AGI 公司;近 360 天其 AGI 时间线判断从"几年"前移至"站在奇点山脚",并以 **FINRA 式前沿 AI 监管框架**主动占据"负责的加速主义"道德高地,完成从 CEO 到公共思想家的升格。

2. **事实订正(任务简述之误,经一手信源核实)**:
   - **象棋年龄**:简述称"8 岁达大师级、世界 14 岁以下第二"。Wikipedia(多源)明确为 **13 岁达大师标准、Elo 2300**(峰值 2300,1990 年 1 月),头衔 Candidate Master;"世界 14 岁以下第二"**未能确认**。
   - **游戏履历**:简述提"Black & White 2 协助"。实际他是在 Lionhead 任《**Black & White**》(2001 原作)首席 AI 程序员,非续作;Elixir Studios 作品为《Republic: The Revolution》与《Evil Genius》。
   - **封爵日期**:简述称"约 2024 新年荣誉"。据 The London Gazette(L0 一手,notice 4603787),Knight Bachelor 实为 **2024 年 3 月 28 日**(dated 28 March 2024)、**4 月 19 日刊宪报**,表彰"services to Artificial Intelligence",并非新年荣誉名单。

3. **信源限制(关键,影响置信度)**:本次调研中 **Tavily MCP 套餐额度中途耗尽**(全部端点持续返回 "exceeds your plan's set usage limit"),内置 WebSearch 在本环境亦不可用。后期 agent 改用 **curl 直抓已知 URL + Wikipedia API(干净 wikitext/extract)+ Google News RSS** 兜底。因此:① nobelprize.org、deepmind.google 博客等重 JS/SPA 站点正文未能一手渲染,诺奖等事实经 Wikipedia 对皇家科学院新闻稿的引用交叉确认;② X/Twitter @demishassabis 因反爬未取到原推,推文内容经 TechCrunch 等权威二手引述确证;③ 部分技术突破(WaveNet/AlphaZero/MuZero/AlphaProof 等)未逐项一手核验,标注为"广为人知、未一手确证"。各处均标注信源层级,存疑见第九节。

---

## 一、背景生平与学术成就

### 1.1 早年、象棋与游戏、教育

**出生与家庭**:Demis Hassabis 1976 年 7 月 27 日生于伦敦,父系希腊裔塞浦路斯人(Costas Hassabis,原姓 Hassapis,后由 p 改 b)、母系华裔新加坡人(Angela),在北伦敦长大。([Wikipedia/L2](https://en.wikipedia.org/wiki/Demis_Hassabis))

**象棋神童**:4 岁起学棋,**13 岁达大师标准、Elo 2300**(峰值 2300,1990 年 1 月),头衔 Candidate Master(候选人大师),多次担任英格兰少年队队长,1995–1997 年代表剑桥出战牛津-剑桥校际赛并获 half blue。
> ⚠️ 订正:任务简述称"8 岁达大师级、世界 14 岁以下第二"。Wikipedia(多源)明确为 **13 岁**达大师标准;"世界 14 岁以下第二"未能确认。

**早期技术与游戏**:1984 年用象棋奖金购入 ZX Spectrum 48K 自学编程,后在 Commodore Amiga 上写出第一个 AI 程序(下黑白棋 reversi)。剑桥因其年龄偏小建议先休学一年。他参加《Amiga Power》"赢取 Bullfrog 工作岗位"竞赛入职 Bullfrog Productions,从为《Syndicate》做测试起步,**17 岁与 Peter Molyneux 合作设计并主程《Theme Park》(1994)**,销量数百万、启发整个模拟沙盒品类;他拒绝七位数留任邀约,用这一年收入自费读完大学。

**教育**:先后就读 Queen Elizabeth's School, Barnet(1988–1990)、家中自学一年、再读 Christ's College 综合中学,16 岁提前两年完成 A-level。随后入**剑桥大学 Queens' College 读 Computer Science Tripos,1997 年以 double first(双第一)毕业**。

**游戏公司 Elixir Studios**:剑桥毕业后先到 Peter Molyneux 新创的 Lionhead Studios,任 2001 年《**Black & White**》首席 AI 程序员(⚠️ 订正:简述提"Black & White 2",实际为原作)。1998 年离开 Lionhead,在伦敦创办 **Elixir Studios**,与 Eidos、Vivendi Universal、微软签发行协议,亲任《Republic: The Revolution》与《Evil Genius》执行设计师(配乐获 BAFTA 提名)。Republic 因野心过大延期(Metacritic 62);Evil Genius 75。**2005 年 4 月**出售 IP 与技术资产后关闭工作室。

**认知神经科学博士**:随后重返学界,2009 年于 **UCL Queen Square 神经学研究所**获认知神经科学博士,导师 **Eleanor Maguire**,博士论文《Neural Processes Underpinning Episodic Memory》([UCL 仓库/L0](https://discovery.ucl.ac.uk/id/eprint/16126/))。其动因是"从人脑寻找新 AI 算法的灵感"。曾在 MIT(Tomaso Poggio 实验室)与哈佛任访问学者,2009 年获 Henry Wellcome 博后基金入 UCL Gatsby 计算神经科学单元(与 Peter Dayan 合作)。代表工作:PNAS 首篇论文([L1](https://www.pnas.org/doi/10.1073/pnas.0610561104))首次系统证明海马体损伤患者不仅失忆、也无法想象新体验,由此提出"**场景构建(scene construction)**"理论,连接情景记忆与想象力,入选《Science》年度十大突破。这一神经科学背景是其后"世界模型/模拟"思想的源头。

### 1.2 DeepMind 创立与初心

2010 年,Hassabis 与 **Shane Legg**、**Mustafa Suleyman** 在伦敦联合创立 DeepMind。他与 Legg 在 Gatsby 计算神经科学单元做博后时相识,与 Suleyman 通过家族世交的朋友结识;还拉来剑桥好友兼 Elixir 合伙人 **David Silver**。

**使命**:DeepMind 的使命被表述为"**先解决智能,再用它解决一切**"("solve intelligence" and then use it "to solve everything else";更简洁版本:"Step one, solve intelligence; step two, use it to solve everything else.")。具体路径是把系统神经科学的洞见与机器学习、算力硬件结合,打造越来越强的通用学习算法,朝通用人工智能(AGI)推进;早期以"让算法精通游戏"为练兵场。([Wikiquote/L2](https://en.wikiquote.org/wiki/Demis_Hassabis))

**资本与归属**:早期投资人含 Horizons Ventures、Founders Fund,以及 Peter Thiel、Elon Musk、Jaan Tallinn 等;2014 年 Google 收购后主体仍以伦敦独立实体运营。Hassabis 同时是 **Isomorphic Labs(2021 至今)** 联合创始人兼 CEO,并任英国政府 AI 顾问。

### 1.3 学术与技术突破时间线

以下为经抓取核验的里程碑(标注来源层级;未能在本会话独立核验者见第九节):

- **2013-12 DQN 玩 Atari**:训练 Deep Q-Network 仅以屏幕原始像素为输入,在 Atari 游戏达超人类水平,开创深度强化学习。([Wikipedia/L2](https://en.wikipedia.org/wiki/Demis_Hassabis))
- **2015-10 / 2016-03 / 2017 AlphaGo**:AlphaGo 5-0 胜欧洲冠军樊麾(2015-10);**4-1 胜前世界冠军李世石**(2016-03,围棋曾被视为 AI"圣杯");3-0 胜世界第一柯洁(2017)。第二局第 37 手成为标志性"创造之手"。
- **Neural Turing Machine**(神经图灵机)与降低 Google 数据中心冷却能耗等。
- **AlphaFold 系列(蛋白质结构预测,50 年科学难题)**:
  - 2016 年 DeepMind 将 AI 转向该问题;**2018-12 AlphaFold 获 CASP13 第一**(43 个蛋白中 25 个最准)。Hassabis 对《卫报》称其为"灯塔项目(lighthouse project)"。
  - **2020-11 AlphaFold 2 在 CASP14 颠覆性突破**:自由建模类中位 GDT 87.0(2018 年同类 <60),整体误差 <1 Å、可比肩实验方法,CASP 组织者宣告问题"基本解决";随后折叠全部约 2 亿已知蛋白,经与 EMBL-EBI 合建的 AlphaFold 蛋白质结构数据库免费开放。([DeepMind 官方博客/L0](https://deepmind.google/blog/article/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology))
  - **AlphaFold 3 于 2024-05-08 发布**,由 Google DeepMind 与 Isomorphic Labs 共同开发,可预测蛋白与 DNA/RNA/配体/离子复合物结构,蛋白-分子互作精度较既有方法提升 ≥50%。

> ⚠️ 以下为广为人知但本次未能独立抓取核验的 DeepMind 成就(Tavily 配额耗尽、DeepMind 大条目 curl 超时/返回空):WaveNet(2016)、AlphaGo Zero / AlphaZero(2017)、MuZero(2019)、AlphaGeometry / AlphaProof(2024)、AlphaProteo。建议后续用 L0 DeepMind 官方博客与 Nature/Science 论文逐项补证。

### 1.4 2024 诺贝尔化学奖

- **宣布(2024-10-09)**:瑞典皇家科学院宣布 2024 诺贝尔化学奖--一半授予 **David Baker**(计算蛋白质设计),另一半共同授予 **Demis Hassabis 与 John M. Jumper**(蛋白质结构预测)。([Nobel 官方/L0](https://www.nobelprize.org/prizes/chemistry/2024/hassabis/))
- **颁奖(2024-12-10)**:按惯例诺贝尔奖颁奖典礼于 12 月 10 日(诺贝尔逝世纪念日)在斯德哥尔摩举行;Hassabis 出席 2024 诺贝尔周。
- **意义**:诺贝尔化学奖首次主要表彰 AI/计算方法对生命科学的贡献,确认 AlphaFold 对蛋白质结构预测这一 50 年难题的颠覆性解决。Hassabis 与 Jumper 此前已凭 AlphaFold 获 2023 Breakthrough Prize(生命科学)与 Lasker 奖。
- **诺奖讲座猜想(思想演进关键,见 §3.6)**:Hassabis 在诺贝尔讲座提出挑衅性猜想--"任何能在自然界中被生成或发现的模式,都能被一个经典学习算法高效地发现与建模"(经 Lex Fridman 2025 访谈转述)。

### 1.5 学术荣誉

- **CBE**:2017 年获大英帝国司令勋章,列入 **2018 新年荣誉名单**,表彰"科学与技术服务"。([BBC/L1](https://www.bbc.com/news/technology-42511365); [London Gazette/L0](https://www.thegazette.co.uk/notice/2937937))
- **骑士爵位(Knight Bachelor)**:据 **The London Gazette(L0,notice 4603787)**,"For services to Artificial Intelligence",**日期 2024-03-28、刊宪日 2024-04-19**(非新年荣誉),称"Sir Demis Hassabis"。
- **学术会员**:2017 当选皇家工程院院士(FREng);**2018-05 当选皇家学会院士(FRS)**;2021 皇家工业设计师;2026 当选美国国家工程院外籍院士。
- **科学大奖(节选)**:2014 Mullard 奖;2016 Nature's 10;2020 Dan David Prize;2022 VinFuture、BBVA Frontiers of Knowledge、Princess of Asturias(与 Hinton/LeCun/Bengio 共享);**2023 Lasker、Gairdner、Breakthrough Prize**;2024 Keio Medical Science Prize。
- **媒体影响力**:Time 100(2017、2025);**2025 年度人物"AI 架构师"群体之一**(与 Altman、Amodei、黄仁勋、李飞飞、马斯克、苏姿丰、扎克伯格并列)。
- **文化产品**:纪录片《The Thinking Game》(2024 Tribeca 首映);**2026 Sebastian Mallaby 传记《The Infinity Machine: Demis Hassabis, DeepMind and the Quest for Superintelligence》**(Penguin Press,2026-03-31)。

---

## 二、商业/社会工程成就与机构演进

### 2.1 Google 收购 DeepMind(2014)与早期条款

2014-01-26,Google 确认收购 DeepMind,金额据报道在 **$400M–$650M** 之间(Google DeepMind 词条);Hassabis 词条表述为 **£400M**([Reuters/L1](https://www.reuters.com/article/google-deepmind-idUSL2N0L102A20140127/))。收购发生在 Facebook 据报 2013 年结束谈判之后。

**Demis 坚持的条款(核心社会工程成就--在出售时为 AI 治理埋下制度约束)**:
- **设立 AI 伦理委员会**:收购后成立人工智能伦理委员会;维基记载其"仍是个谜,Google 与 DeepMind 均拒绝透露成员名单"。
- **保持独立运营**:收购后"公司大部分仍作为基于伦敦的独立实体运营"。
- **不直接用于军事/武器**:广泛见诸二手媒体报道,但英文维基词条未明确陈述该条款(仅确证伦理委员会与独立运营),故标注为**广泛报道、未一手确证**。

这一系列条款使 DeepMind 在被巨头收购的同时保留研究独立性与伦理护栏,成为后来"研究实验室 -> AGI 公司"演进的制度起点。

### 2.2 早期商业化探索与争议:医疗、能源、推荐

**DeepMind Health / Streams 与皇家自由医院争议**([Wikipedia/L2](https://en.wikipedia.org/wiki/Google_DeepMind)):
- 2015-09,DeepMind 与皇家自由伦敦 NHS 信托签信息共享协议,联合开发临床任务管理应用 **Streams**(急性肾损伤预警)。
- 2016-04,《新科学家》获数据共享协议副本,披露 DeepMind Health 可访问三家伦敦医院(年接诊约 160 万患者)的入出院、急诊、病理、放射、重症数据,含 HIV、抑郁症、堕胎等敏感信息。
- 2017-07,英国信息专员办公室(ICO)裁定皇家自由向 DeepMind 移交 160 万患者数据违反《数据保护法》。DeepMind 承认"需做得更好"。
- **2018-11-13**,DeepMind 宣布医疗部门与 Streams 并入 **Google Health**,隐私倡导者批评此举背弃患者信任。

**能源(数据中心冷却)**:2014 年起 Google 用监督学习预测 PUE;2016 年受 AlphaGo 启发引入强化学习,实测 PUE 节省约 **15%**,成熟自主系统进一步达约 **30%**;Hassabis 词条另提"冷却系统能耗降低 40%"(口径为冷却系统而非整体 PUE)。

**推荐系统与端侧**:DeepMind 参与 Google Play 个性化推荐,与 Android 团队推出 Adaptive Battery、Adaptive Brightness 等端侧 ML 功能。

### 2.3 AlphaFold 开源与公共品叙事

AlphaFold 是 Demis 将 DeepMind 定位为"AI for Science"公共品供给者的核心案例。

- 2018-12 AlphaFold 赢得 CASP13;2020-11 AlphaFold2 在 CASP14 达原子级精度,被宣告"问题基本解决"。
- **2021-07**:开源版 RoseTTAFold 与 AlphaFold2 发布;一周后 DeepMind 宣布已完成几乎所有人类蛋白质及 20 种生物全蛋白质组预测,结构发布于与 EMBL-EBI 合建的 **AlphaFold 蛋白质结构数据库**。
- **2022-07**:释放 **2 亿+** 蛋白质结构预测,覆盖几乎所有已知蛋白质。
- 2024-05 AlphaFold3 发布,非商业研究可在 AlphaFold Server 免费使用。

这构成"AI for Science 公共品叙事"--把昂贵的商业 AI 能力以开源与免费数据库形式开放给全球科学界,既积累声誉资本,也为后续商业化(Isomorphic Labs)铺路。

### 2.4 Isomorphic Labs:AI 药物发现商业化

Isomorphic Labs 是 Demis 将 AlphaFold 科学声誉转化为商业价值的主通道,也是 2025–2026 窗口期最重要的机构演进事件之一。

- **成立与定位**:2021-02-24 注册、2021-11-04 公开宣布,Hassabis 创立并兼 CEO,作为 Alphabet 旗下、从 DeepMind 分拆的 AI 药物发现公司。官网使命"**Solve all disease**",称公司"在诺奖级 AlphaFold 系统之上及之外继续构建"。([Isomorphic Labs/L0](https://isomorphiclabs.com))Hassabis 引言:"我相信,AI 没有比帮助改善人类健康更重要的应用了。"
- **合作与产品**:2024-01 与 **Novartis、Eli Lilly** 达成合作;2024-05 与 Google DeepMind 联合发布 AlphaFold 3;**2026-02 发布 Drug Design Engine(IsoDDE)**,在蛋白-配体结构预测基准上将 AlphaFold 3 性能翻倍。
- **融资(窗口内重大商业事件)**:
  - 约 2025-04,完成首轮外部融资约 **$600M**(Series A),Thrive Capital 领投(L2,官方未直接确认)。
  - **2026-05-12,完成 $2.1B Series B**,Thrive Capital 领投,Alphabet、GV、MGX、Temasek、CapitalG 与 **英国主权 AI 基金**参投([L0 官方公告](https://isomorphiclabs.com/articles/isomorphic-labs-announces-series-b-investment-round))。AI 药物发现领域迄今最大单笔融资之一,英国主权基金参投具治理与产业政策含义。

### 2.5 Google DeepMind 合并(2023-04):从研究实验室走向产品+AGI 公司

2023-04,DeepMind 与 Google AI 旗下的 Google Brain 部门合并,组建 **Google DeepMind**,作为 Google 应对 OpenAI ChatGPT 冲击、加速 AI 工作的举措。维基评价此次合并"标志着 DeepMind 高管多年来争取更大自主权的努力宣告终结"--即从"被收购但保持独立的研究实验室"转向与 Google 产品体系深度整合的统一 AI 部门。

Demis 出任合并后 Google DeepMind 的 CEO,统管原 DeepMind 与 Brain 两支队伍。总部仍位于伦敦,并在美、加、法、德、瑞士设研究中心。这是机构演进关键拐点:从以"解决智能"为使命、强调研究独立性与伦理护栏的实验室,转变为同时承担旗舰产品(Gemini)与 AGI 研究的"产品+AGI 公司"。

> 注:Google 官方博客合并公告原文(L0)本轮未能取回(候选 URL 返回 404、Wayback 无快照),合并细节暂以维基(L2)为据。

### 2.6 Gemini 产品化与商业化转向

合并后,Google DeepMind 接管 Google 旗舰大模型 **Gemini** 系列及生成式 AI 工具(Imagen、Veo、Lyria 等)开发,标志 Demis 影响力从研究扩展到核心商业产品。

**Gemini 系列时间线**:
- 2023-12-06:Gemini 首发多模态大模型(Nano/Pro/Ultra),对标 GPT-4。
- 2024-12-12:Gemini 2.0 Flash。
- 2025-03-25:Gemini 2.5(推理模型,回答前先"思考")。
- **2025-11-18:Gemini 3 Pro / Deep Think**(全多模态推理,同日整合 Google Search 与 AI Mode),直接促使 OpenAI 加速推出 GPT-5.2。
- 窗口内持续迭代:Gemini 3 Flash(2025-12-17)、3.1 Pro(2026-02-19)、3.5 Flash(2026-05-19)、3.6 Flash(2026-07-21)等,约一年内五代。

生成式产品通过 Google API 与 Vertex AI 商业化;另推开放权重 Gemma 系列、编程模型 AlphaCode、智能体 SIMA、视频模型 Veo 系列、音乐模型 Lyria 3 等,构成从研究到 API/产品的完整商业栈。

### 2.7 AI 安全文化与治理角色

DeepMind 是最早系统性建立 AI 安全文化的工业实验室之一,Demis 本人在 AI 治理中扮演建言角色。

- **早期安全文化**:2016 Google Research 发布 AI 安全论文;2017 DeepMind 发布开源安全测试床 **GridWorld**(评估算法是否学会关闭其"kill switch");2017-10 成立 **DeepMind Ethics & Society** 研究单元;DeepMind 是 Partnership on AI 成员;2024-01 为机器人产品设立受阿西莫夫"机器人三定律"启发的"Robot Constitution"。
- **政策立场**:2023,Hassabis 签署"减轻 AI 灭绝风险应与应对大流行病、核战争一道列为全球优先事项"声明([CAIS/L0](https://www.safe.ai/statement-on-ai-risk));但他认为全面暂停"很难在全球执行",AI 在医疗、气候的潜在收益值得继续推进,主张优先发展衡量模型能力与可控性的评估测试。
- **治理角色**:维基称其为"UK Government AI Adviser"(英国政府 AI 顾问)。关于英国 AI Safety Institute 顾问、布莱切利园 AI 安全峰会等具体细节,本轮未取到 L0/L1 一手确认。

### 2.8 荣誉与社会影响

2024–2025 年密集顶级荣誉:诺贝尔化学奖(2024,Hassabis 占奖金 1/4);骑士爵位(2024);Time 100(2017、2025)及 2025 年度人物;FRS、Breakthrough Prize、Lasker 等。文化层面:纪录片《The Thinking Game》(2024 Tribeca)、Mallaby 传记《The Infinity Machine》(2026)。这些将"AI for Science"公共品叙事、商业化成就与国家认可叠加,巩固其"科学家-企业家-治理建言者"三位一体的公共形象。

---

## 三、个人/机构/产品思想演进

> 本维度覆盖全期,梳理从早期到 2026 的纵向脉络。核心引述主要源自 Lex Fridman Podcast #475(2025-07-23,略早于窗口起点,属全期思想维度可用的一手 transcript)、MIT Tech Review(2016)、The Guardian(2018/2023)等。

### 3.1 思想源头:游戏 AI -> 神经科学/海马体 -> AGI

Demis 的思想起点是"从棋盘到海马体"的贯通:象棋神童(13 岁 master)与游戏 AI 程序员(Theme Park / Black & White / Elixir)的早年经历,让他把"游戏模拟"视为通用智能的练兵场;UCL 认知神经科学博士(2009)对海马体/情景记忆/"场景构建"的研究,直接启发其"**心智的模拟引擎(simulation engine of the mind)**"--用想象/场景辅助规划--这一思想后来贯通到 AI 的世界模型与规划研究。2010 年创立 DeepMind,确立使命"**solve intelligence, then solve everything else**",结合系统神经科学与机器学习打造通用学习算法迈向 AGI。([MIT Tech Review/L1](https://www.technologyreview.com/s/601139/how-google-plans-to-solve-artificial-intelligence/))

### 3.2 AlphaGo 哲学:自我博弈、超越人类先验、AI 创造力

AlphaGo(2016 胜李世石)确立其方法论信念:**强化学习 + 自我博弈 + MCTS** 可建模高维空间并**超越人类先验知识**(AlphaGo Zero 完全不学人类棋谱、AlphaZero/MuZero 不学规则)。第二局**第 37 手(Move 37)**--人类专家初判误手后被公认为创造性--成为 Demis 反复征引的"AI 创造力与直觉"隐喻,以及迈向 AGI 的"通用算法证据"。胜利被视为"经典系统可高效建模自然"信念的首次大规模验证。

### 3.3 AlphaFold 与 AI for Science 范式

AlphaFold 把 DeepMind 从"感知-决策"推向"解决科学前沿"。Hassabis 2018 年对《卫报》称其为"**灯塔项目**--我们在人与资源上首次重大投入于一个基础、重要、真实的科学问题"。2020 CASP14 后"结构生物学被基本解决"的论断(及争议),2021 开源 2 亿+结构的公共品落地,确立 **AI for Science** 范式:AI 不只做语言/感知,还能解决科学前沿。2021 创立 Isomorphic Labs 即此范式的商业化延伸。

### 3.4 AGI 路线图:RL -> 世界模型 -> 规划/system 2 -> agent -> AGI

Demis 的 AGI 路线呈清晰的阶段性:**RL(感知-决策,DQN/AlphaGo)-> 世界模型(理解环境动力学,Genie 3/Veo)-> 规划与 system 2 thinking(搜索、推理,AlphaProof/AlphaGeometry、Nature 网格细胞自发涌现)-> agent(长程任务、工具使用,SIMA/Gemini)-> AGI**。他判断当前系统**增量 hill climbing 不足以达 AGI**,可能"还需要一两个大突破"。机构层面,2023 Google DeepMind 合并标志从纯研究转向"产品+研究一体化"--他本人表述:"我看不出艺术与科学、产品与研究之间的边界。对我而言它是一个连续体。"

### 3.5 安全与对齐:谨慎乐观、10 倍安全投入

Demis 持"**谨慎乐观(cautious optimism)**"立场:承认灾难概率"肯定不为零,而且可能不可忽略",但拒绝给精确 p(doom) 数字,"唯一理性、明智的做法是以谨慎乐观的态度推进"。他反对全面暂停(难全球执行、牺牲医疗/气候收益),主张优先发展评估测试;并强调"随着越来越接近 AGI 这条线,(安全)方面的努力可能需要是现在的 **10 倍**"。2023 签署 CAIS 灭绝风险声明,但同时在加速与暂停间取"负责任的加速"中间路线。

### 3.6 信息本体论与诺奖猜想

在 2024 诺贝尔讲座(经 Lex Fridman #475 转述)与访谈中,Demis 展现一以贯之的本体论立场:
- **信息第一性**:"我认为信息是第一性的,信息是宇宙最基本的单元,比能量和物质更基本。"
- **P vs NP 是物理问题**:宇宙视为信息系统,AGI 是经典计算的终极表达。
- **诺奖猜想**:"任何能在自然界中被生成或发现的模式,都能被一个经典学习算法高效地发现与建模"--将 AlphaGo/AlphaFold 的成功上升为关于经典计算与可学习性的普遍论断。
- **AGI 后愿景**:"激进富足(radical abundance)时代"--资源充裕到足够每个人分享,消除稀缺。

### 3.7 AGI 时间线判断的演进(核心)

这是 Demis 思想演进中最具跟踪价值的一条轴,口径随竞争加剧而前移:

| 时点 | 出处 | 表述 |
|---|---|---|
| 早年 | 多次访谈 | "几十年" |
| 2025-07-23 | Lex Fridman #475 | "未来五年内、到 2030 年前后约 50% 概率(实现 AGI)" |
| 2025-08-03 | CBS 60 Minutes | "未来五到十年内" |
| 2026-01-24 | 达沃斯 CNBC | "中间派""经验性问题",仍列缺失能力(持续学习/真正创造力/长期规划) |
| 2026-05 约 | Google I/O 2026 | "我们正站在奇点的山脚下(foothills of the singularity)" |
| 2026-05-26/27 | Axios / Sherwood | "AGI 在 2030 年" / "AGI 还有 3 到 4 年" |

10 个月内口径从"5–10 年"推到"奇点山脚",反映叙事随竞争压力(OpenAI/Anthropic)渐激进,但仍保留"missing capabilities"作审慎锚点。

### 3.8 机构演进与近期主轴

机构思想演进:DeepMind 从**纯研究实验室(2010-2014,学术优先不急于商业化)-> Google 旗下研究实验室 -> Google DeepMind 产品+研究一体化(2023)-> AGI 公司**;"做登月研究"到"产品化与 AGI 并进"。近期(2025-2026)主轴:**planning/world model/agent**(Genie 3、Project Genie、SIMA 2、Gemini Robotics)与 **AI for Science**(Weather Lab、Nature "DNA decoder" 封面、Isomorphic Drug Design Engine)并进,迈向 AGI。

---

## 四、近 360 天播客与商业访谈(2025-07-27 至 2026-07-22)

### 4.1 窗口内访谈清单

| 日期 | 场合/主持人 | 核心主题 |
|---|---|---|
| 2025-08-03 | CBS《60 Minutes》(Scott Pelley,二度专访) | AGI 时间线(5–10 年)、Project Astra 多模态、机器人、涌现能力与"二元性"风险、AlphaFold/药物研发/"治愈所有疾病"、radical abundance、像教孩子般教 AI 道德、自我意识、呼吁"新哲学家" |
| 约 2025-09-12 | All-In Podcast(@allin 官方)《Inside Google DeepMind: AGI, Robotics, & World Models》 | AGI、机器人、世界模型(标题即主题;全文 transcript 未取到,具体内容未核实) |
| 2025-12-16 | Google DeepMind 官方播客《The Future of Intelligence》(Hannah Fry,年度对谈) | Gemini 3、世界模型、"根节点问题"(AlphaFold->材料/聚变/量子)、"参差智能"与 AGI、幻觉、模拟世界与机器人、社会影响、后 AGI 社会、计算极限与意识 |
| 2026-01-24 | 达沃斯 WEF 2026,CNBC Squawk Box(Andrew Ross Sorkin) | Gemini 3 登顶榜单、Apple/Siri 合作、AGI"中间派"观点与缺失能力、AI 泡沫/"frothy"警告、就业、算力与资源 |
| 2026-02-11 | Fortune vodcast《Titans and Disruptors》(Alyson Shontell) | "4 步法"让 Google 回到创新"黄金时代"、AI 提升生产力 vs 员工倦怠、回顾 2014 收购(正文付费墙,仅获标题/框架) |
| 约 2026-05-19 | Google I/O 2026 主题演讲 | 宣称"站在奇点山脚(foothills of the singularity)"、AI for Science(WeatherNext 飓风预警)、专用工具 vs 智能体两条路线 |

> 窗口外排除:Lex Fridman #475(约 2025-07-23,早于窗口起点 3-4 天,见 §3 思想演进维度引用)、Dwarkesh Patel 访谈(核实为 2024-02-28,明显窗外)。No Priors / Hard Fork / 20VC / Stratechery 等线索因检索受限未逐一核实,存疑未收。

### 4.2 按主题归纳的核心思想

**1. AGI 时间线:"5 到 10 年" -> "奇点山脚"。** 60 Minutes(2025-08-03)中 Pelley 问是否"on track for AGI",Hassabis 答"In the next five to ten years, I think",并描绘 2030 图景:"a system that really understands everything around you in very nuanced and deep ways and are kind of embedded in your everyday life"。达沃斯(2026-01-24)取"中间派"框架--"I have a kind of in between view which is that I think it's an empirical question",一方面 LLM"getting better and better with each iteration and we see no end to that",另一方面"to get to full AGI, there's some missing capabilities still"(持续学习、真正创造力、长期规划与推理)。I/O 2026 升级为"foothills of the singularity"。([MIT Tech Review/L1](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/))

**2. AI for Science:以 AlphaFold 为"根节点"范式,向材料、聚变、量子、气象扩展。** Google DeepMind 播客(2025-12-16)提出"**root node problems**"框架:AlphaFold 是已解的根节点,下一目标是材料科学(室温超导、电池)、聚变能源(与 Commonwealth Fusion 新合作)、量子计算。60 Minutes 戏剧化回顾:蛋白 3D 结构"less than 1% were known. Mapping each one used to take years. DeepMind's AI model did 200 million in one year"。I/O 2026 以 WeatherNext 提前预警牙买加飓风 Melissa 为科学 AI 案例。

**3. AlphaFold / Isomorphic:从结构预测到"治愈所有疾病"。** 60 Minutes:"on average, it takes ten years and billions of dollars to design just one drug. We can maybe reduce that down from years to maybe months or maybe even weeks";"I think one day maybe we can cure all disease with the help of AI";被问"the end of disease?"答"I think that's within reach. Maybe within the next decade or so"。

**4. Agent / Gemini:从"揭示世界"到"在世界中行动"。** 60 Minutes:训练 Gemini"to not just reveal the world but to act in it like booking tickets and shopping online. It's a step toward AGI",演示 Project Astra。达沃斯:"our latest Gemini model, Gemini 3 is working... topping most of the leaderboards";披露 Apple 选择 Gemini 驱动 Siri--"a massive vote of confidence"。

**5. 安全/对齐:"二元性"与"像教孩子"。** 60 Minutes 给出风险框架:"There's two worries... One is that bad actors... repurpose these systems for harmful ends. And then the second thing is the AI systems themselves as they become more autonomous... Can we make sure that we can keep control... aligned with our values";担忧"the race for AI dominance is a race to the bottom for safety",呼吁国际协调。对"能否教 AI 道德"答"I think you can. They learn by demonstration... much in the way that you would teach a child"。达沃斯则在乐观中插入对 AI 泡沫的警告:"new hot startups that are raising billions of dollars in a seed round with no product or technology yet, that seems a little bit frothy to me"。

**6. 意识/哲学/缺失能力。** 60 Minutes:"I don't think any of today's systems to me feel self-aware or conscious",但"theoretically it's possible";以碳基 vs 硅基底质论证机器意识可能不同;指出当前系统"don't have curiosity... lacking imagination and intuition",但"next maybe five to ten years"将能"coming up with [a novel conjecture] in the first place";呼吁"new great philosophers... in the next five, ten years"。Google DeepMind 播客专章讨论"limits of computation and the nature of consciousness"。

### 4.3 故事叙述手法(专章)

Hassabis 在窗口内访谈中反复使用一套高度稳定的叙事装置,使同一套观点可同时面向大众、投资者与决策者:

1. **"从游戏到科学"的传记弧线**:60 Minutes 用童年棋局开场--"At 12, he was the number two champion in the world for his age. This passion led to computer chess, video games and, finally, thinking machines";达沃斯 Sorkin 也以"约十年前 AlphaGo 击败世界围棋第一人"作引子。效果:把 AGI 使命叙述为一生的必然延伸,赋予连续性与正当性。
2. **"登月式"使命叙事--"推进人类知识的终极工具"**:60 Minutes:"I wanted to see if we could advance human knowledge... to build what I think is the ultimate tool for advancing human knowledge, which is AI"。把 DeepMind 定位为科学工具建造者而非单纯商业公司。
3. **把 AlphaGo 的"直觉"、AlphaFold 的"解决生物学"框架化**:用"root node problems"把 AlphaFold 包装为可复制范式(解一个根节点即解锁下游无数应用);把蛋白结构预测戏剧化("200 million in one year")再顺势推到"治愈所有疾病"。以一个已兑现的奇迹(诺奖)为信用背书,担保更宏大承诺。
4. **风险与乐观并行的"负责的乐观主义"(二元性叙事)**:先讲"radical abundance",紧接"two worries"(坏演员 + 系统自主失控),担忧"race to the bottom for safety"。在加速主义立场中嵌入审慎,争取公众与监管信任。
5. **对 AGI 时间线"谨慎但渐进激进"的表述策略**:60 Minutes 给"5 到 10 年";达沃斯用"中间派""empirical question"留科学不确定性退路;I/O 2026 升级为"奇点山脚"。使预测"失败也不算食言"。
6. **诺奖后身份位移--从"AI 实验室创始人"到"科学家/人文学科桥梁"**:60 Minutes 结尾用"诺贝尔名册何时由机器签署"作哲学叩问,呼吁"new great philosophers";Google DeepMind 播客设专章谈"计算的极限与意识本质"。把 AI 议题从工程问题提升为文明级哲学议题。
7. **用具体实验室演示锚定抽象承诺**(贯穿):60 Minutes 让 Astra 现场识画、机器人"黄+蓝=绿"推理;达沃斯以 Gemini 登顶榜单、Apple 选用 Siri 作"产品质量"背书;I/O 以 WeatherNext 飓风预警作"AI for Science 真实兑现"。每个宏大判断都附一个可感知的小故事。

---

## 五、近 360 天社交媒体(2025-07-27 至 2026-07-22)

### 5.1 X(@demishassabis)纲领性长文:FINRA 式前沿 AI 监管框架

> X 对 curl 反爬严格(直取仅返回 JS 外壳,Nitter 已失效),本节原推文字均经权威二手交叉核实,凡未注明一手者均为转载/引用层级。

**2026-07-14 纲领性 X 长文《A Framework for Frontier AI and the Dawning of a New Age》--窗口内最核心的一条**。TechCrunch(L1)明确写道:"In an X post on Tuesday morning, Google DeepMind CEO Demis Hassabis called for the creation of a new regulatory body to oversee frontier model releases."

核心主张(TechCrunch 引述原帖):
- "Initially, Frontier Labs would voluntarily share models with the Standards Body for review up to **30 days before release**. Once the assessment protocol is shown to be effective and robust, formalisation could quickly follow, meaning that Frontier Models would be required to pass it to be deployed in the US market."
- "The strength of this approach is it would be technically focused, while at the same time supporting innovation and incentivising responsible behaviour... could be **ratcheted up** if the seriousness of the situation demands."

该机构设想由**美国政府背书、AI 行业出资、独立运营**,人员含开源代表与业内技术专家。同日集群报道:Axios"calls for U.S.-led global AI watchdog"、FT"calls for US-led body to test 'frontier' AI models"、The Verge"time for a global AI watchdog - led by the US"、The Economist"Demis Hassabis has a plan to harness AI safely"、Business Insider"humanity has a 'precious window' to ensure AGI is safe"。

**与 6 月 G7 的连续性**:该框架并非孤立。2026-06-12 qz 报道 Sam Altman、Demis、Dario Amodei 赴 G7 法国;2026-06-18 qz 报道"Anthropic and Google DeepMind CEOs called for a U.S.-led AI coalition at the G7"。7 月 X 长文是把 G7 口头呼吁落地为成文方案。

**悼念/致谢类**:2026-06-20,诺贝尔共同得主 John Jumper 离开 DeepMind 转投 Anthropic。TechCrunch 引 Jumper 的 X 帖:"Demis Hassabis 'took a real chance letting me lead the AlphaFold team just six months after finishing my PhD, and the entire GDM team taught me so much about how to do great science.'" Demis 本人回应性 X 帖未直采到原文,但 Semafor(2026-06-24)以"DeepMind Chief Demis Hassabis says Google's still winning AI talent"概括其立场。

### 5.2 DeepMind 官方博客:署名分工的叙事

窗口内 DeepMind 官方博客高频发布,但一个关键观察:**重大产品发布基本不再由 Demis 本人署名**。JSON-LD 作者字段显示:Gemini 3.5 与 Gemini Omni(2026-05-19)署名 Koray Kavukcuoglu(Chief Scientist);Gemini 3 Deep Think(2026-02-12)署名"The Deep Think team";Gemini 3.1 Pro(2026-02-19)署名"The Gemini Team";A24 合作(2026-06-22)署名 Eli Collins(VP Product);Gemini for Science(2026-05-19)署名 Pushmeet Kohli;AGI 认知框架(2026-03-17)署名 Ryan Burnell。**Demis 本人署名的窗口内博文仅检索到 1 篇(见下)**。这构成叙事分工:**产品/技术由首席科学家与产品负责人出面,Demis 退守"使命/地缘/安全"层面的署名与声明**。

**Demis 出镜但非署名的官方内容**:2025-08-11 博客《Hear Google DeepMind CEO Demis Hassabis discuss how world model capabilities are helping AI understand reality》--"In the latest episode of the Google AI: Release Notes podcast, host Logan Kilpatrick sits down with Google DeepMind CEO Demis Hassabis to discuss Deep Think in Gemini 2.5, the 'world model' capabilities of Genie 3 and the new Game Arena on Kaggle as a benchmark for driving the industry closer to AGI."([L0](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/ai-release-notes-podcast-demis-hassabis/))这是窗口内 Demis 在官方渠道阐述"世界模型 -> AGI"路径的代表性一手内容。

**安全/AGI 治理类**:2026-03-17《Measuring progress toward AGI: A cognitive framework》([L0](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/measuring-agi-cognitive-framework/)),提出认知框架评估 AGI 并启动 Kaggle 黑客松--把"AGI 进度衡量"制度化。

**科学/公共品类**:2026-05-19《Gemini for Science》;2026-06-22 DeepMind+A24 研究合作(TechCrunch 报道为 7500 万美元押注 AI 进好莱坞);2026-06-17 AMIE 医疗 AI 登 Nature。共同支撑"AI 为科学/公共品"框架。

### 5.3 Demis 署名博文《Platform 37 and The AI Exchange》(2026-03-12)

窗口内唯一检索到的 Demis 署名 Google 官方博客([L0](https://blog.google/company-news/inside-google/around-the-globe/google-europe/united-kingdom/platform-37-the-ai-exchange/)),几乎集齐其全部叙事母题:

- **起源神话锚定**:新楼命名 Platform 37 致敬 AlphaGo 的"Move 37"--"'Move 37' was so unconventional that human experts initially thought it was a mistake. But as the game unfolded, it became clear it enabled AlphaGo to win the game. AlphaGo's victory heralded the beginning of what is now recognized as the modern era in AI, and catalyzed our work using AI to tackle scientific problems."
- **科学公共品清单**:"our AI systems have helped accelerate advances in fields like materials discovery, fusion energy research, mathematical reasoning and biology."
- **安全责任嵌入**:"our world-leading AI researchers, engineers, ethicists and others will build on our track record of safe and responsible AI development."
- **科学家-创业者双重身份 + 纪念碑叙事**:"I see this spectacular building as more than an office - it is a **monument to science and intelligence**... pioneering the path towards artificial general intelligence to build a better future for the benefit of everyone."
- **地缘/英国归属**:"The UK is a center of extraordinary technological innovation"(呼应 Fortune 2026-04-15 报道"Demis Hassabis is very happy to stay [in London]… Silicon Valley has no monopoly on AI brainpower")。

该篇是窗口内 Demis 亲自下场书写的最完整"使命宣言"式官方文本,与 7 月 14 日 X 安全框架长文形成"科学使命(3 月)+ 安全治理(7 月)"两条署名主线。

### 5.4 故事叙述手法(官方渠道叙事风格)

综合窗口内官方渠道与 Demis 公开声明,其叙事风格稳定且高度模式化:

1. **纪元命名与里程碑式宣告**:7 月 X 长文标题《...Dawning of a New Age》;Platform 37 称新楼"科学与智能的纪念碑";"10 倍工业革命"(Guardian 2025-08-04)、"物种级跃迁"(Stanford Daily 2026-05-29)反复出现--把产品/政策抬升到文明转折高度。
2. **"为全人类/科学"的公共品框架**:"for the benefit of everyone"(Platform 37)、"solve all disease"(Isomorphic 21 亿美元融资)、"追求深刻而非利润与平庸"(Reuters 2025-11-13)--把商业行为去商业化,赋予公共品正当性。
3. **科学家-创业者双重身份**:Demis 在产品发布中退居幕后(由 Koray 等署名),自己只在"深刻/长期/使命"层面发声--Fortune"thinking about something far bigger [than chatbot wars]"、Fast Company"the long game of AI"。这一分工本身就是叙事:让首席科学家讲技术,CEO 讲文明意义。
4. **风险责任叙事(主动自我监管)**:7 月 FINRA 框架("precious window"、"ratcheted up"、发布前 30 天审查)+ Platform 37"safe and responsible AI development"+ AGI 认知框架(2026-03-17)+ The Atlantic 人物特写《The Man Who Thought He Could Keep AI Safe》(2026-03-29)--主动把"守门人"角色揽在身上。
5. **起源神话锚定(AlphaGo/Move 37)**:Platform 37 命名、"catalyzed our work using AI to tackle scientific problems"、AlphaGo 周年韩国推进(EdTech 2026-05-13)--AlphaGo 被反复征引为"现代 AI 时代起点"的创始神话。
6. **地缘叙事与多极安全**:7 月框架明确"美国主导",Economist(2026-07-15)副题"减轻对美中两国的依赖","China just months behind"(CNBC 2026-01-15),"happy to stay in London"(Fortune 2026-04-15)--把安全治理嵌入大国竞争与多极平衡框架。
7. **团队致谦与人才争夺的反叙事**:Jumper 离职转投 Anthropic,Demis 未公开挽留式表态,而是借 Semafor"Google 仍在赢 AI 人才战"定调;Jumper 致谢"导师-门徒"叙事闭环,把人才流失转化为机构魅力力的反叙事。

---

## 六、近 360 天重大事件双轴时间轴(2025-07-27 至 2026-07-22)

### 6.1 时间轴总述(按季度)

**窗口界定**:严格收录 2025-07-27 至 2026-07-22 间事件;窗口前夕(2025 年 2–6 月)关键节点仅作背景:AlphaGeometry 2(2025-02-05)、AlphaEvolve(2025-05)、Veo 3(2025-05-20)、Isomorphic 首轮融资 $600M(2025-04,窗外)、Gemini 2.5 Pro/Flash GA(2025-06-17)、Google DeepMind 入选 Time 100 最具影响力公司(2025-06-26)。

**2025 Q3(8–9 月):研究突破 + 现象级消费爆款 + 定调性表态。** 8-04 Hassabis 接受《卫报》长篇专访,抛出窗口内最具传播力判断--AI 将"比工业革命大 10 倍、可能快 10 倍",谈"彻底的丰裕",同时罕见流露审慎("希望科技巨头当初走得慢一些")。8-05 DeepMind 发布 **Genie 3** 世界模型。8-26 **"Nano Banana"**(Gemini 2.5 Flash Image)正式发布,引爆"3D 手办"图像病毒热潮,数周内为 Gemini 拉来逾 1000 万新用户、超 2 亿次编辑。9 月发布 Gemini Robotics 1.5;9-13 Hassabis 与希腊总理 Mitsotakis 公开对谈([希腊总理府/L0](https://www.primeminister.gr/en/2025/09/13/36924))。

**2025 Q4(10–12 月):旗舰换代 + 科学验证 + 声誉顶点。** 11-04 **Weather Lab** 在 2025 大西洋飓风季击败 NOAA GFS、获美国国家飓风中心认可。11-18 Google 发布 **Gemini 3 Pro 与 Gemini 3 Deep Think**(全模态推理,整合 Search/AI Mode),直接促使 OpenAI 加速推出 GPT-5.2。11-20 连发 Nano Banana Pro 并聘请波士顿动力前 CTO 打造"机器人界的 Android"。约 12 月 Hassabis 作为"AI 架构师"群体入选《时代》2025 年度人物;12-04 Deep Think 推送 Ultra 用户,12-17 Gemini 3 Flash 发布。

**2026 Q1(1–3 月):科学封面 + 药物设计引擎 + 传记出版。** 1-12 Apple 宣布新版 Siri 采用 Gemini;1-28 DeepMind 登上《Nature》第 649 卷封面("DNA decoder",其第 9 篇 Nature 封面)([L0](https://www.nature.com/nature/volumes/649/issues/8099));1-29 向 Ultra 用户发布 Project Genie。约 2 月 Isomorphic 发布 **Drug Design Engine**(蛋白-配体预测性能达 AlphaFold 3 两倍)。2-18 Lyria 3、2-19 Gemini 3.1 Pro、2-26 Nano Banana 2、3-03 Gemini 3.1 Flash Lite 相继发布。3-16《卫报》刊发 Mallaby 传记书评,**3-31 Sebastian Mallaby 传记《The Infinity Machine》由 Penguin Press 出版**--思想/传记轴在窗口内最高规格事件。

**2026 Q2–Q3(4–7 月):高频迭代收尾 + 监管框架。** 4-02 Gemma 4;约 4 月 Gemini Robotics ER-1.6;5-19 Gemini 3.5 Flash + Gemini Omni + Gemini for Science,约 5 月 Google I/O 2026(Demis 宣称"奇点山脚");6-12 G7 法国(三 CEO 呼吁美国主导 AI 联盟);6-20 Jumper 离职转投 Anthropic;6-22 DeepMind+A24 合作;7-14 Demis X 长文《A Framework for Frontier AI and the Dawning of a New Age》;7-21(窗口末日前一天)Gemini 3.6 Flash 与 3.5 Flash-Lite。

**主线归纳**:窗口内 DeepMind 同时在三条战线推进--(1) Gemini 代际跃迁(2.5->3->3.1->3.5->3.6,约一年五代);(2) 科学与世界模型(Genie 3、Weather Lab、Nature "DNA decoder" 封面、Isomorphic Drug Design Engine);(3) Demis 个人从"CEO"向"公共思想家"升格(《卫报》专访、Time 年度人物、Mallaby 传记、FINRA 框架)。

### 6.2 双轴对照表(事件轴 ↔ 思想/声明轴)

| 日期 | 事件轴(左) | Demis 对应声明/思想节点(右) |
|---|---|---|
| 2025-08-04 | (专访节点本身) | 《卫报》专访:AI"比工业革命大 10 倍、可能快 10 倍",谈"彻底的丰裕",称"希望科技巨头当初走得慢一些" |
| 2025-08-05 | Genie 3 世界模型发布 | 延续"模拟引擎/世界模型"研究理念(源自神经科学 scene construction 思想) |
| 2025-08-26 | Nano Banana 正式发布、引爆图像病毒热潮 | (体现"AI 普惠消费端"影响力) |
| 2025-09-13 | 与希腊总理 Mitsotakis 公开对谈 | 以"AI 顾问/公共知识分子"身份参与政策对话 |
| 2025-11-18 | Gemini 3 Pro / Deep Think 发布、整合 Search | 呼应"解决智能、再用智能解决一切"使命;Deep Think 延续"推理/思考"路线 |
| 2025-11-20 | 聘请波士顿动力前 CTO | 呼应早年"将 Gemini 与机器人结合、物理交互世界"设想 |
| 约 2025-12 | (产品线持续) | 入选《时代》2025 年度人物--思想影响力年度顶点 |
| 2026-01-28 | 登《Nature》"DNA decoder" 封面 | 延续 AI for Science 主张(AlphaFold 之后的科学发表主线) |
| 约 2026-02 | Isomorphic 发布 Drug Design Engine | 呼应"AlphaFold 是药物发现起点"的长期判断 |
| 2026-03-12 | Platform 37 / AI Exchange 博文(Demis 署名) | Move 37 起源神话、"智能纪念碑"、AGI"为所有人"使命 |
| 2026-03-31 | Mallaby 传记《The Infinity Machine》出版 | "追求超级智能"叙事被外部权威系统化 |
| 2026-05-19 | Gemini 3.5 + Gemini for Science;约 5 月 I/O 2026 | "站在奇点山脚";AI for Science 两条路线(专用工具 vs 智能体) |
| 2026-06-20 | Jumper 离职转投 Anthropic | (未公开挽留;借"仍在赢 AI 人才"定调,导师-门徒反叙事) |
| 2026-07-14 | Demis X 长文《A Framework for Frontier AI...》 | FINRA 式标准机构、发布前 30 天审查、美国主导;"珍贵窗口" |
| 2026-07-21 | Gemini 3.6 Flash / 3.5 Flash-Lite | Gemini 进入稳定高频小版本迭代 |

### 6.3 窗口内事件清单(节选,按日期升序)

- 2025-08-04《卫报》专访"10 倍工业革命"
- 2025-08-05 Genie 3 世界模型
- 2025-08-12 / 08-26 Nano Banana 登场与正式发布(1000 万+新用户)
- 2025-09-13 与希腊总理对谈
- 2025-11-04 Weather Lab 超越 NOAA
- 2025-11-18 Gemini 3 Pro / Deep Think(促使 OpenAI 加速 GPT-5.2)
- 2025-11-20 聘波士顿动力前 CTO
- 约 2025-12 入选 Time 2025 年度人物
- 2026-01-12 Apple Siri 采用 Gemini
- 2026-01-28 Nature "DNA decoder" 封面(第 9 篇)
- 约 2026-02 Isomorphic Drug Design Engine(AF3 性能翻倍)
- 2026-03-31 Mallaby《The Infinity Machine》出版
- 2026-05-12 Isomorphic $2.1B Series B(英国主权 AI 基金参投)
- 2026-05-19 Gemini 3.5 / Gemini Omni / Gemini for Science
- 2026-06-20 Jumper 离职转投 Anthropic
- 2026-06-22 DeepMind+A24 合作($75M)
- 2026-07-14 Demis X 长文 FINRA 框架
- 2026-07-21 Gemini 3.6 Flash

---

## 七、系统化梳理:Demis Hassabis 的思想脉络

```
象棋神童(13 岁 master, Elo 2300) -> 游戏设计(Theme Park / Black & White / Elixir)
      │  从游戏模拟与神经科学寻找 AI 算法灵感
      ▼
UCL 认知神经科学博士(海马体/情景记忆/scene construction, 2009)
      │  "心智的模拟引擎";2010 确立使命 solve intelligence, then solve everything else
      ▼
DeepMind 创立(2010) -> Google 收购(2014, AI 伦理委员会 + 伦敦独立运营)
      │  以游戏为练兵场:DQN(2013) -> AlphaGo(2016, Move 37)
      ▼
AlphaGo 哲学:自我博弈 + 超越人类先验;AI 创造力与直觉
      │  从"感知-决策"转向"解决科学前沿"
      ▼
AlphaFold(2018 CASP13 -> 2020 CASP14 基本解决 -> 2021 开源 2 亿+结构)
      │  AI for Science 范式;"灯塔项目";2024 诺贝尔化学奖
      ▼
诺奖猜想:经典学习算法可高效建模自然中可生成的模式
      │  信息第一性;P vs NP 是物理问题;AGI 路线 RL->世界模型->规划->agent->AGI
      ▼
Google DeepMind 合并(2023) -> Gemini 产品化 + AGI 研究并进(产品/研究连续体)
      │  Isomorphic Labs(2021, Solve all disease) -> 2026 $2.1B B 轮
      ▼
AGI 时间线前移:几十年 -> 50% by 2030 -> 5-10 年 -> 奇点山脚 -> 3-4 年
      │  安全:谨慎乐观、p(doom) 非零、安全投入需 10 倍、FINRA 式监管
      ▼
近 360 天:从 CEO 升格为公共思想家(Time 年度人物 / Mallaby 传记 / FINRA 框架)
      │  叙事:从游戏到科学的弧线 + 负责的乐观主义 + 起源神话锚定(Move 37)
      ▼
终局:追求超级智能(《The Infinity Machine》),AGI 为全人类
```

**一句话主线**:Demis Hassabis 以"先解决智能、再用它解决一切"为终生使命,从象棋神童与游戏设计师出发,经 UCL 认知神经科学博士训练(海马体/情景记忆/scene construction),2010 年创立 DeepMind 并接连攻克 AlphaGo、AlphaFold(因蛋白结构预测获 2024 诺奖),沿 **RL -> 世界模型 -> 规划 -> agent -> AGI** 路线推进,机构从独立研究实验室演进为 Google DeepMind 产品+AGI 公司(Isomorphic Labs 承载"治愈所有疾病"商业化);近 360 天其 AGI 时间线判断从"几年"前移至"站在奇点山脚",并 以 FINRA 式前沿 AI 监管框架主动占据"负责的加速主义"道德高地,完成从 CEO 到公共思想家的升格--叙事上始终以"从游戏到科学"的弧线 + "负责的乐观主义"二元性 + AlphaGo/Move 37 起源神话为稳定装置。

**与库内其他人物的思想交叉**:
- AGI 时间线 / 前沿安全:[[ilya_sutskever_analysis]](规模结束·价值函数)、[[leopold_aschenbrenner_analysis]](瓶颈轮动)、[[anthropic_openai_ai_forecasting_depts_analysis]](RSP/Preparedness/Superalignment)--Demis 的"谨慎乐观 + 10 倍安全投入 + FINRA 框架"是介于加速派与暂停派之间的"负责任加速"路线。
- AI for Science / 空间智能:[[李飞飞_空间智能与世界模型_2026思科AI峰会观点总结]]--二者都以"世界模型"为 AGI 实现路径,李飞飞从视觉/空间智能切入,Demis 从 RL/规划切入,殊途同归。
- 产业领袖叙事:[[jensen_huang_thoughts_analysis]](五层蛋糕)--同列 Time 2025 年度人物"AI 架构师",黄仁勋重算力基建叙事,Demis 重科学使命叙事。

---

## 八、参考来源

**L0 一手**
- DeepMind/Google 官方博客:https://blog.google/deepmind/ 、https://deepmind.google/blog/
- AlphaFold 解决 50 年大挑战(2020-11):https://deepmind.google/blog/article/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology
- Gemini 3 Pro/Deep Think 发布(2025-11-18):https://blog.google/products/gemini/gemini-3/
- Demis 署名《Platform 37 and The AI Exchange》(2026-03-12):https://blog.google/company-news/inside-google/around-the-globe/google-europe/united-kingdom/platform-37-the-ai-exchange/
- Release Notes 播客:Demis 谈世界模型/AGI(2025-08-11):https://blog.google/innovation-and-ai/models-and-research/google-deepmind/ai-release-notes-podcast-demis-hassabis/
- Measuring progress toward AGI: A cognitive framework(2026-03-17):https://blog.google/innovation-and-ai/models-and-research/google-deepmind/measuring-agi-cognitive-framework/
- Isomorphic Labs 官网(使命"Solve all disease"):https://isomorphiclabs.com
- Isomorphic Labs $2.1B Series B 公告(2026-05-12):https://isomorphiclabs.com/articles/isomorphic-labs-announces-series-b-investment-round
- Nobel 官方 2024 化学奖 Hassabis 事实页:https://www.nobelprize.org/prizes/chemistry/2024/hassabis/facts/
- The London Gazette CBE(2018 新年荣誉,notice 2937937):https://www.thegazette.co.uk/notice/2937937
- The London Gazette Knight Bachelor(2024-03-28,notice 4603787):https://www.thegazette.co.uk/notice/4603787
- UCL 博士论文《Neural Processes Underpinning Episodic Memory》(2009):https://discovery.ucl.ac.uk/id/eprint/16126/
- CBS 60 Minutes 逐字稿(2025-08-03):https://www.cbsnews.com/news/artificial-intelligence-google-deepmind-ceo-demis-hassabis-60-minutes-transcript/
- CNBC Television 达沃斯 2026 官方 YouTube(2026-01-24):https://www.youtube.com/watch?v=5XqDzEtYnqI
- Nature 第 649 卷封面"DNA decoder"(2026-01-28):https://www.nature.com/nature/volumes/649/issues/8099
- 希腊总理府 Mitsotakis 与 Hassabis 对谈(2025-09-13):https://www.primeminister.gr/en/2025/09/13/36924
- CAIS AI 灭绝风险声明(2023):https://www.safe.ai/statement-on-ai-risk
- PNAS 2007 海马体/想象研究:https://www.pnas.org/doi/10.1073/pnas.0610561104

**L1 权威二手**
- Lex Fridman Podcast #475 transcript(2025-07-23,诺奖猜想/AGI 50% by 2030/p(doom)/10 倍安全):https://lexfridman.com/demis-hassabis-2-transcript
- MIT Tech Review 2016(DeepMind 使命):https://www.technologyreview.com/s/601139/how-google-plans-to-solve-artificial-intelligence/
- MIT Tech Review 2026-05-22(I/O 2026"奇点山脚"):https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/
- The Guardian 2018-12(AlphaFold"灯塔项目"):https://www.theguardian.com/science/2018/dec/02/google-deepminds-ai-program-alphafold-predicts-3d-shapes-of-proteins
- The Guardian 2023-10(AI 风险如气候危机):https://www.theguardian.com/technology/2023/oct/24/ai-risk-climate-crisis-google-deepmind-chief-demis-hassabis-regulation
- The Guardian 2025-08-04("10 倍工业革命"专访):https://www.theguardian.com/technology/2025/aug/04/demis-hassabis-ai-future-10-times-bigger-than-industrial-revolution-and-10-times-faster
- The Guardian 2026-03-16(Mallaby 传记书评):https://www.theguardian.com/books/2026/mar/16/the-infinity-machine-by-sebastian-mallaby-review-the-story-of-the-man-who-changed-the-world
- Reuters 2014(Google 4 亿英镑收购):https://www.reuters.com/article/google-deepmind-idUSL2N0L102A20140127/
- TechCrunch 2026-07-14(FINRA 框架 X 长文):https://techcrunch.com/2026/07/14/deepmind-ceo-calls-for-an-independent-standards-body-to-regulate-frontier-ai/
- TechCrunch 2026-06-20(Jumper 离职转投 Anthropic):https://techcrunch.com/2026/06/20/nobel-laureate-john-jumper-is-leaving-deepmind-for-rival-anthropic/
- TechCrunch 2026-06-22(DeepMind+A24 $75M 合作):https://techcrunch.com/2026/06/22/google-deepmind-bets-75m-on-ais-future-in-hollywood-with-a24-deal/
- BBC 2017(CBE):https://www.bbc.com/news/technology-42511365
- Wired 2016(AlphaGo 背后):https://www.wired.com/2016/05/google-alpha-go-ai/
- Ars Technica(Genie 3 / Project Genie / Weather Lab / Lyria 3 等窗口内报道)
- FT / Axios / CNBC / The Verge / Fortune / Semafor / The Atlantic / Reuters / qz / Sherwood / Stanford Daily / Business Insider 等(窗口内声明转述,见 §5)

**L2 一般(交叉验证用)**
- Wikipedia: Demis Hassabis / Google DeepMind / AlphaFold / AlphaGo / Isomorphic Labs / Gemini (language model)
- Wikiquote: Demis Hassabis

---

## 九、信源限制与存疑说明

1. **检索通道受限(关键)**:本环境 Tavily MCP 套餐额度中途耗尽(search/extract/research 均报 "exceeds your plan's set usage limit"),内置 WebSearch 不可用。后期 agent 改用 curl 直抓已知 URL + Wikipedia API(干净 wikitext/extract)+ Google News RSS 兜底。nobelprize.org、deepmind.google 博客等重 JS/SPA 站点正文未能一手渲染(仅得骨架/404/406),相应事实经 Wikipedia 对原始新闻稿的引用交叉确认,非直接读取官网正文。
2. **X/Twitter 反爬**:@demishassabis 原推未能直采(curl 仅返回 JS 外壳,Nitter 2026 已失效)。2026-07-14 FINRA 框架长文经 TechCrunch 明确引述命名确证(可信度较高);其余产品/悼念类推文的存在系由官方博客交叉发布与新闻转载推断,未逐条核对原推文字。
3. **事实订正**:象棋年龄(13 岁非 8 岁)、Black & White(原作非续作)、封爵日期(2024-03-28 非新年荣誉)均经一手/多源订正,见 §0。
4. **未一手确证的技术成就**:WaveNet(2016)、AlphaGo Zero/AlphaZero(2017)、MuZero(2019)、AlphaGeometry/AlphaProof(2024)、AlphaProteo 为广为人知成就,本次未逐项取到 L0/L1 一手正文。
5. **收购条款**:"DeepMind 技术不直接用于军事/武器"条款广泛见诸二手媒体,但英文维基未明确陈述,未取到 L0/L1 一手出处,作"广泛报道、未一手确证"。收购金额各源不一(£400M vs $400–650M)。
6. **Isomorphic 融资**:约 $600M 首轮(2025-04)仅见维基(L2),未取到官方确认;与 2026-05 $2.1B Series B 的轮次区分系推断。
7. **Google DeepMind 2023-04 合并公告** Google 官方博客原文(L0)未能取回(404/Wayback 无快照),合并细节暂以维基(L2)为据。
8. **治理角色细节**:Demis 在英国 AI Safety Institute 顾问、布莱切利园峰会、向政府建言的具体细节仅由维基"UK Government AI Adviser"一句话支撑(L2);DeepMind"Responsible Scaling"/Frontier Safety Framework 政策内容未从本轮信源确证。
9. **AGI 时间线早期端**:"从几十年到几年"的最早源头表述(早年具体措辞与年份)未在一手抓取中定位,演进方向由 2025-07"50% by 2030"确证,早期端为推测性回溯。
10. **播客访谈缺口**:All-In Podcast(2025-09-12)全文 transcript 未取到;Google DeepMind 12/16 播客仅有 podwise 章节级转述(L2);Fortune 2026-02-11 与部分 I/O 2026 报道正文付费墙/反爬未取全,部分主题据标题+L1 报道归纳。No Priors / Hard Fork / 20VC / Stratechery 等线索未逐一核实。
11. **窗口边缘**:Lex Fridman #475(约 2025-07-23)早于窗口起点 07-27 仅 3-4 天,严格不计入"近 360 天访谈清单",但其 transcript 为思想演进维度(全期)的重要一手依据,已用于 §3。
12. **日期精度**:Gemini Robotics 1.5(约 2025-09)、ER-1.6(约 2026-04)、Isomorphic Drug Design Engine(约 2026-02)、Google Pics(约 2026-05)仅有月份或约数;Time 2025 年度人物精确宣布日期未确证(约 2025-12)。

---

*整理方法:6 个子 agent 并行调研(背景生平与学术成就 / 商业社会工程与机构演进 / 思想演进 / 近 360 天播客访谈 / 近 360 天社交媒体 / 近 360 天事件时间轴),经 Tavily MCP 检索 + curl 直抓 + Wikipedia API 兜底(Tavily 套餐中途耗尽),结构化返回后由主 agent 一次性整合成文。耗时约 22 分钟(sonnet+medium 全 6 维度),下次同类任务按 5-8 分钟可实施优化版配置。*
