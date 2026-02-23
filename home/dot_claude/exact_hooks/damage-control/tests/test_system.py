"""Tests for system destruction, kernel, disk, logs, backup patterns."""

import json

from tests.conftest import run_hook

# =============================================================================
# SYSTEM-LEVEL DESTRUCTION (block)
# =============================================================================


class TestSystemBlock:
    def test_block_shutdown(self):
        code, _, _ = run_hook("Bash", {"command": "shutdown -h now"})
        assert code == 2

    def test_block_reboot(self):
        code, _, _ = run_hook("Bash", {"command": "reboot"})
        assert code == 2

    def test_block_halt(self):
        code, _, _ = run_hook("Bash", {"command": "halt"})
        assert code == 2

    def test_block_poweroff(self):
        code, _, _ = run_hook("Bash", {"command": "poweroff"})
        assert code == 2

    def test_block_systemctl_stop(self):
        code, _, _ = run_hook("Bash", {"command": "systemctl stop nginx"})
        assert code == 2

    def test_block_systemctl_disable(self):
        code, _, _ = run_hook("Bash", {"command": "systemctl disable docker"})
        assert code == 2

    def test_block_systemctl_mask(self):
        code, _, _ = run_hook("Bash", {"command": "systemctl mask sshd"})
        assert code == 2

    def test_block_iptables_flush(self):
        code, _, _ = run_hook("Bash", {"command": "iptables -F"})
        assert code == 2

    def test_block_iptables_flush_long(self):
        code, _, _ = run_hook("Bash", {"command": "iptables --flush"})
        assert code == 2

    def test_block_pfctl_disable(self):
        code, _, _ = run_hook("Bash", {"command": "pfctl -d"})
        assert code == 2

    def test_block_tmutil_delete(self):
        code, _, _ = run_hook("Bash", {"command": "tmutil delete /backup/2024"})
        assert code == 2

    def test_block_tmutil_disable(self):
        code, _, _ = run_hook("Bash", {"command": "tmutil disable"})
        assert code == 2

    def test_block_tmutil_disablelocal(self):
        code, _, _ = run_hook("Bash", {"command": "tmutil disablelocal"})
        assert code == 2

    def test_block_fdisk(self):
        code, _, _ = run_hook("Bash", {"command": "fdisk /dev/sda"})
        assert code == 2

    def test_block_parted(self):
        code, _, _ = run_hook("Bash", {"command": "parted /dev/sda"})
        assert code == 2

    def test_block_mkfs(self):
        code, _, _ = run_hook("Bash", {"command": "mkfs.ext4 /dev/sda1"})
        assert code == 2

    def test_block_dd_device(self):
        code, _, _ = run_hook("Bash", {"command": "dd if=/dev/zero of=/dev/sda"})
        assert code == 2

    def test_block_diskutil_erase_disk(self):
        code, _, _ = run_hook(
            "Bash", {"command": "diskutil eraseDisk JHFS+ Untitled /dev/disk2"}
        )
        assert code == 2

    def test_block_diskutil_erase_volume(self):
        code, _, _ = run_hook(
            "Bash", {"command": "diskutil eraseVolume APFS Untitled disk2s1"}
        )
        assert code == 2

    def test_block_diskutil_partition_disk(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "diskutil partitionDisk /dev/disk2 GPT JHFS+ Untitled 0b"},
        )
        assert code == 2

    def test_block_redirect_to_device(self):
        code, _, _ = run_hook("Bash", {"command": "echo data > /dev/sda"})
        assert code == 2

    def test_block_redirect_append_to_device(self):
        code, _, _ = run_hook("Bash", {"command": "echo data >> /dev/sdb"})
        assert code == 2

    def test_block_badblocks_write(self):
        code, _, _ = run_hook("Bash", {"command": "badblocks -w /dev/sda"})
        assert code == 2

    def test_block_blkdiscard(self):
        code, _, _ = run_hook("Bash", {"command": "blkdiscard /dev/sda"})
        assert code == 2

    def test_block_sgdisk_zap_all(self):
        code, _, _ = run_hook("Bash", {"command": "sgdisk --zap-all /dev/sda"})
        assert code == 2

    def test_block_sgdisk_clear(self):
        code, _, _ = run_hook("Bash", {"command": "sgdisk --clear /dev/sda"})
        assert code == 2

    def test_block_sgdisk_delete(self):
        code, _, _ = run_hook("Bash", {"command": "sgdisk --delete=1 /dev/sda"})
        assert code == 2

    def test_block_sgdisk_z(self):
        code, _, _ = run_hook("Bash", {"command": "sgdisk -z /dev/sda"})
        assert code == 2

    def test_block_sgdisk_o(self):
        code, _, _ = run_hook("Bash", {"command": "sgdisk -o /dev/sda"})
        assert code == 2

    def test_block_cryptsetup_close(self):
        code, _, _ = run_hook("Bash", {"command": "cryptsetup close myvolume"})
        assert code == 2

    def test_block_cryptsetup_luks_erase(self):
        code, _, _ = run_hook("Bash", {"command": "cryptsetup luksErase /dev/sda1"})
        assert code == 2

    def test_block_cryptsetup_erase(self):
        code, _, _ = run_hook("Bash", {"command": "cryptsetup erase /dev/sda1"})
        assert code == 2

    def test_block_cryptsetup_luks_close(self):
        code, _, _ = run_hook("Bash", {"command": "cryptsetup luksClose myvolume"})
        assert code == 2

    def test_block_hdparm_security_erase(self):
        code, _, _ = run_hook(
            "Bash", {"command": "hdparm --security-erase password /dev/sda"}
        )
        assert code == 2

    def test_block_hdparm_sanitize_freeze(self):
        code, _, _ = run_hook("Bash", {"command": "hdparm --sanitize-freeze /dev/sda"})
        assert code == 2

    def test_block_hdparm_trim_sector_ranges(self):
        code, _, _ = run_hook(
            "Bash", {"command": "hdparm --trim-sector-ranges 0:100 /dev/sda"}
        )
        assert code == 2

    def test_block_nvme_format(self):
        code, _, _ = run_hook("Bash", {"command": "nvme format /dev/nvme0n1"})
        assert code == 2

    def test_block_nvme_sanitize(self):
        code, _, _ = run_hook("Bash", {"command": "nvme sanitize /dev/nvme0n1"})
        assert code == 2

    def test_block_swapoff_a(self):
        code, _, _ = run_hook("Bash", {"command": "swapoff -a"})
        assert code == 2


