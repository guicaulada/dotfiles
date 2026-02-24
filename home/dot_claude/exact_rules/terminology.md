# Inclusive Terminology

Language shapes understanding. Using inclusive, precise terminology makes code and documentation welcoming and clear for all contributors.

## Preferred Terms

| Use                   | Instead of                                   |
|-----------------------|----------------------------------------------|
| allowlist             | whitelist                                    |
| blocklist             | blacklist                                    |
| primary / replica     | master / slave                               |
| main (branch)         | master (branch)                              |
| placeholder / example | dummy                                        |
| concurrent / parallel | N/A (use the precise term for the situation) |
| conflict-free         | clean (when describing merge state)          |

## Guidelines

- Apply these terms in code, comments, documentation, commit messages, and configuration
- When updating existing code, migrate terminology as part of the change
- Use precise technical terms — "concurrent" and "parallel" have distinct meanings; choose the one that accurately describes the behavior
