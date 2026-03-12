# CLI Reviewer Queue Focus Ladder Note

Use the reviewer queue as a handoff ladder instead of a flat dump.

## Suggested reading order

1. `next_focus_key` and `next_focus_priority_label`
2. `next_focus_handoff_summary`
3. `runner_up_handoff_summary`
4. `queue_mix_summary`

## Why it helps

- Keeps the first remediation target obvious for PR reviewers.
- Preserves a deterministic second target when the leading queue clears.
- Makes markdown/PR-comment exports easier to skim during release gating.

## Small review rule

If the reviewer queue is non-empty, the summary should reveal one primary follow-up lane before listing the full queue mix.
