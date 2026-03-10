# Reviewer queue follow-up priority card

Use this mini-card when the JSON summary already identifies the dominant queue and you need a short human handoff.

## Decision rule

Pick the next reviewer queue by checking these signals in order:

1. higher failing case count,
2. higher queue share,
3. higher source-case rate,
4. stable tie-break metadata.

## One-line handoff shape

`Next reviewer focus: <queue> (<reason>; share <share>; source-case rate <rate>).`

## Sanity check

If the queue only wins on a tie-break and not on the main evidence fields, say that explicitly instead of presenting it as a strong lead.
