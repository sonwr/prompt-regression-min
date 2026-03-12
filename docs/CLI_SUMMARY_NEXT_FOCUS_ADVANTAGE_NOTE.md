# CLI summary next-focus advantage note

Keep reviewer-queue handoffs explicit about *why* the next focus wins when the summary already exposes queue-share and active/source-case advantage fields.

## Why it matters

- A short reviewer update should explain the winning queue without reopening the full JSON payload.
- Queue-share and rate deltas make ties versus clear leads easier to spot.
- This keeps summary JSON, Markdown, and PR-comment outputs aligned around the same next-focus reasoning.

## Maintainer cue

If you change next-focus wording, titles, or saved artifact handoffs, rerun the smallest CLI summary tests before pushing so the advantage wording stays deterministic.
