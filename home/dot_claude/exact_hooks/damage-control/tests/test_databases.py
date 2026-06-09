"""Tests for database security patterns."""

import json

from tests.conftest import assert_asks, run_hook


class TestRedisBlock:
    def test_block_redis_flushall(self):
        assert_asks('Bash', {'command': 'redis-cli FLUSHALL'})

    def test_block_redis_flushdb(self):
        assert_asks('Bash', {'command': 'redis-cli FLUSHDB'})

    def test_block_redis_flushall_with_host(self):
        assert_asks('Bash', {'command': 'redis-cli -h 127.0.0.1 FLUSHALL'})

    def test_block_redis_config_set(self):
        assert_asks('Bash', {'command': 'redis-cli CONFIG SET maxmemory 100mb'})

    def test_block_redis_config_rewrite(self):
        assert_asks('Bash', {'command': 'redis-cli CONFIG REWRITE'})

    def test_block_redis_debug(self):
        assert_asks('Bash', {'command': 'redis-cli DEBUG SLEEP 10'})

    def test_block_redis_slaveof(self):
        assert_asks('Bash', {'command': 'redis-cli SLAVEOF 192.168.1.1 6379'})

    def test_block_redis_replicaof(self):
        assert_asks('Bash', {'command': 'redis-cli REPLICAOF 192.168.1.1 6379'})

    def test_block_redis_shutdown(self):
        assert_asks('Bash', {'command': 'redis-cli SHUTDOWN'})

    def test_block_redis_shutdown_nosave(self):
        assert_asks('Bash', {'command': 'redis-cli SHUTDOWN NOSAVE'})


class TestMongoBlock:
    def test_block_mongosh_drop_database(self):
        assert_asks('Bash', {'command': "mongosh mydb --eval 'db.dropDatabase()'"})

    def test_block_mongo_drop_database(self):
        assert_asks('Bash', {'command': "mongo mydb --eval 'db.dropDatabase()'"})

    def test_block_mongo_drop_collection(self):
        assert_asks('Bash', {'command': "mongosh mydb --eval 'db.users.drop()'"})

    def test_block_mongo_drop_collection_explicit(self):
        assert_asks('Bash', {'command': "mongosh mydb --eval 'db.users.dropCollection()'"})

    def test_block_mongo_delete_many_all(self):
        assert_asks('Bash', {'command': "mongosh mydb --eval 'db.users.deleteMany({})'"})

    def test_block_mongo_delete_many_all_with_spaces(self):
        assert_asks('Bash', {'command': "mongosh mydb --eval 'db.users.deleteMany( { } )'"})


class TestPostgresBlock:
    def test_block_dropdb(self):
        assert_asks('Bash', {'command': 'dropdb production'})

    def test_block_dropdb_with_flags(self):
        assert_asks('Bash', {'command': 'dropdb --if-exists production'})

    def test_block_dropuser(self):
        assert_asks('Bash', {'command': 'dropuser myuser'})

    def test_block_psql_drop_table(self):
        assert_asks('Bash', {'command': "psql mydb -c 'DROP TABLE users'"})

    def test_block_psql_truncate(self):
        assert_asks('Bash', {'command': "psql mydb --command 'TRUNCATE TABLE users'"})

    def test_block_psql_delete_from(self):
        assert_asks('Bash', {'command': "psql mydb -c 'DELETE FROM users'"})


class TestMysqlBlock:
    def test_block_mysql_drop(self):
        assert_asks('Bash', {'command': "mysql mydb -e 'DROP TABLE users'"})

    def test_block_mysqladmin_drop(self):
        assert_asks('Bash', {'command': 'mysqladmin drop production'})

    def test_block_mariadb_delete(self):
        assert_asks('Bash', {'command': "mariadb mydb --execute 'DELETE FROM users'"})

    def test_block_mariadb_truncate(self):
        assert_asks('Bash', {'command': "mariadb mydb -e 'TRUNCATE TABLE users'"})


