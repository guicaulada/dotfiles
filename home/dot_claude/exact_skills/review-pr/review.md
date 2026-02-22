---
description: Review a single pull request with comprehensive code analysis and feedback
---

<purpose>
Fetch PR details from GitHub, analyze the changes comprehensively, and provide structured review feedback. Covers logic correctness, security, performance, code quality, and maintainability. Presents findings organized by severity with a clear verdict and actionable suggestions.
</purpose>

<process>

## Step 1: Parse PR Input

Parse the user's input to extract the PR number and optionally the repository.

**URL format** (e.g., `https://github.com/owner/repo/pull/123`):
- Extract `owner/repo` as REPO
- Extract `123` as PR_NUMBER
- Use `-R [REPO]` flag on all subsequent gh commands

**Number format** (e.g., `123`):
- Set PR_NUMBER to the number
- REPO is empty (use current repository)

**Invalid format:**
- Inform user of expected formats and exit

## Step 2: Validate PR and Repository

```bash
gh pr view [PR_NUMBER] [-R REPO] --json number,state
gh repo view [REPO] --json isArchived -q .isArchived
```

- If PR not found: inform user and exit
- If repository is archived: inform user and skip — archived repositories are read-only and PRs cannot be merged
- If closed/merged: note state but continue (review may still be useful)

## Step 3: Fetch PR Details

Run in parallel to gather full context:

```bash
# Comprehensive PR metadata
gh pr view [PR_NUMBER] [-R REPO] --json number,title,state,body,author,baseRefName,headRefName,additions,deletions,changedFiles,createdAt,labels,isDraft

# PR diff
gh pr diff [PR_NUMBER] [-R REPO]

# Commit information
gh pr view [PR_NUMBER] [-R REPO] --json commits

# Files changed with stats
gh pr view [PR_NUMBER] [-R REPO] --json files

# Existing reviews and comments
gh pr view [PR_NUMBER] [-R REPO] --json reviews,comments

# CI status
gh pr checks [PR_NUMBER] [-R REPO] 2>/dev/null || echo "No checks configured"
```

## Step 4: Checkout Repository for Context

Clone the repository to a unique temp directory so subsequent analysis steps can read full file context beyond the diff. This enables checking callers of modified functions, verifying test coverage, and understanding surrounding code.

**4a. Create temp directory and clone:**
```bash
WORK_DIR=$(mktemp -d /tmp/pr-review-XXXXXX)
gh repo clone [REPO] "$WORK_DIR" -- --depth=1 --single-branch
```

**4b. Checkout the PR branch:**
```bash
cd "$WORK_DIR" && gh pr checkout [PR_NUMBER] [-R REPO]
```

Use `$WORK_DIR` as the base path for all file reads, greps, and globs in subsequent steps.

## Step 5: Analyze PR Scope

Assess overall scope and complexity:

- **Size**: additions, deletions, files changed
- **Type**: feature, bugfix, refactor, docs (infer from title/commits)
- **Risk**: breaking changes, security-sensitive, performance-critical

Size classification:
- Small: < 100 lines changed, < 5 files
- Medium: 100-500 lines, 5-15 files
- Large: > 500 lines or > 15 files (flag as potentially needing split)

## Step 6: Review the Diff

For large diffs (>300 lines), first extract and quote the most critical code sections before analyzing. This grounds your review in specific evidence and prevents important details from being overlooked.

Analyze the diff systematically, using the checked-out code in `$WORK_DIR` to read surrounding context when needed:

**6a. Logic and Correctness:**
- Off-by-one errors, null/undefined handling, edge cases
- Incorrect conditional logic, race conditions in async code

**6b. Security Concerns:**
- Input validation gaps, injection risks (SQL, XSS)
- Hardcoded secrets, improper auth, sensitive data exposure

**6c. Performance Issues:**
- N+1 query patterns, unnecessary loops, missing caching
- Large memory allocations, blocking operations

**6d. Code Quality:**
- Unclear naming, excessive complexity, duplication
- Missing error handling, inconsistent patterns

**6e. Maintainability:**
- Tight coupling, missing documentation for public APIs
- Test coverage gaps, breaking changes without migration

For each finding, note:
- File and line number(s)
- Severity: blocking, suggestion, nitpick, question
- Description of the issue
- Suggested fix when applicable

Use Read, Grep, and Glob on `$WORK_DIR` to inspect full files, check callers of modified functions, and verify test coverage for changed code.

## Step 7: Review Commits

- Are commits logical and atomic?
- Do commit messages follow conventions?
- Could commits be squashed or reorganized?

## Step 8: Check Existing Feedback

- Note unresolved discussions
- Avoid duplicating existing feedback
- Check if prior suggestions were addressed

## Step 9: Check CI Status

- Are all checks passing?
- Any failing tests that need attention?
- Coverage changes?

