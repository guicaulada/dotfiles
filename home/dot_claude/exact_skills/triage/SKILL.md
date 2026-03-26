---
name: triage
description: Fetches GitHub issues, pull requests, reviews, notifications, and project board data for the user and optionally teammates, then analyzes their state and produces a prioritized work plan. Use when prioritizing work, triaging GitHub activity, planning what to work on next, assessing current workload, checking sprint status, or reviewing project board items. Supports teammate usernames and focus areas via arguments. Do NOT use for creating, modifying, or closing issues, PRs, or other GitHub resources.
allowed-tools: Bash(gh *)
argument-hint: [optional focus or context]
---

# Work Triage

Analyzes GitHub activity to produce a prioritized work plan. Gathers issues, PRs, reviews, notifications, and project context, then presents actionable priorities.

## Workflows

### Triage

Trigger: "triage", "prioritize", "what should I work on", "plan my day", "what's on my plate", "workload"

Read and follow [triage.md](triage.md).
