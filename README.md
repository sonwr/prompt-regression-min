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

---

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
  - `regex` (with optional `IGNORECASE`, `MULTILINE`, `DOTALL`, `VERBOSE` flags; `expected.flags` accepts either a list or a comma/pipe/whitespace-delimited string, `expected.flag` works as a single-flag alias, and case/whitespace-insensitive tokens like `" ignorecase "` are normalized)
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
  - `sentence_count_range` (enforces lower/upper output-length bounds using punctuation-delimited sentence counts for summaries, reviewer notes, or support replies)
  - `char_count_range` (enforces lower/upper output-length bounds using raw character counts)
  - `byte_count_range` (enforces UTF-8 byte-length bounds for UI labels, commit titles, or multilingual outputs)
- Example fixture trio for deterministic release-note length checks: `examples/dataset/word_count_range_release_notes.jsonl` + matching outputs
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
That walkthrough now also includes a PR-comment-ready FAIL summary snippet for reviewer notes and release-review threads.
If you want a dedicated reviewer-note template, open `examples/word_count_pr_comment_playbook.md` for a generate -> paste -> rerun flow built around the committed word-count snapshots.
If you need to decide the first rerun lane from reviewer-queue metadata, open `examples/reviewer_queue_next_focus_playbook.md` for a compact `dominant focus -> next-focus -> tie-mode` triage flow.
Committed reviewer-facing markdown output for the same fixture lives at `examples/artifacts/word-count-range.summary.md`, and the matching machine-readable gate payload now lives at `examples/artifacts/word-count-range.summary.json` for CI drift checks.
A ready-to-paste reviewer note snapshot now also lives at `examples/artifacts/word-count-range.pr-comment.md`, regenerated alongside the markdown/json walkthrough artifacts.
The walkthrough PASS fixture now also ships an approval-ready reviewer note snapshot at `examples/artifacts/walkthrough-pass.pr-comment.md`, and the matching FAIL fixture now ships a blocking note snapshot at `examples/artifacts/walkthrough-fail.pr-comment.md`, so teams can paste both approval and failure comment shapes from committed artifacts.
Those walkthrough PR-comment snapshots now use dedicated reviewer-facing titles (`walkthrough approval note` / `walkthrough blocker note`) so the committed comments read like paste-ready review outcomes without changing the markdown artifact headings.
Those PR-comment snapshots keep the same schema marker, explicit pass-rate trend, and deterministic stable/regression ids as the markdown/JSON artifacts, so reviewers can paste the note without reformatting CI output.
`./scripts/regenerate_walkthrough_artifacts.sh` now regenerates those PR-comment snapshots from the same CLI contract via `--summary-pr-comment`, so reviewer-note wording stays formatter-consistent with the committed markdown/JSON summaries.
Need to pipe the reviewer note directly into CI or a PR bot? `--summary-pr-comment -` now shares the same stdout ergonomics as `--summary-markdown -`, so workflows can render or post the ready-to-paste note without creating a temp file first. For a copy-paste CI example (including a shell capture that preserves a custom stdout title), open `examples/ci_pr_comment_stdout.md`.
Need a reviewer-note heading that differs from the markdown artifact title? Use `--summary-pr-comment-title` so PR-comment snapshots can say `review snapshot` or `release blocker note` without changing `--summary-markdown-title`. The committed word-count snapshots demonstrate this split directly: markdown keeps `word-count release-note gate`, while the PR-comment artifact uses `word-count blocker note` for paste-ready reviewer language. CI now also asserts the committed walkthrough PR-comment snapshots keep their custom headings (`walkthrough approval note` / `walkthrough blocker note`) so reviewer-note formatting cannot silently fall back to the default title.
Regex expectations also support the `VERBOSE` flag now, so multiline commented patterns can stay readable in committed datasets without losing deterministic matching.
PR-comment output now also carries `Filtered-out IDs` and `Skipped IDs` when filters or disabled cases shrink the active scope, so reviewers can see scope exclusions without opening the JSON artifact.
PR-comment output now also surfaces `Filtered-out rate` and `Skipped-case rate`, so reviewers can gauge how much scope moved out of the shard without opening the JSON artifact.
PR-comment output now also surfaces `Tool version` plus `Required schema version gate`, so paste-ready reviewer notes expose both the producing build and the expected summary contract without opening the JSON or markdown artifacts.
PR-comment output now also surfaces `Selection rate` and `Active-case rate`, making shard coverage and post-filter execution scope visible in paste-ready reviewer notes without opening the JSON or markdown artifacts.
PR-comment output now also surfaces reviewer-queue breakdown lines (`regressions`, `watchlist`, `filtered-out scope`, `skipped cases`) so reviewers can see what kind of follow-up work dominates a rerun without opening the JSON artifact.
PR-comment output now also surfaces `Reviewer queue dominant focus`, a copy-paste label for the largest follow-up bucket, so triage notes can immediately say whether the rerun is mostly regressions, watchlist carryover, filtered scope review, or skipped-case cleanup.
PR-comment and markdown summaries now also expose `Reviewer queue next-focus case count`, `Reviewer queue next-focus active-case rate`, `Reviewer queue next-focus source-case rate`, and `Reviewer queue next-focus priority rank`, so the first rerun bucket can be sized in absolute cases and placed inside the deterministic follow-up order without opening JSON.
PR-comment and markdown summaries now also expose `Reviewer queue follow-up priority`, so reviewers can see the recommended bucket order (`fix_regressions -> watch_unchanged_fails -> confirm_filtered_scope -> resolve_skipped_cases`) without opening JSON.
PR-comment and markdown summaries now also expose `Reviewer queue follow-up priority labels` (`P1 · fix regressions -> P2 · watch unchanged fails -> ...`), so pasted handoffs can preserve both queue order and reviewer-facing language without reconstructing labels from separate key/rank lines.
They now also expose `Reviewer queue group queue shares`, so reviewers can see how much of the queued follow-up load belongs to each bucket without opening JSON.
They now also expose `Reviewer queue group keys` and `Reviewer queue group labels`, so pasted summaries show the exact queue buckets already present in the current shard without reconstructing them from individual lines.
Those per-group reviewer-queue lines now also show source-case rate, so shard-heavy reruns can distinguish active-case dominance from full-dataset impact at a glance.
PR-comment snapshots now also surface `Reviewer queue tied largest labels`, so tie-heavy reruns spell out the human-readable queue buckets directly when regressions and watchlist/filtered/skipped work land in the same-sized bucket.
Markdown/PR-comment summaries now also surface `Reviewer queue next-focus tie mode` (`unique` vs `tied`), so reviewer notes can tell whether the current next-focus bucket is an unambiguous first action or one of several equally large rerun lanes.
The JSON `summary.reviewer_queue` payload now mirrors that same handoff via explicit `next_focus_key`, `next_focus_label`, `next_focus_priority_rank`, `next_focus_ids`, `next_focus_case_count`, `next_focus_queue_share`, and `next_focus_tie_mode` aliases, so bots can route, rank, and size the first rerun lane without reverse-engineering the larger queue object.
The reviewer-queue JSON now also exposes `next_focus_advantage_summary`, a paste-ready sentence that explains how far ahead the current first rerun lane sits versus the runner-up in cases, queue share, active-case rate, and source-case rate.
That payload now also includes a nested `next_focus_group` object (`key`, `label`, `priority_label`, `priority_rank`, `ids`, `case_count`, `active_case_rate`, `source_case_rate`, `queue_share`, `tie_mode`) so bots can consume the first rerun lane as a single structured handoff instead of stitching alias fields together.
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
