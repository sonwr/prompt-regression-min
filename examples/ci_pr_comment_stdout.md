# CI PR comment stdout recipe

Use this recipe when CI should post the reviewer note directly from stdout instead of writing a temp markdown file first.

## Why this pattern helps

- Keeps the reviewer-facing note generated from the same CLI invocation as the JSON and markdown artifacts.
- Makes it obvious which title is meant for human review (`--summary-pr-comment-title`) versus workflow/archive output (`--summary-markdown-title`).
- Fits PR bots or workflow steps that expect a single stdout payload.

## Example command

```bash
python -m prompt_regression_min run \
  --dataset examples/dataset/walkthrough_fail_artifact_demo.jsonl \
  --baseline examples/outputs/walkthrough_fail_artifact_demo.baseline.jsonl \
  --candidate examples/outputs/walkthrough_fail_artifact_demo.candidate.jsonl \
  --summary-json .tmp/walkthrough-fail.summary.json \
  --summary-markdown .tmp/walkthrough-fail.summary.md \
  --summary-markdown-title "walkthrough release gate" \
  --summary-pr-comment - \
  --summary-pr-comment-title "walkthrough blocker note" \
  --require-summary-schema-version 1
```

## What to look for in stdout

- A reviewer-facing heading such as `## walkthrough blocker note`
- The producing tool version
- The required schema gate line
- The same regression counts and case scope that appear in the JSON/markdown artifacts

## Suggested CI flow

1. Generate JSON and markdown artifacts for archival or uploads.
2. Print the PR comment note to stdout with `--summary-pr-comment -`.
3. Hand that stdout block to the PR bot/action without rewriting the text.
4. If the note title should differ from the archived markdown title, set both title flags explicitly.

## Copy-paste shell capture

```bash
PR_NOTE="$(python -m prompt_regression_min run \
  --dataset examples/dataset/walkthrough_fail_artifact_demo.jsonl \
  --baseline examples/outputs/walkthrough_fail_artifact_demo.baseline.jsonl \
  --candidate examples/outputs/walkthrough_fail_artifact_demo.candidate.jsonl \
  --summary-pr-comment - \
  --summary-pr-comment-title "stdout blocker note" \
  --quiet || true)"

printf '%s\n' "$PR_NOTE"
```

This keeps the stdout heading stable for PR helpers that only receive one pasted markdown payload.

## Failure recovery tip

If stdout and the saved markdown disagree, regenerate both from one command instead of patching the PR note manually. That keeps reviewer comments reproducible across reruns.