# CLI summary markdown status note

If one run saves a Markdown summary, keep the short stdout verdict aligned with the same regression result.

Recommended review loop:

1. run the CLI once,
2. read the stdout status line,
3. open the saved Markdown summary,
4. confirm both describe the same pass/fail and recommendation.

That pairing keeps human-ready release notes and machine-readable CI output in the same deterministic handoff.
