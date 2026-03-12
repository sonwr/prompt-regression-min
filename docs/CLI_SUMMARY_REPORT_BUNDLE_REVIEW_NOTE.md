# CLI summary report bundle review note

When a change touches summary outputs, review the bundle in this order:

1. JSON summary payload for schema and machine-readable fields.
2. Markdown summary for reviewer-facing status lines.
3. HTML or PR-comment artifact only after JSON and Markdown stay aligned.
4. Shared basename and rerun command before posting or uploading artifacts.

Keep one report bundle per run when possible so reviewers can replay the exact output set without guessing filenames.
