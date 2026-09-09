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

Pull requests run isolated validation. To test package installation and system
configuration on a disposable GitHub runner, manually run `chezmoi-validate`
with the `bootstrap` input enabled.

## Tooling

Homebrew installs the default tools from `home/.mac/Brewfile`. Specialist and
interactive utilities live in `home/.mac/Brewfile.optional` and are not installed
by `chezmoi apply`. Install an individual tool when needed, or run:

```sh
brew bundle --file=home/.mac/Brewfile.optional
```

Removing a Brewfile entry does not uninstall an existing package. Check installed
dependents before uninstalling; avoid broad bundle cleanup on a shared workstation.
