"""Tests for Read, Edit, Write, Grep handlers and the dispatcher."""

import subprocess

from tests.conftest import HOME, SCRIPT, run_hook


class TestReadHandler:
    # --- Zero-access blocks ---

    def test_block_ssh_key(self):
        code, _, stderr = run_hook("Read", {"file_path": f"{HOME}/.ssh/id_rsa"})
        assert code == 2
        assert "zero-access" in stderr.lower()

    def test_block_env_file(self):
        code, _, _ = run_hook("Read", {"file_path": "/project/.env"})
        assert code == 2

    def test_block_env_local(self):
        code, _, _ = run_hook("Read", {"file_path": "/project/.env.local"})
        assert code == 2

    def test_block_pem_file(self):
        code, _, _ = run_hook("Read", {"file_path": "/tmp/server.pem"})
        assert code == 2

    def test_block_key_file(self):
        code, _, _ = run_hook("Read", {"file_path": "/tmp/private.key"})
        assert code == 2

    def test_block_aws_credentials(self):
        code, _, _ = run_hook("Read", {"file_path": f"{HOME}/.aws/credentials"})
        assert code == 2

    def test_block_kube_config(self):
        code, _, _ = run_hook("Read", {"file_path": f"{HOME}/.kube/config"})
        assert code == 2

    def test_block_docker_config(self):
        code, _, _ = run_hook("Read", {"file_path": f"{HOME}/.docker/config.json"})
        assert code == 2

    def test_block_gnupg(self):
        code, _, _ = run_hook("Read", {"file_path": f"{HOME}/.gnupg/secring.gpg"})
        assert code == 2

    def test_block_tfstate(self):
        code, _, _ = run_hook("Read", {"file_path": "/infra/terraform.tfstate"})
        assert code == 2

    def test_block_tfvars(self):
        code, _, _ = run_hook("Read", {"file_path": "/infra/prod.tfvars"})
        assert code == 2

    def test_block_credentials_json(self):
        code, _, _ = run_hook("Read", {"file_path": "/tmp/gcp-credentials.json"})
        assert code == 2

    def test_block_service_account(self):
        code, _, _ = run_hook("Read", {"file_path": "/tmp/myServiceAccountKey.json"})
        assert code == 2

    def test_block_netrc(self):
        code, _, _ = run_hook("Read", {"file_path": f"{HOME}/.netrc"})
        assert code == 2

    def test_block_git_credentials(self):
        code, _, _ = run_hook("Read", {"file_path": f"{HOME}/.git-credentials"})
        assert code == 2

    def test_block_keystore(self):
        code, _, _ = run_hook("Read", {"file_path": "/app/release.keystore"})
        assert code == 2

    # --- Credential manager zero-access blocks ---

    def test_block_read_password_store(self):
        code, _, _ = run_hook(
            "Read", {"file_path": f"{HOME}/.password-store/email/gmail.gpg"}
        )
        assert code == 2

    def test_block_read_op_config(self):
        code, _, _ = run_hook("Read", {"file_path": f"{HOME}/.config/op/config"})
        assert code == 2

    def test_block_read_vault_token(self):
        code, _, _ = run_hook("Read", {"file_path": f"{HOME}/.vault-token"})
        assert code == 2

    def test_block_read_gnome_keyrings(self):
        code, _, _ = run_hook(
            "Read", {"file_path": f"{HOME}/.local/share/keyrings/default.keyring"}
        )
        assert code == 2

    def test_block_read_kde_wallet(self):
        code, _, _ = run_hook(
            "Read", {"file_path": f"{HOME}/.local/share/kwalletd/kdewallet.kwl"}
        )
        assert code == 2

    def test_block_read_macos_keychain(self):
        code, _, _ = run_hook(
            "Read", {"file_path": f"{HOME}/Library/Keychains/login.keychain-db"}
        )
        assert code == 2

    # --- Read-only paths: reads should be ALLOWED ---

    def test_allow_read_bashrc(self):
        code, stdout, _ = run_hook("Read", {"file_path": f"{HOME}/.bashrc"})
        assert code == 0
        assert stdout == ""

    def test_allow_read_etc(self):
        code, _, _ = run_hook("Read", {"file_path": "/etc/hosts"})
        assert code == 0

    def test_allow_read_lock_file(self):
        code, _, _ = run_hook("Read", {"file_path": "/project/package-lock.json"})
        assert code == 0

    def test_allow_read_node_modules(self):
        code, _, _ = run_hook(
            "Read", {"file_path": "/project/node_modules/lodash/index.js"}
        )
        assert code == 0

    # --- Normal files: always allowed ---

    def test_allow_normal_file(self):
        code, stdout, _ = run_hook("Read", {"file_path": "/tmp/test.py"})
        assert code == 0
        assert stdout == ""

    def test_allow_empty_path(self):
        code, _, _ = run_hook("Read", {"file_path": ""})
        assert code == 0


