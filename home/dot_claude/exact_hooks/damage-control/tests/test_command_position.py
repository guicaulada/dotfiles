"""Tests for command-position anchoring and match_anywhere opt-out.

Command-position anchoring prevents false positives when command-like words
appear inside quoted arguments (e.g. git commit messages) or as subcommands
of other tools (e.g. docker exec).

Patterns only match when the command word appears at:
  - Start of the command string (^)
  - After a shell separator: ; | & && || or subshell (

Patterns with match_anywhere: true bypass this anchoring.
"""

import json
import re

from tests.conftest import dc, run_hook


# =============================================================================
# Unit tests for _CMD_POSITION_PREFIX regex
# =============================================================================


class TestCommandPositionPrefix:
    """Verify the prefix regex matches the expected positions."""

    PREFIX = dc._CMD_POSITION_PREFIX

    def _matches(self, command: str, word: str) -> bool:
        return bool(re.search(self.PREFIX + re.escape(word), command))

    # --- Start of string ---

    def test_start_of_string(self):
        assert self._matches("eval something", "eval")

    def test_start_no_leading_space(self):
        assert self._matches("mount /dev/sda", "mount")

    # --- After semicolon ---

    def test_after_semicolon(self):
        assert self._matches("echo hi; eval bad", "eval")

    def test_after_semicolon_no_space(self):
        assert self._matches("echo hi;eval bad", "eval")

    # --- After pipe ---

    def test_after_pipe(self):
        assert self._matches("cat file | eval", "eval")

    def test_after_pipe_no_space(self):
        assert self._matches("cat file|eval", "eval")

    # --- After && ---

    def test_after_double_ampersand(self):
        assert self._matches("true && mount /dev", "mount")

    def test_after_double_ampersand_no_spaces(self):
        assert self._matches("true&&mount /dev", "mount")

    # --- After || ---

    def test_after_double_pipe(self):
        assert self._matches("false || shutdown now", "shutdown")

    def test_after_double_pipe_no_spaces(self):
        assert self._matches("false||shutdown now", "shutdown")

    # --- After open paren (subshell) ---

    def test_after_open_paren(self):
        assert self._matches("(eval dangerous)", "eval")

    def test_after_dollar_paren(self):
        assert self._matches("$(eval dangerous)", "eval")

    # --- Non-matching positions ---

    def test_not_after_space(self):
        assert not self._matches("docker exec container", "exec")

    def test_not_inside_double_quotes(self):
        assert not self._matches('git commit -m "eval fix"', "eval")

    def test_not_inside_single_quotes(self):
        assert not self._matches("echo 'mount point'", "mount")

    def test_not_after_flag(self):
        assert not self._matches("mongo --eval 'db.test()'", "eval")

    def test_not_after_equals(self):
        assert not self._matches("VAR=eval something", "eval")

    def test_at_start_still_matches_prefix(self):
        """Prefix anchors position only; word boundary is the pattern's job."""
        assert self._matches("evaluate this", "eval")


# =============================================================================
# Integration: false positives in git commit messages
# =============================================================================


