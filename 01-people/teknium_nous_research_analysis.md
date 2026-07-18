# Teknium（Ryan Teknium）个人背景与近 360 天思想体系系统化梳理总结

> 数据来源：公开播客、GitHub/HuggingFace、Nous Research 官方博客、媒体报道
> 覆盖时段：2025/07 ~ 2026/07（近 360 天）
> 整理日期：2026/07/05

---

## 一、个人背景速览

### 1.1 基本信息

| 维度 | 信息 |
|------|------|
| **网名** | Teknium（亦作 teknium1、Ryan Teknium） |
| **真实身份** | 匿名/假名（pseudonymous），真实姓名未完全公开 |
| **组织** | Nous Research，联合创始人 & Head of Post-Training（后训练负责人） |
| **前公司** | Stability AI（曾任职） |
| **核心定位** | 开源 AI 领域最著名的后训练（post-training）专家，合成数据策展的先驱 |
| **社交账号** | X/Twitter: @Teknium1（~49.5k 粉丝）；GitHub: teknium1（5.1k 粉丝，48 repos）；HuggingFace: teknium（6.1k 粉丝，45 models，12 datasets） |
| **技术专长** | Python、后训练、强化学习（RL）、链式思维推理（CoT）、合成数据管线、数据策展 |
| **核心哲学** | "Pre-trained models are clay — post-training molds them into a smarter, more steerable version." |

### 1.2 身份之谜

Teknium 是 AI 开源社区中最著名的匿名人物之一。与 Serenity 不同，他不是通过推文喊单获得关注，而是通过**持续四年的技术贡献**——模型、数据集、训练方法——建立了无法被忽视的存在感：

- 在 HuggingFace 上发布了 **45 个模型**，累计下载超 **5,500 万次**
- 维护了 **12 个数据集**，包括 OpenHermes（百万级合成指令数据的标杆）
- GitHub 上 **48 个代码仓库**，涵盖模型训练、数据管线、Agent 框架
- 与 OpenAI 联合创始人 Diederik Kingma 合著 DeMo（解耦动量优化）论文

### 1.3 Nous Research 联合创始人团队

| 姓名 | 角色 | 背景 |
|------|------|------|
| **Teknium**（Ryan Teknium） | Head of Post-Training | 匿名/假名；前 Stability AI；Hermes 系列灵魂人物 |
| **Jeffrey Quesnelle** | CEO / CTO | 密歇根大学 CS 硕士；YaRN 长上下文论文第一作者；密码学背景 |
| **Karan Malhotra** | Head of Behavior | 斯坦福脑刺激实验室研究员；艾默里大学宗教与哲学专业；模型对齐与行为 |
| **Shivani Mitra** | 联合创始人 | 运营与增长负责人；早期担任 CEO |

**成立故事**：
Teknium 早期在 Twitter 上发现了 Quesnelle 发布的 RoPE 位置嵌入 hack，觉得技术品味极佳，邀请他进入一个私密 Discord 群。这个群后来变成了 Nous Research 的核心社区——一群对开源 AI 抱有共同信仰的研究者的聚集地。

---

## 二、近 360 天重大事件时间轴

