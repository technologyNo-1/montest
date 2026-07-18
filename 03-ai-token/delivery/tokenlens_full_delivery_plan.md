# TokenLens 第二轮：真实落地全链路设计

> 基于 12 份调研报告 + 竞品分析 + 第一性原理推演
> 目标：3 个月内从 0 到付费用户
> 日期：2026/07/06

---

## 一、竞品复盘 —— 这个赛道到底有没有人在做？

### 1.1 现有竞品全景

| 产品 | 类型 | 主力用户 | 核心功能 | 定价 | 致命缺陷 |
|------|------|------|------|------|------|
| **AgentMeter** v0.4.1 | OSS CLI+Web | Claude Code 个人开发者 | Token 趋势图、模型饼图、缓存命中率、预算告警 | 免费 | 只是个人工具——没有团队、没有 RBAC、没有企业报告 |
| **ccboard** v0.22 | OSS TUI+Web (Rust) | Claude Code/Cursor/Codex 个人 | 13 个交互面板、异常检测、30 天预测、安全审计 | 免费 | TUI 界面——CFO 不可能用 |
| **openclaw-cost-tracker** v1.1 | OSS MCP Server | 多 Agent 运维者 | 成本归属、异常检测（3x 中位数阈值）、429 预测 | 免费 | 纯 MCP 协议——需要技术栈，非开箱即用 |
| **TokenWise Tracker** v1.3.2 | OSS NPM 库 | OpenAI Node.js 开发者 | Proxy 包裹、零代码接入、LangChain 集成 | 免费 | 仅 OpenAI，功能单薄 |
| **Ramp AI Spend** | 企业 SaaS | 财务/采购 | 企业卡级 Token 支出追踪、统一发票+用量 | 捆绑 Ramp（不单独卖） | 粒度不够——看得到花了多少钱，看不到花在哪 |
| **Paid.ai** | 企业 SaaS | AI SaaS 公司的 CFO | 按客户/按操作的成本追踪、利润管理 | 未公开 | 偏 SaaS 公司内部利润管理，不是通用 AI 支出 |
| **Engram** | 企业级（$98M 融资） | 模型层优化 | ~100x Token 压缩（"学习式记忆"） | 未公开 | 不是 FinOps——是模型层面的压缩技术 |
| **Together AI** | 推理平台 | 开发者 | 开源模型推理，$1.3B 融资 | 按 Token | 不是 FinOps——是推理转售商 |
| **Datadog / New Relic** | 企业可观测性 | DevOps 团队 | 正在增加 Token 级别的可观测性和 GPU 监控 | 捆绑现有产品 | 早期阶段，非核心功能 |

### 1.2 竞品缺口 —— 我应该切入的位置

```
个人开发者 ──────── 小团队(5-50人) ──────── 中大型企业(50-5000人)
    │                    │                        │
AgentMeter ✓         ← 空白！→              Ramp (太粗)
ccboard ✓              │                    Paid.ai (偏 SaaS 内部)
                        │                    Datadog (早期)
                   ★ 我的位置               Engram (不同赛道)
```

**核心洞察**：个人开发者工具有 5+ 个 OSS 免费选项。企业巨头的 FinOps 正在被 Datadog/Ramp 抢占。但**中间地带——5-50 人的 AI 原生团队、YC 创业公司、小型软件工作室——完全没有人在服务。**

这些团队的特征：
- 每月在 AI API 上花 $2,000-$50,000
- 没有专门的 FinOps 团队
- 团队里的 CTO 对开销感到不安但没时间追踪
- 不想自己搭建 AgentMeter + SQLite + Grafana
- 愿意为"开箱即用"付费（$50-500/月）

---

## 二、精准切入选定：小团队 AI 支出治理

### 2.1 为什么是这个位置？

