---
description: Guides user through PDD process to create a task-based implementation plan
---

<purpose>
Transform a rough idea into a structured, task-based implementation plan using Prompt-Driven Development (PDD). Guide the user through iterative refinement — capturing the idea, clarifying requirements one question at a time, conducting research, and producing an actionable plan with discrete tasks, dependency mapping, acceptance criteria, and demoable increments. Each task should be self-contained enough to be implemented, tested, and demonstrated independently.
</purpose>

<process>

## Checklist

Copy and track progress:

```
Review Progress:
- [ ] Step 1: Capture idea
- [ ] Step 2: Set up directory
- [ ] Step 3: Initial process planning
- [ ] Step 4: Requirements clarification
- [ ] Step 5: Research
- [ ] Step 6: Iteration checkpoint
- [ ] Step 7: Generate implementation plan
- [ ] Step 8: Refine
```

## Step 1: Capture Idea

Get the rough idea from the user. Support multiple input methods:

- **Direct text** provided in conversation
- **File path** to a local file containing the idea
- **URL** to a resource describing the idea
- **Design document** from a previous `/design-doc` session

Ask for all required parameters upfront in a single prompt:

- `ROUGH_IDEA` (required) — the initial concept or design document
- `PROJECT_DIR` (optional, default: `.impl-plans/[slug]`) — directory for artifacts

If the default `.impl-plans/` directory already exists with contents, ask the user for an explicit project directory to avoid overwriting previous work.

## Step 2: Set Up Directory

Create the project structure at `PROJECT_DIR`:

```
{PROJECT_DIR}/
├── rough-idea.md          # Original idea as provided
├── idea-honing.md         # Requirements Q&A log
├── research/              # Research notes by topic
└── plan/                  # Implementation plan artifacts
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
- Focus on: scope boundaries, technical constraints, integration points, testing strategy, dependencies on external systems, success criteria, risk areas, ordering preferences, delivery milestones
- Continue until sufficient detail is gathered
- Explicitly ask if clarification is complete before moving on
- Offer to conduct research if questions arise that need investigation

## Step 5: Research

Conduct targeted research to inform the implementation plan:

- Identify research areas based on requirements
- Propose a research plan and ask for user input on topics and resources
- Focus on implementation feasibility: how similar problems have been solved, available libraries and tools, existing codebase patterns, API documentation, and known pitfalls
- Document findings in `{PROJECT_DIR}/research/` as separate topic files
- Include links to references and sources
- Check in with the user periodically to share findings and confirm direction
- Summarize key findings that will inform the implementation plan
- Ask if research is sufficient before proceeding

## Step 6: Iteration Checkpoint

Summarize current state of requirements and research. Ask the user:

- **Proceed to planning** — requirements and research are sufficient
- **Return to clarification** — new questions emerged from research
- **More research** — additional topics need investigation

Support iterating between clarification and research as many times as needed. Do NOT proceed to planning without explicit user confirmation.

## Step 7: Generate Implementation Plan

Create `{PROJECT_DIR}/plan/implementation-plan.md` using the template below. The plan must:

- Break work into discrete, independently implementable tasks
- Order tasks so each builds incrementally on previous work
- Ensure core end-to-end functionality is available as early as possible
- Include acceptance criteria and demo description for every task
- Map dependencies between tasks
- Identify risks and mitigations

### Implementation Plan Template

```markdown
# Implementation Plan: [TITLE]

## Overview

[1-2 paragraphs describing what is being built and the implementation approach.
Reference the rough idea and key decisions from requirements clarification.]

## Requirements Summary

[Consolidated requirements from idea-honing. Organized by category.]

### Functional Requirements

- [REQUIREMENT_1]
- [REQUIREMENT_2]

### Non-Functional Requirements

- [REQUIREMENT_1]
- [REQUIREMENT_2]

### Constraints

- [CONSTRAINT_1]
- [CONSTRAINT_2]

### Out of Scope

