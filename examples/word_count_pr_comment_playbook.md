# Word-count PR comment playbook

Use this playbook when the word-count range fixture fails and you need a reviewer-facing PR comment or release-review note quickly.

## 1) Generate the markdown summary

```bash
PYTHONPATH=src python3 -m prompt_regression_min run \
  --dataset examples/dataset/word_count_range_release_notes.jsonl \
  --baseline examples/outputs/word_count_range_release_notes.baseline.jsonl \
  --candidate examples/outputs/word_count_range_release_notes.candidate.jsonl \
  --summary-markdown - \
  --summary-markdown-title "word-count release-note gate"
```

Expected result:
- Status stays `FAIL`.
- `release-note-bullets` and `release-note-short` stay in `Regression ids`.
- The markdown is short enough to paste directly into a PR comment.

## 2) Paste this reviewer note

```markdown
## word-count release-note gate
- Status: `FAIL`
- Summary schema version: `1`
- Regression ids: `release-note-bullets`, `release-note-short`
- Why it failed: both candidate release notes fell below the configured minimum word-count band.
- Reviewer next step: ask the author to expand the candidate release notes, then rerun the same fixture trio before merging.
```

## 3) Optional release-review note

```markdown
Release review note: keep this change blocked until the release-note outputs recover the minimum word-count band for `release-note-bullets` and `release-note-short`. Rerun `examples/word_count_range_walkthrough.md` after updating the candidate text.
```

## 4) Stable artifact references

- Markdown snapshot: `examples/artifacts/word-count-range.summary.md`
- JSON snapshot: `examples/artifacts/word-count-range.summary.json`
- Regeneration helper: `./scripts/regenerate_walkthrough_artifacts.sh`
