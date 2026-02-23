"""Tests for filesystem security patterns (rm, find, shred, permissions, archives)."""

import json

from tests.conftest import run_hook

# =============================================================================
# BLOCK PATTERNS
# =============================================================================


class TestBlockRm:
    """Tests for rm with recursive/force flags."""

    def test_block_rm_rf(self):
        code, _, stderr = run_hook("Bash", {"command": "rm -rf /"})
        assert code == 2
        assert "SECURITY" in stderr

    def test_block_rm_r(self):
        code, _, _ = run_hook("Bash", {"command": "rm -r /tmp/data"})
        assert code == 2

    def test_block_rm_R(self):
        code, _, _ = run_hook("Bash", {"command": "rm -R /tmp/data"})
        assert code == 2

    def test_block_rm_f(self):
        code, _, _ = run_hook("Bash", {"command": "rm -f file.txt"})
        assert code == 2

    def test_block_rm_recursive_long(self):
        code, _, _ = run_hook("Bash", {"command": "rm --recursive /tmp/data"})
        assert code == 2

    def test_block_rm_force_long(self):
        code, _, _ = run_hook("Bash", {"command": "rm --force file.txt"})
        assert code == 2

    def test_block_rm_combined_flags(self):
        code, _, _ = run_hook("Bash", {"command": "rm -rfv /tmp/data"})
        assert code == 2

    def test_block_rm_separated_flags(self):
        code, _, _ = run_hook("Bash", {"command": "rm -v -r /tmp/data"})
        assert code == 2


class TestBlockSudoRm:
    """Tests for sudo rm."""

    def test_block_sudo_rm(self):
        code, _, _ = run_hook("Bash", {"command": "sudo rm /important"})
        assert code == 2

    def test_block_sudo_rm_rf(self):
        code, _, _ = run_hook("Bash", {"command": "sudo rm -rf /var/data"})
        assert code == 2


class TestBlockRmdir:
    """Tests for rmdir with ignore-fail-on-non-empty."""

    def test_block_rmdir_ignore_fail(self):
        code, _, _ = run_hook(
            "Bash", {"command": "rmdir --ignore-fail-on-non-empty /tmp/dir"}
        )
        assert code == 2


class TestBlockAbsolutePathRm:
    """Tests for absolute path rm (bypasses aliases)."""

    def test_block_bin_rm(self):
        code, _, _ = run_hook("Bash", {"command": "/bin/rm file.txt"})
        assert code == 2

    def test_block_usr_bin_rm(self):
        code, _, _ = run_hook("Bash", {"command": "/usr/bin/rm file.txt"})
        assert code == 2


class TestBlockFind:
    """Tests for find with -delete and -exec rm."""

    def test_block_find_delete(self):
        code, _, _ = run_hook("Bash", {"command": "find . -name '*.tmp' -delete"})
        assert code == 2

    def test_block_find_exec_rm(self):
        code, _, _ = run_hook("Bash", {"command": "find /tmp -exec rm {} \\;"})
        assert code == 2

    def test_block_find_exec_bin_rm(self):
        code, _, _ = run_hook("Bash", {"command": "find /tmp -exec /bin/rm {} \\;"})
        assert code == 2

    def test_block_find_exec_usr_bin_rm(self):
        code, _, _ = run_hook("Bash", {"command": "find /tmp -exec /usr/bin/rm {} \\;"})
        assert code == 2

    def test_block_find_exec_shred(self):
        code, _, _ = run_hook("Bash", {"command": "find /tmp -exec shred {} \\;"})
        assert code == 2

    def test_block_find_exec_wipe(self):
        code, _, _ = run_hook("Bash", {"command": "find /data -exec wipe {} \\;"})
        assert code == 2

    def test_block_find_exec_srm(self):
        code, _, _ = run_hook("Bash", {"command": "find /data -exec srm {} \\;"})
        assert code == 2

    def test_block_find_exec_sfill(self):
        code, _, _ = run_hook("Bash", {"command": "find /mnt -exec sfill {} \\;"})
        assert code == 2

    def test_block_find_exec_nwipe(self):
        code, _, _ = run_hook("Bash", {"command": "find /dev -exec nwipe {} \\;"})
        assert code == 2


class TestBlockXargsRm:
    """Tests for xargs piped to rm."""

    def test_block_xargs_rm(self):
        code, _, _ = run_hook("Bash", {"command": "find . -name '*.tmp' | xargs rm"})
        assert code == 2

    def test_block_xargs_rm_with_flags(self):
        code, _, _ = run_hook(
            "Bash", {"command": "find . -name '*.log' | xargs -I{} rm {}"}
        )
        assert code == 2


class TestBlockShred:
    """Tests for shred."""

    def test_block_shred(self):
        code, _, _ = run_hook("Bash", {"command": "shred -u secret.txt"})
        assert code == 2

    def test_block_shred_no_flags(self):
        code, _, _ = run_hook("Bash", {"command": "shred file.txt"})
        assert code == 2


class TestBlockSecureDelete:
    """Tests for sfill, srm, nwipe, wipe (consolidated pattern)."""

    def test_block_sfill(self):
        code, _, _ = run_hook("Bash", {"command": "sfill /tmp"})
        assert code == 2

    def test_block_srm(self):
        code, _, _ = run_hook("Bash", {"command": "srm secret.txt"})
        assert code == 2

    def test_block_nwipe(self):
        code, _, _ = run_hook("Bash", {"command": "nwipe /dev/sda"})
        assert code == 2

    def test_block_wipe(self):
        code, _, _ = run_hook("Bash", {"command": "wipe -r /tmp/sensitive"})
        assert code == 2


