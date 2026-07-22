---
title: Claude Code 记忆全流程：创建·管理·治理（结合本地环境）
type: workflow
date: 2026-07-22
tags: [memory, claude-code, 知识管理, obsidian, 方法论, auto-memory]
status: active
source: "Claude Code 系统机制 + 本地环境实测（2026-07-22）"
---

# Claude Code 记忆全流程：创建·管理·治理

> 写给 wyf 自己看。目标：**听得懂、能照做、结合你本机真实环境**。
> 所有路径、文件名、配置都是 2026-07-22 在你机器上实测的，不是泛泛而谈。

---

## 0. 一句话先听懂

Claude 的"记忆"**不是一个东西，是三层各司其职的体系**：

| 层 | 类比 | 一句话 |
|---|---|---|
| **auto-memory** | Claude 的**小抄本** | 机器自动记的"怎么跟你干活"，跨会话自动翻 |
| **CLAUDE.md** | 给 Claude 的**工作守则** | 你定的规矩，进哪个目录读哪本 |
| **vault** | 你的**知识库** | 人机共建的调研/思想/报告，Obsidian 可视化 |

记住这个类比，下面所有细节都是它的展开。

---

## 1. 先听懂：三层记忆各是什么

### 1.1 auto-memory —— 机器的小抄本

**在哪**：`/Users/wyf/.claude/projects/-Users-wyf/memory/`

你机器上现在有 **20 个 memory 文件 + 1 个 `MEMORY.md` 索引**，就是它。

**长什么样**：一个文件记一件事，前面是 frontmatter，后面是正文。真实例子（你的 `claude-code-session-hygiene.md`）：

```markdown
---
name: claude-code-session-hygiene
description: 用户 Claude Code 会话管理习惯:按项目目录开 claude...
metadata:
  node_type: memory
  type: feedback
  originSessionId: 0ced5679-...
  modified: 2026-07-20T17:17:43.585Z
---

用户 2026-07-21 确立的 Claude Code 会话管理原则:
1. 开 claude 前先 cd 到项目目录...

**Why:** 用户原习惯每天在 home 目录开新会话...

**How to apply:** 若发现用户在 home 目录开 claude 做正经项目工作...
关联 [[claude-code-best-practices-learning]]。
```

**frontmatter 字段须知（属性表）**：

| 字段 | 谁写的 | 作用 |
|---|---|---|
| `name` | Claude | kebab-case 文件名，也是 `[[链接]]` 的锚 |
| `description` | Claude | **一行摘要，recall 时靠它判断相不相关**——最重要 |
| `metadata.type` | Claude | 四选一（见下），决定这条记忆的"身份" |
| `metadata.node_type` | **系统自动** | 固定 `memory` |
| `metadata.originSessionId` | **系统自动** | 记这条记忆的原始会话 ID，可溯源 |
| `metadata.modified` | **系统自动** | 最后修改时间，ISO 格式 |

**四种 `type`（身份须知）**：

- `user` —— **你是谁**：角色、专长、偏好（例：你的终端用 Ghostty、走 Clash 代理）
- `feedback` —— **你怎么要我干活**：你给过的纠正/确认，必须带 `**Why:**` 和 `**How to apply:**`（例：`deploy-integration-checklist`、`change-impact-rollback-workflow`）
- `project` —— **在做什么**：进行中的项目目标/约束/状态（例：`spark-lakehouse-project`）
- `reference` —— **东西在哪**：外部资源指针 URL/dashboard/ticket（例：`websearch-broken-use-tavily-mcp` 指向 Tavily 配置）

**怎么被想起来（recall 机制）**：

1. 每次开新会话，`MEMORY.md`（索引，一行一条）**全量塞进上下文**——所以 Claude 一上来就"知道你有哪些小抄"。
2. 具体某个 memory 文件的**正文**，是**按需召回**的：当前任务和某条 `description` 相关时，才把正文读出来。
3. 召回的内容以 `<system-reminder>` 形式注入，**是背景上下文，不是指令**——Claude 不会盲目执行，且其中提到的文件/函数/flag **可能已过时，用前要验证**。

> 类比：`MEMORY.md` 是小抄本的**目录页**（每次都翻），单条 memory 是**具体页**（用到才翻到）。目录页写得好不好，决定了 Claude 能不能在对的时刻翻到对的页。

### 1.2 CLAUDE.md —— 工作守则

**它不是事实，是规矩**：告诉 Claude "在这个目录干活要守什么规矩"。

**层级（从高到低，后者被前者覆盖）**：

