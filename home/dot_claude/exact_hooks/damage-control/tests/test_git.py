"""Tests for Git security patterns."""

import json

from tests.conftest import run_hook


class TestGitBlock:
    """Tests for git operations that should be blocked (exit code 2)."""

    # --- git reset --hard ---

    def test_block_git_reset_hard(self):
        code, _, _ = run_hook("Bash", {"command": "git reset --hard HEAD~1"})
        assert code == 2

    def test_block_git_reset_hard_no_ref(self):
        code, _, _ = run_hook("Bash", {"command": "git reset --hard"})
        assert code == 2

    # --- git clean with force/directory flags ---

    def test_block_git_clean_f(self):
        code, _, _ = run_hook("Bash", {"command": "git clean -f"})
        assert code == 2

    def test_block_git_clean_fd(self):
        code, _, _ = run_hook("Bash", {"command": "git clean -fd"})
        assert code == 2

    def test_block_git_clean_df(self):
        code, _, _ = run_hook("Bash", {"command": "git clean -df"})
        assert code == 2

    def test_block_git_clean_force(self):
        code, _, _ = run_hook("Bash", {"command": "git clean --force"})
        assert code == 2

    def test_block_git_clean_xfd(self):
        code, _, _ = run_hook("Bash", {"command": "git clean -xfd"})
        assert code == 2

    def test_block_git_clean_d(self):
        code, _, _ = run_hook("Bash", {"command": "git clean -d"})
        assert code == 2

    def test_allow_git_clean_dry_run(self):
        """git clean -n (dry run) should NOT be blocked."""
        code, _, _ = run_hook("Bash", {"command": "git clean -n"})
        assert code == 0

    # --- git push --force (consolidated pattern) ---

    def test_block_git_push_force(self):
        code, _, _ = run_hook("Bash", {"command": "git push --force origin main"})
        assert code == 2

    def test_block_git_push_f(self):
        code, _, _ = run_hook("Bash", {"command": "git push -f origin main"})
        assert code == 2

    def test_block_git_push_force_trailing(self):
        code, _, _ = run_hook("Bash", {"command": "git push origin main --force"})
        assert code == 2

    def test_block_git_push_f_trailing(self):
        code, _, _ = run_hook("Bash", {"command": "git push origin main -f"})
        assert code == 2

    def test_allow_git_push_force_with_lease(self):
        """--force-with-lease should trigger ask (git push), not block."""
        code, stdout, _ = run_hook(
            "Bash", {"command": "git push --force-with-lease origin main"}
        )
        assert code == 0
        if stdout:
            data = json.loads(stdout)
            assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git stash clear ---

    def test_block_git_stash_clear(self):
        code, _, _ = run_hook("Bash", {"command": "git stash clear"})
        assert code == 2

    # --- git reflog expire ---

    def test_block_git_reflog_expire(self):
        code, _, _ = run_hook("Bash", {"command": "git reflog expire --all"})
        assert code == 2

    def test_block_git_reflog_expire_unreachable(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "git reflog expire --expire=now --all"},
        )
        assert code == 2

    # --- git gc --prune=now ---

    def test_block_git_gc_prune_now(self):
        code, _, _ = run_hook("Bash", {"command": "git gc --prune=now"})
        assert code == 2

    def test_block_git_gc_aggressive_prune_now(self):
        code, _, _ = run_hook("Bash", {"command": "git gc --aggressive --prune=now"})
        assert code == 2

    # --- git filter-branch/repo (consolidated) ---

    def test_block_git_filter_branch(self):
        code, _, _ = run_hook("Bash", {"command": "git filter-branch --all"})
        assert code == 2

    def test_block_git_filter_repo(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "git filter-repo --invert-paths --path secret"},
        )
        assert code == 2

    # --- git checkout/switch --force (consolidated) ---

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

    # --- git submodule deinit --force ---

    def test_block_git_submodule_deinit_force(self):
        code, _, _ = run_hook(
            "Bash", {"command": "git submodule deinit --force submod"}
        )
        assert code == 2

    # --- git config --system ---

    def test_block_git_config_system(self):
        code, _, _ = run_hook(
            "Bash", {"command": "git config --system core.editor vim"}
        )
        assert code == 2

    # --- git update-ref -d ---

    def test_block_git_update_ref_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "git update-ref -d refs/heads/feature"}
        )
        assert code == 2


