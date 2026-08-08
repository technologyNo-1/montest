Claude Code 的 continual learning（持续学习）指的是 Claude Code 通过 **CLAUDE.md 文件（你写给 Claude 的持久化指令）+ Auto memory（Claude 自己写给自己的学习笔记）+ `.claude/rules/`（按文件路径作用域加载的规则）+ Skills（按需调用的任务流程）+ Subagent（隔离上下文的子代理）** 这套机制，让一个"每次会话从空白上下文开始"的模型能够跨会话、跨任务地积累项目知识、个人偏好和踩坑教训，从而越用越贴合你的代码库与工作习惯。它的设计哲学是：**把"每次都要重新解释一遍的东西"沉淀成可被 Claude 在会话启动时读取的结构化记忆，让模型在生成第一个 token 之前就已经完成"如何操作"的关键决策**【turn0search0】【turn0search2】。

下面分机制对照、解决问题、融入工作流、场景最佳实践、进阶设计五个模块展开。

---

## 一、机制对照：Claude Code 的记忆体系全景

官方文档明确把记忆分成两套互补系统，二者都在每次会话启动时加载，但 Claude 把它们当作"上下文"而非"强制配置"——也就是说写得越具体、越精简，遵循度越高【turn0search0】。

| 机制 | 谁写 | 存放位置 | 加载时机 | 适用内容 | 共享范围 |
|---|---|---|---|---|---|
| **Managed policy CLAUDE.md** | IT/DevOps | `/Library/Application Support/ClaudeCode/CLAUDE.md`（macOS）等 | 每次会话最先加载，不可被覆盖 | 公司编码标准、安全策略、合规要求 | 全机器所有用户 |
| **User CLAUDE.md** | 你个人 | `~/.claude/CLAUDE.md` | 每次会话启动 | 个人代码风格偏好、跨项目工具快捷方式 | 仅你（所有项目） |
| **Project CLAUDE.md** | 团队 | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 每次会话启动，随 Git 提交 | 项目架构、构建命令、编码标准、常见工作流 | 团队成员 |
| **CLAUDE.local.md** | 你个人 | `./CLAUDE.local.md`（加入 `.gitignore`） | 跟随 Project CLAUDE.md 之后 | 个人沙箱 URL、本地测试数据 | 仅你（当前项目） |
| **`.claude/rules/*.md`（无 paths）** | 团队/你 | `.claude/rules/` | 每次会话启动 | 模块化拆分的主题规则 | 同 Project |
| **`.claude/rules/*.md`（带 paths 前置元数据）** | 团队/你 | `.claude/rules/` | Claude 读取匹配路径文件时按需加载 | 只对 `src/api/**/*.ts` 生用的 API 规则 | 同 Project |
| **Auto memory（MEMORY.md + 主题文件）** | Claude 自己 | `~/.claude/projects/<project>/memory/` | MEMORY.md 前 200 行或 25KB 每次启动加载；主题文件按需读取 | 构建命令、调试洞察、架构笔记、Claude 发现的偏好 | 仅本机本仓库（含所有 worktree） |
| **Skills** | 你/Claude | `.claude/skills/` | 仅在你调用或 Claude 判定相关时加载 | 多步骤任务流程、一次性 Procedure | 同 Project |
| **Subagent memory** | Claude 子代理 | 子代理独立目录 | 子代理被调用时 | 子代理任务范围内的学习 | 仅该子代理 |
| **Hooks** | 你 | `.claude/settings.json` | 生命周期事件（PreToolUse、PostToolUse 等）硬执行 | "提交前必须跑 lint""改文件后必须 format"等强制规则 | 同 Project |

几个关键设计点值得记住：

- **CLAUDE.md 是"上下文"不是"配置"**。它以用户消息形式注入，放在系统提示之后，Claude 会尽力遵循但不保证严格合规。需要"无论 Claude 怎么想都必须执行"的规则（比如禁止改某文件、提交前必须跑测试），应该用 Hook 而不是 CLAUDE.md【turn0search0】。
- **`@path/to/import` 递归导入**，最多 4 跳，相对路径以"包含 import 的那个文件"为基准。反引号包裹的 `` `@README` `` 不会被导入，利用这点可以提及路径而不实际加载【turn0search0】。
- **CLAUDE.md 从工作目录向上遍历到根**，所有命中文件"拼接"而非"覆盖"，越靠近工作目录的越后读（优先级越高）；同目录内 `CLAUDE.local.md` 永远在 `CLAUDE.md` 之后【turn0search0】。
- **Auto memory 的 MEMORY.md 是索引**，主题文件（`debugging.md`、`api-conventions.md`）按需读取。超过 200 行/25KB 阈值后，超出部分下次启动直接丢弃，Claude Code 会要求 Claude 重写索引【turn0search0】。
- **`/context`** 查看本次实际加载了哪些记忆文件，**`/memory`** 浏览/编辑/开关 auto memory，**`/doctor`**（v2.1.206+）会建议裁剪 CLAUDE.md 中可由代码库推断的内容【turn0search0】。

