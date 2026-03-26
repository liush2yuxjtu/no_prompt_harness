#!/bin/bash
# Blocks training commands without timeout or exceeding 5-minute budget
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

MAX_WALLCLOCK=300  # 5 minutes

# Check if command looks like training (contains train, fit, evaluate, etc.)
if echo "$COMMAND" | grep -qEi '(train|fit|evaluate|torchrun|python.+\.py.*train)'; then
  # Must have timeout
  if ! echo "$COMMAND" | grep -qE '(timeout|max_time|max_wallclock)'; then
    echo "Error: Training commands require a time budget (e.g., timeout 300)" >&2
    exit 2
  fi

  # Check timeout value doesn't exceed 5 minutes
  TIMEOUT_VAL=$(echo "$COMMAND" | grep -oE 'timeout\s+([0-9]+)' | grep -oE '[0-9]+')
  if [ -n "$TIMEOUT_VAL" ] && [ "$TIMEOUT_VAL" -gt "$MAX_WALLCLOCK" ]; then
    echo "Error: Training timeout ($TIMEOUT_VAL seconds) exceeds 5-minute budget" >&2
    exit 2
  fi
fi

exit 0