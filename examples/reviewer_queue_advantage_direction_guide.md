# reviewer queue advantage-direction guide

Use this note when `summary.reviewer_queue.next_focus_advantage_direction` is present and you need a short reviewer handoff.

## Read the field first

`next_focus_advantage_direction` tells you how confidently the first rerun lane stands above the runner-up:

- `none` — no queued follow-up work exists
- `tied` — the first lane is tied with another lane; preserve the tie in the handoff
- `solo` — only one queue bucket exists; route that bucket directly
- `ahead` — one lane leads the runner-up; mention the lead and the advantage summary

## Copy-ready phrasing

- `none` → `No reviewer queue follow-up is pending.`
- `tied` → `Next focus is tied; keep the first-priority lane first, but preserve the tied labels in the note.`
- `solo` → `Only one reviewer queue lane remains; route that lane directly.`
- `ahead` → `Route the leading reviewer queue lane first and keep the advantage summary in the note.`

## Short decision rule

1. Start with `next_focus_key` and `next_focus_label`.
2. Check `next_focus_advantage_direction`.
3. If it is `tied`, preserve the tied labels.
4. If it is `ahead`, include `next_focus_advantage_summary`.
5. If it is `solo`, skip runner-up wording.
