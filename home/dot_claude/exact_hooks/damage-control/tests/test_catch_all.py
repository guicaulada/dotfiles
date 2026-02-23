"""Tests for privilege escalation (sudo, su, doas, pkexec, etc.) catch-all patterns."""

import json

from tests.conftest import run_hook


class TestSudoCatchAll:
    """Generic sudo commands that are not caught by more specific patterns."""

    def test_ask_sudo_ls(self):
        code, stdout, _ = run_hook("Bash", {"command": "sudo ls /root"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_sudo_cat(self):
        code, stdout, _ = run_hook("Bash", {"command": "sudo cat /etc/shadow"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_sudo_systemctl_status(self):
        """systemctl status is not caught by system.yaml (only stop/disable/mask)."""
        code, stdout, _ = run_hook("Bash", {"command": "sudo systemctl status nginx"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_sudo_env(self):
        code, stdout, _ = run_hook("Bash", {"command": "sudo -E env"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_sudo_user_flag(self):
        code, stdout, _ = run_hook("Bash", {"command": "sudo -u postgres psql"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestSuCatchAll:
    """su command privilege escalation."""

    def test_ask_su_root(self):
        code, stdout, _ = run_hook("Bash", {"command": "su - root"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_su_user(self):
        code, stdout, _ = run_hook("Bash", {"command": "su postgres"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_su_command(self):
        code, stdout, _ = run_hook("Bash", {"command": "su -c 'whoami' root"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestDoasCatchAll:
    """doas (OpenBSD/FreeBSD sudo alternative) privilege escalation."""

    def test_ask_doas_ls(self):
        code, stdout, _ = run_hook("Bash", {"command": "doas ls /root"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_doas_u_flag(self):
        code, stdout, _ = run_hook("Bash", {"command": "doas -u root whoami"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestPkexecCatchAll:
    """pkexec (PolicyKit) privilege escalation."""

    def test_ask_pkexec_command(self):
        code, stdout, _ = run_hook("Bash", {"command": "pkexec visudo"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_pkexec_env(self):
        code, stdout, _ = run_hook("Bash", {"command": "pkexec --user root /bin/bash"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestRunuserCatchAll:
    """runuser privilege escalation."""

    def test_ask_runuser(self):
        code, stdout, _ = run_hook("Bash", {"command": "runuser -u postgres -- psql"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_runuser_login(self):
        code, stdout, _ = run_hook("Bash", {"command": "runuser -l root -c 'whoami'"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestDzdoCatchAll:
    """dzdo (Centrify) privilege escalation."""

    def test_ask_dzdo_command(self):
        code, stdout, _ = run_hook("Bash", {"command": "dzdo systemctl restart nginx"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestPfexecCatchAll:
    """pfexec (Solaris/illumos) privilege escalation."""

    def test_ask_pfexec_command(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "pfexec /usr/sbin/svcadm restart sshd"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestCatchAllNegative:
    """Commands that should NOT be caught by catch-all patterns."""

    def test_allow_plain_ls(self):
        code, stdout, _ = run_hook("Bash", {"command": "ls /tmp"})
        assert code == 0
        assert stdout == ""

    def test_allow_echo(self):
        code, stdout, _ = run_hook("Bash", {"command": "echo hello"})
        assert code == 0
        assert stdout == ""

    def test_no_false_positive_sudo_in_word(self):
        """Words containing 'sudo' (like 'pseudocode') should not trigger."""
        code, stdout, _ = run_hook("Bash", {"command": "echo pseudocode"})
        assert code == 0
        assert stdout == ""

    def test_no_false_positive_su_in_word(self):
        """Words containing 'su' (like 'super', 'result') should not trigger."""
        code, stdout, _ = run_hook("Bash", {"command": "echo superuser"})
        assert code == 0
        assert stdout == ""
