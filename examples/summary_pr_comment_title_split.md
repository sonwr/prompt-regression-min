# Summary PR comment title split

Use a separate PR-comment heading when the markdown artifact should keep a durable report name but the pasted reviewer note should sound like a decision.

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/walkthrough_fail_artifact_demo.jsonl \
  -b examples/outputs/walkthrough_fail_artifact_demo.baseline.jsonl \
  -c examples/outputs/walkthrough_fail_artifact_demo.candidate.jsonl \
  --summary-markdown artifacts/release-gate.md \
  --summary-markdown-title "release gate artifact" \
  --summary-pr-comment - \
  --summary-pr-comment-title "release blocker note" \
  --quiet
```

Use this when:

- the artifact title should stay stable across reruns,
- the pasted PR note should read like an approval or blocker update,
- and reviewer-facing language should change without renaming the saved markdown artifact.
