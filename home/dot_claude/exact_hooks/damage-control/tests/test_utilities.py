"""Tests for utility functions: is_glob_pattern, glob_to_regex, match_path, check_path_patterns."""

from tests.conftest import HOME, dc


class TestIsGlobPattern:
    def test_star(self):
        assert dc.is_glob_pattern("*.pem") is True

    def test_question_mark(self):
        assert dc.is_glob_pattern("file?.txt") is True

    def test_bracket(self):
        assert dc.is_glob_pattern("[abc].txt") is True

    def test_literal_path(self):
        assert dc.is_glob_pattern("/etc/hosts") is False

    def test_tilde_path(self):
        assert dc.is_glob_pattern("~/.ssh/") is False

    def test_double_star(self):
        assert dc.is_glob_pattern("**/secrets/") is True


class TestGlobToRegex:
    def test_star(self):
        result = dc.glob_to_regex("*.pem")
        assert result == r"[^\s/]*\.pem"

    def test_question_mark(self):
        result = dc.glob_to_regex("file?.txt")
        assert result == r"file[^\s/]\.txt"

    def test_literal(self):
        result = dc.glob_to_regex("hosts")
        assert result == "hosts"

    def test_dot_escaped(self):
        result = dc.glob_to_regex(".env")
        assert result == r"\.env"

    def test_complex_pattern(self):
        result = dc.glob_to_regex(".env.*")
        assert result == r"\.env\.[^\s/]*"


class TestMatchPath:
    # --- Glob patterns ---

    def test_glob_basename_match(self):
        assert dc.match_path("/tmp/server.pem", "*.pem") is True

    def test_glob_basename_no_match(self):
        assert dc.match_path("/tmp/server.txt", "*.pem") is False

    def test_glob_env_match(self):
        assert dc.match_path("/project/.env", ".env") is False  # not a glob
        assert dc.match_path("/project/.env.local", ".env.*") is True

    def test_glob_case_insensitive(self):
        assert dc.match_path("/tmp/Server.PEM", "*.pem") is True

    def test_glob_full_path_match(self):
        # fnmatch matches **/secrets/* against the full path
        assert dc.match_path("/project/secrets/db.yaml", "**/secrets/*") is True

    def test_glob_env_star_local(self):
        assert dc.match_path("/app/.env.production.local", ".env*.local") is True

    def test_glob_credentials_json(self):
        assert dc.match_path("/tmp/gcp-credentials.json", "*-credentials.json") is True

    def test_glob_service_account(self):
        assert (
            dc.match_path("/tmp/myServiceAccount.json", "*serviceAccount*.json") is True
        )

    # --- Prefix patterns ---

    def test_prefix_directory(self):
        assert dc.match_path(f"{HOME}/.ssh/id_rsa", "~/.ssh/") is True

    def test_prefix_directory_nested(self):
        assert dc.match_path(f"{HOME}/.aws/credentials", "~/.aws/") is True

    def test_prefix_no_match(self):
        assert dc.match_path("/tmp/test.py", "~/.ssh/") is False

    def test_prefix_exact_file(self):
        assert dc.match_path(f"{HOME}/.bashrc", "~/.bashrc") is True

    def test_prefix_system_dir(self):
        assert dc.match_path("/etc/hosts", "/etc/") is True

    def test_prefix_system_dir_no_match(self):
        assert dc.match_path("/tmp/file", "/etc/") is False

    def test_prefix_trailing_slash_stripped(self):
        assert dc.match_path("/etc", "/etc/") is True


class TestCheckPathPatterns:
    def test_delete_literal_path(self):
        blocked, reason = dc.check_path_patterns(
            "rm /etc/hosts", "/etc/", dc.DELETE_PATTERNS, "read-only path"
        )
        assert blocked is True
        assert "delete" in reason.lower()

    def test_write_redirect(self):
        blocked, reason = dc.check_path_patterns(
            f"echo foo > {HOME}/.bashrc",
            "~/.bashrc",
            dc.WRITE_PATTERNS,
            "read-only path",
        )
        assert blocked is True

    def test_sed_edit(self):
        blocked, reason = dc.check_path_patterns(
            f"sed -i 's/a/b/' {HOME}/.bashrc",
            "~/.bashrc",
            dc.EDIT_PATTERNS,
            "read-only path",
        )
        assert blocked is True

    def test_chmod_permission(self):
        blocked, reason = dc.check_path_patterns(
            "chmod 644 /etc/hosts", "/etc/", dc.PERMISSION_PATTERNS, "read-only path"
        )
        assert blocked is True

    def test_no_match(self):
        blocked, reason = dc.check_path_patterns(
            "cat /etc/hosts", "/etc/", dc.DELETE_PATTERNS, "read-only path"
        )
        assert blocked is False

    def test_glob_delete_lock_file(self):
        blocked, reason = dc.check_path_patterns(
            "rm package-lock.json", "*.lock", dc.DELETE_PATTERNS, "read-only path"
        )
        # glob pattern matching in commands uses glob_to_regex
        assert (
            blocked is False
        )  # "*.lock" matches "[^\s/]*\.lock" which won't match "package-lock.json" literally
        # This is expected: glob command matching works differently from path matching

    def test_append_pattern(self):
        blocked, reason = dc.check_path_patterns(
            f"echo data >> {HOME}/.bashrc",
            "~/.bashrc",
            dc.APPEND_PATTERNS,
            "read-only path",
        )
        assert blocked is True

    def test_truncate_pattern(self):
        blocked, reason = dc.check_path_patterns(
            f"truncate -s 0 {HOME}/.bashrc",
            "~/.bashrc",
            dc.TRUNCATE_PATTERNS,
            "read-only path",
        )
        assert blocked is True

    def test_move_to_path(self):
        blocked, reason = dc.check_path_patterns(
            f"mv /tmp/evil {HOME}/.bashrc",
            "~/.bashrc",
            dc.MOVE_COPY_PATTERNS,
            "read-only path",
        )
        assert blocked is True
