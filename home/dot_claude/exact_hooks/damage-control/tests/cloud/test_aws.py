"""Tests for AWS CLI security patterns."""

import json

from tests.conftest import assert_asks, run_hook


class TestAwsBlock:
    """Tests for AWS CLI operations that should be blocked."""

    # --- Credential exposure ---

    def test_block_aws_configure_get(self):
        assert_asks('Bash', {'command': 'aws configure get aws_secret_access_key'})

    def test_block_aws_configure_export_credentials(self):
        assert_asks('Bash', {'command': 'aws configure export-credentials --profile default'})

    def test_block_aws_sts_get_session_token(self):
        assert_asks('Bash', {'command': 'aws sts get-session-token --duration-seconds 3600'})

    def test_block_aws_sts_get_access_key_info(self):
        assert_asks('Bash', {'command': 'aws sts get-access-key-info --access-key-id AKIA123'})

    # --- Specific S3 patterns (not caught by catch-all) ---

    def test_block_aws_s3_rm_recursive(self):
        assert_asks('Bash', {'command': 'aws s3 rm s3://my-bucket --recursive'})

    def test_block_aws_s3_rm_recursive_short_flag(self):
        assert_asks('Bash', {'command': 'aws s3 rm s3://my-bucket/prefix/ -r'})

    def test_block_aws_s3_rb_force(self):
        assert_asks('Bash', {'command': 'aws s3 rb s3://my-bucket --force'})

    def test_block_aws_s3_sync_delete(self):
        assert_asks('Bash', {'command': 'aws s3 sync . s3://bucket --delete'})

    # --- IAM detach (must block, ask catch-all would only ask) ---

    def test_block_aws_iam_detach_role_policy(self):
        assert_asks('Bash', {'command': 'aws iam detach-role-policy --role-name myrole --policy-arn arn:aws:iam::policy/test'})

    def test_block_aws_iam_detach_group_policy(self):
        assert_asks('Bash', {'command': 'aws iam detach-group-policy --group-name admins --policy-arn arn:aws:iam::policy/test'})

    def test_block_aws_iam_detach_user_policy(self):
        assert_asks('Bash', {'command': 'aws iam detach-user-policy --user-name bob --policy-arn arn:aws:iam::policy/test'})

    # --- CloudTrail stop-logging (must block, ask catch-all would only ask) ---

    def test_block_aws_cloudtrail_stop_logging(self):
        assert_asks('Bash', {'command': 'aws cloudtrail stop-logging --name my-trail'})

    # --- WAF delete (different command structure) ---

    def test_block_aws_waf_delete(self):
        assert_asks('Bash', {'command': 'aws waf delete-rule --rule-id abc123'})

    def test_block_aws_wafv2_delete(self):
        assert_asks('Bash', {'command': 'aws wafv2 delete-web-acl --name myacl'})

    # --- Block catch-all: "aws <service> delete-/terminate-/remove-/purge-/deregister-" ---

    def test_block_aws_ec2_terminate_instances(self):
        assert_asks('Bash', {'command': 'aws ec2 terminate-instances --instance-ids i-123'})

    def test_block_aws_rds_delete_db_instance(self):
        assert_asks('Bash', {'command': 'aws rds delete-db-instance --db-instance-id mydb'})

    def test_block_aws_cloudformation_delete_stack(self):
        assert_asks('Bash', {'command': 'aws cloudformation delete-stack --stack-name mystack'})

    def test_block_aws_dynamodb_delete_table(self):
        assert_asks('Bash', {'command': 'aws dynamodb delete-table --table-name mytable'})

    def test_block_aws_eks_delete_cluster(self):
        assert_asks('Bash', {'command': 'aws eks delete-cluster --name mycluster'})

    def test_block_aws_lambda_delete_function(self):
        assert_asks('Bash', {'command': 'aws lambda delete-function --function-name myfunc'})

    def test_block_aws_iam_delete_role(self):
        assert_asks('Bash', {'command': 'aws iam delete-role --role-name myrole'})

    def test_block_aws_iam_delete_user(self):
        assert_asks('Bash', {'command': 'aws iam delete-user --user-name bob'})

    def test_block_aws_iam_delete_access_key(self):
        assert_asks('Bash', {'command': 'aws iam delete-access-key --user-name bob --access-key-id AKIA123'})

    def test_block_aws_iam_delete_policy(self):
        assert_asks('Bash', {'command': 'aws iam delete-policy --policy-arn arn:aws:iam::policy/test'})

    def test_block_aws_iam_delete_group(self):
        assert_asks('Bash', {'command': 'aws iam delete-group --group-name admins'})

    def test_block_aws_elasticache_delete_cache_cluster(self):
        assert_asks('Bash', {'command': 'aws elasticache delete-cache-cluster --cache-cluster-id myredis'})

    def test_block_aws_elbv2_delete_load_balancer(self):
        assert_asks('Bash', {'command': 'aws elbv2 delete-load-balancer --load-balancer-arn arn:123'})

    def test_block_aws_elb_delete_load_balancer(self):
        assert_asks('Bash', {'command': 'aws elb delete-load-balancer --load-balancer-name myelb'})

    def test_block_aws_secretsmanager_delete_secret(self):
        assert_asks('Bash', {'command': 'aws secretsmanager delete-secret --secret-id mysecret'})

    def test_block_aws_ssm_delete_parameter(self):
        assert_asks('Bash', {'command': 'aws ssm delete-parameter --name /app/config'})

    def test_block_aws_cognito_delete_user_pool(self):
        assert_asks('Bash', {'command': 'aws cognito-idp delete-user-pool --user-pool-id us-east-1_abc'})

    def test_block_aws_apigateway_delete_rest_api(self):
        assert_asks('Bash', {'command': 'aws apigateway delete-rest-api --rest-api-id abc123'})

    def test_block_aws_sagemaker_delete_endpoint(self):
        assert_asks('Bash', {'command': 'aws sagemaker delete-endpoint --endpoint-name myep'})

    def test_block_aws_glue_delete_job(self):
        assert_asks('Bash', {'command': 'aws glue delete-job --job-name myjob'})

    def test_block_aws_kinesis_delete_stream(self):
        assert_asks('Bash', {'command': 'aws kinesis delete-stream --stream-name mystream'})

    def test_block_aws_states_delete_state_machine(self):
        assert_asks('Bash', {'command': 'aws states delete-state-machine --state-machine-arn arn:123'})

    def test_block_aws_ecs_delete_service(self):
        assert_asks('Bash', {'command': 'aws ecs delete-service --cluster mycluster --service myservice'})

    def test_block_aws_ecs_delete_cluster(self):
        assert_asks('Bash', {'command': 'aws ecs delete-cluster --cluster mycluster'})

    def test_block_aws_amplify_delete_app(self):
        assert_asks('Bash', {'command': 'aws amplify delete-app --app-id abc123'})

    def test_block_aws_opensearch_delete_domain(self):
        assert_asks('Bash', {'command': 'aws opensearch delete-domain --domain-name mydomain'})

    def test_block_aws_acm_delete_certificate(self):
        assert_asks('Bash', {'command': 'aws acm delete-certificate --certificate-arn arn:123'})

    def test_block_aws_codecommit_delete_repository(self):
        assert_asks('Bash', {'command': 'aws codecommit delete-repository --repository-name myrepo'})

    def test_block_aws_codepipeline_delete_pipeline(self):
        assert_asks('Bash', {'command': 'aws codepipeline delete-pipeline --name mypipeline'})

    def test_block_aws_cloudwatch_delete_alarms(self):
        assert_asks('Bash', {'command': 'aws cloudwatch delete-alarms --alarm-names myalarm'})

    def test_block_aws_cloudtrail_delete_trail(self):
        assert_asks('Bash', {'command': 'aws cloudtrail delete-trail --name my-trail'})

    def test_block_aws_backup_delete_backup_vault(self):
        assert_asks('Bash', {'command': 'aws backup delete-backup-vault --backup-vault-name myvault'})

    def test_block_aws_redshift_delete_cluster(self):
        assert_asks('Bash', {'command': 'aws redshift delete-cluster --cluster-identifier mycluster'})

    def test_block_aws_emr_terminate_job_flows(self):
        assert_asks('Bash', {'command': 'aws emr terminate-job-flows --job-flow-ids j-123'})

    def test_block_aws_logs_delete_log_group(self):
        assert_asks('Bash', {'command': 'aws logs delete-log-group --log-group-name /aws/lambda/test'})

    def test_block_aws_ecr_delete_repository(self):
        assert_asks('Bash', {'command': 'aws ecr delete-repository --repository-name myrepo'})

    def test_block_aws_sns_delete_topic(self):
        assert_asks('Bash', {'command': 'aws sns delete-topic --topic-arn arn:aws:sns:us-east-1:123:test'})

    def test_block_aws_sqs_delete_queue(self):
        assert_asks('Bash', {'command': 'aws sqs delete-queue --queue-url https://sqs.us-east-1.amazonaws.com/123/test'})

    def test_block_aws_catch_all_deregister(self):
        """Verify the catch-all covers deregister- operations."""
        assert_asks('Bash', {'command': 'aws ecs deregister-task-definition --task-definition mytask:1'})

    def test_block_aws_catch_all_purge(self):
        """Verify the catch-all covers purge- operations."""
        assert_asks('Bash', {'command': 'aws sqs purge-queue --queue-url https://sqs.us-east-1.amazonaws.com/123/test'})


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


class TestAwsSessionCredentialAsk:
    def test_ask_ssm_start_session(self):
        assert_asks("Bash", {"command": "aws ssm start-session --target i-0abc"})

    def test_ask_configure_set(self):
        assert_asks("Bash", {"command": "aws configure set region us-east-1"})
