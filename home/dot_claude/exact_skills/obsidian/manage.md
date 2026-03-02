---
description: Manages vault organization, properties, tasks, and health using the Obsidian CLI
---

<purpose>
Organize and maintain an Obsidian vault using the CLI. Handles moving/renaming files (with automatic link updates), property management, task operations, plugin management, and vault health audits.
</purpose>

<process>

## Step 1: Identify the Operation

| Operation | Commands | Risk Level |
|-----------|----------|------------|
| Move/rename | `obsidian move`, `obsidian rename` | Medium — updates all backlinks automatically |
| Delete | `obsidian delete` | High — confirm with user first |
| Set properties | `obsidian property:set` | Low |
| Remove properties | `obsidian property:remove` | Medium |
| Toggle task | `obsidian task` | Low |
| Plugin management | `obsidian plugin:*` | Medium |
| Vault health audit | `obsidian orphans`, `obsidian unresolved`, `obsidian deadends` | Read-only |

## Step 2: File Operations

**Move a note (updates all backlinks across vault):**
```bash
obsidian move file="Old Name" to="NewFolder/New Name.md"
obsidian move path="OldFolder/Note.md" to="NewFolder/Note.md"
```

**Rename a note:**
```bash
obsidian rename file="Old Name" to="New Name"
```

**Delete a note (moves to trash by default):**
```bash
obsidian delete file="Note Name"
obsidian delete file="Note Name" permanent   # skip trash — confirm with user
```

**Append/prepend content:**
```bash
obsidian append file="Note Name" content="\n## New Section\n"
obsidian prepend file="Note Name" content="Status update: ...\n"
obsidian append file="Note Name" content="inline addition" inline   # no newline
```

## Step 3: Property Management

**Read properties:**
```bash
obsidian properties file="Note Name"
obsidian properties file="Note Name" format=json
obsidian property:read name="status" file="Note Name"
```

**Set a property:**
```bash
obsidian property:set name="status" value="active" file="Note Name"
obsidian property:set name="priority" value="3" type=number file="Note Name"
obsidian property:set name="due" value="2026-03-15" type=date file="Note Name"
obsidian property:set name="published" value="true" type=checkbox file="Note Name"
obsidian property:set name="tags" value="project,active" type=list file="Note Name"
```

**Remove a property:**
```bash
obsidian property:remove name="status" file="Note Name"
```

**Vault-wide property inventory:**
```bash
obsidian properties sort=count counts
obsidian aliases
```

**Batch property updates (loop pattern):**
```bash
obsidian search query="[status:draft]" format=json | jq -r '.[].path' | while read path; do
  obsidian property:set name="status" value="published" path="$path"
  obsidian property:set name="publishedDate" value="$(date +%Y-%m-%d)" path="$path"
done
```

## Step 4: Task Management

**List tasks:**
```bash
obsidian tasks                     # all tasks
obsidian tasks todo                # incomplete only
obsidian tasks done                # completed only
obsidian tasks file="Note Name"   # tasks in specific note
obsidian tasks daily todo          # today's daily note tasks
obsidian tasks todo total          # count
obsidian tasks format=json         # structured output
obsidian tasks verbose             # show file locations
```

**Toggle/update a task:**
```bash
obsidian task file="Note Name" line=5 toggle
obsidian task file="Note Name" line=5 done
obsidian task file="Note Name" line=5 todo
obsidian task daily line=3 toggle
```

## Step 5: Plugin and Theme Management

**Plugins:**
```bash
obsidian plugins                    # list all
obsidian plugins:enabled            # list enabled
obsidian plugin id=dataview         # info about specific plugin
obsidian plugin:enable id=dataview
obsidian plugin:disable id=calendar
obsidian plugin:install id=tasks enable
obsidian plugin:uninstall id=old-plugin
obsidian plugin:reload id=my-plugin # developer hot-reload
```

**Themes and snippets:**
```bash
obsidian themes
obsidian theme:set name="Minimal"
obsidian snippets
obsidian snippet:enable name="custom-headers"
```

## Step 6: Vault Health Audit

Run a comprehensive vault health check:

```bash
echo "=== VAULT HEALTH ==="
echo "Total notes: $(obsidian files total)"
echo "Orphaned notes: $(obsidian orphans total)"
echo "Dead-end notes: $(obsidian deadends total)"
echo "Broken links: $(obsidian unresolved total)"
echo "Total tags: $(obsidian tags total)"
echo "Open tasks: $(obsidian tasks todo total)"
```

