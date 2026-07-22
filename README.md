# STR Investment Lab

Open-source analytics toolkit for evaluating short-term rental acquisitions.

This project is designed as both a practical investment model and a portfolio-grade data product. It demonstrates data engineering, data wrangling, real estate finance, API integration, predictive modeling, and deployable Python software design.

## Why This Exists

The core question:

> Can a short-term rental investment produce attractive risk-adjusted returns, while also creating tax-relevant depreciation scenarios that should be reviewed with a CPA?

The tool models:

- Purchase price, down payment, credit-score-driven financing assumptions, and closing costs
- AirDNA-style revenue metrics such as ADR, occupancy, and annual revenue
- Operating expenses, cleaning fees, property management, utilities, repairs, insurance, taxes, and HOA
- Debt service, cash flow, cash-on-cash return, cap rate, DSCR, and breakeven occupancy
- Sensitivity matrices across down payments, credit scores, and confidence levels
- Cost segregation and accelerated depreciation scenarios
- Optional machine learning models for revenue prediction and market scoring

## Compliance-First Data Strategy

Real estate data is fragmented and heavily licensed. This project avoids scraping and uses lawful data sources only.

Recommended ingestion order:

1. **AirDNA Enterprise API** for STR revenue metrics, comps, occupancy, and ADR.
2. **Zillow Group / Bridge Interactive APIs** where you have approved access to MLS, public records, Zestimates, or related datasets.
3. **Public/open data** such as Census, FRED, local tax assessor exports, tourism data, and zoning datasets.
4. **Manual CSV imports** for early development and demos.

Redfin and many consumer-facing portals restrict automated crawling or scraping. Do not build this project around prohibited scraping.

## Current Tax Modeling Assumption

This software is not tax advice. It only models scenarios to discuss with a CPA.

For high-income W-2 households, passive activity rules are the key constraint. Short-term rentals may be treated differently from ordinary rental real estate when the average customer stay is short and the taxpayer materially participates, but facts and documentation matter. The tax module therefore marks depreciation benefits as `review_required` unless the user explicitly supplies participation assumptions.

## Project Structure

```text
src/str_investment_lab/
  data_sources/       API client boundaries and mock providers
  models.py           Domain data structures
  underwriting.py     Property-level investment calculations
  sensitivity.py      Matrix generation across assumptions
  tax.py              CPA-review depreciation scenario helpers
  ml.py               Optional ensemble model wrapper
  cli.py              Command-line demo entrypoint
tests/                Unit tests
docs/                 Portfolio and architecture notes
```

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,ml]"
python -m str_investment_lab.cli --sample
str-investment-lab analyze-csv data/sample_properties.csv
python -m unittest discover -s tests
```

The core library is pure Python. Optional dependencies are used for API calls, notebooks, and machine learning.

## Roadmap

- Add real AirDNA Enterprise API integration
- Add Bridge/Zillow approved API integration
- Add SQLite/Postgres persistence layer
- Add Google Cloud Storage export layer
- Add dbt-style transformations or SQLModel models
- Add FastAPI service
- Add Streamlit or React dashboard
- Add CI, Docker, typed config, and deployment artifacts
