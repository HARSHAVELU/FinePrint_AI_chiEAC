# Requirements through Gate 4

The brief names Gates 0 through 4, rather than numbered phases. This delivery includes a demo dashboard as well as backend work. **No gate is certified complete.** Implemented means source exists and the stated tests were run; configured means an optional path exists but was not exercised; pending means evidence or external work is missing.

## Foundations and Gate 0

| Requirement | Status | Evidence or next action |
|---|---|---|
| ChiEAC GitHub organization invitation | Pending | No invitation or organization access supplied |
| fineprint-ai repository in organization | Pending | Source package prepared; import into ChiEAC required |
| MIT license, README, ignore secrets | Implemented | LICENSE, README.md, .gitignore |
| Main branch protection and PR-only workflow | Pending | Requires ChiEAC repository admin access |
| Python, Node development environment | Implemented | Backend tests and frontend build ran |
| Docker Desktop and editor extensions | Pending | Desktop installations are outside this environment |
| API, tracing, host, model accounts and spending cap | Pending | Account setup/settings not available |
| FastAPI hello endpoint deployed early | Pending | Local API tested; Python API not deployed |
| Source scaffold, schema documentation | Implemented | backend/, frontend/, docs/api.md |
| Three example input formats | Implemented | public/templates/ CSV JSON XLSX |
| 15 public and 15 synthetic golden documents | Partial | 30 synthetic fixtures; no public corpus collected |
| First 10 independent labels | Partial | 204 authored fixture facts; independent reconciliation missing |
| Reviewed wireframe | Pending | Working dashboard supersedes sketch; Benjamin review missing |
| Progress plan and kickoff draft | Implemented | progress.md; kickoff publication not verified |
| Kickoff sent and LinkedIn post live | Pending | Drafts only; nothing sent or posted |

## Ingestion and Gate 1

| Requirement | Status | Evidence or next action |
|---|---|---|
| CSV JSON XLSX parsers and fallback | Implemented | Parser tests for all formats and aliases |
| Size row limits and friendly errors | Implemented | Backend and frontend checks |
| Presidio names addresses phones emails SSNs accounts DOB | Configured | Production adapter; seeded pattern fallback tested |
| Typed placeholder mapping in session memory | Implemented | Server mapping; browser masks and discards originals |
| Local bge embeddings and per-session Chroma | Configured | Requires production dependencies and downloaded weights |
| Section boundaries and page metadata | Implemented | One schema row per retrievable section |
| 30-minute inactivity expiry | Implemented | Browser timer; server periodic purge; expiry test |
| Upload and search routes | Implemented | API lifecycle test and OpenAPI |
| 50 query/section retrieval pairs | Implemented | data/golden/retrieval-pairs.json; narrow fixture set |
| All 30 documents parse | Verified | Automated parser test |
| PII recall at least 95% | Not certified | Seven seeded pattern examples pass; no broad Presidio audit |
| Retrieval hit@3 at least .85 | Not certified | Lexical fixture test is not production dense retrieval |
| Review and LinkedIn update | Pending | External human actions not completed |

## Extraction checkpoint and Gate 2

