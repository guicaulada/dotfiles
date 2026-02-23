"""Tests for AWS CLI security patterns."""

import json

from tests.conftest import run_hook


class TestAwsBlock:
    """Tests for AWS CLI operations that should be blocked."""

    # --- Specific S3 patterns (not caught by catch-all) ---

    def test_block_aws_s3_rm_recursive(self):
        code, _, _ = run_hook(
            "Bash", {"command": "aws s3 rm s3://my-bucket --recursive"}
        )
        assert code == 2

    def test_block_aws_s3_rm_recursive_short_flag(self):
        code, _, _ = run_hook(
            "Bash", {"command": "aws s3 rm s3://my-bucket/prefix/ -r"}
        )
        assert code == 2

    def test_block_aws_s3_rb_force(self):
        code, _, _ = run_hook("Bash", {"command": "aws s3 rb s3://my-bucket --force"})
        assert code == 2

    def test_block_aws_s3_sync_delete(self):
        code, _, _ = run_hook("Bash", {"command": "aws s3 sync . s3://bucket --delete"})
        assert code == 2

    # --- IAM detach (must block, ask catch-all would only ask) ---

    def test_block_aws_iam_detach_role_policy(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "aws iam detach-role-policy --role-name myrole --policy-arn arn:aws:iam::policy/test"
            },
        )
        assert code == 2

    def test_block_aws_iam_detach_group_policy(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "aws iam detach-group-policy --group-name admins --policy-arn arn:aws:iam::policy/test"
            },
        )
        assert code == 2

    def test_block_aws_iam_detach_user_policy(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "aws iam detach-user-policy --user-name bob --policy-arn arn:aws:iam::policy/test"
            },
        )
        assert code == 2

    # --- CloudTrail stop-logging (must block, ask catch-all would only ask) ---

    def test_block_aws_cloudtrail_stop_logging(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws cloudtrail stop-logging --name my-trail"},
        )
        assert code == 2

    # --- WAF delete (different command structure) ---

    def test_block_aws_waf_delete(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws waf delete-rule --rule-id abc123"},
        )
        assert code == 2

    def test_block_aws_wafv2_delete(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws wafv2 delete-web-acl --name myacl"},
        )
        assert code == 2

    # --- Block catch-all: "aws <service> delete-/terminate-/remove-/purge-/deregister-" ---

    def test_block_aws_ec2_terminate_instances(self):
        code, _, _ = run_hook(
            "Bash", {"command": "aws ec2 terminate-instances --instance-ids i-123"}
        )
        assert code == 2

    def test_block_aws_rds_delete_db_instance(self):
        code, _, _ = run_hook(
            "Bash", {"command": "aws rds delete-db-instance --db-instance-id mydb"}
        )
        assert code == 2

    def test_block_aws_cloudformation_delete_stack(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws cloudformation delete-stack --stack-name mystack"},
        )
        assert code == 2

    def test_block_aws_dynamodb_delete_table(self):
        code, _, _ = run_hook(
            "Bash", {"command": "aws dynamodb delete-table --table-name mytable"}
        )
        assert code == 2

    def test_block_aws_eks_delete_cluster(self):
        code, _, _ = run_hook(
            "Bash", {"command": "aws eks delete-cluster --name mycluster"}
        )
        assert code == 2

    def test_block_aws_lambda_delete_function(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws lambda delete-function --function-name myfunc"},
        )
        assert code == 2

    def test_block_aws_iam_delete_role(self):
        code, _, _ = run_hook(
            "Bash", {"command": "aws iam delete-role --role-name myrole"}
        )
        assert code == 2

    def test_block_aws_iam_delete_user(self):
        code, _, _ = run_hook(
            "Bash", {"command": "aws iam delete-user --user-name bob"}
        )
        assert code == 2

    def test_block_aws_iam_delete_access_key(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "aws iam delete-access-key --user-name bob --access-key-id AKIA123"
            },
        )
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

    def test_block_aws_elasticache_delete_cache_cluster(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "aws elasticache delete-cache-cluster --cache-cluster-id myredis"
            },
        )
        assert code == 2

    def test_block_aws_elbv2_delete_load_balancer(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws elbv2 delete-load-balancer --load-balancer-arn arn:123"},
        )
        assert code == 2

    def test_block_aws_elb_delete_load_balancer(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws elb delete-load-balancer --load-balancer-name myelb"},
        )
        assert code == 2

    def test_block_aws_secretsmanager_delete_secret(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws secretsmanager delete-secret --secret-id mysecret"},
        )
        assert code == 2

    def test_block_aws_ssm_delete_parameter(self):
        code, _, _ = run_hook(
            "Bash", {"command": "aws ssm delete-parameter --name /app/config"}
        )
        assert code == 2

    def test_block_aws_cognito_delete_user_pool(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "aws cognito-idp delete-user-pool --user-pool-id us-east-1_abc"
            },
        )
        assert code == 2

    def test_block_aws_apigateway_delete_rest_api(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws apigateway delete-rest-api --rest-api-id abc123"},
        )
        assert code == 2

    def test_block_aws_sagemaker_delete_endpoint(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws sagemaker delete-endpoint --endpoint-name myep"},
        )
        assert code == 2

    def test_block_aws_glue_delete_job(self):
        code, _, _ = run_hook(
            "Bash", {"command": "aws glue delete-job --job-name myjob"}
        )
        assert code == 2

    def test_block_aws_kinesis_delete_stream(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws kinesis delete-stream --stream-name mystream"},
        )
        assert code == 2

    def test_block_aws_states_delete_state_machine(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws states delete-state-machine --state-machine-arn arn:123"},
        )
        assert code == 2

    def test_block_aws_ecs_delete_service(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "aws ecs delete-service --cluster mycluster --service myservice"
            },
        )
        assert code == 2

    def test_block_aws_ecs_delete_cluster(self):
        code, _, _ = run_hook(
            "Bash", {"command": "aws ecs delete-cluster --cluster mycluster"}
        )
        assert code == 2

    def test_block_aws_amplify_delete_app(self):
        code, _, _ = run_hook(
            "Bash", {"command": "aws amplify delete-app --app-id abc123"}
        )
        assert code == 2

    def test_block_aws_opensearch_delete_domain(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws opensearch delete-domain --domain-name mydomain"},
        )
        assert code == 2

    def test_block_aws_acm_delete_certificate(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws acm delete-certificate --certificate-arn arn:123"},
        )
        assert code == 2

    def test_block_aws_codecommit_delete_repository(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws codecommit delete-repository --repository-name myrepo"},
        )
        assert code == 2

    def test_block_aws_codepipeline_delete_pipeline(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws codepipeline delete-pipeline --name mypipeline"},
        )
        assert code == 2

    def test_block_aws_cloudwatch_delete_alarms(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws cloudwatch delete-alarms --alarm-names myalarm"},
        )
        assert code == 2

    def test_block_aws_cloudtrail_delete_trail(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws cloudtrail delete-trail --name my-trail"},
        )
        assert code == 2

    def test_block_aws_backup_delete_backup_vault(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws backup delete-backup-vault --backup-vault-name myvault"},
        )
        assert code == 2

    def test_block_aws_redshift_delete_cluster(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws redshift delete-cluster --cluster-identifier mycluster"},
        )
        assert code == 2

    def test_block_aws_emr_terminate_job_flows(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "aws emr terminate-job-flows --job-flow-ids j-123"},
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

    def test_block_aws_catch_all_deregister(self):
        """Verify the catch-all covers deregister- operations."""
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "aws ecs deregister-task-definition --task-definition mytask:1"
            },
        )
        assert code == 2

    def test_block_aws_catch_all_purge(self):
        """Verify the catch-all covers purge- operations."""
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "aws sqs purge-queue --queue-url https://sqs.us-east-1.amazonaws.com/123/test"
            },
        )
        assert code == 2


