"""Tests for JavaScript ecosystem security patterns."""

import json

from tests.conftest import assert_asks, run_hook


class TestDenoBlock:
    def test_block_deno_run_allow_all_short(self):
        assert_asks('Bash', {'command': 'deno run -A script.ts'})

    def test_block_deno_run_allow_all_long(self):
        assert_asks('Bash', {'command': 'deno run --allow-all script.ts'})


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
        assert_asks('Bash', {'command': 'bun pm cache rm'})


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
        assert_asks('Bash', {'command': 'node -e "const f=require(\'fs\'); f.rm(\'/tmp/d\', {recursive:true}, ()=>{})"'})

    def test_block_node_fs_rmdir_sync(self):
        assert_asks('Bash', {'command': 'node -e "const f=require(\'fs\'); f.rmdirSync(\'/tmp/d\')"'})

    def test_block_node_fs_unlink_sync(self):
        assert_asks('Bash', {'command': 'node -e "const f=require(\'fs\'); f.unlinkSync(\'/tmp/f\')"'})

    def test_block_node_fs_rm_sync(self):
        assert_asks('Bash', {'command': 'node -e "fs.rmSync(\'/tmp/d\', {recursive:true})"'})

    def test_block_node_child_process(self):
        assert_asks('Bash', {'command': 'node -e "require(\'child_process\').execSync(\'rm -rf /\')"'})

    def test_block_node_exec_sync(self):
        assert_asks('Bash', {'command': 'node -e "const {execSync} = require(\'child_process\'); execSync(\'ls\')"'})

    def test_block_node_spawn(self):
        assert_asks('Bash', {'command': 'node -e "require(\'child_process\').spawn(\'ls\')"'})


class TestVersionManagerBlock:
    def test_block_nvm_uninstall(self):
        assert_asks('Bash', {'command': 'nvm uninstall 18'})

    def test_block_fnm_uninstall(self):
        assert_asks('Bash', {'command': 'fnm uninstall 18'})

    def test_block_volta_uninstall(self):
        assert_asks('Bash', {'command': 'volta uninstall node'})


class TestCacheBlock:
    def test_block_npm_cache_clean(self):
        assert_asks('Bash', {'command': 'npm cache clean --force'})

    def test_block_yarn_cache_clean(self):
        assert_asks('Bash', {'command': 'yarn cache clean'})

    def test_block_pnpm_store_prune(self):
        assert_asks('Bash', {'command': 'pnpm store prune'})


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
