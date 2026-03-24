---
description: Fetches all relevant GitHub activity and produces a prioritized work plan
---

<purpose>
Gather GitHub issues, pull requests, reviews, notifications, and project data for the authenticated user (and optionally specified teammates), analyze their state, and produce a structured, prioritized work plan. User-provided arguments ($ARGUMENTS) supply optional focus areas, teammate usernames, or specific questions to answer.
</purpose>

<process>

## Step 1: Identify Scope

Parse `$ARGUMENTS` for:

- **Teammate usernames** — mentioned by name or with phrases like "also consider work from [username]"
- **Focus areas** — specific questions like "what PRs can I merge?" or "what should I work on first?"
- **Repository filters** — if the user mentions specific repos, scope queries to those

Get the authenticated user's GitHub username:

```
gh api user --jq '.login'
```

## Step 2: Fetch GitHub Data

Run all queries in parallel. For each user in scope (authenticated user + any teammates):

**Issues assigned:**

```
gh search issues --assignee=USERNAME --state=open --sort=updated --limit=30 --json repository,title,number,url,labels,updatedAt,state,assignees
```

**Authored PRs:**

```
gh search prs --author=USERNAME --state=open --sort=updated --limit=30 --json repository,title,number,url,labels,updatedAt,state,reviewDecision,isDraft,additions,deletions
```

**PRs awaiting your review** (authenticated user only):

```
gh search prs --review-requested=USERNAME --state=open --sort=updated --limit=30 --json repository,title,number,url,labels,updatedAt,state,author,additions,deletions
```

**Notifications** (authenticated user only):

```
gh api notifications --jq '[.[] | {reason, subject: .subject.title, type: .subject.type, url: .subject.url, repo: .repository.full_name, updated: .updated_at}] | sort_by(.updated) | reverse | .[0:20]'
```

If any query fails, note the failure and continue with available data.

## Step 3: Enrich PR Data

For each non-draft authored PR, fetch merge readiness details in parallel:

```
gh pr view NUMBER --repo OWNER/REPO --json mergeable,reviewDecision,statusCheckRollup,reviews,comments,labels
```

Classify each PR:

| State              | Criteria                                                   |
|--------------------|------------------------------------------------------------|
| **Ready to merge** | Approved + CI passing + no conflicts                       |
| **Needs CI**       | Approved but checks pending or failing                     |
| **Needs review**   | No review decision yet or changes requested                |
| **Draft**          | Marked as draft                                            |
| **Blocked**        | Has conflicts, failing required checks, or blocking labels |

## Step 4: Check Project Context

For each issue and PR, note the repository. If issues reference a GitHub Project (via labels, milestones, or the issue body), fetch project context:

```
gh project item-list PROJECT_NUMBER --owner OWNER --limit=50 --format=json
```

Use project data to identify:

- Sprint/iteration deadlines
- Priority fields or status columns
- Items that are overdue or approaching deadline

If no project data is available, skip this step.

## Step 5: Analyze and Prioritize

Apply this priority framework:

1. **Urgent**: PRs ready to merge (unblock others), review requests from teammates, failing CI on your PRs
2. **High**: Issues with approaching deadlines, PRs with review feedback to address, blocked PRs you can unblock
3. **Medium**: Active issues assigned to you, PRs needing review from others, new notifications
4. **Low**: Draft PRs, backlog issues, informational notifications

Cross-reference teammate work (if in scope) to identify:

- PRs where you are blocking each other
- Shared issues or overlapping work
- Collaboration opportunities

If the user asked a specific question in `$ARGUMENTS`, frame the analysis to answer that question directly.

## Step 6: Present the Plan

Output the plan using the structure in `<output>`. Adapt sections based on what data is available — omit empty sections. Lead with the answer to the user's question if they asked one.

</process>

<output>

If the user asked a specific question, lead with a direct answer before the full plan.

