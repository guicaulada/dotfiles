# /// script
# requires-python = ">=3.8"
# dependencies = ["pyyaml", "pytest", "pytest-xdist"]
# ///
"""
Shared test fixtures for damage-control tests.

Run with: uv run pytest tests/ -v -n auto
"""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import damage_control as dc  # noqa: E402, F401

SCRIPT = str(Path(__file__).parent.parent / "damage_control.py")
HOME = str(Path("~").expanduser())


def run_hook(tool_name: str, tool_input: dict) -> tuple:
    """Run the hook via subprocess, returning (exit_code, stdout, stderr)."""
    payload = json.dumps({"tool_name": tool_name, "tool_input": tool_input})
    result = subprocess.run(
        ["uv", "run", SCRIPT],
        input=payload,
        capture_output=True,
        text=True,
        timeout=15,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def assert_allows(tool_name: str, tool_input: dict) -> None:
    """Assert the hook lets the call through with no decision at all."""
    code, stdout, stderr = run_hook(tool_name, tool_input)
    assert code == 0, f"expected allow (exit 0), got {code}: {stderr}"
    assert stdout == "", f"expected no decision output, got: {stdout}"


def assert_asks(tool_name: str, tool_input: dict) -> str:
    """Assert the hook emits an "ask" decision; returns the reason."""
    code, stdout, stderr = run_hook(tool_name, tool_input)
    assert code == 0, f"expected ask (exit 0), got {code}: {stderr}"
    assert stdout, "expected an ask decision on stdout, got nothing"
    decision = json.loads(stdout)["hookSpecificOutput"]
    assert decision["permissionDecision"] == "ask"
    return decision["permissionDecisionReason"]


def assert_blocks(tool_name: str, tool_input: dict) -> str:
    """Assert the hook hard-blocks (exit 2); returns the stderr message."""
    code, stdout, stderr = run_hook(tool_name, tool_input)
    assert code == 2, f"expected block (exit 2), got {code}: {stdout}"
    assert "SECURITY" in stderr
    return stderr
