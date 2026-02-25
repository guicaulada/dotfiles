---
description: Analyze branch commits and create a pull request with generated title and description
---

<purpose>
Analyze all commits on the current branch not on the default branch. Discover related issues and PRs for context. Generate an appropriate PR title and description. Open the PR in browser for human review before final submission.
</purpose>

<process>

## Checklist

Copy and track progress:

```
Create PR Progress:
- [ ] Step 1: Gather repository context
- [ ] Step 2: Validate branch state
- [ ] Step 3: Analyze branch commits
- [ ] Step 4: Analyze full diff
- [ ] Step 5: Discover related issues
- [ ] Step 6: Discover related PRs
- [ ] Step 7: Check for uncommitted changes
- [ ] Step 8: Generate PR title
- [ ] Step 9: Generate PR body
- [ ] Step 10: Present PR preview
- [ ] Step 11: Handle edits (if requested)
- [ ] Step 12: Push branch if needed
- [ ] Step 13: Create PR
```

## Step 1: Gather Repository Context

Run in parallel:

- `git remote show origin | grep "HEAD branch" | cut -d: -f2 | xargs` — default branch
- `git branch --show-current` — current branch name
- `git status -sb` — check if branch tracks remote and is up to date

## Step 2: Validate Branch State

**If on default branch:**

- Inform user they need to be on a feature branch
- Exit workflow

**If branch has no remote tracking:**

- Note that branch will need to be pushed
- Continue with analysis

**If branch is behind remote:**

- Warn user about unpushed/unpulled changes
- Ask if they want to continue

## Step 3: Analyze Branch Commits

Run to understand the branch changes:

- `git log [DEFAULT_BRANCH]..HEAD --oneline` — all commits on branch
- `git log [DEFAULT_BRANCH]..HEAD --format="%h %s%n%b%n---"` — full commit messages
- `git log [DEFAULT_BRANCH]..HEAD --stat` — files changed per commit

**If no commits found:**

- Inform user there are no commits to create a PR for
- Exit workflow

## Step 4: Analyze Full Diff

Run to understand the complete scope:

- `git diff [DEFAULT_BRANCH]...HEAD --stat` — summary of all changes
- `git diff [DEFAULT_BRANCH]...HEAD` — full diff for context

## Step 5: Discover Related Issues

**5a. Extract issue references from commits:**

- Parse commit messages for patterns: `#123`, `fixes #123`, `closes #123`, `resolves #123`

**5b. Extract issue numbers from branch name:**

- Parse for patterns: `feat/123-description`, `fix/GH-456`, `issue-789`

**5c. Fetch details for referenced issues:**

```bash
gh issue view [ISSUE_NUMBER] --json number,title,state,labels,body
```

**5d. Search for potentially related issues:**

```bash
gh issue list --state open --limit 10 --json number,title,labels
```

Filter by relevance: matching labels, similar keywords in titles.

## Step 6: Discover Related PRs

**6a. Find PRs linked to the same issues:**

```bash
gh pr list --search "linked:issue:[ISSUE_NUMBER]" --state all --limit 5 --json number,title,state,url
```

**6b. Find PRs that modified the same files:**

```bash
git diff [DEFAULT_BRANCH]...HEAD --name-only
gh pr list --state merged --limit 10 --json number,title,mergedAt
```

For relevant PRs, fetch file details individually:

```bash
gh pr view [NUMBER] --json files
```

Filter to PRs that touched the same significant files (not config/tests).

**6c. Find open PRs to the same base branch:**

```bash
gh pr list --base [DEFAULT_BRANCH] --state open --limit 10 --json number,title,headRefName
```

Check for potential conflicts or overlap.

## Step 7: Check for Uncommitted Changes

Run `git status --porcelain` to check for uncommitted changes.

**If uncommitted changes exist:**
Use AskUserQuestion:

- "You have uncommitted changes. How would you like to proceed?"
- Options: "Continue without them", "Cancel"

## Step 8: Generate PR Title

**Single commit:** Use the commit message as the PR title (if it follows conventional format).

**Multiple commits, same type/scope:** Use `[TYPE]([SCOPE]): [SUMMARY_OF_CHANGES]`

**Multiple commits, different types:** Identify the primary purpose of the branch and use a descriptive title that captures the overall goal.

Title must be max 72 characters, conventional commit format when appropriate.

## Step 9: Generate PR Body

Write a minimal, readable PR body. Adapt to the complexity of the change.

Simple change:

```
Brief description of what changed and why. Closes #123.
```

