"""Tests for zero-access, read-only, and no-delete path enforcement in Bash handler."""

from tests.conftest import HOME, assert_asks

# =============================================================================
# ZERO ACCESS PATHS
# =============================================================================


class TestZeroAccessEnvFiles:
    """Environment files (.env variants) - block ALL operations."""

    def test_block_cat_env(self):
        assert_asks("Bash", {"command": "cat .env"})

    def test_block_cat_env_local(self):
        assert_asks("Bash", {"command": "cat .env.local"})

    def test_block_cat_env_production(self):
        assert_asks("Bash", {"command": "cat .env.production"})

    def test_block_cat_env_development_local(self):
        assert_asks("Bash", {"command": "cat .env.development.local"})

    def test_block_cat_app_env(self):
        assert_asks("Bash", {"command": "cat app.env"})


class TestZeroAccessSSHAndGPG:
    """SSH and GPG directories - block ALL operations."""

    def test_block_cat_ssh_id_rsa(self):
        assert_asks("Bash", {"command": f"cat {HOME}/.ssh/id_rsa"})

    def test_block_cat_ssh_config(self):
        assert_asks("Bash", {"command": f"cat {HOME}/.ssh/config"})

    def test_block_cat_gnupg(self):
        assert_asks("Bash", {"command": f"cat {HOME}/.gnupg/trustdb.gpg"})


class TestZeroAccessCloudCredentials:
    """Cloud provider credentials - block ALL operations."""

    def test_block_cat_aws(self):
        assert_asks("Bash", {"command": f"cat {HOME}/.aws/credentials"})

    def test_block_cat_gcloud(self):
        assert_asks(
            "Bash",
            {
                "command": f"cat {HOME}/.config/gcloud/application_default_credentials.json"
            },
        )

    def test_block_cat_credentials_json(self):
        assert_asks("Bash", {"command": "cat credentials.json"})

    def test_block_cat_prefixed_credentials_json(self):
        assert_asks("Bash", {"command": "cat gcp-credentials.json"})

    def test_block_cat_service_account(self):
        assert_asks("Bash", {"command": "cat myServiceAccount.json"})

    def test_block_cat_service_account_hyphen(self):
        assert_asks("Bash", {"command": "cat my-service-account-key.json"})

    def test_block_cat_azure(self):
        assert_asks("Bash", {"command": f"cat {HOME}/.azure/profile"})

    def test_block_cat_kube(self):
        assert_asks("Bash", {"command": f"cat {HOME}/.kube/config"})

    def test_block_cat_kubeconfig(self):
        assert_asks("Bash", {"command": "cat kubeconfig"})

    def test_block_cat_k8s_secret_yaml(self):
        assert_asks("Bash", {"command": "cat db-secret.yaml"})

    def test_block_cat_secrets_yaml(self):
        assert_asks("Bash", {"command": "cat secrets.yaml"})

    def test_block_cat_secrets_dir(self):
        assert_asks("Bash", {"command": "cat secrets/db-password.txt"})

    def test_block_cat_nested_secrets_dir(self):
        """'**/secrets/' glob should block nested secrets directories."""
        assert_asks("Bash", {"command": "cat deploy/secrets/db-password.txt"})

    def test_block_cat_docker_config(self):
        assert_asks("Bash", {"command": f"cat {HOME}/.docker/config.json"})


class TestZeroAccessCertificates:
    """SSL/TLS certificates and private keys - block ALL operations."""

    def test_block_cat_pem(self):
        assert_asks("Bash", {"command": "cat server.pem"})

    def test_block_cat_key(self):
        assert_asks("Bash", {"command": "cat private.key"})

    def test_block_cat_p12(self):
        assert_asks("Bash", {"command": "cat certificate.p12"})

    def test_block_cat_pfx(self):
        assert_asks("Bash", {"command": "cat certificate.pfx"})

    def test_block_cat_csr(self):
        assert_asks("Bash", {"command": "cat server.csr"})

    def test_block_cat_cert(self):
        assert_asks("Bash", {"command": "cat server.cert"})

    def test_block_cat_cer(self):
        assert_asks("Bash", {"command": "cat server.cer"})

    def test_block_cat_der(self):
        assert_asks("Bash", {"command": "cat server.der"})


