"""Tests for cloud platform security patterns (Firebase, Vercel, Netlify, Heroku, Fly.io, Railway, DigitalOcean, Supabase)."""

import json

from tests.conftest import run_hook


class TestPlatformsBlock:
    def test_block_flyctl_destroy(self):
        code, _, _ = run_hook("Bash", {"command": "flyctl destroy myapp"})
        assert code == 2

    def test_block_flyctl_apps_destroy(self):
        code, _, _ = run_hook("Bash", {"command": "flyctl apps destroy myapp"})
        assert code == 2

    def test_block_railway_delete(self):
        code, _, _ = run_hook("Bash", {"command": "railway delete"})
        assert code == 2

    def test_block_railway_remove(self):
        code, _, _ = run_hook("Bash", {"command": "railway remove myservice"})
        assert code == 2

    def test_block_heroku_addons_destroy(self):
        code, _, _ = run_hook(
            "Bash", {"command": "heroku addons:destroy heroku-postgresql"}
        )
        assert code == 2

    def test_block_supabase_projects_delete(self):
        code, _, _ = run_hook("Bash", {"command": "supabase projects delete myproject"})
        assert code == 2

    def test_block_supabase_functions_delete(self):
        code, _, _ = run_hook("Bash", {"command": "supabase functions delete myfunc"})
        assert code == 2

    def test_block_doctl_kubernetes_cluster_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "doctl kubernetes cluster delete mycluster"}
        )
        assert code == 2

    def test_block_doctl_apps_delete(self):
        code, _, _ = run_hook("Bash", {"command": "doctl apps delete myapp-id"})
        assert code == 2


class TestPlatformsAsk:
    def test_ask_vercel_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "vercel deploy --prod"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_netlify_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "netlify deploy --prod"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_firebase_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "firebase deploy"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_fly_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "fly deploy"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_wrangler_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "wrangler deploy"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_wrangler_publish(self):
        code, stdout, _ = run_hook("Bash", {"command": "wrangler publish"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gcloud_app_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "gcloud app deploy"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_heroku_container_release(self):
        code, stdout, _ = run_hook("Bash", {"command": "heroku container:release web"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_flyctl_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "flyctl deploy"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_railway_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "railway deploy"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_heroku_config_unset(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "heroku config:unset DATABASE_URL"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_heroku_releases_rollback(self):
        code, stdout, _ = run_hook("Bash", {"command": "heroku releases:rollback v10"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
