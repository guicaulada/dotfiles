---
name: review-pr
description: Review pull requests with detailed code analysis and feedback. Use when user mentions review pr, pr review, review pull request, check pr, analyze pr, code review, review prs, batch review.
allowed-tools: Read, Bash(gh *), Bash(git *), Bash(mktemp *), Bash(rm -rf /tmp/pr-review-*), Grep, Glob, Task
disable-model-invocation: true
argument-hint: [pr-number or url...]
---

# Review PR Skill

Review pull requests with comprehensive code analysis. Fetches PR details, analyzes diffs, examines commits, and provides structured feedback with actionable suggestions. Supports both single PR review and batch review of multiple PRs in parallel.

## Severity Levels

| Level | Description |
|-------|-------------|
| `blocking` | Must be addressed before merge |
| `suggestion` | Recommended improvement |
| `nitpick` | Minor style or preference |
| `question` | Clarification needed from author |

## Review Verdicts

| Verdict | When to Use |
|---------|-------------|
| **Approve** | No blocking issues, code is ready to merge |
| **Comment** | Feedback provided, no explicit approval or change request |
| **Request changes** | Blocking issues that must be addressed before merge |

## Workflows

### Review Single PR

Trigger: "review pr", "pr review", "review pull request", "check pr", "analyze pr", "code review"

Read and follow `skills/review-pr/review.md`.

### Batch Review PRs

Trigger: "review prs", "batch review", "review multiple prs", "review all prs"

Read and follow `skills/review-pr/batch.md`.
