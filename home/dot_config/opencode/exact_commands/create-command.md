---
description: Create an OpenCode command with strong prompt design
agent: build
---

Create a custom OpenCode command for a repeatable workflow.

Use current OpenCode command conventions and prompt-engineering best practices.

## Workflow

### Step 1: Clarify Command Intent

Collect the minimum details needed to generate a robust command:

- What the command should do from start to finish
- What arguments it accepts
- Whether it should write files or stay read-only
- Expected output format and success criteria

Ask 2-4 targeted questions at a time.

### Step 2: Choose Command Identity

Define command metadata:

- File name in kebab-case: `{command-name}.md`
- TUI invocation: `/{command-name}`
- Short description for slash-command picker

Check name collisions before finalizing:

- If `{command-name}` matches an existing built-in command, require explicit user confirmation to override
- If `{command-name}` matches an existing custom command file, ask whether to update the existing command or choose a new name

Use these locations:

- In this dotfiles repo: `home/dot_config/opencode/exact_commands/{command-name}.md`
- In a regular project: `.opencode/commands/{command-name}.md`
- In global config: `~/.config/opencode/commands/{command-name}.md`

### Step 3: Pick Execution Settings

Set frontmatter intentionally:

- Required: `description`
- Optional: `agent`, `model`, `subtask`

Agent guidance:

- `build` for workflows that edit files or run implementation commands
- `plan` for analysis/review workflows

Use `subtask: true` only when isolation from primary context is beneficial.

### Step 4: Draft Command Template

Write the body as a complete workflow with explicit steps and decision points.

Use supported placeholders when needed:

- `$ARGUMENTS` for full trailing text
- `$1`, `$2`, ... for positional arguments
- `` !`command` `` for shell output injection
- `@path/to/file` for file inclusion

Prompt quality requirements:

- Start with the most critical instruction
- Use imperative language and concrete actions
- Define branching conditions explicitly
- Include error handling for missing args, failed tools, and ambiguous requests
- Show exact output format for structured responses

### Step 5: Write Command File

Write the command file to the selected target path.

- Create parent directories when they do not exist
- If the target file already exists, show a brief diff summary and ask whether to overwrite
- Save the final frontmatter and body to `{command-name}.md`

### Step 6: Validate Command Quality

Check before finalizing:

- Frontmatter is valid and minimal
- Description is specific and useful in the TUI list
- Body does one job and avoids unrelated responsibilities
- Arguments are handled correctly
- Safety checks are present for destructive operations
- Built-in command name collisions are intentional
- File was written to the expected location

Fix any failed checks.

### Step 7: Present Result

Return:

- Command path and invocation
- Frontmatter and workflow summary
- Example usage with arguments

## Output Template

```markdown
## Command Created

- **Path:** `[path]`
- **Invocation:** `/{command-name}`
- **Agent:** `[build|plan]`
- **Purpose:** [one sentence]

## Example

`/{command-name} [arguments]`

## Validation

- [x] Frontmatter valid
- [x] Prompt workflow complete
- [x] Argument handling verified
```

$ARGUMENTS
