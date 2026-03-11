# CLI reviewer queue reopen note

Use this note when a regression run already produced JSON, Markdown, and PR-comment artifacts, and you only need to reopen the next reviewer lane.

- Reopen the queue with the next-focus key, its priority label, and the matching artifact bundle path.
- Keep the status line scoped to one owner-visible next action.
- Reuse the saved summary schema version so downstream parsers stay stable.
