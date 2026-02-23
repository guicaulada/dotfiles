# Branching Strategy

Clear branch naming and short-lived branches reduce merge conflicts, simplify code review, and keep the repository history clean.

## Branch Naming

Use the format: `gc/<type>/<short-description>`

Examples:
- `gc/feat/user-auth`
- `gc/fix/login-redirect`
- `gc/refactor/api-client`
- `gc/docs/setup-guide`
- `gc/chore/upgrade-deps`

## Guidelines

- Create feature branches from `main` for all new work
- Keep branches focused on a single concern
- Keep branches short-lived — merge and delete promptly
- Rebase on `main` before opening a pull request to keep history linear
- Delete merged branches to avoid clutter
- Use descriptive names that convey the branch purpose at a glance
