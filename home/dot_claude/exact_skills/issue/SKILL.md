---
name: issue
description: Creates GitHub issues by interviewing the user to clarify the problem before submitting. Use when user mentions create issue, new issue, open issue, file issue, report bug, submit issue, github issue, report issue. Do NOT use for viewing, listing, closing, or editing existing issues.
allowed-tools: Bash(gh *)
disable-model-invocation: true
argument-hint: [brief description of the problem]
---

# Issue Skill

Create well-structured GitHub issues by interviewing the user to gather enough detail for an actionable issue. Discovers related issues for context, composes a clear title and body, and opens the issue in browser for final review.

## Workflows

### Create Issue

Trigger: "create issue", "new issue", "open issue", "file issue", "report bug", "submit issue"

Read and follow [create.md](create.md).
