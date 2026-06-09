"""Tests for GCP (gcloud) security patterns."""

import json

from tests.conftest import assert_asks, run_hook


class TestGcpBlock:
    """Tests for GCP CLI operations that should be blocked."""

    # --- Credential exposure ---

    def test_block_gcloud_auth_print_access_token(self):
        assert_asks('Bash', {'command': 'gcloud auth print-access-token'})

    def test_block_gcloud_auth_print_identity_token(self):
        assert_asks('Bash', {'command': 'gcloud auth print-identity-token'})

    def test_block_gcloud_auth_adc_print_access_token(self):
        assert_asks('Bash', {'command': 'gcloud auth application-default print-access-token'})

    # --- Specific block patterns (not caught by catch-all) ---

    def test_block_gcloud_storage_rm_recursive(self):
        assert_asks('Bash', {'command': 'gcloud storage rm -r gs://my-bucket/path/'})

    def test_block_gcloud_secrets_versions_disable(self):
        assert_asks('Bash', {'command': 'gcloud secrets versions disable 3 --secret=mysecret'})

    def test_block_gcloud_dataflow_jobs_cancel(self):
        assert_asks('Bash', {'command': 'gcloud dataflow jobs cancel job-123'})

    def test_block_gcloud_dataflow_jobs_drain(self):
        assert_asks('Bash', {'command': 'gcloud dataflow jobs drain job-123'})

    # --- Block catch-all: "gcloud ... delete" or "gcloud ... destroy" ---

    def test_block_gcloud_projects_delete(self):
        assert_asks('Bash', {'command': 'gcloud projects delete my-project'})

    def test_block_gcloud_compute_instances_delete(self):
        assert_asks('Bash', {'command': 'gcloud compute instances delete myvm --zone=us-central1-a'})

    def test_block_gcloud_sql_instances_delete(self):
        assert_asks('Bash', {'command': 'gcloud sql instances delete mydb'})

    def test_block_gcloud_container_clusters_delete(self):
        assert_asks('Bash', {'command': 'gcloud container clusters delete mycluster'})

    def test_block_gcloud_functions_delete(self):
        assert_asks('Bash', {'command': 'gcloud functions delete myfunction'})

    def test_block_gcloud_iam_service_accounts_delete(self):
        assert_asks('Bash', {'command': 'gcloud iam service-accounts delete sa@project.iam.gserviceaccount.com'})

    def test_block_gcloud_run_services_delete(self):
        assert_asks('Bash', {'command': 'gcloud run services delete myservice'})

    def test_block_gcloud_spanner_instances_delete(self):
        assert_asks('Bash', {'command': 'gcloud spanner instances delete myinstance'})

    def test_block_gcloud_spanner_databases_delete(self):
        assert_asks('Bash', {'command': 'gcloud spanner databases delete mydb --instance=myinstance'})

    def test_block_gcloud_bigtable_instances_delete(self):
        assert_asks('Bash', {'command': 'gcloud bigtable instances delete mybt'})

    def test_block_gcloud_redis_instances_delete(self):
        assert_asks('Bash', {'command': 'gcloud redis instances delete myredis --region=us-central1'})

    def test_block_gcloud_artifacts_repositories_delete(self):
        assert_asks('Bash', {'command': 'gcloud artifacts repositories delete myrepo'})

    def test_block_gcloud_container_images_delete(self):
        assert_asks('Bash', {'command': 'gcloud container images delete gcr.io/project/image:tag'})

    def test_block_gcloud_secrets_delete(self):
        assert_asks('Bash', {'command': 'gcloud secrets delete mysecret'})

    def test_block_gcloud_secrets_versions_destroy(self):
        assert_asks('Bash', {'command': 'gcloud secrets versions destroy 3 --secret=mysecret'})

    def test_block_gcloud_firestore_databases_delete(self):
        assert_asks('Bash', {'command': 'gcloud firestore databases delete --database=mydb'})

    def test_block_gcloud_composer_environments_delete(self):
        assert_asks('Bash', {'command': 'gcloud composer environments delete myenv --location=us-central1'})

    def test_block_gcloud_logging_sinks_delete(self):
        assert_asks('Bash', {'command': 'gcloud logging sinks delete mysink'})

    def test_block_gcloud_logging_buckets_delete(self):
        assert_asks('Bash', {'command': 'gcloud logging buckets delete mybucket --location=global'})

    def test_block_gcloud_monitoring_dashboards_delete(self):
        assert_asks('Bash', {'command': 'gcloud monitoring dashboards delete projects/myproject/dashboards/123'})

    def test_block_gcloud_compute_disks_delete(self):
        assert_asks('Bash', {'command': 'gcloud compute disks delete mydisk --zone=us-central1-a'})

    def test_block_gcloud_compute_snapshots_delete(self):
        assert_asks('Bash', {'command': 'gcloud compute snapshots delete mysnap'})

    def test_block_gcloud_compute_firewall_rules_delete(self):
        assert_asks('Bash', {'command': 'gcloud compute firewall-rules delete allow-ssh'})

    def test_block_gcloud_compute_networks_delete(self):
        assert_asks('Bash', {'command': 'gcloud compute networks delete myvpc'})

    def test_block_gcloud_pubsub_topics_delete(self):
        assert_asks('Bash', {'command': 'gcloud pubsub topics delete my-topic'})

    def test_block_gcloud_pubsub_subscriptions_delete(self):
        assert_asks('Bash', {'command': 'gcloud pubsub subscriptions delete my-sub'})

    def test_block_gcloud_dns_record_sets_delete(self):
        assert_asks('Bash', {'command': 'gcloud dns record-sets delete myrecord --zone=myzone'})


