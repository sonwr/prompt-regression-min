# Reviewer queue priority-rank scope tiebreak

Use this when multiple follow-up lanes have the same case count and you need a short owner-facing note.

## Short note

Priority rank wins the tiebreak when queued case counts are equal.

- `fix_regressions` stays first because regression repair changes release confidence fastest.
- `watch_unchanged_fails` stays next when failures persist without getting worse.
- `confirm_filtered_scope` and `resolve_skipped_cases` stay behind direct correctness risk.

## Example status line

`watch_unchanged_fails` is tied on count, but loses priority rank to `fix_regressions`, so hold release wording until regression cases move.
