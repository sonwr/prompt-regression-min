# CLI summary exact five-line note

When a five-repo progress pass is requested, keep the user-facing summary to exactly five lines:

- one line per repository
- repository name first
- change status included
- validation result included
- commit/push state included
- if push is held, name the hold reason in the same line

This keeps short reports machine-checkable and human-skimmable.
