"""Tests for commands that should be allowed (not blocked or asked)."""

from tests.conftest import run_hook


class TestAllowedCommands:
    def test_allow_ls(self):
        code, stdout, _ = run_hook("Bash", {"command": "ls -la"})
        assert code == 0
        assert stdout == ""

    def test_allow_git_status(self):
        code, stdout, _ = run_hook("Bash", {"command": "git status"})
        assert code == 0
        assert stdout == ""

    def test_allow_cat_normal_file(self):
        code, stdout, _ = run_hook("Bash", {"command": "cat /tmp/test.py"})
        assert code == 0
        assert stdout == ""

    def test_allow_echo(self):
        code, stdout, _ = run_hook("Bash", {"command": "echo hello world"})
        assert code == 0

    def test_allow_empty_command(self):
        code, stdout, _ = run_hook("Bash", {"command": ""})
        assert code == 0

    def test_allow_npm_test(self):
        code, stdout, _ = run_hook("Bash", {"command": "npm test"})
        assert code == 0
        assert stdout == ""

    def test_allow_python_pytest(self):
        code, stdout, _ = run_hook("Bash", {"command": "pytest tests/"})
        assert code == 0

    def test_allow_export_path_append(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "export PATH=/usr/local/bin:$PATH"}
        )
        # Should not match the block pattern (has $PATH)
        # May hit sudo ask or pass through
        assert code == 0

    # --- Kubernetes read-only commands ---

    def test_allow_kubectl_get(self):
        code, stdout, _ = run_hook("Bash", {"command": "kubectl get pods -n default"})
        assert code == 0
        assert stdout == ""

    def test_allow_kubectl_describe(self):
        code, stdout, _ = run_hook("Bash", {"command": "kubectl describe pod my-pod"})
        assert code == 0
        assert stdout == ""

    def test_allow_kubectl_logs(self):
        code, stdout, _ = run_hook("Bash", {"command": "kubectl logs my-pod"})
        assert code == 0
        assert stdout == ""

    def test_allow_helm_list(self):
        code, stdout, _ = run_hook("Bash", {"command": "helm list -A"})
        assert code == 0
        assert stdout == ""

    def test_allow_helm_status(self):
        code, stdout, _ = run_hook("Bash", {"command": "helm status my-release"})
        assert code == 0
        assert stdout == ""
