#!/bin/bash
# Backup transcript before auto-compaction
# Input: JSON on stdin from PreCompact hook

BACKUP_DIR="${HOME}/.claude/backups"
mkdir -p "$BACKUP_DIR"

INPUT=$(cat)
TRANSCRIPT=$(echo "$INPUT" | jq -r '.transcript_path // empty')
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

if [ -n "$TRANSCRIPT" ] && [ -f "$TRANSCRIPT" ]; then
  cp "$TRANSCRIPT" "$BACKUP_DIR/transcript_${TIMESTAMP}.jsonl"
  # Rotate: keep last 50 backups
  ls -t "$BACKUP_DIR"/transcript_*.jsonl 2>/dev/null | tail -n +51 | xargs rm -f 2>/dev/null
fi
exit 0
