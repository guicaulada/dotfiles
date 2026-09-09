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

Mise owns runtime versions, infrastructure tool versions, and project environments.
Homebrew runtime copies may remain as dependencies of other formulae. Keep
project-specific pins in `mise.toml`; the global pins are defaults. Review a
project's configuration before running `mise trust` and `mise install`.

Use mise's `[env]` table instead of direnv. For example, in a project's `mise.toml`:

```toml
[env]
APP_ENV = "development"
_.file = ".env"
```

The dotenv file is loaded only for projects that explicitly configure it. Keep
secrets out of version control. Existing `.envrc` files are not automatically
executed; migrate any shell logic deliberately. For noninteractive commands, use
`mise exec -- <command>` so both tools and project environment are selected.

Use uv for Python projects, virtual environments, and Python version selection
(`uv python pin`, `uv sync`, `uv run`). Project-local Python requirements take
precedence; no competing global mise Python version is configured.
