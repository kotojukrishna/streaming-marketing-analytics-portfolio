from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

df = pd.read_csv(DATA_DIR / "subscriber_activity.csv", parse_dates=["cohort_month", "activity_month"])

cohort_sizes = (
    df[df["months_since_signup"] == 0]
    .groupby("cohort_month", as_index=False)["subscriber_id"]
    .nunique()
    .rename(columns={"subscriber_id": "cohort_size"})
)

retention = (
    df.groupby(["cohort_month", "months_since_signup"], as_index=False)
    .agg(active_subscribers=("subscriber_id", "nunique"), avg_watch_minutes=("watch_minutes", "mean"), avg_sessions=("sessions", "mean"))
    .merge(cohort_sizes, on="cohort_month", how="left")
)
retention["retention_rate"] = retention["active_subscribers"] / retention["cohort_size"]
retention["cohort_month"] = retention["cohort_month"].dt.strftime("%Y-%m")

retention.to_csv(DATA_DIR / "cohort_retention_summary.csv", index=False)
print(f"Saved dashboard dataset to {DATA_DIR / 'cohort_retention_summary.csv'}")
