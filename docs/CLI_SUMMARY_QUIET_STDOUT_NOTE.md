# CLI summary quiet stdout note

Use `--quiet` when you want machine-readable summary artifacts without the extra human-readable recap lines in stdout.

## Suggested CI pattern

```bash
prm compare baseline.jsonl candidate.jsonl --quiet --summary-json -
```

This keeps stdout focused on the requested summary payload while still letting file outputs or stdout summaries act as the review artifact.
