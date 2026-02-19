---
description: Interview the user about a problem, discover related issues, compose a structured issue, and create it via gh CLI
---

<purpose>
Gather enough detail from the user to create a clear, actionable GitHub issue. Interview based on issue type, check for duplicates, compose the issue, and open it in browser for final review.
</purpose>

<process>

## Step 1: Gather Repository Context

Run in parallel:
- `gh repo view --json nameWithOwner -q .nameWithOwner` — get the owner/repo identifier
- `gh label list --limit 50 --json name -q .[].name` — available labels

**If the user specified a different repository:**
- Validate it exists: `gh repo view [REPO] --json nameWithOwner -q .nameWithOwner`
- Fetch labels from target repo: `gh label list --repo [REPO] --limit 50 --json name -q .[].name`

**If the repository cannot be determined:**
- Ask the user with AskUserQuestion to provide one

## Step 2: Classify the Initial Description

Parse the user's initial description to extract:
- **Type**: bug, feat, docs, chore, perf, or refactor
- **Area**: What part of the system is affected
- **Severity signal**: Whether the description suggests urgency (crash, data loss, security)

**If the user provided no description:**
Use AskUserQuestion:
- "What kind of issue would you like to create?"
- Options: "Bug report", "Feature request", "Documentation", "Chore/maintenance"

## Step 3: Interview for Details

Ask targeted follow-up questions using AskUserQuestion based on issue type. Ask one round of focused questions (up to 4). Only ask a second round if critical information is still missing. Skip questions the user already answered in their initial description.

**For bugs:**
1. What is the expected behavior vs. actual behavior?
2. What steps reproduce the problem?
3. What environment details are relevant (OS, version, browser, config)?
4. How severe is the impact (blocks work, workaround exists, cosmetic)?

**For features:**
1. What problem does this solve or what use case does it enable?
2. Who benefits from this feature (users, developers, ops)?
3. Are there constraints or preferences for the implementation approach?
4. What defines "done" — what are the acceptance criteria?

**For docs:**
1. What is missing, incorrect, or unclear in the current documentation?
2. Who is the target audience for this change?
3. Are there specific pages or sections affected?

**For chores/refactors/perf:**
1. What is the current state and what is the desired state?
2. What motivates this change now?
3. Are there risks or dependencies to consider?

## Step 4: Discover Related Issues

**4a. Search for potential duplicates:**
```bash
gh issue list --repo [REPO] --search "[KEY_TERMS]" --state all --limit 5 --json number,title,state
```

**4b. Search for related open issues:**
```bash
gh issue list --repo [REPO] --state open --limit 10 --json number,title,labels
```
Filter by relevance: matching labels, similar keywords in titles.

**If potential duplicates are found:**
Use AskUserQuestion:
- "These existing issues look related. How would you like to proceed?"
- Options: "Create new issue (not a duplicate)", "Add comment to #[N] instead", "Cancel"

If the user chooses to comment, add a comment with the gathered context and stop.

## Step 5: Compose Issue Title

Use the format `[TYPE]: [CONCISE_SUMMARY]` — keep under 72 characters.

Derive the title from the user's description and interview answers. The title should be specific enough to distinguish this issue from others.

## Step 6: Compose Issue Body

Write a minimal, readable issue body. Adapt sections to the issue type. Include only sections with meaningful content.

**Bug:**
```markdown
## Description
[Clear explanation of the bug]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Behavior
[What should happen]

## Actual Behavior
[What happens instead]

## Environment
- [Relevant environment details]

## Acceptance Criteria
- [ ] [Condition that confirms the fix]
```

**Feature:**
```markdown
## Description
[What the feature does and why it matters]

## Use Case
[Who benefits and how]

## Proposed Approach
[Implementation direction, if discussed]

## Acceptance Criteria
- [ ] [Condition 1]
- [ ] [Condition 2]
```

**Docs/chore/refactor/perf:**
```markdown
## Description
[What needs to change and why]

## Current State
[How things are now]

## Desired State
[How things should be after]

## Acceptance Criteria
- [ ] [Condition 1]
```

Match labels from the available labels list to the issue type and content. Reference related issues when they provide useful context.

## Step 7: Present Issue Preview

Display the composed issue:

```
## Issue Preview

**Repository**: [OWNER/REPO]
**Title**: [TITLE]
**Labels**: [LABELS]

**Body**:
[BODY]

### Discovered Context
**Related Issues**: [LIST_OR_NONE]
```

Use AskUserQuestion:
- "How would you like to proceed?"
- Options: "Create issue", "Edit title", "Edit body", "Cancel"

