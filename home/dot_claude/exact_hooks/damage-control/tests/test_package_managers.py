"""Tests for package manager security patterns."""

import json

from tests.conftest import assert_asks, run_hook

# =============================================================================
# BLOCK TESTS (exit code 2)
# =============================================================================


class TestCredentialTokenExposureBlock:
    """Credential/token exposure operations that are always blocked."""

    def test_block_npm_token_list(self):
        assert_asks('Bash', {'command': 'npm token list'})

    def test_block_npm_token_create(self):
        assert_asks('Bash', {'command': 'npm token create --read-only'})

    def test_block_composer_config_http_basic(self):
        assert_asks('Bash', {'command': 'composer config --global http-basic.repo.example.com'})

    def test_block_composer_config_github_oauth(self):
        assert_asks('Bash', {'command': 'composer config --global github-oauth.github.com'})

    def test_block_gem_credentials(self):
        assert_asks('Bash', {'command': 'gem credentials'})


class TestPackageRegistryBlock:
    """Registry destructive operations that are always blocked."""

    def test_block_npm_unpublish(self):
        assert_asks('Bash', {'command': 'npm unpublish my-package'})

    def test_block_npm_deprecate(self):
        assert_asks('Bash', {'command': "npm deprecate my-package@1.0.0 'deprecated'"})

    def test_block_gem_yank(self):
        assert_asks('Bash', {'command': 'gem yank my-gem -v 1.0.0'})

    def test_block_cargo_yank(self):
        assert_asks('Bash', {'command': 'cargo yank --version 1.0.0'})


class TestSystemPackageRemovalBlock:
    """System package manager removal operations that are always blocked."""

    def test_block_sudo_apt_remove(self):
        assert_asks('Bash', {'command': 'sudo apt remove nginx'})

    def test_block_sudo_apt_get_purge(self):
        assert_asks('Bash', {'command': 'sudo apt-get purge mysql'})

    def test_block_sudo_apt_autoremove(self):
        assert_asks('Bash', {'command': 'sudo apt autoremove'})

    def test_block_sudo_dnf_remove(self):
        assert_asks('Bash', {'command': 'sudo dnf remove httpd'})

    def test_block_sudo_yum_erase(self):
        assert_asks('Bash', {'command': 'sudo yum erase php'})

    def test_block_sudo_yum_autoremove(self):
        assert_asks('Bash', {'command': 'sudo yum autoremove'})

    def test_block_sudo_pacman_remove(self):
        assert_asks('Bash', {'command': 'sudo pacman -Rs nginx'})

    def test_block_sudo_zypper_remove(self):
        assert_asks('Bash', {'command': 'sudo zypper remove vim'})

    def test_block_sudo_zypper_rm(self):
        assert_asks('Bash', {'command': 'sudo zypper rm vim'})

    def test_block_sudo_apk_del(self):
        assert_asks('Bash', {'command': 'sudo apk del nginx'})


class TestSnapFlatpakBlock:
    """Snap and Flatpak removal operations that are always blocked."""

    def test_block_snap_remove(self):
        assert_asks('Bash', {'command': 'snap remove firefox'})

    def test_block_snap_uninstall(self):
        assert_asks('Bash', {'command': 'snap uninstall vlc'})

    def test_block_flatpak_uninstall(self):
        assert_asks('Bash', {'command': 'flatpak uninstall org.gimp.GIMP'})


class TestNixDestructiveBlock:
    """Nix garbage collection and store deletion operations that are always blocked."""

    def test_block_nix_collect_garbage(self):
        assert_asks('Bash', {'command': 'nix-collect-garbage -d'})

    def test_block_nix_store_delete(self):
        assert_asks('Bash', {'command': 'nix-store --delete /nix/store/abc-hello'})

    def test_block_nix_store_gc(self):
        assert_asks('Bash', {'command': 'nix store gc'})

    def test_block_nix_store_delete_flake(self):
        assert_asks('Bash', {'command': 'nix store delete /nix/store/abc-hello'})


class TestVersionManagerBlock:
    """Version manager uninstall operations that are always blocked."""

    def test_block_asdf_uninstall(self):
        assert_asks('Bash', {'command': 'asdf uninstall nodejs 18.0.0'})

    def test_block_mise_uninstall(self):
        assert_asks('Bash', {'command': 'mise uninstall node@18'})

    def test_block_mise_prune(self):
        assert_asks('Bash', {'command': 'mise prune'})

    def test_block_proto_uninstall(self):
        assert_asks('Bash', {'command': 'proto uninstall node 18'})

    def test_block_proto_clean(self):
        assert_asks('Bash', {'command': 'proto clean'})


# =============================================================================
# ASK TESTS (exit code 0, permissionDecision == "ask")
# =============================================================================


