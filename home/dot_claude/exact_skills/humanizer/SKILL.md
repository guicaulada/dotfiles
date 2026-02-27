---
name: humanizer
description: Identifies and removes AI writing patterns from text to restore natural, human voice. Use when user mentions humanize, remove AI patterns, make it sound human, natural writing, AI writing cleanup, or deAI.
allowed-tools: Read, Write, Edit
user-invocable: true
argument-hint: [text or file path]
---

# Humanizer

Rewrites text to remove characteristic AI writing patterns and restore natural human voice. Based on Wikipedia's "Signs of AI writing" catalog (WikiProject AI Cleanup), covering 24 patterns across five categories.

## Pattern Categories

| Category | Patterns | Key Signals |
|---|---|---|
| Content | 1-6 | Significance inflation, promotional tone, vague attribution, formulaic structure |
| Language & Grammar | 7-12 | Overused AI vocabulary, copula avoidance, synonym cycling, false ranges |
| Style | 13-18 | Em dash overuse, mechanical boldface, emoji decoration, title case headings |
| Communication | 19-21 | Chatbot artifacts, knowledge-cutoff disclaimers, sycophantic tone |
| Filler & Hedging | 22-24 | Filler phrases, excessive hedging, generic positive conclusions |

Full pattern reference with before/after examples: [patterns.md](patterns.md).

## Workflow

### Humanize

Trigger: "humanize", "remove AI patterns", "make it sound human", "natural writing", "deAI"

Read and follow [humanize.md](humanize.md).