class TestZeroAccessTerraform:
    """Terraform state and variables - block ALL operations."""

    def test_block_cat_tfstate(self):
        assert_asks("Bash", {"command": "cat terraform.tfstate"})

    def test_block_cat_tfstate_backup(self):
        assert_asks("Bash", {"command": "cat terraform.tfstate.backup"})

    def test_block_cat_tfvars(self):
        assert_asks("Bash", {"command": "cat prod.tfvars"})


class TestZeroAccessTokens:
    """Token files - block ALL operations."""

    def test_block_cat_dot_token(self):
        assert_asks("Bash", {"command": "cat .token"})

    def test_block_cat_glob_token(self):
        assert_asks("Bash", {"command": "cat github.token"})

    def test_block_cat_token_json(self):
        assert_asks("Bash", {"command": "cat token.json"})

    def test_block_cat_tokens_json(self):
        assert_asks("Bash", {"command": "cat tokens.json"})


class TestZeroAccessOAuth:
    """OAuth and client secret files - block ALL operations."""

    def test_block_cat_oauth_json(self):
        assert_asks("Bash", {"command": "cat oauth-config.json"})

    def test_block_cat_client_secret_json(self):
        assert_asks("Bash", {"command": "cat client_secret_12345.json"})

    def test_block_cat_client_secret_hyphen(self):
        assert_asks("Bash", {"command": "cat client-secret-google.json"})


class TestZeroAccessAnsibleVault:
    """Ansible vault files - block ALL operations."""

    def test_block_cat_vault_yml(self):
        assert_asks("Bash", {"command": "cat vault.yml"})

    def test_block_cat_vault_yaml(self):
        assert_asks("Bash", {"command": "cat vault.yaml"})

    def test_block_cat_prefixed_vault_yml(self):
        assert_asks("Bash", {"command": "cat prod-vault.yml"})

    def test_block_cat_underscore_vault_yaml(self):
        assert_asks("Bash", {"command": "cat staging_vault.yaml"})


class TestZeroAccessAgeSops:
    """Age and SOPS encryption files - block ALL operations."""

    def test_block_cat_age_file(self):
        assert_asks("Bash", {"command": "cat keys.age"})

    def test_block_cat_sops_yaml(self):
        assert_asks("Bash", {"command": "cat .sops.yaml"})

    def test_block_cat_sops_yml(self):
        assert_asks("Bash", {"command": "cat .sops.yml"})


class TestZeroAccessApiKeys:
    """API key files - block ALL operations."""

    def test_block_cat_api_key_hyphen(self):
        assert_asks("Bash", {"command": "cat stripe-api-key.txt"})

    def test_block_cat_api_key_underscore(self):
        assert_asks("Bash", {"command": "cat openai_api_key.env"})

    def test_block_cat_dot_api_key(self):
        assert_asks("Bash", {"command": "cat .api_key"})

    def test_block_cat_dot_apikey(self):
        assert_asks("Bash", {"command": "cat .apikey"})

    def test_block_cat_api_keys_json(self):
        assert_asks("Bash", {"command": "cat api-keys.json"})

    def test_block_cat_api_keys_yaml(self):
        assert_asks("Bash", {"command": "cat api_keys.yaml"})


class TestZeroAccessAuthConfig:
    """Auth config files - block ALL operations."""

    def test_block_cat_authinfo(self):
        assert_asks("Bash", {"command": "cat .authinfo"})

    def test_block_cat_authinfo_gpg(self):
        assert_asks("Bash", {"command": "cat .authinfo.gpg"})


class TestZeroAccessHelmSecrets:
    """Helm secret files - block ALL operations."""

    def test_block_cat_secrets_yml(self):
        assert_asks("Bash", {"command": "cat secrets.yml"})


