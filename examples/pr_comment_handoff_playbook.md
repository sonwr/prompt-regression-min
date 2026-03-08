# PR comment handoff playbook

Use this guide when you want a regression run to produce a reviewer-ready comment plus a machine-readable artifact without rewriting the summary by hand.

## Goal

Keep the handoff stable across reruns:

- markdown for humans,
- JSON for CI/parsers,
- explicit gates so the comment can explain **why** the run passed or failed.

## Recommended command

```bash
prm run   --dataset examples/dataset/word_count_range_release_notes.jsonl   --baseline examples/outputs/word_count_range_release_notes.baseline.jsonl   --candidate examples/outputs/word_count_range_release_notes.fail.candidate.jsonl   --summary-markdown artifacts/pr-comment.md   --summary-json artifacts/summary.json   --max-regressions 0   --max-changed-cases 1   --require-pass-rate-trend flat
```

## Handoff rules

1. **Generate both outputs in the same run**
   - The markdown and JSON should describe the same gate set and the same case scope.
2. **Keep scope visible**
   - If you use include/exclude filters, make sure the comment shows selected IDs or the scope reduction is obvious.
3. **Prefer explicit gate snapshots**
   - Reviewers should not need to inspect CLI history to know which thresholds were active.
4. **Document the rerun hint**
   - If a failure is expected or under investigation, note the next rerun focus (for example: narrowed shard, different candidate artifact, or changed-rate budget).

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
