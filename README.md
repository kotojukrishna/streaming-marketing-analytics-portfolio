# Streaming Marketing Analytics Portfolio

This repository contains 3 analytics portfolio projects designed around subscriber growth, retention, and marketing performance use cases commonly seen in streaming and subscription businesses.

## Projects Included

### 1. Subscriber Churn Prediction
Built a churn analysis workflow using Python and SQL to identify at-risk subscribers and segment churn risk by customer behavior patterns.

**What it covers:**
- Synthetic subscriber data generation
- Churn risk segmentation
- Model training and evaluation
- SQL feature engineering example

**Tech used:**
- Python
- pandas
- scikit-learn
- SQL

---

### 2. Marketing Funnel Analytics
Built a funnel analytics project to evaluate conversion performance, customer acquisition cost, retention quality, and estimated LTV/CAC across acquisition channels.

**What it covers:**
- Channel-level performance analysis
- Funnel conversion metrics
- CAC and retention analysis
- SQL KPI logic

**Tech used:**
- Python
- pandas
- SQL

---

### 3. Cohort Retention Dashboard
Built a Streamlit dashboard to analyze retention trends across subscriber cohorts and generate retention summaries.

**What it covers:**
- Cohort-based retention tracking
- Dashboard-ready dataset creation
- Streamlit app for visualization
- SQL cohort logic

**Tech used:**
- Python
- Streamlit
- pandas
- SQL

---

## Repository Structure

```bash
subscriber_churn_prediction/
marketing_funnel_analytics/
cohort_retention_dashboard/
README.md
requirements.txt

## Repository Structure

```bash
subscriber_churn_prediction/
marketing_funnel_analytics/
cohort_retention_dashboard/
README.md
requirements.txt


```markdown
## How to Run

### 1. Create and activate a virtual environment
```bash
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

2. Install dependencies
pip install -r requirements.txt
3. Run the projects
Subscriber Churn Prediction
python .\subscriber_churn_prediction\src\generate_data.py
python .\subscriber_churn_prediction\src\train_model.py
Marketing Funnel Analytics
python .\marketing_funnel_analytics\src\generate_data.py
python .\marketing_funnel_analytics\src\analyze_funnel.py
Cohort Retention Dashboard
python .\cohort_retention_dashboard\src\generate_data.py
python .\cohort_retention_dashboard\src\build_dashboard_data.py
streamlit run .\cohort_retention_dashboard\src\app.py
Business Value

These projects demonstrate how analytics can be used to:

identify churn drivers
improve subscriber retention
evaluate marketing channel quality
support lifecycle and growth decisions
communicate insights through dashboards and data storytelling
Author

Sai Krishna Kotoju


# Step 2: Check formatting before committing

Before you click commit, quickly check these things:

- every code block starts with:
```markdown
```bash
every code block ends with:

- the `Repository Structure` section has a closing triple backtick after `requirements.txt`

This is where people mess up markdown.

# Step 3: Scroll down

Go to the bottom of the GitHub edit page.

# Step 4: Add commit message

In the commit message box, type:

```text
Improve main README
Step 5: Commit changes

Click:

Commit changes