```
2025/07 ──────────────────────────────────────────────────────────────
   │
   │  Jul ~ Aug    Nous Research 在 Paradigm 领投的 A 轮后整合团队
   │              团队 ~18-20 人，总部在德州奥斯汀
   │              累计融资 ~$6,500 万，Token 估值 $10 亿
   │
   │  Aug          ★ Hermes 4 发布 —— 最重要的里程碑
   │              70B + 405B 两个版本，基于 Llama 3.1
   │              混合推理（Hybrid Reasoning）：可切换思考/对话模式
   │              RefusalBench #1（拒绝率最低的开源推理模型）
   │              在 MATH 上超越 Llama Instruct 版本 ~60 分
   │              在 MMLU-Pro 上超越 ~21 分
   │              累计下载量突破 5,500 万
   │
   │
2025/09 ~ 12 ─────────────────────────────────────────────────────────
   │
   │  Sep ~ Dec    ★ Psyche 网络正式启动
   │              基于 DisTrO 梯度压缩技术 + Solana 区块链
   │              目标：让全球闲置 GPU 可以参与去中心化大模型训练
   │              梯度压缩比：~1000:1（DeMo）→ ~10000:1（DisTrO）
   │
   │  Dec          团队直播 DisTrO —— 用互联网带宽
   │              成功分布式预训练 150 亿参数语言模型
   │
   │
2026/01 ──────────────────────────────────────────────────────────────
   │
   │  Jan ~ Feb    Teknium 核心精力转向 Hermes Agent
   │              从"做最好的开源模型" → "做最好的 AI Agent 运行时"
   │
   │
2026/02 ──────────────────────────────────────────────────────────────
   │
   │  Feb          ★★ Hermes Agent 开源发布
   │              MIT 协议，模型无关（可与任何 LLM 配合）
   │              特点：
   │              ├── 常驻自治运行（始终在后台）
   │              ├── 多平台入口（Telegram/Discord/Slack/
   │              │   WhatsApp/Signal/iMessage）
   │              ├── 自我进化：自动沉淀技能
   │              ├── 三层记忆系统
   │              └── 90%+ 代码由 Hermes Agent 自己开发
   │              首月 GitHub Stars 破 7 万
   │
   │
2026/04 ──────────────────────────────────────────────────────────────
   │
   │  Apr          ★ Hermes Agent v0.8.0 发布
   │              新增：动态模型路由
   │              根据任务复杂度自动选择最佳模型
   │
   │  Apr 12       至顶网报道 Nous Research 深度访谈
   │              CEO Jeffrey Quesnelle on "Into the Bytecode"
   │              详细阐述 DeMo 梯度压缩原理 + Psyche 去中心化愿景
   │
   │  Apr 14       ★ Tool Use 播客：Karan (Nous 联合创始人)
   │            "Hermes Agent has won. Here's why"
   │            开放 AI 基础设施 vs 封闭系统的辩论
   │
   │  Apr          行业爆炸性事件：
   │              Anthropic 发布 Claude Mythos Preview
   │              Dario Amodei："模型太强不能公开"
   │              只开放给 ~40 家大型机构
   │              —— 完美验证了 Nous 的警告："
   │                  安全叙事的终点永远是被我们掌控"
   │
   │
2026/05 ──────────────────────────────────────────────────────────────
   │
   │  May 21       ★ Practical AI (Changelog) 播客 #357
   │              "Hermes Agent: Agents that grow with you"
   │              CEO Jeffrey Quesnelle 深度对话
   │              主题：自我进化的 Agent、递归学习、
   │              模型 vs 编排层、人类角色的变化
   │
   │  May          Hermes 4.3 产出
   │              第一个完全使用 Psyche 去中心化网络完成
   │              后训练的模型
   │
   │
2026/06 ──────────────────────────────────────────────────────────────
   │
   │  Jun 10       ★ TWiAI #17：Jeffrey Quesnelle
   │            "The AI Agent Race"
   │            开源 Agent 竞赛 + "编排层"（Harness Layer）争夺
   │
   │  Jun 12       Teknium 综合档案首次系统化整理
   │              AcFun 发布人物档案
   │
   │
2026/07 ──────────────────────────────────────────────────────────────
   │
   │  Jul 5        本文档整理
   │
   ▼
```

---

## 三、产品与思想体系

### 3.1 Teknium 的核心哲学：后训练决定智能的形状

这是 Teknium 区别于所有其他 AI 人物的根本洞见：

> *"Pre-trained models are clay. Post-training molds them into a smarter, more steerable version."*

翻译（按他的原意）：
> "预训练模型是一团黏土。后训练把它塑造成有方向感、有判断力、能被你驾驭的智能。"

