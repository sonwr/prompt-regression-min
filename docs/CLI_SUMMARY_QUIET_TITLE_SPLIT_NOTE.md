# CLI summary quiet title split note

Use this note when CI/stdout should stay quiet with `--quiet`, but the saved markdown handoff and pasted PR-comment snapshot still need intentionally different headings.

Keep these cues together:
- use `--quiet` to suppress the human-readable recap on stdout
- keep `--summary-markdown-title` focused on the fuller artifact/bundle handoff
- keep `--summary-pr-comment-title` focused on the pasted reviewer note
- make sure both titles come from the same regression run so reviewer language and saved artifacts do not drift
