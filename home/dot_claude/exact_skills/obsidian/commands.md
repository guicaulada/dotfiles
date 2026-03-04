---
description: Complete Obsidian CLI command reference organized by category
---

# Obsidian CLI Command Reference

## Files and Content

| Command     | Description                         | Key Parameters                                                                     |
|-------------|-------------------------------------|------------------------------------------------------------------------------------|
| `create`    | Create a new file                   | `name=`, `path=`, `content=`, `template=`, `overwrite`, `open`, `silent`, `newtab` |
| `read`      | Read file contents                  | `file=`, `path=`                                                                   |
| `append`    | Append content to a file            | `file=`, `content=`, `inline` (no newline)                                         |
| `prepend`   | Prepend content to a file           | `file=`, `content=`                                                                |
| `open`      | Open a file in Obsidian             | `file=`, `path=`, `newtab`                                                         |
| `delete`    | Delete a file                       | `file=`, `permanent` (skip trash)                                                  |
| `move`      | Move/rename, updating all backlinks | `file=`, `to=`                                                                     |
| `rename`    | Rename a file                       | `file=`, `to=`                                                                     |
| `file`      | Show file metadata                  | `file=`                                                                            |
| `files`     | List files in vault                 | `folder=`, `ext=`, `total`, `format=`                                              |
| `wordcount` | Count words and characters          | `file=`                                                                            |
| `outline`   | Show headings structure             | `file=`, `format=tree|md|json`                                                     |

## Daily Notes

| Command         | Description                    | Key Parameters       |
|-----------------|--------------------------------|----------------------|
| `daily`         | Open today's daily note        | `open`               |
| `daily:read`    | Read today's daily note        | —                    |
| `daily:append`  | Append to today's daily note   | `content=`, `inline` |
| `daily:prepend` | Prepend to today's daily note  | `content=`           |
| `daily:path`    | Get path of today's daily note | —                    |

## Search

| Command          | Description                     | Key Parameters                                                  |
|------------------|---------------------------------|-----------------------------------------------------------------|
| `search`         | Full-text search                | `query=`, `path=`, `limit=`, `case`, `format=text|json`,`total` |
| `search:context` | Search with surrounding context | `query=`, `limit=`, `format=`                                   |
| `search:open`    | Open Obsidian search UI         | `query=`                                                        |

## Links and Graph

| Command      | Description                  | Key Parameters                          |
|--------------|------------------------------|-----------------------------------------|
| `links`      | List outgoing links          | `file=`, `format=`                      |
| `backlinks`  | List incoming links          | `file=`, `format=`                      |
| `unresolved` | List broken links            | `verbose`, `counts`, `total`, `format=` |
| `orphans`    | Notes with no incoming links | `total`, `format=`                      |
| `deadends`   | Notes with no outgoing links | `total`, `format=`                      |

## Tags

| Command | Description                | Key Parameters                            |
|---------|----------------------------|-------------------------------------------|
| `tags`  | List tags in vault or file | `file=`, `sort=count`, `total`, `format=` |
| `tag`   | Info about a specific tag  | `name=`                                   |

## Properties (YAML Frontmatter)

| Command           | Description           | Key Parameters                                                            |
|-------------------|-----------------------|---------------------------------------------------------------------------|
| `properties`      | List properties       | `file=`, `sort=count`, `counts`, `format=`                                |
| `property:read`   | Read a property value | `name=`, `file=`                                                          |
| `property:set`    | Set a property        | `name=`, `value=`, `type=text|list|number|checkbox|date|datetime`,`file=` |
| `property:remove` | Remove a property     | `name=`, `file=`                                                          |

## Tasks

| Command | Description               | Key Parameters                                                             |
|---------|---------------------------|----------------------------------------------------------------------------|
| `tasks` | List tasks                | `todo`, `done`, `status=`, `file=`, `daily`, `verbose`, `total`, `format=` |
| `task`  | Show/update a single task | `file=`, `line=`, `toggle`, `done`, `todo`, `status=`                      |

## Templates

| Command           | Description                      | Key Parameters             |
|-------------------|----------------------------------|----------------------------|
| `templates`       | List available templates         | —                          |
| `template:read`   | Read template content            | `file=`, resolve variables |
| `template:insert` | Insert template into active file | `file=`                    |

## Vault and Folders

| Command       | Description                               | Key Parameters |
|---------------|-------------------------------------------|----------------|
| `vault`       | Show vault info (name, path, count, size) | —              |
| `vaults`      | List all known vaults                     | —              |
| `folder`      | Show folder info                          | `path=`        |
| `folders`     | List folders                              | —              |
| `recents`     | Recently opened files                     | `limit=`       |
| `random`      | Open a random note                        | —              |
| `random:read` | Read a random note                        | —              |
| `reload`      | Reload the vault                          | —              |
| `restart`     | Restart the app                           | —              |

## Aliases and Bookmarks

| Command     | Description           | Key Parameters                     |
|-------------|-----------------------|------------------------------------|
| `aliases`   | List aliases in vault | `total`, `verbose`                 |
| `bookmark`  | Add a bookmark        | file, folder, search query, or URL |
| `bookmarks` | List bookmarks        | —                                  |

