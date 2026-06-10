"""Tests for Read, Edit, Write, Grep handlers and the dispatcher."""

import subprocess

import pytest

from tests.conftest import HOME, SCRIPT, assert_asks, dc, run_hook


class TestReadHandler:
    # --- Zero-access asks ---

    def test_block_ssh_key(self):
        reason = assert_asks("Read", {"file_path": f"{HOME}/.ssh/id_rsa"})
        assert "zero-access" in reason.lower()

    def test_block_env_file(self):
        assert_asks("Read", {"file_path": "/project/.env"})

    def test_block_env_local(self):
        assert_asks("Read", {"file_path": "/project/.env.local"})

    def test_block_pem_file(self):
        assert_asks("Read", {"file_path": "/tmp/server.pem"})

    def test_block_key_file(self):
        assert_asks("Read", {"file_path": "/tmp/private.key"})

    def test_block_aws_credentials(self):
        assert_asks("Read", {"file_path": f"{HOME}/.aws/credentials"})

    def test_block_kube_config(self):
        assert_asks("Read", {"file_path": f"{HOME}/.kube/config"})

    def test_block_docker_config(self):
        assert_asks("Read", {"file_path": f"{HOME}/.docker/config.json"})

    def test_block_gnupg(self):
        assert_asks("Read", {"file_path": f"{HOME}/.gnupg/secring.gpg"})

    def test_block_tfstate(self):
        assert_asks("Read", {"file_path": "/infra/terraform.tfstate"})

    def test_block_tfvars(self):
        assert_asks("Read", {"file_path": "/infra/prod.tfvars"})

    def test_block_credentials_json(self):
        assert_asks("Read", {"file_path": "/tmp/gcp-credentials.json"})

    def test_block_service_account(self):
        assert_asks("Read", {"file_path": "/tmp/myServiceAccountKey.json"})

    def test_block_netrc(self):
        assert_asks("Read", {"file_path": f"{HOME}/.netrc"})

    def test_block_git_credentials(self):
        assert_asks("Read", {"file_path": f"{HOME}/.git-credentials"})

    def test_block_keystore(self):
        assert_asks("Read", {"file_path": "/app/release.keystore"})

    # --- Credential manager zero-access asks ---

    def test_block_read_password_store(self):
        assert_asks("Read", {"file_path": f"{HOME}/.password-store/email/gmail.gpg"})

    def test_block_read_op_config(self):
        assert_asks("Read", {"file_path": f"{HOME}/.config/op/config"})

    def test_block_read_vault_token(self):
        assert_asks("Read", {"file_path": f"{HOME}/.vault-token"})

    def test_block_read_gnome_keyrings(self):
        assert_asks(
            "Read", {"file_path": f"{HOME}/.local/share/keyrings/default.keyring"}
        )

    def test_block_read_kde_wallet(self):
        assert_asks(
            "Read", {"file_path": f"{HOME}/.local/share/kwalletd/kdewallet.kwl"}
        )

    def test_block_read_macos_keychain(self):
        assert_asks(
            "Read", {"file_path": f"{HOME}/Library/Keychains/login.keychain-db"}
        )

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
    # --- Zero-access asks ---

    def test_block_grep_ssh(self):
        reason = assert_asks("Grep", {"pattern": "password", "path": f"{HOME}/.ssh/"})
        assert "zero-access" in reason.lower()

    def test_block_grep_aws(self):
        assert_asks("Grep", {"pattern": "key", "path": f"{HOME}/.aws/"})

    def test_block_grep_kube(self):
        assert_asks("Grep", {"pattern": "token", "path": f"{HOME}/.kube/"})

    def test_block_grep_gnupg(self):
        assert_asks("Grep", {"pattern": "secret", "path": f"{HOME}/.gnupg/"})

    def test_block_grep_gcloud(self):
        assert_asks("Grep", {"pattern": "token", "path": f"{HOME}/.config/gcloud/"})

    def test_block_grep_env_file(self):
        assert_asks("Grep", {"pattern": "SECRET", "path": "/project/.env"})

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
    # --- Zero-access asks ---

    def test_block_edit_ssh_config(self):
        reason = assert_asks("Edit", {"file_path": f"{HOME}/.ssh/config"})
        assert "zero-access" in reason.lower()

    def test_block_edit_env(self):
        assert_asks("Edit", {"file_path": "/project/.env"})

    def test_block_edit_pem(self):
        assert_asks("Edit", {"file_path": "/tmp/cert.pem"})

    def test_block_edit_aws(self):
        assert_asks("Edit", {"file_path": f"{HOME}/.aws/config"})

    # --- Read-only asks ---

    def test_block_edit_bashrc(self):
        reason = assert_asks("Edit", {"file_path": f"{HOME}/.bashrc"})
        assert "read-only" in reason.lower()

    def test_block_edit_zshrc(self):
        assert_asks("Edit", {"file_path": f"{HOME}/.zshrc"})

    def test_block_edit_etc(self):
        assert_asks("Edit", {"file_path": "/etc/hosts"})

    def test_block_edit_lock_file(self):
        # yarn.lock matches via *.lock glob pattern
        assert_asks("Edit", {"file_path": "/project/yarn.lock"})

    def test_allow_edit_lock_json(self):
        # package-lock.json ends in .json, not .lock; literal "package-lock.json"
        # only prefix-matches, so absolute paths don't match
        code, _, _ = run_hook("Edit", {"file_path": "/project/package-lock.json"})
        assert code == 0

    def test_block_edit_min_js(self):
        assert_asks("Edit", {"file_path": "/project/dist/app.min.js"})

    def test_allow_edit_node_modules_absolute(self):
        # Relative pattern "node_modules/" only prefix-matches relative paths,
        # not absolute ones like /project/node_modules/...
        code, _, _ = run_hook(
            "Edit", {"file_path": "/project/node_modules/lodash/index.js"}
        )
        assert code == 0

    def test_block_edit_node_modules_relative(self):
        # Relative path does prefix-match the relative pattern
        assert_asks("Edit", {"file_path": "node_modules/lodash/index.js"})

    # --- Allowed ---

    def test_allow_edit_normal(self):
        code, stdout, _ = run_hook("Edit", {"file_path": "/tmp/test.py"})
        assert code == 0
        assert stdout == ""

    def test_allow_edit_empty_path(self):
        code, _, _ = run_hook("Edit", {"file_path": ""})
        assert code == 0


