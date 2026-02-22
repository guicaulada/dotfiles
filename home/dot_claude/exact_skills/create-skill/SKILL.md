---
name: create-skill
description: Creates new Claude Code skills or reviews existing ones against Anthropic's best practices for structure, conciseness, and prompt engineering. Use when user mentions create skill, new skill, write skill, build skill, make skill, skill template, review skill, audit skill, improve skill, or skill best practices.
allowed-tools: Read, Write, Edit, Glob, Grep
argument-hint: [create|review] [skill-name]
---

# Create Skill

Create new Claude Code skills or review existing ones. Every skill produced or reviewed follows Anthropic's documented best practices.

## Core Principles

Apply these when authoring or reviewing skills:

1. **Conciseness** — The context window is a public good. Only include information Claude does not already know. Challenge every paragraph: "Does this justify its token cost?"
2. **Progressive disclosure** — SKILL.md provides the overview and pointers. Detailed content goes in separate files loaded on demand. Keep references one level deep from SKILL.md.
3. **Degrees of freedom** — Match instruction specificity to task fragility. Destructive or irreversible operations get exact scripts (low freedom). Creative or exploratory tasks get general guidance (high freedom).
4. **Third-person descriptions** — Write the `description` field as "Processes files..." not "Process files" or "I process files." Third person is critical for reliable skill discovery.

## Frontmatter Reference

| Field | Constraints | Notes |
|-------|------------|-------|
| `name` | Kebab-case, max 64 chars, no `anthropic`/`claude` | Becomes the `/name` command. Consider gerund form (e.g., `reviewing-code`) |
| `description` | Max 1024 chars, third person, non-empty | Include what it does + when to use it with trigger terms |
| `allowed-tools` | Comma-separated | Scope Bash: `Bash(git *)` not `Bash` |
| `disable-model-invocation` | Boolean | `true` for side effects on shared state (git push, API calls, deployments) |
| `user-invocable` | Boolean | `false` only for pure background knowledge |
| `argument-hint` | String | Autocomplete hint shown in UI: `[issue-number]` |
| `context` | `fork` | Run in an isolated subagent |
| `agent` | String | Subagent type when `context: fork`: `Explore`, `Plan`, `general-purpose` |
| `model` | `opus`, `sonnet`, `haiku` | Model override |

## File Organization

```
{name}/
├── SKILL.md           # Overview + frontmatter + workflow index (under 500 lines)
├── {workflow}.md       # One file per workflow, named after action verb
└── {reference}.md      # Optional detailed reference (loaded on demand)
```

Keep references one level deep from SKILL.md. Name files descriptively (`form_validation.md` not `doc2.md`). Use forward slashes in all paths.

## Workflows

### Create Skill

Trigger: "create skill", "new skill", "write skill", "build skill", "make skill"

Read and follow [create.md](create.md).

### Review Skill

Trigger: "review skill", "audit skill", "improve skill", "skill best practices", "check skill"

Read and follow [review.md](review.md).
