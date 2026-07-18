# TokenLens —— 执行决策速查卡

## 产品

**一句话**：小团队 AI 支出的控制面板。5 分钟接入，实时可见，恐慌预防。

**核心数字**：
- TAM：AI API 支出 ~$350 亿/年 → 其中 5-50 人团队 ~$30-50 亿
- 定价：$99-$299/月
- 目标客户：YC 创业公司 / AI 原生软件工作室 / Web3 AI 团队
- 理想状态：一个 20 人团队月花 $20K 在 API 上 → 花 $299 监控 $20K 支出 = 1.5% 成本 → ROI 明确

## 竞品卡位

```
个人开发者 ← → 小团队(5-50人) ← → 大型企业
AgentMeter ✓      ★ 我的位置         Ramp (太粗)
ccboard ✓         （完全真空）        Datadog (早期)
```

## 12 周路线

| 阶段 | 周期 | 关键产出 | 验证节点 |
|------|:---:|------|:---:|
| **1. SDK+摄取** | W1-2 | 4 个 LLM SDK 拦截器 | Anthropic wrapper 能正确抓取 token 数据 |
| **2. 仪表盘+认证** | W3-4 | Next.js Dashboard + GitHub OAuth | 自己能登录看到自己的 API 用量 |
| **3. 告警+预算** | W5-6 | 预算引擎 + Email/Slack 告警 | 超过预算时能收到告警 |
| **4. 优化引擎** | W7-8 | 省钱建议 + 智能路由 | 给前 5 个用户看建议——他们觉得有用吗？ |
| **5. 支付+上线** | W9-10 | Stripe 集成 + Landing Page | 有人愿意填信用卡吗？ |
| **6. Alpha→Beta** | W11-12 | 5 Design Partners → Product Hunt | Product Hunt 发布 |

## 获客漏斗

```
Claude Code Discord 抱怨者 → DM → 免费试用
Twitter 发 "AI 账单太贵" 的 CTO → 回复 → 免费试用
YC 内部推荐 → 试用 14 天 → 付费
Product Hunt → 注册 → 试用 14 天 → 付费
```

## 定价

| Free | Pro | Team |
| $0 | $99/月 | $299/月 |
| <5,000 万 Token | <5 亿 Token | <50 亿 Token |

## 最大的三个风险

1. **没人付钱** → W8 就知道（前 5 个免费用户是否能转化）
2. **我一个人搞不定** → Claude Code 写 80% 代码
3. **AgentMeter 加团队功能** → 比它快 6 个月

## 周一任务

```
[ ] tokenlens init + Anthropic wrapper (20 行)
[ ] 测试成功 → 发推验证需求
[ ] 5+ 回复需要 → 全速推进
[ ] 0 回复 → 私聊找到真实痛点
```

---

*2026/07/06*
