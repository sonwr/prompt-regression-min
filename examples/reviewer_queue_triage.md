# Reviewer queue triage recipe

Use this note when you need a fast, reviewer-facing explanation of *why* a rerun still needs human attention.

## When to use it

Use the reviewer queue markers when a shard or release review needs to explain:

- which active cases still need human review,
- whether the load comes from regressions or unchanged failing cases,
- and how much scope was filtered out before the run.

## Copyable command

```bash
prm run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --summary-markdown artifacts/reviewer-queue.summary.md \
  --summary-pr-comment artifacts/reviewer-queue.pr-comment.md \
  --summary-json artifacts/reviewer-queue.summary.json
```

## What to look for

Check these fields in markdown, PR-comment, or JSON output:

- `Reviewer queue total`
- `Reviewer queue rate`
- `Reviewer handoff`
- `Filtered-out IDs`
- `Skipped IDs`
- `Unchanged fail IDs`

These fields help reviewers decide whether the next action is:

1. rerun only a narrowed shard,
2. keep investigating a stable known-bad watchlist,
3. or escalate a new regression immediately.

## Recommended review note pattern

- **Scope** — mention selected IDs and filtered/skipped IDs.
- **Queue** — mention reviewer queue total + rate.
- **Action** — mention whether the next step is rerun, watchlist carryover, or blocker escalation.

Example reviewer note:

> Reviewer queue total is 3 (rate 0.75). Active scope kept `billing-login`, filtered out `search-canary`, and left `auth-timeout` on the unchanged-fail watchlist. Rerun billing-only after the prompt fix; do not treat the watchlist case as a new regression.
