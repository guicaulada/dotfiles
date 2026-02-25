---
description: Review multiple dependency bump PRs in parallel by spawning deps-reviewer agents and aggregating results
---

<purpose>
Review multiple automated dependency bump pull requests in parallel by spawning deps-reviewer agents, then aggregate all individual reports into a comprehensive dependency review summary. Only reviews automated dependency PRs from bots like Dependabot, Renovate, etc. Use /review-pr for human-created PRs. If no PRs specified, fetches dependency bump PRs requiring your review from GitHub notifications.

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

Filter to unreviewed and bot-authored only:

```bash
ME=$(gh api user --jq '.login')

# Known dependency bot authors
BOT_AUTHORS="dependabot dependabot[bot] renovate renovate[bot] depfu depfu[bot] snyk-bot greenkeeper[bot]"

echo "$ALL_PRS" | jq -c '.[]' | while read pr; do
  REPO=$(echo "$pr" | jq -r '.repository.nameWithOwner')
  NUMBER=$(echo "$pr" | jq -r '.number')

  AUTHOR=$(gh api "repos/$REPO/pulls/$NUMBER" --jq '.user.login' 2>/dev/null)

  # Only include if author is a known dependency bot
  if ! echo "$BOT_AUTHORS" | grep -qw "$AUTHOR"; then
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

Parse arguments to extract PR list (no bot filtering when PRs are explicitly provided):

1. Split on spaces and commas
2. For each item:
   - Full URL: extract repo and PR number
   - `owner/repo#123`: extract repo and PR number
   - Plain number: use current repository

Build a list of `{repo, pr_number, title}` tuples.

## Step 3: Show Review Plan

**From notifications:**

```
Found {N} dependency PRs awaiting your review:

| # | Repository | PR    | Title   | Bot      |
|---|------------|-------|---------|----------|
| 1 | {repo}     | #{pr} | {title} | {author} |
...

Spawning {N} parallel dependency review agents...
```

**From arguments:**

```
Reviewing {N} dependency PRs:
- {repo}#{pr1}
- {repo}#{pr2}
...

Spawning {N} parallel dependency review agents...
```

## Step 4: Spawn Dependency Reviewers in Parallel

For each PR, spawn a deps-reviewer agent using the Task tool. Use a single message with multiple Task calls to run all reviews concurrently.

Prompt template per agent:

```
Review dependency bump PR #{pr_number} in repository {repo}

PR_INPUT: {pr_number or url}
REPO: {repo}

Analyze this dependency update for compatibility and security issues and return a structured review report.
```

Example:

```
Task(prompt="Review dependency bump PR #123 in repository owner/repo...", subagent_type="deps-reviewer", model="sonnet")
Task(prompt="Review dependency bump PR #456 in repository owner/repo...", subagent_type="deps-reviewer", model="sonnet")
```

All agents run concurrently. Task tool blocks until all complete.

## Step 5: Collect Results

Gather all reports from deps-reviewer agents. Parse each to extract:

- PR number and repo
- Packages updated (name, from, to, bump type)
- Verdict (approve/comment/request_changes)
- Security assessment
- Compatibility assessment
- Risk levels

## Step 6: Generate Aggregated Report

Create the summary report using the output format below.

## Step 7: Offer Next Steps

Ask user what they want to do:

- View full report for a specific dependency PR
- Batch approve all low-risk PRs on GitHub
- Post reviews to GitHub
- Export report to file

</process>

<output>

```
## Dependency PR Review Summary

**Reviewed:** [N] dependency PRs
**Source:** [notifications | provided]
**Date:** [TIMESTAMP]

### Overview

| PR                | Repository | Package | From  | To    | Bump   | Verdict   | Risk   |
|-------------------|------------|---------|-------|-------|--------|-----------|--------|
| [#PR_NUMBER](URL) | [REPO]     | [PKG]   | [OLD] | [NEW] | [TYPE] | [VERDICT] | [RISK] |

### Summary by Verdict

- **Approve:** [COUNT] PRs safe to merge
- **Comment:** [COUNT] PRs need review
- **Request Changes:** [COUNT] PRs have issues

### Security Alerts

List each PR with security findings. If none: "No security issues found."

### Compatibility Concerns

List each PR with compatibility issues. If none: "No compatibility issues detected."

### Quick Approvals

PRs that appear safe to merge immediately:

| PR                | Package | Reason   |
|-------------------|---------|----------|
| [#PR_NUMBER](URL) | [PKG]   | [REASON] |

### Needs Attention

PRs requiring manual review or action:

| PR                | Package | Concern   |
|-------------------|---------|-----------|
| [#PR_NUMBER](URL) | [PKG]   | [CONCERN] |

---

### Individual Reports

Include the full report for each PR, separated by horizontal rules.
```

