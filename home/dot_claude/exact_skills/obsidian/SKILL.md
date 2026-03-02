---
name: obsidian
description: >
  Interacts with the Obsidian CLI for vault management, note creation, search, and
  organization. Use when user mentions obsidian, vault, daily note, create a note,
  write a document, create markdown, search vault, find notes, organize notes, manage
  tags, manage properties, vault health, or tasks in obsidian. Handles note creation
  with templates, daily notes, full-text search, link and graph exploration, property
  management, task tracking, and vault maintenance. Do NOT use for general markdown
  editing unrelated to an Obsidian vault.
allowed-tools: Bash(obsidian *), Read, Glob, Grep
user-invocable: true
argument-hint: "[action] [details]"
---

# Obsidian

Interact with Obsidian vaults through the official CLI. The CLI communicates with the running Obsidian app via IPC, giving access to pre-computed indexes (search, backlinks, metadata cache, tags) rather than raw file I/O.

## Prerequisites

- Obsidian desktop v1.12+ running (CLI launches it automatically if closed)
- CLI registered via Settings > General > Command line interface > Register CLI

## Core CLI Syntax

```bash
obsidian <command> [param=value ...] [flags]
```

- **Target vault**: `vault=<name>` (omit to use the active vault)
- **File by name** (wikilink-style resolution): `file=<name>`
- **File by path** (exact): `path=<folder/note.md>`
- **Defaults to active file** when no file/path given
- **Quote values with spaces**: `name="My Note"`
- **Newlines/tabs in content**: use `\n` and `\t`
- **Copy output to clipboard**: append `--copy`
- **Count results**: append `total` to list commands
- **Output formats**: `format=json`, `format=md`, `format=csv`, `format=text`
- Running `obsidian` with no arguments launches the interactive TUI

## Obsidian-Flavored Markdown

When creating notes, use these Obsidian-specific extensions:

**Links and embeds:**
```markdown
[[Note Name]]                    — wikilink
[[Note Name|Display Text]]       — aliased link
[[Note Name#Heading]]            — heading link
[[Note Name#^blockid]]           — block reference
![[Note Name]]                   — embed full note
![[Note Name#Heading]]           — embed section
![[image.png|300]]               — embed image with width
```

**Callouts:**
```markdown
> [!note] Optional Title
> Content here.

> [!tip]+ Expanded by default
> [!warning]- Collapsed by default
```

Types: `note`, `abstract`/`summary`/`tldr`, `info`/`todo`, `tip`/`hint`/`important`, `success`/`check`/`done`, `question`/`help`/`faq`, `warning`/`caution`/`attention`, `failure`/`fail`/`missing`, `danger`/`error`, `bug`, `example`, `quote`/`cite`

**Properties (YAML frontmatter):**
```yaml
---
tags:
  - project
  - active
aliases:
  - "Short Name"
cssclasses:
  - wide-page
status: active
due: 2026-03-15
priority: 2
published: false
created: 2026-03-01T10:30:00
---
```

Property types: text, number, checkbox (boolean), date (`YYYY-MM-DD`), datetime (`YYYY-MM-DDTHH:mm:ss`), list

**Other extensions:**
- Comments: `%% invisible in reading view %%`
- Highlights: `==highlighted text==`
- Tags: `#topic/subtopic` (nested with slashes)
- Tasks: `- [ ] unchecked` / `- [x] checked`
- Math: `$inline$` / `$$block$$` (LaTeX via MathJax)
- Mermaid diagrams in fenced `mermaid` code blocks

## Vault Organization Principles

- Use **wikilinks** for semantic connections between ideas
- Use **tags** for status/type metadata that crosses topics (`#status/active`, `#type/meeting`)
- Use **properties** for structured, queryable metadata (dates, numbers, booleans)
- Use **folders** sparingly (1-2 levels max) for broad note-type separation
- Use **MOCs** (Maps of Content) for navigational structure within topics
- Name notes descriptively — the filename is the default link display text
- Daily notes use ISO format: `YYYY-MM-DD`

## Workflows

### Create

Trigger: "create a note", "write a document", "new note", "daily note", "journal", "create markdown"

Read and follow [create.md](create.md).

### Search

Trigger: "search obsidian", "find in vault", "show backlinks", "orphaned notes", "explore links", "vault search"

Read and follow [search.md](search.md).

### Manage

Trigger: "organize vault", "move note", "update properties", "list tasks", "vault health", "rename note", "batch update"

Read and follow [manage.md](manage.md).

### Command Reference

For the complete CLI command reference, read [commands.md](commands.md).
