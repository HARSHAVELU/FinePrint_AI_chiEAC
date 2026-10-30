# Engineering handoff

## Run and deploy

Use README commands for the standalone browser demo or connected backend. `npm run build` emits `dist/` for static hosting. The browser-only frontend works independently. Deploy the Python backend separately for connected mode. A hosting account and service configuration are required for backend deployment. Set its exact CORS origin, resource/body limits, and one worker. Set `VITE_FINEPRINT_API` at frontend build time and rebuild to connect it.

## Model and secrets

Keys belong only in a server secret manager or local ignored env file. Select `FINEPRINT_MODE=llm`, the available model ID, Presidio, and Chroma, then run production requirements. The model adapter uses the Anthropic SDK with a 30-second request timeout and one retry. Six extraction calls plus section-by-section rewriting can exceed the cost and latency targets; no cost target is certified. Set the provider's monthly budget cap in its own account. Rotate a key in that account, update the server environment, restart, validate `/health`, and run synthetic smoke tests. Never paste keys into frontend config, CI output, Git, or a demonstration.

## Extend families

Add a JSON checklist in `backend/app/checklists/` with at least eight entries: key, regex patterns, and a suggested question. Add a family to classifier keywords or model schema, add independently labeled documents, and update the UI label map. Rebuild `frontend/src/checklists.json` from the backend files. A future provider/config schema should centralize family registration to avoid these duplicate lists.

## Read and reproduce evaluations

Run `python eval/run_eval.py`; inspect timestamped JSON in `eval/runs/`. It stores synthetic questions and metrics, never user sessions. All fixture scores are bounded by the narrow corpus. `docs/evaluation-report.md` distinguishes targets, actual results, and unmeasured gates. The production golden set needs public sources, independent reconciliation on a different day, ambiguity handling, and blinded tests. RAGAS, human entailment checks, deployed 150-row latency, token-cost accounting, and usability remain outstanding. Indicative cost per 1,000 documents is unknown until measured; do not multiply a target into a claim.

## Operations and known limits

Sessions and rate limits are per process. Chroma must remain ephemeral; no persistent storage path is configured. Use process memory limits and cleanup monitoring. Server errors must never expose provider responses or user text. No content is logged by application code; review hosting logs separately. Analysis timeouts do not cancel a worker thread's provider call. Server limits should be reinforced at the edge, including streaming body limits, zip expansion protection, and outbound timeouts. Dependency scanning and current OWASP review are required before public production use.

Import this source package into the intended `fineprint-ai` GitHub repository, enable branch protection and required CI, and assign maintainers. Organization access and administrative settings must be verified separately. No invitation, organization setting, review sign-off, social post, email, or video is represented as completed. Requirement checklists are included for review.
