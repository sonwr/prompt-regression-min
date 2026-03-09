# Reviewer queue runner-up playbook

Use this when the top rerun lane is obvious enough to act on, but you still want the second queue branch visible in a PR comment or release-review note.

## Why this exists

`prompt-regression-min` already emits a deterministic first rerun lane through reviewer-queue fields such as:

- `next_focus_key`
- `next_focus_priority_label`
- `next_focus_handoff_summary`

It also emits a structured runner-up lane so reviewers do not lose the second queue branch while fixing the first one:

- `runner_up_key`
- `runner_up_priority_label`
- `runner_up_summary`
- `runner_up_handoff_summary`

That runner-up is useful when:

- regressions clearly come first, but unchanged failures still need watchlist follow-up,
- the dominant queue only barely leads the second queue,
- you want one pasted note to cover both the immediate rerun lane and the likely next lane.

## Suggested handoff pattern

1. Paste the `next_focus_handoff_summary` as the first repair lane.
2. Paste the `runner_up_handoff_summary` immediately below it.
3. Keep the runner-up as context, not as a reason to split the first rerun.

## Example

```text
Primary rerun lane: fix_regressions=P1 · fix regressions -> `case-2`, `case-9` (2 case(s), 20.00% active-case rate, 20.00% source-case rate, 40.00% of queued follow-up)
Runner-up lane: watch_unchanged_fails=P2 · watch unchanged fails -> `case-1` (1 case(s), 10.00% active-case rate, 10.00% source-case rate, 20.00% of queued follow-up)
```

## Rule of thumb

If the runner-up exists, include it in the handoff; if it does not, keep the note focused on the single active queue lane.