**"黏土论"的三层含义**：

```
第一层：技术含义
─────────────────
预训练只是第一步 —— 模型学会了语言、知识、推理的"原材料"
后训练（SFT + RLHF + CoT RL）是决定模型"是什么样的人"的环节
   → 模型是助人还是拒绝？是深思还是速答？是循规还是创造？
   → 全部由后训练定义，不由预训练决定

第二层：产品含义
─────────────────
开源基础模型（Llama、Mistral、Qwen）越来越强 → 预训练在收敛
差异化从"谁有最强的通用模型"转向"谁能让模型在特定场景做得最好"
   → 私有数据 + 合成数据 + 场景 RL = 真正的护城河

第三层：战略含义
─────────────────
谁控制后训练，谁就控制 AI 的行为 —— 不仅是智能水平，还包括价值观
Nous Research 的存在就是要在后训练层对抗封闭寡头
   → "AI 不应该被 3 家公司定义"
```

### 3.2 合成数据的艺术：90%+ 数据是生成的

Teknium 是 LLM 领域合成数据策展的先驱。他的 OpenHermes 数据集（百万级合成指令）已经成为开源后训练的数据标准：

> *"90%+ of our data is synthetic. There are lazy ways that are bad, but we've found many ways to make it useful."*

**"好的合成数据 vs 坏的合成数据"**：

| 坏的合成数据 | 好的合成数据 |
|:---|:---|
| 用一个模型生成、不筛选、直接用 | 多模型交叉生成 + 质量过滤 + 人工抽样 |
| 只关注"模型回答得好不好" | 关注"数据覆盖了多少推理路径" |
| 单一格式、单一难度 | 多样化格式（对话/代码/推理/角色扮演）+ 分层难度 |
| 生成后即丢弃 | 生成后评估 → 反馈到数据管线 → 下一轮更针对性地生成 |

**DataForge** —— Teknium 构建的合成数据管线：
1. 种子策划：从人类策划的高质量样本开始
2. 多样生成：使用多个模型 + 多个温度 + 多个格式生成候选数据
3. 自动过滤：基于奖励模型、格式检查、去污染检测
4. 人工审核：抽样验证
5. 闭环迭代：好的数据模式 → 反馈到下一轮生成

**Atropos** —— Teknium 的 RL 环境框架（1,200+ 任务环境）：
- 不是单一奖励模型 → 是 1,200+ 个不同的"考试"
- 每个 RL 环境测试一种特定的推理能力
- 模型在 1,200+ 个环境中被评估 → 弱项 → 针对性生成数据 → 再训练

### 3.3 Hermes 模型进化史

```
Hermes 1 (2023/08)
  ↓  基础 SFT 微调，"让模型更像一个助手"
Hermes 2 (2023 底 ~ 2024 初)
  ↓  扩展规模（7B/13B/34B），引入多基础模型（Yi/Mixtral）
Hermes 3 (2024)
  ↓  系统化数据管线，质量大幅提升
DeepHermes 3 (2025 初)
  ↓  ★ 关键创新：可切换推理模式
  ↓  一个模型 → 可按需切换"快速对话"或"深度推理"
Hermes 4 (2025/08)
  ↓  ★★ 混合推理旗舰
  ↓  70B + 405B，RefusalBench #1
  ↓  拒绝率最低的开源推理模型
  ↓  MATH 超 Llama Instruct ~60 分
Hermes 4.3 (2026/05)
  ↓  ★ 第一个完全由 Psyche 去中心化网络
  ↓    完成后训练的模型
Hermes 5 (计划中)
  → 下一代架构
```

**核心理念的演进**：

