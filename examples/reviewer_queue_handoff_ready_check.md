# Reviewer queue handoff ready check

Use this short check before you paste reviewer-queue output into a PR comment, issue, or chat update.

## 30-second pass

Confirm all five statements:

1. The selected next-focus queue is named explicitly.
2. The note explains *why* that queue won (share, case count, source-case rate, or tie rule).
3. Any runner-up or tie context is short but visible.
4. The handoff sentence tells the reviewer what to look at next.
5. The wording still makes sense without opening the JSON artifact.

## Good one-liner shape

- `Next reviewer focus: billing follow-ups (largest queue, 42% share; inspect checkout retry cases first).`

## Red flags

Do not post the handoff yet if the note:

- names a queue without saying why it won,
- hides a meaningful tie,
- repeats raw percentages without a next review action,
- or only makes sense when the reader already knows the summary JSON.