class TestGrepHandler:
    # --- Zero-access blocks ---

    def test_block_grep_ssh(self):
        code, _, stderr = run_hook(
            "Grep", {"pattern": "password", "path": f"{HOME}/.ssh/"}
        )
        assert code == 2
        assert "zero-access" in stderr.lower()

    def test_block_grep_aws(self):
        code, _, _ = run_hook("Grep", {"pattern": "key", "path": f"{HOME}/.aws/"})
        assert code == 2

    def test_block_grep_kube(self):
        code, _, _ = run_hook("Grep", {"pattern": "token", "path": f"{HOME}/.kube/"})
        assert code == 2

    def test_block_grep_gnupg(self):
        code, _, _ = run_hook("Grep", {"pattern": "secret", "path": f"{HOME}/.gnupg/"})
        assert code == 2

    def test_block_grep_gcloud(self):
        code, _, _ = run_hook(
            "Grep", {"pattern": "token", "path": f"{HOME}/.config/gcloud/"}
        )
        assert code == 2

    def test_block_grep_env_file(self):
        code, _, _ = run_hook("Grep", {"pattern": "SECRET", "path": "/project/.env"})
        assert code == 2

    # --- Allowed ---

    def test_allow_grep_normal_dir(self):
        code, stdout, _ = run_hook("Grep", {"pattern": "foo", "path": "/tmp/"})
        assert code == 0
        assert stdout == ""

    def test_allow_grep_no_path(self):
        code, _, _ = run_hook("Grep", {"pattern": "search term"})
        assert code == 0

    def test_allow_grep_empty_path(self):
        code, _, _ = run_hook("Grep", {"pattern": "search", "path": ""})
        assert code == 0

    def test_allow_grep_project_dir(self):
        code, _, _ = run_hook(
            "Grep", {"pattern": "TODO", "path": "/home/user/project/src/"}
        )
        assert code == 0


class TestEditHandler:
    # --- Zero-access blocks ---

    def test_block_edit_ssh_config(self):
        code, _, stderr = run_hook("Edit", {"file_path": f"{HOME}/.ssh/config"})
        assert code == 2
        assert "zero-access" in stderr.lower()

    def test_block_edit_env(self):
        code, _, _ = run_hook("Edit", {"file_path": "/project/.env"})
        assert code == 2

    def test_block_edit_pem(self):
        code, _, _ = run_hook("Edit", {"file_path": "/tmp/cert.pem"})
        assert code == 2

    def test_block_edit_aws(self):
        code, _, _ = run_hook("Edit", {"file_path": f"{HOME}/.aws/config"})
        assert code == 2

    # --- Read-only blocks ---

    def test_block_edit_bashrc(self):
        code, _, stderr = run_hook("Edit", {"file_path": f"{HOME}/.bashrc"})
        assert code == 2
        assert "read-only" in stderr.lower()

    def test_block_edit_zshrc(self):
        code, _, _ = run_hook("Edit", {"file_path": f"{HOME}/.zshrc"})
        assert code == 2

    def test_block_edit_etc(self):
        code, _, _ = run_hook("Edit", {"file_path": "/etc/hosts"})
        assert code == 2

    def test_block_edit_lock_file(self):
        # yarn.lock matches via *.lock glob pattern
        code, _, _ = run_hook("Edit", {"file_path": "/project/yarn.lock"})
        assert code == 2

    def test_allow_edit_lock_json(self):
        # package-lock.json ends in .json, not .lock; literal "package-lock.json"
        # only prefix-matches, so absolute paths don't match
        code, _, _ = run_hook("Edit", {"file_path": "/project/package-lock.json"})
        assert code == 0

    def test_block_edit_min_js(self):
        code, _, _ = run_hook("Edit", {"file_path": "/project/dist/app.min.js"})
        assert code == 2

    def test_allow_edit_node_modules_absolute(self):
        # Relative pattern "node_modules/" only prefix-matches relative paths,
        # not absolute ones like /project/node_modules/...
        code, _, _ = run_hook(
            "Edit", {"file_path": "/project/node_modules/lodash/index.js"}
        )
        assert code == 0

    def test_block_edit_node_modules_relative(self):
        # Relative path does prefix-match the relative pattern
        code, _, _ = run_hook("Edit", {"file_path": "node_modules/lodash/index.js"})
        assert code == 2

    # --- Allowed ---

    def test_allow_edit_normal(self):
        code, stdout, _ = run_hook("Edit", {"file_path": "/tmp/test.py"})
        assert code == 0
        assert stdout == ""

    def test_allow_edit_empty_path(self):
        code, _, _ = run_hook("Edit", {"file_path": ""})
        assert code == 0


