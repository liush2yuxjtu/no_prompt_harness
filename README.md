# No-Prompt Harness: Claude Code Policy Enforcement Template

A reusable template repository implementing the "hard enforcement first" philosophy for Claude Code agent governance.

## Features

This template enforces:
1. **Filesystem as memory** - Memory indexing and session summaries
2. **5-minute training budget** - Hard wall-clock timeout on training commands
3. **AGENTS.md > 200 lines triggers review** - Line count gates
4. **Single file priority** - Multi-file creation restrictions
5. **Progressive disclosure** - Context management rules

## Directory Structure

```
.claude/
  hooks/
    pre-tool/
      bash-trainer-guard.sh    # Block training cmds without timeout
      file-guard.sh           # Block multi-file diffusion
    post-tool/
      lint-format.sh          # Auto-format hook
    file-changed/
      rules-size-check.sh     # Warn/block if AGENTS.md > 200 lines
    post-compact/
      save-summary.sh         # Write compact summaries
    session-end/
      write-handoff.sh        # Write session handoff
    stop/
      completion-check.sh     # Semantic completion check
  memory/
    compacts/                 # Compact summaries
    handoffs/                 # Session handoffs
    index.md                  # Memory index
.github/
  workflows/
    policy.yml                # CI policy checks
  CODEOWNERS                  # Path-based ownership
```

## Setup

1. Copy these files into your repository
2. Make hook scripts executable:
   ```bash
   find .claude/hooks -name "*.sh" -exec chmod +x {} \;
   ```
3. Configure branch protection in GitHub:
   - Require status checks: `policy-single-file`, `policy-line-limits`, `policy-agents-md-size`, `policy-training-time-budget`
   - Require CODEOWNERS review for `.github/`, `.claude/`, `AGENTS.md`, `CLAUDE.md`
   - Enable "Dismiss stale reviews"

## Hooks Reference

| Hook | Trigger | Purpose |
|------|---------|---------|
| `bash-trainer-guard.sh` | PreToolUse/Bash | Enforce timeout on training commands |
| `file-guard.sh` | PreToolUse/Write\|Edit | Block multi-file diffusion |
| `lint-format.sh` | PostToolUse | Auto-format after writes |
| `rules-size-check.sh` | FileChanged | Warn if rules > 200 lines |
| `save-summary.sh` | PostCompact | Persist compact summaries |
| `write-handoff.sh` | SessionEnd | Write session handoffs |
| completion-check | Stop | Semantic completion verification |

## CI Jobs

| Job | Purpose |
|-----|---------|
| `policy-single-file` | Max 3 new source files per PR |
| `policy-line-limits` | Files must be < 500 lines |
| `policy-agents-md-size` | AGENTS.md must be < 200 lines |
| `policy-training-time-budget` | Training scripts need timeout |
| `policy-memory-artifacts` | Memory files follow naming |

## Verification

1. **Local hook testing**: Run `.claude/hooks/pre-tool/bash-trainer-guard.sh` manually with various inputs
2. **CI verification**: The workflow runs on every PR; check Actions tab
3. **Branch protection**: Attempt to merge PR without passing checks (should fail)
4. **CODEOWNERS**: Create PR touching `.claude/` - should auto-request review

## References

- [Claude Code Hooks](https://code.claude.com/docs/en/hooks.md)
- [GitHub Actions](https://docs.github.com/actions)
- [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
# no_prompt_harness
