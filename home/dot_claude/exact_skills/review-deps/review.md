---
description: Review a single dependency bump PR with focus on compatibility and security analysis
---

<purpose>
Fetch dependency bump PR details from GitHub, analyze version changes for security vulnerabilities and compatibility issues, and provide a structured review focused on whether the dependency update is safe to merge. Covers CVEs, breaking changes, migration requirements, peer dependency conflicts, and CI status. Focus exclusively on security and compatibility — dependency bump PRs are auto-generated.
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
# PR metadata
gh pr view [PR_NUMBER] [-R REPO] --json number,title,state,body,author,baseRefName,headRefName,additions,deletions,changedFiles,createdAt,labels,isDraft

# PR diff
gh pr diff [PR_NUMBER] [-R REPO]

# Files changed
gh pr view [PR_NUMBER] [-R REPO] --json files

# CI status
gh pr checks [PR_NUMBER] [-R REPO] 2>/dev/null || echo "No checks configured"
```

## Step 4: Extract Dependency Changes

From the PR title, body, and diff:

**4a. Identify the package manager and ecosystem:**
- npm/yarn/pnpm (JavaScript): `package.json`, lock files
- pip/poetry (Python): `requirements.txt`, `pyproject.toml`
- go modules: `go.mod`, `go.sum`
- cargo (Rust): `Cargo.toml`, `Cargo.lock`
- maven/gradle (Java): `pom.xml`, `build.gradle`
- bundler (Ruby): `Gemfile`, `Gemfile.lock`
- composer (PHP): `composer.json`, `composer.lock`

**4b. Parse version changes from the diff:**
For each dependency being updated, extract:
- Package name
- Previous version (from removed lines)
- New version (from added lines)
- Bump type: major (X.0.0), minor (0.X.0), or patch (0.0.X)

**4c. Check if it's a grouped update:**
Some bots group multiple dependency updates in one PR. Extract ALL packages being updated.

## Step 5: Research Security

For each dependency being updated:

**5a. Check for CVEs and security advisories:**

```bash
gh api graphql -f query='
  query {
    securityAdvisories(first: 5, orderBy: {field: PUBLISHED_AT, direction: DESC}) {
      nodes {
        summary
        severity
        publishedAt
        vulnerabilities(first: 5, package: "{PACKAGE_NAME}") {
          nodes {
            package { name ecosystem }
            vulnerableVersionRange
            firstPatchedVersion { identifier }
          }
        }
      }
    }
  }
' 2>/dev/null || echo "Could not query security advisories"
```

**5b. Search for security information:**
Use WebSearch to look up:
- `"{package_name}" {new_version} CVE security advisory`
- `"{package_name}" vulnerability {old_version}`

**5c. Check if update IS a security fix:**
- Look for "security", "CVE", "vulnerability", "advisory" in PR body
- Check if the bot labels include security-related tags
- Flag security fixes prominently in the report

## Step 6: Research Compatibility

**6a. For major version bumps, search for:**
- Migration guides: `"{package_name}" migration guide {old_major} to {new_major}`
- Breaking changes: `"{package_name}" {new_version} breaking changes changelog`
- Release notes: `"{package_name}" {new_version} release notes`

**6b. For minor/patch bumps, check:**
- Any unexpected breaking changes reported
- Known regressions in the new version

**6c. Analyze the diff for red flags:**
- Lock file changes that seem disproportionate to the update
- Unexpected transitive dependency changes
- Peer dependency warnings in bot's PR description

## Step 7: Checkout Repository for Impact Assessment

Clone the repository to a unique temp directory for codebase analysis. This ensures the user's working directory is unaffected and avoids conflicts when reviewing PRs from different repos.

**7a. Create temp directory and clone:**
```bash
WORK_DIR=$(mktemp -d /tmp/deps-review-XXXXXX)
gh repo clone [REPO] "$WORK_DIR" -- --depth=1 --single-branch
```

**7b. Find usage of the dependency:**
Use Grep to search for imports/requires of the package across the cloned codebase in `$WORK_DIR`.

**7c. Check if any changed APIs are used:**
Cross-reference any breaking changes found in Step 6 with actual usage in the codebase.

**7d. Clean up temp directory:**
```bash
rm -rf "$WORK_DIR"
```

## Step 8: Check CI Status

Review the CI/checks status:
- Are all checks passing?
- Any test failures related to the dependency?
- Did the bot run compatibility tests?

## Step 9: Determine Verdict

| Condition | Verdict |
|-----------|---------|
| Patch update, no issues, CI passing | **Approve** |
| Minor update, backward-compatible, CI passing | **Approve** |
| Security fix (any bump type) | **Approve** (urgent) |
| Major update, no obvious breaking changes in project | **Comment** |
| Major update, needs investigation | **Comment** |
| Known vulnerability in new version | **Request changes** |
| Breaking changes affecting project code | **Request changes** |
| CI failing | **Request changes** |
| Suspicious lock file changes | **Request changes** |

## Step 10: Present Review

Display the full review using the output format below.

Use AskUserQuestion:
- "How would you like to proceed with this dependency review?"
- Options: "Post as PR comment", "Approve on GitHub", "Request changes on GitHub", "Done"

## Step 11: Handle Review Posting

If posting to GitHub:

```bash
gh pr review [PR_NUMBER] [-R REPO] --[comment|approve|request-changes] --body "$(cat <<'EOF'
[REVIEW_CONTENT]
EOF
)"
```

</process>

<output>

```
## Dependency Review: #[PR_NUMBER]

