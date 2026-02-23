"""Tests for Ruby ecosystem security patterns."""

import json

from tests.conftest import run_hook


class TestRubyBlock:
    def test_block_rbenv_uninstall(self):
        code, _, _ = run_hook("Bash", {"command": "rbenv uninstall 3.2.0"})
        assert code == 2

    def test_block_rbenv_remove(self):
        code, _, _ = run_hook("Bash", {"command": "rbenv remove 3.2.0"})
        assert code == 2

    def test_block_rvm_remove(self):
        code, _, _ = run_hook("Bash", {"command": "rvm remove 3.2.0"})
        assert code == 2

    def test_block_rvm_uninstall(self):
        code, _, _ = run_hook("Bash", {"command": "rvm uninstall 3.2.0"})
        assert code == 2


class TestRubyAsk:
    def test_ask_bundle_clean(self):
        code, stdout, _ = run_hook("Bash", {"command": "bundle clean"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestRailsBlock:
    def test_block_rails_db_drop(self):
        code, _, _ = run_hook("Bash", {"command": "rails db:drop"})
        assert code == 2

    def test_block_rails_db_reset(self):
        code, _, _ = run_hook("Bash", {"command": "rails db:reset"})
        assert code == 2

    def test_block_bin_rails_db_drop(self):
        code, _, _ = run_hook("Bash", {"command": "bin/rails db:drop"})
        assert code == 2

    def test_block_rake_db_drop(self):
        code, _, _ = run_hook("Bash", {"command": "rake db:drop"})
        assert code == 2

    def test_block_bin_rake_db_reset(self):
        code, _, _ = run_hook("Bash", {"command": "bin/rake db:reset"})
        assert code == 2

    def test_block_rails_db_schema_load(self):
        code, _, _ = run_hook("Bash", {"command": "rails db:schema:load"})
        assert code == 2

    def test_block_bin_rails_db_schema_load(self):
        code, _, _ = run_hook("Bash", {"command": "bin/rails db:schema:load"})
        assert code == 2


class TestRailsAsk:
    def test_ask_rails_db_rollback(self):
        code, stdout, _ = run_hook("Bash", {"command": "rails db:rollback"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_bin_rails_db_rollback(self):
        code, stdout, _ = run_hook("Bash", {"command": "bin/rails db:rollback"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_rake_db_rollback(self):
        code, stdout, _ = run_hook("Bash", {"command": "rake db:rollback"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_bin_rake_db_rollback(self):
        code, stdout, _ = run_hook("Bash", {"command": "bin/rake db:rollback"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
