#!/usr/bin/env python3
"""Render dotfiles in isolation; never run bootstrap scripts or fetch externals."""

import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "home"
REQUIRED = {
    ".cargo/config.toml",
    ".zshenv",
    ".zprofile",
    ".zshrc",
    ".config/mise/config.toml",
    ".config/uv/uv.toml",
    ".ssh/config",
}


def validate(arch, work):
    with tempfile.TemporaryDirectory(prefix="dotfiles-validation-") as temporary:
        home = Path(temporary)
        config = home / "chezmoi.toml"
        config.write_text(
            '[data]\nname = "Test"\nemail = "test@example.com"\n'
            f"is_work = {str(work).lower()}\n"
            'company = "Example"\nwork_email = "work@example.com"\n'
        )
        env = {
            **os.environ,
            "HOME": temporary,
            "CI": "true",
            "XDG_CONFIG_HOME": str(home / ".config"),
            "XDG_CACHE_HOME": str(home / ".cache"),
            "XDG_DATA_HOME": str(home / ".local/share"),
            "XDG_STATE_HOME": str(home / ".local/state"),
        }
        command = [
            "chezmoi",
            f"--source={ROOT}",
            f"--destination={home}",
            f"--config={config}",
            f"--cache={home / 'cache'}",
            f"--persistent-state={home / 'state.boltdb'}",
            "--no-tty",
            "--refresh-externals=never",
            "--override-data",
            json.dumps({"chezmoi": {"arch": arch, "os": "darwin"}}),
        ]

        def chezmoi(*args):
            return subprocess.check_output(command + list(args), env=env, text=True)

        managed = set(chezmoi("managed", "--include=files").splitlines())
        missing = REQUIRED - managed
        if missing:
            raise RuntimeError(f"Configuration is not managed: {sorted(missing)}")
        files = sorted(SOURCE.rglob("*.tmpl"))
        for index, source in enumerate(files):
            rendered = (
                chezmoi(
                    "execute-template",
                    *(["--init"] if source.name == ".chezmoi.toml.tmpl" else []),
                    "--file",
                    str(source),
                )
                if source.suffix == ".tmpl"
                else source.read_text()
            )
            target = home / f"rendered-{index}"
            target.write_text(rendered)
            if source.name.startswith("dot_z"):
                subprocess.run(["zsh", "-n", str(target)], env=env, check=True)
            elif source.parent.name == ".chezmoiscripts" and rendered.strip():
                subprocess.run(["bash", "-n", str(target)], env=env, check=True)
                subprocess.run(["shellcheck", "--shell=bash", str(target)], env=env, check=True)
        print(f"Validated darwin/{arch}, work={work}")


if __name__ == "__main__":
    for architecture in ("arm64", "amd64"):
        for is_work in (False, True):
            validate(architecture, is_work)