```
# Work Triage

## Action Required

### Ready to Merge
- [ ] [REPO]#[NUMBER] — [TITLE] ([APPROVED], [CI STATUS])

### Reviews Requested
- [ ] [REPO]#[NUMBER] — [TITLE] by [AUTHOR] (+[ADDITIONS]/-[DELETIONS])

### Address Feedback
- [ ] [REPO]#[NUMBER] — [TITLE] ([REVIEWER] requested changes)

## In Progress

### Your PRs
- [REPO]#[NUMBER] — [TITLE] ([STATE]: [DETAILS])

### Your Issues
- [REPO]#[NUMBER] — [TITLE] ([LABELS], updated [RELATIVE_TIME])

## Teammate: [USERNAME]
(Only if teammates were specified)

### Their PRs
- [REPO]#[NUMBER] — [TITLE] ([STATE])

### Their Issues
- [REPO]#[NUMBER] — [TITLE]

### Collaboration Points
- [DESCRIPTION of shared work or dependencies]

## Suggested Priority Order

1. [FIRST TASK — reason it's urgent]
2. [SECOND TASK — reason]
3. [THIRD TASK — reason]
...

## Notifications Summary
- [COUNT] review requests, [COUNT] CI failures, [COUNT] mentions, [COUNT] other
```

Omit any section that has no items. Keep the plan scannable — use one line per item.

</output>

<rules>

- Never mutate GitHub state — this skill is strictly read-only
- Always fetch the authenticated user's username dynamically via `gh api user`
- Run independent `gh` queries in parallel to minimize latency
- If a query fails, note the failure and continue with available data — never abort the whole plan
- Classify every PR into exactly one state: ready to merge, needs CI, needs review, draft, or blocked
- Omit empty sections from the output — do not show headers with no items
- If `$ARGUMENTS` contains a specific question, answer it directly before presenting the full plan
- When teammates are specified, clearly separate their work from the user's in the output
- Use relative timestamps (e.g., "2 hours ago", "yesterday") for readability
- Link every issue and PR with its full URL for easy navigation
- Limit notification summary to unread/recent — do not dump the full notification feed
- If the user has no open items in a category, skip it — do not say "No items found"

</rules>

<examples>

<example>

**Input**: `/triage`

**Output**:

# Work Triage

## Action Required

### Ready to Merge

- [ ] myorg/api#142 — Add rate limiting middleware (approved, CI passing) — <https://github.com/myorg/api/pull/142>

### Reviews Requested

- [ ] myorg/web#89 — Redesign settings page by iainlane (+340/-120) — <https://github.com/myorg/web/pull/89>

## In Progress

### Your PRs

- myorg/api#138 — Fix auth token refresh (needs review, opened 2 days ago) — <https://github.com/myorg/api/pull/138>

### Your Issues

- myorg/api#130 — Investigate timeout errors on /search endpoint (bug, high-priority, updated yesterday) — <https://github.com/myorg/api/issues/130>

## Suggested Priority Order

1. Merge myorg/api#142 — approved and green, unblocks deployment
2. Review myorg/web#89 — iainlane is waiting on you
3. Investigate myorg/api#130 — high-priority bug, updated yesterday
4. Follow up on myorg/api#138 — ping reviewers if no response today

## Notifications Summary

- 1 review request, 1 CI passing, 2 mentions

</example>

<example>

**Input**: `/triage What should I work on first? Also consider work from iainlane besides my own.`

**Output**:

**Work on merging myorg/api#142 first** — it's approved with passing CI and unblocks the next deployment. After that, review iainlane's PR myorg/web#89 since they're waiting on you.

# Work Triage

## Action Required

### Ready to Merge

- [ ] myorg/api#142 — Add rate limiting middleware (approved, CI passing) — <https://github.com/myorg/api/pull/142>

### Reviews Requested

- [ ] myorg/web#89 — Redesign settings page by iainlane (+340/-120) — <https://github.com/myorg/web/pull/89>

## In Progress

### Your PRs

- myorg/api#138 — Fix auth token refresh (needs review) — <https://github.com/myorg/api/pull/138>

### Your Issues

- myorg/api#130 — Investigate timeout errors (bug, high-priority) — <https://github.com/myorg/api/issues/130>

## Teammate: iainlane

### Their PRs

- myorg/web#89 — Redesign settings page (needs your review) — <https://github.com/myorg/web/pull/89>
- myorg/api#141 — Add pagination to list endpoints (needs CI, draft) — <https://github.com/myorg/api/pull/141>

### Their Issues

- myorg/web#85 — Mobile nav broken on Safari (bug) — <https://github.com/myorg/web/issues/85>

### Collaboration Points

- You are blocking iainlane on myorg/web#89 — review requested from you
- Both working in myorg/api — coordinate on deployment timing

## Suggested Priority Order

1. Merge myorg/api#142 — approved and green, unblocks deployment
2. Review myorg/web#89 — unblock iainlane
3. Investigate myorg/api#130 — high-priority bug
4. Follow up on myorg/api#138 — ping reviewers

## Notifications Summary

- 1 review request, 2 mentions

</example>

</examples>
