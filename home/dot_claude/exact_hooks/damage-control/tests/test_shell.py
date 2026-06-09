"""Tests for shell eval, code injection, process destruction, and history patterns."""

import json

from tests.conftest import assert_asks, run_hook


class TestShellBlock:
    """Block patterns (exit code 2) for dangerous shell operations."""

    # --- Process destruction ---

    def test_block_kill_9_all_processes(self):
        assert_asks('Bash', {'command': 'kill -9 -1'})

    def test_block_kill_KILL_all_processes(self):
        assert_asks('Bash', {'command': 'kill -KILL -1'})

    def test_block_kill_SIGKILL_all_processes(self):
        assert_asks('Bash', {'command': 'kill -SIGKILL -1'})

    def test_block_kill_9_job_group(self):
        assert_asks('Bash', {'command': 'kill -9 %1'})

    def test_block_kill_KILL_job_group(self):
        assert_asks('Bash', {'command': 'kill -KILL %2'})

    def test_block_killall_9(self):
        assert_asks('Bash', {'command': 'killall -9 node'})

    def test_block_pkill_9(self):
        assert_asks('Bash', {'command': 'pkill -9 python'})

    def test_block_nohup_rm(self):
        assert_asks('Bash', {'command': 'nohup rm -rf /tmp/data &'})

    def test_block_nohup_shred(self):
        assert_asks('Bash', {'command': 'nohup shred /dev/sda &'})

    def test_block_nohup_dd(self):
        assert_asks('Bash', {'command': 'nohup dd if=/dev/zero of=/dev/sda &'})

    def test_block_nohup_wipe(self):
        assert_asks('Bash', {'command': 'nohup wipe /tmp/data &'})

    def test_block_nohup_mkfs(self):
        assert_asks('Bash', {'command': 'nohup mkfs.ext4 /dev/sda &'})

    def test_block_xargs_kill(self):
        assert_asks('Bash', {'command': "ps aux | grep node | awk '{print $2}' | xargs kill"})

    # --- Crontab destruction ---

    def test_block_crontab_r(self):
        assert_asks('Bash', {'command': 'crontab -r'})

    # --- History manipulation ---

    def test_block_history_clear(self):
        assert_asks('Bash', {'command': 'history -c'})

    def test_block_history_clear_with_other_flags(self):
        assert_asks('Bash', {'command': 'history -wc'})

    # --- Shell evaluation and code injection ---

    def test_block_eval(self):
        assert_asks('Bash', {'command': 'eval $(echo dangerous)'})

    def test_block_eval_variable(self):
        assert_asks('Bash', {'command': 'eval "$CMD"'})

    def test_block_base64_decode_pipe_bash(self):
        assert_asks('Bash', {'command': 'echo cm0gLXJmIC8= | base64 -d | bash'})

    def test_block_base64_decode_pipe_sh(self):
        assert_asks('Bash', {'command': 'echo payload | base64 --decode | sh'})

    def test_block_base64_decode_pipe_python(self):
        assert_asks('Bash', {'command': 'echo cHJpbnQoJ2hpJyk= | base64 -d | python'})

    def test_block_base64_decode_pipe_zsh(self):
        assert_asks('Bash', {'command': 'cat encoded.txt | base64 --decode | zsh'})

    def test_block_backslash_rm(self):
        assert_asks('Bash', {'command': '\\rm -rf /tmp/data'})

    def test_block_command_rm(self):
        assert_asks('Bash', {'command': 'command rm /tmp/file'})

    def test_block_xargs_shred(self):
        assert_asks('Bash', {'command': "find . -name '*.tmp' | xargs shred"})

    def test_block_xargs_chmod(self):
        assert_asks('Bash', {'command': 'find . | xargs chmod 777'})

    def test_block_xargs_chown(self):
        assert_asks('Bash', {'command': 'find . | xargs chown root:root'})

    def test_block_xargs_dd(self):
        assert_asks('Bash', {'command': 'ls /dev/sd* | xargs dd if=/dev/zero'})

    def test_block_xargs_mkfs(self):
        assert_asks('Bash', {'command': 'echo /dev/sda | xargs mkfs.ext4'})

    def test_block_unset_path(self):
        assert_asks('Bash', {'command': 'unset PATH'})

    def test_block_unset_home(self):
        assert_asks('Bash', {'command': 'unset HOME'})

    def test_block_unset_user(self):
        assert_asks('Bash', {'command': 'unset USER'})

    def test_block_unset_shell(self):
        assert_asks('Bash', {'command': 'unset SHELL'})

    def test_block_export_path_overwrite(self):
        assert_asks('Bash', {'command': 'export PATH=/usr/local/bin'})

    def test_allow_export_path_append(self):
        """Appending to PATH should be allowed."""
        code, _, _ = run_hook("Bash", {"command": "export PATH=$PATH:/usr/local/bin"})
        assert code == 0

    def test_allow_export_path_append_braces(self):
        """Appending to PATH with braces should be allowed."""
        code, _, _ = run_hook("Bash", {"command": "export PATH=${PATH}:/usr/local/bin"})
        assert code == 0

    # --- Python one-liners ---

    def test_block_python_rmtree(self):
        assert_asks('Bash', {'command': 'python -c \'import shutil; shutil.rmtree("/tmp")\''})

    def test_block_python3_os_remove(self):
        assert_asks('Bash', {'command': 'python3 -c \'import os; os.remove("/tmp/f")\''})

    def test_block_python_os_unlink(self):
        assert_asks('Bash', {'command': 'python -c \'import os; os.unlink("/tmp/f")\''})

    def test_block_python_os_system(self):
        assert_asks('Bash', {'command': 'python3 -c \'import os; os.system("rm -rf /")\''})

    def test_block_python_subprocess(self):
        assert_asks('Bash', {'command': 'python -c \'import subprocess; subprocess.run(["rm", "-rf", "/"])\''})

    def test_block_python_exec(self):
        assert_asks('Bash', {'command': 'python3 -c \'exec(open("exploit.py").read())\''})

    def test_block_python_import(self):
        assert_asks('Bash', {'command': 'python -c \'__import__("os").system("id")\''})

    def test_block_python_pathlib_unlink(self):
        assert_asks('Bash', {'command': 'python3 -c \'from pathlib import Path; Path("/tmp/f").unlink()\''})

    # --- printf pipe to shell ---

    def test_block_printf_pipe_bash(self):
        assert_asks('Bash', {'command': "printf 'rm -rf /tmp' | bash"})

    def test_block_printf_pipe_sh(self):
        assert_asks('Bash', {'command': "printf '%s\\n' 'echo pwned' | sh"})

    def test_block_printf_pipe_zsh(self):
        assert_asks('Bash', {'command': "printf 'malicious command' | zsh"})


