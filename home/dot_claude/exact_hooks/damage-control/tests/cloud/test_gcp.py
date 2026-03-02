"""Tests for GCP (gcloud) security patterns."""

import json

from tests.conftest import run_hook


class TestGcpBlock:
    """Tests for GCP CLI operations that should be blocked."""

    # --- Credential exposure ---

    def test_block_gcloud_auth_print_access_token(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud auth print-access-token"}
        )
        assert code == 2

    def test_block_gcloud_auth_print_identity_token(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud auth print-identity-token"}
        )
        assert code == 2

    def test_block_gcloud_auth_adc_print_access_token(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "gcloud auth application-default print-access-token"},
        )
        assert code == 2

    # --- Specific block patterns (not caught by catch-all) ---

    def test_block_gcloud_storage_rm_recursive(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud storage rm -r gs://my-bucket/path/"}
        )
        assert code == 2

    def test_block_gcloud_secrets_versions_disable(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "gcloud secrets versions disable 3 --secret=mysecret"},
        )
        assert code == 2

    def test_block_gcloud_dataflow_jobs_cancel(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud dataflow jobs cancel job-123"}
        )
        assert code == 2

    def test_block_gcloud_dataflow_jobs_drain(self):
        code, _, _ = run_hook("Bash", {"command": "gcloud dataflow jobs drain job-123"})
        assert code == 2

    # --- Block catch-all: "gcloud ... delete" or "gcloud ... destroy" ---

    def test_block_gcloud_projects_delete(self):
        code, _, _ = run_hook("Bash", {"command": "gcloud projects delete my-project"})
        assert code == 2

    def test_block_gcloud_compute_instances_delete(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "gcloud compute instances delete myvm --zone=us-central1-a"},
        )
        assert code == 2

    def test_block_gcloud_sql_instances_delete(self):
        code, _, _ = run_hook("Bash", {"command": "gcloud sql instances delete mydb"})
        assert code == 2

    def test_block_gcloud_container_clusters_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud container clusters delete mycluster"}
        )
        assert code == 2

    def test_block_gcloud_functions_delete(self):
        code, _, _ = run_hook("Bash", {"command": "gcloud functions delete myfunction"})
        assert code == 2

    def test_block_gcloud_iam_service_accounts_delete(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "gcloud iam service-accounts delete sa@project.iam.gserviceaccount.com"
            },
        )
        assert code == 2

    def test_block_gcloud_run_services_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud run services delete myservice"}
        )
        assert code == 2

    def test_block_gcloud_spanner_instances_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud spanner instances delete myinstance"}
        )
        assert code == 2

    def test_block_gcloud_spanner_databases_delete(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "gcloud spanner databases delete mydb --instance=myinstance"},
        )
        assert code == 2

    def test_block_gcloud_bigtable_instances_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud bigtable instances delete mybt"}
        )
        assert code == 2

    def test_block_gcloud_redis_instances_delete(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "gcloud redis instances delete myredis --region=us-central1"},
        )
        assert code == 2

    def test_block_gcloud_artifacts_repositories_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud artifacts repositories delete myrepo"}
        )
        assert code == 2

    def test_block_gcloud_container_images_delete(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "gcloud container images delete gcr.io/project/image:tag"},
        )
        assert code == 2

    def test_block_gcloud_secrets_delete(self):
        code, _, _ = run_hook("Bash", {"command": "gcloud secrets delete mysecret"})
        assert code == 2

    def test_block_gcloud_secrets_versions_destroy(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "gcloud secrets versions destroy 3 --secret=mysecret"},
        )
        assert code == 2

    def test_block_gcloud_firestore_databases_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud firestore databases delete --database=mydb"}
        )
        assert code == 2

    def test_block_gcloud_composer_environments_delete(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "gcloud composer environments delete myenv --location=us-central1"
            },
        )
        assert code == 2

    def test_block_gcloud_logging_sinks_delete(self):
        code, _, _ = run_hook("Bash", {"command": "gcloud logging sinks delete mysink"})
        assert code == 2

    def test_block_gcloud_logging_buckets_delete(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "gcloud logging buckets delete mybucket --location=global"},
        )
        assert code == 2

    def test_block_gcloud_monitoring_dashboards_delete(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "gcloud monitoring dashboards delete projects/myproject/dashboards/123"
            },
        )
        assert code == 2

    def test_block_gcloud_compute_disks_delete(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "gcloud compute disks delete mydisk --zone=us-central1-a"},
        )
        assert code == 2

    def test_block_gcloud_compute_snapshots_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud compute snapshots delete mysnap"}
        )
        assert code == 2

    def test_block_gcloud_compute_firewall_rules_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud compute firewall-rules delete allow-ssh"}
        )
        assert code == 2

    def test_block_gcloud_compute_networks_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud compute networks delete myvpc"}
        )
        assert code == 2

    def test_block_gcloud_pubsub_topics_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud pubsub topics delete my-topic"}
        )
        assert code == 2

    def test_block_gcloud_pubsub_subscriptions_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud pubsub subscriptions delete my-sub"}
        )
        assert code == 2

    def test_block_gcloud_dns_record_sets_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud dns record-sets delete myrecord --zone=myzone"}
        )
        assert code == 2


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
