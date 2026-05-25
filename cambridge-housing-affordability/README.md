# Cambridge Housing Affordability — Data and Analysis

Supporting notebooks for the Cambridge housing affordability post. These notebooks reproduce all charts and statistics cited in the piece, using public City of Cambridge and federal data.

Please report errors.

## Notebooks

### [`notebooks/02_property_assessments.ipynb`](notebooks/02_property_assessments.ipynb)

Choropleth maps and analysis of assessed residential property values across Cambridge's thirteen CDD neighborhoods (FY2026 assessment roll).

**Scope:** The residential dataset focuses on ~47,200 housing units across ~21,600 privately-owned properties. This _includes_ ~1,600 deed-restricted inclusionary zoning (IZ) units and ~150 scattered-site homeownership units, which are assessed under standard residential codes. It **excludes** ~2,800 public housing units (Cambridge Housing Authority), university-owned housing (Harvard, MIT, Lesley, etc.), and other institutionally-owned dwellings on tax-exempt land. The city's total housing stock is 58,966 units (CDD Land Use Data, June 2025). As such, this analysis focuses on market-accessible units, even though IZ and Affordable units are deed-restricted and not market-rate. This is a intentional decision and should be kept in mind when assessing this data.

| Section | Output |
|---|---|
| % single-family homes (by units) | `data/out/pct_sfh_map.png` |
| % single-family homes (by structure) | `data/out/pct_sfh_structures_map.png` |

### [`notebooks/04_housing_affordability.ipynb`](notebooks/04_housing_affordability.ipynb)

Cambridge housing affordability indicators: median home price by property type, price-to-income ratios, Zillow ZHVI cross-check, residential property mix, and net housing starts per 1,000 households (1996-2025). All dollar figures in 2024 CPI-U-adjusted dollars.

| Section | Output |
|---|---|
| Net housing units per 1k households (bar chart) | `data/out/housing_starts_per_1k.png` |

## Setup

Requires Python 3.9+ and [uv](https://docs.astral.sh/uv/).

```bash
# Fetch the property assessments dataset (~33 MB, paginated Socrata API).
# Re-run to refresh; the file's modification timestamp records the fetch date.
uv run scripts/fetch_property_assessments.py

# Launch the notebooks
uv run jupyter notebook notebooks/
```

Then open either notebook in the browser and run cells top to bottom.

## Data sources

| File | Source | Notes |
|---|---|---|
| `data/raw/CDD_Neighborhoods.geojson` | [cambridgegis/cambridgegis_data](https://github.com/cambridgegis/cambridgegis_data/tree/main/Boundary/CDD_Neighborhoods) | CDD neighborhood boundaries |
| `data/raw/cambridge_housing_permits_curated.csv` | City of Cambridge Open Data Portal, "Housing Starts 1996-Present" | Hand-corrected; excludes 221 Mt Auburn St (-63 units, 2025 exceptional demolition) and fixes duplicate/mis-attributed records in the raw export |
| `data/raw/cambridge_property_assessments.csv` | Cambridge Assessing, [Property Database FY2016-FY2026](https://data.cambridgema.gov/Assessing/Cambridge-Property-Database-FY2016-FY2026/eey2-rv59/about_data) (Socrata) | **Not committed** (~33 MB). Fetched via `scripts/fetch_property_assessments.py` |
| `data/raw/City_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv` | [Zillow Research](https://www.zillow.com/research/data/), ZHVI SFR+Condo, middle tier, smoothed/seasonally adjusted | Trimmed to 7 Boston-area cities |
| `data/raw/ACSST1Y2024.S1901-2026-05-19T234744.csv` | U.S. Census Bureau, ACS 1-Year 2024, Table S1901 | Cambridge city, Middlesex County, MA |
| `data/raw/cpi_u_annual.csv` | U.S. Bureau of Labor Statistics, Series CUUR0000SA0 | Annual averages, 1996-2024 |
| *(hardcoded in notebook)* | Cambridge CDD, [Affordable Housing Distribution by Neighborhood (Jan 2026)](https://www.cambridgema.gov/CDD/News/2026/01/-/media/583FC7CE9E384FCEA1042F0C09FB99C0.ashx) | Total housing units by neighborhood (58,966 citywide); used as part of SFH choropleth denominator |
