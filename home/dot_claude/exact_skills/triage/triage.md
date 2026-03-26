---
description: Fetches all relevant GitHub activity and produces a prioritized work plan
---

<purpose>
Gather GitHub issues, pull requests, reviews, notifications, and project data for the authenticated user (and optionally specified teammates), analyze their state with full context, and produce a structured, prioritized work plan. User-provided arguments ($ARGUMENTS) supply optional focus areas, teammate usernames, or specific questions to answer.
</purpose>

<process>

## Step 1: Identify Scope

Parse `$ARGUMENTS` for:

- **Teammate usernames** — mentioned by name or with phrases like "also consider work from [username]"
- **Focus areas** — specific questions like "what PRs can I merge?" or "what should I work on first?"
- **Repository filters** — if the user mentions specific repos, scope queries to those

Run in parallel:

```
gh api user --jq '.login'
gh api user/memberships/orgs --jq '[.[] | select(.state == "active") | .organization.login]'
```

Store the username and org list — orgs are needed for project discovery in Step 5.

## Step 2: Fetch GitHub Data

Run all queries in parallel. For each user in scope (authenticated user + any teammates):

**Issues assigned:**

```
gh search issues --assignee=USERNAME --state=open --sort=updated --limit=30 --json repository,title,number,url,labels,updatedAt,state,assignees
```

**Authored PRs:**

```
gh search prs --author=USERNAME --state=open --sort=updated --limit=30 --json repository,title,number,url,labels,updatedAt,state,isDraft
```

**PRs awaiting your review** (authenticated user only):

```
gh search prs --review-requested=USERNAME --state=open --sort=updated --limit=30 --json repository,title,number,url,labels,updatedAt,state,author
```

**PRs and issues where you are mentioned** (authenticated user only):

```
gh search prs --mentions=USERNAME --state=open --sort=updated --limit=20 --json repository,title,number,url,updatedAt,state,author
gh search issues --mentions=USERNAME --state=open --sort=updated --limit=20 --json repository,title,number,url,updatedAt,state,labels
```

**Notifications** (authenticated user only):

```
gh api notifications --jq '[.[] | {reason, subject: .subject.title, type: .subject.type, url: .subject.url, repo: .repository.full_name, updated: .updated_at, unread: .unread}] | sort_by(.updated) | reverse | .[0:20]'
```

Deduplicate across queries — a PR may appear in authored, mentioned, and notifications. Keep the richest version and merge context (e.g., "authored + mentioned in comment").

If any query fails, note the failure and continue with available data.

## Step 3: Enrich PR Data

Enrich **all PRs** in scope — authored PRs, review-requested PRs, and mentioned PRs. Run enrichment queries in parallel across PRs.

### 3a: Fetch Comprehensive PR Details

For each PR, fetch all available REST fields:

```
gh pr view NUMBER --repo OWNER/REPO --json additions,assignees,author,autoMergeRequest,baseRefName,body,changedFiles,closingIssuesReferences,comments,commits,createdAt,deletions,files,headRefName,isDraft,labels,latestReviews,mergeStateStatus,mergeable,milestone,number,projectItems,reactionGroups,reviewDecision,reviewRequests,reviews,state,statusCheckRollup,title,updatedAt,url
```

Then fetch GraphQL-exclusive fields — review threads, per-check details, merge queue state, project field values, and viewer context:

```
gh api graphql -f query='
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: 100) {
        nodes {
          isResolved
          isOutdated
          path
          comments(first: 1) {
            nodes { author { login } body }
          }
        }
      }
      commits(last: 1) {
        nodes {
          commit {
            statusCheckRollup {
              state
              contexts(first: 50) {
                nodes {
                  ... on CheckRun {
                    name
                    conclusion
                    status
                    isRequired
                    detailsUrl
                  }
                  ... on StatusContext {
                    context
                    state
                    targetUrl
                  }
                }
              }
            }
          }
        }
      }
      isInMergeQueue
      mergeQueueEntry { position estimatedTimeToMerge }
      canBeRebased
      viewerLatestReview { state submittedAt }
      viewerLatestReviewRequest { requestedAt }
      projectItems(first: 5) {
        nodes {
          project { title number url }
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2SingleSelectField { name } }
              }
              ... on ProjectV2ItemFieldIterationValue {
                title
                startDate
                duration
                field { ... on ProjectV2IterationField { name } }
              }
              ... on ProjectV2ItemFieldNumberValue {
                number
                field { ... on ProjectV2Field { name } }
              }
              ... on ProjectV2ItemFieldDateValue {
                date
                field { ... on ProjectV2Field { name } }
              }
            }
          }
        }
      }
    }
  }
}' -f owner=OWNER -f repo=REPO -F number=NUMBER
```

