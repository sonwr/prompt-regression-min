# Reviewer queue priority-rank fast check

Use this quick check before posting a reviewer handoff comment.

## Fast check

1. Confirm `next_focus_priority_rank` is present in the summary output.
2. If the top two groups tie on count, also check the tie metadata and margin note.
3. If the margin is zero, mention the tie explicitly instead of implying a unique winner.
4. If the top group wins by a narrow margin, include the runner-up in the handoff note.

## Short handoff template

`Next focus: <label> (rank <n>). Runner-up: <label or none>. Tie mode: <unique|tie>.`

## Why this exists

Priority-rank output is useful only when the handoff language matches the actual tie/margin state.
