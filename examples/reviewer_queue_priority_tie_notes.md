# Reviewer queue priority tie notes

Use this note when two reviewer groups look equally urgent.

## Prefer the group with
- the higher failing-case count
- the larger queue share
- the more recent unresolved regressions
- the clearer next action for a human reviewer

## If the tie still remains
1. Keep the original ordering stable.
2. Mention the tie in markdown and PR-comment outputs.
3. Include one short reason the chosen group stays first.

## Example sentence
`Next focus stays on style-consistency because it matches the top case count tie and has the larger queue share.`