class TestZeroAccessCredentialStores:
    """Credential managers and secret stores - block ALL operations."""

    def test_block_cat_password_store(self):
        assert_asks(
            "Bash", {"command": f"cat {HOME}/.password-store/email/gmail.gpg"}
        )

    def test_block_cat_vault_token(self):
        assert_asks("Bash", {"command": f"cat {HOME}/.vault-token"})

    def test_block_cat_keyrings(self):
        assert_asks(
            "Bash", {"command": f"cat {HOME}/.local/share/keyrings/default.keyring"}
        )

    def test_block_cat_gnome_keyrings(self):
        assert_asks(
            "Bash", {"command": f"cat {HOME}/.gnome2/keyrings/default.keyring"}
        )

    def test_block_cat_kwalletd(self):
        assert_asks(
            "Bash", {"command": f"cat {HOME}/.local/share/kwalletd/kdewallet.kwl"}
        )

    def test_block_cat_macos_keychains(self):
        assert_asks(
            "Bash", {"command": f"cat {HOME}/Library/Keychains/login.keychain-db"}
        )

    def test_block_cat_1password_config(self):
        assert_asks("Bash", {"command": f"cat {HOME}/.config/op/config"})


class TestZeroAccessPlatformCredentials:
    """Additional cloud and platform credentials - block ALL operations."""

    def test_block_cat_wrangler(self):
        assert_asks(
            "Bash", {"command": f"cat {HOME}/.config/wrangler/config/default.toml"}
        )

    def test_block_cat_project_wrangler(self):
        assert_asks("Bash", {"command": "cat .wrangler/state.json"})

    def test_block_cat_fly(self):
        assert_asks("Bash", {"command": f"cat {HOME}/.fly/config.yml"})

    def test_block_cat_heroku(self):
        assert_asks("Bash", {"command": f"cat {HOME}/.heroku/credentials"})

    def test_block_cat_doctl(self):
        assert_asks(
            "Bash", {"command": f"cat {HOME}/.config/doctl/config.yaml"}
        )

    def test_block_cat_bitwarden_cli(self):
        assert_asks(
            "Bash", {"command": f"cat '{HOME}/.config/Bitwarden CLI/data.json'"}
        )

    def test_block_cat_pulumi_credentials(self):
        assert_asks(
            "Bash", {"command": f"cat {HOME}/.pulumi/credentials.json"}
        )


class TestZeroAccessBrowserProfiles:
    """Browser profiles - block ALL operations."""

    def test_block_cat_mozilla(self):
        assert_asks(
            "Bash", {"command": f"cat {HOME}/.mozilla/firefox/profile/logins.json"}
        )

    def test_block_cat_chrome_mac(self):
        assert_asks(
            "Bash",
            {
                "command": f"cat '{HOME}/Library/Application Support/Google/Chrome/Default/Login Data'"
            },
        )

    def test_block_cat_firefox_mac(self):
        assert_asks(
            "Bash",
            {
                "command": f"cat '{HOME}/Library/Application Support/Firefox/profiles.ini'"
            },
        )

    def test_block_cat_chromium_linux(self):
        assert_asks(
            "Bash", {"command": f"cat {HOME}/.config/chromium/Default/Cookies"}
        )

    def test_block_cat_brave_linux(self):
        assert_asks(
            "Bash",
            {
                "command": f"cat {HOME}/.config/BraveSoftware/Brave-Browser/Default/Cookies"
            },
        )


