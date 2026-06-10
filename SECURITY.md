# Security Policy

## Reporting a Vulnerability

If you discover a security issue in this repository (for example, a committed
secret or a misconfigured template that could leak sensitive data), please
**do not** open a public issue.

Instead, report it privately through
[GitHub Security Advisories](https://github.com/guicaulada/dotfiles/security/advisories/new).

## Response and Disclosure

- Reports are acknowledged within **7 days** and triaged within **14 days**.
- Confirmed vulnerabilities (such as an exposed credential) are remediated as
  soon as possible; affected credentials are rotated immediately.
- Please allow up to **90 days** for remediation before any public disclosure,
  and coordinate disclosure timing through the advisory thread.

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