---

## 二、它解决的核心问题

Claude Code 的根本约束是"每次会话从空白上下文窗口开始"。这带来三类高频痛点，continual learning 各有对应：

**1. 重复对齐成本**。每次新会话都要重新解释"我们用 pnpm 不用 npm""API 测试需要本地 Redis""这个仓库的 monorepo 结构是 packages/* 下每个包独立 tsconfig"。CLAUDE.md + Auto memory 让这些事实只说一次，之后每次会话自动加载【turn0search0】【turn0search1】。

**2. 踩坑不沉淀**。Claude 在 session A 踩了"用 `fs.readFileSync` 读大文件导致 OOM"的坑，到 session B 同样的代码库又会重蹈覆辙。Auto memory 让 Claude 自己把"读大文件用 stream"这类洞察写进 `debugging.md`，下次自动读取【turn0search0】【turn0search1】。

**3. 上下文腐烂**。长会话里模型注意力被稀释，开始忘记早期决策、重复已被否定的方案。continual learning 的真正价值在于**把"会话内的工作记忆"外化成"跨会话的持久记忆"**，配合 `/compact`、`/clear`、`/rewind`、subagent 等上下文管理手段，让每次会话都从"已知项目全貌"的干净状态出发，而不是把所有历史塞进一个不断膨胀的窗口【turn0search8】【turn4search7】。

一句话：continual learning 把"AI 的记忆"从"单次会话的 token 窗口"升级成"随项目演进的工程知识库"。

---

## 三、如何融入自己的工作流

### 1. 新项目冷启动：用 `/init` 但不要全盘接受

运行 `/init`（或设 `CLAUDE_CODE_NEW_INIT=1` 启用多阶段交互流），让 Claude 分析代码库后生成 CLAUDE.md 草稿、skills、hooks 的提案。但草稿里通常混入了大量"模型能从代码库自行推断"的内容（目录结构、依赖列表、架构概览），这些应该删掉——保留 Claude 无法自行发现的：构建命令、约定、反模式、rationale【turn0search0】。

建议的初始 CLAUDE.md 骨架（控制在 200 行以内）：

```markdown
# <项目名>
一句话项目定位。

## 构建 / 测试 / lint
- `pnpm install`、`pnpm -F web dev`、`pnpm test`、`pnpm lint`
- 测试需要本地 Redis：`docker run -d -p 6379:6379 redis`

## 架构约定
- Monorepo，packages/* 下每个包独立 tsconfig，引用其他包用 workspace:*
- API 层在 src/api/handlers/，每个 handler 一个文件，导出 POST/GET 工厂
- 数据库迁移走 prisma，禁止手写 SQL 改 schema

## 编码规范
- 用 2 空格缩进；禁止 any，必须用 unknown + 类型守卫
- 错误响应统一用 { code, message, details } 结构
- 提交前必须跑 `pnpm test && pnpm lint`

## 反模式（不要做）
- 不要用 fs.readFileSync 读 >1MB 文件，用 createReadStream
- 不要在 React 组件里直接调 prisma，走 server actions

## 决策偏好
- 优先可读性而非过度抽象；简单重复 > 复杂抽象
- 改动涉及 src/billing/ 时先用 plan mode
```

### 2. 日常沉淀：让 Claude 帮你维护记忆

把这三句话变成肌肉记忆：

- **"把这条加到 CLAUDE.md"**——当 Claude 第二次犯同样的错、Code Review 抓到它本该知道的事、你打出和上次一样的纠正语时，直接让它写入项目 CLAUDE.md【turn0search0】。
- **"记住 API 测试需要本地 Redis"**——这类事实性偏好会进 Auto memory 的 MEMORY.md【turn0search0】。
- **"重新整理一下记忆：去重、删过时、合并同类、按日期排序"**——定期让 Claude 清理 MEMORY.md，保持索引精简【turn0search5】。

