# Code Style

Readable code reduces cognitive load, speeds up reviews, and makes maintenance easier for everyone.

## Naming

- Use clear, descriptive names for variables, functions, and classes
- Names should reveal intent — a reader should understand purpose without comments
- Prefer specificity over brevity: `userAccountBalance` over `bal`

## Functions

- Keep functions small and focused on a single responsibility
- Extract logic when a function does more than one thing
- Limit parameters — group related parameters into objects when there are many

## Comments

- Comments explain **why**, not what
- Prefer self-documenting code over comments that restate the obvious
- Use comments for non-obvious decisions, workarounds, or business rules
- Keep comments up to date when code changes

## Error Handling

- Handle errors explicitly — never silently ignore them
- Provide meaningful error messages that help diagnose the problem
- Fail fast and fail clearly: surface issues early rather than propagating bad state
- Use the error handling patterns established by the project's language and framework

## General

- Follow existing project conventions and patterns
- Avoid premature optimization — write clear code first, optimize when measured
- Prefer simple solutions over clever ones