If no dependency PRs found in notifications:

```
No dependency bump PRs found awaiting your review.

Note: Only PRs from known bots (Dependabot, Renovate, etc.) are included.
Use /review-pr for human-created PRs.

To review specific dependency PRs, provide them as arguments:
  /review-deps owner/repo#123 owner/repo#456
  /review-deps https://github.com/owner/repo/pull/123
```

</output>

<rules>

- Only review bot-authored dependency PRs — filter to known bot authors (Dependabot, Renovate, Depfu, Snyk, Greenkeeper)
- Spawn all deps-reviewer agents in parallel using a single message with multiple Task calls
- Use `--paginate` when fetching from GitHub API to get all results
- If a single dependency review fails, include the error in its report section and continue with others
- Never fail the entire batch because one PR errored
- Present the aggregated report before offering next steps
- Use AskUserQuestion to let user choose next action after presenting results
- Before batch approving, show the full list of PRs that would be approved and require explicit user consent

</rules>

<examples>

<example>

**Input**: `/review-deps` (no arguments, from notifications)

**Step 3 output**:

Found 3 dependency PRs awaiting your review:

| # | Repository | PR   | Title                               | Bot             |
|---|------------|------|-------------------------------------|-----------------|
| 1 | acme/api   | #201 | Bump express from 4.18.2 to 4.21.0  | dependabot[bot] |
| 2 | acme/api   | #203 | Bump lodash from 4.17.20 to 4.17.21 | dependabot[bot] |
| 3 | acme/web   | #89  | Bump axios from 1.6.2 to 1.7.4      | dependabot[bot] |

Spawning 3 parallel dependency review agents...

**Step 6 output** (aggregated report):

## Dependency PR Review Summary

**Reviewed:** 3 dependency PRs
**Source:** notifications
**Date:** 2026-02-10

### Overview

| PR                                           | Repository | Package | From    | To      | Bump  | Verdict | Risk   |
|----------------------------------------------|------------|---------|---------|---------|-------|---------|--------|
| [#201](https://github.com/acme/api/pull/201) | acme/api   | express | 4.18.2  | 4.21.0  | minor | Comment | medium |
| [#203](https://github.com/acme/api/pull/203) | acme/api   | lodash  | 4.17.20 | 4.17.21 | patch | Approve | low    |
| [#89](https://github.com/acme/web/pull/89)   | acme/web   | axios   | 1.6.2   | 1.7.4   | minor | Approve | low    |

### Summary by Verdict

- **Approve:** 2 PRs safe to merge
- **Comment:** 1 PR needs review
- **Request Changes:** 0 PRs have issues

### Security Alerts

**[#89](https://github.com/acme/web/pull/89) - axios 1.6.2 -> 1.7.4**

- CVE-2024-39338: SSRF vulnerability fixed in 1.7.4

### Compatibility Concerns

**[#201](https://github.com/acme/api/pull/201) - express 4.18.2 -> 4.21.0**

- Minor version jump spans 3 releases; review changelog for deprecation notices

### Quick Approvals

| PR                                           | Package | Reason                                |
|----------------------------------------------|---------|---------------------------------------|
| [#203](https://github.com/acme/api/pull/203) | lodash  | Patch bump, CI passing, no advisories |
| [#89](https://github.com/acme/web/pull/89)   | axios   | Security fix, minor bump, CI passing  |

### Needs Attention

| PR                                           | Package | Concern                                                   |
|----------------------------------------------|---------|-----------------------------------------------------------|
| [#201](https://github.com/acme/api/pull/201) | express | Minor bump spanning 3 releases, verify deprecation impact |

</example>

</examples>
