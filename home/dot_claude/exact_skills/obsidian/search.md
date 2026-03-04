---
description: Searches and explores an Obsidian vault using the CLI's indexed search, link graph, and tag system
---

<purpose>
Search and explore Obsidian vault content using the CLI. Leverages Obsidian's pre-computed indexes for fast full-text search, link/backlink exploration, tag discovery, and graph analysis — without reading raw files.
</purpose>

<process>

## Step 1: Choose Search Strategy

| Goal                   | Command                                  | When to Use                    |
|------------------------|------------------------------------------|--------------------------------|
| Find text across vault | `obsidian search`                        | Keyword or phrase lookup       |
| Find with context      | `obsidian search:context`                | Need surrounding lines         |
| Explore connections    | `obsidian backlinks` / `obsidian links`  | Understand how a note connects |
| Find isolated notes    | `obsidian orphans` / `obsidian deadends` | Vault maintenance              |
| Find broken links      | `obsidian unresolved`                    | Link hygiene                   |
| Browse by tag          | `obsidian tags` / `obsidian tag`         | Topic-based exploration        |
| Find recent files      | `obsidian recents`                       | Resume recent work             |
| Read a specific note   | `obsidian read`                          | Direct content access          |
| Get note structure     | `obsidian outline`                       | See headings hierarchy         |

## Step 2: Execute Search

**Full-text search:**

```bash
obsidian search query="search terms"
obsidian search query="search terms" limit=20
obsidian search query="search terms" path=Projects/
obsidian search query="search terms" case          # case-sensitive
obsidian search query="search terms" format=json   # for scripting
```

**Search with surrounding context:**

```bash
obsidian search:context query="authentication" limit=10
obsidian search:context query="TODO" format=json
```

**Property-based search (Obsidian search operators):**

```bash
obsidian search query="[status:active]"
obsidian search query="[priority:>3]"
obsidian search query='[status:"in progress"]'
obsidian search query="#project [status:active]"
obsidian search query="path:Projects"
```

**Open search in Obsidian UI:**

```bash
obsidian search:open query="search terms"
```

## Step 3: Explore Links and Graph

**Outgoing links from a note:**

```bash
obsidian links file="Note Name"
obsidian links file="Note Name" format=json
```

**Backlinks to a note (what references it):**

```bash
obsidian backlinks file="Note Name"
obsidian backlinks file="Note Name" format=json
```

**Orphaned notes (no incoming links):**

```bash
obsidian orphans
obsidian orphans total
obsidian orphans format=json
```

**Dead-end notes (no outgoing links):**

```bash
obsidian deadends
obsidian deadends total
```

**Broken links (pointing to nonexistent notes):**

```bash
obsidian unresolved
obsidian unresolved total
obsidian unresolved verbose    # show broken link text
obsidian unresolved counts     # broken links per note
```

## Step 4: Explore Tags

**List all tags with counts:**

```bash
obsidian tags
obsidian tags sort=count
obsidian tags format=json
```

**Tags for a specific note:**

```bash
obsidian tags file="Note Name"
```

**Info about a specific tag:**

```bash
obsidian tag name="#project"
obsidian tag name="#project/active"
```

## Step 5: Browse and Read

**List files:**

```bash
obsidian files
obsidian files folder=Projects
obsidian files ext=md
obsidian files total
```

**List folders:**

```bash
obsidian folders
```

**Read a note:**

```bash
obsidian read file="Note Name"
obsidian read path="Projects/Note.md"
```

**Get note outline (heading structure):**

```bash
obsidian outline file="Note Name"
obsidian outline file="Note Name" format=json
```

**Recent files:**

```bash
obsidian recents
obsidian recents limit=10
```

**Random note (for review/discovery):**

```bash
obsidian random:read
```

## Step 6: Query Bases (Database Views)

If the vault uses Obsidian Bases:

```bash
obsidian bases                                          # list all bases
obsidian base:views file="Projects"                     # list views in a base
obsidian base:query file="Projects" view="Active" format=json
obsidian base:query file="Projects" view="Active" format=md
```

</process>

<output>

```
## Search Results: [QUERY]

Found [N] results in [SCOPE]:

| Note       | Match/Context      |
|------------|--------------------|
| [[NOTE_1]] | [RELEVANT_EXCERPT] |
| [[NOTE_2]] | [RELEVANT_EXCERPT] |

### Link Analysis (if applicable)
- Backlinks: [N]
- Outgoing links: [N]
- Orphans found: [N]
- Broken links: [N]
```

</output>

<rules>

- Always use CLI search over raw grep — the CLI uses Obsidian's pre-computed indexes (60x faster, 70,000x fewer tokens)
- Use `format=json` when piping results to further processing
- Use `search:context` when the user needs to understand where matches appear
- For property-based queries, use Obsidian's search operator syntax: `[property:value]`
- Present search results with wikilink notation so the user can navigate
- When exploring a topic, combine search + backlinks + tags for comprehensive discovery
- Use `obsidian outline` to understand a note's structure before reading the full content
- Prefer `obsidian base:query` over Dataview for structured queries when a base exists

</rules>

<examples>

<example>
**Input**: "Find all notes related to authentication in my vault"

**Commands**:

```bash
obsidian search query="authentication" limit=20 format=json
obsidian tags | grep -i auth
obsidian search query="#auth"
```

**Output**:

```
## Search Results: authentication

Found 12 results:

| Note                   | Context                                      |
|------------------------|----------------------------------------------|
| [[Auth Architecture]]  | Main authentication flow design document     |
| [[2026-02-28 Standup]] | Discussed auth token refresh strategy        |
| [[API Security]]       | JWT authentication middleware implementation |

### Related Tags
- #auth (5 notes)
- #auth/jwt (3 notes)
- #security (8 notes)
```

</example>

<example>
**Input**: "What links to my API Design note?"

**Commands**:

```bash
obsidian backlinks file="API Design"
obsidian links file="API Design"
```

**Output**:

```
## Link Analysis: API Design

### Backlinks (referenced by):
- [[Project — API Redesign]]
- [[2026-02-15 Architecture Review]]
- [[REST Conventions MOC]]

### Outgoing Links (references):
- [[Auth Architecture]]
- [[Error Handling Patterns]]
- [[Rate Limiting]]
```

</example>

<example>
**Input**: "Show me all my incomplete tasks"

**Commands**:

```bash
obsidian tasks todo
obsidian tasks todo total
```

**Output**:

```
## Open Tasks: 23 total

- [ ] Implement JWT refresh — [[Auth Architecture]]
- [ ] Write API tests — [[Project — API Redesign]]
- [ ] Review PR #142 — [[2026-03-01]]
...
```

</example>

</examples>