- [NON_GOAL_1]
- [NON_GOAL_2]

## Architecture Notes

[Key technical decisions that inform the implementation plan.
Include technology choices, patterns, and integration points.
Reference research findings where applicable.]

## Task Breakdown

### Task 1: [TITLE]

**Objective:** [What this task accomplishes]

**Details:**

- [Implementation guidance]
- [Key considerations]

**Acceptance Criteria:**

- [ ] [TESTABLE_CRITERION_1]
- [ ] [TESTABLE_CRITERION_2]

**Demo:** [What working functionality can be demonstrated after this task]

**Depends on:** None

---

### Task 2: [TITLE]

**Objective:** [What this task accomplishes]

**Details:**

- [Implementation guidance]
- [Key considerations]

**Acceptance Criteria:**

- [ ] [TESTABLE_CRITERION_1]
- [ ] [TESTABLE_CRITERION_2]

**Demo:** [What working functionality can be demonstrated after this task]

**Depends on:** Task 1

---

[Continue for all tasks...]

## Dependency Map

| Task | Depends On | Blocks |
|------|------------|--------|
| 1    | —          | 2, 3   |
| 2    | 1          | 4      |
| 3    | 1          | 4      |
| 4    | 2, 3       | —      |

## Risk Register

| Risk     | Likelihood      | Impact          | Mitigation   |
|----------|-----------------|-----------------|--------------|
| [RISK_1] | Low/Medium/High | Low/Medium/High | [MITIGATION] |
| [RISK_2] | Low/Medium/High | Low/Medium/High | [MITIGATION] |

## Progress Checklist

- [ ] Task 1: [TITLE]
- [ ] Task 2: [TITLE]
- [ ] Task 3: [TITLE]
- [ ] ...
```

Review the plan with the user and iterate based on feedback.

## Step 8: Refine

Iterate with the user until the implementation plan is approved:

- Accept feedback on any section
- Add, remove, split, or merge tasks as requested
- Adjust task ordering and dependencies
- Update acceptance criteria based on discussion
- Refine risk register based on new insights

</process>

<output>

Present a summary after generating the implementation plan:

```
## Implementation Plan Summary

**Title:** [PLAN_TITLE]
**Location:** [PROJECT_DIR]/plan/implementation-plan.md
**Status:** Ready for Review

### Tasks
| #   | Title   | Depends On | Demo         |
|-----|---------|------------|--------------|
| 1   | [TITLE] | —          | [BRIEF_DEMO] |
| 2   | [TITLE] | 1          | [BRIEF_DEMO] |
| 3   | [TITLE] | 1          | [BRIEF_DEMO] |
| ... | ...     | ...        | ...          |

### Risks
- [TOP_RISK_1]: [MITIGATION]
- [TOP_RISK_2]: [MITIGATION]

