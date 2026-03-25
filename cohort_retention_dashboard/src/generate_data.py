from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(21)
cohort_months = pd.date_range("2024-01-01", periods=12, freq="MS")
rows = []
subscriber_id = 200000

for cohort in cohort_months:
    cohort_size = int(rng.integers(700, 1300))
    base_retention = rng.uniform(0.80, 0.88)
    for _ in range(cohort_size):
        subscriber_id += 1
        survived = True
        engagement_base = rng.uniform(180, 900)
        for month_idx in range(0, 7):
            activity_month = cohort + pd.DateOffset(months=month_idx)
            if month_idx == 0:
                active = True
            else:
                retention_prob = max(0.25, base_retention - month_idx * rng.uniform(0.05, 0.08))
                active = survived and (rng.random() < retention_prob)
            if not active:
                survived = False
                continue
            watch_minutes = max(0, int(rng.normal(engagement_base * (0.96 ** month_idx), 110)))
            sessions = max(1, int(rng.normal(9 * (0.93 ** month_idx), 2)))
            rows.append(
                [subscriber_id, cohort, activity_month, month_idx, watch_minutes, sessions]
            )

out = pd.DataFrame(
    rows,
    columns=[
        "subscriber_id",
        "cohort_month",
        "activity_month",
        "months_since_signup",
        "watch_minutes",
        "sessions",
    ],
)
out.to_csv(DATA_DIR / "subscriber_activity.csv", index=False)
print(f"Saved {len(out)} activity records to {DATA_DIR / 'subscriber_activity.csv'}")
