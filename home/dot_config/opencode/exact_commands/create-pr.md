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
git remote
git branch --show-current
git rev-parse --abbrev-ref --symbolic-full-name HEAD@{upstream} 2>/dev/null || echo "no upstream"
git for-each-ref --format='%(refname:short)' refs/remotes/*/HEAD
git branch --list main master
```

Resolve `BASE_BRANCH` using this priority:

1. HEAD branch of the upstream remote (if `HEAD@{upstream}` exists)
2. HEAD branch of `origin` (if available)
3. Local `main`
4. Local `master`
5. Ask the user when no reliable base is available

Resolve `BASE_REMOTE` using this priority:

1. Upstream remote from `HEAD@{upstream}`
2. `origin` if available
3. Ask the user when no remote is available

Identify `BASE_BRANCH`, `BASE_REMOTE`, current branch, and whether the branch tracks a remote.

### Step 2: Analyze Branch Changes

Review the full commit history and diff against `BASE_BRANCH`:

```bash
git log --format="%h %s%n%b" BASE_BRANCH..HEAD
git diff BASE_BRANCH
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
git push -u BASE_REMOTE BRANCH_NAME
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
- If there are no commits ahead of `BASE_BRANCH`, inform the user and stop.
- If `BASE_BRANCH` cannot be determined from repo state, ask the user for the base branch explicitly before generating the PR.
- If `BASE_REMOTE` cannot be determined from repo state, ask the user which remote to push to.

$ARGUMENTS
