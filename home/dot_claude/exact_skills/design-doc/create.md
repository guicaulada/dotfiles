---
description: Guides user through PDD process to create a structured design document
---

<purpose>
Transform a rough idea into a structured design document using Prompt-Driven Development (PDD). Guide the user through iterative refinement — capturing the idea, clarifying requirements one question at a time, conducting research, and producing a design document with multiple proposals and trade-off analysis. Output must be Google Docs compatible (no ASCII art, no Mermaid diagrams).
</purpose>

<process>

## Checklist

Copy and track progress:

```
Design Doc Progress:
- [ ] Step 1: Capture idea
- [ ] Step 2: Set up directory
- [ ] Step 3: Initial process planning
- [ ] Step 4: Requirements clarification
- [ ] Step 5: Research
- [ ] Step 6: Iteration checkpoint
- [ ] Step 7: Generate design document
- [ ] Step 8: Refine
```

## Step 1: Capture Idea

Get the rough idea from the user. Support multiple input methods:

- **Direct text** provided in conversation
- **File path** to a local file containing the idea
- **URL** to a resource describing the idea

Ask for all required parameters upfront in a single prompt:

- `ROUGH_IDEA` (required) — the initial concept
- `PROJECT_DIR` (optional, default: `.design-docs/[slug]`) — directory for artifacts

If the default `.design-docs/` directory already exists with contents, ask the user for an explicit project directory to avoid overwriting previous work.

## Step 2: Set Up Directory

Create the project structure at `PROJECT_DIR`:

```
{PROJECT_DIR}/
├── rough-idea.md          # Original idea as provided
├── idea-honing.md         # Requirements Q&A log
├── research/              # Research notes by topic
├── design/                # Design documents
└── implementation/        # Implementation plans
```

Save the rough idea to `{PROJECT_DIR}/rough-idea.md`.

## Step 3: Initial Process Planning

Ask the user their preferred starting point:

- **Requirements clarification** (default) — refine the idea through questions
- **Preliminary research** — investigate specific topics first
- **Provide additional context** — share more information before proceeding

Explain the process is iterative — they can move between clarification and research at any time. Wait for explicit user direction before proceeding.

## Step 4: Requirements Clarification

Refine the idea through iterative questioning:

- Ask **ONE question at a time** and wait for the response
- Do NOT list multiple questions at once
- Do NOT pre-populate answers without user input
- For each question:
  1. Formulate a single question
  2. Append the question to `{PROJECT_DIR}/idea-honing.md`
  3. Present it to the user
  4. Wait for their complete response (may take multiple turns)
  5. Append the answer to `{PROJECT_DIR}/idea-honing.md`
  6. Proceed to the next question
- A user's response may span multiple turns of brief back-and-forth dialogue — wait for their complete answer before recording it
- Cover: edge cases, user experience, technical constraints, success criteria
- Continue until sufficient detail is gathered
- Explicitly ask if clarification is complete before moving on
- Offer to conduct research if questions arise that need investigation

## Step 5: Research

Conduct targeted research to inform the design:

- Identify research areas based on requirements
- Propose a research plan and ask for user input on topics and resources
- Document findings in `{PROJECT_DIR}/research/` as separate topic files
- Use prose descriptions and tables (NO Mermaid diagrams — Google Docs constraint)
- Include links to references and sources
- Check in with the user periodically to share findings and confirm direction
- Summarize key findings that will inform the design
- Ask if research is sufficient before proceeding

## Step 6: Iteration Checkpoint

Summarize current state of requirements and research. Ask the user:

- **Proceed to design** — requirements and research are sufficient
- **Return to clarification** — new questions emerged from research
- **More research** — additional topics need investigation

Support iterating between clarification and research as many times as needed. Do NOT proceed to design without explicit user confirmation.

## Step 7: Generate Design Document

Create `{PROJECT_DIR}/design/design-doc.md` using the template below. The document must:

