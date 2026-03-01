# /// script
# requires-python = ">=3.8"
# dependencies = ["pyyaml"]
# ///
#
# Based on https://github.com/disler/claude-code-damage-control
# Original work Copyright (c) disler, MIT License
"""
Claude Code Security Firewall - Consolidated Damage Control
============================================================

Single PreToolUse hook handling Bash, Edit, Write, Read, and Grep tools.
Loads patterns from patterns.yaml for easy customization.

Exit codes:
  0 = Allow (or JSON stdout for "ask" decisions)
  2 = Block (stderr message fed back to Claude)
"""

from __future__ import annotations

import fnmatch
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import yaml

# ============================================================================
# PATTERN UTILITIES
# ============================================================================


def is_glob_pattern(pattern: str) -> bool:
    """Check if pattern contains glob wildcards."""
    return "*" in pattern or "?" in pattern or "[" in pattern


def glob_to_regex(glob_pattern: str) -> str:
    """Convert a glob pattern to a regex for matching inside commands."""
    result = ""
    for char in glob_pattern:
        if char == "*":
            result += r"[^\s/]*"
        elif char == "?":
            result += r"[^\s/]"
        elif char in r"\.^$+{}[]|()":
            result += "\\" + char
        else:
            result += char
    return result


def match_path(file_path: str, pattern: str) -> bool:
    """Match a file path against a pattern (glob or prefix)."""
    expanded_pattern = str(Path(pattern).expanduser())
    normalized = os.path.normpath(file_path)
    expanded_normalized = str(Path(normalized).expanduser())

    if is_glob_pattern(pattern):
        basename = Path(expanded_normalized).name
        basename_lower = basename.lower()
        pattern_lower = pattern.lower()
        expanded_pattern_lower = expanded_pattern.lower()

        if fnmatch.fnmatch(basename_lower, expanded_pattern_lower):
            return True
        if fnmatch.fnmatch(basename_lower, pattern_lower):
            return True
        return fnmatch.fnmatch(expanded_normalized.lower(), expanded_pattern_lower)
    if expanded_normalized.startswith(expanded_pattern):
        return True
    return expanded_normalized == expanded_pattern.rstrip("/")


# ============================================================================
# OPERATION PATTERNS (for Bash tool path-based checks)
# ============================================================================

WRITE_PATTERNS = [
    (r">\s*{path}", "write"),
    (r"\btee\s+(?!.*-a).*{path}", "write"),
]

APPEND_PATTERNS = [
    (r">>\s*{path}", "append"),
    (r"\btee\s+-a\s+.*{path}", "append"),
    (r"\btee\s+.*-a.*{path}", "append"),
]

EDIT_PATTERNS = [
    (r"\bsed\s+-i.*{path}", "edit"),
    (r"\bperl\s+-[^\s]*i.*{path}", "edit"),
    (r"\bawk\s+-i\s+inplace.*{path}", "edit"),
]

MOVE_COPY_PATTERNS = [
    (r"\bmv\s+.*\s+{path}", "move"),
    (r"\bcp\s+.*\s+{path}", "copy"),
]

DELETE_PATTERNS = [
    (r"\brm\s+.*{path}", "delete"),
    (r"\bunlink\s+.*{path}", "delete"),
    (r"\brmdir\s+.*{path}", "delete"),
    (r"\bshred\s+.*{path}", "delete"),
]

PERMISSION_PATTERNS = [
    (r"\bchmod\s+.*{path}", "chmod"),
    (r"\bchown\s+.*{path}", "chown"),
    (r"\bchgrp\s+.*{path}", "chgrp"),
]

TRUNCATE_PATTERNS = [
    (r"\btruncate\s+.*{path}", "truncate"),
    (r":\s*>\s*{path}", "truncate"),
]

READ_ONLY_BLOCKED = (
    WRITE_PATTERNS
    + APPEND_PATTERNS
    + EDIT_PATTERNS
    + MOVE_COPY_PATTERNS
    + DELETE_PATTERNS
    + PERMISSION_PATTERNS
    + TRUNCATE_PATTERNS
)

NO_DELETE_BLOCKED = DELETE_PATTERNS


# ============================================================================
# CONFIGURATION
# ============================================================================


