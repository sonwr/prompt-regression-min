# reviewer_queue_html_handoff_note

Use this note when a reviewer queue summary needs a compact HTML-friendly companion view.

## Keep the HTML layer shallow

- surface `next_focus_group`, queue share, and follow-up priority first
- mirror the JSON/markdown labels instead of renaming fields for presentation
- keep one card per queue group so reviewer routing stays scannable

## Minimum card contents

1. Group label and priority rank
2. Case count, queue share, and source-case rate
3. Tie mode or advantage summary when present
4. Suggested owner handoff line

## Validation reminder

After changing reviewer-queue outputs, regenerate committed walkthrough artifacts before commit so docs and emitted schema stay in sync.
