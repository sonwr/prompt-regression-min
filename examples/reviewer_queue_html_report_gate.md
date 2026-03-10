# reviewer_queue_html_report_gate

Use this pattern when a prompt-regression run also emits an HTML artifact and you want a compact gate for reviewer handoff.

## Goal

Keep the summary claim small and reviewable:

- the JSON or CLI summary passed,
- the HTML report exists,
- the HTML report matches the queue or gate scope you claim publicly.

## Suggested check order

1. Run the normal regression command first.
2. Confirm the pass/fail gate in stdout or JSON.
3. Open the HTML report and verify that the same queue, scope, or winner label appears.
4. Post the handoff only if both the machine result and the human-readable artifact agree.

## Example handoff line

- `reviewer-queue gate passed; HTML handoff matches the winner/rank output and is ready for review.`

## When to hold the change

Hold the status update if any of the following happens:

- HTML report is missing,
- HTML report reflects an older run,
- queue winner/rank differs between CLI output and the rendered artifact.