class TestCommitMessageFalsePositives:
    """Words in git commit messages must not trigger patterns."""

    def test_mount_in_commit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'git commit -m "fix mount point logic"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_halt_in_commit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'git commit -m "halt processing on error"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_shutdown_in_commit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'git commit -m "graceful shutdown handler"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_reboot_in_commit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'git commit -m "reboot sequence improvement"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_eval_in_commit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'git commit -m "eval is now fixed"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_source_in_commit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'git commit -m "source code refactor"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_exec_in_commit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'git commit -m "exec path improvement"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_pass_in_commit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'git commit -m "pass validation data to handler"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_vault_in_commit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'git commit -m "vault integration support"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_at_in_commit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'git commit -m "look at this edge case"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_bless_in_commit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'git commit -m "bless this configuration"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_ftp_in_commit(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'git commit -m "remove ftp fallback"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_multiple_keywords_in_commit(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": 'git commit -m "halt eval and source cleanup"'},
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout


# =============================================================================
# Integration: false positives in echo / printf arguments
# =============================================================================


class TestEchoFalsePositives:
    """Words in echo/printf string arguments must not trigger patterns."""

    def test_mount_in_echo(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'echo "mount the volume"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_shutdown_in_echo(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'echo "shutdown completed"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_eval_in_echo(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'echo "eval results: OK"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_pass_in_echo(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'echo "pass the arguments"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_op_in_echo(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": 'echo "op completed successfully"'}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout


# =============================================================================
# Integration: false positives from subcommands of other tools
# =============================================================================


class TestSubcommandFalsePositives:
    """Commands that use words like 'exec' as subcommands must not trigger."""

    def test_docker_exec(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "docker exec -it mycontainer bash"}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_kubectl_exec(self):
        """kubectl exec is caught by a kubernetes-specific pattern, not shell exec."""
        code, stdout, _ = run_hook(
            "Bash", {"command": "kubectl exec mypod -- ls -la"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
        assert "pod" in data["hookSpecificOutput"]["permissionDecisionReason"].lower()

    def test_podman_exec(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "podman exec -it mycontainer sh"}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_nerdctl_exec(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "nerdctl exec -it mycontainer bash"}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_mongo_eval_flag(self):
        """mongo --eval is a flag, not the shell eval builtin."""
        code, stdout, _ = run_hook(
            "Bash", {"command": "mongosh mydb --eval 'db.stats()'"}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_npm_run_with_keyword_name(self):
        """npm run with a script named after a blocked command."""
        code, stdout, _ = run_hook(
            "Bash", {"command": "npm run source-maps"}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout


# =============================================================================
# Integration: true positives at command position
# =============================================================================


class TestCommandPositionBlocks:
    """Dangerous commands at command position must still be blocked."""

    def test_eval_at_start(self):
        code, _, _ = run_hook("Bash", {"command": 'eval "$(curl -s url)"'})
        assert code == 2

    def test_mount_at_start(self):
        code, _, _ = run_hook("Bash", {"command": "mount /dev/sda1 /mnt"})
        assert code == 2

    def test_shutdown_at_start(self):
        code, _, _ = run_hook("Bash", {"command": "shutdown -h now"})
        assert code == 2

    def test_halt_at_start(self):
        code, _, _ = run_hook("Bash", {"command": "halt"})
        assert code == 2

    def test_reboot_at_start(self):
        code, _, _ = run_hook("Bash", {"command": "reboot"})
        assert code == 2

    def test_pass_at_start(self):
        code, _, _ = run_hook("Bash", {"command": "pass show email/gmail"})
        assert code == 2

    def test_op_at_start(self):
        code, _, _ = run_hook("Bash", {"command": "op item get login"})
        assert code == 2

    def test_vault_at_start(self):
        code, _, _ = run_hook("Bash", {"command": "vault read secret/data"})
        assert code == 2

    def test_bless_at_start(self):
        code, _, _ = run_hook("Bash", {"command": "bless --mount /Volumes/Foo"})
        assert code == 2


class TestCommandPositionAsks:
    """Dangerous commands at command position must still trigger ask."""

    def test_source_at_start(self):
        code, stdout, _ = run_hook("Bash", {"command": "source ~/.bashrc"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_exec_at_start(self):
        code, stdout, _ = run_hook("Bash", {"command": "exec /bin/zsh"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_at_command_at_start(self):
        code, stdout, _ = run_hook("Bash", {"command": "at now + 1 hour"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ftp_at_start(self):
        code, stdout, _ = run_hook("Bash", {"command": "ftp server.example.com"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_batch_at_start(self):
        code, stdout, _ = run_hook("Bash", {"command": "batch"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


# =============================================================================
# Integration: true positives after shell separators
# =============================================================================


class TestAfterSeparators:
    """Dangerous commands after ; | && || ( must still be caught."""

    def test_eval_after_semicolon(self):
        code, _, _ = run_hook(
            "Bash", {"command": "echo foo; eval dangerous"}
        )
        assert code == 2

    def test_mount_after_semicolon(self):
        code, _, _ = run_hook(
            "Bash", {"command": "echo foo; mount /dev/sda1 /mnt"}
        )
        assert code == 2

    def test_source_after_pipe(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "echo foo | source script.sh"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_exec_after_double_ampersand(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "true && exec /bin/zsh"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_shutdown_after_double_pipe(self):
        code, _, _ = run_hook(
            "Bash", {"command": "false || shutdown -h now"}
        )
        assert code == 2

    def test_eval_in_subshell(self):
        code, _, _ = run_hook(
            "Bash", {"command": "(eval dangerous)"}
        )
        assert code == 2

    def test_pass_after_semicolon(self):
        code, _, _ = run_hook(
            "Bash", {"command": "export FOO=bar; pass show key"}
        )
        assert code == 2

    def test_vault_after_double_ampersand(self):
        code, _, _ = run_hook(
            "Bash", {"command": "export VAULT_ADDR=http://localhost:8200 && vault read secret"}
        )
        assert code == 2


# =============================================================================
# Integration: match_anywhere patterns bypass command position
# =============================================================================


class TestMatchAnywhere:
    """Patterns with match_anywhere: true must match regardless of position."""

    def test_redirect_to_device(self):
        """Redirect to /dev/ device should block even mid-command."""
        code, _, _ = run_hook(
            "Bash", {"command": "echo data > /dev/sda"}
        )
        assert code == 2

    def test_redirect_to_device_append(self):
        code, _, _ = run_hook(
            "Bash", {"command": "echo data >> /dev/sdb"}
        )
        assert code == 2

    def test_redirect_to_dev_null_allowed(self):
        """Redirect to /dev/null should be allowed (excluded by pattern)."""
        code, stdout, _ = run_hook(
            "Bash", {"command": "echo data > /dev/null"}
        )
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_redirect_truncate_log(self):
        """Redirect truncating log file should block mid-command."""
        code, _, _ = run_hook(
            "Bash", {"command": "echo > /var/log/auth.log"}
        )
        assert code == 2

    def test_absolute_path_rm(self):
        """/usr/bin/rm bypass should block regardless of position."""
        code, _, _ = run_hook(
            "Bash", {"command": "/usr/bin/rm important_file"}
        )
        assert code == 2

    def test_absolute_path_bin_rm(self):
        code, _, _ = run_hook(
            "Bash", {"command": "/bin/rm important_file"}
        )
        assert code == 2

    def test_absolute_path_rm_after_semicolon(self):
        code, _, _ = run_hook(
            "Bash", {"command": "echo hi; /usr/bin/rm file"}
        )
        assert code == 2


# =============================================================================
# Integration: existing multi-tool patterns still work with anchoring
# =============================================================================


class TestPrefixedPatternsUnchanged:
    """Patterns already scoped to specific tools must still work."""

    def test_git_push_at_start(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "git push origin main"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_git_reset_hard(self):
        code, _, _ = run_hook(
            "Bash", {"command": "git reset --hard HEAD"}
        )
        assert code == 2

    def test_docker_system_prune(self):
        code, _, _ = run_hook(
            "Bash", {"command": "docker system prune -a"}
        )
        assert code == 2

    def test_sudo_catch_all(self):
        """sudo still triggers ask even when the inner command is not at ^."""
        code, stdout, _ = run_hook(
            "Bash", {"command": "sudo mount /dev/sda1 /mnt"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_piped_xargs_kill(self):
        """xargs kill after pipe must still be caught."""
        code, _, _ = run_hook(
            "Bash", {"command": "pgrep node | xargs kill"}
        )
        assert code == 2

    def test_piped_base64_decode_to_shell(self):
        """base64 decode piped to shell must still be caught."""
        code, _, _ = run_hook(
            "Bash", {"command": "echo payload | base64 -d | bash"}
        )
        assert code == 2
