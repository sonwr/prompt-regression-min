# CLI summary five-repo hold-reason trim note

Use this note when the cron-facing status output must stay honest and tiny.

## Rule

Keep each repo line to:

- repo name,
- changed/unchanged state,
- validation pass/fail,
- commit/push result or one short hold reason.

## Hold-reason trim examples

- `hold: validator failed`
- `hold: uncommitted upstream changes`
- `hold: smoke test red`
- `hold: push skipped until validator passes`

Avoid stacking multiple explanations into the same line.
