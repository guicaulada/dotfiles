---
name: create-pr
description: Creates pull requests with auto-generated titles and descriptions by analyzing branch commits and discovering related issues. Use when user mentions create pr, open pr, make pr, pull request, pr create, submit pr, open pull request, send pr, or push pr.
allowed-tools: Read, Bash(git *), Bash(gh *)
disable-model-invocation: true
argument-hint: [branch-name]
---

# Create PR

Create well-formatted pull requests by analyzing branch commits, discovering related issues and PRs, and generating titles and descriptions. Opens PR in browser for human review.

## PR Title Format

```
<type>(<scope>): <summary>
```

For PRs with multiple commits of different types, use a descriptive summary that captures the overall change.

### Rules

- **Title**: Max 72 characters, conventional commit format when appropriate
- **Body**: Minimal and readable, adapt detail to change complexity
- **Issues**: Include closing keywords (`Closes #123`, `Fixes #456`) when applicable
- **Context**: Reference related issues/PRs when they provide useful context

## Workflows

### Create PR

Trigger: "create pr", "open pr", "make pr", "pull request", "pr create", "submit pr"

Read and follow [create.md](create.md).
