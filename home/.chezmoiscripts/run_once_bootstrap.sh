#!/bin/bash
set -euo pipefail

echo "==> Bootstrapping dotfiles..."

# Install Homebrew if missing
if ! command -v brew &>/dev/null; then
  echo "==> Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Set up antidote plugins
if command -v antidote &>/dev/null; then
  echo "==> Bundling antidote plugins..."
  antidote bundle <"${HOME}/.zsh_plugins.txt" >"${HOME}/.zsh_plugins.zsh"
fi

# Install mise runtimes
if command -v mise &>/dev/null; then
  echo "==> Installing mise runtimes..."
  mise install
fi

# Set up pre-commit hooks in chezmoi repo
CHEZMOI_DIR="${HOME}/.local/share/chezmoi"
if [ -f "$CHEZMOI_DIR/.pre-commit-config.yaml" ]; then
  echo "==> Installing pre-commit hooks..."
  cd "$CHEZMOI_DIR"
  pre-commit install
fi

echo "==> Bootstrap complete!"
