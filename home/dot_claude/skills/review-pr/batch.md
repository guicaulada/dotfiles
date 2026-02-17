---
description: Review multiple human-created PRs in parallel by spawning pr-reviewer agents and aggregating results
---

<purpose>
Review multiple human-created pull requests in parallel by spawning pr-reviewer agents, then aggregate all individual reports into a comprehensive summary. Excludes automated dependency bump PRs (use /review-deps for those). If no PRs specified, fetches PRs requiring your review from GitHub notifications.

Orchestrator stays lean: parse inputs, spawn agents in parallel, collect results, aggregate.
</purpose>

<process>

## Step 1: Validate gh CLI

```bash
gh auth status 2>&1 | head -1
```

If not authenticated, instruct user to run `gh auth login`.

## Step 2: Parse Input or Fetch from Notifications

**If no arguments provided:**

Fetch all open PRs requesting your review with pagination:

```bash
ALL_PRS=$(gh api --paginate 'search/issues?q=is:pr+is:open+review-requested:@me&per_page=100' --jq '.items[] | {number: .number, title: .title, repository: {nameWithOwner: (.repository_url | split("/") | .[-2:] | join("/"))}}' | jq -s '.')
echo "$ALL_PRS"
```

Filter to unreviewed and human-authored only:

```bash
ME=$(gh api user --jq '.login')

# Known dependency bot authors to exclude
BOT_AUTHORS="dependabot dependabot[bot] renovate renovate[bot] depfu depfu[bot] snyk-bot greenkeeper[bot] imgbot[bot] allcontributors[bot] mergify[bot] codecov[bot] github-actions[bot]"

echo "$ALL_PRS" | jq -c '.[]' | while read pr; do
  REPO=$(echo "$pr" | jq -r '.repository.nameWithOwner')
  NUMBER=$(echo "$pr" | jq -r '.number')

  AUTHOR=$(gh api "repos/$REPO/pulls/$NUMBER" --jq '.user.login' 2>/dev/null)

  # Skip known bots
  if echo "$BOT_AUTHORS" | grep -qw "$AUTHOR"; then
    continue
  fi

  # Skip archived repositories
  IS_ARCHIVED=$(gh repo view "$REPO" --json isArchived -q .isArchived 2>/dev/null)
  if [ "$IS_ARCHIVED" = "true" ]; then
    continue
  fi

  # Skip already reviewed by you
  MY_REVIEWS=$(gh api "repos/$REPO/pulls/$NUMBER/reviews" --jq "[.[] | select(.user.login == \"$ME\")] | length" 2>/dev/null)
  if [ "$MY_REVIEWS" -eq 0 ]; then
    echo "$pr"
  fi
done | jq -s '.'
```

**If arguments provided:**

Parse arguments to extract PR list:
1. Split on spaces and commas
2. For each item:
   - Full URL: extract repo and PR number
   - `owner/repo#123`: extract repo and PR number
   - Plain number: use current repository

Build a list of `{repo, pr_number, title}` tuples.

## Step 3: Show Review Plan

**From notifications:**
```
Found {N} PRs awaiting your review:

| # | Repository | PR | Title |
|---|------------|-----|-------|
| 1 | {repo} | #{pr} | {title} |
...

Spawning {N} parallel review agents...
```

**From arguments:**
```
Reviewing {N} PRs:
- {repo}#{pr1}
- {repo}#{pr2}
...

Spawning {N} parallel review agents...
```

## Step 4: Spawn PR Reviewers in Parallel

For each PR, spawn a pr-reviewer agent using the Task tool. Use a single message with multiple Task calls to run all reviews concurrently.

Prompt template per agent:
```
Review PR #{pr_number} in repository {repo}

PR_INPUT: {pr_number or url}
REPO: {repo}

Analyze this PR and return a structured review report.
```

Example:
```
Task(prompt="Review PR #123 in repository owner/repo...", subagent_type="pr-reviewer", model="sonnet")
Task(prompt="Review PR #456 in repository owner/repo...", subagent_type="pr-reviewer", model="sonnet")
```

All agents run concurrently. Task tool blocks until all complete.

## Step 5: Collect Results

Gather all reports from pr-reviewer agents. Parse each to extract:
- PR number and repo
- Verdict (approve/comment/request_changes)
- Blocking issues count
- Suggestions count
- Questions count
- Risk level
- Quick take

