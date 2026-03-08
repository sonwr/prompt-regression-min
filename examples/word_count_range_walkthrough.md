# Word-count range walkthrough

Use this fixture trio to smoke-test concise release-note or summarization outputs with deterministic length bounds.

```bash
PYTHONPATH=src python3 -m prompt_regression_min run \
  --dataset examples/dataset/word_count_range_release_notes.jsonl \
  --baseline examples/outputs/word_count_range_release_notes.baseline.jsonl \
  --candidate examples/outputs/word_count_range_release_notes.candidate.jsonl \
  --report .tmp/word-count-range-report.json
```

Expected outcome:
- `release-note-short` becomes a regression because the candidate is too short.
- `release-note-bullets` stays passing within the allowed word budget.