**[PR_TITLE]**
Author: @[AUTHOR] ([BOT_NAME])
CI: [CHECKS_STATUS]

---

### Dependencies Updated

| Package | From | To | Bump | Risk |
|---------|------|----|------|------|
| [PKG] | [OLD] | [NEW] | [major/minor/patch] | [low/medium/high/critical] |

---

### Security Assessment

**CVEs Fixed by This Update:**
[LIST_OF_CVES_OR_NONE]

**New Vulnerabilities Introduced:**
[LIST_OR_NONE]

**Security Advisories:**
[RELEVANT_ADVISORIES_OR_NONE]

---

### Compatibility Assessment

**Breaking Changes:**
[LIST_OF_BREAKING_CHANGES_AFFECTING_PROJECT_OR_NONE]

**Deprecated APIs Used by Project:**
[LIST_OR_NONE]

**Peer Dependency Conflicts:**
[LIST_OR_NONE]

**Migration Required:**
[YES_WITH_DETAILS_OR_NO]

---

### CI Status

[SUMMARY_OF_CI_RESULTS]

---

### Risk Assessment

- **Security:** [none|low|medium|high|critical] - [reason]
- **Compatibility:** [none|low|medium|high] - [reason]
- **Scope:** [none|low|medium|high] - [how much of the codebase uses this]

---

## Verdict: [APPROVE | COMMENT | REQUEST_CHANGES]

[CLEAR_RECOMMENDATION_WITH_REASONING]
```

</output>

<examples>

<example>

**Input**: `/review-deps 89`

**Output**:

## Dependency Review: #89

**Bump axios from 1.6.2 to 1.7.4**
Author: @dependabot[bot] (Dependabot)
CI: passing

---

### Dependencies Updated

| Package | From | To | Bump | Risk |
|---------|------|----|------|------|
| axios | 1.6.2 | 1.7.4 | minor | low |

---

### Security Assessment

**CVEs Fixed by This Update:**
- CVE-2024-39338: SSRF vulnerability in axios <= 1.7.3 where relative URL paths could bypass proxy configuration. Fixed in 1.7.4.

**New Vulnerabilities Introduced:**
None

**Security Advisories:**
- GitHub Advisory GHSA-wf5p-g6vw-rhxx (Moderate)

---

### Compatibility Assessment

**Breaking Changes:**
None detected — minor version bump with backward-compatible additions.

**Deprecated APIs Used by Project:**
None detected

**Peer Dependency Conflicts:**
None

**Migration Required:**
No

---

### CI Status

All 23 checks passing.

---

### Risk Assessment

- **Security:** medium - Fixes known SSRF vulnerability (CVE-2024-39338)
- **Compatibility:** none - Minor bump, no breaking changes
- **Scope:** high - axios is used in 14 files across the codebase (primary HTTP client)

---

## Verdict: APPROVE

Security fix for a known SSRF vulnerability. Minor version bump with no breaking changes and all CI passing. Recommend merging promptly.

</example>

</examples>

<rules>
- Focus on security and compatibility, not code style — dependency bump PRs are auto-generated
- Run gh commands in parallel where possible to minimize latency
- Use WebSearch to research changelogs, CVEs, and breaking changes
- Flag urgent security fixes prominently
- For major bumps, explain the risk even if approving
- Be clear about whether it's safe to merge
- Use HEREDOC when posting review body to preserve formatting
- Never post a review to GitHub without explicit user confirmation
- Always clone to a unique `/tmp/deps-review-XXXXXX` directory for codebase analysis
- Clean up temp directories after analysis completes
</rules>