### 3. 任务前：先对齐全貌再动手

复杂任务不要直接 "帮我实现 X"。推荐的开场模板：

```
先读 CLAUDE.md 和相关模块的代码，不要改任何文件。
用 plan mode 给我一个方案，包含：
1. 涉及哪些文件、为什么
2. 你识别到的约束和潜在风险
3. 你打算分几步、每步的验收标准
4. 你不确定、需要我决策的点
```

Plan mode 产出的方案是一个写到 plans 文件夹的 markdown 文件，你可以审阅、修改、否决后再让它执行【turn4search10】【turn4search12】。这一步的价值在于：**让 Claude 在动手前把"任务全貌"显式化，你能在错误成本最低的点纠偏**。一个 .NET 开发者的反面教训是"直接让 Claude 给所有实体加软删除"，结果改了 14 个文件、引入破坏性全局过滤器、 migration 历史冲突，回滚花了 30 分钟——同样的需求用 plan mode 先规划可以完全避免【turn4search13】。

### 4. 任务中：主动管理上下文

| 信号 | 动作 | 原因 |
|---|---|---|
| 同一任务、上下文还有效 | 继续 | 窗口里都是承重内容 |
| Claude 走错路 | `/rewind` 回到读文件之后、错误尝试之前 | 保留有用的文件读取，丢掉失败尝试 |
| 上下文被调试噪音撑爆 | `/compact focus on <当前任务>` | 让模型在还清醒时生成摘要 |
| 真正的新任务 | `/clear` + 贴 3-5 行 brief | 零腐烂，完全控制带入新会话的内容 |
| 下一步会产生大量无用输出 | 让 subagent 去做 | 中间噪音留在子上下文，只回收结论 |
| 上下文用到 ~70%（约 600K token） | 主动 `/compact` | 别等 auto-compact 在模型最弱时触发【turn0fetch0】 |

### 5. 任务后：写 handoff brief

会话结束前让 Claude 写一份交接简报：**做了什么、还剩什么、约束是什么、相关文件有哪些**。把这份 brief 存进 CLAUDE.md、repo 里的 scratch 文件，或直接作为下一会话的第一条消息。长项目跨多会话的连续性就靠这个 pattern 维系【turn0fetch0】。

### 6. 治理：定期审计

- **CLAUDE.md 季度审**：跑 `/doctor` 看裁剪建议，删掉代码库能推断的内容，更新过时模式。6 个月未编辑的 CLAUDE.md 比没有记忆更糟，因为它在教模型做团队早已不这么做的事【turn0fetch1】。
- **Skills 季度退役**：硬上限 ~20 个，按调用量淘汰低于阈值的【turn0fetch1】。
- **权限季度审**：`permissions.allow` 列表会随时间漂移到过度授权【turn0fetch1】。
- **Auto memory 月度浏览**：`/memory` 打开 auto memory 文件夹，看看 Claude 自己记了什么，删掉它误记或过时的【turn0search0】。

---

## 四、经典场景的最佳实践

### 场景 A：接手大型遗留代码库

**痛点**：上下文窗口装不下整个代码库，Claude 容易基于通用假设乱改，破坏隐式约定。

**最佳实践**：
1. 先跑 `/init` 生成草稿，然后人工大刀阔斧裁剪到 <200 行，重点写"反模式"和"为什么这么设计"——这两类是 Claude 无法从代码自行推断的【turn0search0】【turn0fetch1】。
2. 用 `.claude/rules/` 按模块拆分：`rules/legacy-php.md` 带 `paths: ["legacy/**/*.php"]`，`rules/api.md` 带 `paths: ["src/api/**/*.ts"]`。这样老 PHP 代码的怪约定不会污染到新 API 的上下文【turn0search0】。
3. 接手第一步任务前，让 Claude 用 plan mode 先"通读 + 输出理解"，**你审阅它的理解是否正确再放行**。这比直接让它改代码安全得多。
4. 复杂调查任务派给 subagent：让它读完整个模块、总结出"数据流、副作用、隐式契约"再返回结论，主会话只拿结论不背噪音【turn0fetch0】。
5. 边接手边把踩到的坑写进 CLAUDE.md 的"反模式"段，让后续会话自动避坑。

### 场景 B：团队协作下统一 AI 行为规范