class TestAwsAsk:
    """Tests for AWS CLI operations that should prompt for confirmation."""

    # --- Specific ask patterns ---

    def test_ask_aws_route53_delete_hosted_zone(self):
        """Route53 delete should ask, not block."""
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "aws route53 delete-hosted-zone --id Z123"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_aws_route53_change_resource_record_sets(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "aws route53 change-resource-record-sets --hosted-zone-id Z123"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- Ask catch-all: create-/update-/put-/start-/stop-/... ---

    def test_ask_aws_ec2_stop_instances(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "aws ec2 stop-instances --instance-ids i-123"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_aws_ec2_reboot_instances(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "aws ec2 reboot-instances --instance-ids i-123"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_aws_ec2_start_instances(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "aws ec2 start-instances --instance-ids i-123"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_aws_ssm_put_parameter(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "aws ssm put-parameter --name /app/key --value secret"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_aws_secretsmanager_create_secret(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "aws secretsmanager create-secret --name mysecret"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_aws_secretsmanager_update_secret(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "aws secretsmanager update-secret --secret-id mysecret"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_aws_deploy_create_deployment(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "aws deploy create-deployment --application-name myapp"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_aws_ecs_update_service(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "aws ecs update-service --cluster mycluster --service myservice"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_aws_lambda_invoke(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "aws lambda invoke --function-name myfunc output.json"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_aws_ec2_run_instances(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "aws ec2 run-instances --image-id ami-123"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_aws_sns_publish(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "aws sns publish --topic-arn arn:123 --message hello"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_aws_ec2_create_tags(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "aws ec2 create-tags --resources i-123 --tags Key=Name,Value=test"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_aws_iam_attach_role_policy(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "aws iam attach-role-policy --role-name myrole --policy-arn arn:123"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestAwsAllow:
    """Tests for AWS CLI read-only operations that should be allowed."""

    def test_allow_aws_s3_ls(self):
        code, _, _ = run_hook("Bash", {"command": "aws s3 ls s3://my-bucket"})
        assert code == 0

    def test_allow_aws_ec2_describe_instances(self):
        code, _, _ = run_hook("Bash", {"command": "aws ec2 describe-instances"})
        assert code == 0

    def test_allow_aws_sts_get_caller_identity(self):
        code, _, _ = run_hook("Bash", {"command": "aws sts get-caller-identity"})
        assert code == 0

    def test_allow_aws_iam_list_roles(self):
        code, _, _ = run_hook("Bash", {"command": "aws iam list-roles"})
        assert code == 0

    def test_allow_aws_s3_cp_download(self):
        code, _, _ = run_hook(
            "Bash", {"command": "aws s3 cp s3://bucket/file.txt ./local/"}
        )
        assert code == 0

    def test_allow_aws_logs_describe_log_groups(self):
        code, _, _ = run_hook("Bash", {"command": "aws logs describe-log-groups"})
        assert code == 0