class TestGcpAsk:
    """Tests for GCP CLI operations that should prompt for confirmation."""

    # --- Specific ask patterns ---

    def test_ask_gcloud_compute_instances_start(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "gcloud compute instances start myvm --zone=us-central1-a"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gcloud_compute_instances_stop(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "gcloud compute instances stop myvm --zone=us-central1-a"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gcloud_compute_instances_reset(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "gcloud compute instances reset myvm --zone=us-central1-a"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gcloud_add_iam_policy_binding(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "gcloud projects add-iam-policy-binding myproject --member=user:bob@example.com --role=roles/editor"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- Ask catch-all: create/update/deploy/remove-iam-policy-binding/set-iam-policy ---

    def test_ask_gcloud_run_deploy(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "gcloud run deploy myservice --image=gcr.io/project/image"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gcloud_run_services_update(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "gcloud run services update myservice --memory=512Mi"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gcloud_functions_deploy(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "gcloud functions deploy myfunc --runtime=python311"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gcloud_secrets_create(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "gcloud secrets create mysecret"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gcloud_compute_instances_create(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "gcloud compute instances create myvm --zone=us-central1-a"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gcloud_remove_iam_policy_binding(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "gcloud projects remove-iam-policy-binding myproject --member=user:bob@example.com --role=roles/editor"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gcloud_set_iam_policy(self):
        code, stdout, _ = run_hook(
            "Bash",
            {"command": "gcloud projects set-iam-policy myproject policy.json"},
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gcloud_sql_instances_create(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "gcloud sql instances create mydb --database-version=POSTGRES_14"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gcloud_container_clusters_create(self):
        code, stdout, _ = run_hook(
            "Bash",
            {
                "command": "gcloud container clusters create mycluster --zone=us-central1-a"
            },
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestGcpAllow:
    """Tests for GCP CLI read-only operations that should be allowed."""

    def test_allow_gcloud_compute_instances_list(self):
        code, _, _ = run_hook("Bash", {"command": "gcloud compute instances list"})
        assert code == 0

    def test_allow_gcloud_projects_describe(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud projects describe my-project"}
        )
        assert code == 0

    def test_allow_gcloud_config_list(self):
        code, _, _ = run_hook("Bash", {"command": "gcloud config list"})
        assert code == 0

    def test_allow_gcloud_auth_list(self):
        code, _, _ = run_hook("Bash", {"command": "gcloud auth list"})
        assert code == 0

    def test_allow_gcloud_services_list(self):
        code, _, _ = run_hook("Bash", {"command": "gcloud services list --enabled"})
        assert code == 0

    def test_allow_gcloud_compute_instances_describe(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "gcloud compute instances describe myvm --zone=us-central1-a"},
        )
        assert code == 0


class TestGcpSessionCredentialAsk:
    def test_ask_compute_ssh(self):
        assert_asks("Bash", {"command": "gcloud compute ssh my-instance"})

    def test_ask_auth_login(self):
        assert_asks("Bash", {"command": "gcloud auth login"})