class TestShellAsk:
    """Ask patterns (exit code 0 with permissionDecision=ask)."""

    # --- Shell evaluation requiring confirmation ---

    def test_ask_source(self):
        code, stdout, _ = run_hook("Bash", {"command": "source venv/bin/activate"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_source_dot(self):
        """source with a dotfile path."""
        code, stdout, _ = run_hook("Bash", {"command": "source ~/.bashrc"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_exec(self):
        code, stdout, _ = run_hook("Bash", {"command": "exec /bin/zsh"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_allow_exec_redirect(self):
        """exec with redirect (e.g. exec >/dev/null) should NOT trigger the ask."""
        code, stdout, _ = run_hook("Bash", {"command": "exec >/dev/null"})
        # Should pass through without ask (exit 0, no JSON)
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

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

    def test_ask_zsh_c(self):
        code, stdout, _ = run_hook("Bash", {"command": "zsh -c 'echo hello'"})
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

    # --- Process management requiring confirmation ---

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

    def test_ask_pkill_pattern(self):
        code, stdout, _ = run_hook("Bash", {"command": "pkill -f 'my_process'"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestShellAllow:
    """Commands that should be allowed (exit code 0, no JSON output)."""

    def test_allow_echo(self):
        code, stdout, _ = run_hook("Bash", {"command": "echo hello world"})
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_allow_ls(self):
        code, stdout, _ = run_hook("Bash", {"command": "ls -la /tmp"})
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_allow_history_show(self):
        """Plain history command (no -c flag) should be allowed."""
        code, stdout, _ = run_hook("Bash", {"command": "history"})
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_allow_kill_single_pid(self):
        """kill with a normal PID (not -9 -1 or job group) should be allowed."""
        code, stdout, _ = run_hook("Bash", {"command": "kill 12345"})
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_allow_python_c_safe(self):
        """Safe python -c without destructive operations should be allowed."""
        code, stdout, _ = run_hook("Bash", {"command": "python3 -c 'print(1 + 2)'"})
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_allow_crontab_l(self):
        """crontab -l (list) should be allowed."""
        code, stdout, _ = run_hook("Bash", {"command": "crontab -l"})
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_allow_base64_encode(self):
        """base64 encoding (not decoding to shell) should be allowed."""
        code, stdout, _ = run_hook("Bash", {"command": "echo hello | base64"})
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout

    def test_allow_unset_custom_var(self):
        """Unsetting a non-critical variable should be allowed."""
        code, stdout, _ = run_hook("Bash", {"command": "unset MY_CUSTOM_VAR"})
        assert code == 0
        assert stdout == "" or "permissionDecision" not in stdout
