# CLI summary artifact trio reopen note

When one regression check saves machine and human outputs together, keep the reopen path explicit:

- summary JSON for automation,
- summary Markdown for reviewers,
- summary HTML for browser-ready sharing.

If all three files belong to the same run, prefer one shared basename and mention that basename in the status line before push.
