"""Tests for macOS-specific security patterns."""

import json

from tests.conftest import run_hook


class TestMacosBlock:
    def test_block_csrutil(self):
        code, _, _ = run_hook("Bash", {"command": "csrutil disable"})
        assert code == 2

    def test_block_spctl_master_disable(self):
        code, _, _ = run_hook("Bash", {"command": "spctl --master-disable"})
        assert code == 2

    def test_block_dscl_create(self):
        code, _, _ = run_hook("Bash", {"command": "dscl . create /Users/test"})
        assert code == 2

    def test_block_dscl_delete(self):
        code, _, _ = run_hook("Bash", {"command": "dscl . -delete /Users/test"})
        assert code == 2

    def test_block_xattr_quarantine(self):
        code, _, _ = run_hook(
            "Bash", {"command": "xattr -d com.apple.quarantine /Applications/app.app"}
        )
        assert code == 2

    def test_block_launchctl_unload(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "launchctl unload /Library/LaunchDaemons/com.test.plist"},
        )
        assert code == 2

    def test_block_diskutil_apfs_delete_volume(self):
        code, _, _ = run_hook("Bash", {"command": "diskutil apfs deleteVolume disk1s2"})
        assert code == 2

    def test_block_security_delete_keychain(self):
        code, _, _ = run_hook(
            "Bash", {"command": "security delete-keychain login.keychain"}
        )
        assert code == 2

    def test_block_security_delete_generic_password(self):
        code, _, _ = run_hook(
            "Bash", {"command": "security delete-generic-password -s myservice"}
        )
        assert code == 2

    def test_block_security_delete_internet_password(self):
        code, _, _ = run_hook(
            "Bash", {"command": "security delete-internet-password -s example.com"}
        )
        assert code == 2

    def test_block_gpg_delete_key(self):
        code, _, _ = run_hook("Bash", {"command": "gpg --delete-key ABCD1234"})
        assert code == 2

    def test_block_gpg_delete_secret_key(self):
        code, _, _ = run_hook("Bash", {"command": "gpg --delete-secret-key ABCD1234"})
        assert code == 2


class TestMacosAsk:
    def test_ask_defaults_write(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "defaults write com.apple.finder AppleShowAllFiles -bool true"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_networksetup(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "networksetup -setdnsservers Wi-Fi 8.8.8.8"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_scutil_set(self):
        code, stdout, _ = run_hook("Bash", {"command": "scutil --set HostName myhost"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_pmset(self):
        code, stdout, _ = run_hook("Bash", {"command": "pmset -a sleep 0"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_launchctl_load(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "launchctl load /Library/LaunchDaemons/com.test.plist"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_launchctl_bootstrap(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "launchctl bootstrap system /Library/LaunchDaemons/com.test.plist"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_diskutil_unmount(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "diskutil unmount /Volumes/MyDisk"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
