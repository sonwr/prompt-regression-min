# Reviewer queue tie-break guide

When reviewer queue groups are tied, keep the handoff deterministic.

## Suggested order

1. Follow the priority rank first (`P1` before `P2` before `P3`).
2. If the rank is still tied, choose the alphabetically first queue key for automation.
3. Keep the full tie summary in the markdown, PR comment, or JSON output so humans can see the runner-up context.

## Example

If `fix_regressions` and `watch_unchanged_fails` both have one case each:

- next focus key: `fix_regressions`
- runner-up key: `watch_unchanged_fails`
- tie summary: `fix_regressions=P1 · fix regressions, watch_unchanged_fails=P2 · watch unchanged fails`

This keeps bot routing stable while preserving the full reviewer picture.
