from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

st.set_page_config(page_title="Cohort Retention Dashboard", layout="wide")
st.title("Streaming Subscriber Cohort Retention Dashboard")

summary_path = DATA_DIR / "cohort_retention_summary.csv"
if not summary_path.exists():
    st.error("Run generate_data.py and build_dashboard_data.py first.")
    st.stop()

retention = pd.read_csv(summary_path)
cohorts = sorted(retention["cohort_month"].unique())
selected = st.multiselect("Select cohorts", cohorts, default=cohorts[-4:])
filtered = retention[retention["cohort_month"].isin(selected)]

st.subheader("Retention Trend")
pivot = filtered.pivot(index="months_since_signup", columns="cohort_month", values="retention_rate")
st.line_chart(pivot)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Average Watch Minutes")
    watch_pivot = filtered.pivot(index="months_since_signup", columns="cohort_month", values="avg_watch_minutes")
    st.line_chart(watch_pivot)
with col2:
    st.subheader("Average Sessions")
    sessions_pivot = filtered.pivot(index="months_since_signup", columns="cohort_month", values="avg_sessions")
    st.line_chart(sessions_pivot)

st.subheader("Underlying Data")
st.dataframe(filtered, use_container_width=True)
