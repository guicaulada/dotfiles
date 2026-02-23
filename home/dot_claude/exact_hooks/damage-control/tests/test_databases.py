"""Tests for database security patterns."""

import json

from tests.conftest import run_hook


class TestDatabaseBlock:
    def test_block_redis_flushall(self):
        code, _, _ = run_hook("Bash", {"command": "redis-cli FLUSHALL"})
        assert code == 2

    def test_block_drop_database(self):
        code, _, _ = run_hook("Bash", {"command": "DROP DATABASE production"})
        assert code == 2

    def test_block_mongo_drop_collection(self):
        code, _, _ = run_hook(
            "Bash", {"command": "mongosh mydb --eval 'db.users.drop()'"}
        )
        assert code == 2

    def test_block_mongo_delete_many_all(self):
        code, _, _ = run_hook(
            "Bash", {"command": "mongosh mydb --eval 'db.users.deleteMany({})'"}
        )
        assert code == 2

    def test_block_psql_drop(self):
        code, _, _ = run_hook("Bash", {"command": "psql mydb -c 'DROP TABLE users'"})
        assert code == 2

    def test_block_psql_truncate(self):
        code, _, _ = run_hook(
            "Bash", {"command": "psql mydb --command 'TRUNCATE TABLE users'"}
        )
        assert code == 2

    def test_block_mysql_drop(self):
        code, _, _ = run_hook("Bash", {"command": "mysql mydb -e 'DROP TABLE users'"})
        assert code == 2

    def test_block_mariadb_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "mariadb mydb --execute 'DELETE FROM users'"}
        )
        assert code == 2

    def test_block_dropuser(self):
        code, _, _ = run_hook("Bash", {"command": "dropuser myuser"})
        assert code == 2

    def test_block_redis_config_set(self):
        code, _, _ = run_hook(
            "Bash", {"command": "redis-cli CONFIG SET maxmemory 100mb"}
        )
        assert code == 2

    def test_block_redis_debug(self):
        code, _, _ = run_hook("Bash", {"command": "redis-cli DEBUG SLEEP 10"})
        assert code == 2


class TestDatabaseAsk:
    def test_ask_sql_delete_with_where(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "DELETE FROM users WHERE id = 5"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
