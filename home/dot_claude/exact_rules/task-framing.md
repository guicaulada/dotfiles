# Task Framing

Clear task framing reduces ambiguity, prevents wasted effort, and ensures the implementation matches expectations. Use this framework when receiving complex or underspecified tasks.

## Framework

Clarify these dimensions before starting implementation:

### Goal
What should be accomplished? Define the desired outcome in concrete terms.

### Constraints
What boundaries apply? Technology stack, libraries, patterns, performance requirements, or other non-negotiables.

### Context
What existing code, APIs, data shapes, or systems are relevant? Identify the files and modules that will be affected.

### Acceptance Criteria
How will success be verified? Define observable, testable conditions that confirm the task is complete.

### Non-Goals
What is explicitly out of scope? Stating what to avoid prevents scope creep and over-engineering.

## When to Use

- The task involves multiple approaches and the right one is unclear
- Requirements are ambiguous or incomplete
- The change touches multiple systems or has significant blast radius
- Stakeholders may have different expectations about the outcome

## Applying the Framework

- Ask clarifying questions early rather than making assumptions
- Document the framing in the PR description or issue for future reference
- Revisit the framing if scope changes during implementation
- If the current approach hits unexpected friction, stop and re-plan rather than pushing through
