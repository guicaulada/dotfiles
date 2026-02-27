---
name: impl-plan
description: Creates task-based implementation plans using Prompt-Driven Development to refine ideas into actionable plans with dependency mapping, risk registers, and demoable increments. Use when user mentions implementation plan, impl plan, create plan, build plan, development plan, breakdown tasks, task plan, sprint plan, or plan implementation. Do NOT use for general conversation about plans, scheduling, or project management without implementation context.
argument-hint: [idea or file path]
allowed-tools: Read, Write, Bash(mkdir *), Glob, Grep, WebSearch, WebFetch
---

# Implementation Plan Skill

## Plan Structure

| Section            | Purpose                                               |
|--------------------|-------------------------------------------------------|
| Overview           | Sets context and defines the goal                     |
| Requirements       | Consolidated requirements from clarification          |
| Architecture Notes | Key technical decisions informing the plan            |
| Task Breakdown     | Ordered tasks with objectives and acceptance criteria |
| Dependency Map     | Task dependencies and critical path                   |
| Risk Register      | Identified risks and mitigations                      |

## PDD Methodology

The skill follows the Prompt-Driven Development methodology — iterative refinement through requirements clarification, research, and checkpoint reviews before generating the implementation plan. The full process is embedded in the create workflow.

## Workflows

### Create Implementation Plan

Trigger: "impl plan", "implementation plan", "create plan", "build plan", "development plan", "breakdown tasks", "task plan", "sprint plan", "plan implementation"

Read and follow [create.md](create.md).
