---
description: Review dependency bump PRs for compatibility and security
agent: plan
---

Review automated dependency bump pull requests with focus on compatibility and security analysis. Identify version changes, check for CVEs, breaking changes, and migration requirements.

Supports two modes: single PR review and batch review of multiple dependency PRs in parallel.

## Risk Levels

| Level | Criteria |
|-------|----------|
| `critical` | Known security vulnerability, must act immediately |
| `high` | Major version bump with breaking changes, or CI failing |
| `medium` | Major bump without obvious issues, or package health concerns |
| `low` | Patch/minor bump, CI passing, no advisories |

## Verdicts

| Verdict | When to Use |
|---------|-------------|
| **Approve** | Patch/minor bump with no issues, or security fix |
| **Comment** | Major bump needing further review, unclear impact |
| **Request changes** | Known vulnerabilities, breaking changes, CI failures |

## Single PR Review

When given a specific PR number or URL:

1. Spawn the `@deps-reviewer` subagent with the PR number/URL
2. Present the returned report to the user
3. Ask if the user wants to post the review to GitHub

## Batch Review

When asked to review all dependency PRs or no specific PR is given:

### Step 1: List Dependency PRs

```bash
gh pr list --search "author:app/dependabot OR author:app/renovate OR label:dependencies" --json number,title,author --limit 50
```

If no dependency PRs are found, inform the user and stop.

### Step 2: Spawn Parallel Reviews

For each dependency PR, spawn a `@deps-reviewer` subagent with the PR number. Run reviews in parallel for efficiency.

### Step 3: Aggregate Reports

Collect all reports and present a summary table:

```markdown
## Dependency Review Summary

| PR | Package | Bump | Risk | Verdict | Action |
|----|---------|------|------|---------|--------|
| #123 | lodash | 3.x → 4.x | high | comment | Review breaking changes |
| #124 | eslint | 8.50 → 8.51 | low | approve | Safe to merge |

### Critical / Urgent
{List any PRs that need immediate attention, or "None"}

### Recommended Actions
{Ordered list: which PRs to merge first, which need manual review}
```

### Step 4: Ask for Next Steps

Ask the user which PRs to approve, comment on, or request changes for. Post reviews to GitHub only when the user explicitly confirms.

## Error Handling

- If `gh pr list` returns no results, check if the repository uses a different bot or labeling convention.
- If a subagent fails, report the error for that specific PR and continue with the others.

$ARGUMENTS