class TestWriteHandler:
    # --- Zero-access blocks ---

    def test_block_write_ssh_key(self):
        code, _, stderr = run_hook("Write", {"file_path": f"{HOME}/.ssh/id_rsa"})
        assert code == 2
        assert "zero-access" in stderr.lower()

    def test_block_write_env(self):
        code, _, _ = run_hook("Write", {"file_path": "/project/.env"})
        assert code == 2

    def test_block_write_pem(self):
        code, _, _ = run_hook("Write", {"file_path": "/tmp/key.pem"})
        assert code == 2

    def test_block_write_tfstate(self):
        code, _, _ = run_hook("Write", {"file_path": "/infra/state.tfstate"})
        assert code == 2

    # --- Read-only blocks ---

    def test_block_write_bashrc(self):
        code, _, stderr = run_hook("Write", {"file_path": f"{HOME}/.bashrc"})
        assert code == 2
        assert "read-only" in stderr.lower()

    def test_block_write_etc(self):
        code, _, _ = run_hook("Write", {"file_path": "/etc/passwd"})
        assert code == 2

    def test_block_write_lock_file(self):
        code, _, _ = run_hook("Write", {"file_path": "/project/yarn.lock"})
        assert code == 2

    def test_allow_write_dist_absolute(self):
        # Relative pattern "dist/" only prefix-matches relative paths
        code, _, _ = run_hook("Write", {"file_path": "/project/dist/bundle.js"})
        assert code == 0

    def test_block_write_dist_relative(self):
        code, _, _ = run_hook("Write", {"file_path": "dist/bundle.js"})
        assert code == 2

    # --- Allowed ---

    def test_allow_write_normal(self):
        code, stdout, _ = run_hook("Write", {"file_path": "/tmp/test.py"})
        assert code == 0
        assert stdout == ""

    def test_allow_write_empty_path(self):
        code, _, _ = run_hook("Write", {"file_path": ""})
        assert code == 0


class TestDispatcher:
    def test_unknown_tool_allowed(self):
        code, stdout, _ = run_hook("WebSearch", {"query": "test"})
        assert code == 0
        assert stdout == ""

    def test_empty_tool_name(self):
        code, _, _ = run_hook("", {})
        assert code == 0

    def test_invalid_json(self):
        result = subprocess.run(
            ["uv", "run", SCRIPT],
            input="not json",
            capture_output=True,
            text=True,
            timeout=15,
        )
        assert result.returncode == 1
        assert "Error" in result.stderr

    def test_empty_stdin(self):
        result = subprocess.run(
            ["uv", "run", SCRIPT],
            input="",
            capture_output=True,
            text=True,
            timeout=15,
        )
        assert result.returncode == 1

    def test_context_truncation(self):
        """Long commands/paths should be truncated in stderr output."""
        long_cmd = "rm -rf " + "a" * 200
        code, _, stderr = run_hook("Bash", {"command": long_cmd})
        assert code == 2
