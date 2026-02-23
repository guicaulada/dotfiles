"""Tests for JavaScript ecosystem security patterns."""

import json

from tests.conftest import run_hook


class TestDenoBlock:
    def test_block_deno_run_allow_all_short(self):
        code, _, _ = run_hook("Bash", {"command": "deno run -A script.ts"})
        assert code == 2

    def test_block_deno_run_allow_all_long(self):
        code, _, _ = run_hook("Bash", {"command": "deno run --allow-all script.ts"})
        assert code == 2


class TestDenoAsk:
    def test_ask_deno_install(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "deno install --allow-net server.ts"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_deno_eval(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "deno eval \"console.log('hi')\""}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestBunBlock:
    def test_block_bun_pm_cache_rm(self):
        code, _, _ = run_hook("Bash", {"command": "bun pm cache rm"})
        assert code == 2


class TestBunAsk:
    def test_ask_bun_remove(self):
        code, stdout, _ = run_hook("Bash", {"command": "bun remove express"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_bun_rm(self):
        code, stdout, _ = run_hook("Bash", {"command": "bun rm express"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestNodeBlock:
    def test_block_node_fs_rm_require(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "node -e \"const f=require('fs'); f.rm('/tmp/d', {recursive:true}, ()=>{})\""
            },
        )
        assert code == 2

    def test_block_node_fs_rmdir_sync(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "node -e \"const f=require('fs'); f.rmdirSync('/tmp/d')\""},
        )
        assert code == 2

    def test_block_node_fs_unlink_sync(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "node -e \"const f=require('fs'); f.unlinkSync('/tmp/f')\""},
        )
        assert code == 2

    def test_block_node_fs_rm_sync(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "node -e \"fs.rmSync('/tmp/d', {recursive:true})\""},
        )
        assert code == 2

    def test_block_node_child_process(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "node -e \"require('child_process').execSync('rm -rf /')\""},
        )
        assert code == 2

    def test_block_node_exec_sync(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "node -e \"const {execSync} = require('child_process'); execSync('ls')\""
            },
        )
        assert code == 2

    def test_block_node_spawn(self):
        code, _, _ = run_hook(
            "Bash",
            {"command": "node -e \"require('child_process').spawn('ls')\""},
        )
        assert code == 2


class TestVersionManagerBlock:
    def test_block_nvm_uninstall(self):
        code, _, _ = run_hook("Bash", {"command": "nvm uninstall 18"})
        assert code == 2

    def test_block_fnm_uninstall(self):
        code, _, _ = run_hook("Bash", {"command": "fnm uninstall 18"})
        assert code == 2

    def test_block_volta_uninstall(self):
        code, _, _ = run_hook("Bash", {"command": "volta uninstall node"})
        assert code == 2


class TestCacheBlock:
    def test_block_npm_cache_clean(self):
        code, _, _ = run_hook("Bash", {"command": "npm cache clean --force"})
        assert code == 2

    def test_block_yarn_cache_clean(self):
        code, _, _ = run_hook("Bash", {"command": "yarn cache clean"})
        assert code == 2

    def test_block_pnpm_store_prune(self):
        code, _, _ = run_hook("Bash", {"command": "pnpm store prune"})
        assert code == 2


class TestCacheAsk:
    def test_ask_npm_ci(self):
        code, stdout, _ = run_hook("Bash", {"command": "npm ci"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestMonorepoAsk:
    def test_ask_nx_reset(self):
        code, stdout, _ = run_hook("Bash", {"command": "nx reset"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_turbo_clean(self):
        code, stdout, _ = run_hook("Bash", {"command": "turbo clean"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_turbo_prune(self):
        code, stdout, _ = run_hook("Bash", {"command": "turbo prune --scope=app"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_lerna_clean(self):
        code, stdout, _ = run_hook("Bash", {"command": "lerna clean"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_rush_purge(self):
        code, stdout, _ = run_hook("Bash", {"command": "rush purge"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
