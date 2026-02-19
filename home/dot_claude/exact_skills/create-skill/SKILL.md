---
name: create-skill
description: Create new Claude Code skills or review existing ones following Anthropic's best practices for skill structure and prompt engineering. Use when user mentions create skill, new skill, write skill, build skill, make skill, skill template, review skill, audit skill, improve skill, or skill best practices.
allowed-tools: Read, Write, Edit, Glob, Grep
argument-hint: [create|review] [skill-name]
---

# Create Skill

Create new Claude Code skills or review existing ones. Every skill produced or reviewed is evaluated against Anthropic's documented best practices for skill structure, prompt engineering, and content quality.

## Skill Anatomy

A skill is a directory under `.claude/skills/` containing a `SKILL.md` entry point and optional supporting files.

### Directory Layout

```
{skill-name}/
├── SKILL.md           # Entry point: frontmatter + reference content + workflow index
├── {workflow}.md       # One file per workflow (create, review, batch, etc.)
└── {supporting}.md     # Optional: SOPs, templates, detailed references
```

### SKILL.md Frontmatter

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `name` | string | Recommended | Kebab-case identifier, max 64 chars. Defaults to directory name. |
| `description` | string | Recommended | What the skill does + trigger phrases. Claude uses this to decide when to auto-load. |
| `allowed-tools` | string | No | Comma-separated tools permitted without user confirmation. Scope Bash with patterns: `Bash(git *)`. |
| `disable-model-invocation` | boolean | No | Set `true` to prevent auto-loading. User must invoke with `/name`. Use for side-effect operations. |
| `user-invocable` | boolean | No | Set `false` to hide from `/` menu. Use for background knowledge skills. |
| `argument-hint` | string | No | Autocomplete hint: `[issue-number]`, `[file] [format]`. |
| `context` | string | No | Set `fork` to run in an isolated subagent. |
| `agent` | string | No | Subagent type when `context: fork`: `Explore`, `Plan`, `general-purpose`. |
| `model` | string | No | Model override: `opus`, `sonnet`, `haiku`. |

### SKILL.md Content Sections

After frontmatter, the SKILL.md contains:

1. **Heading and overview** — One paragraph explaining the skill's purpose
2. **Reference tables** — Quick-reference for formats, severity levels, types, or conventions the skill uses
3. **Methodology notes** — Brief description of the approach (link to SOP files for details)
4. **Workflows section** — Index of available workflows with trigger phrases and file references

### Workflow File Structure

Each workflow file uses XML tags to separate concerns:

| Tag | Purpose |
|-----|---------|
| `<purpose>` | What this workflow accomplishes and why |
| `<process>` | Numbered steps with clear decision points |
| `<output>` | Exact format of the expected output |
| `<rules>` | Constraints and quality requirements |
| `<examples>` | Concrete input/output pairs demonstrating expected behavior |

## Prompt Engineering Principles

Apply these when writing skill content:

1. **Be explicit** — State what to do, not what to avoid. "Write prose paragraphs" instead of "Don't use bullet points."
2. **Provide context** — Explain why a behavior matters. Claude generalizes from explanations better than from bare rules.
3. **Use XML tags consistently** — Same tag names throughout. Tags separate structure from content and make prompts parseable.
4. **Include examples** — 1-3 diverse, relevant examples demonstrating expected output. Wrap in `<example>` tags inside `<examples>`.
5. **Front-load critical information** — Most important instructions first. Steps in logical order.
6. **Be specific about format** — Show the exact output structure with placeholders. Use templates with `[PLACEHOLDER]` notation.
7. **One responsibility per step** — Each numbered step does one thing. Complex steps get sub-steps.
8. **Specify decision points** — Where the process branches, state conditions and outcomes clearly.
9. **Ground in evidence** — Reference specific files, lines, or data rather than making assumptions.
10. **Keep scope tight** — Each skill does one thing well. Split broad skills into focused ones.

## Quality Checklist

| Category | Criterion |
|----------|-----------|
| **Frontmatter** | `name` is kebab-case, under 64 chars |
| | `description` includes purpose + trigger phrases |
| | `allowed-tools` is minimal and scoped (e.g., `Bash(git *)` not `Bash`) |
| | `disable-model-invocation` is `true` for operations that affect shared state (git push, API calls, external services). Local file writes with user confirmation gates may omit this. |
| **Structure** | SKILL.md stays under 500 lines; detailed content in supporting files |
| | Each workflow is a separate file with XML-tagged sections |
| | `<purpose>`, `<process>`, `<output>`, and `<rules>` tags are present in workflows |
| **Content** | Instructions use imperative mood and active voice |
| | Steps are numbered and sequential |
| | Decision points have explicit conditions and outcomes |
| | Output format uses a template with `[PLACEHOLDER]` notation |
| | At least one example demonstrates expected behavior |
| **Prompt Quality** | Instructions say what to do, not what to avoid |
| | Context explains why, not just what |
| | XML tags are used consistently |
| | Sections are consistent with each other |
| | Emphasis is reserved for genuinely critical items |

## Workflows

### Create Skill

Trigger: "create skill", "new skill", "write skill", "build skill", "make skill", "skill template"

Read and follow `skills/create-skill/create.md`.

### Review Skill

Trigger: "review skill", "audit skill", "improve skill", "skill best practices", "check skill"

Read and follow `skills/create-skill/review.md`.
