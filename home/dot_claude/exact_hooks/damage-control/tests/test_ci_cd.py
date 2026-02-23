"""Tests for CI/CD, deployment, VCS non-git, and archive patterns."""

import json

from tests.conftest import run_hook


class TestCiCdBlock:
    def test_block_hg_strip(self):
        code, _, _ = run_hook("Bash", {"command": "hg strip 1234"})
        assert code == 2

    def test_block_hg_purge(self):
        code, _, _ = run_hook("Bash", {"command": "hg purge"})
        assert code == 2

    def test_block_hg_rollback(self):
        code, _, _ = run_hook("Bash", {"command": "hg rollback"})
        assert code == 2


class TestCiCdAsk:
    def test_ask_ansible_playbook(self):
        code, stdout, _ = run_hook("Bash", {"command": "ansible-playbook deploy.yml"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_ansible_adhoc(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "ansible all -m shell -a 'uptime'"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_svn_delete(self):
        code, stdout, _ = run_hook("Bash", {"command": "svn delete file.txt"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_svn_revert(self):
        code, stdout, _ = run_hook("Bash", {"command": "svn revert -R ."})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_act(self):
        code, stdout, _ = run_hook("Bash", {"command": "act push"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_unzip_overwrite(self):
        code, stdout, _ = run_hook("Bash", {"command": "unzip -o archive.zip"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