- Stand alone — readable without other project files
- Include at least Proposal 0 (Do nothing) plus 2 real alternatives
- Each proposal must have benefits AND trade-offs
- Use prose and tables only (NO ASCII art, NO Mermaid — Google Docs constraint)

### Design Doc Template

```markdown
# [TITLE]

## Background

[1-2 paragraphs setting context. Include key facts and link to relevant
documents or code. Keep concise.]

## Problem

[1-2 paragraphs explaining why this is a problem now or will be in the
future. Make the case for why action is needed.]

## Goals

- Primary goal: [MAIN_OUTCOME]
- Secondary goal: [ADDITIONAL_OUTCOME]
- Non-goals: [EXPLICITLY_OUT_OF_SCOPE]

## Proposals

### Proposal 0: Do nothing

[Describe what happens if we take no action. This establishes the baseline.]

**Impact:**

- [CONSEQUENCE_1]
- [CONSEQUENCE_2]

**When this makes sense:**

- [CONDITION_WHERE_INACTION_IS_OK]

### Proposal 1: [TITLE]

[Describe the proposal and how it addresses the problem.]

**Approach:**

- [KEY_ELEMENT_1]
- [KEY_ELEMENT_2]

**Benefits:**

- [BENEFIT_1]
- [BENEFIT_2]

**Trade-offs:**

- [TRADEOFF_1]
- [TRADEOFF_2]

**Effort:** [LOW/MEDIUM/HIGH]

### Proposal 2: [TITLE]

[Second proposal with different trade-offs. Add more as appropriate.]

## Consensus

**Status:** Draft - Pending Review

**Recommended approach:** [PROPOSAL_N] - [BRIEF_RATIONALE]

**Decision:** [TO_BE_FILLED]

**Participants:**

- [TO_BE_FILLED]

**Discussion notes:**

- [TO_BE_FILLED_AFTER_REVIEW]

## Other Notes

### References

- [RELEVANT_LINK_1]

### Open Questions

- [QUESTION_1]
```

Review the document with the user and iterate based on feedback.

## Step 8: Refine

Iterate with the user until the design document is approved:

- Accept feedback on any section
- Add or modify proposals as requested
- Update trade-off analysis based on discussion
- Finalize the consensus section once agreement is reached

</process>

<output>

Present a summary after generating the design document:

```
## Design Document Summary

**Title:** [DOCUMENT_TITLE]
**Location:** [PROJECT_DIR]/design/design-doc.md
**Status:** Ready for Review

### Proposals
| # | Title      | Effort   | Recommendation |
|---|------------|----------|----------------|
| 0 | Do nothing | -        | Baseline       |
| 1 | [TITLE]    | [EFFORT] | [RECOMMENDED?] |
| 2 | [TITLE]    | [EFFORT] |                |

### Artifacts
- [PROJECT_DIR]/rough-idea.md
- [PROJECT_DIR]/idea-honing.md
- [PROJECT_DIR]/research/*.md
- [PROJECT_DIR]/design/design-doc.md

### Next Steps
- Share document with stakeholders
- Update Consensus section after review
- Begin implementation once decision is made
```

</output>

<rules>

- Always ask ONE question at a time during requirements clarification
- Never proceed to the next phase without explicit user confirmation
- Always include "Do nothing" as Proposal 0
- Always include at least 2 real alternative proposals beyond "Do nothing"
- Every proposal must include both benefits AND trade-offs
- Output must be Google Docs compatible — NO ASCII art, NO Mermaid diagrams, NO code block visuals
- Use prose descriptions, bullet lists, and tables for all structural representation
- Never overwrite an existing project directory without asking
- Save all artifacts to the project directory for traceability
- Keep the user in control — they decide when to move between phases
- When requirements clarification stalls, suggest moving to a different aspect or conducting research to unblock
- When research hits a dead end, document what is missing and continue with available information
- When the design grows too complex, suggest breaking it into smaller components and prioritizing core functionality

</rules>

<examples>

<example>

**Input**: "I want to design a notification system for our internal dashboard"

**Step 1-2 output** (after capturing idea and setting up directory):

