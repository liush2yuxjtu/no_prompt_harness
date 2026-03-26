```text
+------------------- harness --------------------+
| ~/.claude scan | keywords | reusable patterns |
+------------------------------------------------+
```

# Harness

## Source Coverage

- 扫描数据源：
  - `~/.claude/history.jsonl`
  - `~/.claude/projects/**/*.jsonl`
- 实际发现可扫描文件总数：`1725`
- 实际做关键词统计的文件数：`1598`

## Keyword Summary

- `hook`: `304421`
- `hooks`: `73229`
- `harness`: `65421`
- `workflow`: `28280`
- `AGENTS.md`: `29595`
- `CLAUDE.md`: `4443`
- `report.md`: `25110`
- `plan.md`: `23225`

## Candidate Harness Patterns

- 先用本地 hook 做低延迟硬拦截，再用 GitHub workflow 做 PR 级别不可绕过门禁。
- 会话级状态适合承载“单文件模式”这类 Claude 本地行为约束。
- `PostCompact` / `SessionEnd` 很适合做轻量 memory 落盘，不适合重计算任务。

## Evidence Snippets

- `~/.claude/history.jsonl` 真实存在，且体量较大，说明可以作为 post-hook 证据源。
- `~/.claude/projects/**/*.jsonl` 下存在大量 `subagents/agent-*.jsonl`，说明 agent 级历史可被后续 harness 汇总利用。
- 当前环境下与 `hook`、`harness`、`workflow` 相关关键词频次都很高，适合继续沉淀可复用策略模板。

## Recommended Reusable Hooks

- `guard_bash_policy.py`: 适合横向复用到所有训练型仓库。
- `guard_single_source.py`: 适合实验仓库、论文复现仓库、单点 hotfix 仓库。
- `persist_memory.py`: 适合所有需要 compact 后保留摘要的 Claude Code 项目。
