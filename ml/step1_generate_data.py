"""
ARTH ML Finance Planner — Step 1: Generate Training Data
Run: python step1_generate_data.py
Output: data/finance_dataset.csv  (10,000 rows)
"""
import numpy as np
import pandas as pd
import os

np.random.seed(42)
os.makedirs('data', exist_ok=True)

N = 10_000


def generate_dataset(n):
    # ── Input features ──────────────────────────────────────────────────────
    age             = np.random.randint(22, 62, n)
    monthly_income  = np.random.choice(
        [15000, 25000, 35000, 50000, 75000, 100000, 150000, 200000], n,
        p=[0.10, 0.18, 0.20, 0.20, 0.15, 0.10, 0.05, 0.02]
    )
    housing         = np.random.choice(['rented', 'owned'], n, p=[0.55, 0.45])
    monthly_rent    = np.where(housing == 'rented',
                               monthly_income * np.random.uniform(0.15, 0.35, n), 0)
    monthly_food    = monthly_income * np.random.uniform(0.08, 0.20, n)
    monthly_transport = monthly_income * np.random.uniform(0.03, 0.10, n)
    monthly_utilities = monthly_income * np.random.uniform(0.02, 0.07, n)
    monthly_emi     = monthly_income * np.random.uniform(0.00, 0.45, n)
    monthly_other   = monthly_income * np.random.uniform(0.02, 0.15, n)
    dependents      = np.random.choice([0, 1, 2, 3, 4], n, p=[0.25, 0.30, 0.28, 0.12, 0.05])
    risk_appetite   = np.random.choice(['low', 'medium', 'high'], n, p=[0.30, 0.45, 0.25])
    has_emergency_fund   = np.random.choice([0, 1], n, p=[0.60, 0.40])
    has_health_insurance = np.random.choice([0, 1], n, p=[0.45, 0.55])
    has_life_insurance   = np.random.choice([0, 1], n, p=[0.55, 0.45])

    # ── Derived features ────────────────────────────────────────────────────
    total_expenses  = monthly_rent + monthly_food + monthly_transport + monthly_utilities + monthly_emi + monthly_other
    disposable      = np.maximum(0, monthly_income - total_expenses)
    savings_rate    = disposable / monthly_income
    emi_ratio       = monthly_emi / monthly_income
    years_to_retire = np.maximum(1, 60 - age)
    annual_income   = monthly_income * 12

    # ── Target 1: Financial health score (0–100) ────────────────────────────
    health = np.full(n, 100.0)
    health -= np.where(savings_rate < 0.10, 30, np.where(savings_rate < 0.20, 15, 0))
    health -= np.where(~has_emergency_fund.astype(bool), 20, 0)
    health -= np.where(~has_health_insurance.astype(bool), 15, 0)
    health -= np.where((~has_life_insurance.astype(bool)) & (dependents > 0), 10, 0)
    health -= np.where(emi_ratio > 0.50, 15, np.where(emi_ratio > 0.30, 5, 0))
    health += np.random.normal(0, 3, n)          # realistic noise
    health = np.clip(health, 0, 100)

    # ── Target 2: Risk class (low / medium / high) ──────────────────────────
    # Combine user-stated risk with financial reality
    risk_map = {'low': 0, 'medium': 1, 'high': 2}
    base_risk = np.vectorize(risk_map.get)(risk_appetite)
    # Penalise if financial health is weak — high-risk profile but low health → downgrade
    adjusted_risk = base_risk.copy()
    adjusted_risk = np.where(health < 40, np.maximum(0, adjusted_risk - 1), adjusted_risk)
    adjusted_risk = np.where((health > 75) & (age < 40), np.minimum(2, adjusted_risk + 1), adjusted_risk)
    risk_labels = np.vectorize({0: 'low', 1: 'medium', 2: 'high'}.get)(adjusted_risk)

    # ── Target 3: Asset allocation (must sum to 100%) ───────────────────────
    equity_base = np.where(
        risk_appetite == 'high',   75,
        np.where(risk_appetite == 'medium', np.maximum(40, 100 - age), 25)
    ).astype(float)
    equity_base -= np.where(emi_ratio > 0.35, 10, 0)
    equity_base -= np.where(~has_emergency_fund.astype(bool), 10, 0)
    equity_base += np.random.normal(0, 3, n)
    equity_base  = np.clip(equity_base, 10, 85)

    gold_pct     = np.clip(5 + np.random.normal(0, 2, n), 3, 15)
    liquid_pct   = np.clip(
        np.where(~has_emergency_fund.astype(bool), 15, 5) + np.random.normal(0, 2, n),
        3, 25
    )
    debt_pct     = 100 - equity_base - gold_pct - liquid_pct
    debt_pct     = np.clip(debt_pct, 5, 60)
    # Re-normalise to exactly 100
    total        = equity_base + debt_pct + gold_pct + liquid_pct
    equity_pct   = np.round(equity_base / total * 100, 1)
    debt_pct_n   = np.round(debt_pct   / total * 100, 1)
    gold_pct_n   = np.round(gold_pct   / total * 100, 1)
    liquid_pct_n = np.round(100 - equity_pct - debt_pct_n - gold_pct_n, 1)

    # ── Build DataFrame ─────────────────────────────────────────────────────
    df = pd.DataFrame({
        # Raw inputs
        'age':                  age,
        'monthly_income':       monthly_income.round(0),
        'housing':              housing,
        'monthly_rent':         monthly_rent.round(0),
        'monthly_food':         monthly_food.round(0),
        'monthly_transport':    monthly_transport.round(0),
        'monthly_utilities':    monthly_utilities.round(0),
        'monthly_emi':          monthly_emi.round(0),
        'monthly_other':        monthly_other.round(0),
        'dependents':           dependents,
        'risk_appetite':        risk_appetite,
        'has_emergency_fund':   has_emergency_fund,
        'has_health_insurance': has_health_insurance,
        'has_life_insurance':   has_life_insurance,
        # Derived (helps model)
        'savings_rate':         savings_rate.round(4),
        'emi_ratio':            emi_ratio.round(4),
        'disposable_income':    disposable.round(0),
        'annual_income':        annual_income.round(0),
        'years_to_retire':      years_to_retire,
        # Targets
        'health_score':         health.round(1),
        'risk_class':           risk_labels,
        'equity_pct':           equity_pct,
        'debt_pct':             debt_pct_n,
        'gold_pct':             gold_pct_n,
        'liquid_pct':           liquid_pct_n,
    })
    return df


df = generate_dataset(N)
df.to_csv('data/finance_dataset.csv', index=False)
print(f"✅ Dataset created: {len(df):,} rows × {len(df.columns)} columns")
print(f"\nHealth score distribution:")
print(df['health_score'].describe().round(1))
print(f"\nRisk class distribution:")
print(df['risk_class'].value_counts())
print(f"\nAllocation averages (%):")
print(df[['equity_pct','debt_pct','gold_pct','liquid_pct']].mean().round(1))
print(f"\nSaved to: data/finance_dataset.csv")
