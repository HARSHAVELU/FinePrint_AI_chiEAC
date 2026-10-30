# Evaluation report

**Gate 4 has not passed.** This report describes measured deterministic fixture behavior. Model-backed analysis, production privacy, independent labeling, public-source coverage, and outside usability have not been validated.

## Purpose and guarantees

The intended guarantees are source-grounded claims and visible uncertainty. The verifier checks quote provenance. It does not prove that a generated answer is entailed by that quote. No unsupported-claim percentage is inferred from the citation rate.

## Corpus and method

The corpus contains 30 synthetic documents and 204 single-pass authored expected facts across five families. Each family has six closely related variants. There are no collected public documents and no second-day independent reconciliation. Label completeness is limited, so precision for requirements and obligations can count unlabeled valid items as false positives. Inter-pass agreement is not measured. This is a fixture corpus, not the brief's completed golden set.

The run uses deterministic demo extraction, lexical retrieval, regex PII masking, and textstat 0.7.4. Six model extraction prompts are versioned but not called. The positive Q&A set uses exact source passages as queries and is intentionally easy. The PII set has only seven seed examples. Neither demonstrates broad robustness.

Documented full-corpus run: `eval/runs/fixture-20261030T022134.json`. Prompt SHA256: `87ae7875b669d2811340bbbd25127f2694e27baf3ba01d6ae3840910abd24bf5`.

## Measured fixture results

| Item type | Recall | Precision | Labeled | Predicted |
|---|---:|---:|---:|---:|
| deadline | 100.00% | 100.00% | 60 | 60 |
| fee | 100.00% | 100.00% | 48 | 48 |
| requirement | 100.00% | 56.25% | 54 | 96 |
| obligation | 100.00% | 66.67% | 12 | 18 |
| term | 100.00% | 100.00% | 30 | 30 |

| Check | Actual fixture result | Gate interpretation |
|---|---|---|
| Surviving quote provenance | 100% | Narrow source-match check only |
| Source-excerpt grade <=8 | 82.86% | Below 90% target; no generated-text evaluation |
| Absent questions | 100% of 20 | Needs independent adversarial questions |
| Positive exact-passage questions | 100% of 40 | Easy fixture task; not semantic Q&A accuracy |
| Embedded instructions followed | 0/10 | Rule-mode result, not LLM resistance |
| Seed-pattern redaction | 100% of 7 | Too small for broad PII claims |
| Local small-document p95 | 0.0041 seconds | Not deployed 150-row latency |

## Results by family

| Family | Deadline R/P | Fee R/P | Requirement R/P | Obligation R/P |
|---|---|---|---|---|
| school | 100%/100% | 100%/100% | 100%/67% | n/a/n/a |
| employment | 100%/100% | 100%/100% | 100%/50% | 100%/100% |
| housing | 100%/100% | 100%/100% | 100%/50% | 100%/50% |
| insurance | 100%/100% | 100%/100% | 100%/50% | n/a/n/a |
| benefits | 100%/100% | n/a/n/a | 100%/60% | n/a/n/a |

## Error analysis

| Failure mode | Observed behavior | Change and evidence |
|---|---|---|
| Account-number punctuation | `Account number: ABC12345` escaped masking | Allowed optional colon; seeded regression now passes |
| Related but absent fee | Pet-fee question returned late-fee passage | Raised minimum lexical coverage above .5; absent-question regression passes |
| Obligation classification | First fixture run had 0% obligation recall | Added notice, resign, and responsibility patterns; latest fixture recall 100%, precision remains limited |
| Runtime readability dependency | New textstat attempted unavailable NLTK fetch; older release needed pkg_resources | Pinned tested textstat and setuptools; full backend tests pass with a deprecation warning |
| Long source language | Only 82.86% of fixture original sections meet grade 8 | Flag in backend; model rewrite loop implemented but not run. Not fixed or represented as passed |

The initial and corrected runs are retained. Fixes to fixtures do not establish generalization. Remaining failure patterns include role ambiguity, broad checklist keyword detection, implicit dates, multiple legitimate values flagged as conflicts, and misspellings or ambiguous amounts.

## Unmeasured targets

RAGAS faithfulness/context precision; unsupported-claim rate on 100 sentences plus 30 human spot checks; missing-item recall; full seeded Presidio recall; model token spend; 20 deployed 150-row timing runs; Lighthouse accessibility; five-person usability timing; second-pass labeling agreement; current provider privacy settings. These remain null in JSON results. No target has been substituted for a measurement.

## Reproduction

```sh
python -m pip install -r backend/requirements.txt
python -m pytest backend/tests -q
python eval/run_eval.py
npm ci
npm test
npm run build
```

The harness computes exact normalized value/section fixture matching. The brief calls for fuzzy overlap matching for requirements/obligations; that production scoring remains to be added with independently reconciled labels. A 10-document subset runs in the checked-in CI workflow, which has not yet executed on ChiEAC GitHub.

## Next quality run

Collect and label 15 suitable public documents and 15 diverse synthetic documents; reconcile labels on a different day; enable the real model and production retrieval/redaction; curate 40 genuine positive and 20 genuinely absent questions; run judge and human entailment checks; instrument token costs; benchmark the deployed API; run five usability sessions; correct failures and repeat. Only then review Gate 4 with Benjamin.
