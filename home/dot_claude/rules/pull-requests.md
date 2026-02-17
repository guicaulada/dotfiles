# Pull Requests

Focused, well-described pull requests make reviews faster, reduce back-and-forth, and produce a cleaner merge history.

## Scope

- Keep PRs focused on a single concern or feature
- Split large changes into smaller, reviewable PRs
- Separate refactoring from behavior changes — different PRs for each

## Description

- Write a clear title that summarizes the change
- Explain **what** changed and **why** in the description body
- Link related issues using `Closes #123` or `Fixes #456`
- Include context a reviewer needs: screenshots, test output, or migration steps

## Before Requesting Review

- Ensure all tests pass
- Run linters and type checks
- Review your own diff for leftover debug code or unintended changes
- Rebase on the latest `main` to resolve conflicts

## Reviewing

- Review for correctness, clarity, and maintainability
- Ask questions rather than making assumptions
- Approve when confident the change is correct and complete
- Provide actionable feedback with specific suggestions
