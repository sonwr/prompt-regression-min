# Reviewer queue priority alias note

Use `reviewer_queue.follow_up_priority_summary` as the shortest stable handoff string when you need to explain which rerun lane wins first.

## Copy pattern
- Primary lane: `<follow_up_priority_summary>`
- Queue mix: `<queue_mix_summary>`
- Next focus: `<next_focus_handoff_summary>`

## Why it helps
- Humans can paste one deterministic line into PRs or issue comments.
- Bots can reuse the same lane label without rebuilding queue ordering from raw arrays.
- The same phrasing works for regressions, unchanged-fail watchlists, filtered scope, and skipped-case cleanup.