| 理由 | 详细说明 |
|------|------|
| **竞争最弱** | 个人工具和大型企业之间有一片真空地带 |
| **付费意愿强** | 团队每月花 $2K-50K 在 API 上——花 $200 监控 $20K 支出是明显的 ROI |
| **技术可行** | 不需要像 Engram 那样做 $98M 融资才能做的模型层工作 |
| **增长路径清晰** | 5 人团队 → 50 人 → 500 人，产品可平滑升级 |
| **个人经验匹配** | 我自己就是这类团队的目标用户——我知道痛点 |

### 2.2 用户画像

**主要用户**：
- YC/W25 批次的 AI 创业公司 CTO（每月烧 $5K-15K 在 API 上）
- AI 原生软件工作室的技术负责人（5-30 个工程师，每个人都用 Claude/Cursor）
- Web3/AI 跨界团队的工程经理（多模型、多 API Key、多项目）

**他们当前在做什么**：
- 用 Excel/Notion 手工追踪 API 成本（每月花 2-3 小时）
- 或者根本不追踪（"我们怕看到数字"）
- 偶尔被 AWS 账单吓一跳但不知道哪个项目花的最多

### 2.3 产品定位

**一句话**：小团队 AI 支出的控制面板——5 分钟接入，实时可见，恐慌预防。

**不是什么**：
- 不是 Datadog 的竞品（不需要 100 种集成）
- 不是 AgentMeter 的竞品（不是个人工具）
- 不是 Ramp 的竞品（不碰企业卡/发票）

---

## 三、产品设计

### 3.1 MVP 功能范围（Month 1-3）

```
┌─────────────────────────────────────────────────────────────┐
│                      TokenLens MVP                         │
├───────────────┬──────────────────────┬─────────────────────┤
│  接入层       │     核心面板         │    告警与治理        │
├───────────────┼──────────────────────┼─────────────────────┤
│               │                      │                     │
│ · 5 行代码    │ · 实时成本仪表盘     │ · 预算上限告警      │
│   SDK 接入    │   （按团队/项目/模型）│   （"Dev 组 Token   │
│               │                      │   用量超 80%"）     │
│ · 支持 OpenAI │ · 模型使用分布饼图   │                     │
│   Anthropic   │                      │ · 异常检测          │
│   Google      │ · 日/周/月消费趋势   │   （"今天的 Token   │
│   DeepSeek    │                      │   用量是昨天的 3x"）│
│               │ · Top 消费者排行榜   │                     │
│ · 自动读取   │   （按人/按 API Key）│ · 硬上限保护        │
│   环境变量    │                      │   （"超过 $500/天   │
│               │                      │   自动暂停"）       │
└───────────────┴──────────────────────┴─────────────────────┘
```

### 3.2 SDK 设计（最核心的接入体验）

```javascript
// 唯一需要的代码变更——其他都不用改
// Before: 
//   const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })
// After:
//   const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })
//   + import { TokenLens } from 'tokenlens'
//   + TokenLens.wrap(anthropic, { team: 'backend', project: 'api-v2' })

// 或者更简单的——环境变量模式，不需要改任何代码：
//   TOKENLENS_ENABLED=true
//   TOKENLENS_TEAM=backend
//   就这么简单——剩下的全部自动拦截
```

### 3.3 仪表盘设计

**第一屏（CEO/CTO 视角）**：
```
┌──────────────────────────────────────────────────────────┐
│  本月 AI 支出: $12,847  │  较上月: +23%  │  预算剩余: 64% │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  [消费趋势线图: 过去 30 天，按模型颜色分层]               │
│                                                          │
│  按团队拆分:                         按模型拆分:          │
│  Backend:  $5,200 ████████████       Claude:  $8,200    │
│  Frontend: $3,100 ██████             GPT-4o:  $3,500    │
│  Data:     $2,800 █████              DeepSeek: $1,147   │
│  Design:   $1,747 ███                                       │
│                                                          │
│  ⚠️ 告警: Backend 团队昨天 Token 用量是正常的 3.2x       │
│  💡 建议: 切换到 DeepSeek 处理 CRUD 操作可节省 $3,200/月 │
└──────────────────────────────────────────────────────────┘
```

