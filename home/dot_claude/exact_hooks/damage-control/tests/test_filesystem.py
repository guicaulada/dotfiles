"""Tests for filesystem security patterns (rm, find, shred, permissions, archives)."""

import json

from tests.conftest import assert_allows, assert_asks, run_hook

# =============================================================================
# BLOCK PATTERNS
# =============================================================================


class TestBlockRm:
    """Tests for rm with recursive/force flags."""

    def test_block_rm_rf(self):
        assert_asks('Bash', {'command': 'rm -rf /'})

    def test_block_rm_r(self):
        assert_asks('Bash', {'command': 'rm -r /tmp/data'})

    def test_block_rm_R(self):
        assert_asks('Bash', {'command': 'rm -R /tmp/data'})

    def test_block_rm_f(self):
        assert_asks('Bash', {'command': 'rm -f file.txt'})

    def test_block_rm_recursive_long(self):
        assert_asks('Bash', {'command': 'rm --recursive /tmp/data'})

    def test_block_rm_force_long(self):
        assert_asks('Bash', {'command': 'rm --force file.txt'})

    def test_block_rm_combined_flags(self):
        assert_asks('Bash', {'command': 'rm -rfv /tmp/data'})

    def test_block_rm_separated_flags(self):
        assert_asks('Bash', {'command': 'rm -v -r /tmp/data'})


class TestBlockSudoRm:
    """Tests for sudo rm."""

    def test_block_sudo_rm(self):
        assert_asks('Bash', {'command': 'sudo rm /important'})

    def test_block_sudo_rm_rf(self):
        assert_asks('Bash', {'command': 'sudo rm -rf /var/data'})


class TestBlockRmdir:
    """Tests for rmdir with ignore-fail-on-non-empty."""

    def test_block_rmdir_ignore_fail(self):
        assert_asks('Bash', {'command': 'rmdir --ignore-fail-on-non-empty /tmp/dir'})


class TestBlockAbsolutePathRm:
    """Tests for absolute path rm (bypasses aliases)."""

    def test_block_bin_rm(self):
        assert_asks('Bash', {'command': '/bin/rm file.txt'})

    def test_block_usr_bin_rm(self):
        assert_asks('Bash', {'command': '/usr/bin/rm file.txt'})


class TestBlockFind:
    """Tests for find with -delete and -exec rm."""

    def test_block_find_delete(self):
        assert_asks('Bash', {'command': "find . -name '*.tmp' -delete"})

    def test_block_find_exec_rm(self):
        assert_asks('Bash', {'command': 'find /tmp -exec rm {} \\;'})

    def test_block_find_exec_bin_rm(self):
        assert_asks('Bash', {'command': 'find /tmp -exec /bin/rm {} \\;'})

    def test_block_find_exec_usr_bin_rm(self):
        assert_asks('Bash', {'command': 'find /tmp -exec /usr/bin/rm {} \\;'})

    def test_block_find_exec_shred(self):
        assert_asks('Bash', {'command': 'find /tmp -exec shred {} \\;'})

    def test_block_find_exec_wipe(self):
        assert_asks('Bash', {'command': 'find /data -exec wipe {} \\;'})

    def test_block_find_exec_srm(self):
        assert_asks('Bash', {'command': 'find /data -exec srm {} \\;'})

    def test_block_find_exec_sfill(self):
        assert_asks('Bash', {'command': 'find /mnt -exec sfill {} \\;'})

    def test_block_find_exec_nwipe(self):
        assert_asks('Bash', {'command': 'find /dev -exec nwipe {} \\;'})


class TestBlockXargsRm:
    """Tests for xargs piped to rm."""

    def test_block_xargs_rm(self):
        assert_asks('Bash', {'command': "find . -name '*.tmp' | xargs rm"})

    def test_block_xargs_rm_with_flags(self):
        assert_asks('Bash', {'command': "find . -name '*.log' | xargs -I{} rm {}"})


class TestBlockShred:
    """Tests for shred."""

    def test_block_shred(self):
        assert_asks('Bash', {'command': 'shred -u secret.txt'})

    def test_block_shred_no_flags(self):
        assert_asks('Bash', {'command': 'shred file.txt'})


class TestBlockSecureDelete:
    """Tests for sfill, srm, nwipe, wipe (consolidated pattern)."""

    def test_block_sfill(self):
        assert_asks('Bash', {'command': 'sfill /tmp'})

    def test_block_srm(self):
        assert_asks('Bash', {'command': 'srm secret.txt'})

    def test_block_nwipe(self):
        assert_asks('Bash', {'command': 'nwipe /dev/sda'})

    def test_block_wipe(self):
        assert_asks('Bash', {'command': 'wipe -r /tmp/sensitive'})


class TestBlockRsyncDelete:
    """Tests for rsync --delete."""

    def test_block_rsync_delete(self):
        assert_asks('Bash', {'command': 'rsync -av --delete src/ dest/'})

    def test_block_rsync_delete_before(self):
        assert_asks('Bash', {'command': 'rsync --delete -av src/ dest/'})


class TestBlockTruncate:
    """Tests for truncate -s 0."""

    def test_block_truncate_s_0(self):
        assert_asks("Bash", {"command": "truncate -s 0 /var/log/syslog"})

    def test_block_truncate_s0_no_space(self):
        assert_asks("Bash", {"command": "truncate -s0 /var/log/syslog"})


class TestBlockChmod:
    """Tests for chmod 777 and symbolic equivalents."""

    def test_block_chmod_777(self):
        assert_asks('Bash', {'command': 'chmod 777 /tmp/file'})

    def test_block_chmod_0777(self):
        assert_asks('Bash', {'command': 'chmod 0777 /tmp/file'})

    def test_block_chmod_recursive_777(self):
        assert_asks('Bash', {'command': 'chmod -R 777 /tmp/dir'})

    def test_block_chmod_a_plus_rwx(self):
        assert_asks('Bash', {'command': 'chmod a+rwx /tmp/file'})

    def test_block_chmod_ugo_plus_rwx(self):
        assert_asks('Bash', {'command': 'chmod ugo+rwx /tmp/file'})

    def test_block_chmod_plus_rwx(self):
        assert_asks('Bash', {'command': 'chmod +rwx /tmp/file'})

    def test_block_chmod_recursive_a_plus_rwx(self):
        assert_asks('Bash', {'command': 'chmod -R a+rwx /tmp/dir'})


class TestBlockChown:
    """Tests for recursive chown to root."""

    def test_block_chown_r_root(self):
        assert_asks('Bash', {'command': 'chown -R root /var/data'})

    def test_block_chown_r_root_colon_root(self):
        assert_asks('Bash', {'command': 'chown -R root:root /var/data'})

    def test_block_chown_uppercase_r_root(self):
        assert_asks('Bash', {'command': 'chown -r root /var/data'})


class TestBlockTar:
    """Tests for destructive tar operations."""

    def test_block_tar_overwrite(self):
        assert_asks('Bash', {'command': 'tar xf archive.tar --overwrite'})

    def test_block_tar_extract_to_root(self):
        assert_asks('Bash', {'command': 'tar xf archive.tar -C /'})

    def test_block_tar_extract_long_flag_to_root(self):
        assert_asks('Bash', {'command': 'tar --extract -f archive.tar -C /'})

    def test_block_tar_extract_to_root_no_space(self):
        assert_asks("Bash", {"command": "tar xf archive.tar -C/"})

    def test_allow_tar_extract_to_subdir_of_root(self):
        # `-C /etc` must NOT be read as extraction to root.
        assert_allows("Bash", {"command": "tar xf archive.tar -C /etc/app"})


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
