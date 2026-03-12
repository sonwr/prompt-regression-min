# CLI summary report artifact ready note

Use this note when the summary lane already emits JSON, Markdown, and HTML artifacts and you only need a fast readiness check before handoff.

Call the bundle ready only when:

- one shared basename ties the three artifacts together,
- the markdown status line still matches the machine-readable summary,
- the HTML view reopens the same bundle without renaming drift.

If one surface is missing or stale, keep the handoff in hold status and rerun the summary export first.
