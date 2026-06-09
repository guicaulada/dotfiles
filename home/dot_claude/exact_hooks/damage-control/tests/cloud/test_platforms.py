"""Tests for cloud platform security patterns (Firebase, Vercel, Netlify, Cloudflare, Heroku, Fly.io, Railway, DigitalOcean, Supabase)."""

import json

from tests.conftest import assert_asks, run_hook


class TestFirebaseBlock:
    """Tests for Firebase destructive operations that should be blocked."""

    def test_block_firebase_projects_delete(self):
        assert_asks('Bash', {'command': 'firebase projects:delete my-project'})

    def test_block_firebase_firestore_delete_all_collections(self):
        assert_asks('Bash', {'command': 'firebase firestore:delete --all-collections --project my-project'})

    def test_block_firebase_database_remove(self):
        assert_asks('Bash', {'command': 'firebase database:remove /users --project my-project'})

    def test_block_firebase_hosting_disable(self):
        assert_asks('Bash', {'command': 'firebase hosting:disable'})

    def test_block_firebase_functions_delete(self):
        assert_asks('Bash', {'command': 'firebase functions:delete myfunction'})


class TestVercelBlock:
    """Tests for Vercel destructive operations that should be blocked."""

    def test_block_vercel_remove_yes(self):
        assert_asks('Bash', {'command': 'vercel remove my-deployment --yes'})

    def test_block_vercel_projects_rm(self):
        assert_asks('Bash', {'command': 'vercel projects rm my-project'})

    def test_block_vercel_env_rm_yes(self):
        assert_asks('Bash', {'command': 'vercel env rm MY_VAR production --yes'})


class TestNetlifyBlock:
    """Tests for Netlify destructive operations that should be blocked."""

    def test_block_netlify_sites_delete(self):
        assert_asks('Bash', {'command': 'netlify sites:delete'})

    def test_block_netlify_functions_delete(self):
        assert_asks('Bash', {'command': 'netlify functions:delete myfunc'})


class TestWranglerBlock:
    """Tests for Cloudflare Wrangler destructive operations that should be blocked."""

    def test_block_wrangler_delete(self):
        assert_asks('Bash', {'command': 'wrangler delete'})

    def test_block_wrangler_r2_bucket_delete(self):
        assert_asks('Bash', {'command': 'wrangler r2 bucket delete my-bucket'})

    def test_block_wrangler_kv_namespace_delete(self):
        assert_asks('Bash', {'command': 'wrangler kv:namespace delete --namespace-id abc123'})

    def test_block_wrangler_d1_delete(self):
        assert_asks('Bash', {'command': 'wrangler d1 delete my-db'})

    def test_block_wrangler_queues_delete(self):
        assert_asks('Bash', {'command': 'wrangler queues delete my-queue'})


class TestHerokuBlock:
    """Tests for Heroku destructive operations that should be blocked."""

    def test_block_heroku_apps_destroy(self):
        assert_asks('Bash', {'command': 'heroku apps:destroy --app myapp'})

    def test_block_heroku_pg_reset(self):
        assert_asks('Bash', {'command': 'heroku pg:reset DATABASE_URL'})

    def test_block_heroku_addons_destroy(self):
        assert_asks('Bash', {'command': 'heroku addons:destroy heroku-postgresql'})


class TestFlyIoBlock:
    """Tests for Fly.io destructive operations that should be blocked."""

    def test_block_fly_apps_destroy(self):
        assert_asks('Bash', {'command': 'fly apps destroy myapp'})

    def test_block_fly_destroy(self):
        assert_asks('Bash', {'command': 'fly destroy myapp'})

    def test_block_flyctl_destroy(self):
        assert_asks('Bash', {'command': 'flyctl destroy myapp'})

    def test_block_flyctl_apps_destroy(self):
        assert_asks('Bash', {'command': 'flyctl apps destroy myapp'})


class TestRailwayBlock:
    """Tests for Railway destructive operations that should be blocked."""

    def test_block_railway_delete(self):
        assert_asks('Bash', {'command': 'railway delete'})

    def test_block_railway_remove(self):
        assert_asks('Bash', {'command': 'railway remove myservice'})


class TestDigitalOceanBlock:
    """Tests for DigitalOcean destructive operations that should be blocked."""

    def test_block_doctl_droplet_delete(self):
        assert_asks('Bash', {'command': 'doctl compute droplet delete 12345'})

    def test_block_doctl_databases_delete(self):
        assert_asks('Bash', {'command': 'doctl databases delete db-id-123'})

    def test_block_doctl_kubernetes_cluster_delete(self):
        assert_asks('Bash', {'command': 'doctl kubernetes cluster delete mycluster'})

    def test_block_doctl_apps_delete(self):
        assert_asks('Bash', {'command': 'doctl apps delete myapp-id'})


class TestSupabaseBlock:
    """Tests for Supabase destructive operations that should be blocked."""

    def test_block_supabase_db_reset(self):
        assert_asks('Bash', {'command': 'supabase db reset'})

    def test_block_supabase_projects_delete(self):
        assert_asks('Bash', {'command': 'supabase projects delete myproject'})

    def test_block_supabase_functions_delete(self):
        assert_asks('Bash', {'command': 'supabase functions delete myfunc'})


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
