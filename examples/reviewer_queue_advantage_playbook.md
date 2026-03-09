# Reviewer queue advantage playbook

Use this when the summary already exposes a `next_focus` lane, but you still need to explain *why* that lane should be handled before the runner-up.

## Fast reading order

1. Read `next_focus_key` / `next_focus_label`.
2. Read `next_focus_advantage_label`.
3. Paste `next_focus_advantage_summary` into the reviewer note if the lead is meaningful.
4. If the label is `tied`, pair it with `next_focus_tie_summary` instead of pretending there is a clear winner.

## Suggested reviewer-note wording

- `clear lead` → "Start with the dominant reviewer lane first; the queue lead is material enough to justify a focused rerun."
- `narrow lead` → "Start with the dominant lane first, but keep the runner-up visible in the handoff."
- `tied` → "The first two lanes are tied; preserve deterministic priority ordering, but treat the handoff as shared."

## Example

If the summary says:

- `next_focus_label = fix regressions`
- `next_focus_advantage_label = clear lead`
- `next_focus_advantage_summary = clear lead: +2 case(s), +40.00% queue share, +33.33% active-case rate, +33.33% source-case rate`

A compact reviewer note can say:

> First rerun lane: fix regressions — clear lead: +2 case(s), +40.00% queue share, +33.33% active-case rate, +33.33% source-case rate.

That phrasing keeps the handoff deterministic without reopening the JSON artifact.