class TestSqlBlock:
    def test_block_delete_without_where_semicolon(self):
        assert_asks('Bash', {'command': 'DELETE FROM users;'})

    def test_block_delete_without_where_eol(self):
        assert_asks('Bash', {'command': 'DELETE FROM users'})

    def test_block_delete_star_from(self):
        assert_asks('Bash', {'command': 'DELETE * FROM users'})

    def test_block_truncate_table(self):
        assert_asks('Bash', {'command': 'TRUNCATE TABLE users'})

    def test_block_drop_table(self):
        assert_asks('Bash', {'command': 'DROP TABLE users'})

    def test_block_drop_table_if_exists(self):
        assert_asks('Bash', {'command': 'DROP TABLE IF EXISTS users'})

    def test_block_drop_database(self):
        assert_asks('Bash', {'command': 'DROP DATABASE production'})

    def test_block_drop_schema(self):
        assert_asks('Bash', {'command': 'DROP SCHEMA public'})

    def test_block_drop_schema_cascade(self):
        assert_asks('Bash', {'command': 'DROP SCHEMA public CASCADE'})

    def test_block_delete_from_quoted_table(self):
        assert_asks('Bash', {'command': 'DELETE FROM "my_table";'})

    def test_block_delete_from_backtick_table(self):
        assert_asks('Bash', {'command': 'DELETE FROM `my_table`;'})

    def test_block_delete_from_schema_qualified(self):
        assert_asks('Bash', {'command': 'DELETE FROM public.users;'})


class TestRabbitmqBlock:
    def test_block_rabbitmqctl_delete_queue(self):
        assert_asks('Bash', {'command': 'rabbitmqctl delete_queue my_queue'})

    def test_block_rabbitmqctl_delete_vhost(self):
        assert_asks('Bash', {'command': 'rabbitmqctl delete_vhost /production'})

    def test_block_rabbitmqctl_delete_exchange(self):
        assert_asks('Bash', {'command': 'rabbitmqctl delete_exchange my_exchange'})

    def test_block_rabbitmqctl_delete_user(self):
        assert_asks('Bash', {'command': 'rabbitmqctl delete_user guest'})

    def test_block_rabbitmqctl_purge_queue(self):
        assert_asks('Bash', {'command': 'rabbitmqctl purge_queue my_queue'})

    def test_block_rabbitmqctl_reset(self):
        assert_asks('Bash', {'command': 'rabbitmqctl reset'})

    def test_block_rabbitmqctl_stop(self):
        assert_asks('Bash', {'command': 'rabbitmqctl stop'})

    def test_block_rabbitmqctl_shutdown(self):
        assert_asks('Bash', {'command': 'rabbitmqctl shutdown'})


class TestKafkaBlock:
    def test_block_kafka_topics_delete(self):
        assert_asks('Bash', {'command': 'kafka-topics --bootstrap-server localhost:9092 --delete --topic my-topic'})

    def test_block_kafka_consumer_groups_delete(self):
        assert_asks('Bash', {'command': 'kafka-consumer-groups --bootstrap-server localhost:9092 --delete --group my-group'})

    def test_block_kafka_configs_delete(self):
        assert_asks('Bash', {'command': 'kafka-configs --bootstrap-server localhost:9092 --delete --entity-type topics --entity-name my-topic'})


class TestPrismaBlock:
    def test_block_prisma_migrate_reset(self):
        assert_asks('Bash', {'command': 'prisma migrate reset'})

    def test_block_npx_prisma_migrate_reset(self):
        assert_asks('Bash', {'command': 'npx prisma migrate reset'})

    def test_block_prisma_db_push_force_reset(self):
        assert_asks('Bash', {'command': 'prisma db push --force-reset'})

    def test_block_npx_prisma_db_push_force_reset(self):
        assert_asks('Bash', {'command': 'npx prisma db push --force-reset'})


class TestFlywayLiquibaseBlock:
    def test_block_flyway_clean(self):
        assert_asks('Bash', {'command': 'flyway clean'})

    def test_block_liquibase_drop_all(self):
        assert_asks('Bash', {'command': 'liquibase drop-all'})


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
