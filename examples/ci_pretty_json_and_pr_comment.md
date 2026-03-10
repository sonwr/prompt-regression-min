# CI example: pretty JSON plus PR comment

Use this when a workflow needs both machine-readable JSON and a reviewer-ready markdown note from the same `prm run`.

## Example

```bash
python3 -m prompt_regression_min.cli run \
  --dataset examples/dataset/walkthrough_pass_artifact_demo.jsonl \
  --baseline examples/outputs/walkthrough_pass_artifact_demo.baseline.jsonl \
  --candidate examples/outputs/walkthrough_pass_artifact_demo.candidate.jsonl \
  --require-summary-schema-version 1 \
  --summary-json artifacts/summary.pretty.json \
  --summary-json-pretty \
  --summary-pr-comment artifacts/review-note.md \
  --summary-pr-comment-title "review snapshot" \
  --quiet
```

## Why this pattern helps

- `artifacts/summary.pretty.json` stays easy for humans and bots to diff.
- `artifacts/review-note.md` is ready to paste into a PR without reformatting.
- `--quiet` keeps CI logs focused on explicit artifacts instead of the human summary stream.

## Minimal checks

- Confirm the JSON file contains `"summary_schema_version": 1`.
- Confirm the PR note starts with `## review snapshot`.
- If either artifact is missing, treat the run as incomplete handoff evidence.