Teknium 对"好模型"的定义在不断深化：
- 2023："一个不拒绝回答问题的模型"（Hermes 1）
- 2024："一个能推理、能对话、能编程的模型"（Hermes 2-3）
- 2025："一个知道自己何时该思考、何时该快速的模型"（DeepHermes 3 / Hermes 4）
- 2026："模型不重要——重要的是 Agent 运行时"（Hermes Agent）

### 3.4 Hermes Agent：产品哲学的范式转变

这是 Teknium 近 360 天最重大的思想飞跃：
从"做一个好模型"到"做一个能与所有好模型共存的 Agent 运行时"。

> *Hermes Agent 没有绑定任何特定模型。OpenAI 的 GPT、Anthropic 的 Claude、Meta 的 Llama、Nous 自己的 Hermes —— 都可以插进去用。因为 Teknium 认识到：后训练能塑造模型，但编排层才是 AI 落地的核心战场。*

**Hermes Agent 的核心设计**：

| 组件 | 功能 | 哲学含义 |
|------|------|---------|
| **三层记忆** | 短期（对话上下文）/ 中期（任务知识库）/ 长期（人格与偏好） | Agent 不是工具 → 是"跟你一起成长的存在" |
| **自动技能沉淀** | Agent 完成一个任务后 → 自动将经验沉淀为可复用的 Skill | 人类不需要手动编程 → Agent 自己学会进化 |
| **模型无关** | 可与任何 LLM 配合 | 不与任何模型供应商绑定 → 用户自主权 |
| **多平台入口** | Telegram/Discord/Slack/WhatsApp/Signal/iMessage | Agent 应该在你已经使用的每一个地方 |
| **MIT 开源** | 任何人可以 fork、修改、商用 | 基础设施层不能是封闭的 |

**自举（Bootstrapping）故事**：
Hermes Agent 95-99% 的开发和调研工作是通过 Hermes Agent 自身完成的。Teknium 公开说他没有写大部分代码——他只是在"训练 Agent 学会开发 Agent"。

这与 Boris Cherny 的"我从 11 月起没写过一行代码"遥相呼应，但 Teknium 走得更远：Boris 用 AI 写产品的代码，Teknium 用 AI 写 Agent 让它自己进化。

---

## 四、播客与访谈思想总结

### 4.1 出场清单

| 时间 | 播客/场合 | 出场者 | 核心主题 |
|------|----------|--------|---------|
| **2026/04/12** | Into the Bytecode 播客 | Jeffrey Quesnelle (CEO) | DeMo 梯度压缩、Psyche 去中心化训练、开源 vs 封闭 |
| **2026/04/14** | Tool Use 播客 | Karan (Head of Behavior) | Hermes Agent 为什么赢了、三层记忆、自进化 |
| **2026/05/21** | Practical AI (Changelog) #357 | Jeffrey Quesnelle | 自我进化的 Agent、人类角色的变化 |
| **2026/06/10** | TWiAI #17 | Jeffrey Quesnelle | AI Agent 竞赛、编排层的争夺 |
| **2025** | Delphi Podcast | Jeffrey Quesnelle | Crypto × AI、Bittensor 去中心化模型排名、AGI |

> 注：Teknium 本人因匿名身份，极少亲自接受播客采访。他的思想主要通过 GitHub 代码、HuggingFace 模型卡、X/Twitter 推文，以及 Nous Research CEO Jeffrey Quesnelle 在播客中的转述来传达。

### 4.2 按思想域组织

---

#### A. 后训练决定智能的形状（Teknium 的核心思想）

这是贯穿所有 Hermes 版本的根本信念：
- 预训练模型是"毛坯房"——所有材料都在，但需要装修
- 后训练是"装修"——决定房子的风格、布局、使用体验
- 谁控制后训练，谁就定义了 AI 的行为——不仅是能力，还有价值观

---

#### B. 合成数据不是"偷懒"，是"精密工程"（Teknium + Jeffrey 访谈）