Moderate change:

```
Description of what this PR accomplishes.

- Key change 1
- Key change 2

Closes #123. Related to #456.
```

Complex change:

```
Overview of the change and motivation.

Key modifications:
- Change 1
- Change 2
- Change 3

Context: This continues the work from #100 and addresses feedback from #456.

Closes #123.
```

Reference discovered issues/PRs when they provide useful context.

## Step 10: Present PR Preview

Display the generated PR:

```
## PR Preview

**Title**: [PR_TITLE]

**Body**:
[PR_BODY]

**Branch**: [CURRENT_BRANCH] -> [DEFAULT_BRANCH]
**Commits**: [N] commit(s)

### Discovered Context
**Referenced Issues**: [LIST_OR_NONE]
**Related Issues**: [LIST_OR_NONE]
**Related PRs**: [LIST_OR_NONE]
```

Use AskUserQuestion:

- "How would you like to proceed?"
- Options: "Open in browser", "Edit title", "Edit body", "Cancel"

## Step 11: Handle Edits

**If "Edit title":** Ask for the new title, validate length, return to Step 10.

**If "Edit body":** Ask what to modify or provide new body, return to Step 10.

## Step 12: Push Branch if Needed

Check if branch needs to be pushed:

- `git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null` — check tracking
- `git status -sb` — check if ahead of remote

**If not pushed or ahead of remote:**
Run `git push -u origin [CURRENT_BRANCH]`

## Step 13: Create PR

Create the PR with the web flag for human review:

```bash
gh pr create --web --title "[PR_TITLE]" --body "$(cat <<'EOF'
[PR_BODY]
EOF
)"
```

</process>

<output>

```
## PR Ready for Review

The PR has been opened in your browser for final review.

**Branch**: [CURRENT_BRANCH] -> [DEFAULT_BRANCH]
**Commits**: [N] commit(s)

### Generated Title
[PR_TITLE]

### Generated Body
[PR_BODY]

### Next Steps
- Review the PR in your browser
- Add reviewers if needed
- Click "Create pull request" when ready
```

</output>

<rules>

- Always use `gh pr create --web` to open in browser for human review
- Use HEREDOC for PR body to preserve formatting
- Follow conventional commit format for titles when appropriate
- Keep PR titles under 72 characters
- Keep PR body minimal — match detail level to change complexity
- Include issue closing keywords when applicable
- Confirm with user via AskUserQuestion before creating PR
- Verify push is needed before pushing
- Use `git push -u origin` with the branch name for safe pushes

</rules>

<examples>

<example>

**Input**: Single commit on branch `fix/login-redirect`, commit message "fix(auth): handle expired session redirect"

**PR Preview**:

## PR Preview

**Title**: fix(auth): handle expired session redirect

**Body**:
Handle the case where an expired session cookie causes an infinite redirect loop on the login page. Now detects stale sessions and clears them before redirecting.

Closes #89.

**Branch**: fix/login-redirect -> main
**Commits**: 1 commit(s)

### Discovered Context

**Referenced Issues**: #89 — "Login page redirect loop with expired session"
**Related Issues**: None
**Related PRs**: #85 (merged) — "feat(auth): add session timeout handler"

**Final Output**:

## PR Ready for Review

The PR has been opened in your browser for final review.

**Branch**: fix/login-redirect -> main
**Commits**: 1 commit(s)

### Generated Title

fix(auth): handle expired session redirect

### Generated Body

Handle the case where an expired session cookie causes an infinite redirect loop on the login page. Now detects stale sessions and clears them before redirecting.

Closes #89.

### Next Steps

- Review the PR in your browser
- Add reviewers if needed
- Click "Create pull request" when ready

</example>

<example>

**Input**: 4 commits on branch `feat/user-preferences`, touching API routes, models, tests, and docs

**PR Preview**:

## PR Preview

**Title**: feat(api): add user preferences endpoint

**Body**:
Add a new `/api/users/:id/preferences` endpoint for reading and updating user display preferences (theme, language, timezone).

Key changes:

- New `preferences` model with validation
- CRUD routes with auth middleware
- Integration tests for all preference operations
- API docs updated with new endpoint

Related to #142. Closes #138.

**Branch**: feat/user-preferences -> main
**Commits**: 4 commit(s)

### Discovered Context

**Referenced Issues**: #138 — "Add user preferences API"
**Related Issues**: #142 — "User settings page frontend" (open)
**Related PRs**: #130 (merged) — "refactor(api): standardize route handlers"

</example>

</examples>
