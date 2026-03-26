#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys

TRAIN_TIMEOUT_SECONDS = 300
DANGEROUS_PATTERNS = [
    (r"(^|[;&|]\s*)rm\s+-rf\s+(/|\*)", "Blocked dangerous recursive delete."),
    (r"\bsudo\s+rm\s+-rf\b", "Blocked privileged recursive delete."),
    (r"\bgit\s+reset\s+--hard\b", "Blocked destructive git reset."),
    (r"\bgit\s+checkout\s+--\b", "Blocked destructive checkout restore."),
    (r"\bgit\s+clean\s+-fdx?\b", "Blocked destructive git clean."),
    (r"\bmkfs(\.\w+)?\b", "Blocked filesystem formatting command."),
    (r"\bdd\s+.*\bof=/dev/", "Blocked raw device overwrite command."),
    (r"\b(shutdown|reboot|poweroff)\b", "Blocked machine shutdown command."),
]
TRAIN_PATTERNS = [
    r"\btorchrun\b",
    r"\bdeepspeed\b",
    r"\baccelerate\s+launch\b",
    r"\bpython3?\s+[^;\n]*\btrain[\w./-]*\.py\b",
    r"\bbash\s+[^;\n]*\btrain[\w./-]*\.sh\b",
]


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
    command = payload.get("tool_input", {}).get("command", "")

    for pattern, reason in DANGEROUS_PATTERNS:
        if re.search(pattern, command):
            deny(reason)
            return 0

    is_training = any(re.search(pattern, command) for pattern in TRAIN_PATTERNS)
    has_timeout = re.search(r"\btimeout\s+300\b", command) is not None
    if is_training and not has_timeout:
        deny(f"Training commands must include `timeout {TRAIN_TIMEOUT_SECONDS}`.")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