### 3.4 技术架构（单体，不是微服务）

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  SDK     │────▶│  Ingestion   │────▶│  PostgreSQL  │
│ (JS/Py)  │     │  API (FastAPI)│    │  + TimescaleDB│
└──────────┘     └──────────────┘     └──────────────┘
                        │                      │
                        ▼                      ▼
                 ┌──────────────┐     ┌──────────────┐
                 │  Dashboard   │     │  Alert Engine │
                 │  (Next.js)   │     │  (Cron Jobs)  │
                 └──────────────┘     └──────────────┘
                        │
                        ▼
                 ┌──────────────┐
                 │  Stripe      │
                 │  Billing     │
                 └──────────────┘
```

**为什么是单体？**
- 我一个人开发
- 初期用户 < 100 个团队
- 单体可以做到 $1M ARR 之前不拆分
- Next.js + FastAPI + PostgreSQL 一个 docker-compose 启动

---

## 四、开发时间轴（12 周）

### Week 1-2: SDK + Ingestion

```
Week 1:
  Day 1-2: 搭建项目骨架（Next.js + FastAPI + PostgreSQL Docker）
  Day 3-5: 实现 Anthropic SDK wrapper（Python + JS）
           - Monkey-patch Anthropic().messages.create()
           - 抓取: model, input_tokens, output_tokens, stop_reason
           - 异步发送到 ingestion API（fire-and-forget）

Week 2:
  Day 1-3: 实现 OpenAI SDK wrapper（同上模式）
  Day 4-5: Google Gemini + DeepSeek SDK wrapper
           - 4 个 SDK 的统一数据格式
```

### Week 3-4: Dashboard + Auth

```
Week 3:
  Day 1-3: Next.js Dashboard（消费趋势图、按模型拆分饼图、Top 消费者）
  Day 4-5: 用户认证（GitHub OAuth + Magic Link）

Week 4:
  Day 1-2: 团队管理（创建团队、邀请成员、分配角色）
  Day 3-4: API Key 管理（自动读取环境变量中的 API Key）
  Day 5: 部署到 Vercel + Railway
```

### Week 5-6: Alerts + Budget

```
Week 5:
  Day 1-3: 预算引擎（按团队/项目/日/月设置上限）
  Day 4-5: 告警通知（Email + Slack Webhook）

Week 6:
  Day 1-2: 异常检测（Z-score > 3σ → 自动告警）
  Day 3-4: 硬上限保护（达到上限 → 可配置：告警/暂停/继续）
  Day 5: 测试 + 修复
```

### Week 7-8: Optimization Engine

```
Week 7:
  Day 1-3: 成本分析引擎
           - 扫描历史调用 → 识别"用 Claude Opus 写简单 CRUD"的模式
           - 生成建议："这些查询可以用 DeepSeek 处理，节省 $X/月"
  Day 4-5: 建议仪表盘 + Email 周报

Week 8:
  Day 1-3: 智能路由（可选功能——自动把小查询路由到便宜模型）
  Day 4-5: 集成测试
```

### Week 9-10: Billing + Polish

```
Week 9:
  Day 1-3: Stripe 集成（Free / Pro $99/mo / Team $299/mo）
  Day 4-5: 支付页面 + 发票生成

Week 10:
  Day 1-2: Landing Page（tokenlens.io）
  Day 3-5: Onboarding flow 优化 + 文档 + Demo 视频
```

### Week 11-12: Alpha → Beta Launch

```
Week 11:
  Day 1-3: 邀请第一批 5 个 Design Partner 免费使用
  Day 4-5: 收集反馈 + 紧急修复

Week 12:
  Day 1-2: 第二轮修复
  Day 3-4: Product Hunt 发布准备（文案/截图/视频/定价）
  Day 5: Product Hunt Launch 🚀