class TestZeroAccessPackageAuth:
    """Package manager auth files - block ALL operations."""

    def test_block_cat_netrc(self):
        assert_asks("Bash", {"command": f"cat {HOME}/.netrc"})

    def test_block_cat_npmrc_global(self):
        assert_asks("Bash", {"command": f"cat {HOME}/.npmrc"})

    def test_block_cat_npmrc_project(self):
        assert_asks("Bash", {"command": "cat .npmrc"})

    def test_block_cat_pypirc(self):
        assert_asks("Bash", {"command": f"cat {HOME}/.pypirc"})

    def test_block_cat_git_credentials(self):
        assert_asks("Bash", {"command": f"cat {HOME}/.git-credentials"})

    def test_block_cat_gh_hosts(self):
        assert_asks("Bash", {"command": f"cat {HOME}/.config/gh/hosts.yml"})

    def test_block_cat_cargo_credentials(self):
        assert_asks(
            "Bash", {"command": f"cat {HOME}/.cargo/credentials.toml"}
        )


class TestZeroAccessMisc:
    """Miscellaneous zero-access paths."""

    def test_block_cat_htpasswd(self):
        assert_asks("Bash", {"command": "cat .htpasswd"})

    def test_block_cat_keystore(self):
        assert_asks("Bash", {"command": "cat release.keystore"})

    def test_block_cat_jks(self):
        assert_asks("Bash", {"command": "cat server.jks"})

    def test_block_cat_dump_sql(self):
        assert_asks("Bash", {"command": "cat dump.sql"})

    def test_block_cat_backup_sql(self):
        assert_asks("Bash", {"command": "cat backup.sql"})

    def test_block_cat_dump_file(self):
        assert_asks("Bash", {"command": "cat database.dump"})

    def test_block_cat_dot_secret(self):
        assert_asks("Bash", {"command": "cat .secret"})

    def test_block_cat_dot_secrets(self):
        assert_asks("Bash", {"command": "cat .secrets"})

    def test_block_cat_glob_secret(self):
        assert_asks("Bash", {"command": "cat app.secret"})

    def test_block_cat_firebase_admin(self):
        assert_asks("Bash", {"command": "cat firebase-adminsdk-abcde.json"})

    def test_block_cat_service_account_key(self):
        assert_asks("Bash", {"command": "cat serviceAccountKey.json"})

    def test_block_cat_vercel_dir(self):
        assert_asks("Bash", {"command": "cat .vercel/project.json"})

    def test_block_cat_netlify_dir(self):
        assert_asks("Bash", {"command": "cat .netlify/state.json"})

    def test_block_cat_supabase_dir(self):
        assert_asks("Bash", {"command": "cat .supabase/config.toml"})

    def test_block_cat_terraform_dir(self):
        assert_asks("Bash", {"command": "cat .terraform/terraform.tfstate"})


# =============================================================================
# READ-ONLY PATHS
# =============================================================================


class TestReadOnlySystemDirs:
    """System directories - allow read, block write/edit/delete."""

    def test_block_write_etc(self):
        assert_asks("Bash", {"command": "echo data > /etc/hosts"})

    def test_block_write_usr(self):
        assert_asks("Bash", {"command": "echo data > /usr/local/bin/test"})

    def test_block_rm_bin(self):
        assert_asks("Bash", {"command": "rm /bin/ls"})

    def test_block_rm_sbin(self):
        assert_asks("Bash", {"command": "rm /sbin/init"})

    def test_block_write_var_log(self):
        assert_asks("Bash", {"command": "echo data > /var/log/syslog"})

    def test_block_rm_var_log(self):
        assert_asks("Bash", {"command": "rm /var/log/auth.log"})


class TestReadOnlyShellHistory:
    """Shell history files - allow read, block write/edit/delete."""

    def test_block_write_bash_history(self):
        assert_asks("Bash", {"command": f"echo cmd >> {HOME}/.bash_history"})

    def test_block_write_zsh_history(self):
        assert_asks("Bash", {"command": f"echo cmd >> {HOME}/.zsh_history"})

    def test_block_rm_node_repl_history(self):
        assert_asks("Bash", {"command": f"rm {HOME}/.node_repl_history"})

    def test_block_rm_python_history(self):
        assert_asks("Bash", {"command": f"rm {HOME}/.python_history"})

    def test_block_rm_psql_history(self):
        assert_asks("Bash", {"command": f"rm {HOME}/.psql_history"})


