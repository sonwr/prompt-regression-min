# CLI Pass-Rate Trend Gate Note

Keep `--require-pass-rate-trend` explicit when a saved summary bundle is meant to represent a release gate.
If downstream reviewers are looking at `--summary-json`, `--summary-markdown`, or `--summary-pr-comment` artifacts, the expected trend should be visible in the command line too.
Use `improving` or `flat` for release-facing checks; reserve `regressing` for fixture coverage or failure-mode tests.
