---
description: Create a well-formatted conventional commit
agent: build
---

Create well-formatted git commits following the conventional commit standard defined in the project rules. Support standard commits, amending previous commits, and interactive step-by-step commit building.

The commit format, types, and rules are already defined in the project's git-conventions rule file — follow those conventions exactly.

## Workflow

### Step 1: Gather Context

Run these commands in parallel to understand the current state:

```bash
git remote
git rev-parse --abbrev-ref --symbolic-full-name HEAD@{upstream} 2>/dev/null || echo "no upstream"
git for-each-ref --format='%(refname:short)' refs/remotes/*/HEAD
git status
git log --oneline -10
git branch --show-current
git diff --stat
git diff --staged --stat
```

Resolve a base branch using this priority:

1. HEAD branch of the upstream remote (if `HEAD@{upstream}` exists)
2. HEAD branch of `origin` (if available)
3. Local `main` branch
4. Local `master` branch
5. Ask the user if none of the above are available

Use this resolved value as `BASE_BRANCH`.

### Step 2: Analyze Changes

Compare the current branch against `BASE_BRANCH`:

```bash
git log --oneline BASE_BRANCH..HEAD
git diff BASE_BRANCH --stat
git diff --stat
git diff --staged --stat
```

Classify every change by concern, type, and scope. Determine whether to create a single commit or split into multiple atomic commits. Each commit addresses one logical change.

### Step 3: Present Strategy

Present the commit plan to the user before executing:

- **Single commit**: Show the proposed message
- **Multi-commit plan**: Show ordered list of commits with their messages

Wait for user confirmation before proceeding.

### Step 4: Create Commits

Stage files for each logical group and commit using HEREDOC format for multi-line messages:

```bash
git add <files>
git commit -m "$(cat <<'EOF'
type(scope): subject line

Body explaining what changed and why.
Wrap at 72 characters per line.

Closes #123
EOF
)"
```

### Step 5: Verify

Run `git status` and `git log --oneline -5` to confirm the commits were created correctly. Present the result to the user.

## Amend Commit

When the user asks to amend or fix the last commit:

1. Check if HEAD has been pushed: `git log --oneline @{upstream}..HEAD 2>/dev/null`
2. If pushed, warn the user that amending requires a force push and ask for confirmation
3. Stage changes if needed, then run `git commit --amend`
4. Use `--force-with-lease` for safer remote updates if pushing is needed

## Interactive Commit

When the user asks for help writing a commit, walk through each part step-by-step:

1. Show the list of changed files and ask which to include
2. Ask the user to select a commit type
3. Ask for the scope (or skip)
4. Ask if this is a breaking change
5. Ask for the subject line (enforce max 50 characters)
6. Ask if a body is needed
7. Ask for issue references
8. Preview the full message and confirm

## Error Handling

- If `git commit` fails due to a pre-commit hook, read the hook output, explain the issue, and help the user fix it. Create a new commit after fixing — do not amend.
- If there are no changes to commit, inform the user and stop.
- If the working tree has both staged and unstaged changes, ask the user which to include.
- If no remote exists, continue with a local-base comparison (`main`/`master`) and do not fail.

$ARGUMENTS
