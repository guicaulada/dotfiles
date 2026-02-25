# Dotfiles

[![lint](https://github.com/guicaulada/dotfiles/actions/workflows/lint.yml/badge.svg)](https://github.com/guicaulada/dotfiles/actions/workflows/lint.yml)
[![test](https://github.com/guicaulada/dotfiles/actions/workflows/test.yml/badge.svg)](https://github.com/guicaulada/dotfiles/actions/workflows/test.yml)
[![chezmoi-validate](https://github.com/guicaulada/dotfiles/actions/workflows/chezmoi-validate.yml/badge.svg)](https://github.com/guicaulada/dotfiles/actions/workflows/chezmoi-validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Personal development environment managed with [chezmoi](https://github.com/twpayne/chezmoi).

This repository bootstraps and maintains shell, editor, Git, and tooling configuration with reproducible templates and change hooks.

## Highlights

- Chezmoi-managed dotfiles with templating and host-aware data.
- Automated bootstrap scripts for Homebrew packages and runtime setup.
- Zsh stack with antidote, starship, zoxide, direnv, and mise.
- Git defaults with SSH commit signing via 1Password.
- Neovim, tmux, Ghostty, and CLI tooling configuration.
- CI with linting, policy checks, and template validation.

## Prerequisites

- macOS is the primary target (Linux may work for non-macOS-specific files).
- [chezmoi](https://www.chezmoi.io/) `2.48.1+` (see `.chezmoiversion`).
- [1Password CLI](https://developer.1password.com/docs/cli/) for secrets and Git signing key resolution.
- Git and a shell (`zsh` assumed by default config).

Optional but recommended:

- Homebrew (auto-installed by chezmoi hook on macOS if missing).
- `uv` for running the Python test suite under `home/dot_claude/exact_hooks/damage-control`.

## Quick Start

### 1. Install chezmoi

```sh
brew install chezmoi
```

### 2. Initialize and apply

```sh
chezmoi init --apply guicaulada
```

During first apply, chezmoi prompts for:

- Full name
- Email address
- Whether this is a work machine
- Company/work email (if work machine)

### 3. Verify

```sh
chezmoi doctor
chezmoi diff
```

## Secrets and Signing

- Secrets are resolved through 1Password references.
- Git uses SSH signing and expects the signing key reference at:
  `op://Private/SSH Key/public key`
- On macOS, signing is configured to use:
  `/Applications/1Password.app/Contents/MacOS/op-ssh-sign`

If your vault path differs, adjust `home/.chezmoidata/defaults.yaml` and related templates.

## Day-to-Day Usage

```sh
# Pull and apply latest dotfiles
chezmoi update

# Review pending changes before applying
chezmoi diff

# Apply local source changes
chezmoi apply

# Edit a managed file from target path
chezmoi edit ~/.zshrc
```

## Repository Layout

```text
.
|-- home/
|   |-- .chezmoi.toml.tmpl           # prompts/data model
|   |-- .chezmoidata/defaults.yaml   # defaults and paths
|   |-- .chezmoiscripts/             # post-change automation hooks
|   |-- dot_config/                  # XDG app configs (nvim, tmux, etc.)
|   |-- dot_zshrc.tmpl               # shell setup
|   `-- dot_gitconfig.tmpl           # git identity/signing defaults
|-- .github/workflows/               # CI checks
|-- .pre-commit-config.yaml          # local quality gates
`-- README.md
```

## Development and Validation

Run checks locally before opening a PR:

```sh
pre-commit run --all-files
```

Run the `damage-control` tests directly:

```sh
cd home/dot_claude/exact_hooks/damage-control
uv run --with pytest --with pytest-xdist --with pyyaml pytest tests/ -v -n auto
```

CI also runs:

- mega-linter
- zizmor (GitHub Actions security checks)
- chezmoi template initialization/apply validation
- pytest suite for damage-control hooks

## Contributing

Issues and PRs are welcome for improvements that keep the setup reproducible and secure.

Typical flow:

```sh
git checkout -b docs/your-change
pre-commit run --all-files
git commit -m "docs: improve README"
git push -u origin docs/your-change
```

## License

[MIT](LICENSE)
