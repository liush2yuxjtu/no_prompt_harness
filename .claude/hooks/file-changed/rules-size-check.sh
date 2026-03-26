#!/bin/bash
# Warns if AGENTS.md or rule files exceed 200 lines
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.path // empty')

if [ -z "$FILE" ]; then
  exit 0
fi

LINE_COUNT=$(wc -l < "$FILE" 2>/dev/null || echo 0)

if [ "$LINE_COUNT" -gt 200 ]; then
  echo "Warning: $FILE has $LINE_COUNT lines (limit: 200). Consider refactoring." >&2
  # Exit 2 to block - optional, use exit 0 for warning only
  exit 2
fi

exit 0