**痛点**：每个人各自维护一份 prompt，Claude 在不同人手里行为不一致，Code Review 经常抓"早该知道"的问题。

**最佳实践**：
1. **三级层次清晰分工**：Managed policy 放安全/合规（IT 维护）、User CLAUDE.md 放个人偏好（不进 Git）、Project CLAUDE.md 放团队标准（进 Git，是 Code Review 的依据）【turn0search0】【turn0search9】。
2. **Project CLAUDE.md 用 Git 管理 + PR review**：任何修改走 PR，让团队看到"AI 行为规范"的变更。这把"隐性 prompt"变成了"显性工程契约"。
3. **复用其他 agent 的规则**：仓库已有 `AGENTS.md`，用 `@AGENTS.md` 导入而非复制；`/init` 会自动读取 Cursor、Copilot、Windsurf、Cline 的规则并入【turn0search0】。
4. **强制规则用 Hook 不用 CLAUDE.md**：比如"提交前必须跑 lint""禁止改 `.env`"，写成 PreToolUse hook，无论 Claude 怎么想都硬执行【turn0search0】。
5. **组织级统一部署**：用 MDM/Ansible 把 Managed CLAUDE.md 推到所有开发机，确保安全策略不可被个人 settings 覆盖【turn0search0】。
6. **监控三个行为指标**（而非 license 占用率）：subagent 调用量/活跃用户、skill 调用量/活跃用户、CLAUDE.md 行数趋势——这才是"真正被采用"的信号【turn0fetch1】。

### 场景 C：长周期项目的上下文管理

**痛点**：跨天、跨周的项目里，单会话必然腐烂；硬塞所有历史进上下文会撑爆窗口。

**最佳实践**：
1. **任务文件作为上下文锚点**：复杂任务先写一个 `auth-refactor.task` 或 `.plan` 文件，描述任务、约束、验收标准。每次新会话第一句："follow the plan in auth-refactor.task"。Claude 每次重新读，比塞进对话历史稳定【turn0fetch0】。
2. **Handoff brief 跨会话**：每次会话结束让 Claude 写交接简报（做了什么/剩什么/约束/相关文件），存进 CLAUDE.md 或 scratch 文件，下一会话首条消息贴它【turn0fetch0】。
3. **主动 `/compact`**：在 ~600K token（约 70% 窗口）时手动 compact 并给 focus 提示，比等 auto-compact 在模型最弱时触发质量高得多【turn0fetch0】【turn4search9】。
4. **Subagent 隔离重活**：验证实现是否符合 spec、读另一个代码库总结 auth 模式、跑大批量测试——派给 subagent，中间噪音留在子上下文，主会话只收结论【turn0fetch0】。
5. **`/rewind` 而非纠正**：Claude 走错路时，回退到错误之前重新 prompt，比追加"那样不对，试试 X"保持上下文更干净【turn0fetch0】。
6. **里程碑后更新 CLAUDE.md**：每个大阶段结束，把"新建立的架构事实""新发现的反模式"沉淀进 CLAUDE.md，让记忆随项目演进。

---

## 五、进阶：与 Claude 协同理解任务全貌与决策

这一层是 continual learning 的"高阶用法"——不是单纯写记忆文件，而是设计一套**你与 Claude 共建决策上下文**的协作模式。

### 1. Plan-first：让 Claude 先"复述任务"再动手

把"生成代码"拆成两阶段：**理解阶段**（plan mode，只读不写，输出对任务的理解、约束、风险、分步方案、待决策点）和**执行阶段**（你审批后才动手）。这强迫 Claude 在最低成本的时刻暴露它对任务的理解偏差，而你能在它写一行代码之前纠偏【turn4search10】【turn4search12】【turn4search13】。

关键 prompt 设计：

```
进入 plan mode。读 CLAUDE.md、相关模块、相关测试。
输出：
1. 你理解的任务目标（用你自己的话复述，不要照抄我的）
2. 你识别到的隐式约束（代码库里没写但实际存在的）
3. 2-3 个候选方案，各自的权衡（不要只给一个）
4. 你倾向哪个、为什么
5. 你不确定、需要我拍板的点
```

### 2. 显式暴露决策点

不要让 Claude 默默替你做架构决策。在 plan 里要求它列出"待决策点"，把**决策权交还给你**。这比事后发现它选了你不想要的方案再回滚高效得多。一个常见误区是让 Claude"自由发挥"做软删除这类横切改动，结果 14 个文件被改坏——本质就是没在 plan 阶段暴露"要不要全局过滤器""哪些表需要"等决策点【turn4search13】。

