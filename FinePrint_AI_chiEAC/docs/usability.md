# Usability test protocol and observations

## Engineering inspection

The browser preview was opened and the lease dashboard checked. The interface exposes sample selection, date sorting, costs, source chips, missing details, Q&A, and print. This engineering inspection is not one of the five non-technical usability sessions required by the brief. Responsive CSS includes a single-column mobile layout, labeled controls, focus outlines, a skip link, and keyboard-trapped dialogs; these implementations do not establish a Lighthouse score.

## Required sessions

Ask five people who did not build this app: “Open this document and tell me the first deadline.” Start timing when they see the upload screen. Stop when they correctly identify the deadline and source. Do not coach. Use a synthetic sample, collect no sensitive user documents, and record consent for any recording.

| Tester | Device | Correct date | Seconds | Main confusion | Fix and retest |
|---|---|---|---|---|---|
| 1 | Pending | Pending | Pending | Pending | Pending |
| 2 | Pending | Pending | Pending | Pending | Pending |
| 3 | Pending | Pending | Pending | Pending | Pending |
| 4 | Pending | Pending | Pending | Pending | Pending |
| 5 | Pending | Pending | Pending | Pending | Pending |

Gate 3 requires all five below 60 seconds and Lighthouse accessibility at least 90 on the deployed page. No human timing or Lighthouse score is claimed. Fix the three most frequent confusions, rerun on mobile, and record the build version.
