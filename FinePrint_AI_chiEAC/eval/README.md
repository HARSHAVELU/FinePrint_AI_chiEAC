# Evaluation harness

From the repository root: `python eval/run_eval.py`. Use `--subset 10` for the CI smoke subset. See docs/evaluation-report.md for actual results and limitations. The current harness is a fixture regression harness, not a complete implementation of every production metric in Section 9. Unmeasured gates remain null. Do not use these synthetic scores as resume claims.

Runs are timestamped with mode, model ID, prompt SHA256, corpus counts, per-type and per-family scores, quote provenance, readability, basic Q&A, seeded redaction, injection, and local tiny-document latency. The golden sources manifest explicitly records that public data collection is incomplete. No production evaluator has silently used a lexical fallback while claiming dense retrieval results.
