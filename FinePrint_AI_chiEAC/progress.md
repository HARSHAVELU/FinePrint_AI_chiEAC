# FinePrint AI Progress

Reporting period: September 21 to October 29, 2026.

## Reporting basis

This file summarizes the implementation, verification results, and supporting files for the September 21 to October 29 reporting period.

## Implemented

- Created the React, TypeScript, Vite, and Tailwind frontend and FastAPI backend structure.
- Defined input rows and typed extracted items with Pydantic contracts.
- Added CSV, JSON, and XLSX parsing, single-column fallback, and input limits.
- Added LangGraph upload and analysis stages, session handling, and expiry.
- Added pattern masking, lexical retrieval, deterministic extraction, source verification, checklist gaps, and extractive answers in demo mode.
- Added optional adapters for Presidio, bge-small embeddings, ephemeral Chroma, and Anthropic model analysis.
- Built the dashboard, source highlight dialog, confidence display, Q&A, input guide, template downloads, and print stylesheet.
- Added three built-in demos and a separate fictional rental-lease upload sample.
- Created five family checklists, thirty synthetic documents, 204 expected facts, and fifty exact-passage retrieval pairs.
- Added tests, evaluation runs, a CI workflow, and technical documentation.
- Prepared the revised Word progress report, first-person project walkthrough, and standalone source package.

## Verification recorded

| Check | Result | Scope |
|---|---|---|
| Backend automated tests | 36 passed | Parser, redaction, verifier, dates, API lifecycle, expiry, and validation checks |
| Browser-engine tests | 6 passed | Fixture extraction, input handling, masking, Q&A, injection case, and waived fee |
| Frontend production build | Passed | TypeScript and Vite |
| Ten-document evaluation subset | Passed regression assertions | Citation provenance and rule-mode injection checks |
| Source report | Revised | Includes a first-person project walkthrough; requested table and trailing reference lines removed |

## Defects corrected

- Allowed punctuation in account-number masking patterns.
- Raised lexical answer coverage to avoid matching a pet-fee question to an unrelated late fee.
- Expanded obligation patterns for notice, resignation, and responsibility language.
- Pinned compatible readability dependencies after runtime resource failures.

## Measured fixture limitations

The evaluation uses narrow synthetic examples and single-pass, incomplete annotations. Its scores do not establish production accuracy or broad PII protection. Requirement precision was 56.25% and obligation precision was 66.67% on the labeled fixture matching task. Only 82.86% of source excerpts met grade 8, below the brief's 90% target. The browser demo presents source excerpts rather than generated plain-language rewrites.

Model-backed quality, independent annotation agreement, RAGAS, deployed large-document latency, model cost, five-person usability, and Lighthouse accessibility remain unmeasured. Reviewer approval and organizational repository settings are not certified by this file.

## Review

Version 1 is prepared for review and can be modified based on feedback, if necessary.
