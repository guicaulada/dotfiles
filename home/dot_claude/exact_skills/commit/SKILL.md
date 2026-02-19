---
name: commit
description: Create well-formatted git commits following conventional commit standards. Use when user mentions commit, create commit, make a commit, amend commit, fix last commit, help me write a commit, conventional commits, or interactive commit.
allowed-tools: Read, Bash(git *)
disable-model-invocation: true
---

# Commit Skill

Create well-formatted git commits following the conventional commit standard. Supports standard commits, amending previous commits, and interactive step-by-step commit building.

## Commit Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Types

| Type | Use for |
|------|---------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation changes only |
| `style` | Formatting, whitespace (no logic change) |
| `refactor` | Code restructuring without behavior change |
| `test` | Adding or updating tests |
| `chore` | Build, tooling, dependency updates |
| `perf` | Performance improvement |

### Rules

- **Subject**: Imperative mood, max 50 characters, no trailing period
- **Body**: Wrap at 72 characters, explain what and why
- **Footer**: Reference issues (`Closes #123`), note breaking changes (`BREAKING CHANGE:`)

## Workflows

### Create Commit

Trigger: "commit", "create commit", "make a commit", "commit changes"

Read and follow `skills/commit/create.md`.

### Amend Commit

Trigger: "amend commit", "fix last commit", "update commit message"

Read and follow `skills/commit/amend.md`.

### Interactive Commit

Trigger: "help me write a commit", "interactive commit", "commit wizard"

Read and follow `skills/commit/interactive.md`.
