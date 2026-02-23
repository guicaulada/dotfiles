"""Tests for zero-access, read-only, and no-delete path enforcement in Bash handler."""

from tests.conftest import HOME, run_hook


class TestZeroAccessPaths:
    def test_block_cat_env(self):
        code, _, stderr = run_hook("Bash", {"command": "cat .env"})
        assert code == 2
        assert "zero-access" in stderr.lower()

    def test_block_cat_ssh(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.ssh/id_rsa"})
        assert code == 2

    def test_block_cat_aws(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.aws/credentials"})
        assert code == 2

    def test_block_cat_pem(self):
        code, _, _ = run_hook("Bash", {"command": "cat server.pem"})
        assert code == 2

    def test_block_cat_tfstate(self):
        code, _, _ = run_hook("Bash", {"command": "cat terraform.tfstate"})
        assert code == 2

    def test_block_cat_password_store(self):
        code, _, _ = run_hook(
            "Bash", {"command": f"cat {HOME}/.password-store/email/gmail.gpg"}
        )
        assert code == 2

    def test_block_cat_vault_token(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.vault-token"})
        assert code == 2

    def test_block_cat_keyrings(self):
        code, _, _ = run_hook(
            "Bash", {"command": f"cat {HOME}/.local/share/keyrings/default.keyring"}
        )
        assert code == 2


class TestReadOnlyPaths:
    def test_block_sed_bashrc(self):
        code, _, _ = run_hook(
            "Bash", {"command": f"sed -i 's/old/new/' {HOME}/.bashrc"}
        )
        assert code == 2

    def test_block_write_redirect_etc(self):
        code, _, _ = run_hook("Bash", {"command": "echo data > /etc/hosts"})
        assert code == 2

    def test_block_rm_lock_file(self):
        code, _, _ = run_hook("Bash", {"command": "rm package-lock.json"})
        assert code == 2

    def test_block_write_var_log(self):
        code, _, _ = run_hook("Bash", {"command": "echo data > /var/log/syslog"})
        assert code == 2

    def test_block_rm_var_log(self):
        code, _, _ = run_hook("Bash", {"command": "rm /var/log/auth.log"})
        assert code == 2


class TestNoDeletePaths:
    def test_block_rm_gitignore(self):
        code, _, _ = run_hook("Bash", {"command": "rm .gitignore"})
        assert code == 2

    def test_block_rm_license(self):
        code, _, _ = run_hook("Bash", {"command": "rm LICENSE"})
        assert code == 2

    def test_block_rm_claude_dir(self):
        code, _, _ = run_hook("Bash", {"command": f"rm {HOME}/.claude/settings.json"})
        assert code == 2
