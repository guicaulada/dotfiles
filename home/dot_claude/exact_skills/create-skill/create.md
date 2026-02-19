---
description: Guide user through creating a new Claude Code skill following best practices
---

<purpose>
Create a new Claude Code skill from a user's description. Walk through requirements gathering, metadata design, file structure planning, and content generation. Produce skill files that follow Anthropic's best practices for skill structure and prompt engineering.
</purpose>

<process>

## Step 1: Understand the Skill's Purpose

Gather the essential information about what the skill should do. Ask the user with AskUserQuestion for any details not already provided:

- **What does the skill do?** — The core capability in one sentence
- **When should it activate?** — Trigger phrases and scenarios
- **What tools does it need?** — Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, Task, Skill
- **Does it have side effects?** — Operations that change external state (git push, API calls, file writes)
- **How many distinct workflows?** — Different modes of operation (e.g., create vs. review, single vs. batch)

If the user provides a rough description, extract as much as possible before asking clarifying questions. Ask only for what cannot be inferred.

## Step 2: Determine Metadata

Based on the gathered information, determine the frontmatter fields:

**`name`**: Derive from the skill's purpose. Use kebab-case, keep it short and memorable. The name becomes the slash command (`/name`), so it should be easy to type and recall.

**`description`**: Write a single sentence describing what the skill does, followed by trigger phrases. Format: "[What it does]. Use when user mentions [trigger1], [trigger2], [trigger3]..."

Trigger phrases should include:
- The primary action verb (e.g., "review pr")
- Common synonyms (e.g., "code review", "check pr")
- Related phrases users might say naturally (e.g., "look at this pr")

**`allowed-tools`**: Include only the tools the skill genuinely needs. Scope Bash commands with glob patterns when possible:
- `Bash(git *)` instead of `Bash` for git operations
- `Bash(gh *)` instead of `Bash` for GitHub CLI operations
- `Bash(npm *)`, `Bash(python *)` for specific runtimes

**`disable-model-invocation`**: Set to `true` if the skill affects shared state (git push, API calls, external services). Local file writes with user confirmation gates may keep `false` (default). Read-only or advisory skills keep `false`.

**`user-invocable`**: Set to `false` only for pure background knowledge skills with no actionable workflow. Default `true` for most skills.

Present the proposed metadata to the user for confirmation before proceeding.

## Step 3: Design File Structure

Plan the skill's file layout based on the number of workflows and supporting content needed.

**Single-workflow skill:**
```
{name}/
├── SKILL.md        # Frontmatter + reference content + single workflow
```

Only use this for very simple skills where everything fits in SKILL.md under 200 lines.

**Multi-workflow skill (preferred for non-trivial skills):**
```
{name}/
├── SKILL.md        # Frontmatter + reference content + workflow index
├── {workflow-1}.md  # First workflow
├── {workflow-2}.md  # Second workflow
└── {supporting}.md  # Optional: SOP, templates, detailed reference
```

Name workflow files after their action verb: `create.md`, `review.md`, `batch.md`, `amend.md`.

Present the proposed structure to the user.

## Step 4: Write SKILL.md

Generate the SKILL.md with these sections in order:

**1. Frontmatter block** — YAML between `---` delimiters with the metadata from Step 2.

**2. Heading and overview** — `# {Skill Name}` followed by one paragraph explaining the skill's purpose and value.

**3. Reference tables** (if applicable) — Quick-reference material the skill needs across workflows: format specifications, severity levels, type definitions, conventions. Use markdown tables for scannability.

**4. Methodology notes** (if applicable) — Brief description of the approach or process the skill follows. Link to supporting SOP files for details.

**5. Workflows section** — For each workflow:
```markdown
### {Workflow Name}

Trigger: "{trigger phrase 1}", "{trigger phrase 2}"

Read and follow `skills/{skill-name}/{workflow}.md`.
```

Apply these content guidelines:
- Keep SKILL.md under 500 lines. Move detailed content to supporting files.
- Use tables and bullet points for reference material — they scan faster than prose.
- Write in imperative mood: "Create a commit" not "Creates a commit."
- Include only information that applies across all workflows. Workflow-specific content goes in the workflow files.

## Step 5: Write Workflow Files

For each workflow file, generate content using this structure:

**Frontmatter:**
```yaml
---
description: {One-line description of what this workflow does}
---
```

**`<purpose>` tag:**
One paragraph explaining what the workflow accomplishes and why it exists. Be specific about inputs and outputs.

**`<process>` tag:**
Numbered steps using `## Step N: {Action}` headings. For each step:
- State what to do clearly in imperative mood
- Include specific commands, tool calls, or actions
- Mark parallel operations: "Run in parallel:"
- Include decision points with explicit conditions: "If X, do Y. Otherwise, do Z."
- Use AskUserQuestion for user decisions, with specific options
- Keep each step focused on one action

**`<output>` tag:**
A template showing the exact output format with `[PLACEHOLDER]` notation. Use markdown code blocks for structured output. Show separate templates for different output variants (e.g., single vs. multiple results).