## Step 8: Handle Edits

**If "Edit title":** Ask for the new title, validate length, return to Step 7.

**If "Edit body":** Ask what to modify or provide new body, return to Step 7.

## Step 9: Create Issue

Create the issue using gh CLI:

```bash
gh issue create --repo [REPO] --title "[TITLE]" --body "$(cat <<'EOF'
[BODY]
EOF
)" --label "[LABEL1],[LABEL2]"
```

If labels fail (label does not exist), retry without labels.

Open the created issue in the browser:
```bash
gh issue view [NUMBER] --repo [REPO] --web
```

</process>

<output>

```
## Issue Created

The issue has been opened in your browser for final review.

**Repository**: [OWNER/REPO]
**Issue**: #[NUMBER]
**Title**: [TITLE]
**Labels**: [LABELS]

### Next Steps
- Edit: `gh issue edit [NUMBER]`
- Close: `gh issue close [NUMBER]`
- Assign: `gh issue edit [NUMBER] --add-assignee @me`
```

</output>

<rules>
- Interview the user before creating — gather enough detail for an actionable issue
- Skip questions the user already answered in their initial description
- Limit interview to 2 rounds of AskUserQuestion maximum
- Check for duplicate issues before composing
- Present the full issue preview for user confirmation before creating
- Use only labels that exist in the target repository
- Keep issue titles under 72 characters
- Use HEREDOC for the issue body to preserve formatting
- Default to the current repository; use a different one only when the user specifies it
- Open the created issue in the browser for final review
- Confirm with user via AskUserQuestion before creating the issue
</rules>

<examples>

<example>

**Input**: "There's a bug where the login page crashes when you enter a very long password"

**Interview** (one round):
1. Expected vs. actual? → "Should show validation error, page crashes with white screen"
2. Steps? → "Go to login, paste 500+ chars in password, click submit"
3. Environment? → "Chrome 120, production"
4. Severity? → "Workaround: shorter password, but bad UX"

**Issue Preview**:

## Issue Preview

**Repository**: acme/web-app
**Title**: bug: login page crashes on long password input
**Labels**: bug

**Body**:
## Description
The login page crashes with a white screen when submitting a password longer than 500 characters instead of showing a validation error.

## Steps to Reproduce
1. Navigate to the login page
2. Paste 500+ characters into the password field
3. Click submit

## Expected Behavior
A validation error message indicating the password is too long.

## Actual Behavior
The page crashes and displays a white screen.

## Environment
- Browser: Chrome 120
- Environment: Production

## Acceptance Criteria
- [ ] Long password input shows a validation error instead of crashing

### Discovered Context
**Related Issues**: #198 — "Add input validation to auth forms" (open)

**Final Output**:

## Issue Created

The issue has been opened in your browser for final review.

**Repository**: acme/web-app
**Issue**: #234
**Title**: bug: login page crashes on long password input
**Labels**: bug

### Next Steps
- Edit: `gh issue edit 234`
- Close: `gh issue close 234`
- Assign: `gh issue edit 234 --add-assignee @me`

</example>

<example>

**Input**: "We need dark mode support" (targeting acme/design-system)

**Interview** (one round):
1. What problem? → "Users complain about eye strain at night"
2. Who benefits? → "All end users, especially those working late"
3. Constraints? → "CSS custom properties, system preference detection"
4. Acceptance criteria? → "Toggle in settings, respects OS preference, persists choice"

**Issue Preview**:

## Issue Preview

**Repository**: acme/design-system
**Title**: feat: add dark mode theme support
**Labels**: enhancement

**Body**:
## Description
Add dark mode theme support to reduce eye strain for users working in low-light environments.

## Use Case
All end users benefit, particularly those working late or in dark environments. Users have reported eye strain with the current light-only theme.

## Proposed Approach
Use CSS custom properties for theming. Support system preference detection via `prefers-color-scheme`.

## Acceptance Criteria
- [ ] Dark mode toggle available in user settings
- [ ] Respects OS-level dark mode preference by default
- [ ] User's theme choice persists across sessions

### Discovered Context
**Related Issues**: #72 — "Theming infrastructure for design tokens" (merged)

**Final Output**:

## Issue Created

The issue has been opened in your browser for final review.

**Repository**: acme/design-system
**Issue**: #89
**Title**: feat: add dark mode theme support
**Labels**: enhancement

### Next Steps
- Edit: `gh issue edit 89 --repo acme/design-system`
- Close: `gh issue close 89 --repo acme/design-system`
- Assign: `gh issue edit 89 --repo acme/design-system --add-assignee @me`

</example>

</examples>
