# reviewer_queue_report_bundle_note

Use a small artifact bundle when triaging reviewer-queue output:

1. `--summary-json artifacts/summary.json`
2. `--summary-markdown artifacts/summary.md`
3. attach the markdown excerpt that includes `Reviewer queue next focus`

Why this helps:
- bots can parse JSON
- humans can skim markdown
- PR comments can quote the same next-focus line without re-running the job
