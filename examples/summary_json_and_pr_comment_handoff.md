# Summary JSON And PR Comment Handoff

Use one run when CI needs a machine-readable summary plus a paste-ready reviewer note.

```bash
PYTHONPATH=src python3 -m prompt_regression_min.cli run \
  --dataset examples/fixtures/word_count_dataset.jsonl \
  --baseline examples/fixtures/word_count_baseline.jsonl \
  --candidate examples/fixtures/word_count_candidate_pass.jsonl \
  --summary-json summary/review.json \
  --summary-json-pretty \
  --summary-pr-comment summary/review-comment.md \
  --summary-pr-comment-title "review snapshot"
```

This keeps the structured JSON artifact and the reviewer-facing markdown note aligned without a second formatting pass.
