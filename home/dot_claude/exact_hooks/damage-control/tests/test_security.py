"""Tests for credential managers, scheduled execution, and misc security patterns."""

import json

from tests.conftest import assert_asks, run_hook


class TestCredentialManagerBlock:
    """Block patterns for credential manager access (exit code 2)."""

    # -- pass (password-store) catch-all --
    def test_block_pass_show(self):
        assert_asks('Bash', {'command': 'pass show email/gmail'})

    def test_block_pass_ls(self):
        assert_asks('Bash', {'command': 'pass ls'})

    def test_block_pass_insert(self):
        assert_asks('Bash', {'command': 'pass insert email/new'})

    def test_block_pass_rm(self):
        assert_asks('Bash', {'command': 'pass rm email/old'})

    def test_block_pass_generate(self):
        assert_asks('Bash', {'command': 'pass generate email/new 20'})

    def test_block_pass_edit(self):
        assert_asks('Bash', {'command': 'pass edit email/gmail'})

    def test_block_pass_init(self):
        assert_asks('Bash', {'command': 'pass init GPGID'})

    def test_block_pass_otp(self):
        assert_asks('Bash', {'command': 'pass otp email/gmail'})

    def test_block_pass_git(self):
        """pass git push is blocked by the pass credential manager pattern."""
        assert_asks('Bash', {'command': 'pass git push'})

    # -- gopass (password-store alternative) catch-all --
    def test_block_gopass_show(self):
        assert_asks('Bash', {'command': 'gopass show email/gmail'})

    def test_block_gopass_ls(self):
        assert_asks('Bash', {'command': 'gopass ls'})

    def test_block_gopass_insert(self):
        assert_asks('Bash', {'command': 'gopass insert email/new'})

    # -- 1Password CLI (op) catch-all --
    def test_block_op_item(self):
        assert_asks('Bash', {'command': 'op item get MyLogin'})

    def test_block_op_vault(self):
        assert_asks('Bash', {'command': 'op vault list'})

    def test_block_op_document(self):
        assert_asks('Bash', {'command': 'op document get mydoc'})

    def test_block_op_whoami(self):
        assert_asks('Bash', {'command': 'op whoami'})

    def test_block_op_signin(self):
        assert_asks('Bash', {'command': 'op signin'})

    def test_block_op_read(self):
        assert_asks('Bash', {'command': 'op read op://vault/item/field'})

    def test_block_op_inject(self):
        assert_asks("Bash", {"command": "op inject -i template.env"})

    # -- HashiCorp Vault catch-all --
    def test_block_vault_read(self):
        assert_asks('Bash', {'command': 'vault read secret/data/myapp'})

    def test_block_vault_write(self):
        assert_asks('Bash', {'command': 'vault write secret/data/myapp key=value'})

    def test_block_vault_delete(self):
        assert_asks('Bash', {'command': 'vault delete secret/data/myapp'})

    def test_block_vault_kv(self):
        assert_asks('Bash', {'command': 'vault kv get secret/myapp'})

    def test_block_vault_token(self):
        assert_asks('Bash', {'command': 'vault token lookup'})

    def test_block_vault_status(self):
        assert_asks('Bash', {'command': 'vault status'})

    def test_block_vault_seal(self):
        assert_asks('Bash', {'command': 'vault seal'})

    def test_block_vault_unseal(self):
        assert_asks('Bash', {'command': 'vault unseal'})

    def test_block_vault_login(self):
        assert_asks('Bash', {'command': 'vault login -method=ldap'})

    def test_block_vault_secrets(self):
        assert_asks('Bash', {'command': 'vault secrets list'})

    # -- Bitwarden CLI (bw) catch-all --
    def test_block_bw_get(self):
        assert_asks('Bash', {'command': 'bw get password gmail'})

    def test_block_bw_list(self):
        assert_asks('Bash', {'command': 'bw list items'})

    def test_block_bw_unlock(self):
        assert_asks('Bash', {'command': 'bw unlock'})

    def test_block_bw_export(self):
        assert_asks('Bash', {'command': 'bw export --format json'})

    # -- LastPass CLI (lpass) catch-all --
    def test_block_lpass_show(self):
        assert_asks('Bash', {'command': 'lpass show gmail'})

    def test_block_lpass_ls(self):
        assert_asks('Bash', {'command': 'lpass ls'})

    def test_block_lpass_login(self):
        assert_asks('Bash', {'command': 'lpass login user@example.com'})

    # -- Bitwarden CLI unofficial (rbw) catch-all --
    def test_block_rbw_get(self):
        assert_asks('Bash', {'command': 'rbw get gmail'})

    def test_block_rbw_list(self):
        assert_asks('Bash', {'command': 'rbw list'})

    def test_block_rbw_unlock(self):
        assert_asks('Bash', {'command': 'rbw unlock'})

    # -- Doppler secret manager catch-all --
    def test_block_doppler_secrets(self):
        assert_asks('Bash', {'command': 'doppler secrets'})

    def test_block_doppler_run(self):
        assert_asks('Bash', {'command': 'doppler run -- node app.js'})

    def test_block_doppler_configure(self):
        assert_asks('Bash', {'command': 'doppler configure'})

    # -- macOS Keychain (security) --
    def test_block_security_find_generic_password(self):
        assert_asks('Bash', {'command': 'security find-generic-password -s myservice'})

    def test_block_security_find_internet_password(self):
        assert_asks('Bash', {'command': 'security find-internet-password -s example.com'})

    def test_block_security_dump_keychain(self):
        assert_asks('Bash', {'command': 'security dump-keychain'})

    def test_block_security_show_keychain_info(self):
        assert_asks('Bash', {'command': 'security show-keychain-info login.keychain'})

    def test_block_security_find_certificate(self):
        assert_asks('Bash', {'command': 'security find-certificate -a'})

    def test_block_security_find_identity(self):
        assert_asks('Bash', {'command': 'security find-identity -v -p codesigning'})

    # -- GNOME Keyring (secret-tool) --
    def test_block_secret_tool_lookup(self):
        assert_asks('Bash', {'command': 'secret-tool lookup service myservice'})

    def test_block_secret_tool_store(self):
        assert_asks('Bash', {'command': 'secret-tool store --label=myservice service myservice'})

    # -- KDE Wallet (kwallet-query) --
    def test_block_kwallet_query(self):
        assert_asks('Bash', {'command': 'kwallet-query kdewallet'})


