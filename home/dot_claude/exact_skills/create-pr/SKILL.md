---
name: create-pr
description: Creates pull requests with auto-generated titles and descriptions by analyzing branch commits and discovering related issues. Use when user mentions create pr, open pr, make pr, pull request, pr create, submit pr, open pull request, send pr, or push pr. Not for reviewing, merging, or listing existing PRs.
allowed-tools: Read, Bash(git *), Bash(gh *)
disable-model-invocation: true
argument-hint: [branch-name]
---

# Create PR

Create well-formatted pull requests by analyzing branch commits, discovering related issues and PRs, and generating titles and descriptions. Opens PR in browser for human review.

## Workflows

### Create PR

Trigger: "create pr", "open pr", "make pr", "pull request", "pr create", "submit pr"

Read and follow [create.md](create.md).
