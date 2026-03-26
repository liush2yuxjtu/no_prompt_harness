```text
+--------------------- plan ---------------------+
| research -> hooks/workflow -> verify -> report |
+------------------------------------------------+
```

# Plan

## Overview

将“硬实现优先”模板落成一个可直接复制的 Python 版最小仓库，优先保证本地 hook 和 GitHub PR gate 都能独立工作，并把仍需人工在 GitHub 页面开启的 branch protection 明确标注出来。

## Phases

### Phase 1

- [x] 建立仓库骨架与策略入口文件
- [x] 定义主源码范围、owner、行数阈值、训练命令约束

### Phase 2

- [x] 实现 Bash command hook：危险命令 + `timeout 300`
- [x] 实现文件编辑 hook：单文件模式
- [x] 实现文件编辑 hook：主源码长度上限
- [x] 实现文件编辑 hook：规则文档长度上限
- [x] 实现 memory hook：`PostCompact` / `SessionEnd`

### Phase 3

- [x] 实现 GitHub `policy` workflow
- [x] 实现 `.github/CODEOWNERS`
- [x] 生成 `AGENTS.md` 与 `CLAUDE.md`

### Phase 4

- [x] 做静态校验与样例执行
- [x] 回填 `report.md`

## Code Snippets

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Training commands must include timeout 300."
  }
}
```

```bash
git diff --name-only origin/${BASE_REF}...HEAD
```

## Files To Modify

- `AGENTS.md`
- `CLAUDE.md`
- `.claude/settings.json`
- `.claude/hooks/*.py`
- `.github/workflows/policy.yml`
- `.github/CODEOWNERS`
- `docs/hard_policy/research.md`
- `docs/hard_policy/report.md`

## Reference Implementations

- `shandong_-shengli/.claude/settings.json`
- `shandong_-shengli/.claude/hooks/repo_lint_harness.py`
- Claude Code 官方 Hooks 文档

## Post-Hook Expectations

- `report.md` 需要明确哪些策略已经是本地硬门禁，哪些仍依赖 GitHub branch protection / required checks。
