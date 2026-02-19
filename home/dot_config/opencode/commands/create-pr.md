---
description: Create a pull request with auto-generated title and description
agent: build
---

Create a well-formatted pull request by analyzing branch commits, discovering related issues and PRs, and generating a title and description. Use conventional commit format for the PR title when appropriate.

## PR Title Format

```
type(scope): summary
```

For PRs with multiple commits of different types, use a descriptive summary that captures the overall change. Keep the title under 72 characters.

## Workflow

### Step 1: Gather Context

Run these commands in parallel:

```bash
git remote show origin
git branch --show-current
git rev-parse --abbrev-ref HEAD@{upstream} 2>/dev/null || echo "no upstream"
git log --oneline $(git rev-parse --abbrev-ref origin/HEAD 2>/dev/null || echo origin/main)..HEAD
git diff $(git rev-parse --abbrev-ref origin/HEAD 2>/dev/null || echo origin/main) --stat
```

Identify the default branch, current branch, and whether the branch tracks a remote.

### Step 2: Analyze Branch Changes

Review the full commit history and diff against the default branch:

```bash
git log --format="%h %s%n%b" DEFAULT_BRANCH..HEAD
git diff DEFAULT_BRANCH
```

Understand the overall purpose: is this a feature, bugfix, refactor, docs update, or chore?

### Step 3: Discover Related Issues and PRs

Search for related context:

```bash
gh issue list --search "RELEVANT_KEYWORDS" --limit 5
gh pr list --search "RELEVANT_KEYWORDS" --limit 5
```

Look for issues that this PR closes or relates to. Extract issue numbers from commit messages and branch names (e.g., `feat/123-user-auth` implies issue #123).

### Step 4: Generate Title and Description

Write the PR title in conventional commit format when the PR has a clear single type. Use a descriptive title when the PR spans multiple types.

Write the PR body using this template:

```markdown
## Summary
{2-4 bullet points explaining what changed and why}

## Changes
{List of key changes, grouped by concern}

## Testing
{How the changes were tested, or "N/A" for docs/chore}

Closes #{ISSUE_NUMBER}
```

Adapt the template to the PR's complexity — small PRs need less detail, large PRs need more. Omit empty sections.

### Step 5: Push and Create PR

Push the branch if it has no upstream:

```bash
git push -u origin BRANCH_NAME
```

Create the PR:

```bash
gh pr create --title "TITLE" --body "$(cat <<'EOF'
## Summary
...
EOF
)"
```

### Step 6: Present Result

Return the PR URL to the user.

## Error Handling

- If `git push` fails, check for upstream conflicts and advise rebasing.
- If `gh pr create` fails because a PR already exists, show the existing PR URL.
- If there are no commits ahead of the default branch, inform the user and stop.

$ARGUMENTS
