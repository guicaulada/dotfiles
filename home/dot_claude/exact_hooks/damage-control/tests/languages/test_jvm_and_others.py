"""Tests for JVM, Go, Rust, PHP, Elixir, Swift, Haskell, .NET, Dart, Lua, Perl security patterns."""

import json

from tests.conftest import run_hook


# ---------------------------------------------------------------------------
# GO
# ---------------------------------------------------------------------------
class TestGoBlock:
    def test_block_go_clean_modcache(self):
        code, _, _ = run_hook("Bash", {"command": "go clean -modcache"})
        assert code == 2


class TestGoAsk:
    def test_ask_go_clean_cache(self):
        code, stdout, _ = run_hook("Bash", {"command": "go clean -cache"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_go_clean_testcache(self):
        code, stdout, _ = run_hook("Bash", {"command": "go clean -testcache"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_go_clean_fuzzcache(self):
        code, stdout, _ = run_hook("Bash", {"command": "go clean -fuzzcache"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


# ---------------------------------------------------------------------------
# RUST
# ---------------------------------------------------------------------------
class TestRustBlock:
    def test_block_rustup_self_uninstall(self):
        code, _, _ = run_hook("Bash", {"command": "rustup self uninstall"})
        assert code == 2


class TestRustAsk:
    def test_ask_cargo_clean(self):
        code, stdout, _ = run_hook("Bash", {"command": "cargo clean"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_rustup_toolchain_uninstall(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "rustup toolchain uninstall nightly"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_rustup_toolchain_remove(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "rustup toolchain remove stable"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_cargo_uninstall(self):
        code, stdout, _ = run_hook("Bash", {"command": "cargo uninstall ripgrep"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


# ---------------------------------------------------------------------------
# JAVA / JVM
# ---------------------------------------------------------------------------
class TestJvmBlock:
    def test_block_mvn_purge_local_repository(self):
        code, _, _ = run_hook(
            "Bash", {"command": "mvn dependency:purge-local-repository"}
        )
        assert code == 2

    def test_block_sdk_uninstall(self):
        code, _, _ = run_hook("Bash", {"command": "sdk uninstall java 17.0.1-tem"})
        assert code == 2

    def test_block_sdk_rm(self):
        code, _, _ = run_hook("Bash", {"command": "sdk rm java 17.0.1-tem"})
        assert code == 2


class TestJvmAsk:
    def test_ask_mvn_clean(self):
        code, stdout, _ = run_hook("Bash", {"command": "mvn clean install"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gradle_clean(self):
        code, stdout, _ = run_hook("Bash", {"command": "gradle clean"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_gradlew_clean(self):
        code, stdout, _ = run_hook("Bash", {"command": "gradlew clean"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_sbt_clean(self):
        code, stdout, _ = run_hook("Bash", {"command": "sbt clean"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


# ---------------------------------------------------------------------------
# PHP
# ---------------------------------------------------------------------------
class TestPhpBlock:
    def test_block_artisan_migrate_fresh(self):
        code, _, _ = run_hook("Bash", {"command": "php artisan migrate:fresh"})
        assert code == 2

    def test_block_artisan_db_wipe(self):
        code, _, _ = run_hook("Bash", {"command": "php artisan db:wipe"})
        assert code == 2

    def test_block_artisan_migrate_reset(self):
        code, _, _ = run_hook("Bash", {"command": "php artisan migrate:reset"})
        assert code == 2


class TestPhpAsk:
    def test_ask_composer_remove(self):
        code, stdout, _ = run_hook(
            "Bash", {"command": "composer remove monolog/monolog"}
        )
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_artisan_migrate_rollback(self):
        code, stdout, _ = run_hook("Bash", {"command": "php artisan migrate:rollback"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


# ---------------------------------------------------------------------------
# ELIXIR
# ---------------------------------------------------------------------------
class TestElixirBlock:
    def test_block_mix_ecto_drop(self):
        code, _, _ = run_hook("Bash", {"command": "mix ecto.drop"})
        assert code == 2

    def test_block_mix_ecto_reset(self):
        code, _, _ = run_hook("Bash", {"command": "mix ecto.reset"})
        assert code == 2

    def test_block_mix_deps_clean_all(self):
        code, _, _ = run_hook("Bash", {"command": "mix deps.clean --all"})
        assert code == 2


class TestElixirAsk:
    def test_ask_mix_ecto_rollback(self):
        code, stdout, _ = run_hook("Bash", {"command": "mix ecto.rollback"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


# ---------------------------------------------------------------------------
# SWIFT / XCODE
# ---------------------------------------------------------------------------
class TestSwiftBlock:
    def test_block_swift_package_reset(self):
        code, _, _ = run_hook("Bash", {"command": "swift package reset"})
        assert code == 2


class TestSwiftAsk:
    def test_ask_xcodebuild_clean(self):
        code, stdout, _ = run_hook("Bash", {"command": "xcodebuild clean"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


# ---------------------------------------------------------------------------
# .NET / C#
# ---------------------------------------------------------------------------
class TestDotnetBlock:
    def test_block_dotnet_nuget_delete(self):
        code, _, _ = run_hook(
            "Bash", {"command": "dotnet nuget delete MyPackage 1.0.0"}
        )
        assert code == 2


class TestDotnetAsk:
    def test_ask_dotnet_clean(self):
        code, stdout, _ = run_hook("Bash", {"command": "dotnet clean"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


# ---------------------------------------------------------------------------
# HASKELL
# ---------------------------------------------------------------------------
class TestHaskellBlock:
    def test_block_stack_purge(self):
        code, _, _ = run_hook("Bash", {"command": "stack purge"})
        assert code == 2


class TestHaskellAsk:
    def test_ask_stack_clean(self):
        code, stdout, _ = run_hook("Bash", {"command": "stack clean"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


# ---------------------------------------------------------------------------
# DART / FLUTTER
# ---------------------------------------------------------------------------
class TestDartAsk:
    def test_ask_flutter_clean(self):
        code, stdout, _ = run_hook("Bash", {"command": "flutter clean"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_dart_pub_cache_clean(self):
        code, stdout, _ = run_hook("Bash", {"command": "dart pub cache clean"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


# ---------------------------------------------------------------------------
# LUA / PERL
# ---------------------------------------------------------------------------
class TestLuaBlock:
    def test_block_luarocks_purge(self):
        code, _, _ = run_hook("Bash", {"command": "luarocks purge"})
        assert code == 2


class TestLuaAsk:
    def test_ask_luarocks_remove(self):
        code, stdout, _ = run_hook("Bash", {"command": "luarocks remove luasocket"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


class TestPerlAsk:
    def test_ask_cpanm_uninstall(self):
        code, stdout, _ = run_hook("Bash", {"command": "cpanm --uninstall Moose"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"


# ---------------------------------------------------------------------------
# INLINE CODE EXECUTION
# ---------------------------------------------------------------------------
class TestInlineCodeAsk:
    def test_ask_julia_e(self):
        code, stdout, _ = run_hook("Bash", {"command": "julia -e 'println(\"hello\")'"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"

    def test_ask_rscript_e(self):
        code, stdout, _ = run_hook("Bash", {"command": "Rscript -e 'print(1+1)'"})
        assert code == 0
        data = json.loads(stdout)
        assert data["hookSpecificOutput"]["permissionDecision"] == "ask"
