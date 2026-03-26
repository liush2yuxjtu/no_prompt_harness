#!/bin/bash
# Writes session handoff / decision record
INPUT=$(cat)
SUMMARY=$(echo "$INPUT" | jq -r '.compact_summary // empty')

if [ -z "$SUMMARY" ]; then
  exit 0
fi

mkdir -p .claude/memory/handoffs
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cat > ".claude/memory/handoffs/${TIMESTAMP}.md" << EOF
# Session Handoff

**Timestamp:** ${TIMESTAMP}

## Summary
$SUMMARY

## Recent Decisions
<!-- Document key decisions made during this session -->

## Open Items
<!-- Document any remaining tasks or follow-ups -->

## File Changes
<!-- List files created or modified -->
EOF

exit 0