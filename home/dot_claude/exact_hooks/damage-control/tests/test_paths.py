"""Tests for zero-access, read-only, and no-delete path enforcement in Bash handler."""

from tests.conftest import HOME, run_hook

# =============================================================================
# ZERO ACCESS PATHS
# =============================================================================


class TestZeroAccessEnvFiles:
    """Environment files (.env variants) - block ALL operations."""

    def test_block_cat_env(self):
        code, _, stderr = run_hook("Bash", {"command": "cat .env"})
        assert code == 2
        assert "zero-access" in stderr.lower()

    def test_block_cat_env_local(self):
        code, _, _ = run_hook("Bash", {"command": "cat .env.local"})
        assert code == 2

    def test_block_cat_env_production(self):
        code, _, _ = run_hook("Bash", {"command": "cat .env.production"})
        assert code == 2

    def test_block_cat_env_development_local(self):
        code, _, _ = run_hook("Bash", {"command": "cat .env.development.local"})
        assert code == 2

    def test_block_cat_app_env(self):
        code, _, _ = run_hook("Bash", {"command": "cat app.env"})
        assert code == 2


class TestZeroAccessSSHAndGPG:
    """SSH and GPG directories - block ALL operations."""

    def test_block_cat_ssh_id_rsa(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.ssh/id_rsa"})
        assert code == 2

    def test_block_cat_ssh_config(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.ssh/config"})
        assert code == 2

    def test_block_cat_gnupg(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.gnupg/trustdb.gpg"})
        assert code == 2


class TestZeroAccessCloudCredentials:
    """Cloud provider credentials - block ALL operations."""

    def test_block_cat_aws(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.aws/credentials"})
        assert code == 2

    def test_block_cat_gcloud(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": f"cat {HOME}/.config/gcloud/application_default_credentials.json"
            },
        )
        assert code == 2

    def test_block_cat_credentials_json(self):
        code, _, _ = run_hook("Bash", {"command": "cat credentials.json"})
        assert code == 2

    def test_block_cat_prefixed_credentials_json(self):
        code, _, _ = run_hook("Bash", {"command": "cat gcp-credentials.json"})
        assert code == 2

    def test_block_cat_service_account(self):
        code, _, _ = run_hook("Bash", {"command": "cat myServiceAccount.json"})
        assert code == 2

    def test_block_cat_service_account_hyphen(self):
        code, _, _ = run_hook("Bash", {"command": "cat my-service-account-key.json"})
        assert code == 2

    def test_block_cat_azure(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.azure/profile"})
        assert code == 2

    def test_block_cat_kube(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.kube/config"})
        assert code == 2

    def test_block_cat_kubeconfig(self):
        code, _, _ = run_hook("Bash", {"command": "cat kubeconfig"})
        assert code == 2

    def test_block_cat_k8s_secret_yaml(self):
        code, _, _ = run_hook("Bash", {"command": "cat db-secret.yaml"})
        assert code == 2

    def test_block_cat_secrets_yaml(self):
        code, _, _ = run_hook("Bash", {"command": "cat secrets.yaml"})
        assert code == 2

    def test_block_cat_secrets_dir(self):
        code, _, _ = run_hook("Bash", {"command": "cat secrets/db-password.txt"})
        assert code == 2

    def test_block_cat_docker_config(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.docker/config.json"})
        assert code == 2


class TestZeroAccessCertificates:
    """SSL/TLS certificates and private keys - block ALL operations."""

    def test_block_cat_pem(self):
        code, _, _ = run_hook("Bash", {"command": "cat server.pem"})
        assert code == 2

    def test_block_cat_key(self):
        code, _, _ = run_hook("Bash", {"command": "cat private.key"})
        assert code == 2

    def test_block_cat_p12(self):
        code, _, _ = run_hook("Bash", {"command": "cat certificate.p12"})
        assert code == 2

    def test_block_cat_pfx(self):
        code, _, _ = run_hook("Bash", {"command": "cat certificate.pfx"})
        assert code == 2

    def test_block_cat_csr(self):
        code, _, _ = run_hook("Bash", {"command": "cat server.csr"})
        assert code == 2

    def test_block_cat_cert(self):
        code, _, _ = run_hook("Bash", {"command": "cat server.cert"})
        assert code == 2

    def test_block_cat_cer(self):
        code, _, _ = run_hook("Bash", {"command": "cat server.cer"})
        assert code == 2

    def test_block_cat_der(self):
        code, _, _ = run_hook("Bash", {"command": "cat server.der"})
        assert code == 2


class TestZeroAccessTerraform:
    """Terraform state and variables - block ALL operations."""

    def test_block_cat_tfstate(self):
        code, _, _ = run_hook("Bash", {"command": "cat terraform.tfstate"})
        assert code == 2

    def test_block_cat_tfstate_backup(self):
        code, _, _ = run_hook("Bash", {"command": "cat terraform.tfstate.backup"})
        assert code == 2

    def test_block_cat_tfvars(self):
        code, _, _ = run_hook("Bash", {"command": "cat prod.tfvars"})
        assert code == 2


class TestZeroAccessTokens:
    """Token files - block ALL operations."""

    def test_block_cat_dot_token(self):
        code, _, _ = run_hook("Bash", {"command": "cat .token"})
        assert code == 2

    def test_block_cat_glob_token(self):
        code, _, _ = run_hook("Bash", {"command": "cat github.token"})
        assert code == 2

    def test_block_cat_token_json(self):
        code, _, _ = run_hook("Bash", {"command": "cat token.json"})
        assert code == 2

    def test_block_cat_tokens_json(self):
        code, _, _ = run_hook("Bash", {"command": "cat tokens.json"})
        assert code == 2


class TestZeroAccessOAuth:
    """OAuth and client secret files - block ALL operations."""

    def test_block_cat_oauth_json(self):
        code, _, _ = run_hook("Bash", {"command": "cat oauth-config.json"})
        assert code == 2

    def test_block_cat_client_secret_json(self):
        code, _, _ = run_hook("Bash", {"command": "cat client_secret_12345.json"})
        assert code == 2

    def test_block_cat_client_secret_hyphen(self):
        code, _, _ = run_hook("Bash", {"command": "cat client-secret-google.json"})
        assert code == 2


class TestZeroAccessAnsibleVault:
    """Ansible vault files - block ALL operations."""

    def test_block_cat_vault_yml(self):
        code, _, _ = run_hook("Bash", {"command": "cat vault.yml"})
        assert code == 2

    def test_block_cat_vault_yaml(self):
        code, _, _ = run_hook("Bash", {"command": "cat vault.yaml"})
        assert code == 2

    def test_block_cat_prefixed_vault_yml(self):
        code, _, _ = run_hook("Bash", {"command": "cat prod-vault.yml"})
        assert code == 2

    def test_block_cat_underscore_vault_yaml(self):
        code, _, _ = run_hook("Bash", {"command": "cat staging_vault.yaml"})
        assert code == 2


class TestZeroAccessAgeSops:
    """Age and SOPS encryption files - block ALL operations."""

    def test_block_cat_age_file(self):
        code, _, _ = run_hook("Bash", {"command": "cat keys.age"})
        assert code == 2

    def test_block_cat_sops_yaml(self):
        code, _, _ = run_hook("Bash", {"command": "cat .sops.yaml"})
        assert code == 2

    def test_block_cat_sops_yml(self):
        code, _, _ = run_hook("Bash", {"command": "cat .sops.yml"})
        assert code == 2


class TestZeroAccessApiKeys:
    """API key files - block ALL operations."""

    def test_block_cat_api_key_hyphen(self):
        code, _, _ = run_hook("Bash", {"command": "cat stripe-api-key.txt"})
        assert code == 2

    def test_block_cat_api_key_underscore(self):
        code, _, _ = run_hook("Bash", {"command": "cat openai_api_key.env"})
        assert code == 2

    def test_block_cat_dot_api_key(self):
        code, _, _ = run_hook("Bash", {"command": "cat .api_key"})
        assert code == 2

    def test_block_cat_dot_apikey(self):
        code, _, _ = run_hook("Bash", {"command": "cat .apikey"})
        assert code == 2

    def test_block_cat_api_keys_json(self):
        code, _, _ = run_hook("Bash", {"command": "cat api-keys.json"})
        assert code == 2

    def test_block_cat_api_keys_yaml(self):
        code, _, _ = run_hook("Bash", {"command": "cat api_keys.yaml"})
        assert code == 2


class TestZeroAccessAuthConfig:
    """Auth config files - block ALL operations."""

    def test_block_cat_authinfo(self):
        code, _, _ = run_hook("Bash", {"command": "cat .authinfo"})
        assert code == 2

    def test_block_cat_authinfo_gpg(self):
        code, _, _ = run_hook("Bash", {"command": "cat .authinfo.gpg"})
        assert code == 2


class TestZeroAccessHelmSecrets:
    """Helm secret files - block ALL operations."""

    def test_block_cat_secrets_yml(self):
        code, _, _ = run_hook("Bash", {"command": "cat secrets.yml"})
        assert code == 2


class TestZeroAccessCredentialStores:
    """Credential managers and secret stores - block ALL operations."""

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

    def test_block_cat_gnome_keyrings(self):
        code, _, _ = run_hook(
            "Bash", {"command": f"cat {HOME}/.gnome2/keyrings/default.keyring"}
        )
        assert code == 2

    def test_block_cat_kwalletd(self):
        code, _, _ = run_hook(
            "Bash", {"command": f"cat {HOME}/.local/share/kwalletd/kdewallet.kwl"}
        )
        assert code == 2

    def test_block_cat_macos_keychains(self):
        code, _, _ = run_hook(
            "Bash", {"command": f"cat {HOME}/Library/Keychains/login.keychain-db"}
        )
        assert code == 2

    def test_block_cat_1password_config(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.config/op/config"})
        assert code == 2


class TestZeroAccessPlatformCredentials:
    """Additional cloud and platform credentials - block ALL operations."""

    def test_block_cat_wrangler(self):
        code, _, _ = run_hook(
            "Bash", {"command": f"cat {HOME}/.config/wrangler/config/default.toml"}
        )
        assert code == 2

    def test_block_cat_project_wrangler(self):
        code, _, _ = run_hook("Bash", {"command": "cat .wrangler/state.json"})
        assert code == 2

    def test_block_cat_fly(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.fly/config.yml"})
        assert code == 2

    def test_block_cat_heroku(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.heroku/credentials"})
        assert code == 2

    def test_block_cat_doctl(self):
        code, _, _ = run_hook(
            "Bash", {"command": f"cat {HOME}/.config/doctl/config.yaml"}
        )
        assert code == 2

    def test_block_cat_bitwarden_cli(self):
        code, _, _ = run_hook(
            "Bash", {"command": f"cat '{HOME}/.config/Bitwarden CLI/data.json'"}
        )
        assert code == 2

    def test_block_cat_pulumi_credentials(self):
        code, _, _ = run_hook(
            "Bash", {"command": f"cat {HOME}/.pulumi/credentials.json"}
        )
        assert code == 2


class TestZeroAccessBrowserProfiles:
    """Browser profiles - block ALL operations."""

    def test_block_cat_mozilla(self):
        code, _, _ = run_hook(
            "Bash", {"command": f"cat {HOME}/.mozilla/firefox/profile/logins.json"}
        )
        assert code == 2

    def test_block_cat_chrome_mac(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": f"cat '{HOME}/Library/Application Support/Google/Chrome/Default/Login Data'"
            },
        )
        assert code == 2

    def test_block_cat_firefox_mac(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": f"cat '{HOME}/Library/Application Support/Firefox/profiles.ini'"
            },
        )
        assert code == 2

    def test_block_cat_chromium_linux(self):
        code, _, _ = run_hook(
            "Bash", {"command": f"cat {HOME}/.config/chromium/Default/Cookies"}
        )
        assert code == 2

    def test_block_cat_brave_linux(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": f"cat {HOME}/.config/BraveSoftware/Brave-Browser/Default/Cookies"
            },
        )
        assert code == 2


class TestZeroAccessPackageAuth:
    """Package manager auth files - block ALL operations."""

    def test_block_cat_netrc(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.netrc"})
        assert code == 2

    def test_block_cat_npmrc_global(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.npmrc"})
        assert code == 2

    def test_block_cat_npmrc_project(self):
        code, _, _ = run_hook("Bash", {"command": "cat .npmrc"})
        assert code == 2

    def test_block_cat_pypirc(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.pypirc"})
        assert code == 2

    def test_block_cat_git_credentials(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.git-credentials"})
        assert code == 2

    def test_block_cat_gh_hosts(self):
        code, _, _ = run_hook("Bash", {"command": f"cat {HOME}/.config/gh/hosts.yml"})
        assert code == 2

    def test_block_cat_cargo_credentials(self):
        code, _, _ = run_hook(
            "Bash", {"command": f"cat {HOME}/.cargo/credentials.toml"}
        )
        assert code == 2


class TestZeroAccessMisc:
    """Miscellaneous zero-access paths."""

    def test_block_cat_htpasswd(self):
        code, _, _ = run_hook("Bash", {"command": "cat .htpasswd"})
        assert code == 2

    def test_block_cat_keystore(self):
        code, _, _ = run_hook("Bash", {"command": "cat release.keystore"})
        assert code == 2

    def test_block_cat_jks(self):
        code, _, _ = run_hook("Bash", {"command": "cat server.jks"})
        assert code == 2

    def test_block_cat_dump_sql(self):
        code, _, _ = run_hook("Bash", {"command": "cat dump.sql"})
        assert code == 2

    def test_block_cat_backup_sql(self):
        code, _, _ = run_hook("Bash", {"command": "cat backup.sql"})
        assert code == 2

    def test_block_cat_dump_file(self):
        code, _, _ = run_hook("Bash", {"command": "cat database.dump"})
        assert code == 2

    def test_block_cat_dot_secret(self):
        code, _, _ = run_hook("Bash", {"command": "cat .secret"})
        assert code == 2

    def test_block_cat_dot_secrets(self):
        code, _, _ = run_hook("Bash", {"command": "cat .secrets"})
        assert code == 2

    def test_block_cat_glob_secret(self):
        code, _, _ = run_hook("Bash", {"command": "cat app.secret"})
        assert code == 2

    def test_block_cat_firebase_admin(self):
        code, _, _ = run_hook("Bash", {"command": "cat firebase-adminsdk-abcde.json"})
        assert code == 2

    def test_block_cat_service_account_key(self):
        code, _, _ = run_hook("Bash", {"command": "cat serviceAccountKey.json"})
        assert code == 2

    def test_block_cat_vercel_dir(self):
        code, _, _ = run_hook("Bash", {"command": "cat .vercel/project.json"})
        assert code == 2

    def test_block_cat_netlify_dir(self):
        code, _, _ = run_hook("Bash", {"command": "cat .netlify/state.json"})
        assert code == 2

    def test_block_cat_supabase_dir(self):
        code, _, _ = run_hook("Bash", {"command": "cat .supabase/config.toml"})
        assert code == 2

    def test_block_cat_terraform_dir(self):
        code, _, _ = run_hook("Bash", {"command": "cat .terraform/terraform.tfstate"})
        assert code == 2


# =============================================================================
# READ-ONLY PATHS
# =============================================================================


class TestReadOnlySystemDirs:
    """System directories - allow read, block write/edit/delete."""

    def test_block_write_etc(self):
        code, _, _ = run_hook("Bash", {"command": "echo data > /etc/hosts"})
        assert code == 2

    def test_block_write_usr(self):
        code, _, _ = run_hook("Bash", {"command": "echo data > /usr/local/bin/test"})
        assert code == 2

    def test_block_rm_bin(self):
        code, _, _ = run_hook("Bash", {"command": "rm /bin/ls"})
        assert code == 2

    def test_block_rm_sbin(self):
        code, _, _ = run_hook("Bash", {"command": "rm /sbin/init"})
        assert code == 2

    def test_block_write_var_log(self):
        code, _, _ = run_hook("Bash", {"command": "echo data > /var/log/syslog"})
        assert code == 2

    def test_block_rm_var_log(self):
        code, _, _ = run_hook("Bash", {"command": "rm /var/log/auth.log"})
        assert code == 2


class TestReadOnlyShellHistory:
    """Shell history files - allow read, block write/edit/delete."""

    def test_block_write_bash_history(self):
        code, _, _ = run_hook("Bash", {"command": f"echo cmd >> {HOME}/.bash_history"})
        assert code == 2

    def test_block_write_zsh_history(self):
        code, _, _ = run_hook("Bash", {"command": f"echo cmd >> {HOME}/.zsh_history"})
        assert code == 2

    def test_block_rm_node_repl_history(self):
        code, _, _ = run_hook("Bash", {"command": f"rm {HOME}/.node_repl_history"})
        assert code == 2

    def test_block_rm_python_history(self):
        code, _, _ = run_hook("Bash", {"command": f"rm {HOME}/.python_history"})
        assert code == 2

    def test_block_rm_psql_history(self):
        code, _, _ = run_hook("Bash", {"command": f"rm {HOME}/.psql_history"})
        assert code == 2


class TestReadOnlyShellConfig:
    """Shell config files - allow read, block write/edit/delete."""

    def test_block_sed_bashrc(self):
        code, _, _ = run_hook(
            "Bash", {"command": f"sed -i 's/old/new/' {HOME}/.bashrc"}
        )
        assert code == 2

    def test_block_sed_zshrc(self):
        code, _, _ = run_hook("Bash", {"command": f"sed -i 's/old/new/' {HOME}/.zshrc"})
        assert code == 2

    def test_block_write_profile(self):
        code, _, _ = run_hook(
            "Bash", {"command": f"echo export FOO=bar >> {HOME}/.profile"}
        )
        assert code == 2

    def test_block_write_zshenv(self):
        code, _, _ = run_hook(
            "Bash", {"command": f"echo export FOO=bar >> {HOME}/.zshenv"}
        )
        assert code == 2


class TestReadOnlyLockFiles:
    """Lock files - allow read, block write/edit/delete."""

    def test_block_rm_package_lock(self):
        code, _, _ = run_hook("Bash", {"command": "rm package-lock.json"})
        assert code == 2

    def test_block_write_yarn_lock(self):
        code, _, _ = run_hook("Bash", {"command": "echo data > yarn.lock"})
        assert code == 2

    def test_block_sed_pnpm_lock(self):
        code, _, _ = run_hook("Bash", {"command": "sed -i 's/old/new/' pnpm-lock.yaml"})
        assert code == 2

    def test_block_rm_gemfile_lock(self):
        code, _, _ = run_hook("Bash", {"command": "rm Gemfile.lock"})
        assert code == 2

    def test_block_rm_poetry_lock(self):
        code, _, _ = run_hook("Bash", {"command": "rm poetry.lock"})
        assert code == 2

    def test_block_rm_cargo_lock(self):
        code, _, _ = run_hook("Bash", {"command": "rm Cargo.lock"})
        assert code == 2

    def test_block_rm_go_sum(self):
        code, _, _ = run_hook("Bash", {"command": "rm go.sum"})
        assert code == 2

    def test_block_rm_uv_lock(self):
        code, _, _ = run_hook("Bash", {"command": "rm uv.lock"})
        assert code == 2

    def test_block_rm_bun_lockb(self):
        code, _, _ = run_hook("Bash", {"command": "rm bun.lockb"})
        assert code == 2

    def test_block_rm_generic_lock(self):
        code, _, _ = run_hook("Bash", {"command": "rm something.lock"})
        assert code == 2


class TestReadOnlyMinifiedFiles:
    """Minified and compiled files - allow read, block write/edit/delete."""

    def test_block_write_min_js(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > app.min.js"})
        assert code == 2

    def test_block_write_min_css(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > style.min.css"})
        assert code == 2

    def test_block_write_bundle_js(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > main.bundle.js"})
        assert code == 2

    def test_block_write_chunk_js(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > vendor.chunk.js"})
        assert code == 2


class TestReadOnlyBuildArtifacts:
    """Build artifact directories - allow read, block write/edit/delete."""

    def test_block_write_dist(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > dist/index.js"})
        assert code == 2

    def test_block_rm_build(self):
        code, _, _ = run_hook("Bash", {"command": "rm build/output.js"})
        assert code == 2

    def test_block_write_next(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > .next/cache.json"})
        assert code == 2

    def test_block_write_node_modules(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > node_modules/pkg/index.js"})
        assert code == 2

    def test_block_rm_pycache(self):
        code, _, _ = run_hook("Bash", {"command": "rm __pycache__/module.pyc"})
        assert code == 2

    def test_block_write_target(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > target/debug/app"})
        assert code == 2

    def test_block_write_gradle(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > .gradle/caches/file"})
        assert code == 2

    def test_block_write_turbo(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > .turbo/cache/hash"})
        assert code == 2


class TestReadOnlyPythonArtifacts:
    """Python build/test artifact dirs - allow read, block write/edit/delete."""

    def test_block_write_mypy_cache(self):
        code, _, _ = run_hook(
            "Bash", {"command": "echo x > .mypy_cache/3.10/module.meta.json"}
        )
        assert code == 2

    def test_block_rm_pytest_cache(self):
        code, _, _ = run_hook("Bash", {"command": "rm .pytest_cache/v/cache/file"})
        assert code == 2

    def test_block_write_tox(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > .tox/py310/log.txt"})
        assert code == 2

    def test_block_write_eggs(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > .eggs/pkg.egg"})
        assert code == 2

    def test_block_write_pyc(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > module.pyc"})
        assert code == 2

    def test_block_write_pyo(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > module.pyo"})
        assert code == 2


class TestReadOnlyCompiledArtifacts:
    """Compiled native artifacts - allow read, block write/edit/delete."""

    def test_block_write_dot_o(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > main.o"})
        assert code == 2

    def test_block_write_dot_so(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > libfoo.so"})
        assert code == 2

    def test_block_write_dylib(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > libfoo.dylib"})
        assert code == 2

    def test_block_write_class(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > Main.class"})
        assert code == 2

    def test_block_write_jar(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > app.jar"})
        assert code == 2


class TestReadOnlyVendoredDeps:
    """Vendored dependency directories - allow read, block write/edit/delete."""

    def test_block_write_vendor(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > vendor/lib/file.js"})
        assert code == 2

    def test_block_write_third_party(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > third_party/lib/file.go"})
        assert code == 2

    def test_block_write_bower(self):
        code, _, _ = run_hook(
            "Bash", {"command": "echo x > bower_components/pkg/index.js"}
        )
        assert code == 2


class TestReadOnlyGeneratedCode:
    """Generated code files - allow read, block write/edit/delete."""

    def test_block_write_generated(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > types.generated.ts"})
        assert code == 2

    def test_block_write_pb_go(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > service.pb.go"})
        assert code == 2

    def test_block_write_generated_go(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > zz_generated.go"})
        assert code == 2

    def test_block_write_g_dart(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > model.g.dart"})
        assert code == 2


class TestReadOnlySourceMaps:
    """Source map files - allow read, block write/edit/delete."""

    def test_block_write_js_map(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > app.js.map"})
        assert code == 2

    def test_block_write_css_map(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > style.css.map"})
        assert code == 2


class TestReadOnlyIDEDirs:
    """IDE/editor directories - allow read, block write/edit/delete."""

    def test_block_write_idea(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > .idea/workspace.xml"})
        assert code == 2

    def test_block_write_vscode(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > .vscode/settings.json"})
        assert code == 2

    def test_block_write_editorconfig(self):
        code, _, _ = run_hook("Bash", {"command": "echo x > .editorconfig"})
        assert code == 2


# =============================================================================
# NO-DELETE PATHS
# =============================================================================


class TestNoDeleteClaude:
    """Claude configuration - block delete only."""

    def test_block_rm_claude_dir(self):
        code, _, _ = run_hook("Bash", {"command": f"rm {HOME}/.claude/settings.json"})
        assert code == 2

    def test_block_rm_claude_md(self):
        code, _, _ = run_hook("Bash", {"command": "rm CLAUDE.md"})
        assert code == 2


class TestNoDeleteLegal:
    """License and legal files - block delete only."""

    def test_block_rm_license(self):
        code, _, _ = run_hook("Bash", {"command": "rm LICENSE"})
        assert code == 2

    def test_block_rm_license_mit(self):
        code, _, _ = run_hook("Bash", {"command": "rm LICENSE.MIT"})
        assert code == 2

    def test_block_rm_copying(self):
        code, _, _ = run_hook("Bash", {"command": "rm COPYING"})
        assert code == 2

    def test_block_rm_notice(self):
        code, _, _ = run_hook("Bash", {"command": "rm NOTICE"})
        assert code == 2

    def test_block_rm_patents(self):
        code, _, _ = run_hook("Bash", {"command": "rm PATENTS"})
        assert code == 2


class TestNoDeleteDocs:
    """Project documentation files - block delete only."""

    def test_block_rm_readme(self):
        code, _, _ = run_hook("Bash", {"command": "rm README.md"})
        assert code == 2

    def test_block_rm_contributing(self):
        code, _, _ = run_hook("Bash", {"command": "rm CONTRIBUTING.md"})
        assert code == 2

    def test_block_rm_changelog(self):
        code, _, _ = run_hook("Bash", {"command": "rm CHANGELOG.md"})
        assert code == 2

    def test_block_rm_code_of_conduct(self):
        code, _, _ = run_hook("Bash", {"command": "rm CODE_OF_CONDUCT.md"})
        assert code == 2

    def test_block_rm_security_md(self):
        code, _, _ = run_hook("Bash", {"command": "rm SECURITY.md"})
        assert code == 2


class TestNoDeleteGit:
    """Git directory and config files - block delete only."""

    def test_block_rm_gitignore(self):
        code, _, _ = run_hook("Bash", {"command": "rm .gitignore"})
        assert code == 2

    def test_block_rm_gitattributes(self):
        code, _, _ = run_hook("Bash", {"command": "rm .gitattributes"})
        assert code == 2

    def test_block_rm_gitmodules(self):
        code, _, _ = run_hook("Bash", {"command": "rm .gitmodules"})
        assert code == 2

    def test_block_rm_git_dir(self):
        code, _, _ = run_hook("Bash", {"command": "rm .git/config"})
        assert code == 2


class TestNoDeleteCICD:
    """CI/CD configuration - block delete only."""

    def test_block_rm_github_dir(self):
        code, _, _ = run_hook("Bash", {"command": "rm .github/workflows/ci.yml"})
        assert code == 2

    def test_block_rm_gitlab_ci(self):
        code, _, _ = run_hook("Bash", {"command": "rm .gitlab-ci.yml"})
        assert code == 2

    def test_block_rm_circleci(self):
        code, _, _ = run_hook("Bash", {"command": "rm .circleci/config.yml"})
        assert code == 2

    def test_block_rm_jenkinsfile(self):
        code, _, _ = run_hook("Bash", {"command": "rm Jenkinsfile"})
        assert code == 2

    def test_block_rm_travis(self):
        code, _, _ = run_hook("Bash", {"command": "rm .travis.yml"})
        assert code == 2

    def test_block_rm_azure_pipelines(self):
        code, _, _ = run_hook("Bash", {"command": "rm azure-pipelines.yml"})
        assert code == 2

    def test_block_rm_buildkite(self):
        code, _, _ = run_hook("Bash", {"command": "rm .buildkite/pipeline.yml"})
        assert code == 2

    def test_block_rm_drone(self):
        code, _, _ = run_hook("Bash", {"command": "rm .drone.yml"})
        assert code == 2


class TestNoDeleteDocker:
    """Docker configuration - block delete only."""

    def test_block_rm_dockerfile(self):
        code, _, _ = run_hook("Bash", {"command": "rm Dockerfile"})
        assert code == 2

    def test_block_rm_dockerfile_variant(self):
        code, _, _ = run_hook("Bash", {"command": "rm Dockerfile.prod"})
        assert code == 2

    def test_block_rm_docker_compose(self):
        code, _, _ = run_hook("Bash", {"command": "rm docker-compose.yml"})
        assert code == 2

    def test_block_rm_compose(self):
        code, _, _ = run_hook("Bash", {"command": "rm compose.yml"})
        assert code == 2

    def test_block_rm_dockerignore(self):
        code, _, _ = run_hook("Bash", {"command": "rm .dockerignore"})
        assert code == 2


class TestNoDeleteMigrations:
    """Database migration files - block delete only."""

    def test_block_rm_migrations_dir(self):
        code, _, _ = run_hook("Bash", {"command": "rm migrations/001_init.sql"})
        assert code == 2

    def test_block_rm_db_migrate(self):
        code, _, _ = run_hook(
            "Bash", {"command": "rm db/migrate/20230101000000_create_users.rb"}
        )
        assert code == 2

    def test_block_rm_alembic(self):
        code, _, _ = run_hook("Bash", {"command": "rm alembic/versions/001.py"})
        assert code == 2

    def test_block_rm_prisma(self):
        code, _, _ = run_hook("Bash", {"command": "rm prisma/schema.prisma"})
        assert code == 2


class TestNoDeleteBuildTools:
    """Build and task automation files - block delete only."""

    def test_block_rm_makefile(self):
        code, _, _ = run_hook("Bash", {"command": "rm Makefile"})
        assert code == 2

    def test_block_rm_taskfile(self):
        code, _, _ = run_hook("Bash", {"command": "rm Taskfile.yml"})
        assert code == 2

    def test_block_rm_justfile(self):
        code, _, _ = run_hook("Bash", {"command": "rm justfile"})
        assert code == 2

    def test_block_rm_rakefile(self):
        code, _, _ = run_hook("Bash", {"command": "rm Rakefile"})
        assert code == 2

    def test_block_rm_build_gradle(self):
        code, _, _ = run_hook("Bash", {"command": "rm build.gradle"})
        assert code == 2

    def test_block_rm_settings_gradle(self):
        code, _, _ = run_hook("Bash", {"command": "rm settings.gradle"})
        assert code == 2

    def test_block_rm_cmakelists(self):
        code, _, _ = run_hook("Bash", {"command": "rm CMakeLists.txt"})
        assert code == 2

    def test_block_rm_earthfile(self):
        code, _, _ = run_hook("Bash", {"command": "rm Earthfile"})
        assert code == 2


class TestNoDeletePackageManifests:
    """Package manifest files - block delete only."""

    def test_block_rm_package_json(self):
        code, _, _ = run_hook("Bash", {"command": "rm package.json"})
        assert code == 2

    def test_block_rm_cargo_toml(self):
        code, _, _ = run_hook("Bash", {"command": "rm Cargo.toml"})
        assert code == 2

    def test_block_rm_go_mod(self):
        code, _, _ = run_hook("Bash", {"command": "rm go.mod"})
        assert code == 2

    def test_block_rm_pyproject(self):
        code, _, _ = run_hook("Bash", {"command": "rm pyproject.toml"})
        assert code == 2

    def test_block_rm_requirements(self):
        code, _, _ = run_hook("Bash", {"command": "rm requirements.txt"})
        assert code == 2

    def test_block_rm_gemfile(self):
        code, _, _ = run_hook("Bash", {"command": "rm Gemfile"})
        assert code == 2

    def test_block_rm_composer(self):
        code, _, _ = run_hook("Bash", {"command": "rm composer.json"})
        assert code == 2

    def test_block_rm_pom(self):
        code, _, _ = run_hook("Bash", {"command": "rm pom.xml"})
        assert code == 2

    def test_block_rm_mix(self):
        code, _, _ = run_hook("Bash", {"command": "rm mix.exs"})
        assert code == 2

    def test_block_rm_pubspec(self):
        code, _, _ = run_hook("Bash", {"command": "rm pubspec.yaml"})
        assert code == 2

    def test_block_rm_build_sbt(self):
        code, _, _ = run_hook("Bash", {"command": "rm build.sbt"})
        assert code == 2

    def test_block_rm_pipfile(self):
        code, _, _ = run_hook("Bash", {"command": "rm Pipfile"})
        assert code == 2

    def test_block_rm_setup_py(self):
        code, _, _ = run_hook("Bash", {"command": "rm setup.py"})
        assert code == 2

    def test_block_rm_flake_nix(self):
        code, _, _ = run_hook("Bash", {"command": "rm flake.nix"})
        assert code == 2


class TestNoDeleteMonorepo:
    """Monorepo configuration - block delete only."""

    def test_block_rm_lerna(self):
        code, _, _ = run_hook("Bash", {"command": "rm lerna.json"})
        assert code == 2

    def test_block_rm_nx(self):
        code, _, _ = run_hook("Bash", {"command": "rm nx.json"})
        assert code == 2

    def test_block_rm_turbo(self):
        code, _, _ = run_hook("Bash", {"command": "rm turbo.json"})
        assert code == 2

    def test_block_rm_pnpm_workspace(self):
        code, _, _ = run_hook("Bash", {"command": "rm pnpm-workspace.yaml"})
        assert code == 2


class TestNoDeleteVersionManagers:
    """Version manager config files - block delete only."""

    def test_block_rm_tool_versions(self):
        code, _, _ = run_hook("Bash", {"command": "rm .tool-versions"})
        assert code == 2

    def test_block_rm_nvmrc(self):
        code, _, _ = run_hook("Bash", {"command": "rm .nvmrc"})
        assert code == 2

    def test_block_rm_python_version(self):
        code, _, _ = run_hook("Bash", {"command": "rm .python-version"})
        assert code == 2

    def test_block_rm_ruby_version(self):
        code, _, _ = run_hook("Bash", {"command": "rm .ruby-version"})
        assert code == 2

    def test_block_rm_node_version(self):
        code, _, _ = run_hook("Bash", {"command": "rm .node-version"})
        assert code == 2

    def test_block_rm_rust_toolchain(self):
        code, _, _ = run_hook("Bash", {"command": "rm rust-toolchain.toml"})
        assert code == 2


class TestNoDeleteEnvTemplates:
    """Environment template files - block delete only."""

    def test_block_rm_env_example(self):
        code, _, _ = run_hook("Bash", {"command": "rm .env.example"})
        assert code == 2

    def test_block_rm_env_sample(self):
        code, _, _ = run_hook("Bash", {"command": "rm .env.sample"})
        assert code == 2

    def test_block_rm_env_template(self):
        code, _, _ = run_hook("Bash", {"command": "rm .env.template"})
        assert code == 2