class TestReadOnlyShellConfig:
    """Shell config files - allow read, block write/edit/delete."""

    def test_block_sed_bashrc(self):
        assert_asks(
            "Bash", {"command": f"sed -i 's/old/new/' {HOME}/.bashrc"}
        )

    def test_block_sed_zshrc(self):
        assert_asks("Bash", {"command": f"sed -i 's/old/new/' {HOME}/.zshrc"})

    def test_block_write_profile(self):
        assert_asks(
            "Bash", {"command": f"echo export FOO=bar >> {HOME}/.profile"}
        )

    def test_block_write_zshenv(self):
        assert_asks(
            "Bash", {"command": f"echo export FOO=bar >> {HOME}/.zshenv"}
        )


class TestReadOnlyLockFiles:
    """Lock files - allow read, block write/edit/delete."""

    def test_block_rm_package_lock(self):
        assert_asks("Bash", {"command": "rm package-lock.json"})

    def test_block_write_yarn_lock(self):
        assert_asks("Bash", {"command": "echo data > yarn.lock"})

    def test_block_sed_pnpm_lock(self):
        assert_asks("Bash", {"command": "sed -i 's/old/new/' pnpm-lock.yaml"})

    def test_block_rm_gemfile_lock(self):
        assert_asks("Bash", {"command": "rm Gemfile.lock"})

    def test_block_rm_poetry_lock(self):
        assert_asks("Bash", {"command": "rm poetry.lock"})

    def test_block_rm_cargo_lock(self):
        assert_asks("Bash", {"command": "rm Cargo.lock"})

    def test_block_rm_go_sum(self):
        assert_asks("Bash", {"command": "rm go.sum"})

    def test_block_rm_uv_lock(self):
        assert_asks("Bash", {"command": "rm uv.lock"})

    def test_block_rm_bun_lockb(self):
        assert_asks("Bash", {"command": "rm bun.lockb"})

    def test_block_rm_generic_lock(self):
        assert_asks("Bash", {"command": "rm something.lock"})


class TestReadOnlyMinifiedFiles:
    """Minified and compiled files - allow read, block write/edit/delete."""

    def test_block_write_min_js(self):
        assert_asks("Bash", {"command": "echo x > app.min.js"})

    def test_block_write_min_css(self):
        assert_asks("Bash", {"command": "echo x > style.min.css"})

    def test_block_write_bundle_js(self):
        assert_asks("Bash", {"command": "echo x > main.bundle.js"})

    def test_block_write_chunk_js(self):
        assert_asks("Bash", {"command": "echo x > vendor.chunk.js"})


class TestReadOnlyBuildArtifacts:
    """Build artifact directories - allow read, block write/edit/delete."""

    def test_block_write_dist(self):
        assert_asks("Bash", {"command": "echo x > dist/index.js"})

    def test_block_rm_build(self):
        assert_asks("Bash", {"command": "rm build/output.js"})

    def test_block_write_next(self):
        assert_asks("Bash", {"command": "echo x > .next/cache.json"})

    def test_block_write_node_modules(self):
        assert_asks("Bash", {"command": "echo x > node_modules/pkg/index.js"})

    def test_block_rm_pycache(self):
        assert_asks("Bash", {"command": "rm __pycache__/module.pyc"})

    def test_block_write_target(self):
        assert_asks("Bash", {"command": "echo x > target/debug/app"})

    def test_block_write_gradle(self):
        assert_asks("Bash", {"command": "echo x > .gradle/caches/file"})

    def test_block_write_turbo(self):
        assert_asks("Bash", {"command": "echo x > .turbo/cache/hash"})


