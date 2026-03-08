# Gate policy recipes

Copyable `prompt-regression-min` gate combinations for common CI decisions.

## 1) Strict no-regression gate

Use when any regression should block the rollout.

```bash
prm run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --max-regressions 0 \
  --summary-json artifacts/strict-no-regression.json
```

Why use it:

- simplest production gate
- deterministic pass/fail contract
- easy to explain in PR review

## 2) Controlled rollout budget

Use when a candidate may introduce a small amount of churn, but the overall pass rate and stability must stay healthy.

```bash
prm run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --max-regressions 1 \
  --max-regression-rate 0.05 \
  --min-candidate-pass-rate 0.95 \
  --min-stability-rate 0.90 \
  --summary-json artifacts/controlled-rollout.json
```

Why use it:

- separates absolute regression count from overall quality
- reduces noisy approvals when the candidate changes many cases
- keeps release reviews focused on a small failure budget

## 3) Improvement-required cleanup pass

Use when a migration is only worth merging if it fixes at least one existing failing case.

```bash
prm run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --max-regressions 0 \
  --min-improved 1 \
  --summary-json artifacts/improvement-required.json
```

Why use it:

- useful for prompt cleanup branches
- avoids merging “no-op” evaluation updates
- creates a visible contract for quality-improvement work

## 4) Narrow-scope subsystem review

Use when you only want to review one functional slice, such as auth or billing.

```bash
prm run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --include-id-regex '^auth-' \
  --max-filtered-out-cases 50 \
  --max-filtered-out-rate 0.80 \
  --summary-json artifacts/auth-scope.json
```

Why use it:

- keeps experiments scoped to the intended area
- makes filtered-out volume explicit in the result payload
- useful for phased subsystem refactors

## 5) Reviewer-friendly markdown handoff

Use when you want a PR-ready summary plus a machine-readable artifact.

```bash
prm run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --summary-json artifacts/review.summary.json \
  --summary-markdown artifacts/review.summary.md \
  --summary-markdown-title 'release reviewer handoff'
```

Why use it:

- gives humans a compact markdown summary
- keeps CI and release tooling on the JSON artifact
- works well for release notes and PR descriptions