class TestCredentialTokenExposure:
    """Block and ask patterns for credential/token exposure commands."""

    # -- GPG secret key export (block) --
    def test_block_gpg_export_secret_keys(self):
        assert_asks('Bash', {'command': 'gpg --export-secret-keys user@example.com'})

    def test_block_gpg_export_secret_subkeys(self):
        assert_asks('Bash', {'command': 'gpg --export-secret-subkeys KEYID'})

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
        assert_asks('Bash', {'command': 'crontab -r'})

    def test_block_crontab_remove_with_user(self):
        assert_asks('Bash', {'command': 'crontab -r -u root'})


class TestMiscSecurity:
    """Block and ask patterns for chmod setuid/setgid, chattr, systemctl."""

    # -- chmod setuid/setgid (block) --
    def test_block_chmod_setuid_u(self):
        assert_asks("Bash", {"command": "chmod u+s /usr/local/bin/myapp"})

    def test_block_chmod_setgid_g(self):
        assert_asks("Bash", {"command": "chmod g+s /usr/local/bin/myapp"})

    def test_block_chmod_setuid_bare(self):
        """chmod +s without specifying u/g/o/a."""
        assert_asks("Bash", {"command": "chmod +s /usr/local/bin/myapp"})

    def test_block_chmod_setuid_numeric_4755(self):
        """Numeric setuid: 4755."""
        assert_asks("Bash", {"command": "chmod 4755 /usr/local/bin/myapp"})

    def test_block_chmod_setgid_numeric_2755(self):
        """Numeric setgid: 2755."""
        assert_asks("Bash", {"command": "chmod 2755 /usr/local/bin/myapp"})

    def test_block_chmod_setuid_oa(self):
        """chmod oa+s (other and all)."""
        assert_asks('Bash', {'command': 'chmod oa+s /tmp/exploit'})

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
