#!/bin/bash
# Saves PostCompact summary to memory/compacts/
INPUT=$(cat)
SUMMARY=$(echo "$INPUT" | jq -r '.compact_summary // empty')

if [ -z "$SUMMARY" ]; then
  exit 0
fi

mkdir -p .claude/memory/compacts
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo "$SUMMARY" > ".claude/memory/compacts/${TIMESTAMP}.md"

# Update index
echo "- [${TIMESTAMP}](.claude/memory/compacts/${TIMESTAMP}.md)" >> .claude/memory/index.md 2>/dev/null || true

exit 0