## Step 6: Generate Aggregated Report

Create the summary report using the output format below.

## Step 7: Offer Next Steps

Ask user what they want to do:
- View full report for a specific PR
- Post reviews to GitHub
- Export report to file
- Focus on blockers only

</process>

<output>

```
## PR Review Summary

**Reviewed:** [N] PRs
**Source:** [notifications | provided]
**Date:** [TIMESTAMP]

### Overview

| PR | Repository | Title | Verdict | Blocking | Risk |
|----|------------|-------|---------|----------|------|
| [#PR_NUMBER](URL) | [REPO] | [TITLE] | [VERDICT] | [COUNT] | [RISK] |

### Summary by Verdict

- **Approve:** [COUNT] PRs ready to merge
- **Comment:** [COUNT] PRs need discussion
- **Request Changes:** [COUNT] PRs need work

### Attention Required

#### PRs Needing Changes

List each PR with blocking issues. If none: "No PRs require changes."

#### High Risk PRs

List each high-risk PR with risk type and reason. If none: "No high-risk PRs."

### Quick Takes

| PR | Recommendation |
|----|----------------|
| [#PR_NUMBER](URL) | [QUICK_TAKE] |

---

### Individual Reports

Include the full report for each PR, separated by horizontal rules.
```

If no PRs found in notifications:
```
No human-created PRs found awaiting your review.

Automated dependency bump PRs are excluded. Use /review-deps for those.

To review specific PRs, provide them as arguments:
  /review-pr owner/repo#123 owner/repo#456
  /review-pr https://github.com/owner/repo/pull/123
```

</output>

<rules>
- Only review human-created PRs — exclude bot authors (Dependabot, Renovate, etc.)
- Spawn all pr-reviewer agents in parallel using a single message with multiple Task calls
- Use `--paginate` when fetching from GitHub API to get all results
- If a single PR review fails, include the error in its report section and continue with others
- Never fail the entire batch because one PR errored
- Present the aggregated report before offering next steps
- Use AskUserQuestion to let user choose next action after presenting results
</rules>

<examples>

<example>

**Input**: `/review-pr` (no arguments, from notifications)

**Step 3 output**:

Found 3 PRs awaiting your review:

| # | Repository | PR | Title |
|---|------------|-----|-------|
| 1 | acme/api | #142 | fix(auth): handle expired refresh tokens gracefully |
| 2 | acme/api | #145 | feat(users): add bulk user import endpoint |
| 3 | acme/web | #78 | refactor(nav): extract sidebar into standalone component |

Spawning 3 parallel review agents...

**Step 6 output** (aggregated report):

## PR Review Summary

**Reviewed:** 3 PRs
**Source:** notifications
**Date:** 2026-02-10

### Overview

| PR | Repository | Title | Verdict | Blocking | Risk |
|----|------------|-------|---------|----------|------|
| [#142](https://github.com/acme/api/pull/142) | acme/api | fix(auth): handle expired refresh tokens | Approve | 0 | low |
| [#145](https://github.com/acme/api/pull/145) | acme/api | feat(users): add bulk user import endpoint | Request changes | 2 | high |
| [#78](https://github.com/acme/web/pull/78) | acme/web | refactor(nav): extract sidebar component | Approve | 0 | low |

### Summary by Verdict

- **Approve:** 2 PRs ready to merge
- **Comment:** 0 PRs need discussion
- **Request Changes:** 1 PR needs work

### Attention Required

#### PRs Needing Changes

**[#145](https://github.com/acme/api/pull/145) - feat(users): add bulk user import endpoint**
- Missing input validation on CSV upload allows arbitrary file sizes
- SQL injection risk in dynamic column mapping from CSV headers

#### High Risk PRs

**[#145](https://github.com/acme/api/pull/145) - feat(users): add bulk user import endpoint**
- Risk: security - Unvalidated user input flows directly into database queries

### Quick Takes

| PR | Recommendation |
|----|----------------|
| [#142](https://github.com/acme/api/pull/142) | Solid fix, minor race condition suggestion but not blocking |
| [#145](https://github.com/acme/api/pull/145) | Security issues must be addressed before merge |
| [#78](https://github.com/acme/web/pull/78) | Clean refactor, well-tested, ready to merge |

</example>

</examples>