### 3b: Analyze Review State

**Stale approval detection:**

1. From `commits`, take the last entry's `committedDate` — this is the most recent push
2. From `reviews`, filter to `state == "APPROVED"`, sort by `submittedAt`, take the last — this is the most recent approval
3. If the latest commit is **after** the latest approval, the approval is **stale**

**Re-review request detection:**

If `reviewRequests` is non-empty, someone has been asked to review (or re-review). Combined with a stale approval, the PR is waiting for a new review cycle.

**Unresolved review threads:**

From the GraphQL `reviewThreads`, count threads where `isResolved == false` and `isOutdated == false`. These are active unresolved discussions that must be addressed.

**Outstanding changes-requested reviews:**

From `reviews`, identify reviewers whose latest review is `CHANGES_REQUESTED` with no subsequent `APPROVED` from the same reviewer.

**Review-requested PRs — viewer context:**

For PRs where the user's review is requested, use `viewerLatestReview` and `viewerLatestReviewRequest` to determine:

- If the user already submitted a review and was re-requested → this is a re-review after new commits
- If `viewerLatestReviewRequest.requestedAt` is available → compute waiting duration
- If the PR has approvals from others but new commits → the author pushed fixes and wants another pass

### 3c: Analyze Merge State

**Conflicts:**

| `mergeable`   | `mergeStateStatus` | Meaning                                      |
|---------------|--------------------|----------------------------------------------|
| `CONFLICTING` | `DIRTY`            | Merge conflicts — must rebase or resolve     |
| `MERGEABLE`   | `BEHIND`           | Behind base branch — may need rebase         |
| `MERGEABLE`   | `BLOCKED`          | Blocked by branch protection rules           |
| `MERGEABLE`   | `UNSTABLE`         | CI failing or required checks not met        |
| `MERGEABLE`   | `CLEAN`            | Ready to merge from merge-state perspective  |
| `UNKNOWN`     | any                | GitHub hasn't computed yet — note as pending |

**Auto-merge:**

If `autoMergeRequest` is non-null, auto-merge is enabled. Note the enabler and when it was enabled. The PR will merge automatically once conditions are met — less manual action required.

**Merge queue:**

If `isInMergeQueue` is true, the PR is already queued. Note the `position` and `estimatedTimeToMerge` from `mergeQueueEntry`. No action needed unless the queue is stuck.

**Rebasability:**

If `canBeRebased` is false and there are conflicts, a manual merge/conflict resolution is required — `git rebase` alone won't work.

### 3d: Analyze CI State

From the GraphQL `statusCheckRollup.contexts`, parse individual checks:

- **Required failing checks**: `isRequired == true` and `conclusion` is not SUCCESS — these block merge
- **Optional failing checks**: `isRequired == false` and failing — note but don't block
- **Pending checks**: `status != "COMPLETED"` — still running, wait before concluding
- **Specific check names**: Surface the names of failing required checks so the user knows what to fix

Classify CI overall:

- `PASSING` — all required checks pass
- `FAILING` — one or more required checks fail (list which ones)
- `PENDING` — required checks still running
- `MIXED` — required checks pass but optional checks fail

### 3e: Analyze Context

**Linked issues:**

From `closingIssuesReferences`, record which issues this PR will close when merged. Cross-reference with the user's assigned issues from Step 2 — if a PR closes an assigned issue, link them in the output.

**Stacked PRs:**

If `baseRefName` is not `main`, `master`, or `develop`, this PR may be stacked on another PR. Search authored PRs for one whose `headRefName` matches this PR's `baseRefName`. If found, the base PR's state affects this one (e.g., base PR has conflicts → this PR is transitively blocked).

**Dependency references:**

Scan the PR `body` for patterns like "depends on #N", "blocked by #N", "requires #N", "after #N", or cross-repo references like "depends on owner/repo#N". Record these as explicit dependencies.

**PR age and velocity:**

From `createdAt` and `updatedAt`, compute:

