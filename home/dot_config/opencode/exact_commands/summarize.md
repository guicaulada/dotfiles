---
description: Create an exhaustive structured summary for studying
agent: plan
subtask: true
---

Transform text into an exhaustive, structured bullet-point summary that captures every detail for studying and test preparation. This is a restructuring tool — every fact, detail, example, and nuance from the source material appears in the output. Nothing is omitted.

## Workflow

### Step 1: Accept Input

Determine the source material from the user's input:

- **File path**: Read the file using the Read tool
- **URL**: Fetch the content using WebFetch
- **Pasted text**: Use the text provided directly

If the input is ambiguous, ask the user to clarify the source.

### Step 2: Analyze and Categorize

Read through the entire source material. Classify every piece of information into one of these categories:

| Category | What to Include |
|----------|----------------|
| **Core Concepts** | Main ideas, theories, frameworks, models |
| **Key Terms & Definitions** | Vocabulary with complete definitions in context |
| **Facts & Details** | Specific data points, numbers, dates, names to memorize |
| **Relationships & Connections** | How concepts relate, cause and effect chains, comparisons |
| **Examples & Applications** | Concrete illustrations, case studies, real-world uses |
| **Exceptions & Edge Cases** | Special cases, caveats, "except when" rules |
| **Summary Points** | Main conclusions, key takeaways, thesis statements |

### Step 3: Produce Summary

Output the summary using this format:

```markdown
# Summary: {Source Title or Description}

## Core Concepts
- {Main idea with full explanation}
  - {Supporting detail}
  - {Supporting detail}

## Key Terms & Definitions
- **{Term}**: {Complete definition as used in the source}

## Facts & Details
- {Specific fact or data point}

## Relationships & Connections
- {Concept A} → {Concept B}: {How they relate and why}

## Examples & Applications
- {Example}: {What it illustrates}

## Exceptions & Edge Cases
- {Exception}: {When and why it applies}

## Summary Points
- {Key takeaway}
```

### Quality Checks

Before returning the summary, verify:

- Every fact from the source material appears in the output
- No interpretation or opinion is added — only restructuring
- Definitions are complete, not abbreviated
- Relationships preserve the directionality from the source (cause → effect, not just "related")
- Categories with no content are omitted (do not include empty sections)

$ARGUMENTS
