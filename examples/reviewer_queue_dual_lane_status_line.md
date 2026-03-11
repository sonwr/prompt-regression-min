# Reviewer queue dual-lane status line

Use this when the main rerun lane is clear but reviewers should still see the likely second lane.

## Template

`P1 {next_focus_label} first; keep P2 {runner_up_label} visible in the same rerun note.`

## Example

`P1 fix regressions first; keep P2 confirm filtered-out scope visible in the same rerun note.`

## When to use it

- `reviewer_queue.total > 0`
- `next_focus_key` is set
- `runner_up_key` is also set
- you want one short status line instead of a longer triage block
