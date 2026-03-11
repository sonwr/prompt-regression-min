# CLI summary markdown status note

Keep summary output predictable:

- print the short stdout summary in the same run that writes `--summary-markdown`;
- keep the markdown artifact path visible in logs or CI output;
- reuse the same artifact when sharing a reviewer handoff.

That keeps the human-readable status line and saved Markdown summary coupled.