```

---

## 五、精准获客 —— 如何找到前 50 个付费用户

### 5.1 渠道优先级

| 渠道 | 优先级 | 策略 | 预期转化 |
|------|:---:|------|:---:|
| **YC 社区** | ★★★★★ | YC 内部论坛 + YC 群聊 | 最高质量的前 10 个客户 |
| **Twitter/X** | ★★★★ | 发布"Token 成本透明化"的实战内容 | 有机增长 |
| **Claude Code Discord** | ★★★★ | 参与讨论 + 帮助别人解决 Token 成本问题 | 精准 |
| **GitHub** | ★★★ | 开源一个简单的 Token Tracker 工具引流 | 自然 funnel |
| **Product Hunt** | ★★★ | 第 12 周发布 | 一次性爆发 |
| **Indie Hackers** | ★★ | 记录构建过程（build-in-public） | 慢但稳定 |
| **Hacker News** | ★★ | "Show HN: I built a tool to stop $500K AI bills" | 不可预测 |

### 5.2 具体的获客操作

**前 5 个 Design Partner（Week 1-8）**：
1. 从 Claude Code Discord 找到 3 个"抱怨 AI 账单太贵"的人 → DM 他们
2. 从 Twitter 找到 2 个发推"我们的 AI 成本失控了"的 CTO → 免费给他们用
3. 每周和他们通 30 分钟电话 → 功能优先级 100% 由他们定义

**前 50 个付费用户（Week 8-16）**：
1. Product Hunt 发布（预期 200-500 upvotes → 30-50 次注册）
2. YC 内部推荐（前 10 个客户相互推荐）
3. 写一篇 "We spent $X on AI and didn't know where it went — so I built TokenLens" 的文章
4. 录一个 60 秒的 demo 视频 → 投放在 Claude Code Twitter 讨论下面
5. 开源一个小工具（如 `npx tokenlens-cli`）→ GitHub → TokenLens SaaS 的自然 funnel

### 5.3 为什么这个获客策略有效？

- **"抱怨 AI 账单"是正在发生的高频行为** —— 搜索 "Claude bill" / "AI spend" 每天都有新推文
- **YC 的 "tokenmaxx" 哲学意味着 YC 创业公司正在刻意增加 Token 消耗** —— 他们需要监控工具
- **小团队 CTO 是最容易转化的用户** —— 决策链短（一个人决定），痛感强（花的是自己的钱）

---

## 六、商业模式与支付

### 6.1 定价策略

| 版本 | 月费 | 追踪 Token 上限 | 核心功能 |
|------|:---:|------|------|
| **Free** | $0 | <5000 万 Token/月 | 单人仪表盘、基础趋势、1 周数据保留 |
| **Pro** | $99/月 | <5 亿 Token/月 | 团队管理、预算告警、30 天保留、Email 周报 |
| **Team** | $299/月 | <50 亿 Token/月 | SSO、API 路由建议、90 天保留、Slack 告警、优先支持 |
| **Enterprise** | $999+/月 | 无限 | RBAC、审计日志、自定义集成、专属 Onboarding |

**为什么是这个价格点？**
- $99/月 → 一个 5 人团队每月在 API 上花 $5,000→ 监控成本是支出的 2%
- $299/月 → 一个 20 人团队每月花 $20,000 → 监控成本是支出的 1.5%
- 如果我能帮他们省 20%（通过优化建议和异常告警）→ ROI 是 10-20x

### 6.2 支付实现

**支付网关**：Stripe（最成熟、支持全球、自动税务）
- Stripe Checkout → 10 分钟集成
- Stripe Billing → 订阅管理、发票、dunning
- Stripe Tax → 自动计算 VAT/GST

**支付流程**：
```
用户注册（免费）
  ↓
试用 14 天（Pro 功能全开）
  ↓
14 天后 → 选择 Free（降级）或 Pro/Team（付费）
  ↓
Stripe Checkout → 信用卡/借记卡
  ↓
