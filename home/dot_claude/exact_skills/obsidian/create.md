---
description: Creates notes, daily notes, and documents in an Obsidian vault using the CLI
---

<purpose>
Create notes in an Obsidian vault using the CLI. Handles regular notes, daily notes, templated notes, and any markdown document. Applies Obsidian-flavored markdown, proper frontmatter, and vault organization conventions.
</purpose>

<process>

## Step 1: Determine Note Type and Location

Identify the kind of note to create:

| Type | Command | Typical Folder |
|------|---------|----------------|
| Regular note | `obsidian create` | Context-dependent |
| Daily note | `obsidian daily` / `obsidian daily:append` | Daily Notes/ |
| Templated note | `obsidian create template=<name>` | Template-dependent |
| Quick capture | `obsidian daily:append content="..."` | Daily Notes/ |

If the user specifies a folder, use `path=`. If not, use `name=` and let Obsidian resolve placement.

Check available templates when relevant:

```bash
obsidian templates
```

## Step 2: Prepare Content

Structure the note with Obsidian-flavored markdown:

1. **Frontmatter**: Include relevant properties (tags, aliases, dates, status)
2. **Wikilinks**: Link to related notes using `[[Note Name]]`
3. **Callouts**: Use for warnings, tips, summaries
4. **Embeds**: Use `![[Note]]` to transclude related content

For multi-line content, use `\n` for newlines in the CLI:

```bash
obsidian create name="Meeting Notes" content="---\ntags:\n  - meeting\ndate: 2026-03-02\n---\n\n# Meeting Notes\n\n## Attendees\n\n## Discussion\n\n## Action Items\n- [ ] "
```

## Step 3: Create the Note

**Regular note:**
```bash
obsidian create name="Note Title" content="..." open
obsidian create path="Projects/Note Title.md" content="..." open
```

**From template:**
```bash
obsidian create name="Note Title" template="Template Name" open
```

**Daily note (create/open today's):**
```bash
obsidian daily
```

**Append to daily note:**
```bash
obsidian daily:append content="- Captured thought at $(date +%H:%M)"
obsidian daily:append content="- [ ] New task"
```

**Prepend to daily note:**
```bash
obsidian daily:prepend content="## Morning Intentions\n- "
```

Flags:
- `open` — open in Obsidian after creation
- `silent` — create without opening
- `overwrite` — replace existing file
- `newtab` — open in a new tab

## Step 4: Add Links and Context

After creating, optionally link from related notes:

```bash
obsidian append file="Related Note" content="\n- [[New Note Title]]"
```

Or link from a MOC (Map of Content):

```bash
obsidian append file="Topic MOC" content="\n- [[New Note Title]] — brief description"
```

## Step 5: Verify Creation

```bash
obsidian file file="Note Title"
obsidian read file="Note Title"
```

</process>

<output>

```
Created: [NOTE_NAME]
Path: [VAULT_PATH]
Template: [TEMPLATE_NAME or "none"]
Properties: [LIST_OF_SET_PROPERTIES]
Links: [OUTGOING_LINKS_ADDED]
```

</output>

<rules>

- Always include YAML frontmatter with at least `tags` and a date property
- Use wikilinks (`[[Note]]`) not markdown links for internal vault references
- Use `obsidian create` not direct file writes — this preserves Obsidian's link tracking and metadata cache
- For daily notes, prefer `obsidian daily:append` over creating new files
- When the user asks to "create a document" or "write markdown" without specifying a tool, default to creating in the Obsidian vault
- Escape content properly: use `\n` for newlines, quote values with spaces
- Check `obsidian templates` before creating if the note type might have a matching template
- Place notes in contextually appropriate folders — ask the user if unclear
- Use descriptive note titles — the filename becomes the default wikilink text

</rules>

<examples>

<example>
**Input**: "Create a meeting note for today's standup"

**Commands**:
```bash
obsidian create name="2026-03-02 Standup" content="---\ntags:\n  - meeting\n  - standup\ndate: 2026-03-02\n---\n\n# Standup — March 2, 2026\n\n## Updates\n\n## Blockers\n\n## Action Items\n- [ ] " open
```

**Output**:
```
Created: 2026-03-02 Standup
Path: Meetings/2026-03-02 Standup.md
Template: none
Properties: tags (meeting, standup), date
Links: none
```
</example>

<example>
**Input**: "Add a quick thought to my daily note about refactoring the auth module"

**Commands**:
```bash
obsidian daily:append content="\n- Idea: refactor the auth module to use JWT instead of session cookies — see [[Auth Architecture]]"
```

**Output**:
```
Appended to daily note: 2026-03-02
Content: idea capture with link to Auth Architecture
```
</example>

<example>
**Input**: "Create a new project note for the API redesign"

**Commands**:
```bash
obsidian templates
# If a project template exists:
obsidian create name="Project — API Redesign" template="Project" open
# If not:
obsidian create name="Project — API Redesign" content="---\ntags:\n  - project\n  - active\nstatus: active\nstart: 2026-03-02\n---\n\n# API Redesign\n\n## Goal\n\n## Scope\n\n## Tasks\n- [ ] \n\n## Notes\n\n## Related\n- [[API Architecture]]\n" open
```
</example>

</examples>