| 层 | 路径 | 你本地的情况 |
|---|---|---|
| Enterprise | 系统管理员设 | 无 |
| **User**（全局） | `~/.claude/CLAUDE.md` | **你没有**（全局无守则） |
| **Project**（项目） | `<项目根>/CLAUDE.md` | vault 有：`/Users/wyf/Desktop/code/document/CLAUDE.md` |
| **Local**（个人） | `<项目根>/CLAUDE.local.md` | 不提交 git，个人专属 |

**和 auto-memory 的根本区别**：

- CLAUDE.md = **"规矩"**（你怎么要求 Claude 干活，稳定的指令）
- auto-memory = **"事实"**（发生过什么、你偏好什么，动态积累）

> 类比：CLAUDE.md 是贴在墙上的**操作规程**，auto-memory 是 Claude 自己记的**工作笔记**。规程不会因为聊了一次天就变，笔记会。

### 1.3 vault —— 知识库

**在哪**：`/Users/wyf/Desktop/code/document`（Obsidian vault + git 仓库）

**模式**：Karpathy LLM Wiki ——「**人选材料，LLM 维护**」。Obsidian 是 IDE，Claude 是维护者，wiki 是知识库。

**结构**：8 类固定前缀目录（`01-people` ~ `08-book`），每类有 `_index.md`，全库有 `INDEX.md`（概念地图）+ `CHANGELOG.md`（变更日志）+ `CLAUDE.md`（维护规则）。

**每篇文档的 frontmatter**：`title / type / date / tags / status / source`（详见 vault 的 [[CLAUDE.md]] §4）。

**三个核心操作**（vault 的生命线）：

- **ingest**（入库）：归类 → 补 frontmatter → 更新 `_index.md` + `INDEX.md` → 追加 `CHANGELOG.md` → git commit
- **query**（查询）：基于库内文件给 grounded 答案，引用源文件路径
- **lint**（复盘）：扫 orphan/stale/坏链 → 补 frontmatter → 更新索引 → commit

**怎么和 Claude 打通**（你已配好）：

1. **`obsidian-vault` MCP**（`@modelcontextprotocol/server-filesystem`）：让 Claude 直接读写 vault 文件——这是物理通道。
2. **obsidian skills**（kepano 官方）：`obsidian-markdown`（语法）/ `obsidian-bases`（数据库视图）/ `obsidian-cli`（与运行中的 Obsidian 实例交互）——这是"懂 Obsidian 玩法"的技能包。

### 1.4 三层对比一图流

| 维度 | auto-memory | CLAUDE.md | vault |
|---|---|---|---|
| 性质 | 事实/偏好 | 指令/规矩 | 知识/调研 |
| 谁写 | Claude 自动 | 人写（可让 Claude 起草） | 人选材 + LLM 维护 |
| 体量 | 一事一文，轻 | 一个目录一篇，中 | 8 类 dozens 篇，重 |
| 召回 | 索引全量 + 正文按需 | 进目录全量加载 | 主动检索/Grep |
| 可视化 | 无（纯文件） | 无 | Obsidian 图谱 |
| 治理 | 查重/更新/删错 | 版本管理 | ingest/lint/commit |
| 你本机 | 20 条 | vault 1 篇 | 57+ 篇 |

---

## 2. 创建：什么记哪、怎么记

### 2.1 决策树（先问自己三个问题）

```
要记的东西，先过这三关：

Q1: 是"怎么跟你干活"吗？（偏好/反馈/项目状态/外部资源指针）
  └─ 是 -> auto-memory（走 §2.2）

Q2: 是"你关心的领域知识"吗？（调研/思想/报告/方法论/论文）
  └─ 是 -> vault ingest（走 §2.3）

Q3: 下面这些一律不记：
  ├─ repo 已经记录的（代码结构、过往 fix、git history、CLAUDE.md 已写的）
  ├─ 只对本次对话重要的（临时上下文、一次性任务）
  └─ 密钥/密码/token（vault §7 也明令禁止）
```

**一句话边界**：auto-memory 记"**关系**"（你和 Claude 怎么协作），vault 记"**内容**"（你关心什么）。记不住就问：这条是让 Claude 更懂我，还是丰富我的知识库？

### 2.2 auto-memory 写入流程（含本地实例）

**标准 5 步**：

