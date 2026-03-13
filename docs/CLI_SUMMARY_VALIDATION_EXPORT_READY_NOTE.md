# CLI summary validation/export ready note

Before sharing a saved summary bundle, keep one explicit local validation command beside the generated artifact path.

Minimum maintainer loop:

1. rerun the smallest deterministic unittest command
2. regenerate the JSON/Markdown/HTML summary artifact you actually changed
3. report one short status line that names validation state before any commit/push claim
