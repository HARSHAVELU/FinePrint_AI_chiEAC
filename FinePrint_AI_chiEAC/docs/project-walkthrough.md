# Project walkthrough

## Starting with the purpose of FinePrint AI

FinePrint AI brings the important parts of an everyday document into one place. I use a fictional rental lease to walk through the project, from the upload screen to the final action list. The main idea is to help a user find dates, costs, requirements, and unclear details while keeping the original source passage available for every finding.

## Opening the application

I start with the browser application, which is built with React, TypeScript, Vite, and Tailwind. The home screen gives me two ways to begin: upload my own structured file or select one of three built-in examples. There is also a preparation guide and downloadable templates. The standalone browser mode runs locally with deterministic rules and does not require a model API key.

## Uploading the sample document

For this walkthrough, I use FinePrint_Test_Rental_Lease.csv, the fictional sample included with the project. It contains 15 sections covering rent, a deposit, deadlines, tenant duties, repair responsibilities, and a defined term. The application accepts CSV, JSON, and XLSX files. Each row holds one original paragraph or section, with an identifier and optional heading and page number. Input checks enforce the 5 MB and 400-row limits and report invalid or missing fields.

## Processing the document

After upload, the application validates the rows, applies basic masking to supported personal-information patterns, and identifies the document family. For this sample, the expected family is housing. The section identifiers and page numbers stay attached to the text so findings can point back to their source. The browser engine extracts information with rules and matches questions to passages lexically. The separate Python backend organizes processing into typed LangGraph stages and includes optional Presidio, embedding, Chroma, and model adapters. Those production adapters still require validation.

## Reading the two main dashboard columns

The dashboard organizes the document into What this means and What you need to do. In browser mode, What this means presents the original text by section rather than generated paraphrases. What you need to do puts dated findings before other requirements. In the sample, I can see the November 2, 2026 acceptance deadline, the November 3 deposit deadline, and the November 4 document-submission deadline. This lets me move from a long document to a more organized view without losing the underlying wording.

## Checking a finding against its source

Each finding includes a source chip. When I open the chip for the acceptance deadline, the source dialog shows the relevant section, page, and highlighted passage. The confidence badge appears alongside the finding. This makes it possible to inspect the evidence directly. Quote verification checks whether the quoted passage occurs in the source; it does not independently prove every interpretation of that passage.

## Reviewing money obligations and terms

The Money panel brings together the amounts mentioned in the sample: $1,250 rent, a $900 security deposit, and a $40 late fee. The sample also mentions a $75 application fee, but explicitly waives it. That distinction remains visible so a mentioned amount is not automatically treated as a payment due. Watch out groups obligations such as tenant responsibilities and notice requirements. The Glossary panel includes the definition of security deposit stated in the document.

## Looking at missing or unclear information

The Missing or unclear panel compares verified passages with a checklist for the document family. The rental sample does not state pet rules or renewal terms, so the panel can raise questions about those details. I treat these entries as questions for the document sender. A missing checklist match is not proof that a rule or right does not exist, and broad keyword matching can sometimes flag information that needs a closer review.

## Asking questions about the document

The Ask panel lets me explore a specific detail without searching every section manually. For “When is rent due?”, the sample supports an answer with the passage stating November 5, 2026. For “What is the pet fee?”, the sample contains no stated pet fee, so the expected response is “Not stated in your document.” A nearest passage may appear separately, clearly distinguished from an answer. This is how the prototype makes missing evidence visible instead of filling the gap with an invented amount.

## Taking the action list away

The Print my to-do list control opens a print-friendly version of the actions. From the browser print view, the list can be printed or saved as a PDF. The number of pages depends on the source document and print settings. A user can then return to the dashboard to check a source or choose New document to clear the current document from the interface.

## Reviewing the implementation evidence

The project includes 36 passing backend tests, 6 passing browser-engine tests, and a successful frontend production build from the recorded engineering checks. The evaluation data consists of 30 closely related synthetic documents and 204 single-pass expected facts. These results support prototype regression checks, but they do not establish independent production accuracy, complete PII protection, or model-backed quality. This walkthrough shows the implemented workflow and the evidence available for reviewing it.
