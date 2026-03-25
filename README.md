# Disney-Style Marketing Analytics Portfolio Projects

This repository contains 3 GitHub-ready analytics projects tailored for marketing analytics / subscriber growth roles:

1. **subscriber_churn_prediction** - churn scoring and retention segmentation
2. **marketing_funnel_analytics** - acquisition to conversion channel analytics
3. **cohort_retention_dashboard** - monthly retention and engagement tracking dashboard

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # mac/linux
# .venv\Scripts\activate   # windows
pip install -r requirements.txt
```

Run any project:

```bash
python subscriber_churn_prediction/src/generate_data.py
python subscriber_churn_prediction/src/train_model.py
python marketing_funnel_analytics/src/generate_data.py
python marketing_funnel_analytics/src/analyze_funnel.py
python cohort_retention_dashboard/src/generate_data.py
python cohort_retention_dashboard/src/build_dashboard_data.py
```

Optional dashboard:

```bash
streamlit run cohort_retention_dashboard/src/app.py
```
