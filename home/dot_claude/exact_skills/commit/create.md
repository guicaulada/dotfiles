---
description: Analyze changes and create well-formatted conventional commits
---

<purpose>
Analyze all changes (staged, unstaged, and committed on branch) against the default branch. Determine whether to create a single commit or split into multiple atomic commits. Create properly formatted conventional commits.
</purpose>

<process>

## Step 1: Gather Context

Run in parallel:

- `git remote show origin | grep "HEAD branch" | cut -d: -f2 | xargs` — default branch
- `git status` — current changes
- `git log --oneline -5` — recent commit style
- `git branch --show-current` — current branch

## Step 2: Analyze Changes

Run to understand full scope:

- `git diff --stat` — all uncommitted changes
- `git diff --staged --stat` — staged changes

If on a feature branch:

- `git diff [DEFAULT_BRANCH]...HEAD --stat` — branch commits

If on the default branch:

- Only analyze uncommitted changes

## Step 3: Identify Logical Groups

Analyze changes and group by:

1. **Concern** — Do changes touch different features? (auth + UI = 2 commits)
2. **Type** — Are there different change types? (fix + feat + docs = 3 commits)
3. **Scope** — Do changes affect different areas? (api/ + web/ = 2 commits)
4. **Dependency** — Can changes stand alone? (refactor then feature = 2 commits)

## Step 4: Present Strategy

**Single commit**: Present the commit message, proceed to Step 6.

**Multiple commits**: Present a commit plan:

```
## Commit Plan

Splitting into [N] commits:

### Commit 1: [TYPE]([SCOPE]): [SUBJECT]
Files: [FILE_LIST]
Reason: [WHY_SEPARATE]

### Commit 2: [TYPE]([SCOPE]): [SUBJECT]
Files: [FILE_LIST]
Reason: [WHY_SEPARATE]
```

Ask the user with AskUserQuestion:

- "How would you like to proceed?"
- Options: "Create all commits", "Single commit instead", "Modify plan"

## Step 5: Execute Multi-Commit Plan

For each commit in the plan:

1. Reset staging: `git reset HEAD`
2. Stage specific files: `git add [FILES]`
3. Create commit using HEREDOC:

   ```bash
   git commit -m "$(cat <<'EOF'
   [COMMIT_MESSAGE]
   EOF
   )"
   ```

4. Verify: `git log -1 --oneline`

## Step 6: Create Single Commit

If no staged changes, ask which files to stage via AskUserQuestion.

Determine type, scope, subject, and optional body from the diff. Present the message and confirm with AskUserQuestion before committing.

Create using HEREDOC:

```bash
git commit -m "$(cat <<'EOF'
[COMMIT_MESSAGE]
EOF
)"
```

## Step 7: Verify

Run `git status` to confirm state.
Run `git log --oneline [DEFAULT_BRANCH]..HEAD` to show branch commits.

</process>

<output>

### Single Commit

```
## Commit Created

**Hash**: [SHORT_HASH]
**Message**: [TYPE]([SCOPE]): [SUBJECT]

### Files Changed
[FILE_LIST]

### Next Steps
- Push: `git push`
- Create PR: `gh pr create`
```

### Multiple Commits

```
## Commits Created

| # | Hash   | Message   |
|---|--------|-----------|
| 1 | [HASH] | [MESSAGE] |
| 2 | [HASH] | [MESSAGE] |

### Next Steps
- Review: `git log --oneline [DEFAULT_BRANCH]..HEAD`
- Push: `git push`
- Create PR: `gh pr create`
```

</output>

<rules>
- Always use HEREDOC for commit messages to preserve formatting
- Follow conventional commit format: `type(scope): subject`
- Keep subjects under 50 characters, imperative mood, no trailing period
- Wrap body at 72 characters
- Stage specific files by name for precise control
- Confirm with user before creating any commit
- Present multi-commit plans for review before executing
</rules>

<examples>

<example>

**Input**: User has 2 modified files in `src/auth/` fixing a login redirect bug

**Output**:

## Commit Created

**Hash**: a1b2c3d
**Message**: fix(auth): handle expired session redirect

### Files Changed

- src/auth/middleware.ts (modified)
- src/auth/session.ts (modified)

### Next Steps

- Push: `git push`
- Create PR: `gh pr create`

</example>

<example>

**Input**: User has changes across `api/` (new endpoint) and `docs/` (updated README)

**Commit Plan**:

## Commit Plan

Splitting into 2 commits:

### Commit 1: feat(api): add user preferences endpoint

Files: api/routes/preferences.ts, api/models/preferences.ts
Reason: New feature in a distinct module

### Commit 2: docs(readme): add preferences API usage

Files: docs/README.md
Reason: Documentation is a separate concern from implementation

**Output after execution**:

## Commits Created

| # | Hash    | Message                                  |
|---|---------|------------------------------------------|
| 1 | d4e5f6a | feat(api): add user preferences endpoint |
| 2 | b7c8d9e | docs(readme): add preferences API usage  |

### Next Steps

- Review: `git log --oneline main..HEAD`
- Push: `git push`
- Create PR: `gh pr create`

</example>

</examples>
