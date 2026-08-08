---
title: "mattpocock-skills-guide"
type: workflow
date: 2026-08-08
tags: []
status: active
source: "待补"
---

# Matt Pocock Skills 使用指南

> 来源：https://github.com/mattpocock/skills（189k stars，Matt Pocock）
> 安装方式：**Claude Code plugin**（user scope，已装）+ skills.sh（可选，可改）

## 是什么

22 个"工程纪律型" skill，把经典软件工程实践（Pragmatic Programmer / DDD / TDD / XP）封装成 AI agent 可执行的复用流程。**不是 vibe coding**，是给真实工程用的。

设计理念：解决 AI 编程的 4 大失败模式：
1. **agent 没做我想要的**（对齐问题）-> `/grill-me` `/grill-with-docs` 深度问答对齐
2. **agent 太啰嗦**（共享语言缺失）-> `CONTEXT.md` 术语表
3. **代码不工作**（反馈循环缺失）-> `/tdd` 红绿重构 `/diagnosing-bugs` 调试循环
4. **代码变成泥球**（架构腐化）-> `/to-spec` `/improve-codebase-architecture`

## 安装状态（已完成）

```bash
claude plugin marketplace add mattpocock/skills        # ✔ 已添加
claude plugin install mattpocock-skills@mattpocock     # ✔ user scope 已装
```

- 装在 user scope，**所有项目都能用**（不是某项目专属）
- **重启 Claude Code 后生效**（plugin 加载）
- plugin 是只读托管，随作者更新；想改源码用 `npx skills@latest add mattpocock/skills`（skills.sh，复制到 ~/.agents/skills）

## 配置（每个仓库一次）

重启 Claude Code 后，在你要用的项目里运行：
```
/setup-matt-pocock-skills
```
它会问：
1. **issue 追踪器**：GitHub / Linear / 本地文件
2. **triage 标签**：你 triage issue 时用的标签
3. **docs 保存位置**：CONTEXT.md / ADR 等存哪

## 22 个 Skill 清单

### Engineering（17 个）

**用户调用型**（你输命令触发，负责编排）：

| Skill | 作用 |
|---|---|
| `/ask-matt` | 路由入口：问"我该用哪个 skill" |
| `/grill-with-docs` | **核心**：深度问答对齐 + 构建 CONTEXT.md/ADR（最推荐） |
| `/triage` | issue triage 状态机流转 |
| `/improve-codebase-architecture` | 扫架构改进点，出 HTML 报告（每隔几天跑） |
| `/setup-matt-pocock-skills` | 仓库初始化配置 |
| `/to-spec` | 当前对话 -> 规格文档发到 issue 追踪器 |
| `/to-tickets` | 计划/规格 -> tracer-bullet 票据集（带阻塞依赖） |
| `/implement` | 按规格/票据实现，接缝处 /tdd，提交前 /code-review |
| `/wayfinder` | 超大工作规划共享调查票据地图 |

**模型调用型**（agent 自动触发，承载纪律）：

| Skill | 作用 |
|---|---|
| `prototype` | 一次性原型答设计问题 |
| `diagnosing-bugs` | 硬 bug 诊断循环：复现->最小化->假设->插桩->修复->回归 |
| `research` | 高信任度一手来源调研，带引用 markdown |
| `tdd` | 红绿重构，垂直切片 |
| `domain-modeling` | 构建锐化领域模型，更新 CONTEXT.md |
| `codebase-design` | 深度模块设计：行为藏小接口后 |
| `code-review` | 双轴审查：Standards（编码标准）+ Spec（忠实原意） |
| `resolving-merge-conflicts` | 逐 hunk 解决冲突，绝不 --abort |

### Productivity（5 个）

| Skill | 作用 |
|---|---|
| `/grill-me` | 非代码场景的严厉访谈对齐（最受欢迎） |
| `/handoff` | 当前对话压缩成交接文档给下个 agent |
| `/teach` | 跨会话教学，当前目录作教学工作区 |
| `/writing-great-skills` | 编写 skill 的参考文档 |
| `grilling` | grill-me/grill-with-docs 背后的可复用循环 |

## 场景 SOP（核心）

### 场景 1：开发新功能 / 改动（主流程）
```
/grill-with-docs     # 先对齐：agent 反问你的意图，建 CONTEXT.md
  -> /to-spec        # 对齐后出规格文档
  -> /to-tickets     # 拆成 tracer-bullet 票据（带依赖）
  -> /implement      # 按票据实现，自动在接缝处 /tdd，提交前 /code-review
```
**心法**：先 grill 对齐再写码，别上来就 implement。

### 场景 2：非代码计划 / 设计对齐
```
/grill-me            # 严厉访谈，决策树每分支问到底（调研/可视化/飞书 bot 设计前用）
```

