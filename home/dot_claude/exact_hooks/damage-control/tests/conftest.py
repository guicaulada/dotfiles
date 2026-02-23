# /// script
# requires-python = ">=3.8"
# dependencies = ["pyyaml", "pytest"]
# ///
"""
Shared test fixtures for damage-control tests.

Run with: uv run pytest tests/ -v
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
