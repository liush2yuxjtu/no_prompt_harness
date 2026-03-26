```text
+-------------------- report --------------------+
| implemented | verified locally | github manual |
+------------------------------------------------+
```

# Report

## Executive Summary

- 已在 `exp_hard` 实现一套最小可复制的硬策略模板。
- 本地 command hooks 已覆盖危险命令、训练超时、单文件模式、源码行数、规则文档行数、memory 落盘。
- GitHub 侧已提供 `policy` workflow 与 CODEOWNERS；branch protection / required checks 仍需在仓库设置页手动打开。

## Files Modified

- `AGENTS.md`
- `CLAUDE.md`
- `.claude/settings.json`
- `.claude/hooks/guard_bash_policy.py`
- `.claude/hooks/guard_single_source.py`
- `.claude/hooks/guard_source_length.py`
- `.claude/hooks/guard_doc_size.py`
- `.claude/hooks/persist_memory.py`
- `.github/workflows/policy.yml`
- `.github/CODEOWNERS`
- `.gitignore`
- `src/app.py`
- `docs/hard_policy/research.md`
- `docs/hard_policy/plan.md`
- `docs/hard_policy/report.md`
- `docs/hard_policy/review.md`
- `docs/hard_policy/harness.md`

## Verification

- [x] `python3 -m json.tool .claude/settings.json`
- [x] `python3 -m py_compile .claude/hooks/*.py src/app.py`
- [x] Bash hook sample: `rm -rf /tmp/demo` denied
- [x] Bash hook sample: `python train.py --epochs 1` denied without `timeout 300`
- [x] Edit hook sample: second source file denied in same session
- [x] Source length sample: `src/app.py` at 401 lines denied
- [x] Rule doc sample: `AGENTS.md` at 201 lines denied
- [x] Memory hook sample: writes JSON into `.claude/memory/`

## Verification Notes

- `guard_bash_policy.py` returned Claude Code compatible `permissionDecision: deny` JSON for both dangerous delete and missing-timeout training command.
- `guard_single_source.py` allowed the first write to `src/app.py` and denied the second write to `src/other.py` in the same fake session.
- `guard_source_length.py` denied a synthetic 401-line `src/app.py`.
- `guard_doc_size.py` denied a synthetic 201-line `AGENTS.md`.
- `persist_memory.py` wrote a JSON record under `.claude/memory/`.

## Risks

- GitHub branch protection 和 required status checks 只能在仓库设置里启用，仓库文件本身无法替代。
- 训练命令识别采用模式匹配，不是完整 shell 解析器。

## Follow-up

- 在 GitHub 仓库设置中把 `policy` 设为 required status check。
- 为 `main` 分支打开 branch protection，并要求 CODEOWNERS review。
