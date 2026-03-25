from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(7)
dates = pd.date_range("2025-01-01", periods=120, freq="D")
channels = ["Paid Search", "Paid Social", "Affiliate", "Organic", "Bundle", "Email"]

rows = []
for dt in dates:
    seasonal = 1.0 + 0.15 * np.sin(dt.dayofyear / 18)
    for ch in channels:
        base_impressions = {
            "Paid Search": 140000,
            "Paid Social": 180000,
            "Affiliate": 90000,
            "Organic": 110000,
            "Bundle": 70000,
            "Email": 50000,
        }[ch]
        impressions = int(base_impressions * seasonal * rng.uniform(0.85, 1.15))
        ctr = {
            "Paid Search": 0.030,
            "Paid Social": 0.018,
            "Affiliate": 0.022,
            "Organic": 0.040,
            "Bundle": 0.028,
            "Email": 0.050,
        }[ch] * rng.uniform(0.9, 1.1)
        clicks = int(impressions * ctr)
        visits = int(clicks * rng.uniform(0.72, 0.92))
        trial_rate = {
            "Paid Search": 0.09,
            "Paid Social": 0.07,
            "Affiliate": 0.10,
            "Organic": 0.12,
            "Bundle": 0.16,
            "Email": 0.14,
        }[ch] * rng.uniform(0.85, 1.15)
        trials = int(visits * trial_rate)
        paid_rate = {
            "Paid Search": 0.44,
            "Paid Social": 0.36,
            "Affiliate": 0.40,
            "Organic": 0.48,
            "Bundle": 0.57,
            "Email": 0.52,
        }[ch] * rng.uniform(0.9, 1.1)
        paid = int(trials * paid_rate)
        spend = {
            "Paid Search": 11000,
            "Paid Social": 12500,
            "Affiliate": 7000,
            "Organic": 1500,
            "Bundle": 6000,
            "Email": 900,
        }[ch] * seasonal * rng.uniform(0.85, 1.15)
        retained_90d = int(paid * rng.uniform(0.72, 0.92))
        rows.append(
            [dt, ch, impressions, clicks, visits, trials, paid, round(spend, 2), retained_90d]
        )

out = pd.DataFrame(
    rows,
    columns=[
        "event_date",
        "channel",
        "impressions",
        "clicks",
        "landing_page_visits",
        "trial_starts",
        "paid_conversions",
        "marketing_spend",
        "retained_after_90d",
    ],
)
out.to_csv(DATA_DIR / "channel_performance.csv", index=False)
print(f"Saved dataset to {DATA_DIR / 'channel_performance.csv'}")