- How old the PR is (opened X days ago)
- How recently it was updated (last activity X hours ago)
- Whether it's going stale (no activity in >3 days with pending reviews)

**Target branch context:**

If `baseRefName` contains `release`, `hotfix`, or version patterns, the PR has higher urgency — it targets a release.

**Project board context:**

From `projectItems.fieldValues`, extract:

- **Status** (e.g., "In Progress", "In Review", "Ready to Deploy")
- **Priority** (e.g., "P0", "High", "Critical")
- **Iteration** (name, start date, duration — compute if approaching end)
- **Effort/Points** (if available)

### 3f: Classify Each PR

Apply these criteria **in order** — a PR gets the first matching state:

| State                 | Criteria                                                                                                                                |
|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| **In merge queue**    | `isInMergeQueue` is true — already queued, note position                                                                                |
| **Draft**             | `isDraft` is true                                                                                                                       |
| **Has conflicts**     | `mergeable` is CONFLICTING or `mergeStateStatus` is DIRTY                                                                               |
| **Needs re-review**   | Stale approval (commits after approval) OR non-empty `reviewRequests` after approval                                                    |
| **Changes requested** | Latest review from any reviewer is CHANGES_REQUESTED (not superseded by later approval)                                                 |
| **Has failing CI**    | Required checks failing — list the specific failing check names                                                                         |
| **Needs CI**          | Approved (non-stale) but required checks still pending                                                                                  |
| **Blocked**           | `mergeStateStatus` is BLOCKED, or has blocking labels, or depends on unmerged PR                                                        |
| **Ready to merge**    | Approved (non-stale) + all required CI passing + no conflicts + no pending review requests + no unresolved threads + not in merge queue |
| **Needs review**      | No review decision yet, or none of the above apply                                                                                      |

Attach **all applicable secondary signals** as annotations regardless of primary state — a PR can be "needs review" AND "has conflicts" AND "behind base branch". The primary state drives categorization; annotations surface everything the user needs to know.

## Step 4: Enrich Issue Data

For each assigned issue, fetch full details in parallel.

### 4a: Fetch Comprehensive Issue Details

REST fields:

```
gh issue view NUMBER --repo OWNER/REPO --json assignees,author,body,closedByPullRequestsReferences,comments,createdAt,labels,milestone,projectItems,state,title,updatedAt,url
```

GraphQL-exclusive fields — sub-issues, blocking relationships, linked branches, timeline, and project field values:

```
gh api graphql -f query='
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $number) {
      issueType { name }
      subIssuesSummary { completed percentCompleted total }
      linkedBranches(first: 5) {
        nodes { ref { name } }
      }
      timelineItems(itemTypes: [CROSS_REFERENCED_EVENT, CONNECTED_EVENT], first: 20) {
        nodes {
          ... on CrossReferencedEvent {
            willCloseTarget
            source {
              ... on PullRequest {
                number title state url isDraft
                repository { nameWithOwner }
              }
            }
          }
          ... on ConnectedEvent {
            subject {
              ... on PullRequest {
                number title state url
                repository { nameWithOwner }
              }
            }
          }
        }
      }
      projectItems(first: 5) {
        nodes {
          project { title number url }
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2SingleSelectField { name } }
              }
              ... on ProjectV2ItemFieldIterationValue {
                title
                startDate
                duration
                field { ... on ProjectV2IterationField { name } }
              }
              ... on ProjectV2ItemFieldNumberValue {
                number
                field { ... on ProjectV2Field { name } }
              }
              ... on ProjectV2ItemFieldDateValue {
                date
                field { ... on ProjectV2Field { name } }
              }
            }
          }
        }
      }
    }
  }
}' -f owner=OWNER -f repo=REPO -F number=NUMBER
```

### 4b: Analyze Issue State

**Linked PRs:**

Combine `closedByPullRequestsReferences` (REST) and `timelineItems` CROSS_REFERENCED_EVENT where `willCloseTarget == true` and CONNECTED_EVENT (GraphQL). For each linked PR, note its state (open/closed/merged, draft, has conflicts, CI status). If the PR is from Step 3 enrichment, reuse that data.

**Sub-issue progress:**

From `subIssuesSummary`: if `total > 0`, report progress as "X/Y sub-issues complete (Z%)". This gives a progress bar for epic-style issues.

**Task list progress:**

Parse the issue `body` for GitHub task list syntax (`- [ ]` and `- [x]`). Count completed vs total. Report as "X/Y tasks complete" if task lists are present.