1. **查重**：先翻 `MEMORY.md` 和已有文件，看是不是已有覆盖的。有就**更新**那条，不要新建。
2. **起名**：`name` 用 kebab-case，语义化（如 `clash-proxy`、`paper-summaries-07-paper`）。
3. **写 frontmatter**：`name` + `description`（一行，recall 就靠它）+ `metadata.type`（四选一）。
4. **写正文**：
   - `feedback` / `project` 类型**必须**带 `**Why:**`（为什么）和 `**How to apply:**`（怎么用）。
   - 用 `[[name]]` 链接相关 memory（如 `[[clash-proxy]]`），让小抄本织成网。
5. **更新索引**：在 `MEMORY.md` 加一行 `- [Title](file.md) - hook`。
   - `node_type` / `originSessionId` / `modified` 系统自动补，你不用管。

**本地实例**（你的 `deploy-integration-checklist.md` 就是范本）：

```markdown
---
name: deploy-integration-checklist
description: 自部署+集成类任务的侦察与验证清单，避免重复踩坑
metadata:
  type: feedback
---

自部署某服务 + 集成到现有工具链时，曾因侦察不充分...

**Why:** 两个根因最贵——① 选型时用未验证的假设；② 环境侦察漏了代理变量...

**How to apply:**
1. 选型前验证核心能力...
2. 环境侦察清单：必须额外查 ALL_PROXY/HTTPS_PROXY...
   结合 [[clash-proxy]] 记忆主动排查代理。
```

> 注意 `[[clash-proxy]]` 这种链接——它把"集成清单"和"代理配置"两条小抄连起来了，下次踩代理坑时两条会一起被想起。

### 2.3 vault ingest 流程

按 vault [[CLAUDE.md]] §6 的 ingest 六步：归类 → 补 frontmatter → `_index.md` → `INDEX.md` → `CHANGELOG.md` → `git commit`。本文档本身就是一次 ingest（见文末 CHANGELOG 记录）。

---

## 3. 管理：索引·链接·去重·更新·删除

### 3.1 auto-memory 的管理

- **索引（MEMORY.md）**：一行一条，标题 + 钩子（hook）。索引是召回入口，**新条目必须加、删条目必须减**，否则索引和文件脱节。
- **链接（`[[name]]`）**：小抄本内部的网。链接要"语义相关"而非"字面同名"——`[[clash-proxy]]` 出现在 `websearch-broken-use-tavily-mcp` 和 `deploy-integration-checklist` 里，是因为它们都涉及代理，这是对的。
- **去重**：保存前必查。同一事实分散在多条里，recall 时会打架、也会让索引膨胀。
- **更新 vs 新建**：事实变了（如代理端口从 7890 换 7897），**直接改原文件**，不要新建一条"新代理"。`metadata.modified` 会自动刷新。
- **删除**：确认错的、过时的，**删文件 + 从 MEMORY.md 移除一行**。不要留尸体。

### 3.2 ⚠️ 一个关键陷阱：两套 `[[wikilink]]` 不互通

你本地有**两个独立的 wikilink 网络**：

| 网络 | 位置 | 链接锚 |
|---|---|---|
| **auto-memory 网** | `~/.claude/projects/-Users-wyf/memory/` | memory 的 `name`（如 `[[clash-proxy]]`） |
| **vault 网** | `/Users/wyf/Desktop/code/document/` | 文件名（如 `[[INDEX]]`、`[[CLAUDE.md]]`） |

**它们互相看不见**。在 vault 文档里写 `[[clash-proxy]]` 不会链到 auto-memory，反之亦然。跨层引用只能用**路径**（如"见 auto-memory 的 `clash-proxy`"），不能用 wikilink。

> 这是踩过才会记得的坑：别指望一个 `[[xxx]]` 跨层跳转。

### 3.3 vault 的管理

走 [[CLAUDE.md]] §6 的 lint 闭环：扫 orphan/stale/坏链 → 补 frontmatter → 更新 `INDEX.md` + 各 `_index.md` → `CHANGELOG.md` → commit。说「复盘 vault」即触发。

---

## 4. 治理：红线与自检

### 4.1 auto-memory 治理红线

1. **不记 repo 已有的**：代码结构、过往 fix、git history、CLAUDE.md 已写明的——记了就是噪音。
2. **不记一次性的**：只对当前对话有用的临时上下文，别让它污染小抄本。
3. **不存密钥**：token/key/密码一律不进 memory（也永远不进 vault）。
4. **四类 type 不混用**：`user` 是身份、`feedback` 是纠正（带 Why/How）、`project` 是进行中、`reference` 是指针。边界清晰才好召回。
5. **recall 是背景不是指令**：召回的 memory 反映"写入时为真"，引用其中的文件/函数/flag 前**必须验证还在不在**（记忆里 `websearch-broken-use-tavily-mcp` 就反复强调这点）。
6. **定期清尸**：过时项目状态、已废弃的工具配置，及时删。