# =============================================================================
# USER AND GROUP MANAGEMENT (block)
# =============================================================================


class TestUserGroupBlock:
    def test_block_userdel(self):
        code, _, _ = run_hook("Bash", {"command": "userdel testuser"})
        assert code == 2

    def test_block_groupdel(self):
        code, _, _ = run_hook("Bash", {"command": "groupdel testgroup"})
        assert code == 2

    def test_block_deluser(self):
        code, _, _ = run_hook("Bash", {"command": "deluser testuser"})
        assert code == 2


# =============================================================================
# USER AND GROUP MANAGEMENT (ask)
# =============================================================================


class TestUserGroupAsk:
    def test_ask_useradd(self):
        code, stdout, _ = run_hook("Bash", {"command": "useradd testuser"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_adduser(self):
        code, stdout, _ = run_hook("Bash", {"command": "adduser testuser"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_usermod(self):
        code, stdout, _ = run_hook("Bash", {"command": "usermod -aG docker testuser"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_passwd(self):
        code, stdout, _ = run_hook("Bash", {"command": "passwd testuser"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_chpasswd(self):
        code, stdout, _ = run_hook("Bash", {"command": "echo 'user:pass' | chpasswd"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_groupadd(self):
        code, stdout, _ = run_hook("Bash", {"command": "groupadd devteam"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_groupmod(self):
        code, stdout, _ = run_hook("Bash", {"command": "groupmod -n newname oldname"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


# =============================================================================
# KERNEL MODULES (block)
# =============================================================================


class TestKernelBlock:
    def test_block_rmmod(self):
        code, _, _ = run_hook("Bash", {"command": "rmmod mymodule"})
        assert code == 2

    def test_block_modprobe_remove_short(self):
        code, _, _ = run_hook("Bash", {"command": "modprobe -r mymodule"})
        assert code == 2

    def test_block_modprobe_remove_long(self):
        code, _, _ = run_hook("Bash", {"command": "modprobe --remove mymodule"})
        assert code == 2

    def test_block_telinit(self):
        code, _, _ = run_hook("Bash", {"command": "telinit 6"})
        assert code == 2

    def test_block_init_0(self):
        code, _, _ = run_hook("Bash", {"command": "init 0"})
        assert code == 2

    def test_block_init_1(self):
        code, _, _ = run_hook("Bash", {"command": "init 1"})
        assert code == 2

    def test_block_init_6(self):
        code, _, _ = run_hook("Bash", {"command": "init 6"})
        assert code == 2


# =============================================================================
# KERNEL MODULES (ask)
# =============================================================================


class TestKernelAsk:
    def test_ask_insmod(self):
        code, stdout, _ = run_hook("Bash", {"command": "insmod /path/to/module.ko"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


# =============================================================================
# MANDATORY ACCESS CONTROL (block)
# =============================================================================


class TestMACBlock:
    def test_block_setenforce_0(self):
        code, _, _ = run_hook("Bash", {"command": "setenforce 0"})
        assert code == 2

    def test_block_aa_disable(self):
        code, _, _ = run_hook("Bash", {"command": "aa-disable /etc/apparmor.d/profile"})
        assert code == 2

    def test_block_aa_teardown(self):
        code, _, _ = run_hook("Bash", {"command": "aa-teardown"})
        assert code == 2

    def test_block_apparmor_parser_remove_short(self):
        code, _, _ = run_hook(
            "Bash", {"command": "apparmor_parser -R /etc/apparmor.d/profile"}
        )
        assert code == 2

    def test_block_apparmor_parser_remove_long(self):
        code, _, _ = run_hook(
            "Bash", {"command": "apparmor_parser --remove /etc/apparmor.d/profile"}
        )
        assert code == 2


# =============================================================================
# DISK / VOLUME MANAGEMENT (block)
# =============================================================================


class TestDiskVolumeBlock:
    def test_block_mount(self):
        code, _, _ = run_hook("Bash", {"command": "mount /dev/sda1 /mnt"})
        assert code == 2

    def test_block_umount(self):
        code, _, _ = run_hook("Bash", {"command": "umount /mnt"})
        assert code == 2

    def test_block_lvremove(self):
        code, _, _ = run_hook("Bash", {"command": "lvremove /dev/vg0/lv0"})
        assert code == 2

    def test_block_vgremove(self):
        code, _, _ = run_hook("Bash", {"command": "vgremove vg0"})
        assert code == 2

    def test_block_pvremove(self):
        code, _, _ = run_hook("Bash", {"command": "pvremove /dev/sda1"})
        assert code == 2

    def test_block_mdadm_stop(self):
        code, _, _ = run_hook("Bash", {"command": "mdadm --stop /dev/md0"})
        assert code == 2

    def test_block_mdadm_zero_superblock(self):
        code, _, _ = run_hook("Bash", {"command": "mdadm --zero-superblock /dev/sda1"})
        assert code == 2

    def test_block_wipefs(self):
        code, _, _ = run_hook("Bash", {"command": "wipefs -a /dev/sda1"})
        assert code == 2


# =============================================================================
# LOG / AUDIT TRAIL MANIPULATION (block)
# =============================================================================


class TestLogBlock:
    def test_block_journalctl_vacuum(self):
        code, _, _ = run_hook("Bash", {"command": "journalctl --vacuum-time=1d"})
        assert code == 2

    def test_block_journalctl_rotate(self):
        code, _, _ = run_hook("Bash", {"command": "journalctl --rotate"})
        assert code == 2

    def test_block_logrotate_force(self):
        code, _, _ = run_hook(
            "Bash", {"command": "logrotate --force /etc/logrotate.conf"}
        )
        assert code == 2

    def test_block_redirect_truncate_log(self):
        code, _, _ = run_hook("Bash", {"command": "> /var/log/syslog"})
        assert code == 2

    def test_block_redirect_truncate_auth_log(self):
        code, _, _ = run_hook("Bash", {"command": "echo '' > /var/log/auth.log"})
        assert code == 2


# =============================================================================
# BACKUP / RESTORE TOOLS (block)
# =============================================================================


class TestBackupBlock:
    def test_block_restic_forget(self):
        code, _, _ = run_hook("Bash", {"command": "restic forget --keep-last 1"})
        assert code == 2

    def test_block_restic_prune(self):
        code, _, _ = run_hook("Bash", {"command": "restic prune"})
        assert code == 2

    def test_block_borg_delete(self):
        code, _, _ = run_hook("Bash", {"command": "borg delete repo::archive"})
        assert code == 2

    def test_block_borg_prune(self):
        code, _, _ = run_hook("Bash", {"command": "borg prune --keep-daily 7"})
        assert code == 2

    def test_block_borg_compact(self):
        code, _, _ = run_hook("Bash", {"command": "borg compact repo"})
        assert code == 2


# =============================================================================
# ADDITIONAL SYSTEM TOOLS (ask)
# =============================================================================


class TestSystemToolsAsk:
    def test_ask_visudo(self):
        code, stdout, _ = run_hook("Bash", {"command": "visudo"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_vipw(self):
        code, stdout, _ = run_hook("Bash", {"command": "vipw"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_chsh(self):
        code, stdout, _ = run_hook("Bash", {"command": "chsh -s /bin/zsh testuser"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
