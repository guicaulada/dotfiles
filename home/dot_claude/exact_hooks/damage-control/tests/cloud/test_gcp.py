"""Tests for GCP (gcloud) security patterns."""

from tests.conftest import run_hook


class TestGcpBlock:
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

    def test_block_gcloud_dns_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "gcloud dns record-sets delete myrecord --zone=myzone"}
        )
        assert code == 2
