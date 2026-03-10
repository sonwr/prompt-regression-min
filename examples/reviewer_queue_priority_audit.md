# Reviewer queue priority audit

Use this mini-audit before posting a reviewer-queue handoff in CI, a PR comment, or a release note.

## Questions to answer

1. Does the chosen next-focus queue have the highest share of remaining work?
2. If there is a tie, is the tie-break rule visible in the summary payload?
3. Does the handoff mention source-case volume, not just queue count?
4. Can a reviewer tell why the runner-up queue was not selected?

## Good one-line handoff shape

> Prioritize policy-review next: largest queue share, highest source-case load, runner-up is formatting-review.

## Bad one-line handoff shape

> Review policy-review next.

The bad version names a queue but hides the evidence for why that queue won.
