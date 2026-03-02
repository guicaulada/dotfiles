"""Tests for GitHub CLI (gh) security patterns."""

import json

from tests.conftest import run_hook


class TestGitHubBlock:
    """Test blocked (destructive) GitHub CLI operations."""

    # -- gh auth token / --show-token (credential exposure) ----------------

    def test_block_gh_auth_token(self):
        code, _, _ = run_hook("Bash", {"command": "gh auth token"})
        assert code == 2

    def test_block_gh_auth_token_with_hostname(self):
        code, _, _ = run_hook("Bash", {"command": "gh auth token --hostname github.com"})
        assert code == 2

    def test_block_gh_auth_status_show_token_long(self):
        code, _, _ = run_hook("Bash", {"command": "gh auth status --show-token"})
        assert code == 2

    def test_block_gh_auth_status_show_token_short(self):
        code, _, _ = run_hook("Bash", {"command": "gh auth status -t"})
        assert code == 2

    # -- gh repo delete/archive/rename ------------------------------------

    def test_block_gh_repo_delete(self):
        code, _, _ = run_hook("Bash", {"command": "gh repo delete my-repo"})
        assert code == 2

    def test_block_gh_repo_archive(self):
        code, _, _ = run_hook("Bash", {"command": "gh repo archive my-repo"})
        assert code == 2

    def test_block_gh_repo_rename(self):
        code, _, _ = run_hook("Bash", {"command": "gh repo rename new-name"})
        assert code == 2

    # -- gh release delete ------------------------------------------------

    def test_block_gh_release_delete(self):
        code, _, _ = run_hook("Bash", {"command": "gh release delete v1.0.0"})
        assert code == 2


class TestGitHubAsk:
    """Test ask-confirmation GitHub CLI operations."""

    # -- gh pr (create|merge|close|reopen|review|comment|edit|ready) ------

    def test_ask_gh_pr_create(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh pr create --title test"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_pr_merge(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh pr merge 42 --squash"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_pr_close(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh pr close 42"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_pr_reopen(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh pr reopen 42"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_pr_review(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh pr review 42 --approve"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_pr_comment(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh pr comment 42 --body 'looks good'"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_pr_edit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh pr edit 42 --title 'new title'"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_pr_ready(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh pr ready 42"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # -- gh issue (create|close|reopen|comment|edit|transfer|pin|unpin) ---

    def test_ask_gh_issue_create(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh issue create --title bug"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_issue_close(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh issue close 99"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_issue_reopen(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh issue reopen 99"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_issue_comment(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh issue comment 99 --body 'fixed'"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_issue_edit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh issue edit 99 --title 'updated'"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_issue_transfer(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh issue transfer 99 owner/other-repo"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_issue_pin(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh issue pin 99"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_issue_unpin(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh issue unpin 99"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # -- gh release (create|edit) -----------------------------------------

    def test_ask_gh_release_create(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh release create v2.0.0 --title 'Release'"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_release_edit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh release edit v2.0.0 --draft"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # -- gh repo (create|fork|edit) ---------------------------------------

    def test_ask_gh_repo_create(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh repo create my-new-repo --public"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_repo_fork(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh repo fork owner/repo --clone"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_repo_edit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh repo edit --description 'updated'"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # -- gh label (create|edit|delete) ------------------------------------

    def test_ask_gh_label_create(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh label create bug --color FF0000"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_label_edit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh label edit bug --name bugfix"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_label_delete(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh label delete obsolete --yes"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # -- gh api with write methods ----------------------------------------

    def test_ask_gh_api_dash_x_post(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh api -X POST /repos/owner/repo/issues"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_api_dash_x_put(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh api -X PUT /repos/owner/repo/topics"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_api_dash_x_patch(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh api -X PATCH /repos/owner/repo"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_api_dash_x_delete(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh api -X DELETE /repos/owner/repo/issues/1"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_api_method_post(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "gh api --method POST /repos/owner/repo/issues"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_api_method_delete(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "gh api --method DELETE /repos/owner/repo/releases/1"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # -- gh workflow (enable|disable|run) ---------------------------------

    def test_ask_gh_workflow_enable(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gh workflow enable my-workflow"}
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

    def test_ask_gh_workflow_run(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh workflow run deploy.yml"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # -- gh run (cancel|rerun|delete) -------------------------------------

    def test_ask_gh_run_cancel(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh run cancel 12345"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_run_rerun(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh run rerun 12345"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gh_run_delete(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh run delete 12345"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # -- gh secret (set|delete) -------------------------------------------

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

    # -- gh variable (set|delete) -----------------------------------------

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

    # -- gh gist create ---------------------------------------------------

    def test_ask_gh_gist_create(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh gist create file.txt"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestGitHubAllow:
    """Test that read-only GitHub CLI operations are allowed."""

    def test_allow_gh_auth_status_without_show_token(self):
        """gh auth status without --show-token should be allowed."""
        code, _, _ = run_hook("Bash", {"command": "gh auth status"})
        assert code == 0

    def test_allow_gh_pr_list(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh pr list"})
        assert code == 0
        if stdout:
            data = json.loads(stdout)
            assert data["hookSpecificOutput"]["permissionDecision"] != "ask"

    def test_allow_gh_pr_view(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh pr view 42"})
        assert code == 0
        if stdout:
            data = json.loads(stdout)
            assert data["hookSpecificOutput"]["permissionDecision"] != "ask"

    def test_allow_gh_issue_list(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh issue list"})
        assert code == 0
        if stdout:
            data = json.loads(stdout)
            assert data["hookSpecificOutput"]["permissionDecision"] != "ask"

    def test_allow_gh_issue_view(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh issue view 99"})
        assert code == 0
        if stdout:
            data = json.loads(stdout)
            assert data["hookSpecificOutput"]["permissionDecision"] != "ask"

    def test_allow_gh_repo_view(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh repo view owner/repo"})
        assert code == 0
        if stdout:
            data = json.loads(stdout)
            assert data["hookSpecificOutput"]["permissionDecision"] != "ask"

    def test_allow_gh_api_get(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh api /repos/owner/repo"})
        assert code == 0
        if stdout:
            data = json.loads(stdout)
            assert data["hookSpecificOutput"]["permissionDecision"] != "ask"

    def test_allow_gh_run_view(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh run view 12345"})
        assert code == 0
        if stdout:
            data = json.loads(stdout)
            assert data["hookSpecificOutput"]["permissionDecision"] != "ask"

    def test_allow_gh_release_view(self):
        code, stdout, _ = run_hook("Bash", {"command": "gh release view v1.0.0"})
        assert code == 0
        if stdout:
            data = json.loads(stdout)
            assert data["hookSpecificOutput"]["permissionDecision"] != "ask"
