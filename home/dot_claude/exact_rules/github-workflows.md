# GitHub Workflows

Workflow files run with elevated privileges and access to secrets. A single compromised action can exfiltrate credentials, tamper with releases, or pivot to production. Treat every workflow change as a security-sensitive operation.

## Action Pinning

- Pin all actions to **full 40-character commit SHAs** — tags are mutable and can be force-pushed by a compromised maintainer
- Add a version comment after the SHA for readability and Dependabot tracking: `uses: actions/checkout@abc123... # v4.2.1`
- Never pin to a major tag (`v4`) or branch (`main`) — these provide no supply chain integrity
- Configure Dependabot or Renovate to automate SHA update PRs

## Version Pinning

- Use **full semver** (`v4.2.1`) when referencing actions in comments — never shorthand (`v4`)
- Full semver tags are still mutable; the SHA is the actual trust anchor
- Pin runtime versions (Node, Python, Go) explicitly — never use `latest` or bare major versions

## Security Hardening

- Set `permissions: {}` at the **workflow level** to revoke all default token permissions
- Declare only the minimum required permissions per job: `contents: read`, `issues: write`, etc.
- Never combine `pull_request_target` with `actions/checkout` of PR code — this is the "pwn request" attack vector
- Use **OIDC** (`id-token: write`) for cloud authentication instead of long-lived stored credentials
- Enable environment protection rules (required reviewers, deployment branches) for production deployments

## Supply Chain Security

- Every `uses:` is a trust decision — third-party actions can read all job secrets and exfiltrate code
- Prefer actions from the `actions/` org when a first-party option exists
- Audit third-party actions before adopting: review source, check maintainer reputation, verify the action is necessary
- Fork critical third-party actions into the org for full control over updates
- Use `actions/attest-build-provenance` for SLSA provenance on build artifacts
- Enforce action allow-lists at the org level when possible

## Injection Prevention

- **Never** interpolate `${{ github.event.* }}` directly in `run:` blocks — attacker-controlled values (PR titles, branch names, commit messages) become shell injection vectors
- Pass untrusted values through `env:` variables or action `with:` inputs instead
- Avoid `fromJSON` on untrusted data
- Treat all external event data as untrusted input

## Linting and Static Analysis

- Validate all workflows with **actionlint** before committing — it catches syntax errors, type mismatches, invalid action inputs, and shell issues
- Audit all workflows with **zizmor** for security issues — it detects unpinned actions, injection risks, excessive permissions, and dangerous triggers
- Integrate both tools into CI and pre-commit hooks
- Upload zizmor SARIF output to GitHub Code Scanning for PR-level feedback

## Workflow Design

- Use `workflow_call` for **reusable workflows** — full pipelines that multiple repos can share
- Use **composite actions** for shared step groups within workflows
- Always set `timeout-minutes` on jobs — the default 6-hour timeout wastes runner minutes on hung jobs
- Use `concurrency` groups with `cancel-in-progress: true` to avoid redundant runs on rapid pushes
- Cache dependencies with `actions/cache` to reduce build times
- Keep workflows focused — split unrelated CI concerns into separate workflow files

## Runner Security

- Use **GitHub-hosted runners** for public repositories — they are ephemeral and isolated
- Never use self-hosted runners for public repositories — any fork can run code on them
- For private repos with self-hosted runners: use ephemeral/JIT runners, container isolation, network restrictions, and runner groups
- Consider StepSecurity Harden-Runner for egress monitoring on sensitive workflows

## Secrets Management

- Never hardcode secrets — use GitHub encrypted secrets at the appropriate scope (org, repo, or environment)
- Declare environment variables at the **step level**, not workflow level, to limit exposure
- Mask sensitive output with `::add-mask::` to prevent accidental log exposure
- Rotate secrets regularly and prefer short-lived OIDC tokens over stored credentials
- Use environments with approval gates for production secrets

## Monitoring and Auditability

- Add `.github/workflows/` to CODEOWNERS requiring review from a security-aware team member
- Enable branch protection with required reviews and status checks for workflow changes
- Run `ossf/scorecard-action` in CI to continuously assess supply chain security posture
- Review workflow run logs for anomalies in duration, network activity, or unexpected failures
