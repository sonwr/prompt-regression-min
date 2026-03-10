# Reviewer queue priority-rank card

Use this note when the summary already exposes reviewer queue priority ranks and you need a fast human handoff without reopening JSON.

## How to read the rank

- `1 of N` means this queue should be handled first.
- Lower ranks are follow-up queues, not ties, unless the tie fields say otherwise.
- Keep the rank together with the queue label so the reviewer sees both urgency and work type.

## Copy-ready phrases

- `P1 · fix regressions (rank 1 of 3)`
- `P2 · watch improvements (rank 2 of 3)`
- `P3 · review unchanged failures (rank 3 of 3)`

## Posting rule

When space is tight, prefer `priority label + rank + ids` in one line so the reviewer can act without opening the full markdown summary.
