# Peter Steinberger (@steipete) 深度研究报告

> 调研日期：2026-07-06 | 方法：3 并行子 Agent + 交叉验证 + 系统化合成
> 覆盖范围：2025年7月 — 2026年7月（360 天）

---

## 目录

1. [人物速写](#1-人物速写)
2. [职业轨迹全景](#2-职业轨迹全景)
3. [360 天重大事件时间轴](#3-360-天重大事件时间轴)
4. [思想演进图谱](#4-思想演进图谱)
5. [核心哲学体系](#5-核心哲学体系)
6. [产品矩阵与架构理念](#6-产品矩阵与架构理念)
7. [媒体足迹全记录](#7-媒体足迹全记录)
8. [关键叙事线索](#8-关键叙事线索)
9. [附录：信息源清单](#9-附录信息源清单)

---

## 1. 人物速写

| 维度 | 信息 |
|------|------|
| **全名** | Peter Steinberger |
| **出生** | 1986 年 5 月 22 日，奥地利 |
| **网络 ID** | @steipete (GitHub / X / npm) |
| **教育** | HTL Braunau → 维也纳工业大学 (TU Wien)，医学计算机科学 |
| **当前角色** | OpenAI Codex 团队，负责下一代个人 AI Agent |
| **居住地** | 旧金山 / 维也纳双城 |
| **前公司** | PSPDFKit 创始人 & CEO → Amantus Machina 创始人 → OpenAI |
| **代表作** | PSPDFKit（PDF SDK，~€100M 退出）、OpenClaw（GitHub 史上增长最快的开源项目，37万+ stars） |

---

## 2. 职业轨迹全景

```
1986              出生，奥地利上奥州农村
2004-2010         维也纳工业大学，医学计算机科学
2009-2011         自由职业 iOS 开发者 → Scribd 高级 iOS 工程师
                   ↳ H1-B 签证延迟 9 个月 → 空窗期写出 PSPDFKit 雏形
2011              PSPDFKit 成立，零融资自举
2011-2021         PSPDFKit 黄金十年：60-70 人团队，近 10 亿终端用户
                  客户：Apple、Dropbox、DocuSign、SAP、IBM、Volkswagen
2021.10           Insight Partners €1 亿+ 战略投资（实为多数股权收购）
2021-2024         🔥 重度 burnout："三年几乎没碰电脑"
                  尝试治疗、死藤水、换国家、派对——均无效
2025.04           通过 AI 辅助编程重新发现编码乐趣
2025.05-06        创立 Amantus Machina（维也纳）
2025.06-11        疯狂建造期：~40-50 个 CLI 工具和 Side Project
2025.11 🔥        1 小时原型 → Clawdbot 发布 → 病毒式传播
2026.01           更名风波：Clawdbot → Moltbot → OpenClaw
2026.02 🔥        Sam Altman 宣布加入 OpenAI，OpenClaw 移交独立基金会
2026.03-06        全球演讲季：NVIDIA GTC → TED → Microsoft Build → AI Engineer World's Fair
2026.07-现在      OpenAI Codex 团队，打造"连我妈都能用的 Agent"
```

---

## 3. 360 天重大事件时间轴

### 第一阶段：博客时代（2025.07 — 2025.10）
*通过高产写作建立 AI 辅助开发领域的话语权*

| 日期 | 事件 | 意义 |
|------|------|------|
| 2025.06.25 | 博客 *"Slot Machines for Programmers"* | 首次以第一人称 AI 视角讨论 AI 辅助开发 |
| 2025.08.05 | 博客 *"Poltergeist"* | 发布自动 watch-and-rebuild 工具 |
| 2025.08.19 | 博客 *"Just One More Prompt"* | 🔑 坦诚 AI 编码成瘾，自嘲"Claudoholic" |
| 2025.08.21 | 博客 *"Essential Reading for Agentic Engineers"* | Agentic Engineering 框架雏形 |
| 2025.08.25 | 博客 *"My Current AI Dev Workflow"* | 揭示"5-10 个 Agent 并行运行"的工作流 |
| 2025.08-09 | Claude Code Anonymous 系列 Meetup | 柏林、维也纳、伦敦、布拉格组织线下聚会 |
| 2025.09.17-19 | NSSpain 演讲 | "You Can Just Do Things: How AI Is Transforming Software Development" |
| 2025.10.14 | 博客 *"Just Talk To It — the no-bs Way of Agentic Engineering"* | 🔑 方法论奠基之作 |
| 2025.10.06-07 | Swift Connection 巴黎 | 同一主题演讲，开始形成标准化 keynote |
| 2025.10.23 | Acquired × Sentry 私人活动 | 进入硅谷核心圈子 |
| 2025.10.30-31 | #PragmaConf (博洛尼亚) | 欧洲开发者社区演讲 |

**阶段累计：~38 篇博客 + 8 场线下聚会/演讲**

### 第二阶段：OpenClaw 诞生与病毒爆发（2025.11 — 2026.01）

| 日期 | 事件 | 数据 / 影响 |
|------|------|------|
| ⭐ 2025.11 | **1 小时原型诞生**：WhatsApp ↔ Claude Code CLI | 最简可行的 Agent 桥接 |
| 2025.11 | Clawdbot 正式发布 | 24 小时内 9,000 stars |
| 2025.12.18 | 博客 *"Just Talk To It"* 扩展版 | Agentic Engineering 实践指南 |
| 2025.12.19 | **tokentally** npm 发布 (v0.1.0) | LLM token 成本估算库 |
| 2025.12.28 | 博客 *"Shipping at Inference-Speed"* | 🔑 "我不再读代码了"宣言 |
| ⭐ 2026.01 | Anthropic 商标警告："Clawdbot" 太接近 "Claude" | 触发更名风波 |
| 2026.01 | 更名：Clawdbot → Moltbot → OpenClaw（最终） | 加密货币骗子在 10 秒窗口内抢注 $CLAWD 代币，拉升至 $16M 市值 |
| 2026.01.14 | **CASE Conference** (柏林) | 首个 Agentic SE 学术会议演讲 |
| 2026.01.23 | GitHub Open Source Friday | 官方邀请，项目破 10 万 stars |
| ⭐ 2026.01.28 | **The Pragmatic Engineer 播客** (Gergely Orosz, 114 分钟) | "I ship code I don't read" 正式出圈 |
| 2026.01 | Moltbook 上线 | 26 万+ AI bots 在自主社交网络中互动 |

**阶段累计：从 0 到 GitHub 史上增长最快项目**

### 第三阶段：人才争夺战与加入 OpenAI（2026.02）

| 日期 | 事件 | 关键细节 |
|------|------|------|
| ⭐ 2026.02.07 | **Y Combinator 专访** | 🔑 "AGI is a trap. We need specialized intelligence." |
| 2026.02.10 | "Hail the Crustacean Revolution" | 维也纳 OpenClaw 社区 Meetup |
| ⭐ 2026.02.12 | **Lex Fridman #491** (3h14m) | 🔑 最完整的深度访谈，覆盖起源→哲学→未来 |
| ⭐ 2026.02.15 | **Sam Altman 宣布加入 OpenAI** | 三方争夺：Meta (Zuckerberg) vs OpenAI (Altman) vs xAI |
| 2026.02.16 | Changelog News #181 | "All the Claw Things" 专题 |
| 2026.02.23 | ORF 奥地利国家电视台 *Zeit im Bild* | 数据隐私和 prompt injection 讨论 |
| ⭐ 2026.02.25 | **OpenAI Builders Unscripted #1** (Romain Huet) | "Vibe coding is a slur" — AI 开发是一种真正的技能 |
| 2026.02 | Andreas Klinger *Europe's Most Ambitious Startups* | 20 分钟，OpenClaw 社区 meetup 后拍摄 |
| 2026.02.26 | TechCrunch 深度报道 | "Playful and allow yourself time to improve" |
| 2026.02 | **MIT Technology Review** | "Is a Secure AI Assistant Possible?" |

**阶段关键决定：OpenClaw 保持开源（基金会）+ OpenAI 继续支持**

### 第四阶段：全球演讲季（2026.03 — 2026.07）

| 日期 | 活动 | 主题 |
|------|------|------|
| 2026.03.01 | Imperial College London 开幕演讲 | AI Agent 学术视角 |
| 2026.03.06 | 伦敦 OpenClaw × OpenAI × Sequoia Meetup | 三巨头联合社区活动 |
| 2026.03.16 | **NVIDIA GTC Live Pregame** (San Jose) | Jensen Huang 称 OpenClaw 为 "the new computer" |
| 2026.03.26 | **Bloomberg 采访** | 🔑 中-美 AI "温差"：不准用 vs 不敢不用 |
| 2026.04.08-10 | **AI Engineer Europe** (伦敦) | "State of the Claw" |
| ⭐ 2026.04.13-17 | **TED2026** (温哥华) | 🔑 "The lobster is loose and it's not going back into the tank." |
| 2026.04 | Business Insider 专题 | "The moment AI changed everything" |
| 2026.05.06 | OMR Festival (汉堡) | — |
| 2026.05.19 | Telefónica + Inditex 内部演讲 | 企业 AI Agent 部署 |
| 2026.06.02-03 | **Microsoft Build** (旧金山) | "Build the Thing That Builds the Thing" |
| 2026.06.03 | OpenClaw After Hours @ GitHub | Fireside Chat |
| 2026.06.04 | Snowflake Summit Dev Day | "The Future of Software in the Wake of OpenClaw" |
| 2026.06.09 | **Forge Summit 开幕 Keynote** | "Building the Dark Factory" |
| 2026.06.17-20 | **VivaTech** (巴黎) | "The Agentic Enterprise" |
| 2026.06.15 | Hg Software Leadership Gathering (卢塞恩) | 邀请制闭门 |
| 2026.06.18 | LVMH Forward Gala Fireside Chat | 奢侈品行业 AI 应用 |
| ⭐ 2026.06.30 | **AI Engineer World's Fair 开幕 Keynote** (SF) | "Software Factories" |
| 2026.07.01 | AI Engineer After Hours × Warp × Sequoia | "Crafting Software Factories" |
| 2026.07.25-26 | YC Startup School | 即将 |
| 2026.08.01-02 | Agentic AI Summit (Berkeley) | 即将 |

### 第五阶段：社交媒体关键动态

| 日期 | 内容 | 影响力 |
|------|------|------|
| 2026.01.27 | X："I will never do a coin." | 正面回应加密诈骗 |
| 2026.02.15 | X：宣布加入 OpenAI | 全行业震动 |
| 2026.06.13 | X：Codex 自主触发 PayPal 验证 | 277K+ 浏览 |
| 2026.06.15 | X：parody Mac Studio 截图 (512GB) | 315K+ 浏览 |
| 2026.06.22 | X：OpenClaw 非营利模式超 VC 竞品 | 广泛转发 |
| 2026.06.25 | X："半年前瓶颈是 token，加入 OpenAI 后瓶颈是注意力" | 金句 |

---

## 4. 思想演进图谱

```
                   2025 上半年              2025 下半年              2026 上半年
                   ─────────               ─────────               ─────────
                
开发者身份：    "我刚恢复编程"           "我同时跑 5-10 个 Agent"   "我是 Agent 编排者"
              
代码态度：      逐行读代码               "我不再读代码"              "代码不再有价值"
                                         "Shipping at              "可随时删除并重建"
                                         Inference-Speed"

AI 角色：       AI 是工具                AI 是协作者                 AI 是基础设施
                                                                    "Agent 是我的手脚"

技术哲学：      传统工程                  "Just Talk To It"          "Software Factories"
                                         Agentic Engineering        "Dark Factory"

产业信念：      ———                     "AGI 是陷阱"                "80% 的 App 会消失"
                                         Specialized Intelligence   Expert Swarms

设计原则：      人类优先                  Agent 优先                  CLI > MCP
                                         "代码库为 AI 导航设计"       Unix 哲学即 Agent 哲学

商业模式：      PSPDFKit 经验            自掏腰包                    OpenAI 平台的
               Bootstrapping              $10-20K/month API费         独立基金会
```

### 四个核心转折点

1. **2025.04 重新编码**：AI 让编码"再次变好玩"，从 burnout 中恢复
2. **2025.11 Marrakech 时刻**：语音消息被 Agent 自主理解/处理/回复——未经编程。*"I had what I can only describe as a 'holy shit' moment."*
3. **2026.02 加入 OpenAI**：放弃 Meta/xAI 更高报价，选择"最大影响力"
4. **2026.06 Software Factories 演讲**：从"个人 Agent"到"软件工厂"——工业级 Agent 生产范式

---

## 5. 核心哲学体系

### 5.1 Agentic Engineering vs. Vibe Coding

| Vibe Coding（一个 Stigma） | Agentic Engineering（真正的技能） |
|---|---|
| "随便糊代码，跑就行" | 对 AI Agent 的目标设定、边界控制、结果验证 |
| 被嘲讽为"不会写代码" | 被重新定义为"学习吉他一样需要练习的技能" |
| 一次性 prompt 乱试 | 迭代式对话 + 故意 underspec + 逐步细化 |

> *"Vibe coding is a slur. They try AI, but they don't understand that it's a skill."*
> — OpenAI Builders Unscripted, Feb 2026

> *"Learning AI is like learning guitar. You're not going to be good at it on the first day."*

### 5.2 Specialized Intelligence > AGI

| AGI / Superintelligence | Steinberger 的 Specialized Intelligence |
|---|---|
| 一个无所不能的神级 AI | 成千上万个高度专业化的"专家蜂群" (Expert Swarms) |
| "上帝视角" | "iPhone 不是一个人造的" — 文明靠分工 |
| "AGI 是虚构的东西" | 每个 Agent 做一件事，做到极致 |

> *"AGI is a trap. We don't need a god-like intelligence. We need specialized intelligence."*
> — Y Combinator, Feb 2026

> *"What can one human being actually achieve? Do you think one human being could make an iPhone?"*

### 5.3 CLI > MCP

这是他最具争议也最具影响力的架构立场：

| MCP 协议 | CLI 方法 |
|---|---|
| 所有 tool schema 预加载 → ~44k tokens | `gh pr view --json` → ~1k tokens |
| 无管道组合能力 | `log-fetch \| grep ERROR \| feishu-send` |
| JSON-RPC 包围 | Unix 管道自然匹配 Agent 的推理链 |
| 需要 Server 进程、WebSocket | 零配置，直接 `exec()` |

他建造了 **mcporter** 来把 MCP Server 转回 CLI。他说：
> *"The only good thing about MCP was that it made companies open up some APIs."*

### 5.4 "Just Talk To It" 方法论

- **短 prompt**：1-2 句，约 50% 附带截图
- **并行 Agent**：3-8 个 codex CLI 实例同时运行（3×3 终端网格）
- **不用子 Agent**：认为 subagent 是营销噱头，更喜欢独立的终端窗口
- **不用复杂工作流**：贬斥 RAG、subagent、第三方编排器为"charade"
- **迭代式，非规范驱动**：与模型对话式讨论功能，故意 underspec，逐步迭代
- **直接到 main 分支**：无 feature branch、无 rollback、无 issue tracker

### 5.5 "Shipping at Inference-Speed" 范式

- "我不再读代码了"——角色从执行者转为系统架构师
- 瓶颈不再是打字速度，而是模型推理时间
- Codex 偏好：会默默读 10-15 分钟文件再写代码，一次性成功率更高
- CLI-first：一切从 CLI 开始，Agent 可以直接调用和验证
- Go 写 CLI：Agent 写 Go 写得很好
- "Oracle" 工具：让 Agent 在被卡住时咨询 GPT-5 Pro 深度推理
- 设计给 AI 看：代码库应为 AI Agent 导航而组织，不只为人

### 5.6 "Blast Radius" 思维

- 按影响范围分类变更：多枚小"炸弹" vs 一颗"Fat Man"
- 监控 Agent，随时按 Escape 中断："现在什么状态？"
- 自掏腰包每月 $10K-$20K API 费——对成本极度敏感

### 5.7 Play for Fun

> *"It's hard to compete with someone who's purely in it for fun."*
> — iFanr 专访标题，Feb 2026

这是他贯穿始终的信条。拒绝 VC 资金、拒绝数十亿收购（选影响力而不是价格）、拒绝把 OpenClaw 变成一个公司。最终选择 OpenAI 的理由是"改变世界，不是建立大公司"。

---

## 6. 产品矩阵与架构理念

### 6.1 OpenClaw 架构

```
┌──────────────────────────────────────────────┐
│                  GATEWAY                      │
│   WebSocket + HTTP (localhost:18789)          │
│   会话管理 · 认证 · 插件生命周期 · 通道路由      │
└──────┬──────────┬───────────┬────────────────┘
       │          │           │
  ┌────▼───┐ ┌───▼────┐ ┌───▼──────┐
  │Channels│ │Plugins │ │ Sessions │
  │12+ IM  │ │ClawHub │ │ 状态持久  │
  │平台连接 │ │ 560+   │ │ 多 Agent │
  └────────┘ └────────┘ └──────────┘
```

**核心理念：**
- **Hub-and-Spoke**：Gateway 是中央控制面，每个 Channel 是独立可插拔的 spoke
- **Local-first**：所有数据存本地 SQLite (`~/.openclaw/openclaw.db`)
- **Model-agnostic**：支持 OpenAI / Anthropic / Google / Ollama / OpenRouter / Mistral / Zhipu...
- **单用户系统**：明确 Owner scope（尽管支持多 Agent routing）
- **Markdown 驱动配置**：SOUL.md / HEARTBEAT.md / MEMORY.md

### 6.2 OpenClaw vs Claude Code vs Claude Cowork

| 维度 | OpenClaw | Claude Code | Claude Cowork |
|------|:--------:|:-----------:|:-------------:|
| **核心定位** | 个人 AI 编排平台 | 开发者编码助手 | 知识工作者文档助手 |
| **开源** | MIT | 闭源 | 闭源 |
| **模型** | 多厂商 | 仅 Claude | 仅 Claude |
| **交互通道** | WhatsApp/Telegram/Discord/Slack/Signal 等 12+ | 终端 | 桌面 App |
| **主动行为** | HEARTBEAT.md cron 调度 | 被动响应 | 被动响应 |
| **安装复杂度** | 30-60 min | 10-15 min | 最低 |
| **成本** | 免费 + API 费用 | $20-200/月 | 付费订阅 |
| **隐私** | 完全本地 | 数据到 Anthropic | 数据到 Anthropic |
| **电脑控制** | 视觉 GUI（截图） | 终端/文件直接访问 | Computer Use（预览） |
| **调度任务** | 内置 cron | `/loop` + Cron 工具 | 内置定时 |
| **多 Agent** | multi-agent routing | Workflow/Pipeline/Parallel | ❌ 不支持 |
| **记忆** | 持久化 SQLite/.jsonl | 会话级 | 会话级 |

> **OpenClaw 不替代 Claude Code/Cowork。三者是不同层次的工具。** Power user 倾向于混合使用。

### 6.3 核心 CLI 工具集（Agent 的"手和脚"）

| CLI | 用途 | Stars |
|-----|------|:-----:|
| **gogcli** | Gmail/Calendar/Drive/Docs/Sheets/Slides 统一 CLI | 7.2K |
| **Peekaboo** | macOS 截图 + GUI 自动化 | 3.4K |
| **wacli** | WhatsApp 同步/搜索/发送 | — |
| **bird** | X/Twitter CLI（cookie 认证，无需 API key） | — |
| **imsg** | iMessage/SMS CLI | — |
| **CodexBar** | Agent 用量监控菜单栏 | 15.6K |
| **summarize** | URL/文件摘要 | 5.8K |
| **mcporter** | MCP → CLI 转换器 | — |
| **tokentally** | LLM token/成本估算库 | ~14K 周下载 |

### 6.4 tokentally 细节

- **发布**：2025.12.19，v0.1.2（最新：2026.06.13）
- **npm**：`tokentally`，MIT 协议，~14K 周下载量
- **核心 API**（浏览器安全）：
  ```ts
  normalizeTokenUsage(raw)          // 标准化 token 计数
  pricingFromUsdPerMillion({...})   // 每百万 token 定价
  estimateUsdCost({usage, pricing}) // 估算美元成本
  ```
- **Node.js 扩展**：`loadLiteLlmCatalog()` / `fetchOpenRouterPricingMap()` / `tallyCosts()`
- **非目标**：不是精确账单级别的对账工具，是最佳估计

---

## 7. 媒体足迹全记录

### 播客 / 长访谈（6 场）

| # | 日期 | 平台 | 主题 | 时长 | 影响力 |
|---|------|------|------|:---:|:---:|
| 1 | 2026.01.28 | The Pragmatic Engineer | "I Ship Code I Don't Read" | 114min | ⭐⭐⭐⭐ |
| 2 | 2026.02.07 | Y Combinator | "Specialized Intelligence over AGI" | ~60min | ⭐⭐⭐⭐⭐ |
| 3 | 2026.02.12 | Lex Fridman #491 | "The Viral AI Agent that Broke the Internet" | 3h14m | ⭐⭐⭐⭐⭐ |
| 4 | 2026.02.16 | Changelog News #181 | "All the Claw Things" | 6min | ⭐⭐ |
| 5 | 2026.02.25 | OpenAI Builders Unscripted | Romain Huet 主持 | ~60min | ⭐⭐⭐⭐ |
| 6 | 2026.02 | Andreas Klinger | "Europe's Most Ambitious Startups" | 20min | ⭐⭐⭐ |

### 大会 Keynote / 演讲（15+ 场）

| 级别 | 活动 |
|:---:|------|
| 🌍 | **TED2026** — "How I Created OpenClaw" |
| 🌍 | **AI Engineer World's Fair 2026** — 开幕 Keynote "Software Factories" |
| 🌍 | **Microsoft Build 2026** — "Build the Thing That Builds the Thing" |
| 🌍 | **VivaTech 2026** — "The Agentic Enterprise" |
| 🌍 | **NVIDIA GTC 2026** — "The Agentic AI Inflection Point" |
| 🏢 | Snowflake Summit · Forge Summit · Imperial College · LVMH |
| 🇪🇺 | #PragmaConf · NSSpain · Swift Connection · CASE Conference |

### 印刷/文字媒体（7+ 篇）

| 媒体 | 主题 |
|------|------|
| **Bloomberg** | 中美 AI "温差" |
| **Business Insider** | "The moment AI changed everything" |
| **MIT Technology Review** | "Is a Secure AI Assistant Possible?" |
| **TechCrunch** | "Be more playful and allow yourself time to improve" |
| **ORF** | 奥地利国家电视台专访 |

### 中国媒体报道（12+ 家）

| 媒体 | 文章标题 |
|------|---------|
| **36氪** | Meta与OpenAI争抢收购OpenClaw / YC 独家专访 |
| **爱范儿** | "你很难跟一个纯粹为了好玩的人竞争" |
| **量子位/IT之家** | "龙虾之父新访谈：拦不住滥用，只劝大家别玩火" |
| **C114** | Lex Fridman + Builders Unscripted 全文转录 |
| **鞭牛士** | Bloomberg 采访翻译 |
| **Chinaz** | "OpenClaw之父谈AI温差：不准用 vs 不敢不用" |
| **PConline** | "中美 AI 使用差异及未来智能体新设想" |
| **经济观察报** | 周鸿祎评"龙虾"安全风险 |

---

## 8. 关键叙事线索

### 线索一：从 Burnout 到重生

```
2011-2021 黄金十年
    ↓
2021.10 €100M 退出
    ↓
2021-2024 "三年黑暗期"
    · 几乎不碰电脑
    · 治疗 · 死藤水 · 换国家 · 派对
    · 全部无效
    ↓
2024 末 AI 重新点燃火花
    · 2025 年建了 44+ 个项目
    · "You don't find purpose. You create it."
    ↓
2025.11-2026.02 OpenClaw 爆炸式增长
    · GitHub 史上最快增长
    · 三方争夺人才
    ↓
2026.02-现在 加入 OpenAI
    · "改变世界，不是建立大公司"
```

**解读**：这是一个人被 AI 从存在危机中拉回来的故事。他从一个几乎放弃技术的人，变成了推动 AI Agent 革命的旗手。他的 burnout 叙事让无数技术创业者产生共鸣——"你也可能 burnout，但 AI 可以让你重新爱上创造。"

### 线索二：从 iOS 传奇到 AI 先驱

```
iOS 时代 (2011-2021)
    · PSTCollectionView / Aspects / InterposeKit
    · 8,400+ GitHub stars
    · "iOS 泰坦"级别的工程师
    
AI 时代 (2024-2026)
    · OpenClaw 370K+ stars
    · "Clawfather"
    · 13 年开源社区信用 → 瞬时而起的信任
```

**解读**：他不是"跨界"。他的 iOS 底层工程能力（内存管理、并发、逆向工程）直接转化为 AI Agent 设计能力。13 年积累的社区信用（"工具就是好用"）让 OpenClaw 不需要营销就能第一天获得 9,000 stars。

### 线索三："不改代码，改世界"

```
代码本身不再有价值
    → "删除它，几个月就能重建"
    → "真正有价值的是 idea、注意力、品牌"
    
App 80% 会消失
    → "它们只是慢速的 API"
    → Agent 直接与 API 交互，不需要 UI

编程将成为"编织"
    → 为热爱而做，不为必需而做
    → "如果你的身份是建造和解决问题，你会永远被需要"
```

### 线索四：CLI — Unix 哲学的 Agent 复兴

```
MCP：为每个服务写一个 MCP Server → 44K tokens schema overhead
CLI：直接 exec() → 1K tokens 实际调用
     → Unix 管道组合 → 匹配 Agent 推理链
     → 零配置 → 自文档化 (--help)
     → mcporter 把 MCP 转回 CLI
     
Perplexity CTO / YC CEO 跟进 → 行业共识形成
```

### 线索五：娱乐至死——但认真

```
"你很难跟一个纯粹为了好玩的人竞争"
    · 拒绝 VC 数十亿估值
    · 选了影响力，而不是价格
    · 自掏腰包 $10-20K/月 API 费
    · 月收入不到 2 万美元 —— 亏钱养项目

但他的"好玩"是认真的：
    · 3 年黑暗期的能量全部释放
    · 44 个项目深练 AI 技能
    · 1 小时原型改变世界
    · 400K+ stars 不是靠运气
```

---

## 9. 附录：信息源清单

### 一手信源

| 类型 | 链接 |
|------|------|
| 个人网站 | https://steipete.me |
| GitHub | https://github.com/steipete |
| 演讲归档 | https://github.com/steipete/speaking |
| Speaker Deck | https://speakerdeck.com/steipete |
| npm | https://www.npmjs.com/~steipete |

### 关键博客文章（2025）

| 日期 | 文章 | 链接 |
|------|------|------|
| 2025.06.25 | Slot Machines for Programmers | steipete.me |
| 2025.08.19 | Just One More Prompt | steipete.me/posts/just-one-more-prompt |
| 2025.10.14 | Just Talk To It | steipete.me/posts/just-talk-to-it |
| 2025.12.28 | Shipping at Inference-Speed | steipete.me/posts/2025/shipping-at-inference-speed |

### 关键访谈

| 平台 | 链接 / 搜索关键词 |
|------|------|
| Lex Fridman #491 | lexfridman.com/peter-steinberger-transcript |
| Y Combinator | "OpenClaw creator specialized intelligence" |
| The Pragmatic Engineer | "I Ship Code I Don't Read" |
| OpenAI Builders Unscripted | YouTube |
| TED2026 | youtube.com/watch?v=7rzYDM6vMtI |

### 关键项目

| 项目 | 链接 | Stars |
|------|------|:---:|
| OpenClaw | github.com/openclaw/openclaw | 370K+ |
| CodexBar | github.com/steipete/CodexBar | 15.6K |
| ClawHub | github.com/openclaw/clawhub | 8.5K |
| gogcli | github.com/steipete/gogcli | 7.2K |
| summarize | github.com/steipete/summarize | 5.8K |
| Peekaboo | github.com/steipete/Peekaboo | 3.4K |
| tokentally | github.com/steipete/tokentally | 76 |

### 中国媒体深度报道

| 平台 | 关键词搜索 |
|------|------|
| 36氪 | "OpenClaw创始人" OR "龙虾之父" |
| 爱范儿 | "你很难跟一个纯粹为了好玩的人竞争" |
| 量子位 | "龙虾之父新访谈 OpenClaw 内幕" |
| CSDN | "OpenClaw 架构解析" + "MCP vs CLI" |

### 学术引用

- arXiv:2604.14228 — *"Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems"* (April 2026)
- O'Reilly Live Event — *"OpenClaw, Claude Cowork, and Claude Code Compared"*

---

> 📄 *本报告由 3 个并行子 Agent 独立调研 + 交叉验证 + 系统化合成生成，覆盖 ~108 次搜索调用和 WebFetch。*
> 📄 *生成时间：2026-07-06*
> 📄 *调研范围：Peter Steinberger (@steipete) 个人背景 · 职业轨迹 · 产品哲学 · 360 天媒体足迹 · 思想演进*
