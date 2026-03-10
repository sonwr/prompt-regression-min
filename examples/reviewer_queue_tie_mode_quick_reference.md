# Reviewer queue tie-mode quick reference

Use this note when the summary payload exposes reviewer-queue ties and you need a fast handoff sentence.

## Tie modes

- `unique` — one queue clearly leads; hand off the winner directly.
- `priority-rank tie` — queues share the same visible priority rank; keep the runner-up visible in the note.
- `share tie` — queue share is effectively tied; mention the narrow lead or hold the handoff until another signal breaks the tie.

## One-line handoff patterns

- Unique: `Next focus: fix_regressions — clear lead on queue share and active-case rate.`
- Priority-rank tie: `Next focus: fix_regressions (tied on rank with inspect_flakes; keep runner-up visible in the handoff).`
- Share tie: `Hold final handoff — fix_regressions and inspect_flakes are effectively tied on queued follow-up.`

## Posting checklist

1. Confirm the queue winner is not only larger in case count but also credible on queue share.
2. If the winner still has a visible runner-up, include the tie note instead of implying certainty.
3. If no stable lead exists, prefer a hold/escalation sentence over a misleading winner-only summary.
