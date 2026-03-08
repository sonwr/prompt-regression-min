#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

ARTIFACT_DIR="${PRM_WALKTHROUGH_ARTIFACT_DIR:-examples/artifacts}"
mkdir -p "$ARTIFACT_DIR"

PYTHONPATH=src python3 -m prompt_regression_min run \
  -d examples/dataset/walkthrough_pass_artifact_demo.jsonl \
  -b examples/outputs/walkthrough_pass_artifact_demo.baseline.jsonl \
  -c examples/outputs/walkthrough_pass_artifact_demo.candidate.jsonl \
  --summary-json "$ARTIFACT_DIR/walkthrough-pass.summary.json" \
  --summary-markdown "$ARTIFACT_DIR/walkthrough-pass.summary.md" \
  --require-summary-schema-version 1 \
  --quiet

set +e
PYTHONPATH=src python3 -m prompt_regression_min run \
  -d examples/dataset/walkthrough_fail_artifact_demo.jsonl \
  -b examples/outputs/walkthrough_fail_artifact_demo.baseline.jsonl \
  -c examples/outputs/walkthrough_fail_artifact_demo.candidate.jsonl \
  --max-regressions 0 \
  --summary-json "$ARTIFACT_DIR/walkthrough-fail.summary.json" \
  --summary-markdown "$ARTIFACT_DIR/walkthrough-fail.summary.md" \
  --require-summary-schema-version 1 \
  --quiet
status=$?
set -e

if [[ "$status" -eq 0 ]]; then
  echo "expected walkthrough_fail_artifact_demo to fail gate evaluation" >&2
  exit 1
fi

echo "walkthrough artifacts regenerated: PASS"


set +e
PYTHONPATH=src python3 -m prompt_regression_min run \
  -d examples/dataset/word_count_range_release_notes.jsonl \
  -b examples/outputs/word_count_range_release_notes.baseline.jsonl \
  -c examples/outputs/word_count_range_release_notes.candidate.jsonl \
  --max-regressions 0 \
  --summary-json "$ARTIFACT_DIR/word-count-range.summary.json" \
  --summary-markdown "$ARTIFACT_DIR/word-count-range.summary.md" \
  --summary-markdown-title "word-count release-note gate" \
  --quiet
word_count_status=$?
set -e

if [[ "$word_count_status" -eq 0 ]]; then
  echo "expected word_count_range_release_notes fixture to fail gate evaluation" >&2
  exit 1
fi
