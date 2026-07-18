# CLAUDE.md — 本 Vault 的维护规则（LLM Wiki Schema）

> 本文件是 Claude Code 在本 vault 工作的指令手册。任何在本目录（`/Users/wyf/Desktop/code/document`）启动的 claude 会话会自动读取。
> 模式：**Karpathy LLM Wiki** —「人选材料，LLM 维护」。Obsidian 是 IDE，LLM 是维护者，wiki 是知识库。

## 1. Vault 定位

wyf 的个人知识库，存放 AI/大数据领域的调研、人物思想、行业报告、技术实践、求职职业、工作方法论。目标：可被 Claude Code 读写、Obsidian 可视化、定期复盘自我进化的**持久知识网络**（不是一次性问答，而是越用越密的积累）。

## 2. 分类逻辑（6 类，`01-`~`06-` 前缀固定顺序）

| 目录 | frontmatter `type` | 内容 |
|---|---|---|
| `01-people/` | `people-analysis` | 人物思想深度调研（创业者/研究者/高管/分析师/投资人） |
| `02-industry/` | `industry-report` | 行业趋势/公司报告 |
| `03-ai-token/` | `ai-token` | AI Token/算力经济（`research/` `delivery/` `data/`） |
| `04-tech/` | `tech-practice` | 技术实践（`dataworks/` 数仓项目、`interviews/` 面试、散篇） |
| `05-career/` | `career` | 求职/职业/岗位调研 |
| `06-workflows/` | `workflow` | 工作方式/方法论 |

新文档入库按内容归类，存疑时读首段判断；跨类主题按**主旨**归一类，用 tags 跨类关联。

## 3. 文件命名规范

- 小写英文+下划线为主；中文人物名/主题可保留中文
- 人物调研：`<英文名>_analysis.md` 或 `<中文名>_<主题>.md`
- 不用空格，用下划线；日期后缀 `_YYYY-MM-DD`

## 4. frontmatter 标准（每个文档必须有）

```yaml
---
title: 标题
type: people-analysis      # 见 §2 六选一
date: 2026-07-18           # 文档日期/整理日期
tags: [人物名, 主题, 技术]   # 用于跨类关联与 Obsidian 标签
status: active             # active | stale | draft
source: 原始来源或生成方式   # 如 "Tavily 调研 + 官方新闻稿"
---
```

## 5. 链接规范

- **文档间引用用 wikilink**：`[[文件名]]` 或 `[[文件名|显示文本]]`。Obsidian 原生支持，移动文件不失效。
- **不要用相对路径** `../xxx.md`（移动易断）。
- 概念/人物/主题的交叉链接汇聚在 `INDEX.md`。
- 引用源文件时给出 `文件路径:行号` 便于跳转。

## 6. 三个核心操作

### ingest — 新文档入库
1. 判断分类，放入对应目录
2. 补全 frontmatter（§4）
3. 在该类 `_index.md` 添加条目
4. 在 `INDEX.md` 添加交叉链接（人物关系/概念关联）
5. 追加 `CHANGELOG.md` 一行
6. `git add -A && git commit`

### query — 查询
用户问 vault 内容时：先用 Grep/Read 检索相关文件，给出 **grounded 答案**（基于本库内容，不杜撰），引用源文件路径。涉及多文件时交叉综合。

### lint — 检查维护 / 复盘
用户说「复盘 vault」「lint」「整理一下」时执行：
1. 扫 **orphan**（无任何入链的文档）
2. 扫 **stale**（`status: stale` 或长期未更新，提示复核）
3. 扫 **坏链**（失效的 wikilink / 相对链接）
4. 补 **缺失 frontmatter**
5. 更新 `INDEX.md` 与各 `_index.md`
6. 追加 `CHANGELOG.md`
7. `git commit`（message 说明本次 lint 做了什么）

## 7. 安全规则

- **不删除人写的原创正文**；废弃用 `status: stale` 标记，不物理删
- 重大改动前先 `git commit`；可 `git checkout` 回滚
- **不在 vault 存** API key / 密码 / token
- LLM 维护页（`INDEX.md` / `_index.md` / `CHANGELOG.md` / `CLAUDE.md`）可自由改；人的调研文档**只补 frontmatter 与 wikilink，不改正文**
- 每次操作后 `git commit`，保持历史可追溯

## 8. Obsidian 协同

- `/.obsidian/` 是 Obsidian 配置，不要手动改（已被 .gitignore 部分排除）
- 优先用 wikilink、frontmatter、tags（Obsidian 原生能力）
- 保持 frontmatter 规范，便于 Dataview/标签查询
- 图谱视图依赖 wikilink，多建交叉链接让知识网络可视化

## 9. 自我进化闭环

```
新增文档 → ingest 入类 → lint 更新交叉链接与 INDEX → CHANGELOG 记录
   ↑                                                    ↓
   └────────── 定期复盘（用户触发或 cron 提醒）←────────┘
```

知识在 wikilink 网络中沉淀，每次 lint 让网络更密、索引更新、孤儿归位。这是 vault 的核心价值。
