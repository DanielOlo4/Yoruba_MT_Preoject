# Yorùbá–English Translation System

## Project structure

| File | Role |
| --- | --- |
| `app.py`, `translator.py`, `unified_pipeline.py` | Flask routes, public translator interface and live translation pipeline |
| `clause_transfer.py`, `english_morphology_rules.py`, `yoruba_verb_grammar.py` | English inflection analysis, phrase transfer, Yorùbá tense, aspect, polarity and verb valency |
| `yoruba_english_education_dataset.py` | Domain-specific bilingual sentence pairs for school and classroom communication |
| `yoruba_lexicon.py`, `yoruba_curated_pos_lexicon.csv` | Curated lexical entries and a reviewable export with POS, domain, register and tone pattern |
| `yoruba_english_rule_based_lexicon.csv` | Extended bilingual dictionary with POS per lexical sense |
| `build_verb_form_inventory.py`, `yoruba_english_verb_forms.csv` | Regenerates and stores the English inflection and Yorùbá verb form inventory |
| `INTEGRATION_REPORT.md` | Rule table, examples, sources and implementation limits |

Translation uses exact matches first, followed by controlled clause transfer for supported English input, then fuzzy matching and lexical fallback. The translation API returns rule names in `rules_applied`. Run `python build_verb_form_inventory.py` after changing the extended dictionary or controlled verb entries.

## Test on Windows PowerShell

```powershell
cd "C:\path\to\Yoruba_mt_project"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py app.py
```

Open `http://127.0.0.1:5000` in a browser. Stop the test server with `Ctrl + C`.

## Start without PowerShell

Double-click `run_windows.bat` in the extracted project folder. The first start
creates the Python environment and installs the required packages. Later starts
open the web application automatically. Keep the small server window open while
using the website; close it or press `Ctrl + C` to stop the server.

To check the server in a second PowerShell window:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/health
```

## Deploy online

Use a Python host that supports Gunicorn, such as Render, Railway, or a Linux virtual server.

| Setting | Value |
| --- | --- |
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn --workers 2 --bind 0.0.0.0:$PORT app:app` |
| Health check path | `/api/health` |

The app uses the host's `PORT` automatically. Do not use `127.0.0.1` as the production host address.