class TestWriteHandler:
    # --- Zero-access asks ---

    def test_block_write_ssh_key(self):
        reason = assert_asks("Write", {"file_path": f"{HOME}/.ssh/id_rsa"})
        assert "zero-access" in reason.lower()

    def test_block_write_env(self):
        assert_asks("Write", {"file_path": "/project/.env"})

    def test_block_write_pem(self):
        assert_asks("Write", {"file_path": "/tmp/key.pem"})

    def test_block_write_tfstate(self):
        assert_asks("Write", {"file_path": "/infra/state.tfstate"})

    # --- Read-only asks ---

    def test_block_write_bashrc(self):
        reason = assert_asks("Write", {"file_path": f"{HOME}/.bashrc"})
        assert "read-only" in reason.lower()

    def test_block_write_etc(self):
        assert_asks("Write", {"file_path": "/etc/passwd"})

    def test_block_write_lock_file(self):
        assert_asks("Write", {"file_path": "/project/yarn.lock"})

    def test_allow_write_dist_absolute(self):
        # Relative pattern "dist/" only prefix-matches relative paths
        code, _, _ = run_hook("Write", {"file_path": "/project/dist/bundle.js"})
        assert code == 0

    def test_block_write_dist_relative(self):
        assert_asks("Write", {"file_path": "dist/bundle.js"})

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

    def test_context_truncation(self, capsys):
        """The _block helper truncates long context in stderr output.

        Path protections only hard-block when the entry opts in via
        `block: true`, so drive handle_bash directly with such a config to
        exercise the truncation path.
        """
        long_cmd = "cat /etc/secret " + "a" * 200
        config = {"zeroAccessPaths": [{"path": "/etc/secret", "block": True}]}
        with pytest.raises(SystemExit) as exc_info:
            dc.handle_bash({"command": long_cmd}, config)
        assert exc_info.value.code == 2
        stderr = capsys.readouterr().err
        assert "SECURITY" in stderr
        assert "..." in stderr