### 3. 把决策结果沉淀回记忆

每次你做了一个决策（"选方案 A 不选 B，因为 X""这个模块禁止用 Y 模式"），立刻让 Claude 写进 CLAUDE.md 的"决策偏好"或"反模式"段。下次类似任务，Claude 会自动读取并遵循，不需要你重复解释。这是 continual learning 闭环的关键一环：**决策 → 沉淀 → 自动加载 → 影响下次决策**。

### 4. 用 Subagent 做"第二意见"

主会话里 Claude 给了方案后，派一个 subagent："独立评估这个方案，找出三个最可能出问题的点"。子代理在隔离上下文里不受主会话已达成共识的影响，能给出更批判的视角。这种"主代理执行 + 子代理 review"的模式比单线信任更稳【turn0fetch0】。

### 5. 记忆分层 + 按需加载

不要把所有知识堆进 CLAUDE.md。分层原则：

- **每次会话都要知道**（构建命令、核心约定、顶级反模式）→ CLAUDE.md，<200 行
- **特定文件类型/模块才需要**（API 设计规范、测试约定）→ `.claude/rules/` 带 paths，按需加载
- **多步骤流程才需要**（部署流程、发布检查表）→ Skills，调用时加载
- **Claude 自己发现的**（调试洞察、偏好）→ Auto memory，自动管理

这样每会话启动时的上下文负担最小，模型遵循度最高。研究表明 CLAUDE.md 过 500 行模型就开始"略读"，过 1000 行行为不可预测【turn0fetch1】。

### 6. 记忆去重与版本化

定期让 Claude 执行"记忆整理"流程：读所有记忆文件 → 去重 → 删过时 → 合并同类 → 拆分过宽的文件 → 按日期排序 → 更新 MEMORY.md 索引 → 输出变更摘要【turn0search5】。CLAUDE.md 纳入 Git 管理后，每次修改有 diff、有 PR、有 review 历史——这是"团队级 continual learning"区别于"个人 prompt 碎片"的本质。

### 7. Hook 兜底关键约束

Claude 可能"忘记"读 CLAUDE.md 的某条规则。对**不可妥协**的约束（提交前跑测试、禁止改生产配置、敏感文件只读），用 PreToolUse/PostToolUse hook 硬执行。Hook 是 shell 命令，在生命周期事件触发，**无论 Claude 怎么决定都执行**——这是 CLAUDE.md（行为引导）与 Hook（硬性约束）的分工【turn0search0】。

---

## 反模式提醒

几个高频踩坑值得警惕：

- **把 CLAUDE.md 当 README 写**，塞目录结构、依赖列表、架构概览——这些 Claude 读代码就知道，纯属浪费上下文 token 并降低遵循度。`/doctor` 会主动建议删这类内容【turn0search0】。
- **Auto memory 当万能记忆库**，什么都说"记住这个"——MEMORY.md 超 200 行/25KB 后超出部分直接丢弃，且 auto memory 是本机本仓库的，不跨机器、不进 Git，团队协作场景下不能依赖它传递知识【turn0search0】。
- **只加不删**——CLAUDE.md、skills、权限列表都在持续膨胀，没有季度退役机制就会沦为噪音。Digital Applied 审计的真实案例里，50 个 skill 的库实际只用 6 个，其余全是开销【turn0fetch1】。
- **忽视上下文管理**——再好的 CLAUDE.md 也救不了腐烂的会话。长会话必须在 ~70% 窗口时主动 `/compact`，跨会话必须写 handoff brief【turn0fetch0】。
- **把 CLAUDE.md 当强制配置**——它是上下文不是配置，模糊或矛盾的指令 Claude 会任意选一个遵循。需要硬执行就用 Hook【turn0search0】。
- **个人偏好写进 Project CLAUDE.md**——会污染团队所有人的上下文。个人偏好放 `CLAUDE.local.md`（gitignore）或 `~/.claude/CLAUDE.md`【turn0search0】。

continual learning 的本质是把"AI 的记忆"从"单次会话的临时状态"升级为"随项目演进的工程资产"。写得好，Claude 越用越懂你的代码库；写得差，它要么忘事要么被噪音淹没。关键不是记忆多，而是**记忆精、分层清、定期审、决策回写闭环**。