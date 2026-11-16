"""
Offline build step: usage_data.csv -> data/*.parquet + data/meta.json.

    python build_data.py "W:/Portfolio Projects/1. Data-analysis-with-python-Projects/Usage_Analysis_of_Customers"

Each raw row is one customer's use of one feature on one day (sessions, minutes). Usernames are replaced with
"Customer 001" style labels, assigned in alphabetical order, so no personal handle ships with the app.
Feature name "Account Managment" is corrected to "Account Management".
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pandas as pd

DEFAULT_RAW = Path("W:/Portfolio Projects/1. Data-analysis-with-python-Projects/Usage_Analysis_of_Customers")
OUT = Path(__file__).parent / "data"


def main(raw: Path) -> None:
    OUT.mkdir(exist_ok=True)
    u = pd.read_csv(raw / "usage_data.csv", parse_dates=["Date"])
    raw_shape = list(u.shape)
    labels = {n: f"Customer {i:03d}" for i, n in enumerate(sorted(u["Username"].unique()), 1)}
    u["customer"] = u["Username"].map(labels)
    u["feature"] = u["Feature"].replace({"Account Managment": "Account Management"})
    u = u.rename(columns={"Date": "date", "Sessions": "sessions", "Time spent": "minutes"})
    u["month"] = u["date"].dt.to_period("M").dt.to_timestamp()
    rows = u[["date", "month", "customer", "feature", "sessions", "minutes"]]
    rows.to_parquet(OUT / "usage.parquet", index=False)
    rows.sample(50, random_state=7).sort_values("date").to_parquet(OUT / "sample_usage.parquet", index=False)

    meta = {
        "built": date.today().isoformat(),
        "raw_shape": raw_shape,
        "customers": int(u["customer"].nunique()),
        "features": sorted(u["feature"].unique().tolist()),
        "first": str(u["date"].min().date()),
        "last": str(u["date"].max().date()),
        "missing": int(u.isna().sum().sum()),
        "duplicates": int(u.duplicated().sum()),
        "fractional_minutes": int((u["minutes"] % 1 != 0).sum()),
        "avg_matches": bool(((u["Average time spent"] - u["minutes"] / u["sessions"]).abs() < 1e-6).all()),
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_RAW)
