"""Tests for damage_control.py — shorthands expansion and integration."""

from __future__ import annotations

import re

import pytest

from damage_control import (
    _BUILTIN_SHORTHANDS,
    _CMD_POSITION_PREFIX,
    _expand_shorthands,
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
