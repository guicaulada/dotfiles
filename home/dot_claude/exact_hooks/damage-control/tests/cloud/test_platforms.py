"""Tests for cloud platform security patterns (Firebase, Vercel, Netlify, Cloudflare, Heroku, Fly.io, Railway, DigitalOcean, Supabase)."""

import json

from tests.conftest import run_hook


class TestFirebaseBlock:
    """Tests for Firebase destructive operations that should be blocked."""

    def test_block_firebase_projects_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "firebase projects:delete my-project"}
        )
        assert code == 2

    def test_block_firebase_firestore_delete_all_collections(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "firebase firestore:delete --all-collections --project my-project"
            },
        )
        assert code == 2

    def test_block_firebase_database_remove(self):
        code, _, _ = run_hook(
            "Bash", {"command": "firebase database:remove /users --project my-project"}
        )
        assert code == 2

    def test_block_firebase_hosting_disable(self):
        code, _, _ = run_hook("Bash", {"command": "firebase hosting:disable"})
        assert code == 2

    def test_block_firebase_functions_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "firebase functions:delete myfunction"}
        )
        assert code == 2


class TestVercelBlock:
    """Tests for Vercel destructive operations that should be blocked."""

    def test_block_vercel_remove_yes(self):
        code, _, _ = run_hook("Bash", {"command": "vercel remove my-deployment --yes"})
        assert code == 2

    def test_block_vercel_projects_rm(self):
        code, _, _ = run_hook("Bash", {"command": "vercel projects rm my-project"})
        assert code == 2

    def test_block_vercel_env_rm_yes(self):
        code, _, _ = run_hook(
            "Bash", {"command": "vercel env rm MY_VAR production --yes"}
        )
        assert code == 2


class TestNetlifyBlock:
    """Tests for Netlify destructive operations that should be blocked."""

    def test_block_netlify_sites_delete(self):
        code, _, _ = run_hook("Bash", {"command": "netlify sites:delete"})
        assert code == 2

    def test_block_netlify_functions_delete(self):
        code, _, _ = run_hook("Bash", {"command": "netlify functions:delete myfunc"})
        assert code == 2


class TestWranglerBlock:
    """Tests for Cloudflare Wrangler destructive operations that should be blocked."""

    def test_block_wrangler_delete(self):
        code, _, _ = run_hook("Bash", {"command": "wrangler delete"})
        assert code == 2

    def test_block_wrangler_r2_bucket_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "wrangler r2 bucket delete my-bucket"}
        )
        assert code == 2

    def test_block_wrangler_kv_namespace_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "wrangler kv:namespace delete --namespace-id abc123"}
        )
        assert code == 2

    def test_block_wrangler_d1_delete(self):
        code, _, _ = run_hook("Bash", {"command": "wrangler d1 delete my-db"})
        assert code == 2

    def test_block_wrangler_queues_delete(self):
        code, _, _ = run_hook("Bash", {"command": "wrangler queues delete my-queue"})
        assert code == 2


class TestHerokuBlock:
    """Tests for Heroku destructive operations that should be blocked."""

    def test_block_heroku_apps_destroy(self):
        code, _, _ = run_hook("Bash", {"command": "heroku apps:destroy --app myapp"})
        assert code == 2

    def test_block_heroku_pg_reset(self):
        code, _, _ = run_hook("Bash", {"command": "heroku pg:reset DATABASE_URL"})
        assert code == 2

    def test_block_heroku_addons_destroy(self):
        code, _, _ = run_hook(
            "Bash", {"command": "heroku addons:destroy heroku-postgresql"}
        )
        assert code == 2


class TestFlyIoBlock:
    """Tests for Fly.io destructive operations that should be blocked."""

    def test_block_fly_apps_destroy(self):
        code, _, _ = run_hook("Bash", {"command": "fly apps destroy myapp"})
        assert code == 2

    def test_block_fly_destroy(self):
        code, _, _ = run_hook("Bash", {"command": "fly destroy myapp"})
        assert code == 2

    def test_block_flyctl_destroy(self):
        code, _, _ = run_hook("Bash", {"command": "flyctl destroy myapp"})
        assert code == 2

    def test_block_flyctl_apps_destroy(self):
        code, _, _ = run_hook("Bash", {"command": "flyctl apps destroy myapp"})
        assert code == 2


