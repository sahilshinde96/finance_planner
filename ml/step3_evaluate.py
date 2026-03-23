"""
ARTH ML Finance Planner — Step 3: Evaluate Models
Run: python step3_evaluate.py
Output: evaluation/  (plots + metrics report)
"""
import os, pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # headless
import matplotlib.pyplot as plt
from sklearn.metrics import (
    mean_absolute_error, r2_score, accuracy_score,
    confusion_matrix, ConfusionMatrixDisplay
)
from sklearn.model_selection import cross_val_score

os.makedirs('evaluation', exist_ok=True)

# ── Load models + data ────────────────────────────────────────────────────────
print("📂 Loading models and data...")
df = pd.read_csv('data/finance_dataset.csv')

with open('models/preprocessor.pkl', 'rb') as f:
    prep_data = pickle.load(f)
preprocessor = prep_data['preprocessor']
feature_cols = prep_data['feature_cols']

with open('models/health_model.pkl', 'rb') as f:
    health_model = pickle.load(f)

with open('models/risk_model.pkl', 'rb') as f:
    risk_data = pickle.load(f)
risk_model = risk_data['model']
le = risk_data['label_encoder']

with open('models/allocation_model.pkl', 'rb') as f:
    alloc_data = pickle.load(f)
alloc_model = alloc_data['model']

# Additional derived columns
df['is_rented'] = (df['housing'] == 'rented').astype(int)
for col in ['has_emergency_fund', 'has_health_insurance', 'has_life_insurance']:
    df[col] = df[col].astype(int)

X_all = preprocessor.transform(df[feature_cols])
X_te  = X_all[8000:]
df_te = df.iloc[8000:].copy()

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('ARTH Finance Planner — Model Evaluation', fontsize=15, fontweight='bold')

# ── Plot 1: Health score predicted vs actual ──────────────────────────────────
ax = axes[0, 0]
y_true  = df_te['health_score'].values
y_pred  = health_model.predict(X_te)
mae     = mean_absolute_error(y_true, y_pred)
r2      = r2_score(y_true, y_pred)
ax.scatter(y_true, y_pred, alpha=0.3, s=8, color='steelblue')
ax.plot([0, 100], [0, 100], 'r--', linewidth=1.2, label='Perfect')
ax.set_xlabel('Actual health score')
ax.set_ylabel('Predicted health score')
ax.set_title(f'Health Score  (MAE={mae:.1f}, R²={r2:.3f})')
ax.legend()
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# ── Plot 2: Health score error distribution ───────────────────────────────────
ax = axes[0, 1]
errors = y_pred - y_true
ax.hist(errors, bins=50, color='steelblue', edgecolor='white', linewidth=0.5)
ax.axvline(0, color='red', linewidth=1.5, linestyle='--')
ax.set_xlabel('Prediction error (predicted − actual)')
ax.set_ylabel('Count')
ax.set_title(f'Health Score Error  (mean={errors.mean():.2f}, std={errors.std():.2f})')

# ── Plot 3: Risk confusion matrix ─────────────────────────────────────────────
ax = axes[0, 2]
y_risk_true = le.transform(df_te['risk_class'].values)
y_risk_pred = risk_model.predict(X_te)
cm = confusion_matrix(y_risk_true, y_risk_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)
disp.plot(ax=ax, colorbar=False, cmap='Blues')
acc = accuracy_score(y_risk_true, y_risk_pred)
ax.set_title(f'Risk Classification  (Accuracy={acc*100:.1f}%)')

# ── Plot 4: Feature importance (health model) ─────────────────────────────────
ax = axes[1, 0]
cat_feature_names = list(
    preprocessor.named_transformers_['cat']
    .get_feature_names_out(['risk_appetite'])
)
all_feat_names = [
    'age', 'income', 'rent', 'food', 'transport', 'utilities',
    'emi', 'other', 'dependents', 'emerg_fund', 'health_ins', 'life_ins',
    'savings_rate', 'emi_ratio', 'disposable', 'annual_inc', 'yrs_retire', 'is_rented'
] + cat_feature_names

imp = pd.Series(health_model.feature_importances_, index=all_feat_names).nlargest(10)
ax.barh(imp.index, imp.values, color='steelblue')
ax.set_xlabel('Feature importance')
ax.set_title('Top 10 Features (health model)')
ax.invert_yaxis()

# ── Plot 5: Allocation MAE per asset class ────────────────────────────────────
ax = axes[1, 1]
ALLOC_COLS = ['equity_pct', 'debt_pct', 'gold_pct', 'liquid_pct']
y_alloc_te = df_te[ALLOC_COLS].values
pred_alloc  = alloc_model.predict(X_te)
pred_alloc  = pred_alloc / pred_alloc.sum(axis=1, keepdims=True) * 100
maes = [mean_absolute_error(y_alloc_te[:, i], pred_alloc[:, i]) for i in range(4)]
colors = ['#e8593c', '#3b8bd4', '#efb520', '#1e9e75']
ax.bar(ALLOC_COLS, maes, color=colors)
ax.set_ylabel('MAE (%)')
ax.set_title('Allocation Model MAE per Asset Class')

# ── Plot 6: Sample predictions showcase ───────────────────────────────────────
ax = axes[1, 2]
sample = df_te.sample(5, random_state=7)
X_sample = preprocessor.transform(sample[feature_cols])
h_pred  = health_model.predict(X_sample)
alloc_p = alloc_model.predict(X_sample)
alloc_p = alloc_p / alloc_p.sum(axis=1, keepdims=True) * 100

y_pos   = np.arange(5)
ax.barh(y_pos, h_pred, color='steelblue', alpha=0.8)
ax.barh(y_pos, sample['health_score'].values, color='orange', alpha=0.6, label='Actual')
ax.set_yticks(y_pos)
ax.set_yticklabels([f"P{i+1}" for i in range(5)])
ax.set_xlabel('Health score')
ax.set_title('5 Sample Predictions vs Actual')
ax.legend()

plt.tight_layout()
plt.savefig('evaluation/model_evaluation.png', dpi=140, bbox_inches='tight')
print("📊 Evaluation plot saved → evaluation/model_evaluation.png")

# ── Text metrics report ───────────────────────────────────────────────────────
report = f"""
ARTH Finance Planner — ML Model Evaluation Report
=================================================

MODEL 1: Financial Health Score (Random Forest Regressor)
  MAE  : {mean_absolute_error(y_true, y_pred):.2f} points
  R²   : {r2_score(y_true, y_pred):.4f}
  Interpretation: On average, predictions are off by ~{mean_absolute_error(y_true, y_pred):.1f} points out of 100.
  Target: MAE < 5 is good, < 3 is excellent.

MODEL 2: Risk Classification (Gradient Boosting)
  Accuracy : {accuracy_score(y_risk_true, y_risk_pred)*100:.1f}%
  Classes  : low / medium / high
  Target   : > 85% accuracy is good.

MODEL 3: Asset Allocation (Multi-output Random Forest)
  Equity  MAE : {maes[0]:.2f}%
  Debt    MAE : {maes[1]:.2f}%
  Gold    MAE : {maes[2]:.2f}%
  Liquid  MAE : {maes[3]:.2f}%
  Target: MAE < 3% per asset class is good.

All models ready for deployment.
"""
print(report)
with open('evaluation/metrics.txt', 'w') as f:
    f.write(report)
print("📝 Metrics report saved → evaluation/metrics.txt")
