# reviewer_queue tie handoff note

Use this when `reviewer_queue.next_focus_tie_mode` is `tied` and you need one short reviewer-facing sentence without rebuilding the queue by hand.

## Paste pattern

`Next reviewer focus stays on {primary_priority_label}, but keep the tie visible with {tie_summary} before rerun ownership is assigned.`

## Example

`Next reviewer focus stays on P1 · fix regressions, but keep the tie visible with fix_regressions=P1 · fix regressions, watch_unchanged_fails=P2 · watch unchanged fails before rerun ownership is assigned.`

## Quick check

Use this only when:

- `next_focus_tie_mode` is `tied`
- `next_focus_tie_summary` is not `none`
- the reviewer note should preserve the current winner **and** the tie context in one line
