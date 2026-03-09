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

    # --- Paths containing "secrets" as substring (not a secrets dir) ---

    def test_allow_git_add_external_secrets(self):
        """'secrets/' inside 'external-secrets/' should not trigger zero-access."""
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "git add ksonnet/lib/external-secrets/gar-migration/db-o11y.libsonnet"
            },
        )
        assert code == 0
        assert stdout == ""

    def test_allow_cat_external_secrets_path(self):
        """Reading a file under an 'external-secrets' directory should be allowed."""
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "cat charts/external-secrets/templates/deployment.yaml"},
        )
        assert code == 0
        assert stdout == ""

    def test_allow_ls_external_secrets(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "ls external-secrets/"}
        )
        assert code == 0
        assert stdout == ""

    # --- Trusted npx commands ---

    def test_allow_npx_vitest(self):
        code, stdout, _ = run_hook("Bash", {"command": "npx vitest"})
        assert code == 0
        assert stdout == ""

    def test_allow_npx_vitest_run(self):
        code, stdout, _ = run_hook("Bash", {"command": "npx vitest run"})
        assert code == 0
        assert stdout == ""

    def test_allow_npx_vitest_with_flags(self):
        code, stdout, _ = run_hook("Bash", {"command": "npx --yes vitest"})
        assert code == 0
        assert stdout == ""

    def test_allow_npx_eslint(self):
        code, stdout, _ = run_hook("Bash", {"command": "npx eslint ."})
        assert code == 0
        assert stdout == ""

    def test_allow_npx_prettier(self):
        code, stdout, _ = run_hook("Bash", {"command": "npx prettier --write ."})
        assert code == 0
        assert stdout == ""

    def test_allow_npx_tsc(self):
        code, stdout, _ = run_hook("Bash", {"command": "npx tsc --noEmit"})
        assert code == 0
        assert stdout == ""

    def test_allow_npx_jest(self):
        code, stdout, _ = run_hook("Bash", {"command": "npx jest --coverage"})
        assert code == 0
        assert stdout == ""

    def test_allow_npx_playwright(self):
        code, stdout, _ = run_hook("Bash", {"command": "npx playwright test"})
        assert code == 0
        assert stdout == ""

    def test_allow_bunx_vitest(self):
        code, stdout, _ = run_hook("Bash", {"command": "bunx vitest"})
        assert code == 0
        assert stdout == ""

    def test_allow_yarn_dlx_eslint(self):
        code, stdout, _ = run_hook("Bash", {"command": "yarn dlx eslint ."})
        assert code == 0
        assert stdout == ""

    def test_allow_pnpm_dlx_prettier(self):
        code, stdout, _ = run_hook("Bash", {"command": "pnpm dlx prettier ."})
        assert code == 0
        assert stdout == ""

    def test_allow_npx_next_build(self):
        code, stdout, _ = run_hook("Bash", {"command": "npx next build"})
        assert code == 0
        assert stdout == ""

    def test_allow_npx_prisma_migrate(self):
        code, stdout, _ = run_hook("Bash", {"command": "npx prisma migrate dev"})
        assert code == 0
        assert stdout == ""

    def test_allow_npx_turbo_run(self):
        code, stdout, _ = run_hook("Bash", {"command": "npx turbo run build"})
        assert code == 0
        assert stdout == ""
