# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "pandas"]
# ///

"""
Download Cambridge Property Database (FY2016–FY2026) from the Cambridge Open Data Portal.
Selects only the columns needed for neighborhood-level assessment analysis.
Caches to data/raw/ and skips download if already present.
"""

from io import StringIO
from pathlib import Path
import requests
import pandas as pd

CACHE = Path(__file__).parent.parent / "data/raw/cambridge_property_assessments.csv"
URL = "https://data.cambridgema.gov/resource/eey2-rv59.csv"
COLUMNS = (
    "pid,gisid,address,latitude,longitude,"
    "stateclasscode,propertyclass,yearofassessment,"
    "assessedvalue,buildingvalue,landvalue,"
    "interior_numunits,interior_livingarea,"
    "condition_yearbuilt,landarea,"
    "residentialexemption,"
    "saleprice,saledate"
)
PAGE = 50_000


def fetch_all() -> pd.DataFrame:
    frames, offset = [], 0
    while True:
        print(f"  fetching rows {offset}–{offset + PAGE - 1}...")
        r = requests.get(
            URL,
            params={
                "$select": COLUMNS,
                "$order": "pid,yearofassessment",
                "$limit": PAGE,
                "$offset": offset,
            },
            timeout=120,
        )
        r.raise_for_status()
        chunk = pd.read_csv(StringIO(r.text))
        frames.append(chunk)
        if len(chunk) < PAGE:
            break
        offset += PAGE
    return pd.concat(frames, ignore_index=True)


def main() -> None:
    if CACHE.exists():
        print(f"Cache hit: {CACHE}")
        df = pd.read_csv(CACHE)
        print(f"  {len(df):,} rows")
        print(f"  assessment years: {sorted(df['yearofassessment'].dropna().astype(int).unique())}")
        print(f"  state class codes: {sorted(df['stateclasscode'].dropna().astype(int).unique())}")
        return

    print("Downloading Cambridge Property Database (FY2016–FY2026)...")
    df = fetch_all()
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CACHE, index=False)
    print(f"Saved {len(df):,} rows → {CACHE}")
    print(f"Assessment years: {sorted(df['yearofassessment'].dropna().astype(int).unique())}")
    state_codes = sorted(df['stateclasscode'].dropna().astype(int).unique())
    print(f"State class codes ({len(state_codes)} unique): {state_codes}")
    missing_coords = df[['latitude', 'longitude']].isna().any(axis=1).sum()
    print(f"Rows missing lat/lon: {missing_coords:,}")


if __name__ == "__main__":
    main()
