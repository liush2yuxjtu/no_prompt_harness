```text
+---------------- exp_hard policy stack ----------------+
| GitHub policy check | local command hooks | docs only |
+------------------------------------------------------+
```

# AGENTS.md

适用范围：`/Users/m1/projects/exp_hard`。

## Hard Policy

1. 默认语言栈按 Python 单仓处理，主源码范围是 `src/**/*.py` 与根目录 `main.py`。
2. GitHub gate 优先级最高：`policy` workflow + CODEOWNERS + branch protection + required status checks。
3. 本地 command hooks 负责硬拦截：
   - 危险 Bash 命令拒绝执行
   - 训练命令必须显式包含 `timeout 300`
   - Python 主脚本严格白名单：当前只允许编辑 `main.py`
   - 主源码文件超过 `400` 行直接拒绝
   - 仅 `AGENTS.md` 与 `CLAUDE.md` 受 `200` 行限制
4. 如果以后改语言栈，必须同时更新：
   - `.claude/hooks/guard_single_source.py`
   - `.claude/hooks/guard_source_length.py`
   - `.github/workflows/policy.yml`
5. `CLAUDE.md` 只能写 `AGENTS.md`，不要复制本文件内容。

## Tunables

- `MAX_SOURCE_LINES=400`
- `MAX_RULE_DOC_LINES=200`
- `TRAIN_TIMEOUT_SECONDS=300`
- `CODEOWNER=@liush2yuxjtu`
