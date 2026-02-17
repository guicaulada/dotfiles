---
description: Review an existing Claude Code skill against best practices and suggest improvements
---

<purpose>
Evaluate an existing Claude Code skill against Anthropic's documented best practices for skill structure, prompt engineering, and content quality. Produce a structured review with actionable findings organized by severity, covering frontmatter configuration, file structure, content quality, and prompt engineering patterns.
</purpose>

<process>

## Step 1: Locate Skill Files

Determine which skill to review from the user's input. The input may be:

- **Skill name** (e.g., "commit"): Look for `.claude/skills/{name}/SKILL.md`
- **Directory path**: Read from the specified directory
- **`$ARGUMENTS`**: Parse the first argument as the skill name or path

If no skill is specified, list available skills from `.claude/skills/` using Glob and ask the user to choose with AskUserQuestion.

Verify the skill directory exists and contains a `SKILL.md` file. If not found, inform the user and exit.

## Step 2: Read All Skill Files

Read every file in the skill directory:
1. Read `SKILL.md` first for the entry point and structure
2. Read each workflow file referenced in SKILL.md
3. Read any supporting files (SOPs, templates, references)

Build a mental map of the skill:
- What does it do?
- How many workflows does it have?
- What tools does it use?
- How are files connected?

## Step 3: Evaluate Frontmatter

Check each frontmatter field against best practices:

**`name`:**
- Is it kebab-case?
- Is it under 64 characters?
- Is it memorable and easy to type as a slash command?
- Does it clearly suggest the skill's purpose?

**`description`:**
- Does it explain what the skill does in the first sentence?
- Does it include trigger phrases ("Use when user mentions...")?
- Are trigger phrases diverse enough to cover natural phrasing?
- Is it concise (under 300 characters)?

**`allowed-tools`:**
- Are tools scoped to the minimum needed?
- Are Bash commands restricted with glob patterns where possible?
- Are any unnecessary tools included?
- Are any needed tools missing?

**`disable-model-invocation`:**
- Is it `true` for skills with side effects?
- Is it appropriately `false` (or omitted) for advisory/reference skills?

**`user-invocable`:**
- Is it `false` only for pure background knowledge?
- Would users benefit from manual invocation?

Score: Flag any field that deviates from best practices.

## Step 4: Evaluate Structure

Assess the file organization:

**SKILL.md length:**
- Is it under 500 lines?
- Should any content be moved to supporting files?

**Workflow separation:**
- Does each distinct workflow have its own file?
- Are workflow files named after their action verb?

**Supporting files:**
- Is detailed reference content in separate files rather than bloating SKILL.md?
- Are supporting files referenced clearly from SKILL.md?

**Workflow file structure:**
- Does each workflow file have YAML frontmatter with a `description`?
- Does it use the four core XML tags: `<purpose>`, `<process>`, `<output>`, `<rules>`?
- Does it include `<examples>` for workflows with structured output?

Score: Flag missing structure elements.

## Step 5: Evaluate Content Quality

Analyze the actual instructions in each file:

**Clarity:**
- Are instructions in imperative mood? ("Run the tests" not "The tests should be run")
- Is each step focused on one action?
- Are decision points explicit? ("If X, do Y. Otherwise, do Z.")
- Can a reader follow the process without ambiguity?

**Completeness:**
- Are all steps necessary for the workflow present?
- Are parallel operations marked? ("Run in parallel:")
- Are user interaction points specified? (AskUserQuestion with options)
- Does the output section show the exact format with `[PLACEHOLDER]` notation?

**Consistency:**
- Are XML tag names the same across all files?
- Is terminology consistent (same term for same concept)?
- Do referenced files actually exist?

Score: Flag unclear, incomplete, or inconsistent content.

## Step 6: Evaluate Prompt Engineering

Check for adherence to Anthropic's prompt engineering principles:

**Positive framing:**
- Do instructions say what to do, not what to avoid?
- Flag any "do not", "never", "don't" that could be rephrased positively

**Context and motivation:**
- Do rules explain why when the reason is not obvious?
- Does the skill provide enough context for Claude to generalize?

**Specificity:**
- Are output formats precisely defined with templates?
- Are vague instructions replaced with concrete guidance?
- Flag any "be careful", "be thorough", or similarly vague phrases

**Examples:**
- Are examples present for workflows with structured output?
- Do examples cover diverse scenarios (standard, edge, minimal)?
- Are examples wrapped in `<example>` tags inside `<examples>`?

**Emphasis:**
- Is bold/caps/CRITICAL reserved for genuinely important items?
- Flag overuse of emphasis that dilutes impact

Score: Flag prompt engineering anti-patterns.

## Step 7: Compile Review

Organize findings into a structured review report. Classify each finding by severity:

| Severity | Meaning |
|----------|---------|
| `blocking` | Prevents the skill from working correctly or violates a core best practice |
| `suggestion` | Improvement that would meaningfully increase quality |
| `nitpick` | Minor polish or stylistic preference |

Determine an overall verdict:

| Condition | Verdict |
|-----------|---------|
| No blocking findings, follows best practices | **Excellent** |
| No blocking findings, some suggestions | **Good** |
| Blocking findings that are easy to fix | **Needs Work** |
| Fundamental structure or approach issues | **Rework** |

