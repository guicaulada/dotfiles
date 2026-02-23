"""Tests for Git security patterns."""

import json

from tests.conftest import run_hook


class TestGitBlock:
    def test_block_git_reset_hard(self):
        code, _, _ = run_hook("Bash", {"command": "git reset --hard HEAD~1"})
        assert code == 2

    def test_block_git_push_force(self):
        code, _, _ = run_hook("Bash", {"command": "git push --force origin main"})
        assert code == 2

    def test_allow_git_push_force_with_lease(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "git push --force-with-lease origin main"}
        )
        # Should trigger ask (git push pattern), not block
        assert code == 0
        if stdout:
            data = json.loads(stdout)
            assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_block_git_filter_branch(self):
        code, _, _ = run_hook("Bash", {"command": "git filter-branch --all"})
        assert code == 2

    def test_block_git_checkout_force(self):
        code, _, _ = run_hook("Bash", {"command": "git checkout --force main"})
        assert code == 2

    def test_block_git_checkout_f(self):
        code, _, _ = run_hook("Bash", {"command": "git checkout -f main"})
        assert code == 2

    def test_block_git_switch_force(self):
        code, _, _ = run_hook("Bash", {"command": "git switch --force main"})
        assert code == 2

    def test_block_git_switch_f(self):
        code, _, _ = run_hook("Bash", {"command": "git switch -f main"})
        assert code == 2

    def test_block_git_submodule_deinit_force(self):
        code, _, _ = run_hook(
            "Bash", {"command": "git submodule deinit --force submod"}
        )
        assert code == 2

    def test_block_git_config_system(self):
        code, _, _ = run_hook(
            "Bash", {"command": "git config --system core.editor vim"}
        )
        assert code == 2


class TestGitAsk:
    def test_ask_git_push(self):
        code, stdout, _ = run_hook("Bash", {"command": "git push origin main"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_git_checkout_dot(self):
        code, stdout, _ = run_hook("Bash", {"command": "git checkout -- ."})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_git_stash_drop(self):
        code, stdout, _ = run_hook("Bash", {"command": "git stash drop stash@{0}"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_git_branch_force_delete(self):
        code, stdout, _ = run_hook("Bash", {"command": "git branch -D feature"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_git_revert(self):
        code, stdout, _ = run_hook("Bash", {"command": "git revert HEAD"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_git_tag_delete(self):
        code, stdout, _ = run_hook("Bash", {"command": "git tag -d v1.0.0"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_git_config_global(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "git config --global user.name 'Test'"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_git_rebase(self):
        code, stdout, _ = run_hook("Bash", {"command": "git rebase main"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_git_merge_abort(self):
        code, stdout, _ = run_hook("Bash", {"command": "git merge --abort"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_git_cherry_pick_abort(self):
        code, stdout, _ = run_hook("Bash", {"command": "git cherry-pick --abort"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_git_rebase_abort(self):
        code, stdout, _ = run_hook("Bash", {"command": "git rebase --abort"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_git_worktree_remove(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "git worktree remove /tmp/worktree"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