**Investigate specific issues:**
```bash
obsidian orphans format=json          # notes nobody links to
obsidian deadends format=json         # notes that link to nothing
obsidian unresolved verbose           # broken links with context
```

**Fix broken links by creating missing notes:**
```bash
obsidian unresolved format=json | jq -r '.[].link' | sort -u | while read link; do
  obsidian create name="$link" content="---\ntags:\n  - stub\n---\n\n# $link\n\nTODO: flesh out this note.\n" silent
done
```

## Step 7: Advanced Operations with eval

For operations not covered by built-in commands, use `eval` to execute JavaScript in the Obsidian runtime:

```bash
# Count all wikilinks across vault
obsidian eval code="let n=0; app.vault.getMarkdownFiles().forEach(f => { n += (app.metadataCache.getFileCache(f)?.links?.length || 0); }); console.log(n);"

# Find notes modified in last 7 days
obsidian eval code="const week = Date.now() - 7*24*60*60*1000; const recent = app.vault.getMarkdownFiles().filter(f => f.stat.mtime > week).map(f => f.path); console.log(JSON.stringify(recent));"

# Access Dataview API (if installed)
obsidian eval code="const dv = app.plugins.plugins['dataview']?.api; const pages = dv?.pages('#project').where(p => p.status === 'active').array(); console.log(JSON.stringify(pages?.map(p => p.file.path)));"

# Process frontmatter programmatically
obsidian eval code="const file = app.vault.getAbstractFileByPath('Projects/Alpha.md'); await app.fileManager.processFrontMatter(file, fm => { fm.status = 'complete'; }); console.log('done');"
```

Available runtime objects: `app.vault`, `app.metadataCache`, `app.workspace`, `app.fileManager`, `app.commands`, `app.plugins`.

</process>

<output>

```
## Vault Operation: [OPERATION_TYPE]

**Action**: [DESCRIPTION]
**Files affected**: [COUNT]
**Changes**:
- [CHANGE_1]
- [CHANGE_2]

### Health Summary (if audit)
| Metric | Count | Status |
|--------|-------|--------|
| Total notes | [N] | — |
| Orphans | [N] | [OK/ATTENTION] |
| Dead ends | [N] | [OK/ATTENTION] |
| Broken links | [N] | [OK/ATTENTION] |
| Open tasks | [N] | — |
```

</output>

<rules>

- Use `obsidian move` not manual file moves — the CLI automatically updates all backlinks across the vault
- Always confirm with the user before `delete permanent` — use regular `delete` (moves to trash) by default
- For batch operations, show the user what will be affected before executing
- Review `eval` code carefully before running — it executes with full app privileges
- When doing vault health audits, present findings as actionable recommendations, not just numbers
- For property batch updates, use `format=json | jq` piping to extract paths
- Prefer CLI property commands over editing YAML frontmatter directly — the CLI validates types

</rules>

<examples>

<example>
**Input**: "Move all my meeting notes into a Meetings folder"

**Commands**:
```bash
obsidian search query="#meeting" format=json | jq -r '.[].path'
# Review list with user, then:
obsidian search query="#meeting" format=json | jq -r '.[].path' | while read path; do
  filename=$(basename "$path")
  obsidian move path="$path" to="Meetings/$filename"
done
```

**Output**:
```
## Vault Operation: Batch Move

**Action**: Moved meeting notes to Meetings/
**Files affected**: 8
**Changes**:
- Moved 2026-02-15 Standup.md → Meetings/
- Moved 2026-02-22 Architecture Review.md → Meetings/
- ... (6 more)
- All backlinks updated automatically
```
</example>

<example>
**Input**: "Run a health check on my vault"

**Commands**:
```bash
obsidian files total
obsidian orphans total
obsidian deadends total
obsidian unresolved total
obsidian tags total
obsidian tasks todo total
```

**Output**:
```
## Vault Health Audit

| Metric | Count | Status |
|--------|-------|--------|
| Total notes | 342 | — |
| Orphans | 28 | ATTENTION |
| Dead ends | 15 | OK |
| Broken links | 7 | ATTENTION |
| Tags | 45 | — |
| Open tasks | 19 | — |

### Recommendations
1. **28 orphaned notes** have no incoming links — review with `obsidian orphans` and connect or archive
2. **7 broken links** point to nonexistent notes — create stubs or fix with `obsidian unresolved verbose`
```
</example>

<example>
**Input**: "Mark all notes in the Archive folder as status: archived"

**Commands**:
```bash
obsidian files folder=Archive format=json | jq -r '.[].path' | while read path; do
  obsidian property:set name="status" value="archived" path="$path"
done
```
</example>

</examples>
