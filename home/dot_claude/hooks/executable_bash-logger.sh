#!/bin/bash
# Log all Bash commands for audit trail
# Input: JSON on stdin from PostToolUse hook
# Output: JSONL to ~/.claude/logs/bash-commands.jsonl

LOG_DIR="${HOME}/.claude/logs"
mkdir -p "$LOG_DIR"

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if [ -n "$COMMAND" ]; then
  echo "{\"ts\":\"$TIMESTAMP\",\"cmd\":$(echo "$COMMAND" | jq -Rs .)}" >> "$LOG_DIR/bash-commands.jsonl"
fi
exit 0
