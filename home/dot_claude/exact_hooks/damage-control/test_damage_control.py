"""Tests for damage_control.py — comprehensive coverage."""

from __future__ import annotations

import io
import json
import os
import re

import pytest
import yaml

from damage_control import (
    _BUILTIN_SHORTHANDS,
    _CMD_POSITION_PREFIX,
    _block,
    _expand_shorthands,
    NO_DELETE_BLOCKED,
    READ_ONLY_BLOCKED,
    check_path_patterns,
    glob_to_regex,
    handle_bash,
    handle_edit,
    handle_grep,
    handle_read,
    handle_write,
    is_glob_pattern,
    load_config,
    load_patterns_dir,
    main,
    match_path,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _full_pattern(yaml_pattern: str, match_anywhere: bool = False) -> str:
    """Simulate the regex construction from handle_bash."""
    expanded = _expand_shorthands(yaml_pattern, {})
    if not match_anywhere:
        expanded = _CMD_POSITION_PREFIX + expanded
    return expanded


def _matches(yaml_pattern: str, command: str, match_anywhere: bool = False) -> bool:
    """Return True if *command* is caught by the given YAML pattern."""
    full = _full_pattern(yaml_pattern, match_anywhere)
    return bool(re.search(full, command, re.IGNORECASE))


# ---------------------------------------------------------------------------
# _expand_shorthands unit tests
# ---------------------------------------------------------------------------


class TestExpandShorthands:
    """Verify that the shorthand expansion replaces the correct placeholders."""

    def test_flags_expansion(self):
        result = _expand_shorthands(r"\bkubectl{flags}delete\b", {})
        assert _BUILTIN_SHORTHANDS["flags"] in result
        assert r"\bkubectl" in result
        assert r"delete\b" in result

    def test_args_expansion(self):
        result = _expand_shorthands(r"delete{args}\s+--all\b", {})
        assert _BUILTIN_SHORTHANDS["args"] in result
        assert r"delete" in result
        assert r"--all\b" in result

    def test_sudo_expansion(self):
        result = _expand_shorthands(r"{sudo}\bapt{flags}install\b", {})
        assert _BUILTIN_SHORTHANDS["sudo"] in result
        assert _BUILTIN_SHORTHANDS["flags"] in result

    def test_multiple_shorthands(self):
        """All shorthands in one pattern are expanded."""
        result = _expand_shorthands(r"{sudo}\bkubectl{flags}delete{args}\s+--all", {})
        assert _BUILTIN_SHORTHANDS["sudo"] in result
        assert _BUILTIN_SHORTHANDS["flags"] in result
        assert _BUILTIN_SHORTHANDS["args"] in result

    def test_unknown_placeholder_unchanged(self):
        original = r"\btool{unknown}subcommand"
        result = _expand_shorthands(original, {})
        assert result == original

    def test_regex_quantifier_not_expanded(self):
        """Regex quantifiers like {3} or {2,4} must not be treated as shorthands."""
        original = r"[a-z]{3}"
        result = _expand_shorthands(original, {})
        assert result == original

    def test_regex_quantifier_range_not_expanded(self):
        original = r"[a-z]{2,4}"
        result = _expand_shorthands(original, {})
        assert result == original

    def test_custom_shorthand_overrides_builtin(self):
        custom = {"flags": r"\s+"}
        result = _expand_shorthands(r"\bkubectl{flags}delete\b", custom)
        assert r"\bkubectl\s+delete\b" == result

    def test_custom_shorthand_new_name(self):
        custom = {"env": r"(?:env\s+\S+=\S+\s+)?"}
        result = _expand_shorthands(r"{env}\bkubectl{flags}delete\b", custom)
        assert r"(?:env\s+\S+=\S+\s+)?" in result
        assert _BUILTIN_SHORTHANDS["flags"] in result

    def test_no_double_expansion(self):
        """Expanding twice doesn't alter the result."""
        once = _expand_shorthands(r"\bkubectl{flags}delete\b", {})
        twice = _expand_shorthands(once, {})
        assert once == twice


# ---------------------------------------------------------------------------
# kubectl — the reported bug
# ---------------------------------------------------------------------------


class TestKubectlGlobalFlags:
    """The original bug: kubectl --context <ctx> delete pod bypassed patterns."""

    def test_kubectl_delete_with_context(self):
        assert _matches(
            r"\bkubectl{flags}delete\b",
            "kubectl --context ops-eu-south-0 delete pod -n wiki opensearch-cluster-master-0",
        )

    def test_kubectl_delete_without_flags(self):
        assert _matches(r"\bkubectl{flags}delete\b", "kubectl delete pod foo")

    def test_kubectl_delete_namespace_with_context(self):
        assert _matches(
            r"\bkubectl{flags}delete\s+(namespace|ns)\b",
            "kubectl --context prod delete namespace default",
        )

    def test_kubectl_delete_pvc_with_kubeconfig(self):
        assert _matches(
            r"\bkubectl{flags}delete\s+(pv|persistentvolume|pvc|persistentvolumeclaim)\b",
            "kubectl --kubeconfig /tmp/kc delete pvc my-volume",
        )

    def test_kubectl_delete_all_with_flags(self):
        assert _matches(
            r"\bkubectl{flags}delete{args}\s+--all\b",
            "kubectl --context prod delete pods --all",
        )

    def test_kubectl_delete_force_with_flags(self):
        assert _matches(
            r"\bkubectl{flags}delete{args}\s+--force",
            "kubectl -n kube-system delete pod foo --force",
        )

    def test_kubectl_apply_with_context(self):
        assert _matches(
            r"\bkubectl{flags}apply\b",
            "kubectl --context staging apply -f manifest.yaml",
        )

    def test_kubectl_exec_with_namespace(self):
        assert _matches(
            r"\bkubectl{flags}exec\b",
            "kubectl -n wiki exec -it pod/opensearch-0 -- bash",
        )

    def test_kubectl_drain_force_with_context(self):
        assert _matches(
            r"\bkubectl{flags}drain{args}\s+--force",
            "kubectl --context prod drain node-1 --force",
        )

    def test_kubectl_config_delete_with_kubeconfig(self):
        assert _matches(
            r"\bkubectl{flags}config\s+(delete-(context|cluster|user)|unset)\b",
            "kubectl --kubeconfig /tmp/kc config delete-context old-ctx",
        )

    def test_kubectl_rollout_restart_with_context(self):
        assert _matches(
            r"\bkubectl{flags}rollout\s+(restart|undo)\b",
            "kubectl --context prod rollout restart deployment/app",
        )

    def test_kubectl_get_secret_with_context(self):
        assert _matches(
            r"\bkubectl{flags}get\s+secrets?\b",
            "kubectl --context prod get secret my-secret -o yaml",
        )

    def test_kubectl_equals_flag(self):
        """Flags using = syntax: --context=prod."""
        assert _matches(
            r"\bkubectl{flags}delete\b",
            "kubectl --context=ops-eu-south-0 delete pod foo",
        )

    def test_kubectl_multiple_flags(self):
        assert _matches(
            r"\bkubectl{flags}delete\b",
            "kubectl -v=6 --context prod --namespace wiki delete pod foo",
        )


# ---------------------------------------------------------------------------
# Cross-command-boundary safety
# ---------------------------------------------------------------------------


class TestNoCrossCommandBoundary:
    """Ensure the expanded pattern doesn't match across ; | & boundaries."""

    def test_semicolon_boundary(self):
        assert not _matches(
            r"\bkubectl{flags}delete\b",
            "kubectl get pods; rm delete-logs.txt",
        )

    def test_pipe_boundary(self):
        assert not _matches(
            r"\bkubectl{flags}delete\b",
            "kubectl get pods | grep delete",
        )

    def test_and_boundary(self):
        assert not _matches(
            r"\bkubectl{flags}delete\b",
            "kubectl get pods && echo delete done",
        )


# ---------------------------------------------------------------------------
# {args} boundary safety
# ---------------------------------------------------------------------------


class TestArgsBoundarySafety:
    """{args} must not cross shell command boundaries."""

    def test_args_matches_inline_arguments(self):
        assert _matches(
            r"\bkubectl{flags}delete{args}\s+--all\b",
            "kubectl delete pods --all",
        )

    def test_args_matches_multiple_arguments(self):
        assert _matches(
            r"\bkubectl{flags}delete{args}\s+--all\b",
            "kubectl delete pods -n wiki --all",
        )

    def test_args_stops_at_semicolon(self):
        assert not _matches(
            r"\bkubectl{flags}delete{args}\s+--all\b",
            "kubectl delete pod foo; echo --all",
        )

    def test_args_stops_at_pipe(self):
        assert not _matches(
            r"\bkubectl{flags}delete{args}\s+--all\b",
            "kubectl delete pod foo | grep --all",
        )

    def test_args_stops_at_and(self):
        assert not _matches(
            r"\bkubectl{flags}delete{args}\s+--all\b",
            "kubectl delete pod foo && echo --all",
        )

    def test_args_zero_arguments(self):
        """Pattern works when there are no intermediate arguments."""
        assert _matches(
            r"\bkubectl{flags}delete{args}\s+--force",
            "kubectl delete --force",
        )


# ---------------------------------------------------------------------------
# {sudo} optional matching
# ---------------------------------------------------------------------------


class TestSudoOptional:
    """{sudo} makes the sudo prefix optional."""

    def test_with_sudo(self):
        assert _matches(
            r"{sudo}\b(apt|apt-get){flags}(remove|purge|autoremove)\b",
            "sudo apt remove package",
        )

    def test_without_sudo(self):
        assert _matches(
            r"{sudo}\b(apt|apt-get){flags}(remove|purge|autoremove)\b",
            "apt remove package",
        )

    def test_sudo_with_flags(self):
        assert _matches(
            r"{sudo}\bzypper{flags}(remove|rm)\b",
            "sudo zypper --non-interactive remove package",
        )

    def test_without_sudo_with_flags(self):
        assert _matches(
            r"{sudo}\bapk{flags}del\b",
            "apk --no-cache del package",
        )

    def test_sudo_pacman_install(self):
        assert _matches(
            r"{sudo}\bpacman{flags}-S",
            "sudo pacman --noconfirm -S package",
        )

    def test_pacman_without_sudo(self):
        assert _matches(
            r"{sudo}\bpacman{flags}-S",
            "pacman -S package",
        )


# ---------------------------------------------------------------------------
# Position prefix (command-start anchoring)
# ---------------------------------------------------------------------------


class TestPositionPrefix:
    """Patterns should not match inside quoted strings or arguments."""

    def test_not_in_commit_message(self):
        assert not _matches(
            r"\bkubectl{flags}delete\b",
            'git commit -m "kubectl delete pod was too aggressive"',
        )

    def test_matches_after_semicolon(self):
        assert _matches(
            r"\bkubectl{flags}delete\b",
            "echo hello; kubectl --context prod delete pod foo",
        )

    def test_matches_in_subshell(self):
        assert _matches(
            r"\bkubectl{flags}delete\b",
            "$(kubectl --context prod delete pod foo)",
        )


# ---------------------------------------------------------------------------
# Other CLI tools with global flags
# ---------------------------------------------------------------------------


class TestOtherCLIs:
    def test_helm_uninstall_with_kubeconfig(self):
        assert _matches(
            r"\bhelm{flags}(uninstall|delete)\b",
            "helm --kubeconfig /tmp/kc uninstall my-release",
        )

    def test_git_push_with_C(self):
        assert _matches(
            r"\bgit{flags}push\b",
            "git -C /path/to/repo push origin main",
        )

    def test_gh_pr_create_with_repo(self):
        assert _matches(
            r"\bgh{flags}pr\s+(create|merge|close|reopen|review|comment|edit|ready)\b",
            "gh --repo owner/repo pr create --title 'fix'",
        )

    def test_aws_s3_rm_with_region(self):
        assert _matches(
            r"\baws{flags}s3\s+rm{args}\s+(-r\b|--recursive)",
            "aws --region us-east-1 s3 rm s3://bucket --recursive",
        )

    def test_gcloud_with_project(self):
        assert _matches(
            r"\bgcloud{flags}compute\s+instances\s+(start|stop|reset)\b",
            "gcloud --project my-proj compute instances stop vm-1",
        )

    def test_terraform_workspace_delete_with_chdir(self):
        assert _matches(
            r"\bterraform{flags}workspace\s+delete\b",
            "terraform -chdir=/infra workspace delete staging",
        )

    def test_docker_run_with_host(self):
        assert _matches(
            r"\b(docker|podman){flags}run\b",
            "docker --host tcp://remote:2375 run -d nginx",
        )

    def test_az_vm_with_subscription(self):
        assert _matches(
            r"\baz{flags}vm\s+(start|stop|restart|deallocate)\b",
            "az --subscription my-sub vm stop --name my-vm",
        )

    def test_sudo_zypper_with_flags(self):
        assert _matches(
            r"{sudo}\bzypper{flags}(remove|rm)\b",
            "sudo zypper --non-interactive remove package",
        )

    def test_sudo_apk_with_flags(self):
        assert _matches(
            r"{sudo}\bapk{flags}del\b",
            "sudo apk --no-cache del package",
        )

    def test_firebase_deploy_with_project(self):
        assert _matches(
            r"\bfirebase{flags}deploy\b",
            "firebase --project my-proj deploy --only functions",
        )

    def test_nomad_job_stop_with_address(self):
        assert _matches(
            r"\bnomad{flags}job\s+stop\b",
            "nomad -address=http://localhost:4646 job stop my-job",
        )


# ---------------------------------------------------------------------------
# Custom shorthands from YAML
# ---------------------------------------------------------------------------


class TestCustomShorthands:
    """User-defined shorthands from YAML config are expanded."""

    def test_custom_shorthand_in_pattern(self):
        custom = {"env": r"(?:env\s+\S+=\S+\s+)?"}
        pattern = _expand_shorthands(r"{env}\bkubectl{flags}delete\b", custom)
        full = _CMD_POSITION_PREFIX + pattern
        assert re.search(full, "env FOO=bar kubectl delete pod", re.IGNORECASE)
        assert re.search(full, "kubectl delete pod", re.IGNORECASE)

    def test_custom_overrides_builtin(self):
        """User can override built-in shorthands via YAML."""
        custom = {"flags": r"\s+"}
        result = _expand_shorthands(r"\bkubectl{flags}delete\b", custom)
        assert result == r"\bkubectl\s+delete\b"


# ---------------------------------------------------------------------------
# is_glob_pattern
# ---------------------------------------------------------------------------


class TestIsGlobPattern:
    """Verify glob wildcard detection."""

    def test_star_is_glob(self):
        assert is_glob_pattern("*") is True

    def test_question_mark_is_glob(self):
        assert is_glob_pattern("?") is True

    def test_bracket_is_glob(self):
        assert is_glob_pattern("[") is True

    def test_plain_path_not_glob(self):
        assert is_glob_pattern("/etc/passwd") is False

    def test_empty_string_not_glob(self):
        assert is_glob_pattern("") is False


# ---------------------------------------------------------------------------
# glob_to_regex
# ---------------------------------------------------------------------------


class TestGlobToRegex:
    """Verify glob-to-regex conversion."""

    def test_star_becomes_non_greedy_non_slash(self):
        assert glob_to_regex("*") == r"[^\s/]*"

    def test_question_mark_becomes_single_char(self):
        assert glob_to_regex("?") == r"[^\s/]"

    def test_meta_chars_escaped(self):
        for char in r"\.^$+{}[]|()":
            assert glob_to_regex(char) == "\\" + char

    def test_plain_chars_pass_through(self):
        assert glob_to_regex("abc") == "abc"

    def test_mixed_pattern(self):
        result = glob_to_regex("*.log")
        assert result == r"[^\s/]*\.log"

    def test_resulting_regex_matches_expected(self):
        pattern = glob_to_regex("*.py")
        assert re.search(pattern, "script.py")
        assert not re.search(pattern, "script.txt")


# ---------------------------------------------------------------------------
# match_path
# ---------------------------------------------------------------------------


class TestMatchPath:
    """Verify file path matching against glob and prefix patterns."""

    def test_glob_matches_basename(self):
        assert match_path("/home/user/script.py", "*.py") is True

    def test_glob_case_insensitive(self):
        assert match_path("/tmp/FILE.txt", "*.TXT") is True

    def test_glob_non_matching(self):
        assert match_path("/home/user/script.py", "*.txt") is False

    def test_prefix_matches(self):
        assert match_path("/etc/passwd", "/etc/") is True

    def test_prefix_exact_match(self):
        assert match_path("/etc", "/etc") is True

    def test_prefix_no_match_different_path(self):
        assert match_path("/home/user", "/etc") is False

    def test_tilde_expansion(self):
        home = os.path.expanduser("~")
        assert match_path(f"{home}/secrets/key", "~/secrets") is True


# ---------------------------------------------------------------------------
# check_path_patterns
# ---------------------------------------------------------------------------


class TestCheckPathPatterns:
    """Verify command-vs-path pattern checking."""

    def test_literal_path_write_match(self):
        blocked, reason = check_path_patterns(
            "> /etc/config", "/etc/config", READ_ONLY_BLOCKED, "read-only path"
        )
        assert blocked is True
        assert "Blocked:" in reason

    def test_literal_path_no_match(self):
        blocked, reason = check_path_patterns(
            "cat /etc/config", "/etc/other", READ_ONLY_BLOCKED, "read-only path"
        )
        assert blocked is False
        assert reason == ""

    def test_glob_path_delete_match(self):
        blocked, reason = check_path_patterns(
            "rm foo.log", "*.log", NO_DELETE_BLOCKED, "no-delete path"
        )
        assert blocked is True

    def test_invalid_regex_swallowed(self):
        bad_patterns = [(r"[invalid{path}", "test")]
        blocked, reason = check_path_patterns(
            "some command", "/path", bad_patterns, "test"
        )
        assert blocked is False

    def test_both_expanded_and_original_tried(self):
        home = os.path.expanduser("~")
        blocked, reason = check_path_patterns(
            f"> {home}/readonly/file",
            "~/readonly/file",
            READ_ONLY_BLOCKED,
            "read-only path",
        )
        assert blocked is True

    def test_glob_no_substring_match(self):
        """*.o must not match .obsidian (glob boundary prevents prefix match)."""
        blocked, _ = check_path_patterns(
            'git rm --cached ".obsidian/workspace.json"',
            "*.o",
            READ_ONLY_BLOCKED,
            "read-only path",
        )
        assert blocked is False

    def test_glob_no_substring_match_so_vs_something(self):
        """*.so must not match .something/file."""
        blocked, _ = check_path_patterns(
            "rm .ソフト/data",
            "*.so",
            NO_DELETE_BLOCKED,
            "no-delete path",
        )
        assert blocked is False

    def test_glob_matches_exact_extension(self):
        """*.o still matches actual .o files."""
        blocked, _ = check_path_patterns(
            "rm main.o",
            "*.o",
            NO_DELETE_BLOCKED,
            "no-delete path",
        )
        assert blocked is True

    def test_glob_matches_quoted_path(self):
        """*.o matches inside quotes."""
        blocked, _ = check_path_patterns(
            'rm "main.o"',
            "*.o",
            NO_DELETE_BLOCKED,
            "no-delete path",
        )
        assert blocked is True

    def test_glob_matches_path_component(self):
        """*.o matches as path component before /."""
        blocked, _ = check_path_patterns(
            "rm build/main.o",
            "*.o",
            NO_DELETE_BLOCKED,
            "no-delete path",
        )
        assert blocked is True


# ---------------------------------------------------------------------------
# _block
# ---------------------------------------------------------------------------


class TestBlock:
    """Verify the _block output helper."""

    def test_exits_with_code_2(self):
        with pytest.raises(SystemExit) as exc_info:
            _block("some reason", "some context")
        assert exc_info.value.code == 2

    def test_prints_security_and_target(self, capsys):
        with pytest.raises(SystemExit):
            _block("some reason", "some context")
        captured = capsys.readouterr()
        assert "SECURITY:" in captured.err
        assert "Target:" in captured.err

    def test_long_context_truncated(self, capsys):
        long_context = "x" * 200
        with pytest.raises(SystemExit):
            _block("reason", long_context)
        captured = capsys.readouterr()
        assert "..." in captured.err

    def test_context_at_100_chars_not_truncated(self, capsys):
        context = "x" * 100
        with pytest.raises(SystemExit):
            _block("reason", context)
        captured = capsys.readouterr()
        assert "..." not in captured.err
        assert "x" * 100 in captured.err


# ---------------------------------------------------------------------------
# handle_bash — all 4 phases
# ---------------------------------------------------------------------------


class TestHandleBash:
    """Verify the Bash tool handler across all phases."""

    def test_empty_command_exits_0(self):
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": ""}, {})
        assert exc_info.value.code == 0

    # Phase 1 — pattern matching
    def test_pattern_block(self):
        config = {
            "bashToolPatterns": [{"pattern": r"\brm\s+-rf\b", "reason": "dangerous"}],
        }
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": "rm -rf /"}, config)
        assert exc_info.value.code == 2

    def test_pattern_ask(self, capsys):
        config = {
            "bashToolPatterns": [
                {"pattern": r"\bgit\s+push\b", "reason": "push check", "ask": True}
            ],
        }
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": "git push"}, config)
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_match_anywhere_skips_position_prefix(self):
        config = {
            "bashToolPatterns": [
                {
                    "pattern": r">\s*/etc/secret",
                    "reason": "redirect block",
                    "match_anywhere": True,
                }
            ],
        }
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": "echo data > /etc/secret"}, config)
        assert exc_info.value.code == 2

    def test_shorthand_expansion_in_pattern(self):
        config = {
            "bashToolPatterns": [
                {"pattern": r"\bkubectl{flags}delete\b", "reason": "kubectl delete"}
            ],
            "shorthands": {},
        }
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": "kubectl --context prod delete pod"}, config)
        assert exc_info.value.code == 2

    def test_bad_regex_swallowed_in_patterns(self):
        config = {
            "bashToolPatterns": [
                {"pattern": "[invalid", "reason": "bad regex"},
                {"pattern": r"\brm\b", "reason": "rm blocked"},
            ],
        }
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": "rm file.txt"}, config)
        assert exc_info.value.code == 2

    def test_no_pattern_match_falls_through(self):
        config = {
            "bashToolPatterns": [{"pattern": r"\brm\s+-rf\b", "reason": "dangerous"}],
        }
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": "echo hello"}, config)
        assert exc_info.value.code == 0

    # Phase 2 — zero-access paths
    def test_zero_access_glob_blocks(self):
        config = {"zeroAccessPaths": ["*.pem"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": "cat server.pem"}, config)
        assert exc_info.value.code == 2

    def test_zero_access_absolute_blocks(self):
        config = {"zeroAccessPaths": ["/secrets/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": "cat /secrets/key"}, config)
        assert exc_info.value.code == 2

    def test_zero_access_relative_boundary(self):
        """Relative zero-access path does not match inside longer names."""
        config = {"zeroAccessPaths": ["secrets/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": "cat external-secrets/file"}, config)
        assert exc_info.value.code == 0

    def test_zero_access_glob_no_substring(self):
        """*.o in zeroAccessPaths must not match .obsidian paths."""
        config = {"zeroAccessPaths": ["*.o"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": 'cat ".obsidian/workspace.json"'}, config)
        assert exc_info.value.code == 0

    def test_zero_access_glob_exact_match(self):
        """*.o in zeroAccessPaths still blocks actual .o files."""
        config = {"zeroAccessPaths": ["*.o"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": "cat main.o"}, config)
        assert exc_info.value.code == 2

    # Phase 3 — read-only paths
    def test_read_only_write_blocked(self):
        config = {"readOnlyPaths": ["/readonly/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": "> /readonly/file"}, config)
        assert exc_info.value.code == 2

    def test_read_only_read_allowed(self):
        config = {"readOnlyPaths": ["/readonly/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": "cat /readonly/file"}, config)
        assert exc_info.value.code == 0

    # Phase 4 — no-delete paths
    def test_no_delete_rm_blocked(self):
        config = {"noDeletePaths": ["/protected/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": "rm /protected/file"}, config)
        assert exc_info.value.code == 2

    def test_no_delete_write_allowed(self):
        config = {"noDeletePaths": ["/protected/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": "> /protected/file"}, config)
        assert exc_info.value.code == 0

    # All clear
    def test_all_clear_exits_0(self):
        config = {
            "bashToolPatterns": [{"pattern": r"\brm\s+-rf\b", "reason": "dangerous"}],
            "zeroAccessPaths": ["/secrets/"],
            "readOnlyPaths": ["/readonly/"],
            "noDeletePaths": ["/protected/"],
        }
        with pytest.raises(SystemExit) as exc_info:
            handle_bash({"command": "echo hello"}, config)
        assert exc_info.value.code == 0


# ---------------------------------------------------------------------------
# handle_edit
# ---------------------------------------------------------------------------


class TestHandleEdit:
    """Verify the Edit tool handler."""

    def test_empty_file_path_exits_0(self):
        with pytest.raises(SystemExit) as exc_info:
            handle_edit({"file_path": ""}, {})
        assert exc_info.value.code == 0

    def test_zero_access_blocked(self):
        config = {"zeroAccessPaths": ["/secrets/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_edit({"file_path": "/secrets/key"}, config)
        assert exc_info.value.code == 2

    def test_read_only_blocked(self):
        config = {"readOnlyPaths": ["/readonly/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_edit({"file_path": "/readonly/config"}, config)
        assert exc_info.value.code == 2

    def test_allowed(self):
        config = {"zeroAccessPaths": ["/secrets/"], "readOnlyPaths": ["/readonly/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_edit({"file_path": "/home/user/file.txt"}, config)
        assert exc_info.value.code == 0


# ---------------------------------------------------------------------------
# handle_write
# ---------------------------------------------------------------------------


class TestHandleWrite:
    """Verify the Write tool handler."""

    def test_empty_file_path_exits_0(self):
        with pytest.raises(SystemExit) as exc_info:
            handle_write({"file_path": ""}, {})
        assert exc_info.value.code == 0

    def test_zero_access_blocked(self):
        config = {"zeroAccessPaths": ["/secrets/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_write({"file_path": "/secrets/key"}, config)
        assert exc_info.value.code == 2

    def test_read_only_blocked(self):
        config = {"readOnlyPaths": ["/readonly/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_write({"file_path": "/readonly/config"}, config)
        assert exc_info.value.code == 2

    def test_allowed(self):
        config = {"zeroAccessPaths": ["/secrets/"], "readOnlyPaths": ["/readonly/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_write({"file_path": "/home/user/file.txt"}, config)
        assert exc_info.value.code == 0


# ---------------------------------------------------------------------------
# handle_read
# ---------------------------------------------------------------------------


class TestHandleRead:
    """Verify the Read tool handler (reads of read-only paths are fine)."""

    def test_empty_file_path_exits_0(self):
        with pytest.raises(SystemExit) as exc_info:
            handle_read({"file_path": ""}, {})
        assert exc_info.value.code == 0

    def test_zero_access_blocked(self):
        config = {"zeroAccessPaths": ["/secrets/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_read({"file_path": "/secrets/key"}, config)
        assert exc_info.value.code == 2

    def test_read_only_allowed(self):
        config = {"readOnlyPaths": ["/readonly/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_read({"file_path": "/readonly/config"}, config)
        assert exc_info.value.code == 0

    def test_allowed(self):
        config = {"zeroAccessPaths": ["/secrets/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_read({"file_path": "/home/user/file.txt"}, config)
        assert exc_info.value.code == 0


# ---------------------------------------------------------------------------
# handle_grep
# ---------------------------------------------------------------------------


class TestHandleGrep:
    """Verify the Grep tool handler."""

    def test_empty_path_exits_0(self):
        with pytest.raises(SystemExit) as exc_info:
            handle_grep({"path": ""}, {})
        assert exc_info.value.code == 0

    def test_zero_access_blocked(self):
        config = {"zeroAccessPaths": ["/secrets/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_grep({"path": "/secrets/key"}, config)
        assert exc_info.value.code == 2

    def test_allowed(self):
        config = {"zeroAccessPaths": ["/secrets/"]}
        with pytest.raises(SystemExit) as exc_info:
            handle_grep({"path": "/home/user/file.txt"}, config)
        assert exc_info.value.code == 0


# ---------------------------------------------------------------------------
# load_patterns_dir
# ---------------------------------------------------------------------------


class TestLoadPatternsDir:
    """Verify multi-file YAML pattern loading."""

    def test_single_yaml_all_keys(self, tmp_path):
        (tmp_path / "config.yaml").write_text(
            yaml.dump(
                {
                    "bashToolPatterns": [{"pattern": "test"}],
                    "zeroAccessPaths": ["/secret"],
                    "readOnlyPaths": ["/readonly"],
                    "noDeletePaths": ["/nodelete"],
                }
            )
        )
        result = load_patterns_dir(tmp_path)
        assert result["bashToolPatterns"] == [{"pattern": "test"}]
        assert result["zeroAccessPaths"] == ["/secret"]
        assert result["readOnlyPaths"] == ["/readonly"]
        assert result["noDeletePaths"] == ["/nodelete"]

    def test_multiple_yaml_concatenated(self, tmp_path):
        (tmp_path / "a.yaml").write_text(yaml.dump({"zeroAccessPaths": ["/a"]}))
        (tmp_path / "b.yaml").write_text(yaml.dump({"zeroAccessPaths": ["/b"]}))
        result = load_patterns_dir(tmp_path)
        assert result["zeroAccessPaths"] == ["/a", "/b"]

    def test_shorthands_accumulated(self, tmp_path):
        (tmp_path / "config.yaml").write_text(
            yaml.dump({"shorthands": {"env": r"(?:env\s+)?"}})
        )
        result = load_patterns_dir(tmp_path)
        assert result["shorthands"]["env"] == r"(?:env\s+)?"

    def test_missing_keys_empty_lists(self, tmp_path):
        (tmp_path / "config.yaml").write_text(
            yaml.dump({"zeroAccessPaths": ["/secret"]})
        )
        result = load_patterns_dir(tmp_path)
        assert result["bashToolPatterns"] == []
        assert result["readOnlyPaths"] == []
        assert result["noDeletePaths"] == []

    def test_non_list_value_skipped(self, tmp_path):
        (tmp_path / "config.yaml").write_text(
            yaml.dump({"zeroAccessPaths": "not a list"})
        )
        result = load_patterns_dir(tmp_path)
        assert result["zeroAccessPaths"] == []

    def test_empty_yaml_file(self, tmp_path):
        (tmp_path / "empty.yaml").write_text("")
        result = load_patterns_dir(tmp_path)
        assert result["bashToolPatterns"] == []

    def test_yaml_and_yml_both_loaded(self, tmp_path):
        (tmp_path / "a.yaml").write_text(yaml.dump({"zeroAccessPaths": ["/a"]}))
        (tmp_path / "b.yml").write_text(yaml.dump({"zeroAccessPaths": ["/b"]}))
        result = load_patterns_dir(tmp_path)
        assert "/a" in result["zeroAccessPaths"]
        assert "/b" in result["zeroAccessPaths"]
        assert len(result["zeroAccessPaths"]) == 2


# ---------------------------------------------------------------------------
# load_config
# ---------------------------------------------------------------------------


class TestLoadConfig:
    """Verify top-level config loading."""

    def test_patterns_dir_delegates(self, monkeypatch, tmp_path):
        patterns_dir = tmp_path / "patterns"
        patterns_dir.mkdir()
        (patterns_dir / "config.yaml").write_text(
            yaml.dump({"zeroAccessPaths": ["/secret"]})
        )
        monkeypatch.setattr("damage_control.get_patterns_dir", lambda: patterns_dir)
        result = load_config()
        assert result["zeroAccessPaths"] == ["/secret"]

    def test_single_yaml_with_shorthands(self, monkeypatch, tmp_path):
        config_file = tmp_path / "patterns.yaml"
        config_file.write_text(
            yaml.dump({"zeroAccessPaths": ["/secret"], "shorthands": {"env": "test"}})
        )
        monkeypatch.setattr("damage_control.get_patterns_dir", lambda: None)
        monkeypatch.setattr("damage_control.get_config_path", lambda: config_file)
        result = load_config()
        assert result["shorthands"]["env"] == "test"

    def test_single_yaml_without_shorthands(self, monkeypatch, tmp_path):
        config_file = tmp_path / "patterns.yaml"
        config_file.write_text(yaml.dump({"zeroAccessPaths": ["/secret"]}))
        monkeypatch.setattr("damage_control.get_patterns_dir", lambda: None)
        monkeypatch.setattr("damage_control.get_config_path", lambda: config_file)
        result = load_config()
        assert result["shorthands"] == {}

    def test_missing_config_returns_empty(self, monkeypatch, tmp_path, capsys):
        missing = tmp_path / "nonexistent.yaml"
        monkeypatch.setattr("damage_control.get_patterns_dir", lambda: None)
        monkeypatch.setattr("damage_control.get_config_path", lambda: missing)
        result = load_config()
        for key in ("bashToolPatterns", "zeroAccessPaths", "readOnlyPaths", "noDeletePaths"):
            assert result[key] == []
        captured = capsys.readouterr()
        assert "Warning" in captured.err


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


class TestMain:
    """Verify the main dispatcher."""

    def test_valid_json_known_tool(self, monkeypatch):
        input_data = json.dumps({"tool_name": "Bash", "tool_input": {"command": ""}})
        monkeypatch.setattr("sys.stdin", io.StringIO(input_data))
        monkeypatch.setattr("damage_control.load_config", lambda: {})
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    def test_valid_json_unknown_tool(self, monkeypatch):
        input_data = json.dumps({"tool_name": "Unknown", "tool_input": {}})
        monkeypatch.setattr("sys.stdin", io.StringIO(input_data))
        monkeypatch.setattr("damage_control.load_config", lambda: {})
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    def test_invalid_json(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.stdin", io.StringIO("not json"))
        monkeypatch.setattr("damage_control.load_config", lambda: {})
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error" in captured.err

    def test_empty_stdin(self, monkeypatch):
        monkeypatch.setattr("sys.stdin", io.StringIO(""))
        monkeypatch.setattr("damage_control.load_config", lambda: {})
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# _expand_shorthands edge cases
# ---------------------------------------------------------------------------


class TestExpandShorthandsEdgeCases:
    """Additional edge cases for shorthand expansion."""

    def test_escaped_backslash_before_brace_not_expanded(self):
        r"""\\{flags} — backslash before brace prevents expansion."""
        original = r"\\{flags}"
        result = _expand_shorthands(original, {})
        assert result == original

    def test_range_quantifier_not_expanded(self):
        """{3,5} range quantifier left untouched."""
        original = r"[a-z]{3,5}"
        result = _expand_shorthands(original, {})
        assert result == original


# ---------------------------------------------------------------------------
# Tanka (tk) patterns
# ---------------------------------------------------------------------------


class TestTankaPatterns:
    """Verify tanka (tk) patterns catch dangerous commands."""

    # Destructive — blocked
    def test_tk_delete(self):
        assert _matches(r"\btk{flags}delete\b", "tk delete environments/default")

    def test_tk_delete_with_flags(self):
        assert _matches(
            r"\btk{flags}delete\b",
            "tk --tla-code env=prod delete environments/production",
        )

    def test_tk_prune(self):
        assert _matches(r"\btk{flags}prune\b", "tk prune environments/default")

    def test_tk_prune_with_flags(self):
        assert _matches(
            r"\btk{flags}prune\b",
            "tk --tla-str cluster=us-east-1 prune environments/production",
        )

    # Mutating — ask
    def test_tk_apply(self):
        assert _matches(r"\btk{flags}apply\b", "tk apply environments/default")

    def test_tk_apply_with_flags(self):
        assert _matches(
            r"\btk{flags}apply\b",
            "tk --tla-code env=staging apply environments/staging",
        )

    def test_tk_diff(self):
        assert _matches(r"\btk{flags}diff\b", "tk diff environments/default")

    def test_tk_diff_with_flags(self):
        assert _matches(
            r"\btk{flags}diff\b",
            "tk --tla-str cluster=prod diff environments/production",
        )

    # Safe commands — should NOT match destructive/mutating patterns
    def test_tk_show_not_blocked(self):
        assert not _matches(r"\btk{flags}delete\b", "tk show environments/default")
        assert not _matches(r"\btk{flags}prune\b", "tk show environments/default")
        assert not _matches(r"\btk{flags}apply\b", "tk show environments/default")

    def test_tk_export_not_blocked(self):
        assert not _matches(r"\btk{flags}delete\b", "tk export environments/default ./out")

    # Boundary safety — no false positives
    def test_tk_in_commit_message_not_matched(self):
        assert not _matches(
            r"\btk{flags}delete\b",
            'git commit -m "tk delete was too aggressive"',
        )

    def test_tk_after_pipe_not_matched(self):
        assert not _matches(
            r"\btk{flags}delete\b",
            "echo test | grep delete",
        )
