# Reviewer queue queue-share decision card

Use this when the reviewer queue already has multiple groups and you need one short rule for deciding what to look at first.

## Decision order

1. Pick the queue with the highest `queue_share`.
2. If queue share ties, pick the one with the higher `source_case_rate`.
3. If both still tie, keep the built-in priority order:
   - `fix_regressions`
   - `watch_unchanged_fails`
   - `confirm_filtered_scope`
   - `resolve_skipped_cases`
4. Turn the winner into a one-line handoff: `priority label -> ids -> queue share -> source-case rate`.

## Copyable handoff shape

`P1 · fix regressions -> case ids -> 40.00% queue share -> 12.50% source-case rate`

## Good use cases

- PR comments where reviewers need one dominant focus line.
- Release notes that summarize which queue should be reviewed first.
- CI handoffs where queue share matters more than raw count alone.
