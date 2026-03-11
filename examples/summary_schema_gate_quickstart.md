# summary schema gate quickstart

Use this when downstream CI or PR-comment automation should fail fast if the summary contract changes.

```bash
PYTHONPATH=src python3 -m prompt_regression_min.cli run \
  --dataset examples/demo/dataset.jsonl \
  --baseline examples/demo/baseline.jsonl \
  --candidate examples/demo/candidate.jsonl \
  --summary-json artifacts/summary.json \
  --summary-json-pretty \
  --require-summary-schema-version 1
```

What this buys you:

- machine-readable output for bots
- one explicit schema pin for reviewers
- a clear failure when downstream parsers need an update