## Step 8: Present Review

Display the review using the output format below.

If there are blocking or suggestion findings, ask the user with AskUserQuestion:
- "How would you like to proceed?"
- Options: "Apply fixes automatically", "Show me the fixes first", "Done"

## Step 9: Apply Fixes (if requested)

For each finding the user wants fixed:
1. Show the proposed change (before/after)
2. Apply the edit using the Write or Edit tool
3. Mark the finding as resolved

After applying fixes, re-run the validation from Step 3-6 on modified files to confirm no new issues were introduced.

</process>

<output>

```
## Skill Review: {name}

**Location:** {path}
**Files:** {count} ({list})

---

### Summary

| Severity | Count |
|----------|-------|
| Blocking | {N} |
| Suggestions | {N} |
| Nitpicks | {N} |

---

### Blocking Issues

{N}. **{Title}** — `{file}`: {Description}. **Fix:** {Specific action to resolve}.

---

### Suggestions

{N}. **{Title}** — `{file}`: {Description}. **Fix:** {Specific action to resolve}.

---

### Nitpicks

{N}. **{Title}** — `{file}`: {Description}.

---

### Strengths

- {Positive observation about the skill}
- {Another positive observation}

---

## Verdict: {EXCELLENT | GOOD | NEEDS WORK | REWORK}

{One paragraph summary of the skill's quality, key strengths, and priority improvements.}
```

</output>

<rules>
- Read every file in the skill directory before forming any assessment
- Reference specific files and line content for every finding
- Provide a concrete fix for every blocking and suggestion finding
- Acknowledge strengths alongside areas for improvement
- Score against the quality checklist in the SKILL.md reference
- Use the severity levels consistently: blocking for broken/missing essentials, suggestion for meaningful improvements, nitpick for polish
- Apply fixes only with explicit user confirmation
- Re-validate after applying fixes to confirm no regressions
- Be constructive — frame findings as improvements, not criticisms
</rules>

<examples>

<example>

**Input**: `/create-skill review commit`

**Output**:

## Skill Review: commit

**Location:** .claude/skills/commit/
**Files:** 4 (SKILL.md, create.md, amend.md, interactive.md)

---

### Summary

| Severity | Count |
|----------|-------|
| Blocking | 0 |
| Suggestions | 2 |
| Nitpicks | 1 |

---

### Blocking Issues

None

---

### Suggestions

1. **Missing examples in create.md** — `create.md`: The workflow produces structured commit output but has no `<examples>` section demonstrating expected behavior. Examples would help calibrate output format and tone. **Fix:** Add an `<examples>` section with one standard commit and one multi-commit example.

2. **Broad tool scope on amend workflow** — `SKILL.md`: The `allowed-tools` grants `Bash(git *)` to all workflows, but amend only needs `git commit --amend` and `git log`. Consider whether scoping is feasible at the skill level. **Fix:** Document in amend.md which git commands are expected, even if tool scoping cannot be per-workflow.

---

### Nitpicks

1. **Inconsistent trigger format** — `SKILL.md`: Workflow triggers use quoted strings while the description uses plain text. Minor, but consistency aids readability.

---

### Strengths

- Clean separation of three distinct workflows into dedicated files
- Reference tables for commit types and rules in SKILL.md provide useful shared context
- Process steps are well-numbered with clear decision points for single vs. multi-commit paths

---

## Verdict: GOOD

Solid skill with clear structure and well-defined workflows. Adding examples to workflow files would be the highest-impact improvement for output consistency.

</example>

<example>

**Input**: `/create-skill review deploy`

**Output**:

## Skill Review: deploy

**Location:** .claude/skills/deploy/
**Files:** 2 (SKILL.md, run.md)

---

### Summary

| Severity | Count |
|----------|-------|
| Blocking | 2 |
| Suggestions | 1 |
| Nitpicks | 0 |

---

### Blocking Issues

1. **Missing `disable-model-invocation`** — `SKILL.md`: The skill runs deployment commands (`kubectl apply`, `docker push`) that modify production infrastructure. Auto-invocation could trigger an unintended deployment. **Fix:** Add `disable-model-invocation: true` to frontmatter.

2. **Unscoped Bash in `allowed-tools`** — `SKILL.md`: `allowed-tools: Read, Bash` grants unrestricted shell access. The workflow only uses `kubectl` and `docker` commands. **Fix:** Scope to `Bash(kubectl *), Bash(docker *)`.

---

### Suggestions

1. **Missing `<examples>` in run.md** — `run.md`: The workflow produces structured deployment output but has no examples demonstrating expected results for successful and failed deployments. **Fix:** Add an `<examples>` section with one success and one rollback example.

---

### Nitpicks

None

---

### Strengths

- Clear step-by-step deployment process with rollback instructions
- Pre-deployment checklist validates tests pass before proceeding

---

## Verdict: NEEDS WORK

The skill has a solid deployment workflow but lacks critical safety guardrails. Adding `disable-model-invocation` and scoping Bash access are essential before this skill is safe to use — both are straightforward fixes.

</example>

</examples>