class TestReadOnlyPythonArtifacts:
    """Python build/test artifact dirs - allow read, block write/edit/delete."""

    def test_block_write_mypy_cache(self):
        assert_asks(
            "Bash", {"command": "echo x > .mypy_cache/3.10/module.meta.json"}
        )

    def test_block_rm_pytest_cache(self):
        assert_asks("Bash", {"command": "rm .pytest_cache/v/cache/file"})

    def test_block_write_tox(self):
        assert_asks("Bash", {"command": "echo x > .tox/py310/log.txt"})

    def test_block_write_eggs(self):
        assert_asks("Bash", {"command": "echo x > .eggs/pkg.egg"})

    def test_block_write_pyc(self):
        assert_asks("Bash", {"command": "echo x > module.pyc"})

    def test_block_write_pyo(self):
        assert_asks("Bash", {"command": "echo x > module.pyo"})


class TestReadOnlyCompiledArtifacts:
    """Compiled native artifacts - allow read, block write/edit/delete."""

    def test_block_write_dot_o(self):
        assert_asks("Bash", {"command": "echo x > main.o"})

    def test_block_write_dot_so(self):
        assert_asks("Bash", {"command": "echo x > libfoo.so"})

    def test_block_write_dylib(self):
        assert_asks("Bash", {"command": "echo x > libfoo.dylib"})

    def test_block_write_class(self):
        assert_asks("Bash", {"command": "echo x > Main.class"})

    def test_block_write_jar(self):
        assert_asks("Bash", {"command": "echo x > app.jar"})


class TestReadOnlyVendoredDeps:
    """Vendored dependency directories - allow read, block write/edit/delete."""

    def test_block_write_vendor(self):
        assert_asks("Bash", {"command": "echo x > vendor/lib/file.js"})

    def test_block_write_third_party(self):
        assert_asks("Bash", {"command": "echo x > third_party/lib/file.go"})

    def test_block_write_bower(self):
        assert_asks(
            "Bash", {"command": "echo x > bower_components/pkg/index.js"}
        )


class TestReadOnlyGeneratedCode:
    """Generated code files - allow read, block write/edit/delete."""

    def test_block_write_generated(self):
        assert_asks("Bash", {"command": "echo x > types.generated.ts"})

    def test_block_write_pb_go(self):
        assert_asks("Bash", {"command": "echo x > service.pb.go"})

    def test_block_write_generated_go(self):
        assert_asks("Bash", {"command": "echo x > zz_generated.go"})

    def test_block_write_g_dart(self):
        assert_asks("Bash", {"command": "echo x > model.g.dart"})


class TestReadOnlySourceMaps:
    """Source map files - allow read, block write/edit/delete."""

    def test_block_write_js_map(self):
        assert_asks("Bash", {"command": "echo x > app.js.map"})

    def test_block_write_css_map(self):
        assert_asks("Bash", {"command": "echo x > style.css.map"})


class TestReadOnlyIDEDirs:
    """IDE/editor directories - allow read, block write/edit/delete."""

    def test_block_write_idea(self):
        assert_asks("Bash", {"command": "echo x > .idea/workspace.xml"})

    def test_block_write_vscode(self):
        assert_asks("Bash", {"command": "echo x > .vscode/settings.json"})

    def test_block_write_editorconfig(self):
        assert_asks("Bash", {"command": "echo x > .editorconfig"})


# =============================================================================
# NO-DELETE PATHS
# =============================================================================


class TestNoDeleteClaude:
    """Claude configuration - block delete only."""

    def test_block_rm_claude_dir(self):
        assert_asks("Bash", {"command": f"rm {HOME}/.claude/settings.json"})

    def test_block_rm_claude_md(self):
        assert_asks("Bash", {"command": "rm CLAUDE.md"})


class TestNoDeleteLegal:
    """License and legal files - block delete only."""

    def test_block_rm_license(self):
        assert_asks("Bash", {"command": "rm LICENSE"})

    def test_block_rm_license_mit(self):
        assert_asks("Bash", {"command": "rm LICENSE.MIT"})

    def test_block_rm_copying(self):
        assert_asks("Bash", {"command": "rm COPYING"})

    def test_block_rm_notice(self):
        assert_asks("Bash", {"command": "rm NOTICE"})

    def test_block_rm_patents(self):
        assert_asks("Bash", {"command": "rm PATENTS"})


