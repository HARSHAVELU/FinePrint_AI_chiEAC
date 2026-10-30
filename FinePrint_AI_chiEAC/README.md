# FinePrint AI

FinePrint AI is a document-reading prototype developed for Chicago Education Advocacy Cooperative by Harshavelu Irrigisetty. It organizes deadlines, costs, requirements, obligations, missing information, and document-defined terms alongside their source passages.

## Features

- CSV, JSON, and XLSX uploads, with a 5 MB and 400-row limit.
- Single-column input fallback and validation errors.
- Dates, requirements, Money, Watch Out, Missing or Unclear, and Glossary panels.
- Exact source passages, section references, highlighting, and confidence badges.
- Document questions with source citations or an explicit missing-answer response.
- Three fictional examples, downloadable templates, and a printable action list.
- A separate FastAPI backend with typed LangGraph stages and configurable production adapters.

## Version 1 for review

Version 1 is prepared for review and can be modified based on feedback, if necessary.

The browser demo uses deterministic rules, lexical passage matching, and source excerpts. It works without a provider key. The separate backend includes optional model analysis, Presidio redaction, local embeddings, and ephemeral Chroma indexing. Those production adapters still require configuration and validation.

## Run in VS Code on Windows

Install Node.js 20 or later. Open this folder in VS Code and run these commands in its terminal:

```powershell
npm.cmd ci
npm.cmd run dev
```

Open the local URL printed by Vite, usually http://localhost:5173. Use `npm.cmd` in PowerShell if execution policy blocks `npm.ps1`.

On macOS or Linux, use `npm ci` and `npm run dev`.

## Project walkthrough

[Read the project walkthrough](docs/project-walkthrough.md) for a description of the application from document upload through source review, questions, and printing.

## Test with a sample file

Use [the fictional rental lease](public/samples/FinePrint_Test_Rental_Lease.csv). Upload it with **Choose a file**.

- The acceptance deadline is November 2, 2026.
- The rent is $1,250 and the deposit is $900.
- The $75 application fee is explicitly waived.
- Ask **When is rent due?** to retrieve a supporting passage.
- Ask **What is the pet fee?** to test abstention.

All names and contact details in the sample are fictional.

## Optional Python backend

Install Python 3.12. From the project root, open a second terminal:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --no-access-log
```

API documentation is available at http://127.0.0.1:8000/docs while the server is running.

To connect the frontend, create a local `.env.local` file next to `package.json`:

```env
VITE_FINEPRINT_API=http://127.0.0.1:8000
```

Restart the frontend and keep both terminals running. The default allowed frontend origin is http://localhost:5173. If Vite uses a different origin, configure `FINEPRINT_ORIGINS` on the backend to match it.

On macOS or Linux, create the environment with `python3.12 -m venv .venv`, activate it with `source .venv/bin/activate`, install the same requirements, and run the same Uvicorn module.

## Model mode

The backend defaults to demo mode. For model mode, install `backend/requirements-production.txt`, download the Presidio language model using `python -m spacy download en_core_web_lg`, and set server environment variables:

```env
FINEPRINT_MODE=llm
FINEPRINT_MODEL=YOUR_AVAILABLE_ANTHROPIC_MODEL_ID
ANTHROPIC_API_KEY=YOUR_SERVER_SECRET
FINEPRINT_REDACTION=presidio
FINEPRINT_RETRIEVAL=chroma
LANGSMITH_TRACING=false
```

Keep real secrets outside Git. These variables are for the server and must never use a `VITE_` prefix. The local embedding model downloads its weights on first use. See [the handoff guide](docs/handoff.md) for configuration limits and deployment considerations.

## Verification

For the frontend:

```powershell
npm.cmd test
npm.cmd run build
```

For the backend and fixture evaluation:

```powershell
.\.venv\Scripts\python.exe -m pytest backend/tests -q
.\.venv\Scripts\python.exe eval/run_eval.py
```

The recorded engineering checks passed 36 backend tests, 6 browser-engine tests, and the frontend build. The data directory contains 30 closely related synthetic documents and 204 single-pass expected facts. These are regression fixtures, not a completed independent production dataset. The CI workflow checks tests, a ten-document fixture subset, and the build after upload to GitHub.

## Repository contents

| Path | Purpose |
|---|---|
| `frontend/` | React interface and browser engine |
| `backend/` | Python API, pipeline, contracts, prompts, checklists, and tests |
| `public/` | Downloadable templates and sample input |
| `data/golden/` | Synthetic fixtures, labels, source notes, and retrieval pairs |
| `eval/` | Evaluation harness and recorded runs |
| `docs/` | Technical guides and the revised project report |
| `scripts/seed.py` | Reproduce the original synthetic fixture set and templates |
| `progress.md` | Implementation progress and measured limitations |
| `.github/workflows/ci.yml` | Automated verification workflow |
| `.gitignore` | Excludes secrets, dependencies, environments, caches, and build output |

## Privacy and scope

Browser mode processes documents on the current device. Basic masking can miss personal information. Connected mode sends uploads to the configured backend and may send redacted text to a model provider, depending on server settings. Review [the privacy guide](docs/privacy.md) before using real documents.

FinePrint AI explains documents. It is not legal, financial, or medical advice, and it can make mistakes. Check important dates against the original document and ask a person you trust.

## License

The source code uses the MIT license. FinePrint AI branding and the organizational product belong to ChiEAC. See LICENSE for the code license.