### Artifacts
- [PROJECT_DIR]/rough-idea.md
- [PROJECT_DIR]/idea-honing.md
- [PROJECT_DIR]/research/*.md
- [PROJECT_DIR]/plan/implementation-plan.md

### Next Steps
- Review the plan and refine as needed
- Begin implementation starting with Task 1
- Track progress using the checklist in the plan
```

</output>

<rules>

- Always ask ONE question at a time during requirements clarification
- Never proceed to the next phase without explicit user confirmation
- Every task must have acceptance criteria with testable conditions
- Every task must include a demo description showing demoable functionality
- Every task must build incrementally on previous tasks — no orphaned work
- Core end-to-end functionality must be available as early as possible in the task sequence
- Tasks must be ordered to minimize blocked work and maximize parallel opportunities
- Map all task dependencies explicitly in the dependency table
- Include a risk register with at least the top identified risks
- Never overwrite an existing project directory without asking
- Save all artifacts to the project directory for traceability
- Keep the user in control — they decide when to move between phases
- Focus questions on implementation concerns: scope, integration, testing, risk, dependencies
- When requirements clarification stalls, suggest moving to a different aspect or conducting research to unblock
- When research hits a dead end, document what is missing and continue with available information
- When the plan grows too complex, suggest grouping tasks into phases or milestones and prioritizing core functionality
- When task dependencies are unclear, ask the user about preferred implementation sequence and minimize artificial serialization

</rules>

<examples>

<example>

**Input**: "I need a plan to add rate limiting to our REST API"

**Step 1-2 output** (after capturing idea and setting up directory):

I've saved your idea and created the project structure at `.impl-plans/api-rate-limiting/`.

Before we dive into refining the requirements, how would you like to start?

- **Requirements clarification** — I'll ask you questions one at a time to flesh out the details
- **Preliminary research** — I can investigate rate limiting patterns, middleware options, or your existing API code first
- **Provide additional context** — Share more details about the API or constraints before we begin

**Step 7 output** (implementation plan excerpt):

```markdown
# Implementation Plan: API Rate Limiting

## Overview

Add rate limiting to the REST API to protect against abuse and ensure
fair resource allocation across clients. The approach uses a token bucket
algorithm with Redis-backed storage for distributed rate tracking.

## Requirements Summary

### Functional Requirements

- Rate limit by API key with configurable limits per endpoint
- Return standard 429 responses with Retry-After header
- Support burst allowance above steady-state rate

### Non-Functional Requirements

- Sub-5ms overhead per request at p99
- Graceful degradation if Redis is unavailable (allow traffic)

### Constraints

- Must work with the existing Express middleware stack
- Redis 7.x already available in infrastructure

### Out of Scope

- Per-user rate limiting (only per API key)
- Rate limit dashboard or analytics

## Task Breakdown

### Task 1: Token Bucket Core Library

**Objective:** Implement the token bucket algorithm as a standalone module
with in-memory storage.

**Details:**

- Create `src/rate-limit/token-bucket.ts` with configurable rate and burst
- Use a storage interface to decouple algorithm from backing store
- Include time-based token replenishment logic

**Acceptance Criteria:**

- [ ] Token bucket correctly limits requests at the configured rate
- [ ] Burst allowance permits short spikes above steady-state
- [ ] Unit tests cover steady-state, burst, and exhaustion scenarios

**Demo:** Run unit tests showing requests allowed up to the limit,
then rejected, then allowed again after replenishment.

**Depends on:** None

---

### Task 2: Redis Storage Adapter

**Objective:** Implement a Redis-backed storage adapter for distributed
rate tracking across API instances.

**Details:**

- Create `src/rate-limit/redis-store.ts` implementing the storage interface
- Use Lua scripts for atomic check-and-decrement operations
- Add fallback to allow-all when Redis is unreachable

**Acceptance Criteria:**

- [ ] Rate state is shared across multiple API instances
- [ ] Atomic operations prevent race conditions under concurrent load
- [ ] Graceful degradation allows all traffic when Redis is down

**Demo:** Start two API instances, show that rate limits are shared.
Disconnect Redis, show requests continue to be served.

**Depends on:** Task 1

---

### Task 3: Express Middleware Integration

**Objective:** Wire the rate limiter into the Express middleware stack
with per-endpoint configuration.

**Details:**

- Create `src/middleware/rate-limit.ts` that reads API key from headers
- Load per-endpoint limits from configuration
- Set 429 status and Retry-After header on rejection

**Acceptance Criteria:**

- [ ] Middleware extracts API key and applies correct per-endpoint limits
- [ ] 429 response includes accurate Retry-After header
- [ ] Integration tests verify end-to-end rate limiting behavior

**Demo:** curl the API with a test key, exceed the limit, show 429
response with Retry-After header.

**Depends on:** Task 1, Task 2

## Dependency Map

| Task | Depends On | Blocks |
|------|------------|--------|
| 1    | —          | 2, 3   |
| 2    | 1          | 3      |
| 3    | 1, 2       | —      |

## Risk Register

| Risk                                           | Likelihood | Impact | Mitigation                                           |
|------------------------------------------------|------------|--------|------------------------------------------------------|
| Redis latency adds unacceptable overhead       | Low        | High   | Benchmark in staging; local cache fallback if needed |
| Lua script compatibility across Redis versions | Low        | Medium | Test against Redis 7.x in CI                         |

## Progress Checklist

- [ ] Task 1: Token Bucket Core Library
- [ ] Task 2: Redis Storage Adapter
- [ ] Task 3: Express Middleware Integration
```

</example>

<example>

**Input**: "/impl-plan @docs/design/notification-system.md" (design doc as input)

**Step 1-2 output** (after capturing idea and setting up directory):

I've read your design document and saved it to `.impl-plans/notification-system/rough-idea.md`.

The design doc covers a notification system with email, push, and in-app channels. Before we plan the implementation, how would you like to start?

- **Requirements clarification** — I'll ask questions one at a time to fill in implementation details the design doc doesn't cover
- **Preliminary research** — I can investigate notification libraries, queue systems, or your existing infrastructure first
- **Provide additional context** — Share more about current systems or constraints

**Step 7 output** (implementation plan excerpt):

```markdown
# Implementation Plan: Multi-Channel Notification System

## Overview

Implement a notification system supporting email, push, and in-app channels
based on the approved design document. Uses an event-driven architecture
with a message queue for reliable delivery and per-channel adapters.

## Requirements Summary

### Functional Requirements

- Send notifications via email, push, and in-app channels
- Support user notification preferences (opt-in/out per channel)
- Retry failed deliveries with exponential backoff

### Non-Functional Requirements

- Process notifications within 30 seconds of trigger event
- Handle 1000 notifications/minute at peak

### Constraints

- Use existing RabbitMQ infrastructure for message queuing
- Email via SendGrid API (already configured)

### Out of Scope

- SMS channel (future phase)
- Notification templates editor UI

## Task Breakdown

### Task 1: Notification Event Schema and Queue Setup

**Objective:** Define the notification event schema and configure
RabbitMQ queues for routing notifications to channel processors.

**Details:**

- Define TypeScript interfaces for notification events
- Create RabbitMQ exchange with routing keys per channel
- Set up dead-letter queue for failed deliveries

**Acceptance Criteria:**

- [ ] Notification event schema validates required fields
- [ ] Messages route to correct channel queue based on routing key
- [ ] Failed messages land in dead-letter queue after max retries

**Demo:** Publish a test notification event, show it routed to the
correct channel queue. Publish a malformed event, show it rejected.

**Depends on:** None

---

### Task 2: In-App Notification Channel

**Objective:** Implement the in-app channel as the first adapter,
establishing the adapter pattern for other channels.

**Details:**

- Create channel adapter interface that all channels implement
- Implement in-app adapter storing notifications in the database
- Add REST endpoint for fetching user notifications

**Acceptance Criteria:**

- [ ] In-app adapter implements the channel adapter interface
- [ ] Notifications persisted to database with read/unread status
- [ ] GET endpoint returns paginated notifications for a user

**Demo:** Trigger a notification, fetch it via the API, mark as read.

**Depends on:** Task 1

## Dependency Map

| Task | Depends On | Blocks |
|------|------------|--------|
| 1    | —          | 2      |
| 2    | 1          | —      |

## Risk Register

| Risk                                     | Likelihood | Impact | Mitigation                                                   |
|------------------------------------------|------------|--------|--------------------------------------------------------------|
| RabbitMQ message ordering not guaranteed | Medium     | Medium | Design consumers to be idempotent; use message timestamps    |
| SendGrid rate limits during peak         | Low        | High   | Implement send queue with rate limiting; monitor quota usage |

## Progress Checklist

- [ ] Task 1: Notification Event Schema and Queue Setup
- [ ] Task 2: In-App Notification Channel
```

</example>

</examples>
