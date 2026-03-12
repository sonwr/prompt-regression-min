# CLI summary schema version note

When a downstream CI step expects a stable summary payload shape, run the smallest summary command with `--require-summary-schema-version` before posting or pushing the saved bundle.

Recommended replay loop:

```bash
python3 -m prompt_regression_min.cli run \
  --baseline baseline.jsonl \
  --candidate candidate.jsonl \
  --require-summary-schema-version 1 \
  --summary-json out/summary.json
```

That keeps schema gating explicit in the command line instead of relying on reviewers to notice a payload drift after the fact.
