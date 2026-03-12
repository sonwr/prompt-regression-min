# reviewer queue priority ladder

Use this note when a prompt-regression-min handoff needs one compact explanation for why the next reviewer queue group is first.

## Priority order
1. `fix_regressions`
2. `watch_unchanged_fails`
3. `confirm_filtered_scope`
4. `resolve_skipped_cases`

## Why it matters
The queue should lead with regressions, then keep unresolved baseline failures visible before scope-only follow-up.
