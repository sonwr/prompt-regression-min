# Reviewer queue filter playbook

Use this guide when reviewer handoff output is noisy because filtered-out cases, skipped cases, and unchanged failing cases are mixed together.

## Goal

Keep the reviewer queue focused on the next actionable bucket without hiding scope changes.

## Recommended read order

1. Check `filtered_out_cases` and `filtered_out_ids` first.
   - Why: scope drift can make the queue look healthier than reality.
2. Check `skipped_cases` and `skipped_ids` second.
   - Why: skipped execution changes the reliability of every downstream rate.
3. Check `unchanged_fail`, `unchanged_fail_ids`, and any forbidden unchanged-fail regex gates.
   - Why: carryover failures are often the fastest next review target.
4. Then read `reviewer_queue.next_focus_group` and `follow_up_priority_summary`.
   - Why: the queue is most useful after scope and carryover drift are understood.

## Suggested gate combinations

- **Strict CI gate**
  - `--max-filtered-out-cases 0`
  - `--max-skipped-cases 0`
  - `--max-unchanged-fail 0`

- **Human triage gate**
  - Allow small filtered/skipped counts
  - Keep `--summary-markdown` and `--summary-pr-comment` enabled
  - Use the reviewer queue outputs to decide the next batch

## Related files

- `README.md`
- `examples/reviewer_queue_triage.md`
- `examples/pr_comment_handoff_playbook.md`
- `examples/reviewer_queue_next_focus_playbook.md`
