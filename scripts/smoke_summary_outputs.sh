#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

PASS_MD="$TMPDIR/pass.summary.md"
PASS_JSON="$TMPDIR/pass.summary.json"
PASS_PR="$TMPDIR/pass.pr-comment.md"
FAIL_MD="$TMPDIR/fail.summary.md"
FAIL_JSON="$TMPDIR/fail.summary.json"
FAIL_PR="$TMPDIR/fail.pr-comment.md"

cd "$ROOT"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
TOOL_VERSION="$(python3 - <<'PY'
from prompt_regression_min import __version__
print(__version__)
PY
)"

python3 -m prompt_regression_min.cli run \
  --dataset "$ROOT/examples/dataset/walkthrough_pass_artifact_demo.jsonl" \
  --baseline "$ROOT/examples/outputs/walkthrough_pass_artifact_demo.baseline.jsonl" \
  --candidate "$ROOT/examples/outputs/walkthrough_pass_artifact_demo.candidate.jsonl" \
  --min-improved 1 \
  --require-summary-schema-version 1 \
  --summary-markdown "$PASS_MD" \
  --summary-json "$PASS_JSON" \
  --summary-pr-comment "$PASS_PR" \
  --summary-pr-comment-title "walkthrough approval note" \
  --quiet

python3 - <<'PY' "$PASS_MD" "$PASS_JSON" "$PASS_PR" "$TOOL_VERSION"
import json
import sys
from pathlib import Path
md = Path(sys.argv[1]).read_text(encoding='utf-8')
payload = json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
pr = Path(sys.argv[3]).read_text(encoding='utf-8')
tool_version = sys.argv[4]
assert payload['status'] == 'PASS', payload
assert payload['summary']['improved_ids'] == ['checkout-copy'], payload
for marker in (
    '## prompt-regression-min summary',
    '- Status: **PASS**',
    '- Improved IDs (1): `checkout-copy`',
    '- Required schema version gate: `1`',
):
    assert marker in md, marker
for marker in (
    '## walkthrough approval note',
    f'- Tool version: `{tool_version}`',
    '- Required schema version gate: `1`',
    'approval-ready',
):
    assert marker in pr, marker
print('pass smoke: PASS')
PY

set +e
python3 -m prompt_regression_min.cli run \
  --dataset "$ROOT/examples/dataset/walkthrough_fail_artifact_demo.jsonl" \
  --baseline "$ROOT/examples/outputs/walkthrough_fail_artifact_demo.baseline.jsonl" \
  --candidate "$ROOT/examples/outputs/walkthrough_fail_artifact_demo.candidate.jsonl" \
  --summary-markdown "$FAIL_MD" \
  --summary-json "$FAIL_JSON" \
  --summary-pr-comment "$FAIL_PR" \
  --summary-pr-comment-title "walkthrough blocker note" \
  --quiet
STATUS=$?
set -e
if [[ "$STATUS" -ne 1 ]]; then
  echo "expected fail fixture to exit 1, got $STATUS" >&2
  exit 1
fi

python3 - <<'PY' "$FAIL_MD" "$FAIL_JSON" "$FAIL_PR" "$TOOL_VERSION"
import json
import sys
from pathlib import Path
md = Path(sys.argv[1]).read_text(encoding='utf-8')
payload = json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
pr = Path(sys.argv[3]).read_text(encoding='utf-8')
tool_version = sys.argv[4]
assert payload['status'] == 'FAIL', payload
assert payload['summary']['regression_ids'] == ['auth-login'], payload
for marker in (
    '## prompt-regression-min summary',
    '- Status: **FAIL**',
    '- Regression IDs (1): `auth-login`',
    '- Fail reasons:',
):
    assert marker in md, marker
for marker in (
    '## walkthrough blocker note',
    '- Regression IDs (1): `auth-login`',
    f'- Tool version: `{tool_version}`',
    '- Reviewer queue total: 1 case(s)',
    '- Required schema version gate: _disabled_',
):
    assert marker in pr, marker
print('fail smoke: PASS')
PY

echo 'summary output smoke: PASS'
