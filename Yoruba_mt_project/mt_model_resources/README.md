# MT Model supplemental resources

This folder contains data extracted from the supplied MT Model notebooks.
It is an addition to the project, not a replacement for the application.

| Resource | Purpose | Used automatically by the live app? |
| --- | --- | --- |
| `../mt_model_data.py` | Tagged lexicon, pronouns, markers, and rule inventory in importable Python form | No |
| `source_notebooks/` | Original MT Model notebooks retained for traceability | No |
| `INTEGRATION_REPORT.md` | Compatibility decision and verification record | No |

The website continues to initialise `YorubaEnglishTranslator` with
`education_dataset`, exactly as before. The extra MT data is deliberately
separate until a future, explicitly tested dataset merge is approved.
