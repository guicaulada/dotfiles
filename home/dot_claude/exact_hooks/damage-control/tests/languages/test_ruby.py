"""Tests for Ruby ecosystem security patterns."""

import json

from tests.conftest import assert_asks, run_hook


class TestRubyBlock:
    def test_block_rbenv_uninstall(self):
        assert_asks('Bash', {'command': 'rbenv uninstall 3.2.0'})

    def test_block_rbenv_remove(self):
        assert_asks('Bash', {'command': 'rbenv remove 3.2.0'})

    def test_block_rvm_remove(self):
        assert_asks('Bash', {'command': 'rvm remove 3.2.0'})

    def test_block_rvm_uninstall(self):
        assert_asks('Bash', {'command': 'rvm uninstall 3.2.0'})


class TestRubyAsk:
    def test_ask_bundle_clean(self):
        code, stdout, _ = run_hook("Bash", {"command": "bundle clean"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestRailsBlock:
    def test_block_rails_db_drop(self):
        assert_asks('Bash', {'command': 'rails db:drop'})

    def test_block_rails_db_reset(self):
        assert_asks('Bash', {'command': 'rails db:reset'})

    def test_block_bin_rails_db_drop(self):
        assert_asks('Bash', {'command': 'bin/rails db:drop'})

    def test_block_rake_db_drop(self):
        assert_asks('Bash', {'command': 'rake db:drop'})

    def test_block_bin_rake_db_reset(self):
        assert_asks('Bash', {'command': 'bin/rake db:reset'})

    def test_block_rails_db_schema_load(self):
        assert_asks('Bash', {'command': 'rails db:schema:load'})

    def test_block_bin_rails_db_schema_load(self):
        assert_asks('Bash', {'command': 'bin/rails db:schema:load'})


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


class TestGemMutationAsk:
    def test_ask_gem_install(self):
        assert_asks("Bash", {"command": "gem install bundler"})

    def test_ask_gem_push(self):
        assert_asks("Bash", {"command": "gem push mygem-1.0.0.gem"})
