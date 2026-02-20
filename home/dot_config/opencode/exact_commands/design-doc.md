---
description: Create a design document using Prompt-Driven Development
agent: plan
---

Create a structured design document using Prompt-Driven Development (PDD). Guide the user through iterative refinement of a rough idea into a comprehensive design document with multiple proposals, trade-off analysis, and consensus tracking.

## Process

Follow this iterative process. Do not skip to document generation until the user has reviewed at least one checkpoint.

### Phase 1: Clarify Requirements

Ask targeted questions to understand the problem space. Focus on:

- **What** is the desired outcome?
- **Why** is this needed now? What triggered this?
- **Who** are the stakeholders and users affected?
- **What constraints** exist? (technology, timeline, budget, team)
- **What has been tried** before? What failed and why?

Ask 3-5 questions at a time. Avoid overwhelming the user with too many questions at once.

### Phase 2: Research

Explore the existing codebase and documentation to understand:

- Current architecture and relevant systems
- Existing patterns that the solution should follow or deliberately break from
- Technical constraints discovered from code (dependencies, APIs, data shapes)

Summarize findings and present them to the user before drafting proposals.

### Phase 3: Draft Proposals

Create at least 3 proposals, always starting with "Do Nothing" as Proposal 0:

**Proposal 0: Do Nothing**
- What happens if no action is taken?
- What is the cost of inaction?
- This establishes the baseline for comparison.

**Proposal 1-N: Active Options**
For each proposal, include:
- **Approach**: What would be built or changed
- **Trade-offs**: Pros and cons
- **Effort estimate**: Relative sizing (small/medium/large)
- **Risk**: What could go wrong
- **Dependencies**: What this requires or affects

### Phase 4: Checkpoint Review

Present the draft to the user. Ask:
- Are the proposals covering the right solution space?
- Are there options missing?
- Are the trade-offs accurate?

Iterate based on feedback until the user is satisfied.

### Phase 5: Generate Document

Produce the final design document using this structure:

```markdown
# {Title}

## Background
{1-2 paragraphs setting context. What exists today and why it matters.}

## Problem
{Why action is needed now. What pain points or opportunities exist.}

## Goals
{Numbered list of success criteria, ordered by priority.}

## Non-Goals
{What is explicitly out of scope.}

## Proposals

### Proposal 0: Do Nothing
{Baseline analysis.}

### Proposal 1: {Name}
{Approach, trade-offs, effort, risk, dependencies.}

### Proposal 2: {Name}
{Approach, trade-offs, effort, risk, dependencies.}

## Recommendation
{Which proposal is recommended and why.}

## Open Questions
{Unresolved questions that need further investigation.}

## Consensus
{Decision: pending | accepted | rejected}
{Participants: list of reviewers}
```

## Error Handling

- If requirements are missing, ask targeted follow-up questions before drafting proposals.
- If constraints conflict, surface the conflict explicitly and provide at least two resolution options.
- If codebase context is unavailable, state the limitation and proceed with assumption-based proposals labeled as assumptions.
- If the user asks to skip checkpoint review, provide a concise checkpoint summary first and request explicit confirmation.

$ARGUMENTS
