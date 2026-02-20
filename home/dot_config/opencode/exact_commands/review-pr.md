---
description: Review pull requests with detailed code analysis
agent: plan
---

Review pull requests with comprehensive code analysis. Fetch PR details, analyze diffs, examine commits, and provide structured feedback with actionable suggestions.

Supports two modes: single PR review and batch review of multiple PRs in parallel.

## Severity Levels

| Level | Description |
|-------|-------------|
| `blocking` | Must be addressed before merge |
| `suggestion` | Recommended improvement |
| `nitpick` | Minor style or preference |
| `question` | Clarification needed from author |

## Verdicts

| Verdict | When to Use |
|---------|-------------|
| **Approve** | No blocking issues, code is ready to merge |
| **Comment** | Feedback provided, no explicit approval or change request |
| **Request changes** | Blocking issues that must be addressed before merge |

## Single PR Review

When given a specific PR number or URL:

1. Spawn the `@pr-reviewer` subagent with the PR number/URL
2. Present the returned report to the user
3. Ask if the user wants to post the review to GitHub

## Batch Review

When asked to review multiple PRs or no specific PR is given:

### Step 1: List PRs

```bash
gh pr list --json number,title,author,labels,isDraft --limit 20
```

If no open PRs are found, inform the user and stop.

Present the list and ask the user which PRs to review (or review all).

### Step 2: Spawn Parallel Reviews

For each selected PR, spawn a `@pr-reviewer` subagent with the PR number. Run reviews in parallel for efficiency.

### Step 3: Aggregate Reports

Collect all reports and present a summary table:

```markdown
## PR Review Summary

| PR | Title | Size | Verdict | Key Issues |
|----|-------|------|---------|------------|
| #42 | feat: add auth | +350 -20 | comment | 2 suggestions, 1 question |
| #43 | fix: null check | +5 -2 | approve | None |

### Blocking Issues
{List any PRs with blocking issues, or "None"}

### Recommended Actions
{Ordered list: which PRs are ready to merge, which need changes}
```

### Step 4: Ask for Next Steps

Ask the user which PRs to approve, comment on, or request changes for. Post reviews to GitHub only when the user explicitly confirms.

## Draft PRs

Flag draft PRs in the output but still review them. Draft status indicates work-in-progress — provide feedback but note that the author may already be aware of gaps.

## Error Handling

- If a subagent fails, report the error for that specific PR and continue with the others.
- If the PR has been merged or closed since listing, skip it and note the status change.

$ARGUMENTS