def get_patterns_dir() -> Path | None:
    """Get path to patterns/ directory, checking multiple locations."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        project_patterns = (
            Path(project_dir) / ".claude" / "hooks" / "damage-control" / "patterns"
        )
        if project_patterns.is_dir():
            return project_patterns

    script_dir = Path(__file__).parent
    local_patterns = script_dir / "patterns"
    if local_patterns.is_dir():
        return local_patterns

    skill_root = script_dir.parent.parent / "patterns"
    if skill_root.is_dir():
        return skill_root

    return None


def get_config_path() -> Path:
    """Get path to patterns.yaml, checking multiple locations."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        project_config = (
            Path(project_dir) / ".claude" / "hooks" / "damage-control" / "patterns.yaml"
        )
        if project_config.exists():
            return project_config

    script_dir = Path(__file__).parent
    local_config = script_dir / "patterns.yaml"
    if local_config.exists():
        return local_config

    skill_root = script_dir.parent.parent / "patterns.yaml"
    if skill_root.exists():
        return skill_root

    return local_config


_CONFIG_KEYS = ("bashToolPatterns", "zeroAccessPaths", "readOnlyPaths", "noDeletePaths")


def load_patterns_dir(patterns_dir: Path) -> dict[str, Any]:
    """Load and merge all YAML files from a patterns directory."""
    merged: dict[str, list] = {k: [] for k in _CONFIG_KEYS}

    # Sorted paths for deterministic load order; .yaml before .yml
    seen: set[Path] = set()
    files: list[Path] = []
    for ext in ("*.yaml", "*.yml"):
        for p in sorted(patterns_dir.rglob(ext)):
            if p not in seen:
                seen.add(p)
                files.append(p)

    for filepath in files:
        with filepath.open() as f:
            data = yaml.safe_load(f) or {}
        for key in _CONFIG_KEYS:
            items = data.get(key)
            if isinstance(items, list):
                merged[key].extend(items)

    return merged


def load_config() -> dict[str, Any]:
    """Load patterns from patterns/ directory or single YAML file."""
    patterns_dir = get_patterns_dir()
    if patterns_dir is not None:
        return load_patterns_dir(patterns_dir)

    config_path = get_config_path()

    if not config_path.exists():
        print(f"Warning: Config not found at {config_path}", file=sys.stderr)
        return {k: [] for k in _CONFIG_KEYS}

    with config_path.open() as f:
        return yaml.safe_load(f) or {}


# ============================================================================
# BASH TOOL PATH CHECKS
# ============================================================================


def check_path_patterns(
    command: str, path: str, patterns: list[tuple[str, str]], path_type: str
) -> tuple[bool, str]:
    """Check a command against operation patterns for a specific path."""
    if is_glob_pattern(path):
        glob_regex = glob_to_regex(path)
        for pattern_template, operation in patterns:
            try:
                cmd_prefix = pattern_template.replace("{path}", "")
                if cmd_prefix and re.search(
                    cmd_prefix + glob_regex, command, re.IGNORECASE
                ):
                    return True, f"Blocked: {operation} operation on {path_type} {path}"
            except re.error:
                continue
    else:
        expanded = str(Path(path).expanduser())
        escaped_expanded = re.escape(expanded)
        escaped_original = re.escape(path)

        for pattern_template, operation in patterns:
            pattern_expanded = pattern_template.replace("{path}", escaped_expanded)
            pattern_original = pattern_template.replace("{path}", escaped_original)
            try:
                if re.search(pattern_expanded, command) or re.search(
                    pattern_original, command
                ):
                    return True, f"Blocked: {operation} operation on {path_type} {path}"
            except re.error:
                continue

    return False, ""


# ============================================================================
# COMMAND POSITION ANCHORING
# ============================================================================

# Requires the matched command to appear at the start of the command string or
# after a shell separator (; | & && || or subshell open paren).  This prevents
# false positives when command-like words appear inside quoted arguments such as
# git commit messages (e.g. `git commit -m "fix mount point"`).
#
# Patterns that need to match mid-command (redirects, absolute-path overrides)
# can opt out with `match_anywhere: true` in the YAML definition.
_CMD_POSITION_PREFIX = r"(?:^|[;|&(]\s*)"


# ============================================================================
# TOOL HANDLERS
# ============================================================================


