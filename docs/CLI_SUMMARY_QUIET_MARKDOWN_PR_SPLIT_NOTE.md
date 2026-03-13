# CLI summary quiet markdown / PR split note

Use this when one prompt-regression-min run should stay quiet on stdout but still save different reviewer-facing titles for the markdown summary and PR-comment artifact.

Checklist:
- keep `--quiet` enabled for compact logs
- allow `--summary-markdown-title` and `--summary-pr-comment-title` to differ when reviewer context needs it
- keep saved artifacts visible so title drift stays intentional and reviewable