| Requirement | Status | Evidence or next action |
|---|---|---|
| Typed item contracts, required quote and confidence | Implemented | Pydantic Item and CandidateList |
| Six structured extraction calls in model mode | Configured | Versioned prompts and model adapter; untested without key |
| Deterministic exact and fuzzy verifier | Verified | Quote rejection, normalized match, confidence tests |
| Failed citations routed to uncertainty | Implemented | verify and gaps nodes |
| Absolute dates and anchored relative dates | Partial | Explicit formats; calendar arithmetic; business-day dates unresolved |
| High Medium Low badges and calculation steps | Implemented | Backend rules; source cards show badges |
| Analyze endpoint | Verified | API end-to-end test |
| Deadline and fee precision/recall harness | Implemented | eval/run_eval.py and timestamped results |
| 15 then 20 independently labeled documents | Pending | Single-pass synthetic expected facts only |
| Five checklists, eight or more entries per family | Implemented | backend/app/checklists/*.json |
| Plain-language rewrite with textstat and two retries | Configured | Model path untested; demo displays original excerpts |
| Readability grade 8 on 90% of sections | Below target | 82.86% of fixture source excerpts; no generated-text score |
| Grounded Q&A, five passages, verifier, abstention | Implemented | Model adapter plus tested extractive demo |
| 20 absent questions and 10 embedded payloads | Implemented | Evaluation cases and tests; model resistance unmeasured |
| OpenAPI contract and API guide | Implemented | Runtime /openapi.json, docs/api.md |
| Complete production backend gate review | Pending | Model-backed run and Benjamin review required |

## Dashboard and Gate 3

| Requirement | Status | Evidence or next action |
|---|---|---|
| React Vite TypeScript Tailwind dashboard | Implemented | Build passed |
| Upload, downloads, preparation guide, progress state | Implemented | Landing page and templates |
| Two columns and all six item categories | Implemented | Dates, requirements, money, obligations, gaps, terms |
| Source chips and exact-text highlight | Browser checked | Lease source dialog inspected |
| Ask panel and absent answer | Tested | Engine tests and browser interaction |
| My To-Do List print stylesheet | Implemented | Print-to-PDF through browser; page count not guaranteed |
| Disclaimer, who-to-ask links, privacy text | Implemented | Persistent footer and help panel |
| Mobile styles, labels, keyboard navigation | Implemented | Responsive rules and dialog focus handling |
| Lighthouse accessibility at least 90 | Pending | No score measured |
| Three demo documents on deployed URL | Implemented | Hosted standalone browser prototype |
| Frontend connected to deployed FastAPI | Pending | Optional API integration exists; separate host/key required |
| Five non-technical tests below 60 seconds | Pending | Protocol included; no invented tester records |
| Fix top three user confusions | Pending | Requires real sessions |
| Screen recording and weekly post | Pending | Demo script provided; not recorded or published |

## Evaluation and Gate 4

| Requirement | Status | Evidence or next action |
|---|---|---|
| 30 mixed-source documents and about 300 labels | Partial | 30 synthetic fixtures and 204 expected facts |
| Label twice on different days and reconcile | Pending | Cannot be completed retroactively in one session |
| Recall precision by type and family | Implemented | Fixture harness; label coverage limitations disclosed |
| Citation verification rate | Measured on fixtures | 100% of surviving fixture quotes; not entailment |
| Unsupported-claim audit | Pending | 100-sentence judge sample and 30 manual checks needed |
| Abstention in/out of document | Fixture only | 20 absent and 40 exact-passage questions; easy positive set |
| Injection resistance | Fixture only | 0/10 rule-mode payloads; LLM run needed |
| Missing-item recall | Pending | Independent omission labels needed |
| PII redaction recall | Fixture only | 7 seed patterns; full Presidio audit needed |
| Readability | Below target | Demo source excerpts 82.86% at grade 8 or below |
| Deployed 150-row p95 over 20 runs | Pending | Local tiny-fixture latency cannot substitute |
| Model cost below $0.05/document | Pending | No provider calls or token-cost record |
| RAGAS faithfulness and context precision | Pending | No credentials or judge run; do not infer from citations |
| Five failure modes and before/after analysis | Partial | Real defects recorded in evaluation report |
| Timestamped runs and prompt versions | Implemented | eval/runs/ with model/mode and prompt hash |
| Rate limits timeouts resource limits safe errors | Implemented | Application controls; edge controls need deployment review |
| No content logging; tracing capture disabled | Implemented | App settings; host/provider policy review still required |
| OWASP basics review | Partial | security-review.md; external audit not performed |
| Evaluation report and 10-document CI subset | Implemented | Report and workflow; GitHub CI not yet executed |
| All metrics meet target and Benjamin approval | Pending | Gate 4 is not passed |

## External completion actions

The user or ChiEAC must supply access to the intended organization and hosting/model accounts, enable account controls, arrange five outside testers, conduct the second labeling pass on another day, and obtain Benjamin's reviews. Do not commit provider keys. Store secrets directly in the chosen server environment. No email, invitation, or LinkedIn publication is certified by this package.
