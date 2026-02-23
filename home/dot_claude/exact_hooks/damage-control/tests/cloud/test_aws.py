"""Tests for AWS CLI security patterns."""

import json

from tests.conftest import run_hook


class TestAwsBlock:
    def test_block_aws_terminate(self):
        code, _, _ = run_hook(
            "Bash", {"command": "aws ec2 terminate-instances --instance-ids i-123"}
        )
        assert code == 2

    def test_block_aws_s3_sync_delete(self):
        code, _, _ = run_hook("Bash", {"command": "aws s3 sync . s3://bucket --delete"})
        assert code == 2

    def test_block_aws_iam_delete_policy(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws iam delete-policy --policy-arn arn:aws:iam::policy/test"},
        )
        assert code == 2

    def test_block_aws_iam_delete_group(self):
        code, _, _ = run_hook(
            "Bash", {"command": "aws iam delete-group --group-name admins"}
        )
        assert code == 2

    def test_block_aws_iam_detach_role_policy(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "aws iam detach-role-policy --role-name myrole --policy-arn arn:aws:iam::policy/test"
            },
        )
        assert code == 2

    def test_block_aws_logs_delete_log_group(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws logs delete-log-group --log-group-name /aws/lambda/test"},
        )
        assert code == 2

    def test_block_aws_ecr_delete_repository(self):
        code, _, _ = run_hook(
            "Bash", {"command": "aws ecr delete-repository --repository-name myrepo"}
        )
        assert code == 2

    def test_block_aws_sns_delete_topic(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "aws sns delete-topic --topic-arn arn:aws:sns:us-east-1:123:test"
            },
        )
        assert code == 2

    def test_block_aws_sqs_delete_queue(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "aws sqs delete-queue --queue-url https://sqs.us-east-1.amazonaws.com/123/test"
            },
        )
        assert code == 2


class TestAwsAsk:
    def test_ask_aws_route53_change(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "aws route53 change-resource-record-sets --hosted-zone-id Z123"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
