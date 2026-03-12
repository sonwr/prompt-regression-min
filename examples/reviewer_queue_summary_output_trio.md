# Reviewer queue summary output trio

Use one short handoff line when the active queue already won and the reviewer mainly needs the summary command plus the saved artifact trio.

Template:
- Active queue: <queue> | Summary command: `python -m prompt_regression_min run ... --summary-json report.json --summary-markdown report.md --summary-html report.html` | Saved outputs: `report.json`, `report.md`, `report.html`

Keep the wording short enough for PR comments, review notes, or operator handoffs.
