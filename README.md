# Epstien-s-scraper
Epstein Emails Corpus Linguistics Analysis
By Ameen

## About

This project scrapes, cleans, annotates, and analyzes Jeffrey Epstein's publicly released emails (via FOIA) to investigate the use of **coded language, food-item euphemisms, and pragmatic strategies** found in the correspondence. The pipeline prepares the corpus for analysis using **AntConc** and **Voyant Tools**.

## Pipeline

| Step | Script | Description |
|------|--------|-------------|
| 1 | `step1_scrape.py` | Scrapes emails from jmail.world API using keyword queries |
| 2 | `step2_sanitize.py` | Cleans HTML, redactions, duplicates, and short entries |
| 3 | `step3_pos_tag.py` | POS-tags the corpus and flags coded language (food items, euphemisms) |
| 4 | `step4_export.py` | Exports corpus for AntConc, Voyant, and generates a flagged terms report |

## Output Files

| File | Purpose |
|------|---------|
| `epstein_raw_data.json` | Raw scraped emails |
| `epstein_clean_data.json` | Sanitized corpus |
| `epstein_annotated.json` | POS-tagged and flagged corpus |
| `corpus_antconc/` | Individual `.txt` files per email (open as directory in AntConc) |
| `corpus_voyant.txt` | Combined corpus file (upload to Voyant Tools) |
| `corpus_pos_tagged.txt` | Word/TAG formatted corpus for linguistic analysis |
| `flagged_terms_report.txt` | Summary of detected coded language |

## How to Run

```bash
pip install requests nltk
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger'); nltk.download('averaged_perceptron_tagger_eng')"

python step1_scrape.py
python step2_sanitize.py
python step3_pos_tag.py
python step4_export.py
```

## Tools Used

- **Python** (requests, NLTK) for scraping, cleaning, and POS tagging
- **AntConc** for concordance, collocates, n-grams, and keyword analysis
- **Voyant Tools** for word frequency, trends, and corpus visualization

## Data Source

Emails sourced from [jmail.world](https://jmail.world), which hosts publicly released Epstein documents from FOIA requests and court filings.
