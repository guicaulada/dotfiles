#!/bin/bash
# Verify chezmoi source matches the live system after changes
# This runs whenever chezmoi source state changes

echo "==> Verifying dotfiles..."

if chezmoi verify 2>/dev/null; then
  echo "==> Dotfiles are in sync."
else
  echo "==> Drift detected! Run 'chezmoi diff' to see changes, 'chezmoi apply' to fix."
fi
