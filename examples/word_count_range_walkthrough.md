# Word-count range walkthrough

Use this fixture trio to smoke-test concise release-note or summarization outputs with deterministic length bounds.

```bash
PYTHONPATH=src python3 -m prompt_regression_min run \
  --dataset examples/dataset/word_count_range_release_notes.jsonl \
  --baseline examples/outputs/word_count_range_release_notes.baseline.jsonl \
  --candidate examples/outputs/word_count_range_release_notes.candidate.jsonl \
  --report .tmp/word-count-range-report.json
```

Expected outcome:
- `release-note-short` becomes a regression because the candidate is too short.
- `release-note-bullets` also regresses because the candidate drops below the minimum word-count band.

Reviewer-facing markdown summary smoke:

```bash
PYTHONPATH=src python3 -m prompt_regression_min run \
  --dataset examples/dataset/word_count_range_release_notes.jsonl \
  --baseline examples/outputs/word_count_range_release_notes.baseline.jsonl \
  --candidate examples/outputs/word_count_range_release_notes.candidate.jsonl \
  --summary-markdown - \
  --summary-markdown-title "word-count release-note gate"
```

Expected markdown highlights:
- `release-note-short` and `release-note-bullets` appear under regressions.
- The markdown header uses `word-count release-note gate`.


Committed snapshot files:
- Markdown: `examples/artifacts/word-count-range.summary.md`
- JSON: `examples/artifacts/word-count-range.summary.json`

One-command regeneration:

```bash
./scripts/regenerate_walkthrough_artifacts.sh
```

Expected regeneration behavior:
- The word-count fixture remains a FAIL artifact because it intentionally exceeds the release-note budget gate.
- The regenerated markdown keeps the `word-count release-note gate` title so reviewer-facing snapshots stay stable.

Snapshot drift check:

```bash
python3 - <<'PY'
import json
from pathlib import Path

payload = json.loads(Path('examples/artifacts/word-count-range.summary.json').read_text(encoding='utf-8'))
assert payload['status'] == 'FAIL'
assert payload['summary']['regression_ids'] == ['release-note-bullets', 'release-note-short']
md = Path('examples/artifacts/word-count-range.summary.md').read_text(encoding='utf-8')
assert 'word-count release-note gate' in md
assert 'Summary schema version: `1`' in md
print('word-count snapshot drift: PASS')
PY
```