月度自动续费
```

**中国用户支付问题**：
- 如果客户在中国 → 额外提供"手动银行转账 + 手动开通"选项
- 后续可接入支付宝/微信支付（通过 Stripe 或直接集成）

---

## 七、风险与应对

| 风险 | 概率 | 影响 | 应对 |
|------|:---:|:---:|------|
| **AgentMeter 加团队功能** | 中（6 个月） | 中 | AgentMeter 是个人项目——作者不一定想商业化。我专注商业化速度 |
| **OpenAI 自己做了成本仪表盘** | 高 | 中 | 跨供应商的独立中立方价值 > 单一供应商的工具 |
| **Ramp 做细化了** | 中 | 低 | Ramp 不会为 5 人团队优化——他们盯的是 $100M+ 企业 |
| **没人付钱** | 中低 | 高 | 前 5 个免费用户先验证需求——如果没人愿意付钱，第 8 周就知道 |
| **我一个人搞不定** | 高 | 高 | Claude Code 写 80% 的代码，我只做架构决策和代码审查 |
| **获客成本太高** | 中 | 中 | 优先走社区+内容——不投付费广告，直到 LTV/CAC > 3x |

---

## 八、为什么是现在？——时机窗口分析

```
2023-2024:  AI 还在实验阶段 → Token 支出是"研发成本" → 不需要 FinOps
2025 上半年: AI 开始进入生产 → Token 支出快速增长 → 开始有人抱怨
2025 下半年: ★ 转折点 ——
  · Uber 花光了 2026 年全年的 AI 预算（仅在 4 月）
  · 一家公司收到了 $500M 的 Claude 账单
  · Microsoft 撤销了部分 Claude Code 许可证
  · 上市公司 CFO 开始在季度会上问"我们的 AI 花了多少钱？"
  · YC 官宣 "tokenmaxx, not headcountmaxx"
2026 年 7 月: ★ 最好的进入时机 ——
  · 痛点已经明确（"the bill comes due"）
  · 但解决方案还没标准化（Linux Foundation 7 月才启动标准讨论）
  · 个人工具有 5+ 个——但企业/团队工具是真空
  · 竞品还在早期阶段（Datadog "正在添加"、Ramp "太粗"）
```

**6 个月后会发生什么？** 如果我不做，以下之一会发生：
- Datadog 买下 AgentMeter 或 ccboard，加上团队功能
- Ramp 收购一家 Token 追踪公司，把它塞进企业卡产品
- OpenAI 自己发布 "API Cost Dashboard"（但他们只会追踪自己的 API）

**答案**：现在就是最好的时刻。不是 3 个月前（痛点还不够痛），不是 6 个月后（会有人先做）。

---

## 九、第一周应该做什么——砍掉一切废话

如果现在是周四下午，我给自己周一早上的任务清单：

```
MONDAY MORNING TASK LIST:

[ ] 1. mkdir tokenlens && cd tokenlens && git init
[ ] 2. npm create next-app@latest dashboard --typescript --tailwind
[ ] 3. 写第一个 Anthropic SDK wrapper（20 行 monkey-patch）
[ ] 4. 测试：拦截自己的 Claude Code 调用 → console.log 出 model/tokens/cost
[ ] 5. 如果 Step 4 成功 → 发推 "I hacked a 20-line
       token tracker for Anthropic. Should I build this for teams?"
[ ] 6. 如果 Step 5 有 5+ 个人回复"需要" → 就是它了
[ ] 7. 如果有 0 个回复 → 找他们私聊——问"你们团队 AI 花了多少钱？"
```

**不需要的**：
- 商业计划书 → 已经写好了
- 融资 → TokenLens 不需要 $1M+ 种子轮来启动
- 域名 → `.vercel.app` 可以先跑起来
- Logo → emoji 先用三个月

---

## 十、给自己一句话

> "Token 的钱在流向企业，但控制面还没有流向企业。你做它的控制面。"

---

*规划日期：2026/07/06 | 基于竞品分析 + 第一性原理 + 可执行性评估*
