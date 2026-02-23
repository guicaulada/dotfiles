"""Tests for credential managers, scheduled execution, and misc security patterns."""

import json

from tests.conftest import run_hook


class TestCredentialManagerBlock:
    def test_block_pass_show(self):
        code, _, _ = run_hook("Bash", {"command": "pass show email/gmail"})
        assert code == 2

    def test_block_pass_ls(self):
        code, _, _ = run_hook("Bash", {"command": "pass ls"})
        assert code == 2

    def test_block_pass_insert(self):
        code, _, _ = run_hook("Bash", {"command": "pass insert email/new"})
        assert code == 2

    def test_block_pass_rm(self):
        code, _, _ = run_hook("Bash", {"command": "pass rm email/old"})
        assert code == 2

    def test_block_pass_generate(self):
        code, _, _ = run_hook("Bash", {"command": "pass generate email/new 20"})
        assert code == 2

    def test_ask_pass_git(self):
        code, stdout, _ = run_hook("Bash", {"command": "pass git push"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_block_pass_edit(self):
        code, _, _ = run_hook("Bash", {"command": "pass edit email/gmail"})
        assert code == 2

    def test_block_op_item(self):
        code, _, _ = run_hook("Bash", {"command": "op item get MyLogin"})
        assert code == 2

    def test_block_op_vault(self):
        code, _, _ = run_hook("Bash", {"command": "op vault list"})
        assert code == 2

    def test_block_op_document(self):
        code, _, _ = run_hook("Bash", {"command": "op document get mydoc"})
        assert code == 2

    def test_block_op_whoami(self):
        code, _, _ = run_hook("Bash", {"command": "op whoami"})
        assert code == 2

    def test_block_op_signin(self):
        code, _, _ = run_hook("Bash", {"command": "op signin"})
        assert code == 2

    def test_block_vault_read(self):
        code, _, _ = run_hook("Bash", {"command": "vault read secret/data/myapp"})
        assert code == 2

    def test_block_vault_write(self):
        code, _, _ = run_hook(
            "Bash", {"command": "vault write secret/data/myapp key=value"}
        )
        assert code == 2

    def test_block_vault_delete(self):
        code, _, _ = run_hook("Bash", {"command": "vault delete secret/data/myapp"})
        assert code == 2

    def test_block_vault_kv(self):
        code, _, _ = run_hook("Bash", {"command": "vault kv get secret/myapp"})
        assert code == 2

    def test_block_vault_token(self):
        code, _, _ = run_hook("Bash", {"command": "vault token lookup"})
        assert code == 2

    def test_block_vault_status(self):
        code, _, _ = run_hook("Bash", {"command": "vault status"})
        assert code == 2

    def test_block_vault_seal(self):
        code, _, _ = run_hook("Bash", {"command": "vault seal"})
        assert code == 2

    def test_block_vault_unseal(self):
        code, _, _ = run_hook("Bash", {"command": "vault unseal"})
        assert code == 2

    def test_block_security_find_generic_password(self):
        code, _, _ = run_hook(
            "Bash", {"command": "security find-generic-password -s myservice"}
        )
        assert code == 2

    def test_block_security_find_internet_password(self):
        code, _, _ = run_hook(
            "Bash", {"command": "security find-internet-password -s example.com"}
        )
        assert code == 2

    def test_block_security_dump_keychain(self):
        code, _, _ = run_hook("Bash", {"command": "security dump-keychain"})
        assert code == 2

    def test_block_security_show_keychain_info(self):
        code, _, _ = run_hook(
            "Bash", {"command": "security show-keychain-info login.keychain"}
        )
        assert code == 2

    def test_block_security_find_certificate(self):
        code, _, _ = run_hook("Bash", {"command": "security find-certificate -a"})
        assert code == 2

    def test_block_security_find_identity(self):
        code, _, _ = run_hook(
            "Bash", {"command": "security find-identity -v -p codesigning"}
        )
        assert code == 2

    def test_block_secret_tool(self):
        code, _, _ = run_hook(
            "Bash", {"command": "secret-tool lookup service myservice"}
        )
        assert code == 2

    def test_block_kwallet_query(self):
        code, _, _ = run_hook("Bash", {"command": "kwallet-query kdewallet"})
        assert code == 2


class TestMiscSecurity:
    def test_block_chmod_setuid(self):
        code, _, _ = run_hook("Bash", {"command": "chmod u+s /usr/local/bin/myapp"})
        assert code == 2

    def test_block_chmod_setgid(self):
        code, _, _ = run_hook("Bash", {"command": "chmod g+s /usr/local/bin/myapp"})
        assert code == 2

    def test_ask_chattr(self):
        code, stdout, _ = run_hook("Bash", {"command": "chattr +i important_file"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_systemctl_start(self):
        code, stdout, _ = run_hook("Bash", {"command": "systemctl start nginx"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_systemctl_restart(self):
        code, stdout, _ = run_hook("Bash", {"command": "systemctl restart docker"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_systemctl_enable(self):
        code, stdout, _ = run_hook("Bash", {"command": "systemctl enable sshd"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestScheduledExecution:
    def test_ask_crontab_file(self):
        code, stdout, _ = run_hook("Bash", {"command": "crontab mycron.txt"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_at(self):
        code, stdout, _ = run_hook("Bash", {"command": "at now + 1 hour"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_batch(self):
        code, stdout, _ = run_hook("Bash", {"command": "batch"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
