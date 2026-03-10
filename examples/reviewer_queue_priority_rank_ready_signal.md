# reviewer_queue_priority_rank_ready_signal

Use this note when the reviewer queue already exposes a priority-rank winner and you need a fast post-or-hold decision.

## Ready signal

Call the handoff ready only when all four checks pass:

1. the winner queue key is explicit,
2. the visible priority rank is not contradicted by tie metadata,
3. the runner-up context is still visible when the lead is narrow,
4. the next action names who should review next.

## Post now

Post the handoff when the winner, rank, tie mode, and next action fit in one sentence without reopening the JSON output.

## Hold

Hold the handoff when the exposed rank still needs a margin note, runner-up qualifier, or tie-break explanation.
