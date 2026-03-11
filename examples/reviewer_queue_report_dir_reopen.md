# Reviewer queue report-dir reopen note

Use this when one deterministic run produced a shared JSON summary plus markdown/PR-comment artifacts and the next reviewer only needs the fastest reopen path.

## One-line reopen pattern

```text
Reopen <report-dir> first: summary.json + summary.md + pr-comment.md still anchor the same reviewer queue.
```

## Minimum checks

1. Confirm the three artifact names still point to the same run.
2. Reuse the queue winner from the summary instead of recomputing it by hand.
3. If the queue changed, regenerate the bundle instead of patching one file.
