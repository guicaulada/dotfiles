"""Tests for privilege escalation (sudo, su, doas) catch-all patterns."""

import json

from tests.conftest import run_hook


class TestCatchAll:
    def test_ask_sudo_generic(self):
        code, stdout, _ = run_hook("Bash", {"command": "sudo ls /root"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_su(self):
        code, stdout, _ = run_hook("Bash", {"command": "su - root"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_doas(self):
        code, stdout, _ = run_hook("Bash", {"command": "doas ls /root"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
