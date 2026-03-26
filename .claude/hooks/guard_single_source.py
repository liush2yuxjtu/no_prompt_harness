#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ALLOWED_MAIN_SCRIPTS = (Path("main.py"),)


def repo_root() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR", Path.cwd())).resolve()


def relative_target(path_str: str) -> Path:
    root = repo_root()
    path = Path(path_str).resolve()
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def is_python_file(path: Path) -> bool:
    return path.suffix == ".py"


def is_allowed_main_script(path: Path) -> bool:
    return path in ALLOWED_MAIN_SCRIPTS


def deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )


def main() -> int:
    payload = json.load(sys.stdin)
    target = relative_target(payload.get("tool_input", {}).get("file_path", ""))
    if not is_python_file(target):
        return 0

    if not is_allowed_main_script(target):
        deny(
            "Only listed Python scripts may be edited. "
            f"Allowed scripts: {', '.join(path.as_posix() for path in ALLOWED_MAIN_SCRIPTS)}. "
            f"Blocked target: {target.as_posix()}."
        )
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