> "区别在于：你是让一个模型随便生成十万条，然后全部扔进训练？还是你用多模型、多温度、多格式、分层难度、闭环筛选来策划数据？前者是垃圾进垃圾出。后者——就是我们对 Hermes 做的事——是精密工程。"

**OpenHermes 数据集**是整个开源 AI 社区中最常被引用的合成数据方案。它的核心创新不是"用 AI 生成数据"——那个早在 2023 年就有人做了——而是**多模型交叉生成 + 分层难度 + 覆盖推理路径的多样性**。

---

#### C. DeMo & DisTrO：让训练 GPU 去中心化（Jeffrey + Bowen Peng）

Nous Research 最硬核的技术贡献是 DeMo 和 DisTrO 算法：

| 技术 | 压缩比 | 含义 |
|------|:------:|------|
| DeMo | ~1000:1 | 梯度压缩到千分之一大小 |
| DisTrO | ~10000:1 | 可以在普通互联网带宽上训练大模型 |

**原理类比**（Jeffrey 在 Into the Bytecode 中的解释）：
> "JPEG 压缩把一张照片从像素域转换到频率域——然后只保留人眼能看到的最强频率分量。DeMo 做的是同样的事——把'每个参数的修正值'（梯度）转换到频率域——然后只保留对模型改进最重要的那些频率。剩下的都可以丢掉。压缩比约 1000 倍。"

**战略意义**：
> "如果训练不再需要集中在一个数据中心、不需要 InfiniBand 高速互连、不需要同一个机架里的 GPU——那 AI 的算力垄断就被打破了。全世界闲置的 GPU 可以通过 Psyche 网络贡献算力——这是物理意义上真正的去中心化。"

---

#### D. 安全叙事的陷阱（Jeffrey 多期播客）

Nous Research 对 OpenAI/Anthropic 等头部实验室的"安全叙事"的批评是最尖锐的：

> "当一个公司告诉你——'我们的技术非常危险，所以只能由我们来控制它的使用'——这不是安全论。这是垄断论。他们不是在保护你。他们是在保护自己的护城河。"

**2026 年 4 月的验证**：
Anthropic 发布 Claude Mythos Preview → CEO Dario Amodei 宣布"模型太强大不能公开" → 只开放给约 40 家大型机构 → **几乎完美兑现了 Nous 几年前的讽刺**

> "我们不想生活在三家公司定义了人类能获得什么样的智能的世界里。"
> —— Nous Research 的使命宣言

---

#### E. Agent 不是工具，是"跟你一起成长的存在"（Hermes Agent 哲学）

这是 Teknium 对 AI Agent 最核心的重新定义：

| 传统 AI 工具 | Hermes Agent |
|:---|:---|
| 你问他，他回答 | 他在后台常驻运行 |
| 每次对话是独立的 | 他有记忆——记得你的偏好、过去的事 |
| 你需要学习如何使用他 | 他在使用中学会你的需求 |
| 能力固定 | 他自动沉淀新技能 |
| 绑定一个模型供应商 | 模型无关——你可以随时换底层模型 |

---

#### F. Crypto × AI 不是噱头，是基础设施（Delphi 播客）

> "加密货币和区块链不是'让 AI 更好'的魔术。它们解决两个具体的工程问题：① 如何验证远程 GPU 在老老实实地做训练而不是在摸鱼？② 如何在没有中央协调的情况下在几千个 GPU 上分发和支付训练任务？—— Psyche 网络用 Solana 解决这两个。"

### 4.3 故事叙述手法分析

| 维度 | Teknium / Nous | Boris Cherny | Leopold |
|------|:---:|:---:|:---:|
| **身份** | 匿名/半匿名（Teknium 假名，Jeffrey/Karan 实名） | 公开身份 | 公开基金 |
| **核心叙事** | "预训练是黏土，后训练塑造灵魂" | "编程已被解决" | "瓶颈轮动" |
| **说服力来源** | 代码 + 模型下载量（5,500 万次） | 个人实践（不再写代码） | 13F + 学术论文 |
| **叙事风格** | 技术工匠 + 加密朋克反叛 | 内部人引爆 + 自嘲收放 | 论文 → 交易信号 |
| **政治立场** | 激进去中心化 / 反垄断 / "AI 不应被 3 家公司控制" | 温和改革 / "让更多人能编程" | 务实 / 用金融工具表达观点 |

