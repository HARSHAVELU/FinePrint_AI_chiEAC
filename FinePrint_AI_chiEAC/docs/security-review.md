# API security review checklist

This is an implementation review, not an external penetration test or a certification against a current OWASP release.

| Area | Implemented control | Remaining verification |
|---|---|---|
| Session access | Random unguessable session capability; no session listing | Host TLS, token leakage checks, origin isolation |
| Resource limits | 5 MB, 400 rows, 30 requests/minute/IP, 100 sessions, two analysis tasks | Enforce streaming limits and trusted proxy configuration |
| Input validation | Pydantic fields; duplicate ID checks; file extension allowlist | Fuzz malformed XLSX and archive edge cases |
| Data minimization | Memory-only sessions; expiry; no app content logging | Inspect host logs, crash dumps, provider policies |
| Prompt injection | Static system instruction; JSON data; no tools; quote checks | Broader adaptive attacks in actual model mode |
| Error handling | Generic unexpected error; validation input suppressed | Provider failure/load tests |
| Dependencies | Build lockfile and reproducible environment snapshot | Registry vulnerability review and upgrades |
| Browser rendering | React text interpolation; no dangerous HTML | Deployed CSP, accessibility audit |
| Configuration | No client provider key; tracing forced off | Host secret rotation and monthly spending cap |
| Third-party output | Typed output and quote validation | Independent entailment and hallucination audits |

Do not upload real private documents to connected mode until the remaining privacy and provider checks are done.
