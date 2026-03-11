# Reviewer queue priority mix summary

Use this when the JSON already exposes `reviewer_queue.top` and `reviewer_queue.queue_mix_summary`, and you need one short reviewer line.

## Handoff line

Route **{{queue_label}}** first because it leads the queue mix now (`{{queue_mix_summary}}`), while the runner-up stays visible enough to reopen without re-reading the full summary.

## Why it helps

This keeps the recommendation grounded in the emitted queue composition instead of relying on a vague “highest priority” note.
