---
description: Guides creation of a new Claude Code skill following Anthropic's best practices
---

<purpose>
Create a new Claude Code skill from a user's description. Gather requirements, design metadata and structure, generate concise skill files, and validate against best practices. Produce skills that follow Anthropic's guidelines for conciseness, progressive disclosure, and prompt engineering.
</purpose>

<process>

## Checklist

Copy and track progress:

```
Skill Creation:
- [ ] Step 1: Gather requirements
- [ ] Step 2: Design metadata
- [ ] Step 3: Plan file structure
- [ ] Step 4: Write SKILL.md
- [ ] Step 5: Write workflow files
- [ ] Step 6: Validate and iterate
```

## Step 1: Gather Requirements

Determine from the user's input:

- **Core capability** — What the skill does in one sentence
- **Trigger scenarios** — When it should activate and common phrases users would say
- **Required tools** — Which tools it needs (Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, Task, Skill)
- **Side effects** — Operations that change shared state (git push, API calls, deployments)
- **Task fragility** — How destructive or irreversible are the operations? This determines the degree of freedom in instructions
- **Workflow count** — Distinct modes of operation (e.g., create vs. review, single vs. batch)

Extract as much as possible from the user's description before asking clarifying questions. Ask only for what cannot be inferred.

## Step 2: Design Metadata

**`name`**: Kebab-case, max 64 chars. This becomes the `/name` command — keep it short and memorable. Consider gerund form (e.g., `reviewing-code`). Must not contain `anthropic` or `claude`.

**`description`**: Write in third person, max 1024 chars. Format: "[What it does]. Use when [trigger terms]."

- Third person: "Generates changelogs..." not "Generate changelogs"
- Include the primary action and common synonyms as trigger terms
- Example: "Generates changelogs from git history. Use when user mentions changelog, release notes, or version history."

**`allowed-tools`**: Include only the tools the skill genuinely needs. Scope Bash commands with glob patterns:

- `Bash(git *)` for git operations
- `Bash(gh *)` for GitHub CLI
- `Bash(npm *)`, `Bash(python *)` for specific runtimes

**`disable-model-invocation`**: Set `true` for skills that affect shared state (git push, API calls, deployments, external services). Read-only and advisory skills keep the default (`false`).

Present proposed metadata to the user for confirmation before proceeding.

## Step 3: Plan File Structure

**Simple skill (everything fits under 200 lines):**

```
{name}/
└── SKILL.md
```

**Standard skill (preferred for non-trivial skills):**

```
{name}/
├── SKILL.md          # Overview + workflow index
├── {workflow}.md      # One per workflow
└── {reference}.md     # Optional detailed reference
```

Name workflow files after their action verb: `create.md`, `review.md`, `analyze.md`. Use forward slashes in all paths.

Present proposed structure to the user.

## Step 4: Write SKILL.md

Structure in this order:

1. **Frontmatter** — YAML with metadata from Step 2
2. **Heading and overview** — One paragraph on purpose
3. **Reference content** (if shared across workflows) — Tables and concise lists for conventions, formats, or types that workflows share
4. **Workflow index** — For each workflow:

```markdown
### [Workflow Name]

Trigger: "[phrase 1]", "[phrase 2]"

Read and follow [{workflow}.md]({workflow}.md).
```

**Conciseness check**: For every paragraph, ask "Does Claude already know this?" Remove explanations of general concepts (what markdown is, how XML tags work, general programming advice). Include only information specific to this skill's domain.

Keep SKILL.md under 500 lines. Move detailed content to supporting files.

## Step 5: Write Workflow Files

Each workflow file uses this structure:

**Frontmatter:**

```yaml
---
description: [One-line description of what this workflow does]
---
```

**`<purpose>`** — One paragraph: what the workflow accomplishes, its inputs, and its outputs.

**`<process>`** — Numbered steps with `## Step N: [Action]` headings.

- Include a copyable checklist at the top for multi-step workflows
- Use imperative mood and positive framing (state what to do)
- Mark parallel operations: "Run in parallel:"
- State decision points explicitly: "If [condition], [action]. Otherwise, [alternative]."
- Include feedback loops for quality-critical operations: validate, fix, re-validate until clean
- Keep each step focused on one action

**`<output>`** — Template with `[PLACEHOLDER]` notation showing exact output format. Show separate templates for different output variants if applicable.

**`<rules>`** — Bullet list of constraints. Each rule is actionable (pass/fail checkable), specific (no vague guidance), and stated positively (what to do).

**`<examples>`** — One or more `<example>` blocks with input/output pairs. Cover the standard case and at least one edge case or variant.

**Calibrate degrees of freedom**: Match instruction specificity to task fragility.