class TestGitAsk:
    """Tests for git operations that should prompt for confirmation (ask)."""

    # --- git push (general) ---

    def test_ask_git_push(self):
        code, stdout, _ = run_hook("Bash", {"command": "git push origin main"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git checkout -- . ---

    def test_ask_git_checkout_dot(self):
        code, stdout, _ = run_hook("Bash", {"command": "git checkout -- ."})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git restore . ---

    def test_ask_git_restore_dot(self):
        code, stdout, _ = run_hook("Bash", {"command": "git restore ."})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git stash drop ---

    def test_ask_git_stash_drop(self):
        code, stdout, _ = run_hook("Bash", {"command": "git stash drop stash@{0}"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git branch -D ---

    def test_ask_git_branch_force_delete(self):
        code, stdout, _ = run_hook("Bash", {"command": "git branch -D feature"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git push --delete ---

    def test_ask_git_push_delete(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "git push origin --delete feature"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git push :branch (old delete syntax) ---

    def test_ask_git_push_colon_branch(self):
        code, stdout, _ = run_hook("Bash", {"command": "git push origin :feature"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git revert ---

    def test_ask_git_revert(self):
        code, stdout, _ = run_hook("Bash", {"command": "git revert HEAD"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git tag -d ---

    def test_ask_git_tag_delete(self):
        code, stdout, _ = run_hook("Bash", {"command": "git tag -d v1.0.0"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git tag -f ---

    def test_ask_git_tag_force(self):
        code, stdout, _ = run_hook("Bash", {"command": "git tag -f v1.0.0"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git notes remove/prune ---

    def test_ask_git_notes_remove(self):
        code, stdout, _ = run_hook("Bash", {"command": "git notes remove HEAD"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_git_notes_prune(self):
        code, stdout, _ = run_hook("Bash", {"command": "git notes prune"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git config --global ---

    def test_ask_git_config_global(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "git config --global user.name 'Test'"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git remote remove/rm ---

    def test_ask_git_remote_remove(self):
        code, stdout, _ = run_hook("Bash", {"command": "git remote remove upstream"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_git_remote_rm(self):
        code, stdout, _ = run_hook("Bash", {"command": "git remote rm upstream"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git remote set-url ---

    def test_ask_git_remote_set_url(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "git remote set-url origin https://example.com/repo"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git fetch --prune ---

    def test_ask_git_fetch_prune(self):
        code, stdout, _ = run_hook("Bash", {"command": "git fetch --prune origin"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_git_fetch_origin_prune(self):
        code, stdout, _ = run_hook("Bash", {"command": "git fetch origin --prune"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git rebase ---

    def test_ask_git_rebase(self):
        code, stdout, _ = run_hook("Bash", {"command": "git rebase main"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- git merge/cherry-pick/rebase --abort ---

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

    # --- git worktree remove ---

    def test_ask_git_worktree_remove(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "git worktree remove /tmp/worktree"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestGitAllow:
    """Tests for git operations that should be allowed (not blocked or asked)."""

    def test_allow_git_status(self):
        code, stdout, _ = run_hook("Bash", {"command": "git status"})
        assert code == 0
        assert not stdout  # No ask output

    def test_allow_git_log(self):
        code, stdout, _ = run_hook("Bash", {"command": "git log --oneline"})
        assert code == 0
        assert not stdout

    def test_allow_git_diff(self):
        code, stdout, _ = run_hook("Bash", {"command": "git diff"})
        assert code == 0
        assert not stdout

    def test_allow_git_add(self):
        code, stdout, _ = run_hook("Bash", {"command": "git add file.txt"})
        assert code == 0
        assert not stdout

    def test_allow_git_branch_list(self):
        code, stdout, _ = run_hook("Bash", {"command": "git branch -a"})
        assert code == 0
        assert not stdout

    def test_allow_git_clean_dry_run(self):
        code, stdout, _ = run_hook("Bash", {"command": "git clean -n"})
        assert code == 0
        assert not stdout

    def test_allow_git_stash(self):
        code, stdout, _ = run_hook("Bash", {"command": "git stash"})
        assert code == 0
        assert not stdout

    def test_allow_git_stash_list(self):
        code, stdout, _ = run_hook("Bash", {"command": "git stash list"})
        assert code == 0
        assert not stdout
