"""Exercise bootstrap without host Corepack, network access, or real installations."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "home/.chezmoiscripts/run_onchange_after_yarn-berry-activate.sh.tmpl"
)

MISE = """#!/bin/bash
printf '%s\\n' "$*" >> "$HOME/calls"
[[ "$1 $2" == 'exec --' ]] || exit 90
shift 2
case "$*" in
    'corepack --version') [[ "${FAIL_COREPACK:-0}" == 0 ]] ;;
    'corepack enable yarn') [[ "${FAIL_ENABLE:-0}" == 0 ]] ;;
    'corepack prepare yarn@'*' --activate')
    [[ "${FAIL_PREPARE:-0}" == 0 ]] || exit 91
    printf '%s\\n' "${3#yarn@}" > "$HOME/version" ;;
    'yarn --version')
    [[ "$COREPACK_ENABLE_NETWORK" == 0 ]] || exit 92
    [[ "$COREPACK_ENABLE_PROJECT_SPEC" == 0 ]] || exit 93
    if [[ "${WRONG_VERSION:-0}" == 1 ]]; then printf '0.0.0\\n'
    elif [[ -f "$HOME/version" ]]; then /bin/cat "$HOME/version"
    else exit 94
    fi ;;
    *) exit 95 ;;
esac
"""


class YarnBootstrapTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.home = Path(self.temporary.name)
        self.bin = self.home / "bin"
        self.bin.mkdir()
        mise = self.bin / "mise"
        mise.write_text(MISE)
        mise.chmod(0o755)
        self.env = {**os.environ, "HOME": str(self.home), "PATH": str(self.bin)}

    def run_script(self, **overrides):
        return subprocess.run(
            ["/bin/bash", str(SCRIPT)],
            env={**self.env, **overrides},
            capture_output=True,
            text=True,
            check=False,
        )

    def test_bootstraps_without_host_corepack_and_is_idempotent(self):
        first = self.run_script()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertIn("Verified Yarn", first.stdout)
        second = self.run_script()
        self.assertEqual(second.returncode, 0, second.stderr)
        calls = (self.home / "calls").read_text()
        self.assertEqual(calls.count("corepack prepare"), 1)
        self.assertIn("corepack enable yarn", calls)

    def test_missing_mise_fails(self):
        (self.bin / "mise").unlink()
        result = self.run_script()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("mise is required", result.stderr)

    def test_missing_corepack_fails(self):
        result = self.run_script(FAIL_COREPACK="1")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Corepack is unavailable", result.stderr)

    def test_enable_and_download_failures_propagate(self):
        for setting in ("FAIL_ENABLE", "FAIL_PREPARE"):
            with self.subTest(setting=setting):
                self.assertNotEqual(self.run_script(**{setting: "1"}).returncode, 0)

    def test_wrong_version_fails(self):
        result = self.run_script(WRONG_VERSION="1")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("got 0.0.0", result.stderr)


if __name__ == "__main__":
    unittest.main()
