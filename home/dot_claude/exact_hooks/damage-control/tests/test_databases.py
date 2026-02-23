"""Tests for database security patterns."""

import json

from tests.conftest import run_hook


class TestRedisBlock:
    def test_block_redis_flushall(self):
        code, _, _ = run_hook("Bash", {"command": "redis-cli FLUSHALL"})
        assert code == 2

    def test_block_redis_flushdb(self):
        code, _, _ = run_hook("Bash", {"command": "redis-cli FLUSHDB"})
        assert code == 2

    def test_block_redis_flushall_with_host(self):
        code, _, _ = run_hook("Bash", {"command": "redis-cli -h 127.0.0.1 FLUSHALL"})
        assert code == 2

    def test_block_redis_config_set(self):
        code, _, _ = run_hook(
            "Bash", {"command": "redis-cli CONFIG SET maxmemory 100mb"}
        )
        assert code == 2

    def test_block_redis_config_rewrite(self):
        code, _, _ = run_hook("Bash", {"command": "redis-cli CONFIG REWRITE"})
        assert code == 2

    def test_block_redis_debug(self):
        code, _, _ = run_hook("Bash", {"command": "redis-cli DEBUG SLEEP 10"})
        assert code == 2

    def test_block_redis_slaveof(self):
        code, _, _ = run_hook("Bash", {"command": "redis-cli SLAVEOF 192.168.1.1 6379"})
        assert code == 2

    def test_block_redis_replicaof(self):
        code, _, _ = run_hook(
            "Bash", {"command": "redis-cli REPLICAOF 192.168.1.1 6379"}
        )
        assert code == 2

    def test_block_redis_shutdown(self):
        code, _, _ = run_hook("Bash", {"command": "redis-cli SHUTDOWN"})
        assert code == 2

    def test_block_redis_shutdown_nosave(self):
        code, _, _ = run_hook("Bash", {"command": "redis-cli SHUTDOWN NOSAVE"})
        assert code == 2


class TestMongoBlock:
    def test_block_mongosh_drop_database(self):
        code, _, _ = run_hook(
            "Bash", {"command": "mongosh mydb --eval 'db.dropDatabase()'"}
        )
        assert code == 2

    def test_block_mongo_drop_database(self):
        code, _, _ = run_hook(
            "Bash", {"command": "mongo mydb --eval 'db.dropDatabase()'"}
        )
        assert code == 2

    def test_block_mongo_drop_collection(self):
        code, _, _ = run_hook(
            "Bash", {"command": "mongosh mydb --eval 'db.users.drop()'"}
        )
        assert code == 2

    def test_block_mongo_drop_collection_explicit(self):
        code, _, _ = run_hook(
            "Bash", {"command": "mongosh mydb --eval 'db.users.dropCollection()'"}
        )
        assert code == 2

    def test_block_mongo_delete_many_all(self):
        code, _, _ = run_hook(
            "Bash", {"command": "mongosh mydb --eval 'db.users.deleteMany({})'"}
        )
        assert code == 2

    def test_block_mongo_delete_many_all_with_spaces(self):
        code, _, _ = run_hook(
            "Bash", {"command": "mongosh mydb --eval 'db.users.deleteMany( { } )'"}
        )
        assert code == 2


class TestPostgresBlock:
    def test_block_dropdb(self):
        code, _, _ = run_hook("Bash", {"command": "dropdb production"})
        assert code == 2

    def test_block_dropdb_with_flags(self):
        code, _, _ = run_hook("Bash", {"command": "dropdb --if-exists production"})
        assert code == 2

    def test_block_dropuser(self):
        code, _, _ = run_hook("Bash", {"command": "dropuser myuser"})
        assert code == 2

    def test_block_psql_drop_table(self):
        code, _, _ = run_hook("Bash", {"command": "psql mydb -c 'DROP TABLE users'"})
        assert code == 2

    def test_block_psql_truncate(self):
        code, _, _ = run_hook(
            "Bash", {"command": "psql mydb --command 'TRUNCATE TABLE users'"}
        )
        assert code == 2

    def test_block_psql_delete_from(self):
        code, _, _ = run_hook("Bash", {"command": "psql mydb -c 'DELETE FROM users'"})
        assert code == 2


class TestMysqlBlock:
    def test_block_mysql_drop(self):
        code, _, _ = run_hook("Bash", {"command": "mysql mydb -e 'DROP TABLE users'"})
        assert code == 2

    def test_block_mysqladmin_drop(self):
        code, _, _ = run_hook("Bash", {"command": "mysqladmin drop production"})
        assert code == 2

    def test_block_mariadb_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "mariadb mydb --execute 'DELETE FROM users'"}
        )
        assert code == 2

    def test_block_mariadb_truncate(self):
        code, _, _ = run_hook(
            "Bash", {"command": "mariadb mydb -e 'TRUNCATE TABLE users'"}
        )
        assert code == 2


