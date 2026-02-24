---
name: review-deps
description: Reviews dependency bump PRs with focus on compatibility and security issues. Use when user mentions review deps, review dependencies, dependency review, check deps, dependency prs, dep bumps, review deps prs, batch dep review.
allowed-tools: Read, Bash(gh *), Bash(mktemp *), Bash(rm -rf /tmp/deps-review-*), Grep, Task, WebSearch
argument-hint: [pr-number or url...]
---

# Review Dependencies Skill

Review automated dependency bump pull requests with focus on compatibility and security analysis. Identifies version changes, checks for CVEs, breaking changes, and migration requirements. Supports both single dependency PR review and batch review of multiple dependency PRs in parallel.

## Risk Levels

| Level      | Description                                                   |
| ---------- | ------------------------------------------------------------- |
| `critical` | Known security vulnerability, must act immediately            |
| `high`     | Major version bump with breaking changes, or CI failing       |
| `medium`   | Major bump without obvious issues, or package health concerns |
| `low`      | Patch/minor bump, CI passing, no advisories                   |

## Review Verdicts

| Verdict             | When to Use                                          |
| ------------------- | ---------------------------------------------------- |
| **Approve**         | Patch/minor bump with no issues, or security fix     |
| **Comment**         | Major bump needing further review, unclear impact    |
| **Request changes** | Known vulnerabilities, breaking changes, CI failures |

## Workflows

### Review Single Dependency PR

Trigger: "review deps", "review dependencies", "dependency review", "check deps", "dependency prs", "dep bumps"

Read and follow [review.md](review.md).

### Batch Review Dependency PRs

Trigger: "review deps prs", "batch dep review", "review dependency prs", "review all dep prs"

Read and follow [batch.md](batch.md).
