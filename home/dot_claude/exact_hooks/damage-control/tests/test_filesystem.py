"""Tests for filesystem security patterns (rm, find, shred, permissions)."""

from tests.conftest import run_hook


class TestFilesystemBlock:
    def test_block_rm_rf(self):
        code, stdout, stderr = run_hook("Bash", {"command": "rm -rf /"})
        assert code == 2
        assert "SECURITY" in stderr

    def test_block_rm_recursive(self):
        code, _, stderr = run_hook("Bash", {"command": "rm --recursive /tmp/data"})
        assert code == 2

    def test_block_rm_force(self):
        code, _, stderr = run_hook("Bash", {"command": "rm --force file.txt"})
        assert code == 2

    def test_block_sudo_rm(self):
        code, _, _ = run_hook("Bash", {"command": "sudo rm /important"})
        assert code == 2

    def test_block_find_delete(self):
        code, _, _ = run_hook("Bash", {"command": "find . -name '*.tmp' -delete"})
        assert code == 2

    def test_block_shred(self):
        code, _, _ = run_hook("Bash", {"command": "shred -u secret.txt"})
        assert code == 2

    def test_block_find_exec_rm(self):
        code, _, _ = run_hook("Bash", {"command": "find /tmp -exec rm {} \\;"})
        assert code == 2

    def test_block_xargs_rm(self):
        code, _, _ = run_hook("Bash", {"command": "find . -name '*.tmp' | xargs rm"})
        assert code == 2

    def test_block_rsync_delete(self):
        code, _, _ = run_hook("Bash", {"command": "rsync -av --delete src/ dest/"})
        assert code == 2

    def test_block_chmod_777(self):
        code, _, _ = run_hook("Bash", {"command": "chmod 777 /tmp/file"})
        assert code == 2