## Bases (Database Views)

| Command       | Description           | Key Parameters                                   |
|---------------|-----------------------|--------------------------------------------------|
| `bases`       | List all .base files  | —                                                |
| `base:views`  | List views in a base  | `file=`                                          |
| `base:query`  | Query a base view     | `file=`, `view=`, `format=json|csv|tsv|md|paths` |
| `base:create` | Create item in a base | `file=`, `name=`, `content=`, `open`             |

## Plugins

| Command            | Description              | Key Parameters                    |
|--------------------|--------------------------|-----------------------------------|
| `plugins`          | List installed plugins   | `filter=core|community`,`format=` |
| `plugins:enabled`  | List enabled plugins     | —                                 |
| `plugin`           | Plugin info              | `id=`                             |
| `plugin:enable`    | Enable a plugin          | `id=`                             |
| `plugin:disable`   | Disable a plugin         | `id=`                             |
| `plugin:install`   | Install community plugin | `id=`, `enable`                   |
| `plugin:uninstall` | Uninstall a plugin       | `id=`                             |
| `plugin:reload`    | Reload a plugin (dev)    | `id=`                             |
| `plugins:restrict` | Toggle restricted mode   | `on`, `off`                       |

## Themes and CSS Snippets

| Command            | Description           | Key Parameters    |
|--------------------|-----------------------|-------------------|
| `themes`           | List installed themes | —                 |
| `theme`            | Active theme info     | —                 |
| `theme:set`        | Set active theme      | `name=`           |
| `theme:install`    | Install a theme       | `name=`, `enable` |
| `theme:uninstall`  | Uninstall a theme     | `name=`           |
| `snippets`         | List CSS snippets     | —                 |
| `snippets:enabled` | List enabled snippets | —                 |
| `snippet:enable`   | Enable a snippet      | `name=`           |
| `snippet:disable`  | Disable a snippet     | `name=`           |

## Commands and Hotkeys

| Command    | Description              | Key Parameters |
|------------|--------------------------|----------------|
| `commands` | List all command IDs     | `filter=`      |
| `command`  | Execute a command        | `id=`          |
| `hotkeys`  | List hotkeys             | —              |
| `hotkey`   | Get hotkey for a command | `id=`          |

## Sync and Version History

| Command           | Description                 | Key Parameters      |
|-------------------|-----------------------------|---------------------|
| `sync`            | Pause/resume sync           | `pause`, `resume`   |
| `sync:status`     | Show sync status            | —                   |
| `sync:history`    | File sync history           | `file=`             |
| `sync:read`       | Read a sync version         | `file=`, `version=` |
| `sync:restore`    | Restore a sync version      | `file=`, `version=` |
| `sync:deleted`    | Files deleted via sync      | —                   |
| `sync:open`       | Open sync history UI        | —                   |
| `diff`            | Diff local vs sync version  | `file=`             |
| `history`         | Local file history versions | `file=`             |
| `history:read`    | Read a history version      | `file=`, `version=` |
| `history:restore` | Restore a history version   | `file=`, `version=` |
| `history:list`    | Files with history          | —                   |
| `history:open`    | Open file recovery UI       | —                   |

## Workspace and Tabs

| Command            | Description           | Key Parameters |
|--------------------|-----------------------|----------------|
| `workspace`        | Show workspace tree   | —              |
| `workspaces`       | List saved workspaces | —              |
| `workspace:save`   | Save workspace        | `name=`        |
| `workspace:load`   | Load workspace        | `name=`        |
| `workspace:delete` | Delete workspace      | `name=`        |
| `tabs`             | List open tabs        | —              |
| `tab:open`         | Open a new tab        | —              |

## Developer

| Command          | Description               | Key Parameters |
|------------------|---------------------------|----------------|
| `eval`           | Execute JavaScript        | `code=`        |
| `dev:console`    | View console messages     | —              |
| `dev:errors`     | View captured errors      | —              |
| `dev:cdp`        | Chrome DevTools Protocol  | —              |
| `dev:debug`      | Attach/detach debugger    | —              |
| `dev:dom`        | Query DOM by CSS selector | `selector=`    |
| `dev:css`        | Inspect CSS with sources  | —              |
| `dev:screenshot` | Take a screenshot         | `path=`        |
| `dev:mobile`     | Toggle mobile emulation   | —              |
| `devtools`       | Toggle developer tools    | —              |

## Publish

| Command          | Description            | Key Parameters |
|------------------|------------------------|----------------|
| `publish:site`   | Show publish site info | —              |
| `publish:list`   | List published notes   | —              |
| `publish:status` | Show publish status    | —              |
| `publish:add`    | Publish a note         | `path=`        |
| `publish:remove` | Unpublish a note       | `path=`        |
| `publish:open`   | Open publish UI        | —              |

## Global Options

| Option                    | Description                        |
|---------------------------|------------------------------------|
| `vault=<name>`            | Target a specific vault            |
| `--copy`                  | Copy output to clipboard           |
| `format=json|md|csv|text` | Output format (command-dependent)  |
| `total`                   | Show count only (on list commands) |
| `verbose`                 | Show additional details            |
| `help`                    | Show help for any command          |
