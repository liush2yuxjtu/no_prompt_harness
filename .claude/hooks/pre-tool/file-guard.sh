#!/bin/bash
# Blocks multi-file diffusion and enforces single-file priority
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Check for multi-file write patterns in session
SESSION_FILE="/tmp/.claude_multi_file_$$"
touch "$SESSION_FILE" 2>/dev/null || SESSION_FILE="/dev/null"

# Track file creation this session
MULTI_COUNT=$(cat "$SESSION_FILE" 2>/dev/null | grep -c "$FILE_PATH" || echo 0)

# If this is a new source file, check session activity
if [ ! -f "$FILE_PATH" ] && echo "$FILE_PATH" | grep -qE '\.(py|ts|js|go|rs|java|cpp|c|h)$'; then
  TOTAL=$(cat "$SESSION_FILE" 2>/dev/null | wc -l || echo 0)
  if [ "$TOTAL" -ge 2 ]; then
    echo "Warning: Multiple new source files in session. Prefer single-file approach." >&2
    # Exit 2 to block if creating 3+ files in a session
    if [ "$TOTAL" -ge 3 ]; then
      exit 2
    fi
  fi
  echo "$FILE_PATH" >> "$SESSION_FILE"
fi

exit 0