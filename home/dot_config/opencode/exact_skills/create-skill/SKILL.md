---
name: create-skill
description: Create new OpenCode skills or commands, or review existing ones following best practices for structure and prompt engineering. Use when user mentions create skill, new skill, write skill, build skill, make skill, skill template, review skill, audit skill, improve skill, skill best practices, create command, or new command.
---

# Create Skill or Command

Create new OpenCode skills or commands, or review existing ones. Every artifact produced or reviewed is evaluated against best practices for structure, prompt engineering, and content quality.

## When to Use Skills vs. Commands

Choose the right artifact for the job:

| Use a **Skill** when... | Use a **Command** when... |
|---|---|
| The agent discovers and loads it contextually | The user triggers it explicitly with `/name` |
| Multiple commands or workflows might need it | It maps to a single user-facing action |
| It provides reference knowledge (formats, patterns, guidelines) | It defines a complete workflow from start to finish |
| It augments the agent's capabilities in various situations | It replaces typing a long prompt every time |

**Rule of thumb**: If the content is always triggered by one specific user action, make it a command. If the agent might need the knowledge in different contexts, make it a skill.

## Skill Anatomy

A skill is a directory under `~/.config/opencode/skills/` or `.opencode/skills/` containing a `SKILL.md` entry point.

### SKILL.md Frontmatter

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `name` | string | Yes | Kebab-case identifier, 1-64 chars, must match directory name |
| `description` | string | Yes | What the skill does + trigger phrases (1-1024 chars) |
| `license` | string | No | License identifier |
| `compatibility` | string | No | Tool compatibility hint |
| `metadata` | map | No | String-to-string key-value pairs |

### Name Validation

`name` must:
- Be 1-64 characters
- Be lowercase alphanumeric with single hyphen separators
- Not start or end with `-`
- Not contain consecutive `--`
- Match regex: `^[a-z0-9]+(-[a-z0-9]+)*$`

## Command Anatomy

A command is a markdown file in `~/.config/opencode/commands/` or `.opencode/commands/`.

### Command Frontmatter

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `description` | string | Yes | Shown in the TUI when typing `/` |
| `agent` | string | No | Which agent executes (`build`, `plan`, or a custom agent) |
| `model` | string | No | Override the default model |
| `subtask` | boolean | No | Run as a subagent to avoid polluting primary context |

### Command Body

The markdown body is the prompt template. It supports:
- `$ARGUMENTS` — Replaced with everything the user types after `/name`
- `$1`, `$2`, etc. — Positional arguments
- `` !`command` `` — Inject shell command output
- `@path/to/file` — Include file contents

## Prompt Engineering Principles

Apply these when writing skill or command content:

1. **Be explicit** — State what to do, not what to avoid. "Use imperative mood" instead of "Don't use past tense."
2. **Front-load critical information** — The most important instructions come first. The agent may truncate or compress long content.
3. **Include concrete examples** — Show the exact output format with placeholders. An example is worth more than a paragraph of description.
4. **One responsibility per step** — Each workflow step does one thing. "Gather context" and "Analyze changes" are separate steps.
5. **Specify decision points** — When the workflow branches, state the condition and both outcomes. Use tables for decision matrices.
6. **Add error handling** — Specify what to do when tools fail, when input is missing, or when the user's request is ambiguous.
7. **Avoid duplicating rules** — If content exists in a rule file (loaded via `instructions` in config), reference it instead of repeating it. This saves context tokens.
8. **Keep scope tight** — Each skill or command does one thing well. If it has two unrelated workflows, split it into two.

## Quality Checklist

Evaluate every skill and command against these criteria:

- [ ] **Frontmatter is valid**: Required fields present, name matches directory (skills) or filename (commands)
- [ ] **Description is specific**: Includes what it does and trigger phrases/keywords
- [ ] **Content starts with the most important instruction**: Not background or preamble
- [ ] **Workflow has concrete steps**: Each step specifies exact commands, tools, or questions to use
- [ ] **Output format is shown**: At least one example of the expected output with placeholders
- [ ] **Decision points are explicit**: Conditions and outcomes are stated, not implied
- [ ] **Error handling exists**: Covers tool failures, missing input, and ambiguous requests
- [ ] **No duplication with rules**: Referenced instead of repeated
- [ ] **Scope is focused**: One responsibility per artifact

## Workflows

### Create Skill

1. Ask the user: What should the skill do? When should it be loaded?
2. Determine if a skill is the right artifact (vs. a command) using the decision table above
3. Choose a kebab-case name that describes the skill's purpose
4. Create the directory and `SKILL.md` with valid frontmatter
5. Write the content following the prompt engineering principles
6. Validate against the quality checklist
7. If any checklist item fails, fix it before presenting to the user

### Create Command

1. Ask the user: What should the command do? What arguments does it take?
2. Choose a name that makes sense as `/name` in the TUI
3. Determine the right agent (`build` for write operations, `plan` for read-only analysis)
4. Write the command markdown with valid frontmatter
5. Write the workflow in the body, ending with `$ARGUMENTS`
6. Validate against the quality checklist

### Review Skill or Command

1. Read the artifact's content
2. Evaluate against every item in the quality checklist
3. For each failing item, provide:
   - What is wrong (with a quote from the content)
   - Why it matters
   - A concrete fix
4. Ask the user if fixes should be applied
5. Apply fixes if confirmed
