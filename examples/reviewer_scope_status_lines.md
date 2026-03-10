# Reviewer scope status line examples

Use a scope status line when the regression summary is correct, but the public reviewer update should stay narrowly framed.

## Template

`Reviewer scope: keep the update scoped to <suite/case ids> + <summary artifact> until <follow-up check> finishes.`

## Examples

- `Reviewer scope: keep the update scoped to smoke-pass fixtures + examples/pass_fail_walkthrough.md until the full shard rerun finishes.`
- `Reviewer scope: keep the update scoped to trend-summary cases + summary.json until the PR-comment formatter rerun finishes.`
- `Reviewer scope: keep the update scoped to regex-flag validation + fail_summary.md until multilingual punctuation cases finish.`

## Why this helps

A short scope line prevents reviewers from over-reading a partial PASS as a release-wide green light.
