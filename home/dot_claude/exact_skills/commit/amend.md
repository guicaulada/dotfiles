---
description: Amend the previous commit with new changes or an updated message
---

<purpose>
Modify the most recent commit by adding staged changes, updating the commit message, or both. Handles safety checks for already-pushed commits.
</purpose>

<process>

## Step 1: Check Current State

Run in parallel:

- `git log -1 --format="%H%n%s%n%b"` — current commit details
- `git status` — staged and unstaged changes
- `git branch -vv` — remote tracking status

## Step 2: Safety Check

If the commit has been pushed to a remote:

- Warn: "This commit has already been pushed. Amending requires a force push."
- Ask with AskUserQuestion: "Continue with amend?"
- Options: "Yes, I understand", "Cancel"
- If "Cancel": exit workflow

## Step 3: Determine Amend Type

Ask with AskUserQuestion:

- "What would you like to amend?"
- Options: "Message only", "Add staged changes", "Both"

## Step 4: Update Message

If amending the message ("Message only" or "Both"):

Show the current message, then ask with AskUserQuestion:

- "How would you like to update the message?"
- Options: "Write new message", "Fix typo", "Add details"

For "Write new message": analyze the commit diff (`git diff HEAD~1`) and propose a new message following conventional commit format.

For "Fix typo" or "Add details": ask what to change.

## Step 5: Stage Changes

If amending with changes ("Add staged changes" or "Both"):

- If no staged changes: ask whether to stage all changes
- If staged changes exist: show what will be added and confirm

## Step 6: Execute Amend

Message only:

```bash
git commit --amend -m "$(cat <<'EOF'
[NEW_MESSAGE]
EOF
)"
```

Changes only (keep message):

```bash
git commit --amend --no-edit
```

Both:

```bash
git commit --amend -m "$(cat <<'EOF'
[NEW_MESSAGE]
EOF
)"
```

## Step 7: Verify

Run `git log -1` to show the amended commit.
Run `git status` to confirm state.

If the original commit was pushed, remind about force push:

```
You'll need to force push: git push --force-with-lease
```

</process>

<output>
```
## Commit Amended

**New Hash**: [NEW_HASH]
**Previous Hash**: [OLD_HASH]
**Message**: [COMMIT_MESSAGE]

### What Changed

- [AMEND_DESCRIPTION]

### Next Steps

[Force push instructions if applicable]

```
</output>

<rules>
- Always warn before amending pushed commits
- Use `--force-with-lease` for safer remote updates
- Confirm with user before executing the amend
- Use HEREDOC for commit messages
- Show before/after comparison of the commit
</rules>

<examples>

<example>

**Input**: User wants to fix a typo in the last commit message. Commit is not pushed.

**Flow**: User selects "Message only" → "Fix typo"

**Output**:

## Commit Amended

**New Hash**: f1a2b3c
**Previous Hash**: d4e5f6a
**Message**: feat(auth): add session timeout handler

### What Changed
- Fixed typo in subject: "timout" → "timeout"

### Next Steps
- Push: `git push`

</example>

<example>

**Input**: User wants to add a forgotten file to the last commit. Commit was already pushed.

**Flow**: Warning about force push → User selects "Yes, I understand" → "Add staged changes"

**Output**:

## Commit Amended

**New Hash**: c9d8e7f
**Previous Hash**: a1b2c3d
**Message**: fix(api): validate request headers

### What Changed
- Added src/api/validators.ts to the commit

### Next Steps
- Force push required: `git push --force-with-lease`

</example>

</examples>
```