def handle_bash(tool_input: dict[str, Any], config: dict[str, Any]) -> None:
    """Handle Bash tool: patterns, zero-access, read-only, no-delete checks."""
    command = tool_input.get("command", "")
    if not command:
        sys.exit(0)

    patterns = config.get("bashToolPatterns", [])
    zero_access_paths = config.get("zeroAccessPaths", [])
    read_only_paths = config.get("readOnlyPaths", [])
    no_delete_paths = config.get("noDeletePaths", [])

    # 1. Check against regex patterns from YAML (may block or ask)
    for item in patterns:
        pattern = item.get("pattern", "")
        reason = item.get("reason", "Blocked by pattern")
        should_ask = item.get("ask", False)

        if not item.get("match_anywhere", False):
            pattern = _CMD_POSITION_PREFIX + pattern

        try:
            if re.search(pattern, command, re.IGNORECASE):
                if should_ask:
                    output = {
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "permissionDecision": "ask",
                            "permissionDecisionReason": reason,
                        }
                    }
                    print(json.dumps(output))
                    sys.exit(0)
                else:
                    _block(f"Blocked: {reason}", command)
        except re.error:
            continue

    # 2. Zero-access paths: block ANY mention
    for zero_path in zero_access_paths:
        if is_glob_pattern(zero_path):
            glob_regex = glob_to_regex(zero_path)
            try:
                if re.search(glob_regex, command, re.IGNORECASE):
                    msg = f"Blocked: zero-access pattern {zero_path}"
                    _block(
                        f"{msg} (no operations allowed)",
                        command,
                    )
            except re.error:
                continue
        else:
            expanded = str(Path(zero_path).expanduser())
            escaped_expanded = re.escape(expanded)
            escaped_original = re.escape(zero_path)
            if re.search(escaped_expanded, command) or re.search(
                escaped_original, command
            ):
                _block(
                    f"Blocked: zero-access path {zero_path} (no operations allowed)",
                    command,
                )

    # 3. Read-only paths: block modifications
    for readonly in read_only_paths:
        blocked, reason = check_path_patterns(
            command, readonly, READ_ONLY_BLOCKED, "read-only path"
        )
        if blocked:
            _block(reason, command)

    # 4. No-delete paths: block deletions only
    for no_delete in no_delete_paths:
        blocked, reason = check_path_patterns(
            command, no_delete, NO_DELETE_BLOCKED, "no-delete path"
        )
        if blocked:
            _block(reason, command)

    sys.exit(0)


def handle_edit(tool_input: dict[str, Any], config: dict[str, Any]) -> None:
    """Handle Edit tool: block zero-access and read-only paths."""
    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    for zero_path in config.get("zeroAccessPaths", []):
        if match_path(file_path, zero_path):
            _block(
                f"Blocked edit to zero-access path {zero_path} (no operations allowed)",
                file_path,
            )

    for readonly in config.get("readOnlyPaths", []):
        if match_path(file_path, readonly):
            _block(f"Blocked edit to read-only path {readonly}", file_path)

    sys.exit(0)


def handle_write(tool_input: dict[str, Any], config: dict[str, Any]) -> None:
    """Handle Write tool: block zero-access and read-only paths."""
    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    for zero_path in config.get("zeroAccessPaths", []):
        if match_path(file_path, zero_path):
            msg = f"Blocked write to zero-access path {zero_path}"
            _block(f"{msg} (no operations allowed)", file_path)

    for readonly in config.get("readOnlyPaths", []):
        if match_path(file_path, readonly):
            _block(f"Blocked write to read-only path {readonly}", file_path)

    sys.exit(0)


def handle_read(tool_input: dict[str, Any], config: dict[str, Any]) -> None:
    """Handle Read tool: block zero-access paths only (reads of read-only are fine)."""
    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    for zero_path in config.get("zeroAccessPaths", []):
        if match_path(file_path, zero_path):
            _block(
                f"Blocked read of zero-access path {zero_path} (no operations allowed)",
                file_path,
            )

    sys.exit(0)


def handle_grep(tool_input: dict[str, Any], config: dict[str, Any]) -> None:
    """Handle Grep tool: block searching in zero-access paths."""
    search_path = tool_input.get("path", "")
    if not search_path:
        sys.exit(0)

    for zero_path in config.get("zeroAccessPaths", []):
        if match_path(search_path, zero_path):
            _block(
                f"Blocked grep in zero-access path {zero_path} (no operations allowed)",
                search_path,
            )

    sys.exit(0)


# ============================================================================
# OUTPUT HELPERS
# ============================================================================


def _block(reason: str, context: str) -> None:
    """Print block message to stderr and exit with code 2."""
    truncated = context[:100] + "..." if len(context) > 100 else context
    print(f"SECURITY: {reason}", file=sys.stderr)
    print(f"Target: {truncated}", file=sys.stderr)
    sys.exit(2)


# ============================================================================
# MAIN DISPATCHER
# ============================================================================

HANDLERS = {
    "Bash": handle_bash,
    "Edit": handle_edit,
    "Write": handle_write,
    "Read": handle_read,
    "Grep": handle_grep,
}


def main() -> None:
    config = load_config()

    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    handler = HANDLERS.get(tool_name)
    if handler:
        handler(tool_input, config)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
