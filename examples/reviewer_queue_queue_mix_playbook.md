# Reviewer queue mix playbook

Use this note when the reviewer queue is non-trivial and you want one short explanation of *what kind* of follow-up dominates the shard.

## Why this exists

`prompt-regression-min` already emits queue-share, source-case-rate, and dominant-focus metadata.
This playbook turns those fields into one repeatable triage habit for humans writing PR comments or CI summaries.

## Fast reading order

1. Check `reviewer_queue.queue_mix_summary` in JSON.
2. Check `reviewer_queue.largest_group.label` and `reviewer_queue.largest_group.queue_share`.
3. Check `reviewer_queue.next_focus_group` to confirm the first deterministic rerun lane.
4. If the largest group is tied, preserve `next_focus_tie_summary` in the pasted note.

## Copy-ready triage sentence

Use this shape in reviewer notes:

> Queue mix: regressions dominate the follow-up load (50.00% of queued work); first rerun lane is `fix_regressions`.

Swap in the emitted queue label/share so the note stays deterministic.

## When it helps most

- a shard includes regressions plus unchanged-fail watchlist cases,
- filters or skipped cases are inflating follow-up work,
- a reviewer needs to explain why the next rerun lane is not obvious from pass rate alone,
- or a PR comment should summarize queue composition in one line instead of listing every bucket manually.
