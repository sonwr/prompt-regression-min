# CLI summary output bundle status note

Use this note when one regression-summary run needs to say, in one line, whether JSON, Markdown, and HTML artifacts were written successfully.

## Keep visible
- stdout status stays short enough for CI logs and PR comments
- saved artifact paths still share the same bundle identity
- failures should tell the reviewer which output is missing first

## One-line check
A good status line names the shared bundle, then calls out pass/fail for stdout plus saved outputs.