### 场景 3：修硬 bug / 性能回归
```
/diagnosing-bugs     # 复现 -> 最小化 -> 假设 -> 插桩 -> 修复 -> 回归测试
  -> /tdd            # 修复时红绿重构
```

### 场景 4：代码审查
```
/code-review         # 双轴并行：Standards（编码标准）+ Spec（忠实原 issue）
```

### 场景 5：架构改进（定期）
```
/improve-codebase-architecture   # 扫模块深化机会，出 HTML 报告
  -> /grill-with-docs            # 选定改进项深度问答
```
每隔几天跑一次，防泥球。

### 场景 6：超大工作（超单会话容量）
```
/wayfinder           # 规划共享调查票据地图，逐一解决
  -> /to-tickets -> /implement
```

### 场景 7：跨会话交接
```
/handoff             # 压缩当前对话成交接文档，下个 agent 接着干
```

### 场景 8：merge / rebase 冲突
```
/resolving-merge-conflicts    # 逐 hunk 按双方原始意图解决，不 --abort
```

### 场景 9：不知道用哪个
```
/ask-matt            # 路由：告诉它你的情况，它推荐 skill
```

## 最佳实践

1. **每次改动前先 grill**：`/grill-with-docs`（代码）或 `/grill-me`（非代码）。对齐意图比写码快。
2. **维护 CONTEXT.md**：项目专属术语表，压缩啰嗦描述，命名一致，省 token。这是"最酷的技巧"。
3. **`/implement` 是主入口**：它编排 `/tdd`（接缝处测试）+ `/code-review`（提交前审查），不要手动跳过。
4. **定期 `/improve-codebase-architecture`**：agent 加速编码也加速熵增，定期扫架构防泥球。
5. **组合用**：用户调用型编排（你触发），模型调用型执行（agent 自动）。用户调用型**不能**调用户调用型，只能调模型调用型。
6. **`/tdd` 红绿重构**：一次一个垂直切片，别一次写一大坨。
7. **`/code-review` 双轴**：Standards（Fowler 异味基线）+ Spec（忠实原意）并行子代理，互不污染。

## 注意事项

- **重启 Claude Code 生效**：plugin 装好后要重启会话，skill 才加载。
- **`/setup-matt-pocock-skills` 每仓库跑一次**：配 issue 追踪器/标签/docs 位置。不跑则 triage/to-spec/to-tickets 无法对接追踪器。
- **plugin 只读**：不能改源码。要定制用 `npx skills@latest add mattpocock/skills`（skills.sh 复制可改），但两套别混装。
- **skill 调用规则**：用户调用型可调模型调用型，**不可调用户调用型**（防递归编排）。
- **CONTEXT.md / ADR 要维护**：grill-with-docs 会内联更新，但你要 review，别让术语表跑偏。
- **issue 追踪器集成**：GitHub/Linear/本地文件。本地文件模式不依赖追踪器，适合个人项目。
- **和现有 skill 共存**：你已装 arkcli/lark/superpowers 等，mattpocock 是工程纪律类，不冲突。`/ask-matt` 路由时不认识你的领域 skill，需自己判断。
- **Codex 不支持 plugin**：plugin 是 Claude Code 专属。Codex 要用 skills.sh 方式装（`npx skills@latest add`）。

## 适合你的工作流吗

| 你的场景 | 用哪个 | 契合度 |
|---|---|---|
| 写代码（spark 湖仓/Java） | `/grill-with-docs` -> `/implement` -> `/code-review` | 高 |
| 调研（半导体/算力） | `/research` 或 `/grill-me`（对齐调研框架） | 中（你有自己的调研工作流，可能重复） |
| 飞书 bot / Handy 这类集成 | `/grill-me` 对齐需求 -> `/implement` | 中 |
| 可视化/视频 | `/grill-me` 对齐 -> `/prototype` 原型 | 中 |
| 跨会话多项目 | `/handoff` 交接 | 高 |
| 修 bug | `/diagnosing-bugs` -> `/tdd` | 高 |

**核心价值**：grill 系列强制对齐 + CONTEXT.md 共享语言，治"agent 没做我想要的"和"太啰嗦"。你做技术工作多，这俩痛点你应该常遇到。

**不直接适合**：飞书 bot 已装好（不需 skill）、Handy 已配好、arkcli/lark 是领域 skill（mattpocock 不覆盖）。

## 快速验证（重启 Claude Code 后）

1. 重启 Claude Code
2. 在某项目跑 `/setup-matt-pocock-skills`（选 issue 追踪器、标签、docs 位置）
3. 试 `/ask-matt` 问"我想加个功能 X"，看它路由到哪个 skill
4. 或直接 `/grill-me` 对齐一个你正在想的需求，体验严厉访谈
