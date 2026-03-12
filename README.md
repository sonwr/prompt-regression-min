# prompt-regression-min

Minimal, deterministic regression checks for prompt and workflow changes in LLM-powered products.

`prompt-regression-min` helps teams answer one practical question before shipping:

> **Did this prompt/model/workflow change improve quality, or quietly break something?**

---

## Table of Contents

- [Project Introduction](#project-introduction)
- [Vision](#vision)
- [Philosophy](#philosophy)
- [Who This Is For](#who-this-is-for)
- [What It Does Today](#what-it-does-today)
- [Quickstart](#quickstart)
- [Core Concepts](#core-concepts)
- [Data Format](#data-format)
- [CLI Reference](#cli-reference)
- [Example Output](#example-output)
- [PR Comment Tips](#pr-comment-tips)
- [JSONL Case Hygiene](#jsonl-case-hygiene)
- [CI/CD Integration](#cicd-integration)
- [Development Direction](#development-direction)
- [Quality and Contribution Guidelines](#quality-and-contribution-guidelines)
- [FAQ](#faq)
- [License](#license)

---

## Project Introduction

In real-world LLM systems, regressions rarely appear as crashes. They show up as:

- answers becoming less specific,
- policies being skipped,
- key terms disappearing,
- or edge-cases quietly failing.

`prompt-regression-min` is intentionally small and strict.
It compares **baseline** and **candidate** outputs on the same test set and reports:

- pass-rate changes,
- regressions,
- improvements,
- unchanged behavior.

The goal is to become a lightweight quality gate that is easy to adopt in any repo.

## Quick validation loop

When updating CLI summaries, examples, or docs, run the smallest reproducible local check first:

```bash
python3 -m unittest tests/test_core.py tests/test_cli.py
```

That keeps the README examples, CLI output, and summary payload expectations moving together.
If you want the quietest machine-readable handoff for CI logs, open `docs/CLI_SUMMARY_QUIET_STDOUT_NOTE.md` before combining `--quiet` with summary artifact flags.
If you need the shortest reminder that quiet stdout still pairs cleanly with saved JSON/Markdown/HTML artifacts, open `docs/CLI_SUMMARY_QUIET_BUNDLE_NOTE.md`.
If you need a compact reminder for keeping saved Markdown summaries paired with the same stdout status line, open `docs/CLI_SUMMARY_MARKDOWN_STATUS_NOTE.md`.
If you need a compact reminder for one summary run that saves JSON, Markdown, and HTML artifacts together, open `docs/CLI_SUMMARY_ONE_BUNDLE_NOTE.md`.
If you need a compact note for keeping the same report basename across saved JSON, Markdown, and HTML artifacts, open `docs/CLI_SUMMARY_SHARED_BASENAME_NOTE.md`.
For release-wide CLI or summary payload edits, run `python3 -m unittest discover -s tests` so the full regression and rendering contract stays aligned.
If you need a compact phrase set for reviewer-queue handoffs, start with `examples/reviewer_queue_priority_labels.md`.
If you need a one-line PR-comment handoff sentence, open `examples/reviewer_queue_priority_handoff_card.md`.
If you need a compact owner handoff template after queue selection, open `examples/reviewer_queue_owner_handoff_template.md`.
If you need a compact reviewer note for JSON-exposed scaffold presets, open `examples/reviewer_queue_presets_json_handoff.md`.
If you need a compact rule for naming the winning queue, shared report bundle, and owner in that order, open `examples/reviewer_queue_report_bundle_priority_note.md`.
If you need a compact note for title-ready reviewer bundles that still need deterministic shared artifact naming, open `examples/reviewer_queue_title_and_basename_handoff.md`.
If you need a compact note for keeping the queue winner, pass-rate trend gate, and saved summary bundle in one reviewer handoff, open `examples/reviewer_queue_trend_bundle_handoff.md`.
If you need the shortest reviewer handoff that reopens both JSON and markdown artifacts together, open `examples/reviewer_queue_json_bundle_quickstart.md`.
If you need a one-line note that points reviewers to the full summary artifact bundle, open `examples/reviewer_queue_artifact_bundle_note.md`.
If you need a shorter queue-plus-bundle status sentence once the winner is already known, open `examples/reviewer_queue_bundle_scope_quick_note.md`.
If you need a markdown-first reopen cue for the same handoff, open `examples/reviewer_queue_markdown_bundle_note.md`.
If you need a two-line handoff that pairs the active reviewer queue with the exact artifact bundle to reopen first, open `examples/reviewer_queue_artifact_reopen_line.md`.
If you need a compact naming rule for that JSON/HTML reviewer bundle, open `examples/reviewer_queue_report_bundle_name_note.md`.
If you need a compact example for reviewer-queue markdown/json/html bundle checks before posting a short status, open `examples/reviewer_queue_bundle_gate_note.md`.
If you need a compact handoff that names the active reviewer queue, the winning reason, and the shared report bundle in one pass, open `examples/reviewer_queue_report_bundle_handoff_card.md`.
If you need a one-line scope-safe note that names the active reviewer queue and the shared JSON/Markdown/HTML bundle together, open `examples/reviewer_queue_report_bundle_scope_note.md`.
If you need a compact release-gate reminder for keeping `--require-pass-rate-trend` explicit before sharing a saved summary bundle, open `docs/CLI_PASS_RATE_TREND_GATE_NOTE.md`.
If you need a compact baseline reminder before reopening that shared report bundle, open `examples/reviewer_queue_report_bundle_baseline_note.md`.
If you need the shortest reopen cue for one reviewer queue plus one shared report bundle, open `examples/reviewer_queue_report_bundle_start.md`.
If you need a compact pre-post audit for reopening the JSON summary, HTML report, and queue handoff together, open `examples/reviewer_queue_report_bundle_reopen_check.md`.
If you need a one-line reviewer note for reopening the queue with the shared JSON, markdown, and HTML bundle, open `examples/reviewer_queue_html_bundle_reopen_note.md`.
If you need a shorter handoff sentence that names the recommendation, queue lead, and shared report bundle together, open `examples/reviewer_queue_report_bundle_handoff.md`.
If you need a shorter handoff sentence that names the recommendation, queue lead, and shared report bundle together, open `examples/reviewer_queue_report_bundle_handoff.md`.
If you need a one-line follow-up for a queue that is already stable enough to trust, open `examples/reviewer_queue_stable_bundle_handoff.md`.
If you need a slightly broader follow-up that keeps the selected reviewer queue tied to the shared JSON / Markdown / HTML bundle, open `examples/reviewer_queue_report_bundle_followup_card.md`.
If you need a compact gate for deciding whether that same stable queue still has a believable shared report bundle behind it, open `examples/reviewer_queue_stable_bundle_gate.md`.
If you need a one-sentence summary based on queue share and source-case rate, open `examples/reviewer_queue_share_quick_note.md`.
If you need a one-line reviewer update specifically for HTML-ready queue reports, open `examples/reviewer_queue_html_report_status_line.md`.
If you need a one-line reviewer update that also names the regenerated JSON/Markdown/HTML bundle, open `examples/reviewer_queue_report_bundle_status_line.md`.
If you need a compact handoff that keeps the winning reviewer queue, its priority rank, and the shared artifact bundle visible together, open `examples/reviewer_queue_priority_rank_bundle_handoff.md`.
If you need a compact reminder to keep the saved JSON/Markdown/HTML report paths visible in that same handoff, open `docs/CLI_SUMMARY_REPORT_PATHS_NOTE.md`.
If you need a one-line reminder to keep the summary status and saved artifact paths together, open `docs/CLI_SUMMARY_REPORT_STATUS_AND_PATHS_NOTE.md`.
If you need a quick one-line note that explains the winning queue using queue share alone, open `examples/reviewer_queue_share_quick_note.md`.
If you need the matching handoff when queue share and source-case rate should stay visible together, open `examples/reviewer_queue_share_and_source_case_handoff.md`.
If you need a slightly fuller one-card update for the same HTML-ready bundle handoff, open `examples/reviewer_queue_html_bundle_status_card.md`.
If you need a compact replay note for reopening the queue decision together with its saved artifact bundle, open `examples/reviewer_queue_bundle_replay_note.md`.
If you need the same update to stay explicitly scoped to the shared report bundle, open `examples/reviewer_queue_report_bundle_scope_status_line.md`.
If you need a compact gate before trusting that HTML-ready handoff, open `examples/reviewer_queue_html_report_gate.md`.
If you need a compact owner-facing gate before reposting a saved reviewer queue bundle, open `examples/reviewer_queue_report_bundle_owner_gate.md`.
If you need a quick reopen check before posting that HTML-ready handoff, open `examples/reviewer_queue_html_report_download_gate.md`.
If you need a quick artifact check before claiming the HTML-ready bundle is reviewable, open `examples/reviewer_queue_html_report_bundle_check.md`.
If you need a compact owner-facing cue that names the active reviewer queue, the report basename, and the saved JSON / Markdown / HTML trio together, open `examples/reviewer_queue_bundle_owner_handoff.md`.
If you need a compact note for keeping reviewer-facing bundle filenames stable with `--report-file-stem`, open `examples/reviewer_queue_report_file_stem_note.md`.
If you need a short reminder that one stable basename should anchor the saved JSON/Markdown/HTML summary trio, open `docs/CLI_SUMMARY_BASENAME_NOTE.md`.
If you need the shortest reviewer cue for a queue summary that already includes the baseline vs candidate case counts, open `examples/reviewer_queue_case_count_status_line.md`.
If you need a compact reminder for quiet stdout plus saved JSON artifacts in the same review bundle, open `docs/CLI_SUMMARY_QUIET_JSON_BUNDLE_NOTE.md`.
If the HTML summary layout changed and you need a visual reviewer pass, open `examples/reviewer_queue_html_report_visual_check.md`.
If you need a one-line note for the queue that stays next after the current focus, open `examples/reviewer_queue_runner_up_handoff_card.md`.
If you need a compact reviewer handoff for a small but still non-empty rerun queue, open `examples/reviewer_queue_small_batch_handoff.md`.
If you need a compact yes/no note for whether the current next-focus queue still has enough evidence to justify a short progress post, open `examples/reviewer_queue_progress_post_gate.md`.
If you need a one-line reminder to keep the rerun winner paired with its report bundle in a release review, open `examples/reviewer_queue_release_gate_bundle_scope_card.md`.
If you need a one-line reviewer update once the priority-rank winner is already trustworthy, open `examples/reviewer_queue_priority_rank_quick_post.md`.
If you need a compact reminder to keep the exposed priority label attached to the winning reviewer queue and saved bundle handoff, open `docs/CLI_REVIEWER_QUEUE_PRIORITY_LABELS_NOTE.md`.
If you need a one-line reviewer cue for keeping the winning queue share visible beside that same priority label, open `docs/CLI_REVIEWER_QUEUE_SHARE_PRIORITY_NOTE.md`.
If you need a compact reviewer note for the ranked winner before reopening the bundle, open `examples/reviewer_queue_priority_rank_triage_card.md`.
If you need a compact priority-rank note that keeps both the winner and the runner-up visible in one sentence, open `examples/reviewer_queue_priority_rank_runner_up_note.md`.
If you need a fast pre-commit review pass for next-focus handoffs, open `examples/reviewer_queue_followup_checklist.md`.
If you need to explain why one queue became the next reviewer focus, open `examples/reviewer_queue_next_focus_playbook.md`.
If you need a one-sentence reviewer note for the unique next-focus queue, open `examples/reviewer_queue_next_focus_one_liner.md`.
If you need a shortest-path order for turning queue metadata into a human handoff, open `examples/reviewer_queue_handoff_sequence.md`.
If you need a compact first-pass audit before posting the handoff, open `examples/reviewer_queue_first_pass_checklist.md`.
If you need a compact rule card for choosing the next reviewer queue during ties or close calls, open `examples/reviewer_queue_priority_decision_card.md`.
If you need the shortest copy-ready command for pinning downstream automation to one summary contract, open `examples/summary_schema_gate_quickstart.md`.
If you need a queue-share-first rule card for picking the dominant reviewer focus, open `examples/reviewer_queue_queue_share_decision_card.md`.
If you need a queue-share-first rule card for picking the dominant reviewer focus, open `examples/reviewer_queue_queue_share_decision_card.md`.
If you need a copy-ready next-focus reviewer note without reopening JSON, open `examples/reviewer_queue_next_focus_handoff_card.md`.
If you need a short audit for whether the selected queue actually has a convincing lead, open `examples/reviewer_queue_next_focus_advantage_audit.md`.
If you need a final yes/no check before posting the reviewer handoff, open `examples/reviewer_queue_post_ready_check.md`.
If you need a compact last-mile check for whether the handoff sentence is actually human-ready, open `examples/reviewer_queue_handoff_ready_check.md`.
If you need the shortest queue-first note that keeps the selected reviewer lane paired with its saved markdown/html/json report bundle, open `examples/reviewer_queue_bundle_start_note.md`.
If you need one compact gate that keeps the selected reviewer queue tied to its saved report bundle before sharing the handoff, open `examples/reviewer_queue_report_bundle_gate.md`.
If you need a compact audit for whether the dominant reviewer queue really deserves the next-focus callout, open `examples/reviewer_queue_dominant_focus_checklist.md`.
If you need a short reopen handoff for the next reviewer queue plus its saved artifact bundle, open `docs/CLI_REVIEWER_QUEUE_REOPEN_NOTE.md`.
If you want a compact reminder to keep one CLI command, one summary artifact, and one reviewer-facing drift line in the same proof loop, open `docs/CLI_SUMMARY_REPORT_NOTE.md`.
If you need a one-line gate note for pairing the next-focus reviewer queue with one saved artifact path, open `examples/reviewer_queue_next_focus_gate_note.md`.
If you need a compact reminder to keep one explicit owner with that saved summary bundle, open `docs/CLI_SUMMARY_REPORT_OWNER_NOTE.md`.
If you need a short reviewer cue for keeping the saved summary bundle paired with one named report owner, open `docs/CLI_SUMMARY_BUNDLE_OWNER_NOTE.md`.
If you need a compact note for keeping stdout summary text paired with the saved summary bundle in one reviewer handoff, open `docs/CLI_SUMMARY_STDOUT_BUNDLE_NOTE.md`.
If you need a compact reviewer cue for keeping one saved HTML summary paired with the same `--summary-pr-comment` handoff, open `docs/CLI_SUMMARY_HTML_PR_COMMENT_NOTE.md`.

If you need a compact note for keeping one reviewer-facing subtitle attached to the same saved summary bundle, open `docs/CLI_SUMMARY_REPORT_SUBTITLE_NOTE.md`.
If you need a compact note for keeping one reviewer-facing subject attached to that same saved summary bundle, open `docs/CLI_SUMMARY_REPORT_SUBJECT_NOTE.md`.
If you need a compact reviewer note that keeps report subject and report owner paired on the same saved summary bundle, open `docs/CLI_SUMMARY_REPORT_SUBJECT_OWNER_NOTE.md`.
If you need the narrowest start for that same saved summary bundle with subject + owner metadata, open `docs/CLI_SUMMARY_REPORT_SUBJECT_OWNER_START.md`.
If you need the shortest start note for that same subject+owner handoff, open `docs/CLI_SUMMARY_REPORT_SUBJECT_OWNER_START_NOTE.md`.
If you need a compact note for keeping pass-rate delta, recommendation, and saved bundle basename visible in one reviewer-ready status line, open `docs/CLI_SUMMARY_STATUS_TRIO_NOTE.md`.
If you need a compact reviewer note for keeping one summary subject, owner, and markdown bundle aligned after `--summary-report`, open `docs/CLI_SUMMARY_MARKDOWN_OWNER_SUBJECT_NOTE.md`.
If you need a compact markdown status line that keeps owner and pass/fail state visible together, open `docs/CLI_SUMMARY_MARKDOWN_STATUS_OWNER_NOTE.md`.

If you need a one-line owner-ready handoff that still keeps the active reviewer queue tied to its shared artifact bundle, open `examples/reviewer_queue_bundle_owner_ready_note.md`.
If you need a short evidence-first review pass before posting the selected queue, open `examples/reviewer_queue_priority_audit.md`.
If you need a compact four-step tie-break before forcing a single next-focus queue, open `examples/reviewer_queue_tie_break_sequence.md`.
If you need a quick top-two comparison before posting a near-tied reviewer handoff, open `examples/reviewer_queue_top_two_checklist.md`.
If you need a compact reminder for the next reviewer follow-up sentence, open `examples/reviewer_queue_followup_priority_card.md`.
If you need a single-line reviewer handoff after the next-focus queue is chosen, open `examples/reviewer_queue_next_focus_status_line.md`.
If you need a short status-card version once the priority-rank winner is already known, open `examples/reviewer_queue_priority_rank_status_card.md`.
If you need that handoff to keep source-dataset impact visible in one sentence, open `examples/reviewer_queue_source_case_note.md`.
If you need a compact note for keeping a priority-rank winner paired with `source_case_rate` before posting, open `examples/reviewer_queue_priority_rank_source_case_gate.md`.
If you need a compact example that explains source-case rate when the active window is empty, open `examples/reviewer_queue_source_case_rate_note.md`.
If you need a quick rank-first phrase for the queue that should be handled next, open `examples/reviewer_queue_priority_rank_card.md`.
If you need a single-line reviewer update once the rank is already known, open `examples/reviewer_queue_priority_rank_status_line.md`.
If you need a one-line note for explaining that the exposed priority-rank lead is still narrow, open `examples/reviewer_queue_priority_rank_margin_note.md`.
- `examples/reviewer_queue_next_focus_owner_ping.md` — owner ping line when the next-focus queue is clear but still needs a named action.
If you need a compact note that keeps the runner-up visible when the next-focus lead is real but still close, open `examples/reviewer_queue_runner_up_boundary_note.md`.
If you need a compact rule for keeping a reported winner narrow when the queue lead is real but still modest, open `examples/reviewer_queue_priority_rank_narrow_lead_rule.md`.
If you need a slightly fuller one-sentence handoff that still keeps the runner-up visible, open `examples/reviewer_queue_priority_rank_margin_summary.md`.
If you need a compact yes/no gate before posting a narrow priority-rank winner, open `examples/reviewer_queue_priority_rank_margin_gate.md`.
If you need a compact pre-post audit before trusting the exposed priority rank, open `examples/reviewer_queue_priority_rank_checklist.md`.
If you need a compact sentence for keeping a narrow priority-rank lead credible without hiding the runner-up, open `examples/reviewer_queue_priority_rank_boundary_note.md`.
If you need a final yes/no rule before posting that priority-rank winner publicly, open `examples/reviewer_queue_priority_rank_posting_rule.md`.
If you need a one-screen exit check before posting the final priority-rank handoff, open `examples/reviewer_queue_priority_rank_exit_check.md`.
If you need a compact ready-to-post cue after the priority-rank winner is exposed, open `examples/reviewer_queue_priority_rank_ready_signal.md`.
If you need a last-pass post-ready audit before sending that winner to reviewers, open `examples/reviewer_queue_priority_rank_post_ready_check.md`.
If you need a last-pass human-handoff check before posting that winner, use `examples/reviewer_queue_priority_rank_ready_signal.md` to confirm the winner, tie mode, narrow-lead context, and next action still align.
If you need a ready-to-paste owner note once the priority rank is already decided, open `examples/reviewer_queue_priority_rank_owner_note.md`.
If you need a 30-second owner-ready audit before posting that winner, open `examples/reviewer_queue_priority_rank_owner_ready_check.md`.
If you need a short owner-ready bridge from the exposed winner to one reviewable handoff sentence, open `examples/reviewer_queue_priority_rank_owner_ready_bridge.md`.
If you need the shortest owner-facing line after the rank is already exposed, open `examples/reviewer_queue_priority_rank_owner_handoff_line.md`.
If you need a compact escalation handoff once the winning queue still needs an explicit owner escalation, open `examples/reviewer_queue_owner_escalation_card.md`.
If you need a compact last-pass audit before trusting the exposed priority rank in a human handoff, open `examples/reviewer_queue_priority_rank_quick_audit.md`.
If you need a compact check for whether the visible priority-rank lead is large enough to post without hiding the runner-up, open `examples/reviewer_queue_priority_rank_gap_check.md`.
If you need a one-sentence note for a winner that still has only a narrow lead, open `examples/reviewer_queue_priority_rank_gap_summary.md`.
If you need a compact wording note for keeping that exposed winner intentionally scope-limited, open `examples/reviewer_queue_priority_rank_scope_note.md`.
If you need the shortest winner-first wording path before the larger scope examples, open `examples/reviewer_queue_priority_rank_scope_quickstart.md`.
If you need a one-screen release-note version of that same scope rule, open `examples/reviewer_queue_priority_rank_scope_release_note.md`.
If you need copy-ready examples for winner-only, narrow-lead, or shared-focus scope wording, open `examples/reviewer_queue_priority_rank_scope_examples.md`.
If you need a one-line queue-scoped update once the priority-rank winner is already known, open `examples/reviewer_queue_priority_rank_scope_status_line.md`.
If you need the shortest winner-first path before opening the larger tie/hold playbooks, open `examples/reviewer_queue_priority_rank_scope_quickstart.md`.
If you need the shortest winner-first wording path before opening the larger playbooks, start with `examples/reviewer_queue_priority_rank_scope_quickstart.md`.
If you need a one-line release-gate note once the priority-rank winner is stable enough to drive the next ship/no-ship conversation, open `examples/reviewer_queue_priority_rank_release_gate.md`.
If you need a slightly fuller release-facing handoff once that winner is already clear, open `examples/reviewer_queue_priority_rank_release_handoff.md`.
If you need a compact note that keeps the winning queue plus the shared JSON/Markdown/HTML report bundle visible in one release-gate handoff, open `examples/reviewer_queue_release_gate_bundle_note.md`.
If you need a one-line release-facing note that keeps the priority-rank winner paired with the saved bundle path, open `examples/reviewer_queue_priority_rank_release_bundle_note.md`.
If you need a shorter release-facing note that keeps the exposed priority-rank winner honest about scope, open `examples/reviewer_queue_priority_rank_scope_release_gate.md`.
If you need a compact reviewer note for bundles that also keep the runner-up queue visible beside the current winner, open `examples/reviewer_queue_bundle_runner_up_note.md`.
If you need a compact triage card that pairs the exposed winner with the immediate reviewer action, open `examples/reviewer_queue_priority_rank_triage_card.md`.
If you need a shortest-path note for reopening the runner-up after the winner is already posted, open `examples/reviewer_queue_runner_up_note.md`.
If you need a compact queue-scoped handoff sentence that keeps queue share and source-case impact together, open `examples/reviewer_queue_scope_handoff_card.md`.
If you need a one-line bridge from source-case impact to the owner who should act next, open `examples/reviewer_queue_source_case_owner_bridge.md`.
If you need a one-line note that says the runner-up still deserves review even after a clear lead appears, open `examples/reviewer_queue_runner_up_keepalive_note.md`.
If you need a broader rule for keeping that queue-scoped sentence intentionally narrow, open `examples/reviewer_queue_scope_status_rule.md`.
If you need a compact last-pass audit before posting a priority-rank winner as a queue-scoped handoff, open `examples/reviewer_queue_priority_rank_scope_checklist.md`.
If you need a deterministic tie-break rule before naming the next reviewer focus, open `examples/reviewer_queue_next_focus_tie_break_card.md`.
If you need a compact note that keeps every tied first lane visible in one handoff, open `examples/reviewer_queue_next_focus_tie_summary.md`.
If you need a compact reference for how to word unique, rank-tied, or share-tied reviewer handoffs, open `examples/reviewer_queue_tie_mode_quick_reference.md`.
If you need a one-line reviewer note that keeps the current winner and tie context together, open `examples/reviewer_queue_tie_handoff_note.md`.
If you need the shortest reviewer-ready status line once the next focus is settled, open `examples/reviewer_queue_next_focus_quick_brief.md`.
If you need a one-sentence owner-facing update once the next focus is already known, open `examples/reviewer_queue_next_focus_owner_note.md`.
If you need a one-line explanation for why the selected queue still wins when the lead is narrow, open `examples/reviewer_queue_priority_margin_card.md`.
If you need a compact last-pass audit before trusting that narrow lead in a human handoff, open `examples/reviewer_queue_priority_margin_audit.md`.
If you need a compact rule card for breaking reviewer handoff ties that share the same priority rank, open `examples/reviewer_queue_priority_rank_tie_card.md`.
If you need a one-line reopen cue for that same tied-rank case with bundle-proof language, open `examples/reviewer_queue_priority_rank_reopen_tiebreak.md`.
If you need a quick checklist before calling that tie a real shared next focus, open `examples/reviewer_queue_priority_rank_tie_checklist.md`.
If you need a compact wording note for a tied priority rank with only a narrow margin cue, open `examples/reviewer_queue_priority_rank_tie_margin_note.md`.
If you need a one-line confidence qualifier when the exposed priority-rank winner still has a visible runner-up, open `examples/reviewer_queue_priority_rank_confidence_note.md`.
If you need a compact bridge sentence when the next-focus winner still has a narrow lead, open `examples/reviewer_queue_next_focus_gap_bridge.md`.
If you need a compact owner bridge once the priority-rank winner is already clear, open `examples/reviewer_queue_priority_rank_owner_bridge.md`.
If you need a compact rule for when an exposed priority rank should still stay on hold instead of becoming a decisive handoff, open `examples/reviewer_queue_priority_rank_hold_boundary.md`.
If you need copy-ready hold wording examples before posting that scoped update, open `examples/reviewer_queue_priority_rank_hold_examples.md`.
If you need a one-line reviewer note for that hold state without reopening the longer checklist, open `examples/reviewer_queue_priority_rank_hold_note.md`.
If you need a copy-ready sentence for that hold state without reopening the larger playbook, open `examples/reviewer_queue_next_focus_hold_note.md`.
If you need a quick post-versus-hold decision before naming the next reviewer focus, open `examples/reviewer_queue_next_focus_decider.md`.
If you need a compact rank-first note for whether to hold or post the exposed winner, open `examples/reviewer_queue_priority_rank_hold_vs_post.md`.
If you need a compact command-first reminder for turning the chosen queue into a quick owner status update, open `examples/reviewer_queue_owner_status_command.md`.
If you need a 20-second audit before posting that owner update, open `examples/reviewer_queue_owner_status_ready_check.md`.
If you need a short tiebreak note when reviewer-queue counts are equal, open `examples/reviewer_queue_priority_rank_scope_tiebreak.md`.
If you need the shortest rank-first route from exposed queue metadata to a human handoff, open `examples/reviewer_queue_priority_rank_sequence.md`.
If you need a compact winner-only sentence once the exposed priority rank is already trustworthy, open `examples/reviewer_queue_priority_rank_winner_note.md`.

---
If you need one compact explanation for why the next queue is ahead, tied, or solo, open `examples/reviewer_queue_next_focus_advantage_summary.md`.

## Vision

Build a "small but reliable" open-source quality layer for LLM iteration.

### Near-term vision

- Make prompt/workflow evaluation reproducible in under 5 minutes.
- Integrate cleanly with CI for pass/fail decisions.
- Keep logic deterministic and easy to audit.

### Mid-term vision

- Add weighted and semantic scoring while keeping deterministic baselines.
- Provide richer developer reports (JSON + HTML).
- Support team-level quality contracts (per-domain thresholds).

### Long-term vision

A composable evaluation toolkit where teams can plug in:

- syntax-level checks,
- semantic checks,
- policy checks,
- and business KPI checks,

without losing simplicity.

---

## Philosophy

### 1) Determinism first
If quality cannot be reproduced, it cannot be trusted.

### 2) Small surface area
Fewer moving parts means easier adoption and lower maintenance cost.

### 3) Explicit tradeoffs
Every scorer has failure modes; make them visible instead of hiding complexity.

### 4) CI-native by default
Tooling should fit shipping workflows, not add ceremony.

### 5) Open by design
Readable code, inspectable data format, and practical docs over hype.

---

## Who This Is For

- Teams iterating on prompts rapidly
- Agent/workflow products with frequent model routing changes
- Developers who need fast regression signals before deploy
- OSS maintainers who want transparent quality checks in public repos

---

## What It Does Today

- Compares **baseline** vs **candidate** outputs on shared cases
- Supports lightweight expectation scorers:
  - `exact`
  - `exact_ci`
  - `not_exact`
  - `not_exact_ci`
  - `substring`
  - `substring_ci`
  - `not_substring`
  - `not_substring_ci`
  - `contains_all`
  - `contains_all_ci`
  - `contains_any`
  - `contains_any_ci`
  - `contains_all_ordered`
  - `contains_all_ordered_ci`
  - `equals_any`
  - `equals_any_ci`
  - `not_contains`
  - `not_contains_ci`
  - `contains_none` (alias of `not_contains`)
  - `contains_none_ci` (alias of `not_contains_ci`)
  - `starts_with`
  - `starts_with_ci`
  - `not_starts_with`
  - `not_starts_with_ci`
  - `ends_with`
  - `ends_with_ci`
  - `not_ends_with`
  - `not_ends_with_ci`
  - `regex` (with optional `IGNORECASE`, `MULTILINE`, `DOTALL`, `VERBOSE` flags; short aliases `i`, `m`, `s`, `x` also work; `expected.flags` accepts either a list or a comma/pipe/whitespace-delimited string, newline-delimited flag strings also work, blank list entries are ignored, `expected.flag` works as a single-flag alias, and case/whitespace-insensitive tokens like `" ignorecase "` are normalized)
  - `regex_ci` (alias of `regex` with implicit `IGNORECASE`)
  - `regex_fullmatch` (same flags, but requires the entire output to match)
  - `regex_fullmatch_ci` (alias of `regex_fullmatch` with implicit `IGNORECASE`)
  - `not_regex` (same flags, but fails if the pattern appears anywhere)
  - `not_regex_ci` (alias of `not_regex` with implicit `IGNORECASE`)
  - `not_regex_fullmatch` (same flags, but fails if the entire output matches the pattern)
  - `not_regex_fullmatch_ci` (alias of `not_regex_fullmatch` with implicit `IGNORECASE`)
  - `word_count_range` (enforces lower/upper output-length bounds using whitespace-delimited word counts)
  - `line_count_range` (enforces lower/upper output-length bounds using newline-delimited line counts)
  - `paragraph_count_range` (enforces lower/upper output-length bounds using blank-line-delimited paragraph counts for release notes, summaries, or email drafts)
  - `sentence_count_range` (enforces lower/upper output-length bounds using punctuation-delimited sentence counts for summaries, reviewer notes, or support replies, including multilingual `. ! ? 。 ！ ？` sentence endings while ignoring inverted Spanish openers `¿` / `¡`)
  - `char_count_range` (enforces lower/upper output-length bounds using raw character counts)
  - `byte_count_range` (enforces UTF-8 byte-length bounds for UI labels, commit titles, or multilingual outputs)
- Example fixture trio for deterministic release-note length checks: `examples/dataset/word_count_range_release_notes.jsonl` + matching outputs
- Multibyte-safe byte-budget coverage is part of the core contract: use `byte_count_range` when UI labels, commit titles, or Korean/Japanese outputs must stay within a strict UTF-8 byte ceiling.
- Produces:
  - terminal summary (including `outcome_counts` rollup and explicit `unchanged_pass` / `unchanged_fail` counters)
  - machine-readable JSON report (including `summary.regression_ids` / `summary.improved_ids`)
  - compact markdown summaries for PR comments/release notes, now including explicit regression/improvement case IDs with per-list counts when present, plus changed/filtered-out IDs and their rates for triage handoff
  - reviewer-friendly markdown snapshots that surface selected dataset IDs, active case IDs, scope reduction from filters, and a reviewer-queue total so shard-scoped reruns are easier to size without opening JSON, plus explicit active-case rate so shard coverage stays visible in pasted PR comments.
  - skipped-case handoff cues in markdown summaries, including skipped IDs, skipped-case rate, and skipped source-case rate, so disabled cases remain visible during shard/release review.
- Exits with non-zero status when regressions are detected (CI-friendly)

---

## Quickstart

### Smoke-check the documented summary artifacts

```bash
scripts/smoke_summary_outputs.sh
```

This smoke check reruns the committed pass/fail walkthrough fixtures, verifies the expected exit codes, and confirms that both markdown and JSON summaries still expose the reviewer-facing markers used in the docs.
It now also rechecks the PR-comment contract (`--summary-pr-comment`) for the same PASS/FAIL fixtures, including the custom reviewer-note headings used in the walkthrough artifacts.
If you need a copy-ready partial-PASS update for reviewers, start with `examples/reviewer_scope_status_lines.md` before widening the public summary.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# either CLI entrypoint
prm run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --report report.json

# or module execution
python -m prompt_regression_min run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --report report.json
```

For a copyable length-budget smoke test, see `examples/word_count_range_walkthrough.md`.
For a rendered-line budget variant, open `examples/line_count_range_walkthrough.md` to compare PASS/FAIL reviewer-note flows for `line_count_range` without introducing semantic scorers.
For short memo/release-summary structure checks, open `examples/paragraph_count_range_walkthrough.md` to keep paragraph budgets deterministic without introducing semantic scorers.
That walkthrough now also includes a PR-comment-ready FAIL summary snippet for reviewer notes and release-review threads.
For multilingual byte-budget checks, open `examples/byte_count_range_walkthrough.md` to keep UTF-8 storage and transport limits explicit before a copy change ships.
For sentence-budget reviewer notes, open `examples/sentence_count_range_walkthrough.md` to keep short summaries and approval comments within a deterministic sentence cap.
If you want a dedicated reviewer-note template, open `examples/word_count_pr_comment_playbook.md` for a generate -> paste -> rerun flow built around the committed word-count snapshots.
If you need to decide the first rerun lane from reviewer-queue metadata, open `examples/reviewer_queue_next_focus_playbook.md` for a compact `dominant focus -> next-focus -> tie-mode` triage flow.
If you need to justify the documented `P1 -> P2` queue order in one short reviewer note, open `examples/reviewer_queue_priority_rank_playbook.md`.
If `next_focus_tie_mode` is `tied`, open `examples/reviewer_queue_tie_playbook.md` for a deterministic “keep the first priority lane, but preserve the tie in the pasted note” workflow.
If you need the tied first lane and the likely second lane in one short note, open `examples/reviewer_queue_tie_and_runner_up_playbook.md` for a combined tie + runner-up handoff pattern.
If you want the first rerun lane plus the likely second lane in one reviewer handoff, open `examples/reviewer_queue_runner_up_playbook.md` for a compact `primary lane + runner-up lane` paste pattern.
If you need to justify why the dominant lane should go first, open `examples/reviewer_queue_advantage_playbook.md` for a compact `label + advantage summary` reviewer-note pattern.
If you need one short explanation of what kind of follow-up dominates the shard, open `examples/reviewer_queue_queue_mix_playbook.md` for a queue-share-driven reviewer note.
If you need a compact rule for `next_focus_advantage_direction` (`none` / `tied` / `solo` / `ahead`), open `examples/reviewer_queue_advantage_direction_guide.md`.
If you need the shortest human-facing repost pattern once that direction is already known, open `examples/reviewer_queue_advantage_direction_quickstart.md`.
If the run is clean and `reviewer_queue.total` is `0`, open `examples/reviewer_queue_zero_queue_playbook.md` for a short "nothing to route" handoff line instead of improvising reviewer-note wording.
If you need the shortest explanation of why one rerun lane should go first, open `examples/reviewer_queue_priority_alias_note.md` for a compact `follow_up_priority_summary` handoff pattern.
If you need the queue-mix rationale in one reviewer-ready sentence, open `examples/reviewer_queue_priority_mix_summary.md`.
If filtered-out cases, skipped cases, or unchanged-fail watchlists are muddying the handoff, open `examples/reviewer_queue_filter_playbook.md` before trusting the queue priority string.
If you need a one-line reviewer note that names the winner and the second lane together, open `examples/reviewer_queue_dual_lane_status_line.md`.
Reviewer-queue JSON and paste-ready summaries now also expose a structured runner-up lane (`runner_up_key`, `runner_up_priority_label`, `runner_up_summary`) so rerun handoffs can keep the second queue branch visible without reopening the full artifact.
They now also emit `next_focus_tie_summary`, a paste-ready `key=P# · label` line for tied first lanes, so PR comments can preserve deterministic rerun ordering without re-reading the full JSON artifact.
Committed reviewer-facing markdown output for the same fixture lives at `examples/artifacts/word-count-range.summary.md`, and the matching machine-readable gate payload now lives at `examples/artifacts/word-count-range.summary.json` for CI drift checks.
A ready-to-paste reviewer note snapshot now also lives at `examples/artifacts/word-count-range.pr-comment.md`, regenerated alongside the markdown/json walkthrough artifacts.
The walkthrough PASS fixture now also ships an approval-ready reviewer note snapshot at `examples/artifacts/walkthrough-pass.pr-comment.md`, and the matching FAIL fixture now ships a blocking note snapshot at `examples/artifacts/walkthrough-fail.pr-comment.md`, so teams can paste both approval and failure comment shapes from committed artifacts.
Those walkthrough PR-comment snapshots now use dedicated reviewer-facing titles (`walkthrough approval note` / `walkthrough blocker note`) so the committed comments read like paste-ready review outcomes without changing the markdown artifact headings.
Those PR-comment snapshots keep the same schema marker, explicit pass-rate trend, and deterministic stable/regression ids as the markdown/JSON artifacts, so reviewers can paste the note without reformatting CI output.
`./scripts/regenerate_walkthrough_artifacts.sh` now regenerates those PR-comment snapshots from the same CLI contract via `--summary-pr-comment`, so reviewer-note wording stays formatter-consistent with the committed markdown/JSON summaries.
Need to pipe the reviewer note directly into CI or a PR bot? `--summary-pr-comment -` now shares the same stdout ergonomics as `--summary-markdown -`, so workflows can render or post the ready-to-paste note without creating a temp file first. For a copy-paste CI example (including a shell capture that preserves a custom stdout title), open `examples/ci_pr_comment_stdout.md`.
Need a reviewer-note heading that differs from the markdown artifact title? Use `--summary-pr-comment-title` so PR-comment snapshots can say `review snapshot` or `release blocker note` without changing `--summary-markdown-title`. The committed word-count snapshots demonstrate this split directly: markdown keeps `word-count release-note gate`, while the PR-comment artifact uses `word-count blocker note` for paste-ready reviewer language. CI now also asserts the committed walkthrough PR-comment snapshots keep their custom headings (`walkthrough approval note` / `walkthrough blocker note`) so reviewer-note formatting cannot silently fall back to the default title.
Need the shortest example for pretty JSON handoff plus reviewer-facing markdown in the same run? Open `examples/ci_pretty_json_and_pr_comment.md`.
If you need the shortest example for keeping the saved markdown title stable while changing the pasted PR-comment title, open `examples/summary_pr_comment_title_split.md`.
If you need the same split with pretty JSON in the same run, open `examples/summary_json_and_pr_comment_handoff.md`.
Regex expectations also support the `VERBOSE` flag now, so multiline commented patterns can stay readable in committed datasets without losing deterministic matching.
PR-comment output now also carries `Filtered-out IDs` and `Skipped IDs` when filters or disabled cases shrink the active scope, so reviewers can see scope exclusions without opening the JSON artifact.
PR-comment output now also surfaces `Filtered-out rate` and `Skipped-case rate`, so reviewers can gauge how much scope moved out of the shard without opening the JSON artifact.
PR-comment output now also surfaces `Tool version` plus `Required schema version gate`, so paste-ready reviewer notes expose both the producing build and the expected summary contract without opening the JSON or markdown artifacts.
PR-comment output now also surfaces `Selection rate` and `Active-case rate`, making shard coverage and post-filter execution scope visible in paste-ready reviewer notes without opening the JSON or markdown artifacts.
PR-comment output now also surfaces reviewer-queue breakdown lines (`regressions`, `watchlist`, `filtered-out scope`, `skipped cases`) so reviewers can see what kind of follow-up work dominates a rerun without opening the JSON artifact.
PR-comment output now also surfaces `Reviewer queue dominant focus`, a copy-paste label for the largest follow-up bucket, so triage notes can immediately say whether the rerun is mostly regressions, watchlist carryover, filtered scope review, or skipped-case cleanup.
PR-comment and markdown summaries now also expose `Reviewer queue next-focus case count`, `Reviewer queue next-focus active-case rate`, `Reviewer queue next-focus source-case rate`, and `Reviewer queue next-focus priority rank`, so the first rerun bucket can be sized in absolute cases and placed inside the deterministic follow-up order without opening JSON.
PR-comment and markdown summaries now also expose `Reviewer queue runner-up` and `Reviewer queue runner-up case count`, so reviewers can see the second rerun lane without opening JSON when the lead bucket is tied or only narrowly ahead.
PR-comment and markdown summaries now also expose `Reviewer queue follow-up priority`, so reviewers can see the recommended bucket order (`fix_regressions -> watch_unchanged_fails -> confirm_filtered_scope -> resolve_skipped_cases`) without opening JSON.
The same ordering now ships as `reviewer_queue.follow_up_priority_summary` in JSON and as a dedicated markdown/PR-comment line, so bots and humans can paste one deterministic triage string without rebuilding the queue from arrays.
PR-comment and markdown summaries now also expose `Reviewer queue follow-up priority labels` (`P1 · fix regressions -> P2 · watch unchanged fails -> ...`), so pasted handoffs can preserve both queue order and reviewer-facing language without reconstructing labels from separate key/rank lines.
They now also expose `Reviewer queue group queue shares`, so reviewers can see how much of the queued follow-up load belongs to each bucket without opening JSON.
They now also expose `Reviewer queue group keys` and `Reviewer queue group labels`, so pasted summaries show the exact queue buckets already present in the current shard without reconstructing them from individual lines.
Those per-group reviewer-queue lines now also show source-case rate, so shard-heavy reruns can distinguish active-case dominance from full-dataset impact at a glance.
PR-comment snapshots now also surface `Reviewer queue tied largest labels`, so tie-heavy reruns spell out the human-readable queue buckets directly when regressions and watchlist/filtered/skipped work land in the same-sized bucket.
Markdown/PR-comment summaries now also surface `Reviewer queue next-focus tie mode` (`unique` vs `tied`), so reviewer notes can tell whether the current next-focus bucket is an unambiguous first action or one of several equally large rerun lanes.
The JSON `summary.reviewer_queue` payload now mirrors that same handoff via explicit `next_focus_key`, `next_focus_label`, `next_focus_priority_rank`, `next_focus_ids`, `next_focus_case_count`, `next_focus_queue_share`, and `next_focus_tie_mode` aliases, so bots can route, rank, and size the first rerun lane without reverse-engineering the larger queue object.
It now also exposes `next_focus_tie_keys`, `next_focus_tie_labels`, `next_focus_tie_count`, and `next_focus_has_ties`, so bots can preserve every same-sized first rerun lane instead of keeping only the priority winner.
The reviewer-queue JSON now also exposes `next_focus_advantage_summary`, a paste-ready sentence that explains how far ahead the current first rerun lane sits versus the runner-up in cases, queue share, active-case rate, and source-case rate.
It now also emits compact `next_focus_handoff_summary` / `runner_up_handoff_summary` strings that combine priority label, IDs, and rate/share context into a single paste-ready reviewer handoff line.
That payload now also includes a nested `next_focus_group` object (`key`, `label`, `priority_label`, `priority_rank`, `ids`, `case_count`, `active_case_rate`, `source_case_rate`, `queue_share`, `tie_mode`) so bots can consume the first rerun lane as a single structured handoff instead of stitching alias fields together.
That payload now also includes `next_focus_advantage_direction` (`none` | `tied` | `solo` | `ahead`) and mirrors it under `next_focus_group.advantage_direction`, so bots can branch on tie-vs-lead state without parsing the prose summary.
Markdown/PR-comment summaries now also expose `Reviewer queue next-focus key`, so human reviewers and paste-driven bots can lift the deterministic rerun lane name directly without parsing the longer `Reviewer queue next focus` sentence.
The largest reviewer-queue group line now also shows its share of queued follow-up, so reviewers can tell whether one class of action dominates the entire rerun plan.
Markdown/PR-comment summaries now also expose `Reviewer queue source-case rate`, so shard-heavy reruns can distinguish active-case overload from total dataset impact without opening JSON.
Markdown summaries now also expose `Reviewer queue next focus`, `Reviewer queue next-focus active-case rate`, and `Reviewer queue next-focus source-case rate`, so markdown artifacts match PR-comment rerun guidance when reviewers need the first follow-up IDs without opening JSON.
The `Reviewer queue largest group` line now also shows both active-case rate and source-case rate, so the dominant rerun bucket is easy to size against the current shard and the full dataset without opening JSON.

`--summary-json` also emits `largest_group_label`, a human-ready copy of the dominant follow-up bucket name (`fix regressions`, `watch unchanged fails`, `confirm filtered-out scope`, `resolve skipped cases`). That means bots and PR templates can paste a readable next-step label without re-mapping internal queue keys.
`reviewer_queue.group_counts_by_key` and `reviewer_queue.group_ids_by_key` now expose per-bucket counts plus exact case IDs in stable maps, so bots can route regressions/watchlists/filtered scope/skipped cleanup without walking the ordered `groups` array first.
`reviewer_queue.groups_by_key` now also exposes each queue bucket as a keyed object (`label`, `ids`, `count`, `active_case_rate`, `source_case_rate`, `queue_share`, `priority_rank`, `priority_label`), so bots can consume one stable map instead of stitching multiple per-key summaries together.
`reviewer_queue.largest_group` now mirrors the dominant queue bucket as one structured object (`key`, `label`, `priority_label`, `ids`, rates, queue share, tie metadata), so bots can lift the main rerun lane without combining separate `largest_group_*` aliases.
PR-comment output now also surfaces `Regression rate` and `Improvement rate`, so reviewers can gauge how concentrated the changed outcomes are without opening the JSON artifact.
Markdown/PR-comment summaries now also expose `Regression source-case rate`, `Improvement source-case rate`, `Changed source-case rate`, and `Watchlist source-case rate`, so reviewers can tell whether regressions/watchlists are shard-local or source-dataset-wide without opening JSON.
PR-comment output now also carries `Unchanged fail IDs` plus a watchlist rate, so reviewers can separate known-bad carryover cases from newly regressed IDs without opening the JSON artifact.
PR-comment snapshots now also include `Changed IDs` plus the changed-case rate, so reviewers can tell whether a failure is concentrated in one case or spread across the active shard without opening the full markdown/JSON summary.
Refresh all committed walkthrough snapshots (including the word-count markdown/JSON pair) with `./scripts/regenerate_walkthrough_artifacts.sh` before updating docs that cite those artifacts.
The CI workflow also re-checks that the committed word-count markdown snapshot keeps both the schema marker and the documented regression IDs (`release-note-bullets`, `release-note-short`) so reviewer-facing release-note examples do not drift silently.
For practical threshold combinations you can copy into CI, see `examples/gate_policy_recipes.md`.
For a focused pass-rate + trend + stable-core gating recipe, see `examples/pass_rate_gate_walkthrough.md`.
For a trend-label-specific reviewer handoff recipe, see `examples/pass_rate_trend_gate_walkthrough.md`.
For a compact expectation-picking rubric when writing new dataset cases, see `examples/expectation_selection_guide.md`.
For compact regex authoring with short flag aliases, see `examples/regex_flag_aliases.md`.
For shard-focused reviewer workflows that must make filtered-out scope obvious, see `examples/shard_filter_walkthrough.md`.
For dual-output reviewer/CI handoffs that combine summary JSON with markdown, see `examples/summary_json_handoff.md`.
For reviewer-queue triage notes that explain filtered scope, stable watchlists, and rerun load in one place, see `examples/reviewer_queue_triage.md`.
For a copy-paste PR comment workflow that keeps reviewer notes stable across reruns, see `examples/pr_comment_handoff_playbook.md`.

---

## Core Concepts

- **Dataset**: test cases with expectations
- **Baseline output**: currently accepted behavior
- **Candidate output**: new behavior after a change
- **Regression**: baseline passes, candidate fails
- **Improvement**: baseline fails, candidate passes

This framing keeps release discussions objective and diff-driven.

---

## Data Format

### Dataset JSONL

Each line:

```json
{
  "id": "case-1",
  "input": "How do I reset my password?",
  "expected": {
    "type": "contains_all",
    "values": ["reset", "email"]
  }
}
```

Supported `expected.type` values:

- `exact` (`value` must be a string; leading/trailing whitespace is ignored on both expected and output):
  ```json
  { "type": "exact", "value": "..." }
  ```
- `exact_ci` (case-insensitive variant of `exact`; still trims surrounding whitespace):
  ```json
  { "type": "exact_ci", "value": "approved" }
  ```
- `line_count_range` (useful for enforcing compact bullets or multi-line templates):
  ```json
  { "type": "line_count_range", "min_lines": 2, "max_lines": 4 }
  ```
- `sentence_count_range` (useful when reviewer notes, summaries, or support replies must stay within a predictable sentence budget):
  ```json
  { "type": "sentence_count_range", "min_sentences": 2, "max_sentences": 4 }
  ```
  You can set `min_sentences`, `max_sentences`, or both.
- `char_count_range` (useful when UI labels, commit titles, or release-note blurbs must stay within a strict character budget):
  ```json
  { "type": "char_count_range", "max_chars": 72 }
  ```
  You can set `min_chars`, `max_chars`, or both.
- `byte_count_range` (useful when downstream systems enforce UTF-8 byte budgets and multibyte Korean/Japanese text must stay within a hard limit):
  ```json
  { "type": "byte_count_range", "max_bytes": 96 }
  ```
  You can set `min_bytes`, `max_bytes`, or both.
- `not_exact` (`value` must be a string; passes only when normalized output differs):
  ```json
  { "type": "not_exact", "value": "Forbidden" }
  ```
- `not_exact_ci` (case-insensitive variant of `not_exact`; still trims surrounding whitespace):
  ```json
  { "type": "not_exact_ci", "value": "forbidden" }
  ```
- `substring` (`value` must be a non-empty string):
  ```json
  { "type": "substring", "value": "..." }
  ```
- `substring_ci` (case-insensitive variant of `substring`):
  ```json
  { "type": "substring_ci", "value": "error code" }
  ```
- `not_substring` (fails if the output includes the forbidden token):
  ```json
  { "type": "not_substring", "value": "secret" }
  ```
- `not_substring_ci` (case-insensitive variant of `not_substring`):
  ```json
  { "type": "not_substring_ci", "value": "secret" }
  ```
- `word_count_range` (uses whitespace-delimited word counts; set `min_words`, `max_words`, or both):
  ```json
  { "type": "word_count_range", "min_words": 20, "max_words": 60 }
  ```
- `contains_all` (requires a non-empty `values` list of non-empty strings):
  ```json
  { "type": "contains_all", "values": ["a", "b"] }
  ```
- `contains_all_ci` (case-insensitive variant of `contains_all`):
  ```json
  { "type": "contains_all_ci", "values": ["order", "resolved"] }
  ```
- `starts_with` (`value` must be a non-empty string prefix):
  ```json
  { "type": "starts_with", "value": "Order #" }
  ```
- `starts_with_ci` (case-insensitive variant of `starts_with`; `value` must be a non-empty string prefix):
  ```json
  { "type": "starts_with_ci", "value": "order #" }
  ```
- `not_starts_with` (`value` must be a non-empty string prefix that must not appear at output start):
  ```json
  { "type": "not_starts_with", "value": "Error:" }
  ```
- `not_starts_with_ci` (case-insensitive variant of `not_starts_with`):
  ```json
  { "type": "not_starts_with_ci", "value": "error:" }
  ```
- `ends_with` (`value` must be a non-empty string suffix):
  ```json
  { "type": "ends_with", "value": "resolved" }
  ```
- `ends_with_ci` (case-insensitive variant of `ends_with`; `value` must be a non-empty string suffix):
  ```json
  { "type": "ends_with_ci", "value": "resolved" }
  ```
- `not_ends_with` (`value` must be a non-empty string suffix that must not appear at output end):
  ```json
  { "type": "not_ends_with", "value": "debug" }
  ```
- `not_ends_with_ci` (case-insensitive variant of `not_ends_with`):
  ```json
  { "type": "not_ends_with_ci", "value": "debug" }
  ```
- `contains_any` (candidate output must include at least one value from a non-empty `values` list):
  ```json
  { "type": "contains_any", "values": ["reset", "password"] }
  ```
- `contains_any_ci` (case-insensitive variant of `contains_any`):
  ```json
  { "type": "contains_any_ci", "values": ["approved", "pending"] }
  ```
- `equals_any` (normalized output must exactly match one candidate in a non-empty `values` list):
  ```json
  { "type": "equals_any", "values": ["Approved", "Pending"] }
  ```
- `equals_any_ci` (case-insensitive variant of `equals_any`):
  ```json
  { "type": "equals_any_ci", "values": ["approved", "pending"] }
  ```
- `not_contains` (candidate output must not include any value from a non-empty `values` list):
  ```json
  { "type": "not_contains", "values": ["SSN", "credit card"] }
  ```
- `not_contains_ci` (case-insensitive variant of `not_contains`):
  ```json
  { "type": "not_contains_ci", "values": ["ssn", "credit card"] }
  ```
- `contains_none` (readability alias of `not_contains`):
  ```json
  { "type": "contains_none", "values": ["SSN", "credit card"] }
  ```
- `contains_none_ci` (readability alias of `not_contains_ci`):
  ```json
  { "type": "contains_none_ci", "values": ["ssn", "credit card"] }
  ```
- `regex` (requires non-empty `pattern`; optional `flags` list or single-string `flag` alias):
  ```json
  { "type": "regex", "pattern": "order\\s+#?\\d{4}", "flags": ["IGNORECASE"] }
  ```
  ```json
  { "type": "regex", "pattern": "^approved$", "flag": "IGNORECASE" }
  ```
- `regex_fullmatch` (same as `regex` but requires full-string match):
  ```json
  { "type": "regex_fullmatch", "pattern": "Order #[0-9]{4}" }
  ```
- `not_regex` (same as `regex` but requires the pattern to *not* appear in output):
  ```json
  { "type": "not_regex", "pattern": "\\b(SSN|credit card)\\b", "flags": ["IGNORECASE"] }
  ```
- `not_regex_fullmatch` (same as `regex_fullmatch` but requires full-string *non-match*):
  ```json
  { "type": "not_regex_fullmatch", "pattern": "(Approved|Pending)" }
  ```

### Output JSONL

Each line:

```json
{
  "id": "case-1",
  "output": "Use the reset link and check your email inbox."
}
```

Both baseline and candidate output files must contain the same IDs used in the dataset.

IDs must be non-empty, non-whitespace strings across dataset/baseline/candidate rows.

Dataset files must be non-empty (at least one valid JSONL case).

Optional dataset field:
- `disabled` (boolean): if `true`, the case is skipped from scoring but still validated for ID alignment.

At least one case must remain active after applying `disabled: true` filters.

When `--report` is used, each case includes an `outcome` field:
- `regressed`
- `improved`
- `unchanged_pass`
- `unchanged_fail`

The report summary includes `outcome_counts` for quick CI diagnostics, plus `changed` / `changed_rate` to track blast radius.

---

## CLI Reference

```bash
prm run \
  --dataset <dataset.jsonl> \
  --baseline <baseline.jsonl> \
  --candidate <candidate.jsonl> \
  [--report report.json] \
  [--max-regressions 0] \
  [--max-regression-rate <float>] \
  [--min-candidate-pass-rate 0.0] \
  [--max-unchanged-fail -1] \
  [--max-unchanged-fail-rate <float>] \
  [--forbid-unchanged-fail-id-regex <regex>] \
  [--max-skipped-cases -1] \
  [--min-delta-pass-rate-pp <float>] \
  [--max-delta-pass-rate-pp <float>] \
  [--min-improved 0] \
  [--max-improved -1] \
  [--max-improved-rate 1.0] \
  [--max-changed-cases -1] \
  [--max-changed-rate <float>] \
  [--min-active-cases 1] \
  [--max-filtered-out-cases -1] \
  [--max-filtered-out-rate <float>] \
  [--min-unchanged-pass 0] \
  [--max-unchanged-pass -1] \
  [--min-stability-rate <float>] \
  [--require-pass-rate-trend <improving|flat|regressing>] \
  [--include-id-regex <regex>] \
  [--exclude-id-regex <regex>] \
  [--summary-json [path|-]] \
  [--summary-json-pretty] \
  [--summary-markdown path] \
  [--quiet]

# short aliases: -d, -b, -c, -r
```

Use `--include-id-regex` / `--exclude-id-regex` to run deterministic subsets (e.g., shard by feature area) without editing the source dataset.

### Exit codes

- `0`: quality gate passed (`regressions <= max-regressions`, regression rate meets `--max-regression-rate` when enabled, candidate pass rate meets threshold, unchanged fails are within `--max-unchanged-fail` and `--max-unchanged-fail-rate` when enabled, critical unchanged failing ids do not match `--forbid-unchanged-fail-id-regex` when enabled, skipped cases are within `max-skipped-cases` when enabled, pass-rate delta stays within `--min-delta-pass-rate-pp` / `--max-delta-pass-rate-pp` when enabled, improved cases meet `--min-improved` / `--max-improved` / `--max-improved-rate` when enabled, changed-case budget/rate meet `--max-changed-cases` / `--max-changed-rate` when enabled, active cases meet `--min-active-cases`, filtered-out case budget/rate meet `--max-filtered-out-cases` / `--max-filtered-out-rate` when enabled, unchanged passing cases stay within `--min-unchanged-pass` / `--max-unchanged-pass` gates, stability rate meets `--min-stability-rate` when enabled, and pass-rate trend matches `--require-pass-rate-trend` when enabled)
- `1`: quality gate failed
- `>1`: invalid input / runtime error

Terminal summary now includes `pass_rate_trend` (`improving` | `flat` | `regressing`) for quick directional triage.

### Mixed expectation fixture (CI smoke)

Use the fixture pack to smoke-test `equals_any` + `regex_fullmatch` together:

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/mixed_expectations.jsonl \
  -b examples/outputs/mixed_expectations.baseline.jsonl \
  -c examples/outputs/mixed_expectations.candidate.jsonl \
  --max-regressions 0 \
  --summary-json
```

### FAIL payload fixture (CI audit smoke)

Use this fixture to verify that `fail_reasons` and `gates` are emitted together in FAIL mode:

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/fail_payload_gate_demo.jsonl \
  -b examples/outputs/fail_payload_gate_demo.baseline.jsonl \
  -c examples/outputs/fail_payload_gate_demo.candidate.jsonl \
  --max-unchanged-fail 0 \
  --summary-json
```

Expected: exit code `1`, JSON payload `status=FAIL`, non-empty `fail_reasons`, and `gates.max_unchanged_fail=0`.

### Unchanged-pass band fixture (CI policy smoke)

Use this fixture to enforce a bounded unchanged-pass policy (minimum and maximum both fixed to `3`):

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/unchanged_pass_band_demo.jsonl \
  -b examples/outputs/unchanged_pass_band_demo.baseline.jsonl \
  -c examples/outputs/unchanged_pass_band_demo.candidate.jsonl \
  --min-unchanged-pass 3 \
  --max-unchanged-pass 3 \
  --summary-json
```

Expected: exit code `0`, JSON payload `status=PASS`, `summary.unchanged_pass=3`, and gate echo values `gates.min_unchanged_pass=3` + `gates.max_unchanged_pass=3`.

### Improved-band fixture (CI policy smoke)

Use this fixture to enforce an exact improved-case budget (`min=max=1`) while still banning regressions:

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/improved_band_demo.jsonl \
  -b examples/outputs/improved_band_demo.baseline.jsonl \
  -c examples/outputs/improved_band_demo.candidate.jsonl \
  --max-regressions 0 \
  --min-improved 1 \
  --max-improved 1 \
  --summary-json
```

Expected: exit code `0`, JSON payload `status=PASS`, `summary.improved=1`, and gate echo values `gates.min_improved=1` + `gates.max_improved=1`.

### Filtered-out band fixture (CI shard-policy smoke)

Use this fixture to enforce a bounded filtered-out shard policy while selecting `auth-*` case IDs:

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/filtered_out_band_demo.jsonl \
  -b examples/outputs/filtered_out_band_demo.baseline.jsonl \
  -c examples/outputs/filtered_out_band_demo.candidate.jsonl \
  --include-id-regex '^auth-' \
  --max-filtered-out-cases 2 \
  --max-filtered-out-rate 0.5 \
  --summary-json
```

Expected: exit code `0`, JSON payload `status=PASS`, `summary.filtered_out_cases=2`, `summary.filtered_out_rate=0.5`, and gate echo values `gates.max_filtered_out_cases=2` + `gates.max_filtered_out_rate=0.5`.

### Trend + stability fixture (CI release-shape smoke)

Use this fixture when you want a deterministic policy that allows one regression only if one improvement offsets it and the overall pass-rate trend stays flat with at least 50% stability:

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/trend_stability_demo.jsonl \
  -b examples/outputs/trend_stability_demo.baseline.jsonl \
  -c examples/outputs/trend_stability_demo.candidate.jsonl \
  --max-regressions 1 \
  --min-stability-rate 0.5 \
  --require-pass-rate-trend flat \
  --summary-json
```

Expected: exit code `0`, JSON payload `status=PASS`, `summary.pass_rate_trend="flat"`, `summary.stability_rate=0.5`, plus one regression id and one improvement id for balanced rollout triage.

### Machine-readable summary

Use `--summary-json` for CI parsers:

- `--summary-json` (no value): print compact JSON payload to stdout
- `--summary-json artifacts/summary.json`: write JSON payload to file
- `--summary-json-pretty`: pretty-print summary JSON (`indent=2`) for stdout/file outputs
- Combined CI example: `examples/ci_pretty_json_and_pr_comment.md`
- Compact vs pretty parity check: `examples/summary_json_pretty_diff_check.md`
- `--summary-markdown artifacts/summary.md`: write a compact markdown summary for PR comments/release notes
  - Markdown summaries now echo `Tool version` plus `Required schema version gate` so reviewers can see both the producing build and whether the artifact was generated under an explicit compatibility contract or free-run mode.
  - Markdown summaries also include filtered/skipped/unchanged-fail case IDs when present, making shard drift and lingering broken flows reviewable without opening the JSON payload first.
  - Gate snapshots in markdown now echo delta-pass-rate, changed-case, filtered-out, active-case, unchanged-pass, improvement budgets/rates, and the required summary schema gate too, so PR reviewers can verify rollout/shard constraints plus JSON-contract expectations without opening JSON.
  - Markdown summaries also show dataset scope (`source`, `selected`, `active`) so reviewers can spot regex-filter shrinkage before comparing pass/fail outcomes.
- Summary JSON now also includes `selected_dataset_ids`, `active_case_ids`, and `selection_rate`, making shard/debug handoffs deterministic when CI runs only a subset of the dataset.
- `--summary-markdown -`: print the markdown summary to stdout so CI jobs can pipe it straight into PR-comment or release-note helpers without creating a temporary file first.
- `--quiet`: suppress all human-readable summary lines (including baseline/candidate/delta and outcome rollups) so CI logs can keep only JSON/artifact paths
- In CI, persist `.tmp/` summary artifacts (JSON + Markdown) with `actions/upload-artifact` so failed gates stay reviewable after the job exits.

Compact vs pretty smoke commands:

```bash
# compact JSON (single-line payload)
python3 -m prompt_regression_min run \
  -d examples/dataset/mixed_expectations.jsonl \
  -b examples/outputs/mixed_expectations.baseline.jsonl \
  -c examples/outputs/mixed_expectations.candidate.jsonl \
  --summary-json --quiet

# pretty JSON artifact (human diff-friendly)
python3 -m prompt_regression_min run \
  -d examples/dataset/mixed_expectations.jsonl \
  -b examples/outputs/mixed_expectations.baseline.jsonl \
  -c examples/outputs/mixed_expectations.candidate.jsonl \
  --summary-json artifacts/summary.pretty.json --summary-json-pretty
```

CI parity smoke (serializer drift guard):

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/mixed_expectations.jsonl \
  -b examples/outputs/mixed_expectations.baseline.jsonl \
  -c examples/outputs/mixed_expectations.candidate.jsonl \
  --summary-json .tmp/summary.compact.json --quiet

python3 -m prompt_regression_min run \
  -d examples/dataset/mixed_expectations.jsonl \
  -b examples/outputs/mixed_expectations.baseline.jsonl \
  -c examples/outputs/mixed_expectations.candidate.jsonl \
  --summary-json .tmp/summary.pretty.json --summary-json-pretty --quiet

python3 - <<'PY'
import json
from pathlib import Path

compact = json.loads(Path('.tmp/summary.compact.json').read_text(encoding='utf-8'))
pretty = json.loads(Path('.tmp/summary.pretty.json').read_text(encoding='utf-8'))
assert compact == pretty, 'compact/pretty summary payload mismatch'
PY
```

Payload shape:

```json
{
  "status": "PASS|FAIL",
  "fail_reasons": ["..."],
  "summary": {"selection_rate": 1.0, "...": "..."},
  "gates": {
    "max_regressions": 0,
    "max_regression_rate": null,
    "min_candidate_pass_rate": 0.0,
    "max_unchanged_fail": -1,
    "max_skipped_cases": -1,
    "min_delta_pass_rate_pp": null,
    "min_improved": 0,
    "max_changed_cases": -1,
    "max_changed_rate": null,
    "min_active_cases": 1,
    "max_filtered_out_cases": -1,
    "max_filtered_out_rate": null,
    "min_unchanged_pass": 0,
    "max_unchanged_pass": -1
  }
}
```

### Local test command

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py" -v
```

---

## Example Output

```text
prompt-regression-min summary
- cases: 3
- baseline: 3 (100.0%)
- candidate: 2 (66.7%)
- delta: -1 (-33.33pp)
- regressions: 1
- improved: 0
- unchanged: 2
- report: report.json
```

---

## PR Comment Tips

Use `--summary-markdown-title` when the generated markdown needs a repo- or workflow-specific heading.

```bash
prm run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --summary-markdown - \
  --summary-markdown-title "checkout release gate" \
  --quiet
```

This keeps the body deterministic while making pasted PR comments easier to scan.
The same title override is preserved when `--summary-markdown <path>` writes a file, so CI artifacts and pasted PR comments can keep the same workflow-specific heading. Markdown summaries now also list `Unchanged pass IDs` when available, which makes reviewer handoff easier because the stable controls remain visible next to regressions and improvements.

---

## JSONL Case Hygiene

When you add or review evaluation cases, use `examples/jsonl_case_hygiene.md` to keep ids stable, expectations deterministic, and failure diffs easy to debug.

## CI/CD Integration

### CI artifact review walkthrough

If your workflow uploads `.tmp/` summary artifacts, use [`examples/ci_artifact_walkthrough.md`](examples/ci_artifact_walkthrough.md) as the reviewer playbook.
It shows what PASS vs FAIL summary JSON/Markdown artifacts look like and how to triage them quickly in pull requests.
The walkthrough now points at copyable fixture pairs (`walkthrough_pass_artifact_demo.*`, `walkthrough_fail_artifact_demo.*`) so reviewers can regenerate the documented artifacts exactly.

It also ships stable snapshot filenames under `examples/artifacts/` so docs can reference concrete PASS/FAIL artifact paths without depending on CI-only `.tmp/` names.
Both committed markdown snapshots retain `Summary schema version: 1` so reviewer-facing artifacts expose the same contract marker as JSON outputs.
The drift checker also verifies expected markdown headings (including custom review titles like `## word-count release-note gate`) so docs-ready artifacts do not silently fall back to the default summary heading.

Regenerate those committed walkthrough snapshots with one command:

```bash
./scripts/regenerate_walkthrough_artifacts.sh

# downstream parser compatibility gate
PYTHONPATH=src python3 -m prompt_regression_min run \
  -d examples/dataset/walkthrough_pass_artifact_demo.jsonl \
  -b examples/outputs/walkthrough_pass_artifact_demo.baseline.jsonl \
  -c examples/outputs/walkthrough_pass_artifact_demo.candidate.jsonl \
  --summary-json .tmp/walkthrough-pass.json \
  --require-summary-schema-version 1 \
  --quiet
```

Summary JSON now includes explicit parser metadata:

- `summary_schema_version`: stable schema marker for downstream CI parsers
- generated summary markdown now includes the same schema marker for human review parity plus the producing tool version
- summary markdown now also surfaces unchanged-fail budget usage so reviewers can spot watchlist pressure beside regression/changed-case budgets
- `tool_version`: package version that produced the JSON artifact
- `selection_rate`: selected/source dataset ratio for shard-size visibility in CI handoffs

Use the generated report and fail deployment when regressions exceed your tolerance.

Example policy:

- block merge if `summary.regressions > 0`
- allow merge if regressions are zero and candidate pass rate is above threshold

This lets teams move fast while preserving quality guarantees.

---

## Development Direction

The project will be developed continuously with an MVP-first approach.

### Phase 1 (current)

- Deterministic baseline/candidate comparison
- Minimal scorer set
- CI-friendly behavior

### Phase 2

- Weighted case scoring
- Better case-level diff output
- Optional threshold flags (e.g., max allowed regressions)

### Phase 3

- Semantic similarity scorer (configurable)
- HTML report for team review
- GitHub Action wrapper for easy adoption

### Phase 4

- Domain packs (support, compliance, coding-assistant, etc.)
- Plugin interface for custom scorers
- Longitudinal quality trends across releases

---

## Quality and Contribution Guidelines

Contributions are welcome.

When proposing changes:

1. Keep behavior deterministic unless explicitly labeled experimental.
2. Add or update example cases for new scoring behavior.
3. Prefer readability over clever abstractions.
4. Document tradeoffs in PR descriptions.

Suggested commit style:

- `feat:` new capability
- `fix:` bug or correctness issue
- `docs:` documentation
- `refactor:` non-functional code changes

---

## FAQ

### Why not use semantic scoring only?

Semantic scoring is useful, but deterministic checks are easier to trust and debug.
`prompt-regression-min` starts with strict checks and can layer semantics later.

### Is this a benchmark framework?

Not exactly. It is a practical regression guard for day-to-day shipping.

### Can I use this for agents, not just prompts?

Yes. Any workflow producing text outputs can be compared via baseline/candidate files.

---

### Summary schema compatibility gate

Use `--require-summary-schema-version <n>` when downstream CI or PR bots depend on a fixed summary contract.

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/walkthrough_pass_artifact_demo.jsonl \
  -b examples/outputs/walkthrough_pass_artifact_demo.baseline.jsonl \
  -c examples/outputs/walkthrough_pass_artifact_demo.candidate.jsonl \
  --summary-json - \
  --require-summary-schema-version 1 \
  --quiet
```

This fails fast if the emitted `summary_schema_version` drifts from the parser expectation, which makes CI handoff breakage visible before a bot posts stale review output.

## Reviewer-oriented shard workflow

When a PR only touches one feature area, prefer a shard run that still makes skipped scope explicit.

1. Start from `examples/shard_filter_walkthrough.md`.
2. Keep `selected_dataset_ids`, `filtered_out_ids`, and `selection_rate` visible in the emitted summary.
3. Treat filtered-out budgets as a release gate, not just an informational metric.
4. Use a markdown or PR-comment summary so reviewers do not need raw JSON to see scope loss.

If you need a copy-ready one-liner for that public handoff, use `examples/reviewer_queue_scope_status_examples.md`.
If you want a compact note that separates filtered-out scope from skipped-case rerun debt in the same reviewer update, open `examples/reviewer_queue_scope_vs_skip_note.md`.
If you want a shorter filtered-scope budget reminder for the same reviewer handoff, open `examples/reviewer_queue_filtered_scope_budget_note.md`.

This keeps shard runs deterministic while preserving reviewer trust in what was, and was not, exercised.

## License

MIT


## Structured reviewer queue in summary JSON

`--summary-json` now emits a `reviewer_queue` object for downstream automation and PR bots, including top-level `rate` and `source_case_rate` plus per-group `rate`, `source_case_rate`, and `queue_share` values alongside `group_count`, `largest_group_key`, and `largest_group_count` so triage dashboards can spot both the dominant follow-up bucket and how much of the active/source dataset follow-up load it owns without recomputing it. It also publishes stable per-key maps (`group_labels_by_key`, `group_rates_by_key`, `group_source_case_rates_by_key`, `group_queue_shares_by_key`) for bots that want direct key lookups without walking the ordered `groups` array first. `follow_up_priority` stays a deterministic queue-order list sorted by follow-up size first and the built-in reviewer urgency order second (`fix_regressions` → `watch_unchanged_fails` → `confirm_filtered_scope` → `resolve_skipped_cases`).
It groups case IDs into four follow-up buckets:

- `fix_regressions`
- `watch_unchanged_fails`
- `confirm_filtered_scope`
- `resolve_skipped_cases`

This keeps markdown/PR-comment handoffs and machine-readable JSON aligned.


## Report bundle shortcut

If reviewers need both human and machine outputs from the same run, start with `examples/reviewer_queue_report_dir_walkthrough.md` and `examples/summary_json_handoff.md` so the markdown/PR-comment handoff and the JSON contract stay generated from one deterministic command.
If you need the shortest reopen path for that same reviewer bundle, open `examples/reviewer_queue_report_bundle_quickstart.md`.
If you need an even smaller report-dir reopen cue for the same shared bundle, open `examples/reviewer_queue_report_dir_reopen.md`.
If you need a compact naming note for keeping JSON plus markdown/PR-comment artifacts under one shared rerun bundle, open `examples/reviewer_queue_report_bundle_alias_note.md`.
If you need a tiny stdin-first reminder for keeping JSON, markdown, and PR-comment outputs under one shared basename, open `examples/summary_stdin_bundle_note.md`.


If you need a compact note for keeping CLI JSON baselines reviewable in docs and CI together, open `docs/CLI_JSON_BASELINE_NOTE.md`.
If you need the quickest stdout-first handoff for JSON or markdown summaries, open `docs/CLI_SUMMARY_STDOUT_NOTE.md`.
If you need that stdout-first summary to keep a stable human-readable heading in CI or pasted handoffs, open `docs/CLI_SUMMARY_STDOUT_TITLE_NOTE.md`.
If you need the same stdout-first pattern for reviewer-note markdown, open `docs/CLI_SUMMARY_PR_COMMENT_STDOUT_NOTE.md`.
If you need a compact rule for keeping parser-facing summary automation tied to an explicit schema gate, open `docs/CLI_SUMMARY_SCHEMA_GATE_NOTE.md`.
If you need a compact reminder to pair `--quiet` stdout handoffs with the same summary-schema expectation, open `docs/CLI_SUMMARY_QUIET_SCHEMA_NOTE.md`.
If you need a compact reminder to review the JSON summary artifact next to the markdown handoff, open `docs/CLI_SUMMARY_ARTIFACT_NOTE.md`.
If you need a quick note for keeping reviewer-queue source-case rate visible beside active-case rate in CLI summaries, open `docs/CLI_REVIEWER_QUEUE_SOURCE_CASE_RATE_NOTE.md`.
If you need a one-line reviewer handoff pattern that keeps next-focus scope tied to source-case impact, open `examples/reviewer_queue_source_case_scope_note.md`.
If you need a compact rule for keeping stdout-first summaries tied to one explicit owner line, open `docs/CLI_SUMMARY_STDOUT_OWNER_NOTE.md`.
If you need a one-line reviewer update once the winner and shared bundle are already known, open `examples/reviewer_queue_priority_rank_ready_post.md`.
If you need the same handoff phrased as a bundle-first ready-to-post cue, open `examples/reviewer_queue_priority_rank_bundle_ready_post.md`.

If you need a short reviewer note for queue-share-first tie resolution, open `examples/reviewer_queue_queue_share_tiebreak_note.md`.

If you need a compact handoff that keeps the active reviewer queue explicitly paired with the shared report bundle scope, open `examples/reviewer_queue_report_bundle_scope_handoff.md`.

If you need a compact bot-facing note for the reviewer-queue per-group maps in `summary.json`, open `examples/reviewer_queue_priority_rank_group_map.md`.
If you need a compact note for shard-safe CI handoffs that must reopen `--summary-json` and `--summary-markdown` together, open `docs/CLI_SUMMARY_JSON_MARKDOWN_PAIR_NOTE.md`.


If you need a compact note for preserving `report_author` / `report_authors` ownership fields inside reviewer-queue bundles, open `examples/reviewer_queue_report_owner_alias_note.md`.


If you need a compact reviewer note for one owner-routable next-focus summary after `--summary-pr-comment`, open `examples/reviewer_queue_priority_rank_owner_summary.md`.

If you want a compact source-provenance reminder before handing off a generated scenario report bundle, open `examples/reviewer_queue_pass_rate_trend_owner_handoff.md`.
If you need a compact title check before posting one saved reviewer queue bundle, open `examples/reviewer_queue_report_bundle_title_gate.md`.
If you need a shorter reminder to keep reviewer handoff copy pinned to the top priority lane first, open `docs/CLI_REVIEWER_QUEUE_PRIORITY_LANE_NOTE.md`.
If you need a short contract note for keeping JSON, markdown, and HTML summary artifacts aligned in one handoff, open `docs/CLI_SUMMARY_JSON_MARKDOWN_HTML_NOTE.md`.
If you want a tiny reviewer-ready stdout example with an explicit owner handoff, open `examples/summary_stdout_owner_handoff.md`.

If you need the shortest reminder for keeping queue share visible in the reviewer follow-up lane, open `docs/CLI_REVIEWER_QUEUE_QUEUE_SHARE_STATUS_NOTE.md`.

If you need a compact status cue that names the shared JSON/Markdown/HTML artifact trio in one reviewer-facing line, open `docs/CLI_SUMMARY_REPORT_ARTIFACT_TRIO_NOTE.md`.

If you need a compact note for reopening one saved summary bundle with the same subject, owner, and status line, open `docs/CLI_SUMMARY_REPORT_REOPEN_CARD.md`.

If you need a faster gate for deciding whether one summary JSON/Markdown/HTML trio is actually handoff-ready, open `docs/CLI_SUMMARY_REPORT_ARTIFACT_READY_NOTE.md`.
