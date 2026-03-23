"""
ARTH ML Finance Planner — Step 2 & 3: Preprocess + Train Models
Run: python step2_train.py
Output: models/  (health_model.pkl, risk_model.pkl, allocation_model.pkl, preprocessor.pkl)
"""
import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import (
    mean_absolute_error, r2_score, accuracy_score, classification_report
)
import warnings
warnings.filterwarnings('ignore')

os.makedirs('models', exist_ok=True)

# ── Load data ────────────────────────────────────────────────────────────────
print("📂 Loading dataset...")
df = pd.read_csv('data/finance_dataset.csv')
print(f"   {len(df):,} rows loaded\n")

# ── Feature engineering ──────────────────────────────────────────────────────
# Encode binary targets
df['has_emergency_fund']   = df['has_emergency_fund'].astype(int)
df['has_health_insurance'] = df['has_health_insurance'].astype(int)
df['has_life_insurance']   = df['has_life_insurance'].astype(int)
df['is_rented']            = (df['housing'] == 'rented').astype(int)

NUMERIC_FEATURES = [
    'age', 'monthly_income', 'monthly_rent', 'monthly_food',
    'monthly_transport', 'monthly_utilities', 'monthly_emi', 'monthly_other',
    'dependents', 'has_emergency_fund', 'has_health_insurance', 'has_life_insurance',
    'savings_rate', 'emi_ratio', 'disposable_income', 'annual_income',
    'years_to_retire', 'is_rented',
]
CATEGORICAL_FEATURES = ['risk_appetite']

ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

# ── Build preprocessor ────────────────────────────────────────────────────────
preprocessor = ColumnTransformer(transformers=[
    ('num', StandardScaler(), NUMERIC_FEATURES),
    ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CATEGORICAL_FEATURES),
])

X = df[ALL_FEATURES]
X_transformed = preprocessor.fit_transform(X)
print("🔧 Preprocessing complete")
print(f"   Feature matrix: {X_transformed.shape[0]:,} samples × {X_transformed.shape[1]} features\n")

# Save preprocessor
with open('models/preprocessor.pkl', 'wb') as f:
    pickle.dump({'preprocessor': preprocessor, 'feature_cols': ALL_FEATURES}, f)
print("💾 Preprocessor saved → models/preprocessor.pkl\n")

# ── Split ─────────────────────────────────────────────────────────────────────
X_train, X_test, _, _ = train_test_split(X_transformed, df.index, test_size=0.2, random_state=42)
train_idx = _.index if hasattr(_, 'index') else _
# Simpler: just split the whole df
X_tr, X_te = X_transformed[:8000], X_transformed[8000:]
df_tr, df_te = df.iloc[:8000], df.iloc[8000:]


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL 1: Health Score — RandomForest Regressor
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("🌲 MODEL 1: Financial Health Score (Regressor)")
print("=" * 60)

y_health_tr = df_tr['health_score'].values
y_health_te = df_te['health_score'].values

health_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    min_samples_leaf=5,
    n_jobs=-1,
    random_state=42
)
health_model.fit(X_tr, y_health_tr)
pred_health = health_model.predict(X_te)

mae  = mean_absolute_error(y_health_te, pred_health)
r2   = r2_score(y_health_te, pred_health)
print(f"   MAE  : {mae:.2f} points")
print(f"   R²   : {r2:.4f}")
print(f"   Prediction range: {pred_health.min():.1f} – {pred_health.max():.1f}")

with open('models/health_model.pkl', 'wb') as f:
    pickle.dump(health_model, f)
print("   ✅ Saved → models/health_model.pkl\n")

# Feature importance (top 10)
feat_names = (
    NUMERIC_FEATURES +
    list(preprocessor.named_transformers_['cat']
         .get_feature_names_out(CATEGORICAL_FEATURES))
)
importances = pd.Series(health_model.feature_importances_, index=feat_names)
print("   Top 10 important features:")
for name, val in importances.nlargest(10).items():
    print(f"     {name:30s}  {val:.4f}")
print()


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL 2: Risk Class — GradientBoosting Classifier
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("🎯 MODEL 2: Risk Classification (Classifier)")
print("=" * 60)

le = LabelEncoder()
y_risk_tr = le.fit_transform(df_tr['risk_class'].values)
y_risk_te = le.transform(df_te['risk_class'].values)

risk_model = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.08,
    max_depth=4,
    subsample=0.8,
    random_state=42
)
risk_model.fit(X_tr, y_risk_tr)
pred_risk = risk_model.predict(X_te)

acc = accuracy_score(y_risk_te, pred_risk)
print(f"   Accuracy: {acc:.4f} ({acc*100:.1f}%)")
print()
print(classification_report(
    le.inverse_transform(y_risk_te),
    le.inverse_transform(pred_risk)
))

with open('models/risk_model.pkl', 'wb') as f:
    pickle.dump({'model': risk_model, 'label_encoder': le}, f)
print("   ✅ Saved → models/risk_model.pkl\n")


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL 3: Asset Allocation — MultiOutput Regressor
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("📊 MODEL 3: Asset Allocation % (Multi-output Regressor)")
print("=" * 60)

ALLOC_COLS = ['equity_pct', 'debt_pct', 'gold_pct', 'liquid_pct']
y_alloc_tr = df_tr[ALLOC_COLS].values
y_alloc_te = df_te[ALLOC_COLS].values

alloc_model = MultiOutputRegressor(
    RandomForestRegressor(
        n_estimators=150,
        max_depth=10,
        min_samples_leaf=5,
        n_jobs=-1,
        random_state=42
    ),
    n_jobs=-1
)
alloc_model.fit(X_tr, y_alloc_tr)
pred_alloc = alloc_model.predict(X_te)

# Normalise predictions to sum to 100
pred_alloc_norm = pred_alloc / pred_alloc.sum(axis=1, keepdims=True) * 100

for i, col in enumerate(ALLOC_COLS):
    mae_col = mean_absolute_error(y_alloc_te[:, i], pred_alloc_norm[:, i])
    r2_col  = r2_score(y_alloc_te[:, i], pred_alloc_norm[:, i])
    print(f"   {col:12s}  MAE={mae_col:.2f}%  R²={r2_col:.4f}")

with open('models/allocation_model.pkl', 'wb') as f:
    pickle.dump({'model': alloc_model, 'columns': ALLOC_COLS}, f)
print("\n   ✅ Saved → models/allocation_model.pkl\n")

print("=" * 60)
print("🎉 All 3 models trained and saved to models/")
print("=" * 60)
print("""
Models directory:
  models/
    preprocessor.pkl     ← Feature scaler + encoder
    health_model.pkl     ← RandomForest → health score (0–100)
    risk_model.pkl       ← GradientBoosting → risk class (low/med/high)
    allocation_model.pkl ← MultiOutput RF → equity/debt/gold/liquid %

Next step: python step3_evaluate.py
""")