### 4.2 ⚠️ 治理核心洞察：auto-memory 按"启动目录"隔离

**实测结论**（2026-07-22）：

```
/Users/wyf 启动 claude       -> memory 落在 -Users-wyf/memory/        （当前 20 条全在这）
~/.claude/skills/... 启动    -> 落在 -Users-wyf--claude-skills-.../   （无 memory）
其他目录启动                  -> 各自独立，互不可见
```

**这意味着**：

- 你当前所有 memory 都堆在 `-Users-wyf/memory/`，是因为你**主要在 home 目录开 claude**（呼应 [[claude-code-session-hygiene]] 记忆里说的"原习惯在 home 开会话"）。
- 如果你严格"按项目目录开 claude"（vault 目录开 vault 会话、spark 目录开 spark 会话），memory 会**分散到各项目目录**，每套独立——recall 时只看到当前项目的 memory，看不到别的项目。
- **治理选择**（你需要决策）：
  - **方案 A·集中**：继续在 home 维护一套大 memory，跨项目共享偏好/反馈。**适合**：通用工作习惯、代理配置、工具链偏好这类"跟人走"的记忆。
  - **方案 B·分散**：按项目目录开 claude，memory 随项目走。**适合**：项目专属状态（如 spark 的 Phase 进度）。
  - **推荐**：**通用记忆集中 home + 项目状态写进对应项目目录的 memory**，两头都顾。这也是 [[claude-code-session-hygiene]] 的精神。

### 4.3 vault 治理红线

见 [[CLAUDE.md]] §7：不删人写的原创正文（废弃用 `status: stale`）、重大改动先 commit 可回滚、不存密钥、LLM 维护页可自由改、人写的调研文档只补 frontmatter/wikilink 不改正文。

---

## 5. 结合外部应用（MCP/Skills）

### 5.1 双记忆协同：auto-memory × vault

这是你本地最核心的设计——**两个记忆系统各管一摊，又互相引用**：

```
   auto-memory（机器小抄）              vault（人知识库）
   ┌─────────────────┐                 ┌─────────────────┐
   │ 怎么跟你干活      │   ──路径引用──>  │ 你关心什么       │
   │ 偏好/反馈/状态    │                 │ 调研/思想/报告    │
   │ [[clash-proxy]]  │                 │ [[semiconductor]]│
   └─────────────────┘                 └─────────────────┘
        轻量·自动·跨会话                   结构化·人参与·可视化
```

- auto-memory 里的 `personal-knowledge-vault`、`paper-summaries-07-paper`、`vault-auto-fix-format` 这几条，就是**用 auto-memory 记录"vault 怎么治理"**——小抄本记规则，知识库存内容。
- 反过来 vault 文档可以用路径提到 auto-memory（不能用 wikilink，见 §3.2）。

### 5.2 外部应用 = Claude 的"延伸记忆"

你本地装的 4 个 MCP，每一个都是一种记忆延伸：

| MCP | 记的是什么 | 在记忆体系里的角色 |
|---|---|---|
| **obsidian-vault** | vault 文件 | vault 的物理通道（§1.3） |
| **tavily** | 网络信源 | "外部世界"的短期记忆（搜索即用即弃） |
| **mysql-local** | 数据库内容 | 结构化数据记忆（只读） |
| **macos-mcp** | 本机状态/操作 | 本机环境的"身体记忆"（能看屏、能点鼠标） |

**怎么把它们纳入治理**：

- **能持久化的**（vault、mysql）-> 当长期记忆用，但 vault 才需要 ingest/lint 治理。
- **即用即弃的**（tavily 搜索结果）-> 当工作记忆，不落盘，除非提炼成 vault 文档。
- **本机操作**（macos-mcp）-> 不是记忆本身，是"感知/执行"通道；操作过的东西若有价值，再落 vault 或 auto-memory。

> 一句话：**MCP 让外部数据成为 Claude 可读写的"工作记忆"，但哪些值得沉淀进长期记忆（auto-memory/vault），仍要过 §2.1 决策树。**

### 5.3 Skills 的角色

skills 不是记忆，是"**懂怎么操作记忆载体**"的技能包：

- `obsidian-markdown`：懂 Obsidian 语法（wikilink/callout/frontmatter），写 vault 文档不出错。
- `obsidian-bases`：懂 Obsidian 数据库视图，能结构化查 vault。
- `obsidian-cli`：能跟运行中的 Obsidian 实例对话（建笔记、搜内容、截图）。

