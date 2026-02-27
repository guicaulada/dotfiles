---
description: Guide user through commit creation with interactive questions
---

<purpose>
Walk the user through creating a commit step-by-step using AskUserQuestion at each stage. Helps choose the right type, scope, and message. Ideal for users learning conventional commits or unsure about categorization.
</purpose>

<process>

## Step 1: Check for Changes

Run `git status` and `git diff --staged --stat`.

If nothing is staged, ask with AskUserQuestion:

- "No changes are staged. What would you like to do?"
- Options: "Stage all changes", "Let me stage manually", "Cancel"

## Step 2: Show Changes Summary

Display staged changes:

```
Staged for commit:
- [FILE1] (modified)
- [FILE2] (new file)
- [FILE3] (deleted)
```

## Step 3: Select Commit Type

Ask with AskUserQuestion:

- "What type of change is this?"
- Options: "feat — New feature", "fix — Bug fix", "refactor — Restructuring"

If none fit, follow up with:

- Options: "docs — Documentation", "style — Formatting", "test — Tests", "chore — Maintenance", "perf — Performance"

## Step 4: Define Scope

Analyze staged files and suggest scopes based on file paths.

Ask with AskUserQuestion:

- "What's the scope of this change? (optional)"
- Options: "[SUGGESTED_SCOPE_1]", "[SUGGESTED_SCOPE_2]", "No scope"

## Step 5: Check for Breaking Changes

Ask with AskUserQuestion:

- "Is this a breaking change?"
- Options: "No", "Yes — adds ! and BREAKING CHANGE footer"

## Step 6: Write Subject Line

Analyze the diff and suggest 2-3 subject lines.

Ask with AskUserQuestion:

- "Choose or write the commit subject (max 50 chars):"
- Options: "[SUGGESTION_1]", "[SUGGESTION_2]"

Validate: max 50 characters, imperative mood, no trailing period.

## Step 7: Add Body (Optional)

Ask with AskUserQuestion:

- "Add a commit body to explain what and why?"
- Options: "No body needed", "Yes, add explanation"

If adding a body: collect the content, wrap at 72 characters.

## Step 8: Reference Issues (Optional)

Ask with AskUserQuestion:

- "Reference any issues?"
- Options: "No", "Closes #", "Refs #"

If referencing: ask for the issue number.

## Step 9: Preview and Confirm

Build and display the complete message:

```
[TYPE]([SCOPE])[!]: [SUBJECT]

[BODY]

[BREAKING CHANGE: description]
[Closes #ISSUE]
```

Ask with AskUserQuestion:

- "Create this commit?"
- Options: "Yes, commit", "Edit", "Cancel"

## Step 10: Create Commit

```bash
git commit -m "$(cat <<'EOF'
[FULL_COMMIT_MESSAGE]
EOF
)"
```

Run `git log -1` to show the result.

</process>

<output>
```
## Commit Created

**Type**: [TYPE]
**Scope**: [SCOPE or "none"]
**Breaking**: [YES/NO]

### Message

[FULL_COMMIT_MESSAGE]

### Files Committed

[FILE_LIST]

### Next Steps

- Push: `git push`
- View history: `git log --oneline`

```
</output>

<rules>

- Use AskUserQuestion at every decision point
- Suggest commit types and scopes based on the actual diff
- Validate subject line length (max 50 characters)
- Always preview the full message before committing
- Use HEREDOC for the final commit command
- Provide helpful context at each step for users learning the format

</rules>

<examples>

<example>

**Input**: User has staged `src/components/Button.tsx` (modified)

**Wizard flow**:
1. Type → "fix — Bug fix"
2. Scope → "components"
3. Breaking → "No"
4. Subject → "correct button focus ring on dark mode"
5. Body → "No body needed"
6. Issues → "Closes #89"
7. Preview → User confirms

**Output**:

## Commit Created

**Type**: fix
**Scope**: components
**Breaking**: No

### Message
fix(components): correct button focus ring on dark mode

Closes #89

### Files Committed
- src/components/Button.tsx (modified)

### Next Steps
- Push: `git push`
- View history: `git log --oneline`

</example>

</examples>
