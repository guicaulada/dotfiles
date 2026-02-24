---
name: design-doc
description: Creates design documents using Prompt-Driven Development to refine ideas into structured proposals. Use when user mentions design doc, design document, RFC, technical proposal, architecture proposal, write a proposal, or PDD.
allowed-tools: Read, Write, Bash(mkdir *), Glob, Grep, WebSearch
argument-hint: [topic or rough idea]
---

# Design Doc Skill

Create structured design documents using Prompt-Driven Development (PDD). Guides users through iterative refinement of rough ideas into comprehensive design documents with multiple proposals, trade-off analysis, and consensus tracking.

## Document Structure

| Section    | Purpose                                 |
| ---------- | --------------------------------------- |
| Background | Sets context in 1-2 paragraphs          |
| Problem    | Explains why action is needed now       |
| Goals      | Defines success criteria and priorities |
| Proposals  | At least 2-3 options with trade-offs    |
| Do Nothing | Always included as Proposal 0 baseline  |
| Consensus  | Documents decision and participants     |

## PDD Methodology

The skill follows the Prompt-Driven Development methodology — iterative refinement through requirements clarification, research, and checkpoint reviews before generating the design document. The full process is embedded in the create workflow.

## Workflows

### Create Design Document

Trigger: "design doc", "design document", "RFC", "technical proposal", "architecture proposal", "write a proposal", "PDD"

Read and follow `create.md`.
