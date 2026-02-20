---
description: Review an OpenCode command for workflow and prompt quality
agent: plan
---

Review a custom OpenCode command and report concrete improvements.

Evaluate command metadata, workflow completeness, and prompt clarity.

## Workflow

### Step 1: Locate the Command

Resolve input as command name or file path. Check likely locations:

- `home/dot_config/opencode/exact_commands/{name}.md`
- `.opencode/commands/{name}.md`
- `~/.config/opencode/commands/{name}.md`

If input resolves to a directory, treat it as batch mode:

- List all `*.md` command files in that directory
- Exclude non-command files
- Review each command independently, then produce an aggregate summary

If no target is provided, list available commands and ask the user to choose.

### Step 2: Read the Full Command File(s)

Read frontmatter and body before assessing anything.

- Single mode: read one command file
- Batch mode: read every matched command file completely before scoring

### Step 3: Validate OpenCode Command Conventions

Check:

- `description` exists and matches actual behavior
- Optional fields (`agent`, `model`, `subtask`) are justified
- File name is a sensible slash command name
- Command does not accidentally override built-in commands
- Argument placeholders are used correctly (`$ARGUMENTS`, `$1`, `$2`, ...)
- File references (`@path`) and shell injections (`` !`cmd` ``) are used intentionally

### Step 4: Review Prompt Engineering Quality

Assess whether the command body:

- Starts with core instructions
- Uses concrete, actionable steps
- Defines decisions with explicit conditions
- Includes error handling for failed commands and missing input
- Shows expected output shape for structured responses
- Keeps scope focused to one user-facing action

### Step 5: Score Findings

Use severity levels:

- `blocking`: likely failure, unsafe behavior, or invalid structure
- `suggestion`: substantial quality or reliability improvement
- `nitpick`: minor readability or style improvement

For each blocking or suggestion item, provide evidence, impact, and a specific fix.

For batch mode, include both:

- Per-command finding counts
- Aggregate totals across all reviewed commands

### Step 6: Offer Fixes

Ask whether to apply fixes.

If confirmed, apply minimal edits and re-run validation.

## Output Template

```markdown
## Command Review: [name]

- **Path:** `[path]`

### Findings
- **blocking:** [count]
- **suggestion:** [count]
- **nitpick:** [count]

### Details
1. **[severity] [title]**
   - **Evidence:** [quote or file reference]
   - **Impact:** [why this matters]
   - **Fix:** [specific update]

## Verdict
[ready | needs changes | major rework]
```

In batch mode, repeat the command section per file and append:

```markdown
## Aggregate Summary

- **Commands reviewed:** [count]
- **blocking:** [total]
- **suggestion:** [total]
- **nitpick:** [total]
```

$ARGUMENTS
