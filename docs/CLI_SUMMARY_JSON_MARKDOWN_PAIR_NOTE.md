# CLI Summary JSON + Markdown Pair Note

When a reviewer or bot needs a deterministic rerun handoff, prefer one run that emits both artifacts:

- `--summary-json` for parser-safe automation
- `--summary-markdown` for human review

Keep both outputs generated from the same command so schema drift and reviewer wording drift are caught together.
