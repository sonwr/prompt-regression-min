# Summary schema version walkthrough

Use `--require-summary-schema-version 1` when a downstream parser or CI step must reject drift in the compact JSON summary contract.

```bash
PYTHONPATH=src python3 -m prompt_regression_min.cli run \
  --dataset examples/dataset/walkthrough_pass_artifact_demo.jsonl \
  --baseline examples/outputs/walkthrough_pass_artifact_demo.baseline.jsonl \
  --candidate examples/outputs/walkthrough_pass_artifact_demo.candidate.jsonl \
  --summary-json - \
  --require-summary-schema-version 1
```

Expected behavior:
- exit code `0` when the summary schema version matches
- a `summary_schema_version` field in the emitted JSON payload
- a fast failure if a future CLI change breaks the agreed summary contract
