#!/bin/bash
# Auto-format and lightweight lint after Write/Edit/Bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty')

# Only run for Write/Edit tools
if [ "$TOOL" != "Write" ] && [ "$TOOL" != "Edit" ]; then
  exit 0
fi

exit 0