# CLI Summary Quiet + Schema Note

Use this note when a prompt-regression-min workflow wants quiet stdout for humans but still needs an explicit JSON summary schema expectation for automation.

## Quick rule

- use `--quiet` when the terminal handoff should stay short
- keep the summary schema gate explicit when another parser or CI step will read the artifact
- verify the quiet human handoff and schema-bound artifact come from the same run
