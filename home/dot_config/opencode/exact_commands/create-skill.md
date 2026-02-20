---
description: Create an OpenCode skill with best-practice structure
agent: build
---

Create a new OpenCode skill that is easy for agents to discover and safe to use.

Base all decisions on current OpenCode conventions for skills, commands, and prompt design.

## Workflow

### Step 1: Clarify the Request

Ask focused questions to capture:

- What capability the skill should provide
- When the skill should load automatically
- Expected inputs and outputs
- Whether the workflow is read-only or can cause side effects

Ask 2-4 questions at a time and stop once requirements are clear.

### Step 2: Confirm Artifact Choice

Apply this decision rule:

- Choose a command when the behavior is one explicit `/name` action
- Choose a skill when the knowledge should be reusable across multiple contexts

If the request is command-shaped, recommend `/create-command` before continuing. If the user still wants a skill, continue.

### Step 3: Choose Target Path

Write the skill in the correct location:

- In this dotfiles repo: `home/dot_config/opencode/exact_skills/{name}/SKILL.md`
- In a regular project: `.opencode/skills/{name}/SKILL.md`
- In global config: `~/.config/opencode/skills/{name}/SKILL.md`

Derive `{name}` from the purpose and enforce:

- Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`
- 1-64 characters
- Directory name matches frontmatter `name`

### Step 4: Build Frontmatter

Create frontmatter with recognized fields:

- Required: `name`, `description`
- Optional: `license`, `compatibility`, `metadata`

Write `description` as one sentence plus trigger phrases. Keep it specific and within 1-1024 characters.

### Step 5: Draft Skill Content

Write concise, reusable guidance that follows prompt-engineering best practices:

- Front-load critical instructions
- Use explicit, positive directives
- Keep one responsibility per step
- Include concrete output examples when format matters
- Define decision points with clear conditions and outcomes
- Add error handling for missing input, tool failures, and ambiguity

Use this scaffold:

````markdown
---
name: [skill-name]
description: [what it does]. Use when user mentions [trigger1], [trigger2], [trigger3].
---

# [Skill Title]

[One-paragraph purpose]

## When to Use
- [Condition 1]
- [Condition 2]

## Process
1. [Actionable step]
2. [Actionable step]

## Output Format
```markdown
[Expected output template]
```

## Error Handling
- [Missing input behavior]
- [Tool failure behavior]
````

### Step 6: Validate Quality

Before presenting, verify:

- Frontmatter is valid and minimal
- Name and directory match exactly
- Description includes realistic trigger phrases
- Content starts with the most important instruction
- Output format is explicit when needed
- No redundant duplication of rules already in `opencode.jsonc` instructions

Fix all failed checks before presenting the result.

### Step 7: Write Skill Files

Write the final skill artifact to disk.

- Ensure the target directory exists: `{name}/`
- Write `SKILL.md` with validated frontmatter and content
- If `SKILL.md` already exists, ask whether to overwrite and apply only after confirmation

### Step 8: Present Result

Return:

- Chosen path and skill name
- Final frontmatter
- Brief rationale for the structure
- Any assumptions made

## Output Template

```markdown
## Skill Created

- **Path:** `[path]`
- **Name:** `[name]`
- **Purpose:** [one sentence]
- **Auto-load cues:** [trigger phrases]

## Validation

- [x] Frontmatter valid
- [x] Name/path match
- [x] Prompt quality checks passed
```

$ARGUMENTS
