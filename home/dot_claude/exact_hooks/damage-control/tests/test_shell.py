"""Tests for shell eval, code injection, process destruction, and history patterns."""

import json

from tests.conftest import run_hook


class TestShellBlock:
    def test_block_eval(self):
        code, _, _ = run_hook("Bash", {"command": "eval $(echo dangerous)"})
        assert code == 2

    def test_block_base64_decode_pipe_bash(self):
        code, _, _ = run_hook(
            "Bash", {"command": "echo cm0gLXJmIC8= | base64 -d | bash"}
        )
        assert code == 2

    def test_block_base64_decode_pipe_sh(self):
        code, _, _ = run_hook(
            "Bash", {"command": "echo payload | base64 --decode | sh"}
        )
        assert code == 2

    def test_block_backslash_rm(self):
        code, _, _ = run_hook("Bash", {"command": "\\rm -rf /tmp/data"})
        assert code == 2

    def test_block_command_rm(self):
        code, _, _ = run_hook("Bash", {"command": "command rm /tmp/file"})
        assert code == 2

    def test_block_xargs_shred(self):
        code, _, _ = run_hook("Bash", {"command": "find . -name '*.tmp' | xargs shred"})
        assert code == 2

    def test_block_xargs_chmod(self):
        code, _, _ = run_hook("Bash", {"command": "find . | xargs chmod 777"})
        assert code == 2

    def test_block_unset_path(self):
        code, _, _ = run_hook("Bash", {"command": "unset PATH"})
        assert code == 2

    def test_block_unset_home(self):
        code, _, _ = run_hook("Bash", {"command": "unset HOME"})
        assert code == 2

    def test_block_export_path_overwrite(self):
        code, _, _ = run_hook("Bash", {"command": "export PATH=/usr/local/bin"})
        assert code == 2

    def test_block_python_rmtree(self):
        code, _, _ = run_hook(
            "Bash", {"command": "python -c 'import shutil; shutil.rmtree(\"/tmp\")'"}
        )
        assert code == 2

    def test_block_python3_os_remove(self):
        code, _, _ = run_hook(
            "Bash", {"command": "python3 -c 'import os; os.remove(\"/tmp/f\")'"}
        )
        assert code == 2

    def test_block_socat_listen(self):
        code, _, _ = run_hook(
            "Bash", {"command": "socat TCP-LISTEN:4444,reuseaddr EXEC:/bin/bash"}
        )
        assert code == 2

    def test_block_kill_all(self):
        code, _, _ = run_hook("Bash", {"command": "kill -9 -1"})
        assert code == 2

    def test_block_history_clear(self):
        code, _, _ = run_hook("Bash", {"command": "history -c"})
        assert code == 2


class TestShellAsk:
    def test_ask_source(self):
        code, stdout, _ = run_hook("Bash", {"command": "source venv/bin/activate"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_exec(self):
        code, stdout, _ = run_hook("Bash", {"command": "exec /bin/zsh"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_bash_c(self):
        code, stdout, _ = run_hook("Bash", {"command": "bash -c 'echo hello'"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_sh_c(self):
        code, stdout, _ = run_hook("Bash", {"command": "sh -c 'echo hello'"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_node_e(self):
        code, stdout, _ = run_hook("Bash", {"command": "node -e 'console.log(1)'"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_ruby_e(self):
        code, stdout, _ = run_hook("Bash", {"command": "ruby -e 'puts 1'"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_perl_e(self):
        code, stdout, _ = run_hook("Bash", {"command": "perl -e 'print 1'"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_killall(self):
        code, stdout, _ = run_hook("Bash", {"command": "killall node"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_pkill(self):
        code, stdout, _ = run_hook("Bash", {"command": "pkill python"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
