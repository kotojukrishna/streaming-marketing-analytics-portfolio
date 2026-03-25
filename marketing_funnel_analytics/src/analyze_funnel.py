from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

df = pd.read_csv(DATA_DIR / "channel_performance.csv", parse_dates=["event_date"])

summary = (
    df.groupby("channel", as_index=False)
    .agg(
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        visits=("landing_page_visits", "sum"),
        trial_starts=("trial_starts", "sum"),
        paid_conversions=("paid_conversions", "sum"),
        marketing_spend=("marketing_spend", "sum"),
        retained_after_90d=("retained_after_90d", "sum"),
    )
)
summary["ctr"] = summary["clicks"] / summary["impressions"]
summary["visit_rate"] = summary["visits"] / summary["clicks"]
summary["trial_start_rate"] = summary["trial_starts"] / summary["visits"]
summary["trial_to_paid_rate"] = summary["paid_conversions"] / summary["trial_starts"]
summary["cac"] = summary["marketing_spend"] / summary["paid_conversions"]
summary["retention_90d_rate"] = summary["retained_after_90d"] / summary["paid_conversions"]
summary["estimated_ltv_to_cac"] = (summary["retained_after_90d"] * 18.0) / summary["marketing_spend"]

summary = summary.sort_values(["estimated_ltv_to_cac", "paid_conversions"], ascending=[False, False])
summary.to_csv(DATA_DIR / "funnel_summary_by_channel.csv", index=False)

monthly = df.copy()
monthly["month"] = monthly["event_date"].dt.to_period("M").astype(str)
monthly_summary = (
    monthly.groupby(["month", "channel"], as_index=False)
    .agg(
        visits=("landing_page_visits", "sum"),
        trial_starts=("trial_starts", "sum"),
        paid_conversions=("paid_conversions", "sum"),
        spend=("marketing_spend", "sum"),
    )
)
monthly_summary.to_csv(DATA_DIR / "monthly_funnel_summary.csv", index=False)

print("Saved:")
print(DATA_DIR / "funnel_summary_by_channel.csv")
print(DATA_DIR / "monthly_funnel_summary.csv")
print("\nTop channels:")
print(summary[["channel", "paid_conversions", "cac", "retention_90d_rate", "estimated_ltv_to_cac"]].head())
