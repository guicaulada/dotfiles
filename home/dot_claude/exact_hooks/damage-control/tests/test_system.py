"""Tests for system destruction, kernel, disk, logs, backup patterns."""

import json

from tests.conftest import assert_asks, run_hook

# =============================================================================
# SYSTEM-LEVEL DESTRUCTION (block)
# =============================================================================


class TestSystemBlock:
    def test_block_shutdown(self):
        assert_asks('Bash', {'command': 'shutdown -h now'})

    def test_block_reboot(self):
        assert_asks('Bash', {'command': 'reboot'})

    def test_block_halt(self):
        assert_asks('Bash', {'command': 'halt'})

    def test_block_poweroff(self):
        assert_asks('Bash', {'command': 'poweroff'})

    def test_block_systemctl_stop(self):
        assert_asks('Bash', {'command': 'systemctl stop nginx'})

    def test_block_systemctl_disable(self):
        assert_asks('Bash', {'command': 'systemctl disable docker'})

    def test_block_systemctl_mask(self):
        assert_asks('Bash', {'command': 'systemctl mask sshd'})

    def test_block_iptables_flush(self):
        assert_asks('Bash', {'command': 'iptables -F'})

    def test_block_iptables_flush_long(self):
        assert_asks('Bash', {'command': 'iptables --flush'})

    def test_block_pfctl_disable(self):
        assert_asks('Bash', {'command': 'pfctl -d'})

    def test_block_tmutil_delete(self):
        assert_asks('Bash', {'command': 'tmutil delete /backup/2024'})

    def test_block_tmutil_disable(self):
        assert_asks('Bash', {'command': 'tmutil disable'})

    def test_block_tmutil_disablelocal(self):
        assert_asks('Bash', {'command': 'tmutil disablelocal'})

    def test_block_fdisk(self):
        assert_asks('Bash', {'command': 'fdisk /dev/sda'})

    def test_block_parted(self):
        assert_asks('Bash', {'command': 'parted /dev/sda'})

    def test_block_mkfs(self):
        assert_asks('Bash', {'command': 'mkfs.ext4 /dev/sda1'})

    def test_block_dd_device(self):
        assert_asks('Bash', {'command': 'dd if=/dev/zero of=/dev/sda'})

    def test_block_diskutil_erase_disk(self):
        assert_asks('Bash', {'command': 'diskutil eraseDisk JHFS+ Untitled /dev/disk2'})

    def test_block_diskutil_erase_volume(self):
        assert_asks('Bash', {'command': 'diskutil eraseVolume APFS Untitled disk2s1'})

    def test_block_diskutil_partition_disk(self):
        assert_asks('Bash', {'command': 'diskutil partitionDisk /dev/disk2 GPT JHFS+ Untitled 0b'})

    def test_block_redirect_to_device(self):
        assert_asks('Bash', {'command': 'echo data > /dev/sda'})

    def test_block_redirect_append_to_device(self):
        assert_asks('Bash', {'command': 'echo data >> /dev/sdb'})

    def test_block_badblocks_write(self):
        assert_asks('Bash', {'command': 'badblocks -w /dev/sda'})

    def test_block_blkdiscard(self):
        assert_asks('Bash', {'command': 'blkdiscard /dev/sda'})

    def test_block_sgdisk_zap_all(self):
        assert_asks('Bash', {'command': 'sgdisk --zap-all /dev/sda'})

    def test_block_sgdisk_clear(self):
        assert_asks('Bash', {'command': 'sgdisk --clear /dev/sda'})

    def test_block_sgdisk_delete(self):
        assert_asks('Bash', {'command': 'sgdisk --delete=1 /dev/sda'})

    def test_block_sgdisk_z(self):
        assert_asks('Bash', {'command': 'sgdisk -z /dev/sda'})

    def test_block_sgdisk_o(self):
        assert_asks('Bash', {'command': 'sgdisk -o /dev/sda'})

    def test_block_cryptsetup_close(self):
        assert_asks('Bash', {'command': 'cryptsetup close myvolume'})

    def test_block_cryptsetup_luks_erase(self):
        assert_asks('Bash', {'command': 'cryptsetup luksErase /dev/sda1'})

    def test_block_cryptsetup_erase(self):
        assert_asks('Bash', {'command': 'cryptsetup erase /dev/sda1'})

    def test_block_cryptsetup_luks_close(self):
        assert_asks('Bash', {'command': 'cryptsetup luksClose myvolume'})

    def test_block_hdparm_security_erase(self):
        assert_asks('Bash', {'command': 'hdparm --security-erase password /dev/sda'})

    def test_block_hdparm_sanitize_freeze(self):
        assert_asks('Bash', {'command': 'hdparm --sanitize-freeze /dev/sda'})

    def test_block_hdparm_trim_sector_ranges(self):
        assert_asks('Bash', {'command': 'hdparm --trim-sector-ranges 0:100 /dev/sda'})

    def test_block_nvme_format(self):
        assert_asks('Bash', {'command': 'nvme format /dev/nvme0n1'})

    def test_block_nvme_sanitize(self):
        assert_asks('Bash', {'command': 'nvme sanitize /dev/nvme0n1'})

    def test_block_swapoff_a(self):
        assert_asks('Bash', {'command': 'swapoff -a'})