**Comment analysis:**

From `comments` (last 5), determine:

- Is the latest comment a question directed at the assignee? → "awaiting your response"
- Has the assignee not commented since the last question? → "unanswered question from [author]"
- Is the issue stale (no comments in >7 days, no linked PR)? → "stale — needs attention or deprioritization"

**Linked branches:**

From `linkedBranches`, check if there's an active branch for this issue. If so, the user has started work even if no PR exists yet.

**Milestone proximity:**

If `milestone` has a `dueOn` date, compute days remaining. Flag issues in milestones due within 7 days.

**Project board context:**

From `projectItems.fieldValues`, extract status, priority, iteration, and effort — same as PR enrichment.

## Step 5: Discover and Fetch Project Data

Project commands require the `read:project` OAuth scope. If any query in this step fails with a permission error, skip project discovery and suggest `gh auth refresh -s read:project` in the output.

### 5a: Collect Known Projects

Gather all unique project references from the `projectItems` fetched in Steps 3 and 4. Record each project's title, number, owner, and URL.

### 5b: Discover Additional Projects

For the authenticated user and each org from Step 1:

```
gh project list --owner @me --format json --limit 20
gh project list --owner ORG --format json --limit 20
```

Filter to non-closed projects. Identify projects not already referenced by fetched items — these may contain assigned work not yet surfaced.

### 5c: Fetch User's Items from Discovered Projects

For each discovered project not already referenced, query for items assigned to the user:

```
gh project item-list PROJECT_NUMBER --owner OWNER --format json --limit 50
```

Filter results to items assigned to the authenticated user that are not in a "Done"/"Closed" status. Cross-reference with items already fetched in Step 2 — only keep items that are **new** (not already in the assigned issues or authored PRs lists).

### 5d: Fetch Field Definitions for Context

For each project in scope, fetch field definitions to understand the project's workflow:

```
gh project field-list PROJECT_NUMBER --owner OWNER --format json
```

Use field definitions to interpret field values — e.g., map "Status: In Review" or "Priority: P0" correctly. Identify iteration/sprint fields and their current iteration boundaries (start date + duration → end date).

### 5e: Identify Sprint Context

From iteration field definitions and current date:

- Determine the **current sprint** for each project
- Compute **days remaining** in the current sprint
- Flag items in the current sprint that are still in early-stage statuses (e.g., "To Do" with 2 days left)
- Identify items from **past sprints** that weren't completed — these are carryover items needing attention

## Step 6: Cross-correlate

Link all data together before prioritization.

### 6a: PR-Issue Linking

For each PR with `closingIssuesReferences`, link it bidirectionally with the corresponding issue. In the output, the issue should note "has PR: REPO#N (state)" and the PR should note "closes: REPO#N".

### 6b: Stacked PR Chains

Identify chains where PR A's `baseRefName` matches PR B's `headRefName`. Build the dependency chain and propagate state: if a base PR has conflicts or failing CI, all PRs stacked on it are transitively blocked.

### 6c: Explicit Dependency Chains

From body-parsed dependency references (Step 3e), build a dependency graph. Identify:

- Items that block the user's work
- Items the user is blocking for others

### 6d: Notification Deduplication

Cross-reference notifications with already-surfaced PRs and issues. For notifications that match an already-enriched item, merge the notification context (reason, read status) into that item's annotation rather than listing it separately. Only keep notifications in the "Notifications Summary" that are **not** already covered by other sections.

### 6e: Mention Deduplication

Cross-reference mention search results with assigned issues, authored PRs, and review-requested PRs. Only surface mentions that are **not** already captured — these represent items where the user is involved but not assigned or a reviewer.

### 6f: Project Context Merge

For each PR and issue that has `projectItems`, attach the project context (status, priority, sprint, effort) as an annotation. If an item appears in multiple projects, include context from all of them.

## Step 7: Analyze and Prioritize

Apply this priority framework, integrating all signals:

1. **Urgent**: PRs ready to merge (unblock deployments and teammates), review requests waiting >1 day, failing required CI on your PRs, PRs with merge conflicts (fix before they diverge further), items flagged P0/Critical in project boards
2. **High**: PRs needing re-review after your commits (reviewer is waiting), items in current sprint approaching deadline, PRs with review feedback to address (unresolved threads/changes requested), blocked PRs you can unblock, issues with milestone due within 7 days
3. **Medium**: Active issues assigned to you, PRs needing review from others (follow up), PRs behind base branch, new unseen mentions, items in current sprint with time remaining, project items in early status
4. **Low**: Draft PRs, backlog issues, informational notifications, items not in any sprint, future sprint items

