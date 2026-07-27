# Git Commit Conventions

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

## Rules

- Subject: imperative mood, under 50 characters, lowercase after the colon, no trailing period
- Body (when needed): wrap at 72 characters, explain what and why
- Footer: `Closes #123`, `BREAKING CHANGE: description`
- Base commit messages solely on the code diff — never leak terminology or context from external sources like design docs or planning artifacts
- Create pull requests with `gh pr create --web` for final review in the browser
