# Git Commit Conventions

Consistent commit messages make history readable, enable automated changelogs, and help teammates understand changes at a glance.

## Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

## Types

- `feat` — New feature or capability
- `fix` — Bug fix
- `docs` — Documentation changes only
- `style` — Formatting, whitespace, semicolons (no logic change)
- `refactor` — Code restructuring without behavior change
- `test` — Adding or updating tests
- `chore` — Build, tooling, dependency updates
- `perf` — Performance improvement

## Subject Line

- Use imperative mood: "add feature" not "added feature"
- Keep under 50 characters
- Start lowercase after the colon
- Omit trailing period

## Body

- Wrap at 72 characters per line
- Explain **what** changed and **why**, not how
- Separate from subject with a blank line
- Use for complex changes; simple changes need only a subject line

## Footer

- Reference issues: `Closes #123`, `Fixes #456`
- Note breaking changes: `BREAKING CHANGE: description`

## Principles

- Keep commits atomic — one logical change per commit
- Make each commit self-explanatory from the message alone
- Split unrelated changes into separate commits
- Commit working code; avoid committing broken states