When project board priority fields exist, integrate them:

- Project priority always overrides the default framework if it's more urgent (e.g., a "P0" backlog issue becomes Urgent)
- Sprint boundaries create implicit deadlines — items due this sprint but in early status escalate

Cross-reference teammate work (if in scope) to identify:

- PRs where you are blocking each other
- Shared issues or overlapping work
- Collaboration opportunities
- Stacked PRs across teammates

If the user asked a specific question in `$ARGUMENTS`, frame the analysis to answer that question directly.

## Step 8: Present the Plan

Output the plan using the structure in `<output>`. Adapt sections based on what data is available — omit empty sections. Lead with the answer to the user's question if they asked one.

</process>

<output>

If the user asked a specific question, lead with a direct answer before the full plan.

```
# Work Triage

## Action Required

### Ready to Merge
- [ ] [REPO]#[NUMBER] — [TITLE] (approved by [REVIEWERS], CI passing, no conflicts)
  - Closes: [REPO]#[ISSUE_NUMBER] | Auto-merge: enabled | Sprint: [NAME] ([N] days left) | Priority: [LEVEL]

### Needs Re-review
- [ ] [REPO]#[NUMBER] — [TITLE] ([N] commits after approval, re-review requested from [REVIEWERS])
  - Failing checks: [CHECK_NAMES] | Conflicts: yes/no | Sprint: [NAME]

### Has Conflicts
- [ ] [REPO]#[NUMBER] — [TITLE] (merge conflicts — [rebase possible / manual resolution needed])
  - [ADDITIONAL CONTEXT: also behind base, stacked on #N which also has conflicts]

### Has Failing CI
- [ ] [REPO]#[NUMBER] — [TITLE] (required checks failing: [CHECK_NAMES])
  - Approved: yes/no | Conflicts: no | [OTHER CONTEXT]

### Reviews Requested
- [ ] [REPO]#[NUMBER] — [TITLE] by [AUTHOR] (+[ADDITIONS]/-[DELETIONS], [N] files, waiting [DURATION])
  - [CONTEXT: first review / re-review after [N] new commits / has conflicts / CI failing: [NAMES]]
  - Closes: [REPO]#[ISSUE_NUMBER] | Sprint: [NAME] | Priority: [LEVEL]

### Address Feedback
- [ ] [REPO]#[NUMBER] — [TITLE] ([REVIEWER] requested changes, [N] unresolved threads)
  - Key threads: [FILE:LINE — brief description of each unresolved thread]

## In Progress

### Your PRs
- [REPO]#[NUMBER] — [TITLE] ([STATE]: [DETAILS])
  - [ALL APPLICABLE: conflicts, stale approval, failing CI ([NAMES]), pending reviewers ([WHO]), behind base, stacked on #N]
  - Closes: [REPO]#[ISSUE_NUMBER] | Sprint: [NAME] | Priority: [LEVEL] | Opened [RELATIVE_TIME]

### Your Issues
- [REPO]#[NUMBER] — [TITLE] ([TYPE], [LABELS], updated [RELATIVE_TIME])
  - [ALL APPLICABLE: linked PR (#N — state), sub-issues (X/Y, Z%), tasks (X/Y), milestone (due [DATE]), unanswered question from [USER], linked branch: [NAME]]
  - Sprint: [NAME] ([N] days left) | Priority: [LEVEL] | Status: [PROJECT_STATUS]

## Mentioned
(Items where you are @mentioned but not assigned or reviewing)
- [REPO]#[NUMBER] — [TITLE] ([TYPE], mentioned [RELATIVE_TIME])

## From Project Boards
(Items assigned to you in projects but not captured above)
- [REPO]#[NUMBER] — [TITLE] ([PROJECT_NAME]: [STATUS], Priority: [LEVEL], Sprint: [NAME])

## Teammate: [USERNAME]
(Only if teammates were specified)

### Their PRs
- [REPO]#[NUMBER] — [TITLE] ([STATE])

### Their Issues
- [REPO]#[NUMBER] — [TITLE]

### Collaboration Points
- [DESCRIPTION of shared work, dependencies, or blocking relationships]

## Suggested Priority Order

1. [FIRST TASK — reason, sprint/deadline context if applicable]
2. [SECOND TASK — reason]
3. [THIRD TASK — reason]
...

## Notifications Summary
- [COUNT] review requests, [COUNT] CI failures, [COUNT] mentions, [COUNT] other
- Unseen: [ITEMS not yet covered in sections above]
```