- Destructive or irreversible operations (deployments, data mutations, external API calls) → exact commands, strict sequence, low freedom
- Creative or exploratory operations (code review, analysis, brainstorming) → general guidance, high freedom
- Most operations fall in between → preferred patterns with noted alternatives

## Step 6: Validate and Iterate

Validate the complete skill against this checklist:

```
Quality Check:
- [ ] Description is third person, specific, includes trigger terms, under 1024 chars
- [ ] Name is kebab-case, under 64 chars, no "anthropic"/"claude"
- [ ] SKILL.md body under 500 lines
- [ ] Every paragraph justifies its token cost (no information Claude already knows)
- [ ] References one level deep from SKILL.md (no chaining)
- [ ] File paths use forward slashes only
- [ ] Each workflow has <purpose>, <process>, <output>, <rules>
- [ ] At least one <example> per workflow with structured output
- [ ] Steps are numbered with explicit decision points
- [ ] Output format uses [PLACEHOLDER] templates
- [ ] Feedback loops present for quality-critical operations
- [ ] Instructions use imperative mood, positive framing
- [ ] allowed-tools scoped to minimum required, Bash uses glob patterns
- [ ] disable-model-invocation set for shared-state side effects
- [ ] Terminology consistent throughout (one term per concept)
- [ ] Degrees of freedom match task fragility
- [ ] No time-sensitive content (specific versions, dates, URLs that may change)
```

Fix any failures. After fixing, re-run the full checklist. Repeat until all criteria pass.

Present the complete skill to the user with:

1. File structure
2. Each file's content
3. Key design decisions and rationale

Ask the user: "How would you like to proceed?" with options: "Save skill files", "Revise content", "Change structure".

If revisions are requested, apply changes and re-validate before presenting again.

</process>

<output>

```
## Skill Created: [NAME]

**Location:** .claude/skills/[NAME]/
**Invocation:** /[NAME] [ARGUMENTS]
**Auto-trigger:** [yes/no]

### Files
| File          | Purpose   | Lines |
|---------------|-----------|-------|
| SKILL.md      | [PURPOSE] | [N]   |
| [WORKFLOW].md | [PURPOSE] | [N]   |

### Workflows
| Workflow | Trigger     | File      |
|----------|-------------|-----------|
| [NAME]   | "[PHRASES]" | [FILE].md |

### Metadata
- Tools: [ALLOWED-TOOLS]
- Model invocation: [enabled/disabled]
- User invocable: [yes/no]
```

</output>

<rules>
- Confirm metadata and file structure with the user before generating content
- Write descriptions in third person ("Generates..." not "Generate..." or "I generate...")
- Scope allowed-tools to the minimum required; use `Bash(pattern *)` over bare `Bash`
- Set `disable-model-invocation: true` for skills affecting shared state
- Keep SKILL.md under 500 lines; move detailed content to supporting files
- Include `<purpose>`, `<process>`, `<output>`, and `<rules>` in every workflow file
- Include at least one `<example>` per workflow with structured output
- Apply conciseness: remove information Claude already knows; include only domain-specific context
- Match degrees of freedom to task fragility
- Keep file references one level deep from SKILL.md
- Use forward slashes in all file paths
- Avoid time-sensitive content (specific versions, dates, URLs that may change)
- Use `$ARGUMENTS` for dynamic skill arguments
- Name workflow files after their action verb
- Use consistent terminology throughout (one term per concept)
- Validate against the full quality checklist before presenting to the user
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

| File        | Purpose                                              | Lines |
|-------------|------------------------------------------------------|-------|
| SKILL.md    | Entry point with format reference and workflow index | 40    |
| generate.md | Generates changelog from git history                 | 80    |

### Workflows

| Workflow | Trigger                                         | File        |
|----------|-------------------------------------------------|-------------|
| Generate | "changelog", "release notes", "version history" | generate.md |

### Metadata

- Tools: Read, Bash(git \*)
- Model invocation: disabled (pushes tags and writes release files)
- User invocable: yes

</example>

<example>

**Input**: "Create a skill for our team's API design conventions that auto-loads when working on endpoints"

**Output**:

## Skill Created: api-conventions

**Location:** .claude/skills/api-conventions/
**Invocation:** /api-conventions
**Auto-trigger:** yes

### Files

| File     | Purpose                                     | Lines |
|----------|---------------------------------------------|-------|
| SKILL.md | API naming, error format, and auth patterns | 90    |

### Workflows

| Workflow         | Trigger                                | File |
|------------------|----------------------------------------|------|
| (reference only) | Auto-loads for API and endpoint design | —    |

### Metadata

- Tools: Read
- Model invocation: enabled (reference content only, no side effects)
- User invocable: yes

</example>

</examples>
