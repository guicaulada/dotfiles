"""Tests for Infrastructure as Code security patterns."""

import json

from tests.conftest import run_hook


class TestIacBlock:
    def test_block_terraform_destroy(self):
        code, _, _ = run_hook("Bash", {"command": "terraform destroy"})
        assert code == 2

    def test_block_terraform_state_rm(self):
        code, _, _ = run_hook(
            "Bash", {"command": "terraform state rm aws_instance.web"}
        )
        assert code == 2

    def test_block_terraform_force_unlock(self):
        code, _, _ = run_hook("Bash", {"command": "terraform force-unlock 12345-abcde"})
        assert code == 2

    def test_block_cdk_destroy(self):
        code, _, _ = run_hook("Bash", {"command": "cdk destroy MyStack"})
        assert code == 2

    def test_block_cdktf_destroy(self):
        code, _, _ = run_hook("Bash", {"command": "cdktf destroy"})
        assert code == 2

    def test_block_tofu_destroy(self):
        code, _, _ = run_hook("Bash", {"command": "tofu destroy"})
        assert code == 2

    def test_block_tofu_state_rm(self):
        code, _, _ = run_hook("Bash", {"command": "tofu state rm aws_instance.web"})
        assert code == 2

    def test_block_tofu_force_unlock(self):
        code, _, _ = run_hook("Bash", {"command": "tofu force-unlock 12345"})
        assert code == 2


class TestIacAsk:
    def test_ask_terraform_apply(self):
        code, stdout, _ = run_hook("Bash", {"command": "terraform apply"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_terraform_import(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "terraform import aws_instance.web i-12345"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_terraform_state_mv(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "terraform state mv aws_instance.old aws_instance.new"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_pulumi_up(self):
        code, stdout, _ = run_hook("Bash", {"command": "pulumi up"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_tofu_apply(self):
        code, stdout, _ = run_hook("Bash", {"command": "tofu apply"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
