---
name: issue
description: Create GitHub issues by interviewing the user to clarify the problem before submitting. Use when user mentions create issue, new issue, open issue, file issue, report bug, submit issue, github issue, report issue.
allowed-tools: Bash(gh *), Bash(git *)
disable-model-invocation: true
argument-hint: [brief description of the problem]
---

# Issue Skill

Create well-structured GitHub issues by interviewing the user to gather enough detail for an actionable issue. Discovers related issues for context, composes a clear title and body, and opens the issue in browser for final review.

## Issue Title Format

```
<type>: <concise summary>
```

### Rules

- **Title**: Max 72 characters, type prefix when appropriate
- **Body**: Minimal and readable, adapt sections to the issue type
- **Labels**: Use only labels that exist in the target repository
- **Context**: Reference related issues when they provide useful context

## Workflows

### Create Issue

Trigger: "create issue", "new issue", "open issue", "file issue", "report bug", "submit issue"

Read and follow `skills/issue/create.md`.
