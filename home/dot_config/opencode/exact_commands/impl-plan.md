---
description: Create a task-based implementation plan
agent: plan
---

Create a structured, task-based implementation plan using Prompt-Driven Development (PDD). Guide the user through iterative refinement of a rough idea into an actionable plan with discrete tasks, dependency mapping, and demoable increments.

## Process

Follow this iterative process. Do not skip to plan generation until the user has reviewed at least one checkpoint.

### Phase 1: Clarify Requirements

Ask targeted questions to understand the implementation scope:

- **What** is the desired end state?
- **What** existing systems or code will be affected?
- **What constraints** apply? (stack, libraries, patterns, performance)
- **What** is the acceptance criteria for "done"?
- **What** is explicitly out of scope?

Ask 3-5 questions at a time. Gather enough detail to break the work into concrete tasks.

### Phase 2: Research

Explore the existing codebase and architecture to understand:

- Current patterns and conventions that tasks should follow
- Integration points and data shapes
- Test infrastructure and coverage expectations
- Build and deployment pipeline considerations

Summarize findings before proposing the task breakdown.

### Phase 3: Break Down Tasks

Create discrete, demoable tasks. Each task should:

- Be completable independently (or only depend on previously listed tasks)
- Produce a visible or testable result when done
- Take no more than a few hours of focused work

Use this format for each task:

```markdown
### Task {N}: {Title}

**Objective:** {What this task accomplishes}

**Files affected:**
- {path/to/file.ts} — {what changes}

**Steps:**
1. {Concrete implementation step}
2. {Concrete implementation step}

**Acceptance criteria:**
- [ ] {Observable, testable condition}
- [ ] {Observable, testable condition}

**Depends on:** {Task numbers or "None"}
**Estimate:** {small | medium | large}
```

### Phase 4: Map Dependencies

Create a dependency map showing:

- Which tasks can run in parallel
- Which tasks block others
- The critical path (longest chain of sequential dependencies)

Present this as a simple list:

```
Task 1 (no deps) ─┬─ Task 2 (depends on 1) ── Task 4 (depends on 2)
                   └─ Task 3 (depends on 1) ── Task 5 (depends on 3)
```

### Phase 5: Checkpoint Review

Present the plan to the user. Ask:
- Are the tasks scoped correctly?
- Are there missing tasks or unnecessary ones?
- Is the ordering and dependency mapping correct?

Iterate based on feedback.

### Phase 6: Generate Plan

Produce the final implementation plan:

```markdown
# Implementation Plan: {Title}

## Overview
{1-2 paragraphs describing the goal and approach.}

## Requirements
{Consolidated list from the clarification phase.}

## Architecture Notes
{Key technical decisions that inform the task breakdown.}

## Task Breakdown

{Tasks in execution order, using the format from Phase 3.}

## Dependency Map

{Visual dependency map from Phase 4.}

## Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| {risk} | {high/medium/low} | {high/medium/low} | {mitigation strategy} |

## Summary

- **Total tasks:** {N}
- **Critical path:** {task chain}
- **Estimated effort:** {total relative sizing}
- **Parallel tracks:** {N independent streams}
```

## Error Handling

- If requirements are ambiguous, ask focused clarification questions before creating tasks.
- If repository context cannot be inspected, label architecture assumptions explicitly and continue with best-effort planning.
- If dependencies between tasks are uncertain, mark them as tentative and call out validation steps.
- If requested scope is too broad for one plan, split into phased plans and identify a first shippable increment.

$ARGUMENTS