class TestRailwayBlock:
    """Tests for Railway destructive operations that should be blocked."""

    def test_block_railway_delete(self):
        code, _, _ = run_hook("Bash", {"command": "railway delete"})
        assert code == 2

    def test_block_railway_remove(self):
        code, _, _ = run_hook("Bash", {"command": "railway remove myservice"})
        assert code == 2


class TestDigitalOceanBlock:
    """Tests for DigitalOcean destructive operations that should be blocked."""

    def test_block_doctl_droplet_delete(self):
        code, _, _ = run_hook("Bash", {"command": "doctl compute droplet delete 12345"})
        assert code == 2

    def test_block_doctl_databases_delete(self):
        code, _, _ = run_hook("Bash", {"command": "doctl databases delete db-id-123"})
        assert code == 2

    def test_block_doctl_kubernetes_cluster_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "doctl kubernetes cluster delete mycluster"}
        )
        assert code == 2

    def test_block_doctl_apps_delete(self):
        code, _, _ = run_hook("Bash", {"command": "doctl apps delete myapp-id"})
        assert code == 2


class TestSupabaseBlock:
    """Tests for Supabase destructive operations that should be blocked."""

    def test_block_supabase_db_reset(self):
        code, _, _ = run_hook("Bash", {"command": "supabase db reset"})
        assert code == 2

    def test_block_supabase_projects_delete(self):
        code, _, _ = run_hook("Bash", {"command": "supabase projects delete myproject"})
        assert code == 2

    def test_block_supabase_functions_delete(self):
        code, _, _ = run_hook("Bash", {"command": "supabase functions delete myfunc"})
        assert code == 2


class TestPlatformsAsk:
    """Tests for platform deployment operations that should prompt for confirmation."""

    # --- Deployment operations ---

    def test_ask_vercel_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "vercel deploy --prod"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_vercel_prod_flag(self):
        code, stdout, _ = run_hook("Bash", {"command": "vercel --prod"})
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

    def test_ask_firebase_deploy_only(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "firebase deploy --only functions"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_fly_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "fly deploy"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_flyctl_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "flyctl deploy"})
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

    def test_ask_railway_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "railway deploy"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    # --- Heroku config/rollback operations ---

    def test_ask_heroku_config_unset(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "heroku config:unset DATABASE_URL"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_heroku_domains_remove(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "heroku domains:remove www.example.com"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_heroku_releases_rollback(self):
        code, stdout, _ = run_hook("Bash", {"command": "heroku releases:rollback v10"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestPlatformsAllow:
    """Tests for platform read-only operations that should be allowed."""

    def test_allow_firebase_projects_list(self):
        code, _, _ = run_hook("Bash", {"command": "firebase projects:list"})
        assert code == 0

    def test_allow_vercel_ls(self):
        code, _, _ = run_hook("Bash", {"command": "vercel ls"})
        assert code == 0

    def test_allow_netlify_status(self):
        code, _, _ = run_hook("Bash", {"command": "netlify status"})
        assert code == 0

    def test_allow_heroku_apps_info(self):
        code, _, _ = run_hook("Bash", {"command": "heroku apps:info --app myapp"})
        assert code == 0

    def test_allow_fly_status(self):
        code, _, _ = run_hook("Bash", {"command": "fly status"})
        assert code == 0

    def test_allow_doctl_account_get(self):
        code, _, _ = run_hook("Bash", {"command": "doctl account get"})
        assert code == 0

    def test_allow_supabase_status(self):
        code, _, _ = run_hook("Bash", {"command": "supabase status"})
        assert code == 0

    def test_allow_wrangler_whoami(self):
        code, _, _ = run_hook("Bash", {"command": "wrangler whoami"})
        assert code == 0

    def test_allow_railway_status(self):
        code, _, _ = run_hook("Bash", {"command": "railway status"})
        assert code == 0
