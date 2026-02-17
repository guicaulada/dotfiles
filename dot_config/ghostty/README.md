# Ghostty Config

Personal [Ghostty](https://ghostty.org) terminal configuration for macOS.

## Theme

**One Double Dark** with a true black (`#000000`) background. High-contrast variant of the One Dark color scheme — matches well with `onedark-darker` in Neovim.

## Font

JetBrains Mono (Ghostty built-in) with Nerd Font symbol support. `font-thicken` enabled for sharper rendering on Retina displays.

## Keybindings

### Splits

| Action | Keybinding |
|--------|-----------|
| Split right | `Cmd+D` |
| Split down | `Cmd+Shift+D` |
| Split left | `Cmd+Shift+Left` |
| Split up | `Cmd+Shift+Up` |
| Split right | `Cmd+Shift+Right` |
| Split down | `Cmd+Shift+Down` |
| Navigate left | `Cmd+Opt+H` |
| Navigate down | `Cmd+Opt+J` |
| Navigate up | `Cmd+Opt+K` |
| Navigate right | `Cmd+Opt+L` |
| Equalize splits | `Cmd+Shift+=` |
| Zoom split | `Cmd+Shift+Enter` |
| Rename tab | `Cmd+R` |

## Tab Title Patch

Ghostty's shell integration (`_ghostty_precmd`) always moves itself to the end of zsh's `precmd_functions` and reports the full working directory via OSC 7, which Ghostty uses as the tab title. This makes it impossible to override the tab title with a regular `precmd` hook.

The fix is to append a title-setting command directly to `_ghostty_precmd` and `_ghostty_preexec` so it runs as the very last thing in the very last hook. Add this to the **end** of `~/.zshrc`:

```zsh
# Tab title — append to Ghostty's hooks to guarantee running last
_ghostty_title_hook() {
  if (( $+functions[_ghostty_precmd] )); then
    functions[_ghostty_precmd]+='
      builtin print -Pn "\e]0;%1~\a"'
    functions[_ghostty_preexec]+='
      builtin print -Pn "\e]0;%1~\a"'
    print -Pn "\e]0;%1~\a"
    add-zsh-hook -d precmd _ghostty_title_hook
  fi
}
autoload -Uz add-zsh-hook
add-zsh-hook precmd _ghostty_title_hook
```

This one-time hook waits for Ghostty's deferred init to create `_ghostty_precmd`, then permanently patches both hooks to set the title to the current directory basename (`%1~`).

Programs that set their own terminal title (like Claude Code) will still override it while running. To prevent that, set `CLAUDE_CODE_DISABLE_TERMINAL_TITLE=1` in your Claude Code settings.
