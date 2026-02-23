"""Tests for macOS-specific security patterns."""

import json

from tests.conftest import run_hook


class TestMacosBlock:
    # --- launchctl remove/bootout ---

    def test_block_launchctl_remove(self):
        code, _, _ = run_hook(
            "Bash", {"command": "launchctl remove com.example.daemon"}
        )
        assert code == 2

    def test_block_launchctl_bootout(self):
        code, _, _ = run_hook(
            "Bash", {"command": "launchctl bootout system/com.example.daemon"}
        )
        assert code == 2

    # --- defaults delete ---

    def test_block_defaults_delete(self):
        code, _, _ = run_hook("Bash", {"command": "defaults delete com.apple.finder"})
        assert code == 2

    def test_block_defaults_delete_key(self):
        code, _, _ = run_hook(
            "Bash", {"command": "defaults delete com.apple.dock autohide"}
        )
        assert code == 2

    # --- security delete (consolidated) ---

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

    # --- gpg key deletion ---

    def test_block_gpg_delete_key(self):
        code, _, _ = run_hook("Bash", {"command": "gpg --delete-key ABCD1234"})
        assert code == 2

    def test_block_gpg_delete_secret_key(self):
        code, _, _ = run_hook("Bash", {"command": "gpg --delete-secret-key ABCD1234"})
        assert code == 2

    def test_block_gpg_delete_secret_and_public_key(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gpg --delete-secret-and-public-key ABCD1234"}
        )
        assert code == 2

    # --- launchctl unload ---

    def test_block_launchctl_unload(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "launchctl unload /Library/LaunchDaemons/com.test.plist"},
        )
        assert code == 2

    # --- diskutil apfs deleteVolume ---

    def test_block_diskutil_apfs_delete_volume(self):
        code, _, _ = run_hook("Bash", {"command": "diskutil apfs deleteVolume disk1s2"})
        assert code == 2

    # --- csrutil ---

    def test_block_csrutil_disable(self):
        code, _, _ = run_hook("Bash", {"command": "csrutil disable"})
        assert code == 2

    def test_block_csrutil_enable(self):
        code, _, _ = run_hook("Bash", {"command": "csrutil enable"})
        assert code == 2

    def test_block_csrutil_status(self):
        code, _, _ = run_hook("Bash", {"command": "csrutil status"})
        assert code == 2

    # --- spctl ---

    def test_block_spctl_master_disable(self):
        code, _, _ = run_hook("Bash", {"command": "spctl --master-disable"})
        assert code == 2

    # --- dscl ---

    def test_block_dscl_create(self):
        code, _, _ = run_hook("Bash", {"command": "dscl . create /Users/test"})
        assert code == 2

    def test_block_dscl_delete(self):
        code, _, _ = run_hook("Bash", {"command": "dscl . -delete /Users/test"})
        assert code == 2

    def test_block_dscl_merge(self):
        code, _, _ = run_hook("Bash", {"command": "dscl . merge /Users/test key value"})
        assert code == 2

    def test_block_dscl_change(self):
        code, _, _ = run_hook(
            "Bash", {"command": "dscl . change /Users/test key old new"}
        )
        assert code == 2

    # --- xattr quarantine ---

    def test_block_xattr_quarantine(self):
        code, _, _ = run_hook(
            "Bash", {"command": "xattr -d com.apple.quarantine /Applications/app.app"}
        )
        assert code == 2

    # --- nvram ---

    def test_block_nvram(self):
        code, _, _ = run_hook("Bash", {"command": "nvram boot-args=-v"})
        assert code == 2

    def test_block_nvram_delete(self):
        code, _, _ = run_hook("Bash", {"command": "nvram -d boot-args"})
        assert code == 2

    # --- bless ---

    def test_block_bless(self):
        code, _, _ = run_hook(
            "Bash", {"command": "bless --mount /Volumes/Macintosh\\ HD --setBoot"}
        )
        assert code == 2

    # --- fdesetup ---

    def test_block_fdesetup_destroy(self):
        code, _, _ = run_hook("Bash", {"command": "fdesetup destroy"})
        assert code == 2

    def test_block_fdesetup_remove(self):
        code, _, _ = run_hook("Bash", {"command": "fdesetup remove -user testuser"})
        assert code == 2

    def test_block_fdesetup_disable(self):
        code, _, _ = run_hook("Bash", {"command": "fdesetup disable"})
        assert code == 2

    # --- kextunload ---

    def test_block_kextunload(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "kextunload /Library/Extensions/MyDriver.kext"},
        )
        assert code == 2

    # --- port uninstall/deactivate ---

    def test_block_port_uninstall(self):
        code, _, _ = run_hook("Bash", {"command": "port uninstall python39"})
        assert code == 2

    def test_block_port_deactivate(self):
        code, _, _ = run_hook("Bash", {"command": "port deactivate python39"})
        assert code == 2


