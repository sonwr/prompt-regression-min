# Reviewer-queue tie + runner-up playbook

Use this when `reviewer_queue.next_focus_tie_mode` is `tied`, but you still want one short reviewer note that names both the tied first lane and the next most likely follow-up lane.

## When to use this

Choose this playbook when the JSON report exposes all three of these signals:

- `next_focus_tie_mode: tied`
- `next_focus_tie_summary` is populated
- `runner_up_summary` is populated

This keeps the first pasted note deterministic without hiding that another queue lane is effectively tied or immediately behind it.

## Suggested reviewer-note shape

```text
Primary rerun lane: {next_focus_tie_summary}
Runner-up lane: {runner_up_summary}
Why this ordering: keep the first priority lane deterministic, but preserve the tie and second lane for the next rerun.
```

## Example

```text
Primary rerun lane: p0=P1 · policy-sensitive failures, p1=P2 · formatting drift
Runner-up lane: P3 · latency-only follow-up
Why this ordering: keep the first priority lane deterministic, but preserve the tie and second lane for the next rerun.
```

## Quick checklist

- Keep the exact priority labels from the generated artifact.
- Do not collapse the tie into a single winner if `next_focus_has_ties` is `true`.
- If `runner_up_summary` is `none`, fall back to `examples/reviewer_queue_tie_playbook.md`.
- If the queue is empty, use `examples/reviewer_queue_zero_queue_playbook.md` instead.