Omit any section that has no items. Keep the plan scannable — use one line per item with an indented annotation line for additional context. Only include annotation lines when there is meaningful context to add.

</output>

<rules>

- Never mutate GitHub state — this skill is strictly read-only
- Always fetch the authenticated user's username dynamically via `gh api user`
- Run independent `gh` queries in parallel to minimize latency — batch as many concurrent calls as possible across Steps 2, 3, and 4
- If a query fails, note the failure and continue with available data — never abort the whole plan
- If a GraphQL query fails for any PR or issue (rate limits, missing permissions, schema mismatches), fall back to REST-only data for that item and classify using available fields — note reduced confidence when GraphQL-exclusive signals (review threads, check `isRequired`, merge queue state) are unavailable
- Classify every PR into exactly one primary state using the classification table in Step 3f — apply criteria in order, first match wins
- Attach all applicable secondary signals as annotations regardless of primary state
- **The classification table in Step 3f is authoritative** — every condition in the "Ready to merge" row must be satisfied (non-stale approval, no pending review requests, no conflicts, no unresolved threads, all required checks passing). If any condition is violated, the PR is not ready to merge — classify it under the first matching earlier row instead
- Always compare the latest commit timestamp against the latest approval timestamp to detect stale approvals
- Surface blockers explicitly in annotations — do not hide conflicts, stale approvals, failing CI, unresolved threads, or dependency blocks behind a generic state label
- Name specific failing CI checks — "CI failing" alone is not actionable; "CI failing: lint, e2e-tests" is
- When a PR has `autoMergeRequest` enabled, note it — the user may not need to take action
- When a PR is `isInMergeQueue`, note position — the user should not try to merge manually
- Detect stacked PRs via `baseRefName` and propagate blocking state through the chain
- Deduplicate across all data sources — never show the same item in multiple sections without purpose
- Omit empty sections from the output — do not show headers with no items
- If `$ARGUMENTS` contains a specific question, answer it directly before presenting the full plan
- When teammates are specified, clearly separate their work from the user's in the output
- Use relative timestamps (e.g., "2 hours ago", "yesterday") for readability
- Link every issue and PR with its full URL for easy navigation
- Limit notification summary to items not already covered by other sections
- If the user has no open items in a category, skip it — do not say "No items found"
- Integrate project board context (priority, status, sprint) into item annotations when available
- Flag sprint deadline proximity — items in sprints ending within 2 days get escalated

</rules>

<examples>

<example>

**Input**: `/triage`

**Output**:

# Work Triage

## Action Required

### Ready to Merge

- [ ] myorg/api#142 — Add rate limiting middleware (approved by jdoe, CI passing, no conflicts) — <https://github.com/myorg/api/pull/142>
  - Closes: myorg/api#135 | Sprint: Sprint 12 (3 days left) | Priority: High

### Needs Re-review

- [ ] myorg/api#145 — Refactor connection pooling (2 commits after approval, re-review requested from msmith) — <https://github.com/myorg/api/pull/145>
  - Sprint: Sprint 12 (3 days left) | Priority: Medium

### Has Conflicts

- [ ] myorg/web#92 — Update dependency versions (merge conflicts — rebase possible) — <https://github.com/myorg/web/pull/92>

### Has Failing CI

- [ ] myorg/api#148 — Add caching layer (required checks failing: e2e-tests) — <https://github.com/myorg/api/pull/148>
  - Approved by jdoe, no conflicts — fix CI to unblock merge

### Reviews Requested

- [ ] myorg/web#89 — Redesign settings page by alee (+340/-120, 12 files, waiting 2 days) — <https://github.com/myorg/web/pull/89>
  - First review, CI passing, no conflicts | Closes: myorg/web#78 | Sprint: Sprint 12 | Priority: High

## In Progress

### Your PRs

- myorg/api#138 — Fix auth token refresh (needs review, opened 2 days ago) — <https://github.com/myorg/api/pull/138>
  - Pending reviewers: msmith, jdoe | Closes: myorg/api#130

