# CLI summary PR comment stdout note

Use `--summary-pr-comment -` when you want the reviewer-note markdown snapshot to print directly to stdout instead of being written to a file.

This is useful for shell pipelines, CI logs, and quick copy/paste review flows where the markdown should stay visible alongside the command output.

Example:

```bash
python3 -m prompt_regression_min run \
  --dataset examples/dataset.jsonl \
  --baseline examples/baseline.jsonl \
  --candidate examples/candidate.jsonl \
  --summary-pr-comment -
```
