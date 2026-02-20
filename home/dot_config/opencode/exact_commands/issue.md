---
description: Create a GitHub issue by interviewing for details
agent: build
---

Create a well-structured GitHub issue by interviewing the user to gather enough detail for an actionable issue. Discover related issues for context, compose a clear title and body, and create the issue via the `gh` CLI.

## Workflow

### Step 1: Interview the User

Ask targeted questions to understand the issue. Adapt questions to the issue type:

**For bugs:**
- What is the expected behavior?
- What is the actual behavior?
- What are the steps to reproduce?
- What environment is affected? (OS, version, browser)

**For features:**
- What problem does this solve?
- Who benefits from this?
- What does the ideal solution look like?
- Are there constraints or requirements?

**For tasks/chores:**
- What needs to be done?
- Why is this needed now?
- What is the scope?

Ask 2-3 questions at a time. Stop when you have enough detail for an actionable issue.

### Step 2: Discover Related Issues

Search for related context:

```bash
gh issue list --search "RELEVANT_KEYWORDS" --state all --limit 10
```

Check for duplicates or related issues. If a duplicate exists, inform the user and link to it instead of creating a new one.

### Step 3: Determine Labels

Fetch available labels for the repository:

```bash
gh label list --limit 50
```

Select labels that match the issue type and affected area. Use only labels that exist in the repository.

### Step 4: Compose the Issue

Write the title in this format:
```
type: concise summary
```
Keep the title under 72 characters.

Write the body adapted to the issue type:

**Bug report:**
```markdown
## Description
{What is happening and why it is a problem}

## Steps to Reproduce
1. {Step}
2. {Step}

## Expected Behavior
{What should happen}

## Actual Behavior
{What happens instead}

## Environment
- {OS, version, browser, etc.}

## Related
- #{ISSUE_NUMBER} — {brief context}
```

**Feature request:**
```markdown
## Problem
{What problem this solves}

## Proposed Solution
{What the ideal solution looks like}

## Alternatives Considered
{Other approaches and why they were rejected, or "None"}

## Related
- #{ISSUE_NUMBER} — {brief context}
```

Omit empty sections. Keep the body minimal and readable.

### Step 5: Present Draft

Show the complete issue (title, body, labels) to the user for review. Wait for confirmation or edits.

### Step 6: Create Issue

```bash
gh issue create --title "TITLE" --body "$(cat <<'EOF'
...
EOF
)" --label "label1,label2"
```

### Step 7: Return Result

Present the issue URL to the user.

## Error Handling

- If `gh issue create` fails, show the error and suggest fixes (e.g., invalid label, missing permissions).
- If the user describes something too vague, ask for clarification rather than creating a low-quality issue.

$ARGUMENTS
