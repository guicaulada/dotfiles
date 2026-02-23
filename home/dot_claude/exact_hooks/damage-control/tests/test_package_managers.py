"""Tests for package manager security patterns."""

import json

from tests.conftest import run_hook

# =============================================================================
# BLOCK TESTS (exit code 2)
# =============================================================================


class TestPackageRegistryBlock:
    """Registry destructive operations that are always blocked."""

    def test_block_npm_unpublish(self):
        code, _, _ = run_hook("Bash", {"command": "npm unpublish my-package"})
        assert code == 2

    def test_block_npm_deprecate(self):
        code, _, _ = run_hook(
            "Bash", {"command": "npm deprecate my-package@1.0.0 'deprecated'"}
        )
        assert code == 2

    def test_block_gem_yank(self):
        code, _, _ = run_hook("Bash", {"command": "gem yank my-gem -v 1.0.0"})
        assert code == 2

    def test_block_cargo_yank(self):
        code, _, _ = run_hook("Bash", {"command": "cargo yank --version 1.0.0"})
        assert code == 2


class TestSystemPackageRemovalBlock:
    """System package manager removal operations that are always blocked."""

    def test_block_sudo_apt_remove(self):
        code, _, _ = run_hook("Bash", {"command": "sudo apt remove nginx"})
        assert code == 2

    def test_block_sudo_apt_get_purge(self):
        code, _, _ = run_hook("Bash", {"command": "sudo apt-get purge mysql"})
        assert code == 2

    def test_block_sudo_apt_autoremove(self):
        code, _, _ = run_hook("Bash", {"command": "sudo apt autoremove"})
        assert code == 2

    def test_block_sudo_dnf_remove(self):
        code, _, _ = run_hook("Bash", {"command": "sudo dnf remove httpd"})
        assert code == 2

    def test_block_sudo_yum_erase(self):
        code, _, _ = run_hook("Bash", {"command": "sudo yum erase php"})
        assert code == 2

    def test_block_sudo_yum_autoremove(self):
        code, _, _ = run_hook("Bash", {"command": "sudo yum autoremove"})
        assert code == 2

    def test_block_sudo_pacman_remove(self):
        code, _, _ = run_hook("Bash", {"command": "sudo pacman -Rs nginx"})
        assert code == 2

    def test_block_sudo_zypper_remove(self):
        code, _, _ = run_hook("Bash", {"command": "sudo zypper remove vim"})
        assert code == 2

    def test_block_sudo_zypper_rm(self):
        code, _, _ = run_hook("Bash", {"command": "sudo zypper rm vim"})
        assert code == 2

    def test_block_sudo_apk_del(self):
        code, _, _ = run_hook("Bash", {"command": "sudo apk del nginx"})
        assert code == 2


class TestSnapFlatpakBlock:
    """Snap and Flatpak removal operations that are always blocked."""

    def test_block_snap_remove(self):
        code, _, _ = run_hook("Bash", {"command": "snap remove firefox"})
        assert code == 2

    def test_block_snap_uninstall(self):
        code, _, _ = run_hook("Bash", {"command": "snap uninstall vlc"})
        assert code == 2

    def test_block_flatpak_uninstall(self):
        code, _, _ = run_hook("Bash", {"command": "flatpak uninstall org.gimp.GIMP"})
        assert code == 2


class TestNixDestructiveBlock:
    """Nix garbage collection and store deletion operations that are always blocked."""

    def test_block_nix_collect_garbage(self):
        code, _, _ = run_hook("Bash", {"command": "nix-collect-garbage -d"})
        assert code == 2

    def test_block_nix_store_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "nix-store --delete /nix/store/abc-hello"}
        )
        assert code == 2

    def test_block_nix_store_gc(self):
        code, _, _ = run_hook("Bash", {"command": "nix store gc"})
        assert code == 2

    def test_block_nix_store_delete_flake(self):
        code, _, _ = run_hook(
            "Bash", {"command": "nix store delete /nix/store/abc-hello"}
        )
        assert code == 2


class TestVersionManagerBlock:
    """Version manager uninstall operations that are always blocked."""

    def test_block_asdf_uninstall(self):
        code, _, _ = run_hook("Bash", {"command": "asdf uninstall nodejs 18.0.0"})
        assert code == 2

    def test_block_mise_uninstall(self):
        code, _, _ = run_hook("Bash", {"command": "mise uninstall node@18"})
        assert code == 2

    def test_block_mise_prune(self):
        code, _, _ = run_hook("Bash", {"command": "mise prune"})
        assert code == 2

    def test_block_proto_uninstall(self):
        code, _, _ = run_hook("Bash", {"command": "proto uninstall node 18"})
        assert code == 2

    def test_block_proto_clean(self):
        code, _, _ = run_hook("Bash", {"command": "proto clean"})
        assert code == 2


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
