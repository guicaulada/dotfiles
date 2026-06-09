"""Tests for Infrastructure as Code security patterns."""

import json

from tests.conftest import assert_asks, run_hook

# =============================================================================
# BLOCK PATTERNS
# =============================================================================


class TestBlockTerraformDestroy:
    """Tests for terraform/tofu/terragrunt destroy (consolidated pattern)."""

    def test_block_terraform_destroy(self):
        assert_asks('Bash', {'command': 'terraform destroy'})

    def test_block_terraform_destroy_with_target(self):
        assert_asks('Bash', {'command': 'terraform destroy -target=aws_instance.web'})

    def test_block_tofu_destroy(self):
        assert_asks('Bash', {'command': 'tofu destroy'})

    def test_block_terragrunt_destroy(self):
        assert_asks('Bash', {'command': 'terragrunt destroy'})


class TestBlockTerragruntRunAllDestroy:
    """Tests for terragrunt run-all destroy."""

    def test_block_terragrunt_run_all_destroy(self):
        assert_asks('Bash', {'command': 'terragrunt run-all destroy'})


class TestBlockPulumiDestroy:
    """Tests for pulumi destroy."""

    def test_block_pulumi_destroy(self):
        assert_asks('Bash', {'command': 'pulumi destroy'})

    def test_block_pulumi_destroy_with_stack(self):
        assert_asks('Bash', {'command': 'pulumi destroy --stack prod'})


class TestBlockServerlessRemove:
    """Tests for serverless/sls remove (consolidated pattern)."""

    def test_block_serverless_remove(self):
        assert_asks('Bash', {'command': 'serverless remove'})

    def test_block_sls_remove(self):
        assert_asks('Bash', {'command': 'sls remove'})

    def test_block_serverless_remove_with_stage(self):
        assert_asks('Bash', {'command': 'serverless remove --stage prod'})

    def test_block_sls_remove_with_stage(self):
        assert_asks('Bash', {'command': 'sls remove --stage dev'})


class TestBlockSamDelete:
    """Tests for sam delete."""

    def test_block_sam_delete(self):
        assert_asks('Bash', {'command': 'sam delete'})

    def test_block_sam_delete_with_flags(self):
        assert_asks('Bash', {'command': 'sam delete --stack-name my-app --no-prompts'})


class TestBlockStateRm:
    """Tests for terraform/tofu state rm (consolidated pattern)."""

    def test_block_terraform_state_rm(self):
        assert_asks('Bash', {'command': 'terraform state rm aws_instance.web'})

    def test_block_tofu_state_rm(self):
        assert_asks('Bash', {'command': 'tofu state rm aws_instance.web'})


class TestBlockForceUnlock:
    """Tests for terraform/tofu force-unlock (consolidated pattern)."""

    def test_block_terraform_force_unlock(self):
        assert_asks('Bash', {'command': 'terraform force-unlock 12345-abcde'})

    def test_block_tofu_force_unlock(self):
        assert_asks('Bash', {'command': 'tofu force-unlock 12345'})


class TestBlockCdkDestroy:
    """Tests for cdk/cdktf destroy (consolidated pattern)."""

    def test_block_cdk_destroy(self):
        assert_asks('Bash', {'command': 'cdk destroy MyStack'})

    def test_block_cdktf_destroy(self):
        assert_asks('Bash', {'command': 'cdktf destroy'})


class TestBlockTerraformWorkspaceDelete:
    """Tests for terraform workspace delete."""

    def test_block_terraform_workspace_delete(self):
        assert_asks('Bash', {'command': 'terraform workspace delete staging'})


class TestBlockPulumiStackRm:
    """Tests for pulumi stack rm."""

    def test_block_pulumi_stack_rm(self):
        assert_asks('Bash', {'command': 'pulumi stack rm dev'})

    def test_block_pulumi_stack_rm_force(self):
        assert_asks('Bash', {'command': 'pulumi stack rm --force prod'})


class TestBlockStatePushReplaceProvider:
    """Tests for terraform/tofu state push/replace-provider."""

    def test_block_terraform_state_push(self):
        code, _, _ = run_hook(
            "Bash", {"command": "terraform state push errored.tfstate"}
        )
        assert code == 2

    def test_block_terraform_state_replace_provider(self):
        assert_asks('Bash', {'command': 'terraform state replace-provider hashicorp/aws registry.acme.corp/acme/aws'})

    def test_block_tofu_state_push(self):
        code, _, _ = run_hook("Bash", {"command": "tofu state push errored.tfstate"})
        assert code == 2

    def test_block_tofu_state_replace_provider(self):
        assert_asks('Bash', {'command': 'tofu state replace-provider hashicorp/aws registry.acme.corp/acme/aws'})


# =============================================================================
# ASK PATTERNS
# =============================================================================


class TestAskTerraformApply:
    """Tests for terraform/tofu apply (consolidated pattern)."""

    def test_ask_terraform_apply(self):
        code, stdout, _ = run_hook("Bash", {"command": "terraform apply"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_terraform_apply_with_plan(self):
        code, stdout, _ = run_hook("Bash", {"command": "terraform apply tfplan"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_tofu_apply(self):
        code, stdout, _ = run_hook("Bash", {"command": "tofu apply"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAskTerraformStateModify:
    """Tests for terraform/tofu import and state mv (consolidated pattern)."""

    def test_ask_terraform_import(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "terraform import aws_instance.web i-12345"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_terraform_state_mv(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "terraform state mv aws_instance.old aws_instance.new"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_tofu_import(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "tofu import aws_instance.web i-12345"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_tofu_state_mv(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "tofu state mv aws_instance.old aws_instance.new"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAskPulumiUp:
    """Tests for pulumi up."""

    def test_ask_pulumi_up(self):
        code, stdout, _ = run_hook("Bash", {"command": "pulumi up"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_pulumi_up_with_stack(self):
        code, stdout, _ = run_hook("Bash", {"command": "pulumi up --stack dev"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAskTerraformWorkspace:
    """Tests for terraform workspace new/select."""

    def test_ask_terraform_workspace_new(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "terraform workspace new staging"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_terraform_workspace_select(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "terraform workspace select prod"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAskPulumiStack:
    """Tests for pulumi stack init/select."""

    def test_ask_pulumi_stack_init(self):
        code, stdout, _ = run_hook("Bash", {"command": "pulumi stack init dev"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_pulumi_stack_select(self):
        code, stdout, _ = run_hook("Bash", {"command": "pulumi stack select prod"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAskCdkDeploy:
    """Tests for cdk/cdktf deploy (consolidated pattern)."""

    def test_ask_cdk_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "cdk deploy MyStack"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_cdktf_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "cdktf deploy"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAskTerraformRefresh:
    """Tests for terraform/tofu refresh (consolidated pattern)."""

    def test_ask_terraform_refresh(self):
        code, stdout, _ = run_hook("Bash", {"command": "terraform refresh"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_tofu_refresh(self):
        code, stdout, _ = run_hook("Bash", {"command": "tofu refresh"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAskPulumiRefresh:
    """Tests for pulumi refresh."""

    def test_ask_pulumi_refresh(self):
        code, stdout, _ = run_hook("Bash", {"command": "pulumi refresh"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_pulumi_refresh_with_stack(self):
        code, stdout, _ = run_hook("Bash", {"command": "pulumi refresh --stack prod"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
