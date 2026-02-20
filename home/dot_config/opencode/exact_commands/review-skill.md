---
description: Review an OpenCode skill against quality and prompt standards
agent: plan
---

Review an existing OpenCode skill and produce actionable findings.

Evaluate structure, OpenCode compatibility, and prompt-engineering quality.

## Workflow

### Step 1: Locate the Skill

Resolve input as skill name or path. Check likely locations:

- `home/dot_config/opencode/exact_skills/{name}/SKILL.md`
- `.opencode/skills/{name}/SKILL.md`
- `~/.config/opencode/skills/{name}/SKILL.md`

If not found, list candidates and ask the user to choose one.

### Step 2: Read All Related Files

Read `SKILL.md` and any supporting files in the same directory.

Build context first; do not review from partial content.

### Step 3: Validate OpenCode Requirements

Check these criteria:

- Frontmatter includes required `name` and `description`
- `name` matches directory and regex `^[a-z0-9]+(-[a-z0-9]+)*$`
- `name` length is 1-64
- `description` length is 1-1024 and specific enough for discovery
- Only recognized frontmatter fields are relied upon

### Step 4: Review Prompt Engineering Quality

Assess whether the skill content:

- Front-loads critical instructions
- Uses explicit, positive directives
- Separates responsibilities into clear steps
- Defines branch conditions and outcomes
- Provides concrete output templates when needed
- Includes error handling for tool failures and ambiguous requests
- Avoids duplicating rules that should live in shared instruction files

### Step 5: Score Findings

Use severity levels:

- `blocking`: violates core structure or causes likely misbehavior
- `suggestion`: meaningful quality improvement
- `nitpick`: minor polish

For every blocking or suggestion finding, include:

- What is wrong (quote or precise reference)
- Why it matters
- Exact fix

### Step 6: Offer Fixes

Ask whether to apply fixes.

If the user confirms, apply minimal edits and re-run the same checks.

## Output Template

```markdown
## Skill Review: [name]

- **Path:** `[path]`
- **Files read:** [count]

### Findings
- **blocking:** [count]
- **suggestion:** [count]
- **nitpick:** [count]

### Details
1. **[severity] [title]**
   - **Evidence:** [file/line or quote]
   - **Impact:** [why this matters]
   - **Fix:** [concrete change]

## Verdict
[ready | needs changes | major rework]
```

$ARGUMENTS
