"""Tests for GitHub CLI (gh) security patterns."""

import json

from tests.conftest import run_hook


class TestGitHubBlock:
    def test_block_gh_repo_delete(self):
        code, _, _ = run_hook("Bash", {"command": "gh repo delete my-repo"})
        assert code == 2


class TestGitHubAsk:
    def test_ask_gh_pr_create(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh pr create --title test"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_issue_create(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh issue create --title bug"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_api_post(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh api -X POST /repos/owner/repo/issues"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_workflow_disable(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh workflow disable my-workflow"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_run_cancel(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh run cancel 12345"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_secret_set(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh secret set MY_SECRET"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_secret_delete(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh secret delete MY_SECRET"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_variable_set(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh variable set MY_VAR --body value"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_variable_delete(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh variable delete MY_VAR"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_gist_create(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh gist create file.txt"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