**`<rules>` tag:**
Bullet list of constraints and quality requirements. Each rule should be:
- Actionable (can be checked: pass/fail)
- Specific (no vague guidance like "be careful")
- Positive (state what to do, not what to avoid)

**`<examples>` tag (when applicable):**
Wrap in `<examples>` containing one or more `<example>` blocks. Each example shows:
- **Input**: What the user provides
- **Output**: What the skill produces

Include diverse examples covering:
- The standard case
- An edge case or variant
- A minimal input case

Apply these prompt engineering principles:
- Be explicit — if a behavior matters, state it directly
- Provide context — explain why a rule exists when the reason is not obvious
- Front-load important information — critical instructions before supporting details
- Use consistent terminology — same terms for the same concepts throughout
- Specify format precisely — templates with placeholders, not vague descriptions

## Step 6: Validate Against Quality Checklist

Before presenting the skill to the user, verify it against the quality checklist defined in the SKILL.md reference. Check every criterion and fix any failures.

Key validation points:
- Frontmatter has `name`, `description` with trigger phrases, and scoped `allowed-tools`
- SKILL.md is under 500 lines with detailed content in supporting files
- Every workflow has `<purpose>`, `<process>`, `<output>`, and `<rules>` tags
- Steps are numbered and sequential with clear decision points
- Output format uses templates with `[PLACEHOLDER]` notation
- At least one example demonstrates expected behavior (for non-trivial workflows)
- Instructions use imperative mood and say what to do (positive framing)
- XML tags are consistent throughout

## Step 7: Present and Iterate

Present the complete skill to the user:
1. Show the file structure
2. Show each file's content
3. Highlight any design decisions made and the reasoning behind them

Ask the user with AskUserQuestion:
- "How would you like to proceed?"
- Options: "Save skill files", "Revise content", "Change structure"

If the user requests revisions, apply changes and re-validate against the checklist before presenting again.

</process>

<output>

After generating the skill files, present a summary:

```
## Skill Created: {name}

**Location:** .claude/skills/{name}/
**Invocation:** /{name} [arguments]
**Auto-trigger:** {yes/no}

### Files
| File | Purpose | Lines |
|------|---------|-------|
| SKILL.md | {purpose} | {N} |
| {workflow}.md | {purpose} | {N} |
| ... | ... | ... |

### Workflows
| Workflow | Trigger | File |
|----------|---------|------|
| {name} | "{trigger phrases}" | {file}.md |
| ... | ... | ... |

### Tools
{allowed-tools value}

### Metadata
- Model invocation: {enabled/disabled}
- User invocable: {yes/no}
- Context: {main/fork}
```

</output>

<rules>
- Ask the user for confirmation before writing any files
- Present proposed metadata and structure for review before generating content
- Scope `allowed-tools` to the minimum required; prefer `Bash(pattern *)` over bare `Bash`
- Set `disable-model-invocation: true` for skills that affect shared state (git push, API calls, external services)
- Keep SKILL.md under 500 lines; delegate detailed content to supporting files
- Every workflow file includes `<purpose>`, `<process>`, `<output>`, and `<rules>` XML tags
- Use consistent XML tag names across all workflow files
- Write instructions in imperative mood with positive framing
- Include at least one example in workflows that produce structured output
- Validate against the full quality checklist before presenting to the user
- Use `$ARGUMENTS` for dynamic skill arguments, not hardcoded values
- Name workflow files after their action verb (create, review, batch, amend)
</rules>

<examples>

<example>

**Input**: "Create a skill that generates changelogs from git history"

**Output**:

## Skill Created: changelog

**Location:** .claude/skills/changelog/
**Invocation:** /changelog [version]
**Auto-trigger:** no

### Files
| File | Purpose | Lines |
|------|---------|-------|
| SKILL.md | Entry point with format reference and workflow index | 45 |
| create.md | Generate changelog from git history | 95 |

### Workflows
| Workflow | Trigger | File |
|----------|---------|------|
| Create Changelog | "changelog", "generate changelog", "release notes" | create.md |

### Tools
Read, Bash(git *)

### Metadata
- Model invocation: disabled (writes files)
- User invocable: yes
- Context: main

</example>

<example>

**Input**: "Create a skill for our team's API design conventions — it should auto-load when someone is working on endpoints"

**Output**:

## Skill Created: api-conventions

**Location:** .claude/skills/api-conventions/
**Invocation:** /api-conventions
**Auto-trigger:** yes

### Files
| File | Purpose | Lines |
|------|---------|-------|
| SKILL.md | API conventions with naming, error format, and auth patterns | 120 |

### Workflows
| Workflow | Trigger | File |
|----------|---------|------|
| (reference only) | Auto-loads when designing APIs or writing endpoint handlers | — |

### Tools
Read

### Metadata
- Model invocation: enabled (reference content)
- User invocable: yes
- Context: main

</example>

</examples>
