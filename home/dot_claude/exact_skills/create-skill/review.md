---
description: Reviews an existing Claude Code skill against Anthropic's best practices and suggests improvements
---

<purpose>
Evaluate an existing Claude Code skill against Anthropic's best practices for structure, conciseness, and prompt engineering. Produce a structured review with actionable findings organized by severity, covering metadata, structure, conciseness, content quality, and degrees of freedom.
</purpose>

<process>

## Checklist

Copy and track progress:

```
Review Progress:
- [ ] Step 1: Locate and read skill files
- [ ] Step 2: Evaluate metadata
- [ ] Step 3: Evaluate structure and conciseness
- [ ] Step 4: Evaluate content quality
- [ ] Step 5: Compile and present review
- [ ] Step 6: Apply fixes (if requested)
```

## Step 1: Locate and Read Skill Files

Determine the skill from user input or `$ARGUMENTS`:

- **Skill name**: Look in `.claude/skills/[name]/SKILL.md`
- **Directory path**: Read from the specified path

If no skill is specified, list available skills with Glob and ask the user to choose.

Read every file in the skill directory. Build a map of what the skill does, its workflows, tools, and how files connect.

## Step 2: Evaluate Metadata

Check each frontmatter field against the reference table in SKILL.md:

| Field                      | Check                                                                 |
|----------------------------|-----------------------------------------------------------------------|
| `name`                     | Kebab-case, under 64 chars, no `anthropic`/`claude`, matches folder name |
| `description`              | Third person, specific, includes trigger terms, under 1024 chars, has negative triggers if needed |
| `allowed-tools`            | Minimum required, Bash scoped with glob patterns                      |
| `disable-model-invocation` | `true` for shared-state side effects                                  |
| `user-invocable`           | `false` only for pure background knowledge                            |

Flag any deviation.

## Step 3: Evaluate Structure and Conciseness

**Structure checks:**

- No README.md in skill folder (all docs in SKILL.md or references)
- SKILL.md under 500 lines; detailed content in separate files
- Each workflow in its own file, named after its action verb
- Workflow files have frontmatter with `description`
- Workflow files use `<purpose>`, `<process>`, `<output>`, `<rules>` tags
- `<examples>` present for workflows with structured output
- File references one level deep from SKILL.md (no chaining)
- File paths use forward slashes only

**Conciseness checks:**

- Each paragraph justifies its token cost — flag content that restates what Claude already knows (general programming concepts, basic prompt engineering, standard formatting rules)
- No verbose preambles or unnecessary background explanations
- Tables and templates used instead of prose where appropriate
- No time-sensitive content (specific versions, dates, URLs that may change)

Flag missing structure elements and unnecessary verbosity.

## Step 4: Evaluate Content Quality

**Instructions:**

- Imperative mood, positive framing (what to do, not what to avoid)
- Each step focused on one action
- Decision points explicit: "If [condition], [action]. Otherwise, [alternative]."
- One default approach per decision (no unnecessary multiple options)
- Parallel operations marked
- Feedback loops present for quality-critical operations (validate → fix → re-validate)
- Error handling/troubleshooting included for fragile or external operations
- Copyable checklists for multi-step workflows

**Output format:**

- Template with `[PLACEHOLDER]` notation
- Separate templates for output variants

**Degrees of freedom:**

- Destructive/irreversible operations have exact instructions (low freedom)
- Creative/exploratory operations have general guidance (high freedom)
- Flag mismatches: vague guidance for dangerous operations, or rigid scripts for flexible tasks

**Terminology and examples:**

- Consistent terms throughout (one term per concept)
- At least one example per workflow with structured output, covering standard and edge cases
- Examples wrapped in `<example>` tags inside `<examples>`
- Basic triggering tests defined (should-trigger + should-NOT-trigger phrases)

Flag unclear, incomplete, inconsistent, or miscalibrated content.

## Step 5: Compile and Present Review

Classify each finding by severity:

| Severity     | Meaning                                                     |
|--------------|-------------------------------------------------------------|
| `blocking`   | Prevents correct operation or violates a core best practice |
| `suggestion` | Meaningful quality improvement                              |
| `nitpick`    | Minor polish                                                |

Determine verdict:

| Condition                                    | Verdict        |
|----------------------------------------------|----------------|
| No blocking findings, follows best practices | **Excellent**  |
| No blocking findings, some suggestions       | **Good**       |
| Blocking findings, easy to fix               | **Needs Work** |
| Fundamental structure or approach issues     | **Rework**     |

Present the review using the output template.

If blocking or suggestion findings exist, ask the user: "How would you like to proceed?" with options: "Apply fixes automatically", "Show fixes first", "Done".

## Step 6: Apply Fixes (if requested)

For each finding:

1. Show the proposed change (before/after)
2. Apply with Edit or Write
3. Mark as resolved

After applying all fixes, re-validate from Step 2 to confirm no regressions. If re-validation finds new issues, fix and re-validate again. Repeat until clean.

</process>

<output>

```
## Skill Review: [NAME]

**Location:** [PATH]
**Files:** [COUNT] ([LIST])

---

### Summary

| Severity    | Count |
|-------------|-------|
| Blocking    | [N]   |
| Suggestions | [N]   |
| Nitpicks    | [N]   |

---

### Blocking Issues

[N]. **[TITLE]** — `[FILE]`: [DESCRIPTION]. **Fix:** [ACTION].

---

### Suggestions

[N]. **[TITLE]** — `[FILE]`: [DESCRIPTION]. **Fix:** [ACTION].

---

### Nitpicks

[N]. **[TITLE]** — `[FILE]`: [DESCRIPTION].

---

### Strengths

- [POSITIVE_OBSERVATION]
- [POSITIVE_OBSERVATION]

---

## Verdict: [EXCELLENT | GOOD | NEEDS WORK | REWORK]

[ONE_PARAGRAPH_SUMMARY]
```

</output>

<rules>

- Read every file in the skill directory before forming any assessment
- Reference specific files and content for every finding
- Provide a concrete fix for every blocking and suggestion finding
- Acknowledge strengths alongside improvements
- Use severity levels consistently: blocking for broken essentials, suggestion for meaningful improvements, nitpick for polish
- Prioritize conciseness findings: skills that explain what Claude already knows are at least suggestion-level
- Apply fixes only with explicit user confirmation
- Re-validate after applying fixes; repeat until clean
- Frame findings constructively as improvements

</rules>

<examples>

<example>

**Input**: `/create-skill review commit`

**Output**:

## Skill Review: commit

**Location:** .claude/skills/commit/
**Files:** 3 (SKILL.md, create.md, amend.md)

---

### Summary

| Severity    | Count |
|-------------|-------|
| Blocking    | 1     |
| Suggestions | 2     |
| Nitpicks    | 0     |

---

### Blocking Issues

1. **Description uses imperative mood** — `SKILL.md`: Description reads "Create well-formatted git commits." Descriptions must use third person for reliable skill discovery. **Fix:** Change to "Creates well-formatted git commits by analyzing staged changes."

---

### Suggestions

1. **Verbose git explanation** — `create.md`: Lines 15-30 explain what git staging is. Claude already knows this; the explanation wastes context tokens. **Fix:** Remove the background explanation; keep only the skill-specific process steps.

2. **Missing examples** — `create.md`: Produces structured commit output but has no `<examples>` section. **Fix:** Add an `<examples>` section with one standard and one multi-file commit example.

---

### Nitpicks

None

---

### Strengths

- Clean workflow separation between create and amend
- Scoped `Bash(git *)` in allowed-tools
- Clear decision points for single vs. multi-commit paths

---

## Verdict: NEEDS WORK

Good structure and workflow separation. Fix the imperative description first (blocks reliable discovery), then trim verbose explanations and add examples for output consistency.

</example>

<example>

**Input**: `/create-skill review deploy`

**Output**:

## Skill Review: deploy

**Location:** .claude/skills/deploy/
**Files:** 2 (SKILL.md, run.md)

---

### Summary

| Severity    | Count |
|-------------|-------|
| Blocking    | 2     |
| Suggestions | 1     |
| Nitpicks    | 0     |

---

### Blocking Issues

1. **Missing `disable-model-invocation`** — `SKILL.md`: The skill runs `kubectl apply` and `docker push`, modifying production infrastructure. Auto-invocation could trigger an unintended deployment. **Fix:** Add `disable-model-invocation: true` to frontmatter.

2. **Unscoped Bash** — `SKILL.md`: `allowed-tools: Read, Bash` grants unrestricted shell access. The workflow only uses `kubectl` and `docker` commands. **Fix:** Scope to `Bash(kubectl *), Bash(docker *)`.

---

### Suggestions

1. **Degrees of freedom mismatch** — `run.md`: The deployment steps say "deploy the application" without exact commands. Deployments are destructive and irreversible — instructions should specify exact commands with no room for interpretation. **Fix:** Replace general guidance with exact command sequences and validation checks.

---

### Nitpicks

None

---

### Strengths

- Pre-deployment checklist validates tests pass before proceeding
- Rollback instructions included

---

## Verdict: NEEDS WORK

Solid deployment workflow with good safety habits (pre-checks, rollback). The missing `disable-model-invocation` and unscoped Bash are critical safety gaps — both are straightforward fixes. Tighten the deployment instructions to match the high-fragility nature of the operation.

</example>

</examples>