记忆是"存什么"，skills 是"怎么存得对"。两者配合，Claude 才能又准又规范地维护 vault。

---

## 6. 你本地的全流程一图流

```
┌─────────────────────────────────────────────────────────────┐
│  一次会话中，Claude 要"记点东西"时：                          │
│                                                             │
│  ① 过决策树（§2.1）                                          │
│     ├─ 怎么干活 -> auto-memory                               │
│     ├─ 领域知识 -> vault ingest                              │
│     └─ repo已有/一次性/密钥 -> 不记                           │
│                                                             │
│  ② auto-memory 路径                                          │
│     查重 -> 写 frontmatter(name/description/type)+正文       │
│         (feedback/project 带 Why/How, [[链接]]相关)          │
│     -> 更新 MEMORY.md 索引 -> 系统自动补 node_type/           │
│        originSessionId/modified                             │
│     [注意落点由"启动目录"决定，见 §4.2]                       │
│                                                             │
│  ③ vault 路径                                                │
│     归类(01~08) -> 补 frontmatter -> _index.md + INDEX.md    │
│     -> CHANGELOG.md -> git commit                           │
│                                                             │
│  ④ 下次会话                                                  │
│     MEMORY.md 索引全量进上下文 -> 相关正文按需召回            │
│     (是背景,不是指令;引用前先验证)                            │
└─────────────────────────────────────────────────────────────┘

外部应用协同：
  tavily(信源) ─┐
  mysql(数据)  ─┼─> 即用即弃的工作记忆 ─> 沉淀 ─> auto-memory/vault
  macos(本机)  ─┘
  obsidian-vault MCP + 3 skills ─> vault 的读写与治理通道
```

---

## 7. 常见坑（你本地已踩或会踩的）

1. **两套 `[[wikilink]]` 当一套用**：auto-memory 的 `[[name]]` 和 vault 的 `[[文件名]]` 不互通，跨层只能用路径。见 §3.2。
2. **memory 散落到多个项目目录**：按项目开 claude 是好习惯，但 memory 会随之分散；通用偏好应集中 home。见 §4.2。
3. **把 recall 当指令执行**：召回的 memory 是"写入时为真"的背景，里面的路径/函数/flag 可能已变，**用前验证**。
4. **`description` 写得太虚**：索引行是召回唯一入口，"一些配置信息"这种描述等于没写。要写具体到能触发相关性判断（对比你的 `websearch-broken-use-tavily-mcp` 描述就很好）。
5. **新建而非更新**：事实变了去改原文件，别新建"v2"，否则索引膨胀、召回打架。
6. **vault 里存密钥**：`~/.claude.json` 和 `settings.json` 里已有 LANGFUSE/TAVILY 的 key，**绝不要复制进 vault**（vault 是 git 仓库，会提交）。
7. **feedback/project 缺 Why/How**：没这两段的 feedback 等于吐槽，下次不会用。范本见 `deploy-integration-checklist`。

---

## 8. 速查清单

**该记 auto-memory 当且仅当**：是"怎么跟你干活"的偏好/反馈/项目状态/资源指针，且 repo 没记、非一次性、非密钥。

**该 ingest vault 当且仅当**：是"你关心的领域知识"，能归入 01~08 某类，值得长期沉淀。

**写 auto-memory 必做**：查重 → name/description/type → 正文(feedback/project 带 Why/How) → `[[链接]]` → 更新 MEMORY.md。

**写 vault 必做**：归类 → frontmatter → `_index.md` → `INDEX.md` → `CHANGELOG.md` → commit。

**召回的 memory**：是背景不是指令，引用前先验证。

**两层链接**：auto-memory 用 `[[name]]`（小抄内部），vault 用 `[[文件名]]`（库内），**跨层用路径不用 wikilink**。

---

## 附：本文档的 self-check

- ✅ 三层记忆体系讲清（auto-memory / CLAUDE.md / vault）
- ✅ memory 属性须知（frontmatter 全字段 + 四种 type + recall 机制）
- ✅ 结合本地实测（20 条 memory、vault 8 类、4 个 MCP、3+ skills、按目录隔离机制）
- ✅ 结合外部应用（MCP/skills 作为延伸记忆与治理通道）
- ✅ 创建/管理/治理全流程 + 决策树 + 一图流 + 常见坑 + 速查
- ✅ 遵循 vault frontmatter 规范，落盘 06-workflows，配套更新 `_index.md`/`INDEX.md`/`CHANGELOG.md`
