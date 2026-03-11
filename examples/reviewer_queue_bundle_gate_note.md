# Reviewer queue bundle gate note

Use this note when a prompt-regression run already emits markdown/json/html artifacts and you only need a quick reviewer-facing gate before posting status.

Quick check:
- confirm the summary status still matches the JSON payload
- confirm the markdown report names the current next-focus queue
- confirm the HTML artifact is the same run, not a stale bundle

Short status template:
- Bundle status: ready / hold
- Next focus: `<queue-key>`
- Evidence: `summary.json`, `summary.md`, `summary.html`
