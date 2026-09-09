# github.com/guicaulada/dotfiles

Personal dotfiles, managed with [`chezmoi`](https://github.com/twpayne/chezmoi).

Install them with:

```sh
chezmoi init guicaulada
```

Personal secrets are stored in [1Password](https://1password.com), and you'll
need the [1Password CLI](https://developer.1password.com/docs/cli/) installed.

Validate templates locally without applying settings or installing packages:

```sh
python3 scripts/validate-dotfiles.py
```

Requires `chezmoi`, `zsh`, `bash`, and `shellcheck`. Validation covers personal and
work configurations on both Apple Silicon and Intel Macs.
