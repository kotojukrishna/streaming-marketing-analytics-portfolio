from __future__ import annotations

from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

df = pd.read_csv(DATA_DIR / "subscribers.csv")

features = [
    "plan_type",
    "region",
    "acquisition_channel",
    "monthly_price",
    "promo_applied",
    "watch_minutes_30d",
    "active_days_30d",
    "titles_watched_30d",
    "sports_view_share",
    "kids_view_share",
    "drama_view_share",
    "customer_service_tickets_90d",
    "payment_failures_90d",
    "days_since_last_watch",
    "tenure_months",
]
target = "churned"

X = df[features]
y = df[target]

num_cols = [c for c in features if X[c].dtype != "object"]
cat_cols = [c for c in features if X[c].dtype == "object"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", Pipeline([("scaler", StandardScaler())]), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ]
)

models = {
    "logistic_regression": LogisticRegression(max_iter=1000),
    "random_forest": RandomForestClassifier(n_estimators=250, max_depth=8, random_state=42),
}

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

best_name = None
best_auc = -1.0
best_pipeline = None

for name, model in models.items():
    pipeline = Pipeline([("preprocessor", preprocessor), ("model", model)])
    pipeline.fit(X_train, y_train)
    probs = pipeline.predict_proba(X_test)[:, 1]
    preds = (probs >= 0.5).astype(int)
    auc = roc_auc_score(y_test, probs)
    print(f"\n{name} ROC-AUC: {auc:.4f}")
    print(classification_report(y_test, preds))

    if auc > best_auc:
        best_auc = auc
        best_name = name
        best_pipeline = pipeline

scored = df.copy()
scored["churn_probability"] = best_pipeline.predict_proba(X)[:, 1]
scored["risk_segment"] = pd.cut(
    scored["churn_probability"],
    bins=[-0.01, 0.30, 0.60, 1.0],
    labels=["Low", "Medium", "High"],
)

scored.to_csv(DATA_DIR / "churn_scored_subscribers.csv", index=False)
summary = (
    scored.groupby("risk_segment", observed=False)
    .agg(subscribers=("subscriber_id", "count"), avg_watch_minutes=("watch_minutes_30d", "mean"), actual_churn_rate=("churned", "mean"))
    .reset_index()
)
summary.to_csv(DATA_DIR / "risk_segment_summary.csv", index=False)

print(f"\nBest model: {best_name} with ROC-AUC {best_auc:.4f}")
print(f"Saved scored file to {DATA_DIR / 'churn_scored_subscribers.csv'}")
print(summary)