class TestBlockRsyncDelete:
    """Tests for rsync --delete."""

    def test_block_rsync_delete(self):
        code, _, _ = run_hook("Bash", {"command": "rsync -av --delete src/ dest/"})
        assert code == 2

    def test_block_rsync_delete_before(self):
        code, _, _ = run_hook("Bash", {"command": "rsync --delete -av src/ dest/"})
        assert code == 2


class TestBlockTruncate:
    """Tests for truncate -s 0."""

    def test_block_truncate_s_0(self):
        code, _, _ = run_hook("Bash", {"command": "truncate -s 0 /var/log/syslog"})
        assert code == 2

    def test_block_truncate_s0_no_space(self):
        code, _, _ = run_hook("Bash", {"command": "truncate -s0 /var/log/syslog"})
        assert code == 2


class TestBlockChmod:
    """Tests for chmod 777 and symbolic equivalents."""

    def test_block_chmod_777(self):
        code, _, _ = run_hook("Bash", {"command": "chmod 777 /tmp/file"})
        assert code == 2

    def test_block_chmod_0777(self):
        code, _, _ = run_hook("Bash", {"command": "chmod 0777 /tmp/file"})
        assert code == 2

    def test_block_chmod_recursive_777(self):
        code, _, _ = run_hook("Bash", {"command": "chmod -R 777 /tmp/dir"})
        assert code == 2

    def test_block_chmod_a_plus_rwx(self):
        code, _, _ = run_hook("Bash", {"command": "chmod a+rwx /tmp/file"})
        assert code == 2

    def test_block_chmod_ugo_plus_rwx(self):
        code, _, _ = run_hook("Bash", {"command": "chmod ugo+rwx /tmp/file"})
        assert code == 2

    def test_block_chmod_plus_rwx(self):
        code, _, _ = run_hook("Bash", {"command": "chmod +rwx /tmp/file"})
        assert code == 2

    def test_block_chmod_recursive_a_plus_rwx(self):
        code, _, _ = run_hook("Bash", {"command": "chmod -R a+rwx /tmp/dir"})
        assert code == 2


class TestBlockChown:
    """Tests for recursive chown to root."""

    def test_block_chown_r_root(self):
        code, _, _ = run_hook("Bash", {"command": "chown -R root /var/data"})
        assert code == 2

    def test_block_chown_r_root_colon_root(self):
        code, _, _ = run_hook("Bash", {"command": "chown -R root:root /var/data"})
        assert code == 2

    def test_block_chown_uppercase_r_root(self):
        code, _, _ = run_hook("Bash", {"command": "chown -r root /var/data"})
        assert code == 2


class TestBlockTar:
    """Tests for destructive tar operations."""

    def test_block_tar_overwrite(self):
        code, _, _ = run_hook("Bash", {"command": "tar xf archive.tar --overwrite"})
        assert code == 2

    def test_block_tar_extract_to_root(self):
        code, _, _ = run_hook("Bash", {"command": "tar xf archive.tar -C /"})
        assert code == 2

    def test_block_tar_extract_long_flag_to_root(self):
        code, _, _ = run_hook("Bash", {"command": "tar --extract -f archive.tar -C /"})
        assert code == 2


# =============================================================================
# ASK PATTERNS
# =============================================================================


class TestAskUnzip:
    """Tests for unzip -o (overwrite without prompting)."""

    def test_ask_unzip_overwrite(self):
        code, stdout, _ = run_hook("Bash", {"command": "unzip -o archive.zip"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_unzip_overwrite_with_dest(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "unzip -o archive.zip -d /tmp/out"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


# =============================================================================
# NEGATIVE TESTS (should NOT trigger)
# =============================================================================


class TestFilesystemAllow:
    """Commands that should pass through without blocking or asking."""

    def test_allow_rm_single_file(self):
        """Plain rm without -r/-R/-f should not be blocked by filesystem patterns."""
        code, stdout, _ = run_hook("Bash", {"command": "rm file.txt"})
        # Should not be blocked by filesystem patterns (code 2)
        # May be caught by other patterns, but not filesystem block
        assert code != 2 or "recursive" in stdout.lower() or "force" in stdout.lower()

    def test_allow_ls(self):
        code, stdout, _ = run_hook("Bash", {"command": "ls -la /tmp"})
        assert code == 0
        assert stdout == ""

    def test_allow_chmod_644(self):
        code, stdout, _ = run_hook("Bash", {"command": "chmod 644 file.txt"})
        assert code == 0

    def test_allow_chmod_755(self):
        code, stdout, _ = run_hook("Bash", {"command": "chmod 755 script.sh"})
        assert code == 0

    def test_allow_chown_non_root(self):
        code, stdout, _ = run_hook("Bash", {"command": "chown user:group file.txt"})
        assert code == 0

    def test_allow_tar_extract_to_dir(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "tar xf archive.tar -C /tmp/safe"}
        )
        assert code == 0

    def test_allow_rsync_without_delete(self):
        code, stdout, _ = run_hook("Bash", {"command": "rsync -av src/ dest/"})
        assert code == 0

    def test_allow_unzip_without_overwrite(self):
        code, stdout, _ = run_hook("Bash", {"command": "unzip archive.zip"})
        assert code == 0
        assert stdout == ""

    def test_allow_find_without_delete(self):
        code, stdout, _ = run_hook("Bash", {"command": "find . -name '*.py' -type f"})
        assert code == 0
        assert stdout == ""

    def test_allow_truncate_nonzero_size(self):
        code, stdout, _ = run_hook("Bash", {"command": "truncate -s 1024 file.dat"})
        assert code == 0
