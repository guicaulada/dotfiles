# Branching Strategy

Clear branch naming and short-lived branches reduce merge conflicts, simplify code review, and keep the repository history clean.

## Branch Naming

Use the format: `<type>/<short-description>`

Examples:
- `feat/user-auth`
- `fix/login-redirect`
- `refactor/api-client`
- `docs/setup-guide`
- `chore/upgrade-deps`

## Guidelines

- Create feature branches from `main` for all new work
- Keep branches focused on a single concern
- Keep branches short-lived — merge and delete promptly
- Rebase on `main` before opening a pull request to keep history linear
- Delete merged branches to avoid clutter
- Use descriptive names that convey the branch purpose at a glance
