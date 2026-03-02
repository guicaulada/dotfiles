"""Tests for credential managers, scheduled execution, and misc security patterns."""

import json

from tests.conftest import run_hook


class TestCredentialManagerBlock:
    """Block patterns for credential manager access (exit code 2)."""

    # -- pass (password-store) catch-all --
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

    def test_block_pass_edit(self):
        code, _, _ = run_hook("Bash", {"command": "pass edit email/gmail"})
        assert code == 2

    def test_block_pass_init(self):
        code, _, _ = run_hook("Bash", {"command": "pass init GPGID"})
        assert code == 2

    def test_block_pass_otp(self):
        code, _, _ = run_hook("Bash", {"command": "pass otp email/gmail"})
        assert code == 2

    def test_block_pass_git(self):
        """pass git push is blocked by the pass credential manager pattern."""
        code, _, _ = run_hook("Bash", {"command": "pass git push"})
        assert code == 2

    # -- gopass (password-store alternative) catch-all --
    def test_block_gopass_show(self):
        code, _, _ = run_hook("Bash", {"command": "gopass show email/gmail"})
        assert code == 2

    def test_block_gopass_ls(self):
        code, _, _ = run_hook("Bash", {"command": "gopass ls"})
        assert code == 2

    def test_block_gopass_insert(self):
        code, _, _ = run_hook("Bash", {"command": "gopass insert email/new"})
        assert code == 2

    # -- 1Password CLI (op) catch-all --
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

    def test_block_op_read(self):
        code, _, _ = run_hook("Bash", {"command": "op read op://vault/item/field"})
        assert code == 2

    def test_block_op_inject(self):
        code, _, _ = run_hook("Bash", {"command": "op inject -i template.env"})
        assert code == 2

    # -- HashiCorp Vault catch-all --
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

    def test_block_vault_login(self):
        code, _, _ = run_hook("Bash", {"command": "vault login -method=ldap"})
        assert code == 2

    def test_block_vault_secrets(self):
        code, _, _ = run_hook("Bash", {"command": "vault secrets list"})
        assert code == 2

    # -- Bitwarden CLI (bw) catch-all --
    def test_block_bw_get(self):
        code, _, _ = run_hook("Bash", {"command": "bw get password gmail"})
        assert code == 2

    def test_block_bw_list(self):
        code, _, _ = run_hook("Bash", {"command": "bw list items"})
        assert code == 2

    def test_block_bw_unlock(self):
        code, _, _ = run_hook("Bash", {"command": "bw unlock"})
        assert code == 2

    def test_block_bw_export(self):
        code, _, _ = run_hook("Bash", {"command": "bw export --format json"})
        assert code == 2

    # -- LastPass CLI (lpass) catch-all --
    def test_block_lpass_show(self):
        code, _, _ = run_hook("Bash", {"command": "lpass show gmail"})
        assert code == 2

    def test_block_lpass_ls(self):
        code, _, _ = run_hook("Bash", {"command": "lpass ls"})
        assert code == 2

    def test_block_lpass_login(self):
        code, _, _ = run_hook("Bash", {"command": "lpass login user@example.com"})
        assert code == 2

    # -- Bitwarden CLI unofficial (rbw) catch-all --
    def test_block_rbw_get(self):
        code, _, _ = run_hook("Bash", {"command": "rbw get gmail"})
        assert code == 2

    def test_block_rbw_list(self):
        code, _, _ = run_hook("Bash", {"command": "rbw list"})
        assert code == 2

    def test_block_rbw_unlock(self):
        code, _, _ = run_hook("Bash", {"command": "rbw unlock"})
        assert code == 2

    # -- Doppler secret manager catch-all --
    def test_block_doppler_secrets(self):
        code, _, _ = run_hook("Bash", {"command": "doppler secrets"})
        assert code == 2

    def test_block_doppler_run(self):
        code, _, _ = run_hook("Bash", {"command": "doppler run -- node app.js"})
        assert code == 2

    def test_block_doppler_configure(self):
        code, _, _ = run_hook("Bash", {"command": "doppler configure"})
        assert code == 2

    # -- macOS Keychain (security) --
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

    # -- GNOME Keyring (secret-tool) --
    def test_block_secret_tool_lookup(self):
        code, _, _ = run_hook(
            "Bash", {"command": "secret-tool lookup service myservice"}
        )
        assert code == 2

    def test_block_secret_tool_store(self):
        code, _, _ = run_hook(
            "Bash", {"command": "secret-tool store --label=myservice service myservice"}
        )
        assert code == 2

    # -- KDE Wallet (kwallet-query) --
    def test_block_kwallet_query(self):
        code, _, _ = run_hook("Bash", {"command": "kwallet-query kdewallet"})
        assert code == 2


