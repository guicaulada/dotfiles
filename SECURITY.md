# Security Policy

## Reporting a Vulnerability

If you discover a security issue in this repository (for example, a committed
secret or a misconfigured template that could leak sensitive data), please
**do not** open a public issue.

Instead, report it privately through
[GitHub Security Advisories](https://github.com/guicaulada/dotfiles/security/advisories/new).

## Scope

This is a personal dotfiles repository. Relevant security concerns include:

- Accidentally committed secrets, tokens, or credentials
- Templates that could expose sensitive data when rendered
- Scripts that perform unsafe operations

## Secrets Management

Secrets in this repository are managed through
[1Password CLI](https://developer.1password.com/docs/cli/) and are never stored
in plain text. A [gitleaks](https://github.com/gitleaks/gitleaks) pre-commit hook
scans for accidental secret commits.