### Your Issues

- myorg/api#130 — Investigate timeout errors on /search endpoint (bug, high-priority, updated yesterday) — <https://github.com/myorg/api/issues/130>
  - Linked PR: myorg/api#138 (needs review) | Tasks: 2/5 complete | Sprint: Sprint 12 | Priority: High

## From Project Boards

- myorg/api#151 — Write migration guide for v2 API (API Roadmap: To Do, Priority: Medium, Sprint: Sprint 12) — <https://github.com/myorg/api/issues/151>

## Suggested Priority Order

1. Merge myorg/api#142 — approved and green, closes #135, sprint ends in 3 days
2. Fix CI on myorg/api#148 — e2e-tests failing, otherwise ready to merge
3. Rebase myorg/web#92 — resolve conflicts before they diverge further
4. Review myorg/web#89 — alee waiting 2 days, sprint item, high priority
5. Push fixes for myorg/api#145 — msmith waiting for re-review, sprint item
6. Investigate myorg/api#130 — high-priority bug, tasks 2/5 complete
7. Follow up on myorg/api#138 — ping msmith and jdoe for review
8. Start myorg/api#151 — sprint item still in To Do

## Notifications Summary

- 1 review request, 1 CI failure, 2 mentions

</example>

<example>

**Input**: `/triage What should I work on first? Also consider work from alee besides my own.`

**Output**:

**Work on merging myorg/api#142 first** — it's approved with passing CI, closes a sprint issue, and the sprint ends in 3 days. After that, review alee's PR myorg/web#89 since they've been waiting 2 days and it's also a sprint item. Note: myorg/api#145 looks approved but has 2 commits pushed after the approval and re-review was requested — don't merge it yet.

# Work Triage

## Action Required

### Ready to Merge

- [ ] myorg/api#142 — Add rate limiting middleware (approved by jdoe, CI passing, no conflicts) — <https://github.com/myorg/api/pull/142>
  - Closes: myorg/api#135 | Sprint: Sprint 12 (3 days left) | Priority: High

### Needs Re-review

- [ ] myorg/api#145 — Refactor connection pooling (2 commits after approval, re-review requested from msmith) — <https://github.com/myorg/api/pull/145>

### Reviews Requested

- [ ] myorg/web#89 — Redesign settings page by alee (+340/-120, 12 files, waiting 2 days) — <https://github.com/myorg/web/pull/89>
  - First review, CI passing, no conflicts | Closes: myorg/web#78 | Sprint: Sprint 12 | Priority: High

### Address Feedback

- [ ] myorg/api#138 — Fix auth token refresh (jdoe requested changes, 2 unresolved threads) — <https://github.com/myorg/api/pull/138>
  - Threads: src/auth.ts:42 — token expiry check, src/auth.ts:87 — error handling

## In Progress

### Your Issues

- myorg/api#130 — Investigate timeout errors (bug, high-priority) — <https://github.com/myorg/api/issues/130>
  - Linked PR: myorg/api#138 (changes requested) | Tasks: 2/5 complete

## Teammate: alee

### Their PRs

- myorg/web#89 — Redesign settings page (needs your review, waiting 2 days) — <https://github.com/myorg/web/pull/89>
- myorg/api#141 — Add pagination to list endpoints (draft, CI passing) — <https://github.com/myorg/api/pull/141>

### Their Issues

- myorg/web#85 — Mobile nav broken on Safari (bug) — <https://github.com/myorg/web/issues/85>
  - Sub-issues: 1/3 complete (33%)

### Collaboration Points

- You are blocking alee on myorg/web#89 — review requested from you 2 days ago
- Both working in myorg/api — coordinate on deployment timing
- myorg/api#141 stacked on myorg/api#138 — alee is blocked until your PR merges

## Suggested Priority Order

1. Merge myorg/api#142 — approved and green, closes sprint issue, sprint ends in 3 days
2. Review myorg/web#89 — unblock alee (waiting 2 days), sprint item, high priority
3. Address feedback on myorg/api#138 — 2 unresolved threads from jdoe, blocks alee's #141
4. Investigate myorg/api#130 — high-priority bug, 2/5 tasks done
5. Check on myorg/api#145 — needs re-review from msmith after your recent push

## Notifications Summary

- 1 review request, 2 mentions

</example>

</examples>
