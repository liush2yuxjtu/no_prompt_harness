#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

MAX_SOURCE_LINES = 400
ALLOWED_MAIN_SOURCES = {Path("main.py")}


def repo_root() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR", Path.cwd())).resolve()


def relative_target(path_str: str) -> Path:
    root = repo_root()
    path = Path(path_str).resolve()
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def is_main_source(path: Path) -> bool:
    return path in ALLOWED_MAIN_SOURCES


def prospective_content(payload: dict) -> str:
    tool_input = payload.get("tool_input", {})
    file_path = Path(tool_input.get("file_path", ""))
    if payload.get("tool_name") == "Write":
        return tool_input.get("content", "")

    current = file_path.read_text(encoding="utf-8") if file_path.exists() else ""
    old_string = tool_input.get("old_string", "")
    new_string = tool_input.get("new_string", "")
    replace_all = bool(tool_input.get("replace_all", False))
    if replace_all:
        return current.replace(old_string, new_string)
    return current.replace(old_string, new_string, 1)


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
    if not is_main_source(target):
        return 0

    content = prospective_content(payload)
    line_count = len(content.splitlines()) or 1
    if line_count > MAX_SOURCE_LINES:
        deny(
            f"Main source files may not exceed {MAX_SOURCE_LINES} lines. "
            f"{target.as_posix()} would become {line_count} lines."
        )
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
