# dotfiles

Personal dotfiles managed with [chezmoi](https://www.chezmoi.io/).

## What's included

| Path | Description |
|------|-------------|
| `~/.zshrc`, `~/.zprofile` | Zsh shell configuration |
| `~/.claude/` | Claude Code rules, skills, hooks, and agents |
| `~/.config/ghostty/` | Ghostty terminal config |
| `~/.config/kitty/` | Kitty terminal config |
| `~/.config/starship.toml` | Starship prompt theme |
| `~/.config/nvim/` | Neovim config (Lazy plugin manager) |
| `~/.local/bin/` | Custom scripts (`gh-tidy`, `rebalance-shares`) |

## Setup

```sh
# Install chezmoi and apply dotfiles
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply guicaulada
```

## Usage

```sh
# Pull latest changes and apply
chezmoi update

# See what would change
chezmoi diff

# Add a new file
chezmoi add ~/.config/example/config

# Edit a managed file
chezmoi edit ~/.zshrc

# Apply changes
chezmoi apply
```
