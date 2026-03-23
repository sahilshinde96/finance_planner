# ARTH — ML Finance Planner Training Guide

## Folder structure

```
ml/
├── step1_generate_data.py   ← Creates 10,000 training samples
├── step2_train.py           ← Trains 3 ML models
├── step3_evaluate.py        ← Evaluation plots + metrics
├── step5_updated_views.py   ← Copy to backend/planner/views.py
├── ml_predictor.py          ← Copy to backend/planner/ml_predictor.py
├── requirements.txt         ← ML-specific packages
├── data/                    ← Generated after Step 1
│   └── finance_dataset.csv
├── models/                  ← Generated after Step 2
│   ├── preprocessor.pkl
│   ├── health_model.pkl
│   ├── risk_model.pkl
│   └── allocation_model.pkl
└── evaluation/              ← Generated after Step 3
    ├── model_evaluation.png
    └── metrics.txt
```

---

## Step-by-step

### 1. Install ML packages
```bash
cd ml
pip install -r requirements.txt
```

### 2. Generate training data (10,000 synthetic profiles)
```bash
python step1_generate_data.py
```
Creates: `data/finance_dataset.csv`

### 3. Train the three models
```bash
python step2_train.py
```
Creates: `models/preprocessor.pkl`, `models/health_model.pkl`,
         `models/risk_model.pkl`, `models/allocation_model.pkl`

Expected output:
- Health score: MAE ~4–6 points, R² ~0.85–0.92
- Risk class: Accuracy ~85–92%
- Allocation: MAE ~2–4% per asset class

### 4. Evaluate (optional but recommended)
```bash
python step3_evaluate.py
```
Creates: `evaluation/model_evaluation.png` with 6 plots

### 5. Deploy to Django

Copy two files into the backend:
```bash
cp ml_predictor.py ../backend/planner/ml_predictor.py
cp step5_updated_views.py ../backend/planner/views.py
```

Also copy the `models/` folder to `backend/planner/`:
```bash
cp -r models/ ../backend/planner/models/
```

The view will automatically use ML models if they exist,
or fall back to the rule-based engine if not.

---

## What the 3 models predict

| Model | Algorithm | Target | Performance goal |
|-------|-----------|--------|-----------------|
| Health score | Random Forest Regressor | 0–100 score | MAE < 5 |
| Risk class | Gradient Boosting Classifier | low/medium/high | Accuracy > 85% |
| Asset allocation | Multi-output Random Forest | equity/debt/gold/liquid % | MAE < 3% |

---

## Improving accuracy

### Option A — Collect real user data
Replace synthetic data with anonymised real user profiles + financial advisor labels.
Even 500 real labelled samples dramatically improves accuracy.

### Option B — Tune hyperparameters
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [8, 12, 16],
    'min_samples_leaf': [3, 5, 10],
}
grid = GridSearchCV(RandomForestRegressor(), param_grid, cv=5, scoring='neg_mean_absolute_error')
grid.fit(X_tr, y_health_tr)
print(grid.best_params_)
```

### Option C — Add more features
- Income growth rate (current vs 2 years ago)
- Existing investments (MF, FD, PF balance)
- Credit score
- Location (metro vs tier-2 vs rural affects cost of living)

### Option D — Use XGBoost (usually better)
```bash
pip install xgboost
```
```python
from xgboost import XGBRegressor
health_model = XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=6)
```
