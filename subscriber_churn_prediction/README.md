# Subscriber Churn Prediction

## What this project shows
- Builds a synthetic streaming subscriber dataset
- Engineers behavioral and lifecycle features
- Trains logistic regression and random forest churn models
- Produces churn scores and segment recommendations

## Files
- `src/generate_data.py` - creates realistic sample subscriber data
- `src/train_model.py` - trains model and exports predictions
- `sql/churn_feature_query.sql` - warehouse-style feature engineering SQL

## Run
```bash
python src/generate_data.py
python src/train_model.py
```
