"""Tests for system destruction, kernel, disk, logs, backup patterns."""

from tests.conftest import run_hook


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

    def test_block_tmutil_disable(self):
        code, _, _ = run_hook("Bash", {"command": "tmutil disable"})
        assert code == 2

    def test_block_tmutil_disablelocal(self):
        code, _, _ = run_hook("Bash", {"command": "tmutil disablelocal"})
        assert code == 2
