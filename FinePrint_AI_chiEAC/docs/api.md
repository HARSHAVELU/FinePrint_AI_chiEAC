# API guide

Start the server using the README. Open `/docs` for interactive documentation and `/openapi.json` for the runtime-generated contract. No API key belongs in frontend code. No content should appear in access logs.

| Method | Path | Input | Result |
|---|---|---|---|
| GET | /health | none | mode and backend status |
| POST | /upload | multipart file; optional family_hint | session_id, family, redacted rows, assumptions, redacted count |
| POST | /search | session_id, question | up to five rows and retrieval scores |
| POST | /analyze | session_id | typed verified items, section rewrites, gap questions |
| POST | /ask | session_id, question | answer, abstained flag, citations, nearest passages |
| DELETE | /session/{session_id} | opaque session token | deletion confirmation |

```sh
curl -F file=@public/templates/fineprint-template.csv http://localhost:8000/upload
curl -H 'Content-Type: application/json' -d '{"session_id":"COPY_UPLOAD_TOKEN","question":"When is rent due?"}' http://localhost:8000/ask
```

The API uses 422 for invalid documents, 404 for expired sessions, 413 for oversized requests, 429 for rate limits, 503 for session capacity, and 504 for analysis timeout. Unexpected failures return a generic message; validation responses omit raw input values. Do not log request bodies, upload contents, session tokens, user questions, or provider responses. Rate limiting is per connection IP, so configure a trusted edge proxy before a shared deployment. CORS is an exact allowlist supplied through `FINEPRINT_ORIGINS`.

Retrieval scores are lexical coverage in demo mode and cosine similarity in Chroma mode; thresholds must be calibrated separately. Low retrieval scores or no verified answer spans cause abstention. Nearest passages are labeled separately and may not answer the question.


# FinePrint input schema

CSV and XLSX use a header row. JSON uses an array of objects. Each row is one original section or paragraph. Limits: 5 MB and 400 rows; one document per upload.

| Field | Type | Rule |
|---|---|---|
| doc_id | string | Same on every row. Generated from the filename in fallback mode. |
| section_id | string | Unique within the file; generated r1, r2, etc. if absent. |
| text | string | Required, nonempty original passage; maximum 50,000 characters per row. |
| heading | string | Optional section name. |
| page | positive integer | Optional source page. |
| source_file | string | Optional original filename, never a path to open. |

Single-column fallback maps the column to text. `content`, `paragraph`, `clause`, or `body` also maps to text and produces an assumption notice. JSON strings are supported as paragraph rows. Empty files, mixed doc_ids, duplicate section_ids, invalid page values, and oversized files receive friendly errors. Backend identifiers must be strings. CSV and JSON should use UTF-8.

Examples and downloads are in `public/templates/`. Run `python scripts/seed.py` to reproduce them. The browser XLSX parser uses a row-limited read; the backend also guards expanded ZIP size. CSV formula-like strings are treated as text and never executed; no user-content spreadsheet export is provided.