class TestNoDeleteDocs:
    """Project documentation files - block delete only."""

    def test_block_rm_readme(self):
        assert_asks("Bash", {"command": "rm README.md"})

    def test_block_rm_contributing(self):
        assert_asks("Bash", {"command": "rm CONTRIBUTING.md"})

    def test_block_rm_changelog(self):
        assert_asks("Bash", {"command": "rm CHANGELOG.md"})

    def test_block_rm_code_of_conduct(self):
        assert_asks("Bash", {"command": "rm CODE_OF_CONDUCT.md"})

    def test_block_rm_security_md(self):
        assert_asks("Bash", {"command": "rm SECURITY.md"})


class TestNoDeleteGit:
    """Git directory and config files - block delete only."""

    def test_block_rm_gitignore(self):
        assert_asks("Bash", {"command": "rm .gitignore"})

    def test_block_rm_gitattributes(self):
        assert_asks("Bash", {"command": "rm .gitattributes"})

    def test_block_rm_gitmodules(self):
        assert_asks("Bash", {"command": "rm .gitmodules"})

    def test_block_rm_git_dir(self):
        assert_asks("Bash", {"command": "rm .git/config"})


class TestNoDeleteCICD:
    """CI/CD configuration - block delete only."""

    def test_block_rm_github_dir(self):
        assert_asks("Bash", {"command": "rm .github/workflows/ci.yml"})

    def test_block_rm_gitlab_ci(self):
        assert_asks("Bash", {"command": "rm .gitlab-ci.yml"})

    def test_block_rm_circleci(self):
        assert_asks("Bash", {"command": "rm .circleci/config.yml"})

    def test_block_rm_jenkinsfile(self):
        assert_asks("Bash", {"command": "rm Jenkinsfile"})

    def test_block_rm_travis(self):
        assert_asks("Bash", {"command": "rm .travis.yml"})

    def test_block_rm_azure_pipelines(self):
        assert_asks("Bash", {"command": "rm azure-pipelines.yml"})

    def test_block_rm_buildkite(self):
        assert_asks("Bash", {"command": "rm .buildkite/pipeline.yml"})

    def test_block_rm_drone(self):
        assert_asks("Bash", {"command": "rm .drone.yml"})


class TestNoDeleteDocker:
    """Docker configuration - block delete only."""

    def test_block_rm_dockerfile(self):
        assert_asks("Bash", {"command": "rm Dockerfile"})

    def test_block_rm_dockerfile_variant(self):
        assert_asks("Bash", {"command": "rm Dockerfile.prod"})

    def test_block_rm_docker_compose(self):
        assert_asks("Bash", {"command": "rm docker-compose.yml"})

    def test_block_rm_compose(self):
        assert_asks("Bash", {"command": "rm compose.yml"})

    def test_block_rm_dockerignore(self):
        assert_asks("Bash", {"command": "rm .dockerignore"})


class TestNoDeleteMigrations:
    """Database migration files - block delete only."""

    def test_block_rm_migrations_dir(self):
        assert_asks("Bash", {"command": "rm migrations/001_init.sql"})

    def test_block_rm_db_migrate(self):
        assert_asks(
            "Bash", {"command": "rm db/migrate/20230101000000_create_users.rb"}
        )

    def test_block_rm_alembic(self):
        assert_asks("Bash", {"command": "rm alembic/versions/001.py"})

    def test_block_rm_prisma(self):
        assert_asks("Bash", {"command": "rm prisma/schema.prisma"})


