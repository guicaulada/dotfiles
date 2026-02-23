"""Tests for package manager security patterns."""

import json

from tests.conftest import run_hook


class TestPackageManagerBlock:
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

    def test_block_sudo_pacman_remove(self):
        code, _, _ = run_hook("Bash", {"command": "sudo pacman -Rs nginx"})
        assert code == 2

    def test_block_sudo_zypper_remove(self):
        code, _, _ = run_hook("Bash", {"command": "sudo zypper remove vim"})
        assert code == 2

    def test_block_sudo_apk_del(self):
        code, _, _ = run_hook("Bash", {"command": "sudo apk del nginx"})
        assert code == 2


class TestPackageManagerAsk:
    def test_ask_npm_publish(self):
        code, stdout, _ = run_hook("Bash", {"command": "npm publish"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_brew_uninstall(self):
        code, stdout, _ = run_hook("Bash", {"command": "brew uninstall node"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_brew_remove(self):
        code, stdout, _ = run_hook("Bash", {"command": "brew remove python"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_pip_uninstall(self):
        code, stdout, _ = run_hook("Bash", {"command": "pip uninstall requests"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gem_uninstall(self):
        code, stdout, _ = run_hook("Bash", {"command": "gem uninstall rails"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_sudo_apt_install(self):
        code, stdout, _ = run_hook("Bash", {"command": "sudo apt install nginx"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_sudo_dnf_install(self):
        code, stdout, _ = run_hook("Bash", {"command": "sudo dnf install httpd"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_sudo_pacman_install(self):
        code, stdout, _ = run_hook("Bash", {"command": "sudo pacman -S vim"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_sudo_zypper_install(self):
        code, stdout, _ = run_hook("Bash", {"command": "sudo zypper install vim"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_sudo_apk_add(self):
        code, stdout, _ = run_hook("Bash", {"command": "sudo apk add nginx"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_brew_install_force(self):
        code, stdout, _ = run_hook("Bash", {"command": "brew install node --force"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_brew_reinstall(self):
        code, stdout, _ = run_hook("Bash", {"command": "brew reinstall python"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_brew_install_cask(self):
        code, stdout, _ = run_hook("Bash", {"command": "brew install --cask firefox"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_pip_install(self):
        code, stdout, _ = run_hook("Bash", {"command": "pip install requests"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_pip3_install(self):
        code, stdout, _ = run_hook("Bash", {"command": "pip3 install flask"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_cargo_install(self):
        code, stdout, _ = run_hook("Bash", {"command": "cargo install ripgrep"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_go_install(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "go install golang.org/x/tools/gopls@latest"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_nix_profile_install(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "nix profile install nixpkgs#hello"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_npx(self):
        code, stdout, _ = run_hook("Bash", {"command": "npx create-react-app myapp"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_bunx(self):
        code, stdout, _ = run_hook("Bash", {"command": "bunx create-svelte"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_yarn_dlx(self):
        code, stdout, _ = run_hook("Bash", {"command": "yarn dlx create-react-app"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_pnpm_dlx(self):
        code, stdout, _ = run_hook("Bash", {"command": "pnpm dlx create-next-app"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_npm_install_global(self):
        code, stdout, _ = run_hook("Bash", {"command": "npm install -g typescript"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_npm_i_global(self):
        code, stdout, _ = run_hook("Bash", {"command": "npm i -g eslint"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_yarn_global_add(self):
        code, stdout, _ = run_hook("Bash", {"command": "yarn global add typescript"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_pnpm_add_global(self):
        code, stdout, _ = run_hook("Bash", {"command": "pnpm add -g typescript"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_npm_link(self):
        code, stdout, _ = run_hook("Bash", {"command": "npm link my-package"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_yarn_link(self):
        code, stdout, _ = run_hook("Bash", {"command": "yarn link my-package"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
