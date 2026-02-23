"""Tests for CI/CD, deployment, and VCS non-git patterns."""

import json

from tests.conftest import run_hook

# =============================================================================
# BLOCK PATTERNS
# =============================================================================


class TestBlockGlabProjectDelete:
    """Tests for glab project delete."""

    def test_block_glab_project_delete(self):
        code, _, _ = run_hook("Bash", {"command": "glab project delete my-project"})
        assert code == 2

    def test_block_glab_project_delete_with_flags(self):
        code, _, _ = run_hook(
            "Bash", {"command": "glab project delete my-group/my-project --yes"}
        )
        assert code == 2


class TestBlockCircleci:
    """Tests for CircleCI context destructive operations."""

    def test_block_circleci_context_delete(self):
        code, _, _ = run_hook("Bash", {"command": "circleci context delete my-context"})
        assert code == 2

    def test_block_circleci_context_remove_secret(self):
        code, _, _ = run_hook(
            "Bash", {"command": "circleci context remove-secret my-context MY_KEY"}
        )
        assert code == 2

    def test_block_circleci_context_store_secret(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "circleci context store-secret my-context MY_KEY"},
        )
        assert code == 2


class TestBlockHg:
    """Tests for Mercurial destructive operations."""

    def test_block_hg_strip(self):
        code, _, _ = run_hook("Bash", {"command": "hg strip 1234"})
        assert code == 2

    def test_block_hg_purge(self):
        code, _, _ = run_hook("Bash", {"command": "hg purge"})
        assert code == 2

    def test_block_hg_rollback(self):
        code, _, _ = run_hook("Bash", {"command": "hg rollback"})
        assert code == 2


class TestBlockSstRemove:
    """Tests for sst remove."""

    def test_block_sst_remove(self):
        code, _, _ = run_hook("Bash", {"command": "sst remove"})
        assert code == 2

    def test_block_sst_remove_with_stage(self):
        code, _, _ = run_hook("Bash", {"command": "sst remove --stage prod"})
        assert code == 2


# =============================================================================
# ASK PATTERNS
# =============================================================================


class TestAskAnsible:
    """Tests for Ansible operations."""

    def test_ask_ansible_playbook(self):
        code, stdout, _ = run_hook("Bash", {"command": "ansible-playbook deploy.yml"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_ansible_playbook_with_inventory(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "ansible-playbook -i hosts.ini site.yml"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_ansible_adhoc_module(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "ansible all -m shell -a 'uptime'"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_ansible_adhoc_module_name(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "ansible webservers --module-name ping"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAskAct:
    """Tests for act (local GitHub Actions runner)."""

    def test_ask_act_push(self):
        code, stdout, _ = run_hook("Bash", {"command": "act push"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_act_pull_request(self):
        code, stdout, _ = run_hook("Bash", {"command": "act pull_request"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAskGlabMr:
    """Tests for GitLab merge request actions."""

    def test_ask_glab_mr_merge(self):
        code, stdout, _ = run_hook("Bash", {"command": "glab mr merge 42"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_glab_mr_close(self):
        code, stdout, _ = run_hook("Bash", {"command": "glab mr close 42"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_glab_mr_create(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "glab mr create --title 'Fix bug'"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAskGlabIssue:
    """Tests for GitLab issue actions."""

    def test_ask_glab_issue_create(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "glab issue create --title 'New issue'"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_glab_issue_close(self):
        code, stdout, _ = run_hook("Bash", {"command": "glab issue close 99"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAskGlabPipeline:
    """Tests for GitLab pipeline actions."""

    def test_ask_glab_pipeline_cancel(self):
        code, stdout, _ = run_hook("Bash", {"command": "glab pipeline cancel 123"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_glab_pipeline_delete(self):
        code, stdout, _ = run_hook("Bash", {"command": "glab pipeline delete 123"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_glab_pipeline_retry(self):
        code, stdout, _ = run_hook("Bash", {"command": "glab pipeline retry 123"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAskServerlessDeploy:
    """Tests for serverless/sls deploy (consolidated pattern)."""

    def test_ask_serverless_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "serverless deploy"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_sls_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "sls deploy"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_serverless_deploy_with_stage(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "serverless deploy --stage prod"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAskSstDeploy:
    """Tests for sst deploy."""

    def test_ask_sst_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "sst deploy"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_sst_deploy_with_stage(self):
        code, stdout, _ = run_hook("Bash", {"command": "sst deploy --stage prod"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAskSvn:
    """Tests for SVN destructive operations."""

    def test_ask_svn_delete(self):
        code, stdout, _ = run_hook("Bash", {"command": "svn delete file.txt"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_svn_revert(self):
        code, stdout, _ = run_hook("Bash", {"command": "svn revert -R ."})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
