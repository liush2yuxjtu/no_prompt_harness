```text
+------------------- research -------------------+
| verified hooks | local gates | github gates   |
+------------------------------------------------+
```

# Research

## Architecture

- 本仓库是一个最小 Python 模板，真实硬约束分成三层：
  - GitHub: `policy` workflow + CODEOWNERS + branch protection + required status checks
  - Local: `.claude/settings.json` 绑定的 `PreToolUse` / `PostCompact` / `SessionEnd`
  - Soft: `Stop` prompt hook 与 `AGENTS.md`
- 主源码范围刻意收窄到 `src/**/*.py` 和 `main.py`，这样“单文件模式”可以明确落地。

## Verified Upstream Capability

- 2026-03-26 已核对 Claude Code 官方 Hooks 文档。
- 官方文档确认：
  - handler 支持 `command`、`http`、`prompt`、`agent`
  - 事件包含 `PreToolUse`、`InstructionsLoaded`、`FileChanged`、`PostCompact`、`SessionEnd`、`Stop`
  - `PreToolUse` 可返回 `hookSpecificOutput.permissionDecision`
  - `PostCompact` 与 `SessionEnd` 仅适合副作用任务，不能阻断流程
- 这意味着“本地先硬拦、GitHub 再最终兜底”的分层方案在能力上成立。

## Patterns And Conventions

- command hook 用 Python 脚本直接读 stdin JSON，再返回 Claude Code 规定的 JSON。
- GitHub workflow 不重复实现所有本地逻辑，只覆盖 PR 维度真正不可绕过的门禁：
  - 多主源码文件修改
  - 主源码行数超限
  - 规则文档行数超限
- CODEOWNERS 只覆盖策略面：`.claude/`、`.github/`、`AGENTS.md`、`CLAUDE.md`、`docs/rules/`。

## Potential Impact Areas

- 如果项目未来不是 Python 单仓，必须一起改 hook 和 workflow 里的主源码匹配规则。
- 单文件模式依赖会话级状态文件；它限制的是 Claude 本地会话，不等于 Git 历史级别限制。
- branch protection 和 required checks 不能通过仓库文件完全自动开启，仍需 GitHub 仓库设置配合。

## Edge Cases

- `timeout 300` 目前按命令字符串匹配，能拦住大多数训练入口，但不是 shell AST 级解析。
- `Edit` 预估行数基于字符串替换；极端复杂编辑可能与最终文件略有偏差。
- SessionEnd hook 默认超时较短，因此 memory 落盘逻辑必须保持轻量。