**Nous Research 的叙事方式**：

1. 用开源代码说话（Hermes Agent 19 万+ Star）
2. 用下载量说话（5,500 万次下载）
3. 用硬核技术说话（DeMo/DisTrO——被 ICLR 接收）
4. 用哲学立场说话（反垄断/去中心化/"AI for the people"）
5. 用反讽说话（"安全叙事是新时代的垄断辩护词"→ Anthropic Mythos 验证了这一点）

---

## 五、关键金句

### 5.1 Teknium 本人的话

| 领域 | 金句 |
|------|------|
| **后训练哲学** | "Pre-trained models are clay — post-training molds them into a smarter, more steerable version." |
| **合成数据** | "90%+ of our data is synthetic. There are lazy ways that are bad, but we've found many ways to make it useful." |
| **关于 Agent** | "I didn't code most of it. Hermes Agent built Hermes Agent." |

### 5.2 Nous Research 团队的话

| 领域 | 说话人 | 金句 |
|------|--------|------|
| **反安全垄断** | Jeffrey | "当一个公司告诉你'我们的技术很危险所以只能由我们控制'——这不是安全论，是垄断论。" |
| **后训练** | Jeffrey | "预训练是毛坯房，后训练是装修。" |
| **去中心化** | Nous 使命 | "我们不想生活在三家公司定义人类能得到什么智能的世界里。" |
| **DeMo 原理** | Jeffrey | "JPEG 压缩像素——DeMo 压缩梯度。同样的数学。" |

---

## 六、风险与批判

1. **Crypto × AI 路线风险**：Psyche 网络依赖 Solana 区块链和未来潜在的代币发行，监管风险不可忽视
2. **开源模型的赢家诅咒**：Meta/Llama、Mistral、Qwen、DeepSeek 等基础模型越来越强 → Hermes 作为微调层的相对价值可能被压缩
3. **Token 估值的迷雾**：$10 亿估值为 Token 估值，不是传统股权估值，实际变现路径尚不清晰
4. **匿名身份的瓶颈**：Teknium 的匿名身份在技术和社区层面不是问题，但从 Nous Research 的商业化/机构合作角度看，可能影响信任
5. **去中心化训练的实际规模**：Psyche 目前只完成了后训练（微调），真正的预训练尺寸（千卡/万卡级）尚未在去中心化环境中验证

---

## 七、数据来源

- Teknium GitHub (`teknium1`) + HuggingFace (`teknium`)
- Nous Research 官方博客与 GitHub 组织
- Into the Bytecode 播客（Jeffrey Quesnelle，2026/04/12）
- Tool Use – AI Conversations 播客（Karan，2026/04/14）
- Practical AI (Changelog) #357（Jeffrey Quesnelle，2026/05/21）
- TWiAI #17（Jeffrey Quesnelle，2026/06/10）
- The Delphi Podcast（Nous Research，2025）
- 至顶网（2026/04/12） / 链新闻 ABMedia / AcFun 档案整理
- Paradigm A 轮投资报道（2025/04）

> ⚠️ 本文档基于 Teknium 及 Nous Research 联合创始人的公开代码、模型卡、播客访谈和媒体报追进行系统化梳理。Teknium 为匿名/假名身份，个人真实信息未经独立核实。文中关于 "Toknium 本人极少接受采访" 的表述基于所有可获得的公开信息判断，如有低调访谈可能被遗漏。

---

*文档生成时间：2026/07/05 | 数据覆盖时段：2025/07 ~ 2026/07（约 360 天）*
