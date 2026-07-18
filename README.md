# wyf 的知识库 Vault

> 个人 AI/大数据知识库 · Obsidian vault · Claude Code 维护
> 模式：**Karpathy LLM Wiki** — 人选材料，LLM 维护
> 最近整理：2026-07-18

## 这是什么

存放 AI 人物思想、行业报告、AI Token 经济、大数据技术、求职职业、工作方法论的**持久知识网络**。可用 Obsidian 浏览/编辑，用 Claude Code 查询/维护，定期复盘自我进化。

## 分类地图

| 目录 | 内容 | 文件数 |
|---|---|---|
| [`01-people`](./01-people/_index.md) | 人物思想深度调研（Ilya/黄仁勋/Thiel/Karpathy 系/a16z 系列/李飞飞等） | 19 |
| [`02-industry`](./02-industry/_index.md) | 行业趋势/公司报告（Cresta/顺网/半导体/MIT AI 专业等） | 6 |
| [`03-ai-token`](./03-ai-token/_index.md) | AI Token/算力经济（研究/TokenLens 落地/数据源） | 12 |
| [`04-tech`](./04-tech/_index.md) | 技术实践（Spark/数仓 dataworks 项目/字节面试） | 12 |
| [`05-career`](./05-career/_index.md) | 求职/职业/岗位调研 | 6 |
| [`06-workflows`](./06-workflows/_index.md) | 工作方式/方法论 | 2 |

## 按用途导航

| 我想知道… | 去哪 |
|---|---|
| 某位 AI 人物的思想 | [`01-people/`](./01-people/_index.md) |
| AI 行业趋势 / 某家公司 | [`02-industry/`](./02-industry/_index.md) |
| Token 经济 / 算力 / TokenLens | [`03-ai-token/`](./03-ai-token/_index.md) |
| 大数据技术 / 数仓 / 字节面试 | [`04-tech/`](./04-tech/_index.md) |
| 求职 / 职业规划 | [`05-career/`](./05-career/_index.md) |
| 工作方法论 / AI Native 实践 | [`06-workflows/`](./06-workflows/_index.md) |
| 全库概念关系与人物网络 | [`INDEX.md`](./INDEX.md) |

## 如何维护（Claude Code 用法）

在本目录启动 claude 后：

- **新增文档**：把文件放对应目录，对 claude 说「入库 xxx」，它会补 frontmatter + 更新索引 + commit
- **查询**：直接问，如「总结 Ilya 的核心观点」「Token 经济有哪些反向风险」，claude 检索本库给出 grounded 答案
- **复盘**：说「复盘 vault」或「lint」，claude 扫孤儿/坏链/补 frontmatter/更新索引/commit
- **可视化**：用 Obsidian 打开本目录作为 vault，看图谱/标签/反向链接

## 维护规则

- 完整规则见 [`CLAUDE.md`](./CLAUDE.md)（claude 自动读取）
- 变更记录见 [`CHANGELOG.md`](./CHANGELOG.md)
- 不删原创正文；废弃标 `status: stale`；不存密钥

## 目录结构

```
document/
├── README.md          ← 本文件（面向人）
├── CLAUDE.md          ← 维护规则（面向 claude）
├── INDEX.md           ← 概念地图/人物网络（LLM 维护）
├── CHANGELOG.md       ← 维护日志
├── 01-people/         _index.md + 19 篇
├── 02-industry/       _index.md + 6 篇
├── 03-ai-token/       _index.md + research/ delivery/ data/
├── 04-tech/           _index.md + dataworks/ interviews/ + 散篇
├── 05-career/         _index.md + 6 篇
└── 06-workflows/      _index.md + 2 篇
```