def _assert_ask(command: str) -> None:
    """Helper: run command and assert it triggers an ask decision."""
    code, stdout, _ = run_hook("Bash", {"command": command})
    assert code == 0, f"Expected exit 0 (ask) for: {command}"
    data = json.loads(stdout)
    assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestSystemPackageInstallAsk:
    """System package manager install operations that require confirmation."""

    def test_ask_sudo_apt_install(self):
        _assert_ask("sudo apt install nginx")

    def test_ask_sudo_apt_get_install(self):
        _assert_ask("sudo apt-get install nginx")

    def test_ask_sudo_dnf_install(self):
        _assert_ask("sudo dnf install httpd")

    def test_ask_sudo_yum_install(self):
        _assert_ask("sudo yum install httpd")

    def test_ask_sudo_pacman_install(self):
        _assert_ask("sudo pacman -S vim")

    def test_ask_sudo_zypper_install(self):
        _assert_ask("sudo zypper install vim")

    def test_ask_sudo_zypper_in(self):
        _assert_ask("sudo zypper in vim")

    def test_ask_sudo_apk_add(self):
        _assert_ask("sudo apk add nginx")


class TestHomebrewAsk:
    """Homebrew operations that require confirmation."""

    def test_ask_brew_uninstall(self):
        _assert_ask("brew uninstall node")

    def test_ask_brew_remove(self):
        _assert_ask("brew remove python")

    def test_ask_brew_install_force(self):
        _assert_ask("brew install node --force")

    def test_ask_brew_reinstall(self):
        _assert_ask("brew reinstall python")

    def test_ask_brew_install_cask(self):
        _assert_ask("brew install --cask firefox")

    def test_ask_brew_cleanup(self):
        _assert_ask("brew cleanup")

    def test_ask_brew_autoremove(self):
        _assert_ask("brew autoremove")

    def test_ask_brew_install(self):
        _assert_ask("brew install ripgrep")

    def test_ask_brew_upgrade(self):
        _assert_ask("brew upgrade")

    def test_ask_brew_update(self):
        _assert_ask("brew update")

    def test_ask_brew_tap(self):
        _assert_ask("brew tap homebrew/cask-fonts")

    def test_ask_brew_untap(self):
        _assert_ask("brew untap homebrew/cask-fonts")

    def test_ask_brew_link(self):
        _assert_ask("brew link --overwrite python")

    def test_ask_brew_services(self):
        _assert_ask("brew services start postgresql")

    def test_ask_brew_bundle(self):
        _assert_ask("brew bundle --file=Brewfile")

    def test_ask_mas_install(self):
        _assert_ask("mas install 497799835")

    def test_ask_corepack_enable(self):
        _assert_ask("corepack enable")

    def test_ask_mise_install(self):
        _assert_ask("mise install node@24")

    def test_ask_mise_use(self):
        _assert_ask("mise use node@24")


class TestPipGemAsk:
    """Pip and gem operations that require confirmation."""

    def test_ask_pip_install(self):
        _assert_ask("pip install requests")

    def test_ask_pip3_install(self):
        _assert_ask("pip3 install flask")

    def test_ask_pip_uninstall(self):
        _assert_ask("pip uninstall requests")

    def test_ask_gem_uninstall(self):
        _assert_ask("gem uninstall rails")


class TestCargoGoAsk:
    """Cargo and Go install operations that require confirmation."""

    def test_ask_cargo_install(self):
        _assert_ask("cargo install ripgrep")

    def test_ask_go_install(self):
        _assert_ask("go install golang.org/x/tools/gopls@latest")


class TestNixProfileAsk:
    """Nix profile operations that require confirmation."""

    def test_ask_nix_profile_install(self):
        _assert_ask("nix profile install nixpkgs#hello")

    def test_ask_nix_profile_remove(self):
        _assert_ask("nix profile remove nixpkgs#hello")

    def test_ask_nix_env_uninstall(self):
        _assert_ask("nix-env -e hello")

    def test_ask_nix_env_uninstall_with_flags(self):
        _assert_ask("nix-env -p /nix/var/nix/profiles/default -e hello")


class TestRegistryPublishAsk:
    """Registry publish operations that require confirmation."""

    def test_ask_npm_publish(self):
        _assert_ask("npm publish")


class TestRemoteExecutionAsk:
    """Remote package execution tools that require confirmation."""

    def test_ask_npx(self):
        _assert_ask("npx create-react-app myapp")

    def test_ask_bunx(self):
        _assert_ask("bunx create-svelte")

    def test_ask_yarn_dlx(self):
        _assert_ask("yarn dlx create-react-app")

    def test_ask_pnpm_dlx(self):
        _assert_ask("pnpm dlx create-next-app")


class TestGlobalInstallAsk:
    """Global install operations that require confirmation."""

    def test_ask_npm_install_global(self):
        _assert_ask("npm install -g typescript")

    def test_ask_npm_i_global(self):
        _assert_ask("npm i -g eslint")

    def test_ask_yarn_global_add(self):
        _assert_ask("yarn global add typescript")

    def test_ask_pnpm_add_global(self):
        _assert_ask("pnpm add -g typescript")


class TestLinkAsk:
    """Package linking operations that require confirmation."""

    def test_ask_npm_link(self):
        _assert_ask("npm link my-package")

    def test_ask_yarn_link(self):
        _assert_ask("yarn link my-package")