# =============================================================================
# USER AND GROUP MANAGEMENT (block)
# =============================================================================


class TestUserGroupBlock:
    def test_block_userdel(self):
        assert_asks('Bash', {'command': 'userdel testuser'})

    def test_block_groupdel(self):
        assert_asks('Bash', {'command': 'groupdel testgroup'})

    def test_block_deluser(self):
        assert_asks('Bash', {'command': 'deluser testuser'})


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
        assert_asks('Bash', {'command': 'rmmod mymodule'})

    def test_block_modprobe_remove_short(self):
        assert_asks('Bash', {'command': 'modprobe -r mymodule'})

    def test_block_modprobe_remove_long(self):
        assert_asks('Bash', {'command': 'modprobe --remove mymodule'})

    def test_block_telinit(self):
        assert_asks('Bash', {'command': 'telinit 6'})

    def test_block_init_0(self):
        assert_asks('Bash', {'command': 'init 0'})

    def test_block_init_1(self):
        assert_asks('Bash', {'command': 'init 1'})

    def test_block_init_6(self):
        assert_asks('Bash', {'command': 'init 6'})


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
        assert_asks('Bash', {'command': 'setenforce 0'})

    def test_block_aa_disable(self):
        assert_asks('Bash', {'command': 'aa-disable /etc/apparmor.d/profile'})

    def test_block_aa_teardown(self):
        assert_asks('Bash', {'command': 'aa-teardown'})

    def test_block_apparmor_parser_remove_short(self):
        assert_asks('Bash', {'command': 'apparmor_parser -R /etc/apparmor.d/profile'})

    def test_block_apparmor_parser_remove_long(self):
        assert_asks('Bash', {'command': 'apparmor_parser --remove /etc/apparmor.d/profile'})


# =============================================================================
# DISK / VOLUME MANAGEMENT (block)
# =============================================================================


class TestDiskVolumeBlock:
    def test_block_mount(self):
        assert_asks('Bash', {'command': 'mount /dev/sda1 /mnt'})

    def test_block_umount(self):
        assert_asks('Bash', {'command': 'umount /mnt'})

    def test_block_lvremove(self):
        assert_asks('Bash', {'command': 'lvremove /dev/vg0/lv0'})

    def test_block_vgremove(self):
        assert_asks('Bash', {'command': 'vgremove vg0'})

    def test_block_pvremove(self):
        assert_asks('Bash', {'command': 'pvremove /dev/sda1'})

    def test_block_mdadm_stop(self):
        assert_asks('Bash', {'command': 'mdadm --stop /dev/md0'})

    def test_block_mdadm_zero_superblock(self):
        assert_asks('Bash', {'command': 'mdadm --zero-superblock /dev/sda1'})

    def test_block_wipefs(self):
        assert_asks('Bash', {'command': 'wipefs -a /dev/sda1'})


# =============================================================================
# LOG / AUDIT TRAIL MANIPULATION (block)
# =============================================================================


class TestLogBlock:
    def test_block_journalctl_vacuum(self):
        assert_asks('Bash', {'command': 'journalctl --vacuum-time=1d'})

    def test_block_journalctl_rotate(self):
        assert_asks('Bash', {'command': 'journalctl --rotate'})

    def test_block_logrotate_force(self):
        assert_asks('Bash', {'command': 'logrotate --force /etc/logrotate.conf'})

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
        assert_asks('Bash', {'command': 'restic forget --keep-last 1'})

    def test_block_restic_prune(self):
        assert_asks('Bash', {'command': 'restic prune'})

    def test_block_borg_delete(self):
        assert_asks('Bash', {'command': 'borg delete repo::archive'})

    def test_block_borg_prune(self):
        assert_asks('Bash', {'command': 'borg prune --keep-daily 7'})

    def test_block_borg_compact(self):
        assert_asks('Bash', {'command': 'borg compact repo'})


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