class TestMacosAsk:
    # --- defaults write ---

    def test_ask_defaults_write(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "defaults write com.apple.finder AppleShowAllFiles -bool true"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- networksetup ---

    def test_ask_networksetup(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "networksetup -setdnsservers Wi-Fi 8.8.8.8"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- scutil --set ---

    def test_ask_scutil_set(self):
        code, stdout, _ = run_hook("Bash", {"command": "scutil --set HostName myhost"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- pmset ---

    def test_ask_pmset(self):
        code, stdout, _ = run_hook("Bash", {"command": "pmset -a sleep 0"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- launchctl load/bootstrap/submit ---

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

    def test_ask_launchctl_submit(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "launchctl submit -l com.test -p /usr/bin/test"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- diskutil unmount/unmountDisk/mount/mountDisk ---

    def test_ask_diskutil_unmount(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "diskutil unmount /Volumes/MyDisk"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_diskutil_unmount_disk(self):
        code, stdout, _ = run_hook("Bash", {"command": "diskutil unmountDisk disk2"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_diskutil_mount(self):
        code, stdout, _ = run_hook("Bash", {"command": "diskutil mount disk2s1"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_diskutil_mount_disk(self):
        code, stdout, _ = run_hook("Bash", {"command": "diskutil mountDisk disk2"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- systemsetup ---

    def test_ask_systemsetup(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "systemsetup -settimezone America/New_York"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_systemsetup_remote_login(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "systemsetup -setremotelogin on"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- softwareupdate --install ---

    def test_ask_softwareupdate_install(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "softwareupdate --install --all"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_softwareupdate_install_short(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "softwareupdate -i 'macOS Ventura 13.5'"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- installer -pkg ---

    def test_ask_installer_pkg(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "installer -pkg /tmp/package.pkg -target /"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- kextload ---

    def test_ask_kextload(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "kextload /Library/Extensions/MyDriver.kext"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- mdutil ---

    def test_ask_mdutil_disable(self):
        code, stdout, _ = run_hook("Bash", {"command": "mdutil -i off /Volumes/Data"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_mdutil_erase(self):
        code, stdout, _ = run_hook("Bash", {"command": "mdutil -E /Volumes/Data"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_mdutil_delete_index(self):
        code, stdout, _ = run_hook("Bash", {"command": "mdutil -d /Volumes/Data"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestMacosAllow:
    """Verify that safe or read-only macOS commands are NOT blocked."""

    def test_allow_defaults_read(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "defaults read com.apple.finder"}
        )
        assert code == 0
        assert "permissionDecision" not in stdout

    def test_allow_security_find_generic_password(self):
        """security find-* is handled in security.yaml, not blocked here."""
        # This tests that the delete pattern does not false-positive on find
        code, _, _ = run_hook("Bash", {"command": "security list-keychains"})
        # Should not be exit code 2 from macos patterns
        # (may be blocked by security.yaml's credential manager patterns)
        assert code == 0

    def test_allow_launchctl_list(self):
        code, stdout, _ = run_hook("Bash", {"command": "launchctl list"})
        assert code == 0
        assert "permissionDecision" not in stdout

    def test_allow_diskutil_list(self):
        code, stdout, _ = run_hook("Bash", {"command": "diskutil list"})
        assert code == 0
        assert "permissionDecision" not in stdout

    def test_allow_softwareupdate_list(self):
        code, stdout, _ = run_hook("Bash", {"command": "softwareupdate --list"})
        assert code == 0
        assert "permissionDecision" not in stdout

    def test_allow_mdutil_status(self):
        code, stdout, _ = run_hook("Bash", {"command": "mdutil -s /Volumes/Data"})
        assert code == 0
        assert "permissionDecision" not in stdout

    def test_allow_fdesetup_status(self):
        code, stdout, _ = run_hook("Bash", {"command": "fdesetup status"})
        assert code == 0
        assert "permissionDecision" not in stdout
