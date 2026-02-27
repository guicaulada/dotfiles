---
description: Rewrites text to remove AI writing patterns and inject natural human voice
---

<purpose>
Takes text (inline or from a file) and rewrites it to remove AI writing patterns while preserving meaning. Produces a draft, self-audits for remaining tells, then revises. The goal is text that sounds like a specific person wrote it, not just text with AI patterns removed.
</purpose>

<process>

## Checklist

```
Humanize:
- [ ] Step 1: Load text
- [ ] Step 2: Scan for AI patterns
- [ ] Step 3: Draft rewrite
- [ ] Step 4: Self-audit
- [ ] Step 5: Final revision
- [ ] Step 6: Deliver result
```

## Step 1: Load text

If `$ARGUMENTS` is a file path, read the file. Otherwise, treat `$ARGUMENTS` as inline text.

## Step 2: Scan for AI patterns

Load [patterns.md](patterns.md) and scan the text against all 24 patterns. Note every instance found.

## Step 3: Draft rewrite

Rewrite the text, addressing every flagged pattern. While rewriting, inject personality:

- **Vary rhythm.** Mix short punchy sentences with longer ones.
- **Have opinions.** React to facts rather than neutrally listing them.
- **Acknowledge complexity.** Real humans have mixed feelings.
- **Use "I" when appropriate.** First person signals a real person thinking.
- **Be specific.** Replace vague claims with concrete details.
- **Use simple constructions.** Prefer "is/are/has" over "serves as/stands as/features."

Removing AI patterns without adding voice produces sterile text that is equally obvious.

## Step 4: Self-audit

Ask: "What makes this text still obviously AI generated?" List remaining tells as brief bullets.

## Step 5: Final revision

Revise the draft to address the remaining tells from the audit. Ensure the text sounds natural when read aloud.

## Step 6: Deliver result

If the input was a file, write the revised text back. If inline, present the output.

</process>

<output>

For inline text:

```
## Draft

[REWRITTEN_TEXT]

## Audit

Remaining tells:
- [TELL_1]
- [TELL_2]

## Final

[FINAL_REWRITTEN_TEXT]

## Changes

- [CHANGE_SUMMARY_1]
- [CHANGE_SUMMARY_2]
```

For file input:

```
## Changes to [FILE_PATH]

- [CHANGE_SUMMARY_1]
- [CHANGE_SUMMARY_2]

## Audit

Remaining tells addressed:
- [TELL_1]
- [TELL_2]
```

</output>

<rules>

- Preserve the original meaning and factual content
- Match the intended tone (formal, casual, technical) of the surrounding context
- Replace vague claims with specific details where possible; if no specific detail is available, cut the claim rather than inventing one
- Use simple copulas ("is", "are", "has") over elaborate substitutes ("serves as", "stands as")
- Vary sentence length and structure naturally
- Convert inline-header vertical lists to prose when the content allows it
- Use sentence case for headings, not title case
- Replace curly quotes with straight quotes
- Remove emojis unless they serve a clear communicative purpose
- Remove chatbot artifacts ("I hope this helps", "Great question!", "Let me know if...")
- Remove knowledge-cutoff disclaimers ("as of [date]", "based on available information")
- Cut filler phrases rather than shortening them
- Do not invent facts, citations, or named sources to replace vague attributions
- Always complete the self-audit step; never skip it

</rules>

<examples>

<example>

**Input:** "humanize this paragraph"

> AI-assisted coding serves as an enduring testament to the transformative potential of large language models, marking a pivotal moment in the evolution of software development. Additionally, the ability to generate documentation, tests, and refactors showcases how AI can contribute to better outcomes, highlighting the intricate interplay between automation and human judgment.

**Output:**

## Draft

AI coding assistants can generate docs, tests, and simple refactors. They're useful, but they don't replace judgment — you still have to review what they produce.

## Audit

Remaining tells:
- Em dash usage in the second sentence
- Slightly generic closer ("review what they produce")

## Final

AI coding assistants can generate docs, tests, and simple refactors. They're useful, but you still need to read what comes out. I've accepted suggestions that compiled fine and still did the wrong thing.

## Changes

- Removed significance inflation ("enduring testament", "pivotal moment", "evolution of software development")
- Removed copula avoidance ("serves as")
- Removed overused AI vocabulary ("additionally", "showcases", "intricate interplay", "highlighting")
- Removed superficial -ing phrases ("marking", "highlighting")
- Added first-person voice and specific observation
- Replaced em dash with comma in revision

</example>

</examples>
