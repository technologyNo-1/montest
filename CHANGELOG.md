# 维护日志 CHANGELOG

> LLM Wiki 操作记录，按时间倒序。每次 ingest/lint 追加一条。

## 2026-07-18 · 首次 vault 化整理

**操作**：将杂散文档目录重组为 Obsidian vault + LLM Wiki。

- 整体备份 `document` -> `document.bak.20260719-050444`
- `git init` + `.gitignore`（排除 `.DS_Store` / `.obsidian` 机器状态）
- 按 6 类重组 57 个内容文件：
  - `01-people/`（19）· `02-industry/`（6）· `03-ai-token/`（12）· `04-tech/`（12）· `05-career/`（6）· `06-workflows/`（2）
- 删除 0B 空文件 `ai_token_data_verification.md`（`token/` 内有同名实质文件）
- 修复 `README_agent3.md` 的 4 个失效 `../` 链接（文件已同目录）
- 写 LLM Wiki 维护层：`CLAUDE.md` / `INDEX.md` / `CHANGELOG.md` / `README.md` / 6×`_index.md`
- frontmatter 标准化：核心文档全量 + 其余脚本批量打底

**已完成**：
- ✅ 装 Obsidian 1.12.7（brew --cask）并指向 document vault
- ✅ 配 filesystem MCP server（`obsidian-vault`，写入 `~/.claude.json`，重启 CC 生效）
- ✅ 装 obsidian-skills（kepano 官方 5 skills：defuddle / json-canvas / obsidian-bases / obsidian-cli / obsidian-markdown）

## 2026-07-18 · 首次 lint

**检查结果**：
- frontmatter 覆盖率：54/54 内容文档 = 100%
- 坏链：无（`../` 与 `[[文件名]]` 仅为规则文本，非实际链接）
- 分类：6 类 57 内容文件归位
- git 提交：6 次

**待办（用户侧）**：
- [ ] 在 Obsidian GUI 点 "Trust author and enable plugins" 信任 document vault（生成 `.obsidian`）
- [ ] 重启 Claude Code 使 filesystem MCP（`obsidian-vault`）生效
- [ ] 后续说「复盘 vault」触发深度 lint（通读全库完善 INDEX 人物关系网）
