from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(42)
N = 5000

plan_types = ["Basic", "Standard", "Premium"]
regions = ["US", "Canada", "LATAM"]
channels = ["Paid Search", "Paid Social", "Affiliate", "Organic", "Bundle"]

plan = rng.choice(plan_types, size=N, p=[0.35, 0.45, 0.20])
region = rng.choice(regions, size=N, p=[0.7, 0.15, 0.15])
channel = rng.choice(channels, size=N, p=[0.20, 0.18, 0.12, 0.25, 0.25])
promo_applied = rng.binomial(1, 0.42, N)
monthly_price = np.select(
    [plan == "Basic", plan == "Standard", plan == "Premium"],
    [7.99, 12.99, 18.99],
)
tenure_months = np.clip(rng.normal(16, 10, N).round(), 1, 60).astype(int)
watch_minutes_30d = np.clip(rng.normal(850, 420, N), 0, None).round().astype(int)
active_days_30d = np.clip((watch_minutes_30d / 90) + rng.normal(0, 3, N), 0, 30).round().astype(int)
titles_watched_30d = np.clip((watch_minutes_30d / 120) + rng.normal(0, 2, N), 0, None).round().astype(int)
sports_view_share = np.clip(rng.beta(2, 8, N), 0, 1)
kids_view_share = np.clip(rng.beta(2, 6, N), 0, 1)
drama_view_share = np.clip(rng.beta(3, 5, N), 0, 1)
customer_service_tickets_90d = rng.poisson(0.4, N)
payment_failures_90d = rng.binomial(2, 0.08, N)
days_since_last_watch = np.clip(rng.normal(6, 7, N), 0, 45).round().astype(int)

logit = (
    -2.0
    + 0.9 * (watch_minutes_30d < 300)
    + 0.7 * (active_days_30d <= 3)
    + 0.8 * (days_since_last_watch > 14)
    + 0.6 * (payment_failures_90d > 0)
    + 0.25 * (customer_service_tickets_90d >= 2)
    - 0.3 * (plan == "Premium")
    - 0.2 * (channel == "Bundle")
    - 0.15 * (tenure_months > 24)
    + 0.18 * promo_applied
)
prob = 1 / (1 + np.exp(-logit))
churned = rng.binomial(1, prob)

signup_offsets = rng.integers(30, 900, N)
signup_date = pd.Timestamp("2024-12-31") - pd.to_timedelta(signup_offsets, unit="D")

out = pd.DataFrame(
    {
        "subscriber_id": range(100001, 100001 + N),
        "signup_date": signup_date,
        "plan_type": plan,
        "region": region,
        "acquisition_channel": channel,
        "monthly_price": monthly_price,
        "promo_applied": promo_applied,
        "watch_minutes_30d": watch_minutes_30d,
        "active_days_30d": active_days_30d,
        "titles_watched_30d": titles_watched_30d,
        "sports_view_share": sports_view_share.round(3),
        "kids_view_share": kids_view_share.round(3),
        "drama_view_share": drama_view_share.round(3),
        "customer_service_tickets_90d": customer_service_tickets_90d,
        "payment_failures_90d": payment_failures_90d,
        "days_since_last_watch": days_since_last_watch,
        "tenure_months": tenure_months,
        "churned": churned,
    }
)

out.to_csv(DATA_DIR / "subscribers.csv", index=False)
print(f"Saved {len(out)} rows to {DATA_DIR / 'subscribers.csv'}")
