"""Tests for dotfile manager security patterns (chezmoi, home-manager, stow)."""

import json

from tests.conftest import run_hook

# =============================================================================
# ASK PATTERNS
# =============================================================================


class TestAskChezmoi:
    """Tests for chezmoi operations that modify dotfiles on disk."""

    def test_ask_chezmoi_apply(self):
        code, stdout, _ = run_hook("Bash", {"command": "chezmoi apply"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_chezmoi_apply_with_path(self):
        code, stdout, _ = run_hook("Bash", {"command": "chezmoi apply ~/.bashrc"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_chezmoi_update(self):
        code, stdout, _ = run_hook("Bash", {"command": "chezmoi update"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_chezmoi_re_add(self):
        code, stdout, _ = run_hook("Bash", {"command": "chezmoi re-add"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_chezmoi_remove(self):
        code, stdout, _ = run_hook("Bash", {"command": "chezmoi remove ~/.config/old"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_chezmoi_forget(self):
        code, stdout, _ = run_hook("Bash", {"command": "chezmoi forget ~/.config/old"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAskHomeManager:
    """Tests for home-manager switch."""

    def test_ask_home_manager_switch(self):
        code, stdout, _ = run_hook("Bash", {"command": "home-manager switch"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_home_manager_switch_with_flake(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "home-manager switch --flake .#user"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAskStow:
    """Tests for GNU stow with delete/restow flags."""

    def test_ask_stow_delete(self):
        code, stdout, _ = run_hook("Bash", {"command": "stow -D vim"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_stow_delete_long(self):
        code, stdout, _ = run_hook("Bash", {"command": "stow --delete vim"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_stow_restow(self):
        code, stdout, _ = run_hook("Bash", {"command": "stow -R vim"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_stow_restow_long(self):
        code, stdout, _ = run_hook("Bash", {"command": "stow --restow vim"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_stow_delete_with_target(self):
        code, stdout, _ = run_hook("Bash", {"command": "stow -t ~ -D vim zsh"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


# =============================================================================
# NEGATIVE TESTS (should NOT trigger)
# =============================================================================


class TestDotfilesAllow:
    """Commands that should pass through without blocking or asking."""

    def test_allow_chezmoi_diff(self):
        code, stdout, _ = run_hook("Bash", {"command": "chezmoi diff"})
        assert code == 0
        assert stdout == ""

    def test_allow_chezmoi_status(self):
        code, stdout, _ = run_hook("Bash", {"command": "chezmoi status"})
        assert code == 0
        assert stdout == ""

    def test_allow_chezmoi_data(self):
        code, stdout, _ = run_hook("Bash", {"command": "chezmoi data"})
        assert code == 0
        assert stdout == ""

    def test_allow_chezmoi_add(self):
        code, stdout, _ = run_hook("Bash", {"command": "chezmoi add ~/.bashrc"})
        assert code == 0
        assert stdout == ""

    def test_allow_stow_without_flags(self):
        code, stdout, _ = run_hook("Bash", {"command": "stow vim"})
        assert code == 0
        assert stdout == ""

    def test_allow_home_manager_build(self):
        code, stdout, _ = run_hook("Bash", {"command": "home-manager build"})
        assert code == 0
        assert stdout == ""
