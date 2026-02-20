---
description: Create an exhaustive structured summary for studying
agent: plan
subtask: true
---

Transform text into an exhaustive, structured bullet-point summary for studying and test preparation. This is a restructuring tool: preserve source details, examples, and nuance without adding opinion.

## Workflow

### Step 1: Accept Input

Determine the source material from the user's input:

- **File path**: Read the file using the Read tool
- **URL**: Fetch the content using WebFetch
- **Pasted text**: Use the text provided directly

If the input is ambiguous, ask the user to clarify the source.

### Step 2: Validate Access and Coverage Strategy

Before analysis, verify the source can be read fully:

- If a file cannot be read, report the path error and ask for a corrected path
- If URL fetch fails or times out, report the failure and ask for a new URL or pasted text
- If the source is too large for one pass, split it into ordered chunks and process all chunks before final output

When chunking is used, keep a coverage log with:

- Chunk count and ordering
- Any skipped or unreadable sections
- Confirmation that final output merges all successfully processed chunks

### Step 3: Analyze and Categorize

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

### Step 4: Produce Summary

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

- Every fact from the successfully processed source content appears in the output
- No interpretation or opinion is added — only restructuring
- Definitions are complete, not abbreviated
- Relationships preserve the directionality from the source (cause → effect, not just "related")
- Categories with no content are omitted (do not include empty sections)
- If chunking was required, include a brief coverage note describing what was processed

## Error Handling

- If the source is missing, unreadable, or unsupported, stop and request a valid source.
- If only partial content is available after retries, clearly label the output as partial and list missing sections.

$ARGUMENTS