I've saved your idea and created the project structure at `.design-docs/notification-system/`.

Before we dive into refining the requirements, how would you like to start?

- **Requirements clarification** — I'll ask you questions one at a time to flesh out the details
- **Preliminary research** — I can investigate notification patterns, delivery mechanisms, or your existing dashboard code first
- **Provide additional context** — Share more details about the dashboard or constraints before we begin

**Step 7 output** (design document excerpt):

```markdown
# Notification System for Internal Dashboard

## Background

The internal dashboard serves 50+ team members for daily operations monitoring.
Currently, users must manually check the dashboard for updates, leading to missed
alerts and delayed responses to critical events.

## Problem

Teams frequently miss time-sensitive updates because the dashboard has no push
notification capability. This has led to delayed incident response on at least
three occasions in the past quarter.

## Goals

- Primary goal: Deliver real-time notifications for critical dashboard events
- Secondary goal: Support user-configurable notification preferences
- Non-goals: External notification channels (SMS, phone calls), notification analytics

## Proposals

### Proposal 0: Do nothing

Continue with the current manual-check workflow.

**Impact:**

- Missed alerts continue at current rate
- Team relies on ad-hoc Slack messages for urgent items

**When this makes sense:**

- Dashboard usage is declining or being replaced

### Proposal 1: Browser Push Notifications

Use the Web Push API to deliver native browser notifications.

**Approach:**

- Register a service worker for push subscription management
- Add notification preferences UI to user settings
- Create a server-side event dispatcher for triggered alerts

**Benefits:**

- Works even when the dashboard tab is in the background
- Native OS integration (notification center, sounds)

**Trade-offs:**

- Requires browser permission grant from each user
- Limited formatting options in notification payload

**Effort:** Medium

### Proposal 2: In-App Notification Center

Add a notification panel within the dashboard with a bell icon and unread count.

**Approach:**

- Server-Sent Events (SSE) connection for real-time delivery
- Notification center component with read/unread state
- Persistent storage for notification history

**Benefits:**

- Works without browser permissions
- Rich formatting and actionable notifications

**Trade-offs:**

- Only visible when the dashboard tab is active
- Adds persistent connection overhead per user

**Effort:** Medium

## Consensus

**Status:** Draft - Pending Review
**Recommended approach:** Proposal 1 - Browser push notifications address the core
problem of missed alerts even when the dashboard is not in focus.
```

</example>

<example>

**Input**: "I want to explore options for migrating our monolith to microservices" (user chooses to start with research)

**Step 1-2 output** (after capturing idea and setting up directory):

I've saved your idea and created the project structure at `.design-docs/monolith-migration/`.

Before we dive into refining the requirements, how would you like to start?

- **Requirements clarification** — I'll ask you questions one at a time to flesh out the details
- **Preliminary research** — I can investigate migration patterns, service boundaries, or your existing architecture first
- **Provide additional context** — Share more details about the monolith or constraints before we begin

**Step 5 output** (after user chose preliminary research):

I've documented my findings in `.design-docs/monolith-migration/research/`:

- `migration-patterns.md` — Strangler Fig, Branch by Abstraction, and parallel-run patterns with comparison table
- `service-boundaries.md` — Domain analysis of your codebase identifying candidate service boundaries

Key findings:

- The authentication module has the cleanest boundaries and fewest cross-dependencies — strongest candidate for first extraction
- The reporting module shares database tables with three other modules — high coupling makes it a poor early candidate

Want me to investigate any other topics, or are we ready to move to requirements clarification?

**Step 6 output** (iteration checkpoint after research + clarification):

Here's where we stand:

**Requirements gathered:** Target architecture (event-driven), performance SLAs (p99 < 200ms), team capacity (2 engineers, 3 months), data consistency model (eventual OK for reporting, strong for auth)

**Research completed:** Migration patterns, service boundary analysis, team case studies

Ready to proceed? Options:

- **Proceed to design** — requirements and research are sufficient
- **Return to clarification** — new questions emerged from research
- **More research** — additional topics need investigation

</example>

</examples>