class TestSqlBlock:
    def test_block_delete_without_where_semicolon(self):
        code, _, _ = run_hook("Bash", {"command": "DELETE FROM users;"})
        assert code == 2

    def test_block_delete_without_where_eol(self):
        code, _, _ = run_hook("Bash", {"command": "DELETE FROM users"})
        assert code == 2

    def test_block_delete_star_from(self):
        code, _, _ = run_hook("Bash", {"command": "DELETE * FROM users"})
        assert code == 2

    def test_block_truncate_table(self):
        code, _, _ = run_hook("Bash", {"command": "TRUNCATE TABLE users"})
        assert code == 2

    def test_block_drop_table(self):
        code, _, _ = run_hook("Bash", {"command": "DROP TABLE users"})
        assert code == 2

    def test_block_drop_table_if_exists(self):
        code, _, _ = run_hook("Bash", {"command": "DROP TABLE IF EXISTS users"})
        assert code == 2

    def test_block_drop_database(self):
        code, _, _ = run_hook("Bash", {"command": "DROP DATABASE production"})
        assert code == 2

    def test_block_drop_schema(self):
        code, _, _ = run_hook("Bash", {"command": "DROP SCHEMA public"})
        assert code == 2

    def test_block_drop_schema_cascade(self):
        code, _, _ = run_hook("Bash", {"command": "DROP SCHEMA public CASCADE"})
        assert code == 2

    def test_block_delete_from_quoted_table(self):
        code, _, _ = run_hook("Bash", {"command": 'DELETE FROM "my_table";'})
        assert code == 2

    def test_block_delete_from_backtick_table(self):
        code, _, _ = run_hook("Bash", {"command": "DELETE FROM `my_table`;"})
        assert code == 2

    def test_block_delete_from_schema_qualified(self):
        code, _, _ = run_hook("Bash", {"command": "DELETE FROM public.users;"})
        assert code == 2


class TestRabbitmqBlock:
    def test_block_rabbitmqctl_delete_queue(self):
        code, _, _ = run_hook("Bash", {"command": "rabbitmqctl delete_queue my_queue"})
        assert code == 2

    def test_block_rabbitmqctl_delete_vhost(self):
        code, _, _ = run_hook(
            "Bash", {"command": "rabbitmqctl delete_vhost /production"}
        )
        assert code == 2

    def test_block_rabbitmqctl_delete_exchange(self):
        code, _, _ = run_hook(
            "Bash", {"command": "rabbitmqctl delete_exchange my_exchange"}
        )
        assert code == 2

    def test_block_rabbitmqctl_delete_user(self):
        code, _, _ = run_hook("Bash", {"command": "rabbitmqctl delete_user guest"})
        assert code == 2

    def test_block_rabbitmqctl_purge_queue(self):
        code, _, _ = run_hook("Bash", {"command": "rabbitmqctl purge_queue my_queue"})
        assert code == 2

    def test_block_rabbitmqctl_reset(self):
        code, _, _ = run_hook("Bash", {"command": "rabbitmqctl reset"})
        assert code == 2

    def test_block_rabbitmqctl_stop(self):
        code, _, _ = run_hook("Bash", {"command": "rabbitmqctl stop"})
        assert code == 2

    def test_block_rabbitmqctl_shutdown(self):
        code, _, _ = run_hook("Bash", {"command": "rabbitmqctl shutdown"})
        assert code == 2


class TestKafkaBlock:
    def test_block_kafka_topics_delete(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "kafka-topics --bootstrap-server localhost:9092 --delete --topic my-topic"
            },
        )
        assert code == 2

    def test_block_kafka_consumer_groups_delete(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "kafka-consumer-groups --bootstrap-server localhost:9092 --delete --group my-group"
            },
        )
        assert code == 2

    def test_block_kafka_configs_delete(self):
        code, _, _ = run_hook(
            "Bash",
            {
                "command": "kafka-configs --bootstrap-server localhost:9092 --delete --entity-type topics --entity-name my-topic"
            },
        )
        assert code == 2


class TestPrismaBlock:
    def test_block_prisma_migrate_reset(self):
        code, _, _ = run_hook("Bash", {"command": "prisma migrate reset"})
        assert code == 2

    def test_block_npx_prisma_migrate_reset(self):
        code, _, _ = run_hook("Bash", {"command": "npx prisma migrate reset"})
        assert code == 2

    def test_block_prisma_db_push_force_reset(self):
        code, _, _ = run_hook("Bash", {"command": "prisma db push --force-reset"})
        assert code == 2

    def test_block_npx_prisma_db_push_force_reset(self):
        code, _, _ = run_hook("Bash", {"command": "npx prisma db push --force-reset"})
        assert code == 2


class TestFlywayLiquibaseBlock:
    def test_block_flyway_clean(self):
        code, _, _ = run_hook("Bash", {"command": "flyway clean"})
        assert code == 2

    def test_block_liquibase_drop_all(self):
        code, _, _ = run_hook("Bash", {"command": "liquibase drop-all"})
        assert code == 2


class TestDatabaseAsk:
    def test_ask_sql_delete_with_where(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "DELETE FROM users WHERE id = 5"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_prisma_db_execute(self):
        code, stdout, _ = run_hook("Bash", {"command": "prisma db execute --stdin"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_npx_prisma_db_execute(self):
        code, stdout, _ = run_hook("Bash", {"command": "npx prisma db execute --stdin"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_prisma_migrate_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "prisma migrate deploy"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_npx_prisma_migrate_deploy(self):
        code, stdout, _ = run_hook("Bash", {"command": "npx prisma migrate deploy"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_flyway_undo(self):
        code, stdout, _ = run_hook("Bash", {"command": "flyway undo"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_liquibase_rollback(self):
        code, stdout, _ = run_hook("Bash", {"command": "liquibase rollback v1.0"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
