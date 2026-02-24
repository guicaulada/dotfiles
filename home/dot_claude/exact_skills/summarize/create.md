---
description: Transform text into exhaustive structured bullet-point summaries for studying and test preparation
---

<purpose>

Restructure content into a scannable study-ready format that:

- Captures 100% of the source content — nothing is omitted
- Organizes information under clear categorical headings
- Preserves all facts, terms, definitions, numbers, dates, and relationships exactly
- Facilitates systematic review and memorization

This is a restructuring tool, not a condensing tool. Every fact, detail, example, and nuance from the source material appears in the output.

</purpose>

<process>

## Step 1: Acquire Source Material

Determine input type and read the content:

- **Pasted text**: Use the text directly as provided in the conversation
- **File path**: Use the Read tool to load the file contents
- **URL**: Use the WebFetch tool to retrieve and extract the page content
- **PDF**: Use the Read tool with page ranges for large documents

If the input type is ambiguous, ask the user to clarify.

## Step 2: Extract All Content

Read through the source material and capture:

- Every definition and explanation
- All facts, statistics, and data points
- Every name, date, place, and number
- All examples and illustrations
- Every cause-effect relationship
- All comparisons and contrasts
- Exceptions and special cases
- Conclusions and implications

## Step 3: Organize by Category

Group extracted information under appropriate headings:

- **Core Concepts** — main ideas and theories
- **Key Terms & Definitions** — vocabulary with complete definitions
- **Facts & Details** — specific information to memorize
- **Relationships & Connections** — how things connect, cause and effect
- **Examples & Applications** — concrete illustrations
- **Exceptions & Edge Cases** — special cases and caveats
- **Summary Points** — main conclusions and key takeaways

Omit empty sections. Add custom sections when the material warrants it.

## Step 4: Format for Study

For each bullet point:

- Start with the most important word or phrase in **bold**
- Include complete information without abbreviating away detail
- Add sub-bullets for related supporting points
- Preserve technical terminology exactly as written
- Include page/section references when available

</process>

<output>

```
## Study Notes: [TOPIC_OR_TITLE]

**Core Concepts:**
- [FUNDAMENTAL_CONCEPT_WITH_FULL_EXPLANATION]

**Key Terms & Definitions:**
- **[TERM]**: [COMPLETE_DEFINITION]

**Facts & Details:**
- [SPECIFIC_FACT_WITH_NUMBERS_DATES_NAMES]

**Relationships & Connections:**
- [HOW_CONCEPT_A_RELATES_TO_CONCEPT_B]

**Examples & Applications:**
- [EXAMPLE_WITH_FULL_CONTEXT]

**Exceptions & Edge Cases:**
- [SPECIAL_CASES_MENTIONED]

**Summary Points:**
- [MAIN_CONCLUSIONS_AND_KEY_TAKEAWAYS]
```

</output>

<rules>

- Include every piece of information from the source — when in doubt, include it
- Preserve exact numbers, dates, names, and terminology
- Keep each bullet self-contained and understandable on its own
- Use sub-bullets for related details under main points
- Maintain consistent formatting across all sections
- Include all examples from the source material
- Make implicit connections between concepts explicit
- Preserve all specific values rather than generalizing them

</rules>

<examples>

<example>

**Input**: Textbook section on cellular respiration

**Output**:

## Study Notes: Cellular Respiration

**Core Concepts:**

- **Cellular respiration** is the process cells use to convert glucose into ATP (energy currency)
- Occurs in three main stages: glycolysis, Krebs cycle, electron transport chain
- Overall equation: C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + 36-38 ATP
- Can be aerobic (with oxygen) or anaerobic (without oxygen)

**Key Terms & Definitions:**

- **ATP (Adenosine Triphosphate)**: Primary energy carrier molecule in cells
- **Glycolysis**: First stage; breaks glucose into two pyruvate molecules; occurs in cytoplasm
- **Krebs Cycle (Citric Acid Cycle)**: Second stage; occurs in mitochondrial matrix; produces NADH and FADH₂
- **Electron Transport Chain (ETC)**: Third stage; occurs in inner mitochondrial membrane; produces most ATP

**Facts & Details:**

- Glycolysis produces 2 ATP (net), 2 NADH, and 2 pyruvate per glucose
- Glycolysis does not require oxygen (anaerobic)
- ETC creates proton gradient across inner mitochondrial membrane
- Total ATP yield: 36-38 per glucose (varies by cell type)

**Relationships & Connections:**

- Glycolysis → pyruvate → acetyl-CoA → Krebs cycle (sequential dependency)
- NADH and FADH₂ from glycolysis and Krebs cycle fuel the ETC
- Oxygen is final electron acceptor in ETC (why we breathe)

**Exceptions & Edge Cases:**

- Some cells lack mitochondria (red blood cells) → rely solely on glycolysis
- Cancer cells often use glycolysis even with oxygen present (Warburg effect)

**Summary Points:**

- Cellular respiration converts glucose to ATP through three sequential stages
- Glycolysis is anaerobic; Krebs cycle and ETC require oxygen
- Most ATP (34-36 of 36-38 total) is produced by the electron transport chain
- Disruption at any stage (e.g., lack of oxygen) forces cells to rely on less efficient anaerobic pathways

</example>

</examples>