## Step 10: Compile Review

Organize findings by priority:
1. Blocking issues (must fix)
2. Important suggestions (should fix)
3. Minor suggestions (nice to fix)
4. Questions/clarifications
5. Nitpicks (optional)

Determine verdict:

| Condition | Verdict |
|-----------|---------|
| No blocking issues, code is solid | **Approve** |
| Feedback provided, no strong opinion on merge | **Comment** |
| Blocking issues that must be addressed | **Request changes** |

Compose a friendly, professional verdict message that acknowledges the author's work, summarizes key points, and states next steps.

## Step 11: Clean Up Temp Directory

```bash
rm -rf "$WORK_DIR"
```

## Step 12: Present Review

Display the full review using the output format below.

Use AskUserQuestion:
- "How would you like to proceed?"
- Options: "Post as PR comment", "Copy to clipboard", "Done"

## Step 13: Handle Review Posting

If posting to GitHub, use AskUserQuestion to confirm review type:
- Options: "Comment", "Approve", "Request changes"

```bash
gh pr review [PR_NUMBER] [-R REPO] --[comment|approve|request-changes] --body "$(cat <<'EOF'
[REVIEW_CONTENT]
EOF
)"
```

</process>

<output>

```
## PR Review: #[PR_NUMBER]

**[PR_TITLE]**
Author: @[AUTHOR] | Base: [BASE] <- [HEAD]
Size: +[ADDITIONS] -[DELETIONS] across [FILES] files
Status: [STATE] | CI: [CHECKS_STATUS]

---

### Overview

[HIGH_LEVEL_SUMMARY_OF_PR_PURPOSE_AND_CHANGES]

---

### Review Summary

| Severity | Count |
|----------|-------|
| Blocking | [N] |
| Suggestions | [N] |
| Questions | [N] |
| Nitpicks | [N] |

---

### Blocking Issues

[LIST_WITH_FILE:LINE_REFERENCES]

---

### Suggestions

[LIST_WITH_FILE:LINE_REFERENCES]

---

### Questions

[LIST_FOR_AUTHOR]

---

### Nitpicks

[LIST_OF_MINOR_ITEMS]

---

### What's Good

[POSITIVE_FEEDBACK_ON_GOOD_PATTERNS]

---

## Verdict: [APPROVE | COMMENT | REQUEST_CHANGES]

[FRIENDLY_PROFESSIONAL_MESSAGE_TO_AUTHOR]
```

</output>

<rules>
- Run gh commands in parallel where possible to minimize latency
- Reference specific file:line for every finding
- Be constructive — acknowledge good patterns alongside areas for improvement
- Focus on logic and correctness over style preferences
- Provide concrete suggestions, not just criticism
- Ask questions when intent is unclear
- Consider broader context and constraints the author may be working under
- Use HEREDOC when posting review body to preserve formatting
- Never post a review to GitHub without explicit user confirmation
- Always clone to a unique `/tmp/pr-review-XXXXXX` directory for codebase analysis
- Clean up temp directories after analysis completes
</rules>

<examples>

<example>

**Input**: `/review-pr 142`

**Output**:

## PR Review: #142

**fix(auth): handle expired refresh tokens gracefully**
Author: @jsmith | Base: main <- fix/token-refresh
Size: +47 -12 across 3 files
Status: open | CI: passing

---

### Overview

Adds retry logic when refresh tokens expire during API calls. Previously, expired tokens caused a 401 cascade that logged users out. Now the auth middleware detects token expiry, attempts one silent refresh, and only logs out if the refresh itself fails.

---

### Review Summary

| Severity | Count |
|----------|-------|
| Blocking | 0 |
| Suggestions | 2 |
| Questions | 1 |
| Nitpicks | 0 |

---

### Blocking Issues

None

---

### Suggestions

1. **Race condition on concurrent requests** — `src/middleware/auth.ts:34`: If two API calls hit token expiry simultaneously, both will attempt a refresh. Consider a mutex or deduplication flag so only one refresh runs at a time.

2. **Missing test for network failure during refresh** — `tests/auth.test.ts`: Tests cover successful refresh and invalid refresh token, but not the case where the refresh endpoint is unreachable.

---

### Questions

1. **Intentional retry limit?** — `src/middleware/auth.ts:42`: The retry count is hardcoded to 1. Was this intentional, or should it be configurable?

---

### Nitpicks

None

---

### What's Good

- Clean separation of refresh logic into `attemptTokenRefresh`
- Good error messages distinguishing "token expired" from "refresh failed"
- Tests cover the main happy path and primary failure case

---

## Verdict: APPROVE

Solid fix for a real user-facing issue. The race condition suggestion is worth addressing but not blocking — it's an edge case under heavy concurrent load.

</example>

</examples>