class TestNoDeleteBuildTools:
    """Build and task automation files - block delete only."""

    def test_block_rm_makefile(self):
        assert_asks("Bash", {"command": "rm Makefile"})

    def test_block_rm_taskfile(self):
        assert_asks("Bash", {"command": "rm Taskfile.yml"})

    def test_block_rm_justfile(self):
        assert_asks("Bash", {"command": "rm justfile"})

    def test_block_rm_rakefile(self):
        assert_asks("Bash", {"command": "rm Rakefile"})

    def test_block_rm_build_gradle(self):
        assert_asks("Bash", {"command": "rm build.gradle"})

    def test_block_rm_settings_gradle(self):
        assert_asks("Bash", {"command": "rm settings.gradle"})

    def test_block_rm_cmakelists(self):
        assert_asks("Bash", {"command": "rm CMakeLists.txt"})

    def test_block_rm_earthfile(self):
        assert_asks("Bash", {"command": "rm Earthfile"})


class TestNoDeletePackageManifests:
    """Package manifest files - block delete only."""

    def test_block_rm_package_json(self):
        assert_asks("Bash", {"command": "rm package.json"})

    def test_block_rm_cargo_toml(self):
        assert_asks("Bash", {"command": "rm Cargo.toml"})

    def test_block_rm_go_mod(self):
        assert_asks("Bash", {"command": "rm go.mod"})

    def test_block_rm_pyproject(self):
        assert_asks("Bash", {"command": "rm pyproject.toml"})

    def test_block_rm_requirements(self):
        assert_asks("Bash", {"command": "rm requirements.txt"})

    def test_block_rm_gemfile(self):
        assert_asks("Bash", {"command": "rm Gemfile"})

    def test_block_rm_composer(self):
        assert_asks("Bash", {"command": "rm composer.json"})

    def test_block_rm_pom(self):
        assert_asks("Bash", {"command": "rm pom.xml"})

    def test_block_rm_mix(self):
        assert_asks("Bash", {"command": "rm mix.exs"})

    def test_block_rm_pubspec(self):
        assert_asks("Bash", {"command": "rm pubspec.yaml"})

    def test_block_rm_build_sbt(self):
        assert_asks("Bash", {"command": "rm build.sbt"})

    def test_block_rm_pipfile(self):
        assert_asks("Bash", {"command": "rm Pipfile"})

    def test_block_rm_setup_py(self):
        assert_asks("Bash", {"command": "rm setup.py"})

    def test_block_rm_flake_nix(self):
        assert_asks("Bash", {"command": "rm flake.nix"})


class TestNoDeleteMonorepo:
    """Monorepo configuration - block delete only."""

    def test_block_rm_lerna(self):
        assert_asks("Bash", {"command": "rm lerna.json"})

    def test_block_rm_nx(self):
        assert_asks("Bash", {"command": "rm nx.json"})

    def test_block_rm_turbo(self):
        assert_asks("Bash", {"command": "rm turbo.json"})

    def test_block_rm_pnpm_workspace(self):
        assert_asks("Bash", {"command": "rm pnpm-workspace.yaml"})


class TestNoDeleteVersionManagers:
    """Version manager config files - block delete only."""

    def test_block_rm_tool_versions(self):
        assert_asks("Bash", {"command": "rm .tool-versions"})

    def test_block_rm_nvmrc(self):
        assert_asks("Bash", {"command": "rm .nvmrc"})

    def test_block_rm_python_version(self):
        assert_asks("Bash", {"command": "rm .python-version"})

    def test_block_rm_ruby_version(self):
        assert_asks("Bash", {"command": "rm .ruby-version"})

    def test_block_rm_node_version(self):
        assert_asks("Bash", {"command": "rm .node-version"})

    def test_block_rm_rust_toolchain(self):
        assert_asks("Bash", {"command": "rm rust-toolchain.toml"})


class TestNoDeleteEnvTemplates:
    """Environment template files - block delete only."""

    def test_block_rm_env_example(self):
        assert_asks("Bash", {"command": "rm .env.example"})

    def test_block_rm_env_sample(self):
        assert_asks("Bash", {"command": "rm .env.sample"})

    def test_block_rm_env_template(self):
        assert_asks("Bash", {"command": "rm .env.template"})