class TestCredentialTokenExposure:
    """Block and ask patterns for credential/token exposure commands."""

    # -- GPG secret key export (block) --
    def test_block_gpg_export_secret_keys(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gpg --export-secret-keys user@example.com"}
        )
        assert code == 2

    def test_block_gpg_export_secret_subkeys(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gpg --export-secret-subkeys KEYID"}
        )
        assert code == 2

    # -- printenv dump (ask) --
    def test_ask_printenv_bare(self):
        code, stdout, _ = run_hook("Bash", {"command": "printenv"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_printenv_piped(self):
        code, stdout, _ = run_hook("Bash", {"command": "printenv | grep TOKEN"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_allow_printenv_specific_var(self):
        """printenv with a specific variable name should be allowed."""
        code, _, _ = run_hook("Bash", {"command": "printenv HOME"})
        assert code == 0

    # -- export -p / declare -x (ask) --
    def test_ask_export_p(self):
        code, stdout, _ = run_hook("Bash", {"command": "export -p"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_declare_x(self):
        code, stdout, _ = run_hook("Bash", {"command": "declare -x"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestScheduledExecution:
    """Ask patterns for scheduled execution and crontab destruction block."""

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

    def test_block_crontab_remove(self):
        """crontab -r block lives in shell.yaml but is tested here thematically."""
        code, _, _ = run_hook("Bash", {"command": "crontab -r"})
        assert code == 2

    def test_block_crontab_remove_with_user(self):
        code, _, _ = run_hook("Bash", {"command": "crontab -r -u root"})
        assert code == 2


class TestMiscSecurity:
    """Block and ask patterns for chmod setuid/setgid, chattr, systemctl."""

    # -- chmod setuid/setgid (block) --
    def test_block_chmod_setuid_u(self):
        code, _, _ = run_hook("Bash", {"command": "chmod u+s /usr/local/bin/myapp"})
        assert code == 2

    def test_block_chmod_setgid_g(self):
        code, _, _ = run_hook("Bash", {"command": "chmod g+s /usr/local/bin/myapp"})
        assert code == 2

    def test_block_chmod_setuid_bare(self):
        """chmod +s without specifying u/g/o/a."""
        code, _, _ = run_hook("Bash", {"command": "chmod +s /usr/local/bin/myapp"})
        assert code == 2

    def test_block_chmod_setuid_numeric_4755(self):
        """Numeric setuid: 4755."""
        code, _, _ = run_hook("Bash", {"command": "chmod 4755 /usr/local/bin/myapp"})
        assert code == 2

    def test_block_chmod_setgid_numeric_2755(self):
        """Numeric setgid: 2755."""
        code, _, _ = run_hook("Bash", {"command": "chmod 2755 /usr/local/bin/myapp"})
        assert code == 2

    def test_block_chmod_setuid_oa(self):
        """chmod oa+s (other and all)."""
        code, _, _ = run_hook("Bash", {"command": "chmod oa+s /tmp/exploit"})
        assert code == 2

    # -- chattr (ask) --
    def test_ask_chattr(self):
        code, stdout, _ = run_hook("Bash", {"command": "chattr +i important_file"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_chattr_recursive(self):
        code, stdout, _ = run_hook("Bash", {"command": "chattr -R +a /var/log"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # -- systemctl start/restart/enable/unmask (ask) --
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

    def test_ask_systemctl_unmask(self):
        code, stdout, _ = run_hook("Bash", {"command": "systemctl unmask firewalld"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
