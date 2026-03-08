#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p examples/artifacts

PYTHONPATH=src python3 -m prompt_regression_min run \
  -d examples/dataset/walkthrough_pass_artifact_demo.jsonl \
  -b examples/outputs/walkthrough_pass_artifact_demo.baseline.jsonl \
  -c examples/outputs/walkthrough_pass_artifact_demo.candidate.jsonl \
  --summary-json examples/artifacts/walkthrough-pass.summary.json \
  --summary-markdown examples/artifacts/walkthrough-pass.summary.md \
  --quiet

set +e
PYTHONPATH=src python3 -m prompt_regression_min run \
  -d examples/dataset/walkthrough_fail_artifact_demo.jsonl \
  -b examples/outputs/walkthrough_fail_artifact_demo.baseline.jsonl \
  -c examples/outputs/walkthrough_fail_artifact_demo.candidate.jsonl \
  --max-regressions 0 \
  --summary-json examples/artifacts/walkthrough-fail.summary.json \
  --summary-markdown examples/artifacts/walkthrough-fail.summary.md \
  --quiet
status=$?
set -e

if [[ "$status" -eq 0 ]]; then
  echo "expected walkthrough_fail_artifact_demo to fail gate evaluation" >&2
  exit 1
fi

echo "walkthrough artifacts regenerated: PASS"
