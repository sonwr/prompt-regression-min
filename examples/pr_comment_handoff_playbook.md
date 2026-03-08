# PR comment handoff playbook

Use this guide when you want a regression run to produce a reviewer-ready comment plus a machine-readable artifact without rewriting the summary by hand.

## Goal

Keep the handoff stable across reruns:

- markdown for humans,
- JSON for CI/parsers,
- explicit gates so the comment can explain **why** the run passed or failed.

## Recommended command

```bash
prm run \
  --dataset examples/dataset/word_count_range_release_notes.jsonl \
  --baseline examples/outputs/word_count_range_release_notes.baseline.jsonl \
  --candidate examples/outputs/word_count_range_release_notes.candidate.jsonl \
  --summary-pr-comment artifacts/review-note.md \
  --summary-pr-comment-title "release blocker note" \
  --summary-markdown artifacts/release-gate.summary.md \
  --summary-markdown-title "word-count release-note gate" \
  --summary-json artifacts/summary.json \
  --max-regressions 0 \
  --max-changed-cases 1 \
  --require-pass-rate-trend flat
```

Why this shape:

- `--summary-pr-comment` produces the paste-ready reviewer note directly instead of reusing markdown artifacts as an approximation.
- `--summary-pr-comment-title` lets the PR-facing heading stay reviewer-friendly even when the markdown artifact keeps a workflow/report title.
- `--summary-json` keeps the machine-readable payload aligned with the exact same gate set.

## Handoff rules

1. **Generate PR note, markdown, and JSON in the same run**
   - The reviewer note, markdown summary, and JSON should describe the same gate set and the same case scope.
2. **Keep scope visible**
   - If you use include/exclude filters, make sure the comment shows selected IDs or the scope reduction is obvious.
3. **Prefer explicit gate snapshots**
   - Reviewers should not need to inspect CLI history to know which thresholds were active.
4. **Document the rerun hint**
   - If a failure is expected or under investigation, note the next rerun focus (for example: narrowed shard, different candidate artifact, or changed-rate budget).
5. **Separate reviewer wording from artifact wording when needed**
   - Use `--summary-pr-comment-title` for paste-ready notes and keep `--summary-markdown-title` focused on the workflow/report name.

## Output mode quick picks

- **Write files for CI upload** — use concrete paths for `--summary-pr-comment`, `--summary-markdown`, and `--summary-json`.
- **Print the reviewer note to stdout** — use `--summary-pr-comment -` when a PR bot or workflow step will post it directly.
- **Print markdown to stdout** — use `--summary-markdown -` when you need a release-note style summary in logs or downstream tooling.

## Copy-paste PR comment skeleton

```md
## prompt-regression-min summary

- Status: **FAIL**
- Scope: shard/release-note smoke
- Why it failed: regression budget exceeded
- What changed: see `regression_ids` and `changed_ids`
- Next rerun: rerun only release-note shard after fixing candidate wording
```

## Reviewer checklist

- Does the markdown summary match the JSON payload status?
- Are the active thresholds visible in the gate snapshot?
- Are regression/improved/unchanged buckets explicit enough for the next person to rerun?
