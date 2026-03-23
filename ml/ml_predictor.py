"""
ARTH ML Finance Planner — Step 4: Prediction Engine
This module is imported by Django's planner/views.py

Usage:
    from .ml_predictor import FinancePlanner
    result = FinancePlanner.predict(user_data_dict)
"""
import os
import pickle
import numpy as np
import pandas as pd
from pathlib import Path

# Path to models/ directory — adjust if needed
MODELS_DIR = Path(__file__).parent / 'models'


class FinancePlanner:
    _preprocessor  = None
    _health_model  = None
    _risk_model    = None
    _risk_le       = None
    _alloc_model   = None
    _alloc_cols    = None
    _feature_cols  = None
    _loaded        = False

    @classmethod
    def _load(cls):
        if cls._loaded:
            return
        try:
            with open(MODELS_DIR / 'preprocessor.pkl', 'rb') as f:
                d = pickle.load(f)
                cls._preprocessor = d['preprocessor']
                cls._feature_cols  = d['feature_cols']

            with open(MODELS_DIR / 'health_model.pkl', 'rb') as f:
                cls._health_model = pickle.load(f)

            with open(MODELS_DIR / 'risk_model.pkl', 'rb') as f:
                d = pickle.load(f)
                cls._risk_model = d['model']
                cls._risk_le    = d['label_encoder']

            with open(MODELS_DIR / 'allocation_model.pkl', 'rb') as f:
                d = pickle.load(f)
                cls._alloc_model = d['model']
                cls._alloc_cols  = d['columns']

            cls._loaded = True
        except FileNotFoundError:
            # Models not yet trained — fall back to rule-based
            cls._loaded = False

    @classmethod
    def predict(cls, data: dict) -> dict:
        """
        data keys:
          monthly_income, housing, monthly_rent, monthly_food,
          monthly_transport, monthly_utilities, monthly_emi, monthly_other,
          dependents, age, risk_appetite, has_emergency_fund,
          has_health_insurance, has_life_insurance, goals (list)
        """
        cls._load()

        # ── Extract & derive features ─────────────────────────────────────
        monthly_income  = float(data.get('monthly_income', 0))
        housing         = data.get('housing', 'rented')
        monthly_rent    = float(data.get('monthly_rent', 0))
        monthly_food    = float(data.get('monthly_food', 0))
        monthly_transport = float(data.get('monthly_transport', 0))
        monthly_utilities = float(data.get('monthly_utilities', 0))
        monthly_emi     = float(data.get('monthly_emi', 0))
        monthly_other   = float(data.get('monthly_other', 0))
        dependents      = int(data.get('dependents', 0))
        age             = int(data.get('age', 30))
        risk_appetite   = data.get('risk_appetite', 'medium')
        has_emergency_fund   = int(bool(data.get('has_emergency_fund', False)))
        has_health_insurance = int(bool(data.get('has_health_insurance', False)))
        has_life_insurance   = int(bool(data.get('has_life_insurance', False)))

        total_expenses   = monthly_rent + monthly_food + monthly_transport + monthly_utilities + monthly_emi + monthly_other
        disposable       = max(0, monthly_income - total_expenses)
        savings_rate     = disposable / monthly_income if monthly_income > 0 else 0
        emi_ratio        = monthly_emi / monthly_income if monthly_income > 0 else 0
        years_to_retire  = max(1, 60 - age)
        annual_income    = monthly_income * 12
        is_rented        = 1 if housing == 'rented' else 0

        row = pd.DataFrame([{
            'age': age,
            'monthly_income': monthly_income,
            'monthly_rent': monthly_rent,
            'monthly_food': monthly_food,
            'monthly_transport': monthly_transport,
            'monthly_utilities': monthly_utilities,
            'monthly_emi': monthly_emi,
            'monthly_other': monthly_other,
            'dependents': dependents,
            'has_emergency_fund': has_emergency_fund,
            'has_health_insurance': has_health_insurance,
            'has_life_insurance': has_life_insurance,
            'savings_rate': savings_rate,
            'emi_ratio': emi_ratio,
            'disposable_income': disposable,
            'annual_income': annual_income,
            'years_to_retire': years_to_retire,
            'is_rented': is_rented,
            'risk_appetite': risk_appetite,
        }])

        # ── ML predictions (if models loaded) ────────────────────────────
        if cls._loaded:
            X = cls._preprocessor.transform(row[cls._feature_cols])

            health_score = float(cls._health_model.predict(X)[0])
            health_score = round(max(0, min(100, health_score)), 1)

            risk_encoded = cls._risk_model.predict(X)[0]
            risk_proba   = cls._risk_model.predict_proba(X)[0]
            risk_label   = cls._risk_le.inverse_transform([risk_encoded])[0]
            risk_confidence = float(risk_proba.max())

            alloc_raw  = cls._alloc_model.predict(X)[0]
            alloc_norm = alloc_raw / alloc_raw.sum() * 100
            equity_pct, debt_pct, gold_pct, liquid_pct = [round(float(v), 1) for v in alloc_norm]

        else:
            # Rule-based fallback (same as before — always available)
            health_score = _rule_based_health(
                savings_rate, has_emergency_fund, has_health_insurance,
                has_life_insurance, dependents, emi_ratio
            )
            risk_label, risk_confidence = risk_appetite, 0.7
            equity_pct, debt_pct, gold_pct, liquid_pct = _rule_based_allocation(
                risk_appetite, age, has_emergency_fund, emi_ratio
            )

        # ── Build full response ───────────────────────────────────────────
        health_grade = (
            'Excellent' if health_score >= 80 else
            'Good' if health_score >= 60 else
            'Fair' if health_score >= 40 else 'Needs Work'
        )

        health_issues, health_positives = [], []
        if savings_rate < 0.10:
            health_issues.append(f'Very low savings rate ({savings_rate*100:.0f}%) — target ≥20%')
        elif savings_rate < 0.20:
            health_issues.append(f'Savings rate {savings_rate*100:.0f}% — aim for 20%+')
        else:
            health_positives.append(f'Good savings rate: {savings_rate*100:.0f}%')
        if not has_emergency_fund:
            health_issues.append('No emergency fund — critical gap')
        else:
            health_positives.append('Emergency fund in place ✓')
        if not has_health_insurance:
            health_issues.append('No health insurance — high risk')
        else:
            health_positives.append('Health insurance active ✓')
        if not has_life_insurance and dependents > 0:
            health_issues.append(f'{dependents} dependent(s) with no life cover')
        elif has_life_insurance:
            health_positives.append('Life insurance active ✓')

        allocation = {
            'equity':  {'pct': equity_pct,  'amount': round(disposable * equity_pct / 100)},
            'debt':    {'pct': debt_pct,    'amount': round(disposable * debt_pct / 100)},
            'gold':    {'pct': gold_pct,    'amount': round(disposable * gold_pct / 100)},
            'liquid':  {'pct': liquid_pct,  'amount': round(disposable * liquid_pct / 100)},
        }

        products = _build_products(
            monthly_income, disposable, allocation, has_emergency_fund,
            has_health_insurance, has_life_insurance, dependents,
            annual_income, risk_label
        )

        from planner.calculators import calculate_sip
        sip_months = round(disposable * equity_pct / 100)
        sip_proj = calculate_sip(
            monthly_investment=max(500, sip_months),
            annual_rate=12.0 if risk_label == 'high' else 10.0 if risk_label == 'medium' else 8.0,
            years=min(years_to_retire, 30)
        ) if sip_months > 0 else None

        return {
            'ml_powered': cls._loaded,
            'risk_confidence': risk_confidence if cls._loaded else None,
            'health_score': health_score,
            'health_grade': health_grade,
            'health_issues': health_issues,
            'health_positives': health_positives,
            'budget': {
                'monthly_income': monthly_income,
                'housing': monthly_rent if housing == 'rented' else 0,
                'food': monthly_food,
                'transport': monthly_transport,
                'utilities': monthly_utilities,
                'emis': monthly_emi,
                'other': monthly_other,
                'total_expenses': total_expenses,
                'investable_surplus': disposable,
                'savings_rate_pct': round(savings_rate * 100, 1),
            },
            'allocation': allocation,
            'products': products,
            'sip_projection': sip_proj,
            'profile_summary': {
                'age': age, 'years_to_retire': years_to_retire,
                'risk_appetite': risk_label, 'dependents': dependents,
                'annual_income': annual_income,
            },
        }


# ── Helpers ───────────────────────────────────────────────────────────────────
def _rule_based_health(savings_rate, emerg, health_ins, life_ins, deps, emi_ratio):
    s = 100.0
    s -= 30 if savings_rate < 0.10 else 15 if savings_rate < 0.20 else 0
    s -= 20 if not emerg else 0
    s -= 15 if not health_ins else 0
    s -= 10 if (not life_ins and deps > 0) else 0
    s -= 15 if emi_ratio > 0.50 else 5 if emi_ratio > 0.30 else 0
    return round(max(0, min(100, s)), 1)


def _rule_based_allocation(risk, age, emerg, emi_ratio):
    if risk == 'high' and age < 45:
        e, d, g, l = 75, 14, 6, 5
    elif risk == 'medium':
        e = min(65, max(35, 100 - age))
        g, l = 7, 5
        d = 100 - e - g - l
    else:
        e = max(20, 55 - age)
        g, l = 10, 15
        d = 100 - e - g - l
    if not emerg:
        l += 10; e -= 10
    total = e + d + g + l
    return round(e/total*100, 1), round(d/total*100, 1), round(g/total*100, 1), round(100 - e/total*100 - d/total*100 - g/total*100, 1)


def _build_products(income, disposable, allocation, emerg, health_ins, life_ins, deps, annual_inc, risk):
    products = []
    p = 1
    if not emerg:
        products.append({'priority': p, 'category': 'Safety Net', 'icon': '🛡️',
                         'name': 'Emergency Fund (Liquid Mutual Fund)',
                         'amount': min(disposable * 0.5, income * 0.5),
                         'why': f'Build {income*6:,.0f} corpus (6 months expenses) first'})
        p += 1
    if not health_ins:
        products.append({'priority': p, 'category': 'Protection', 'icon': '🏥',
                         'name': 'Family Health Insurance (₹10L cover)',
                         'amount': round(income * 0.03),
                         'why': '₹10L cover costs ~₹15K/year — protect against medical emergencies'})
        p += 1
    if not life_ins and deps > 0:
        products.append({'priority': p, 'category': 'Protection', 'icon': '💼',
                         'name': f'Term Life Insurance ({income*12*20/100000:.0f}L cover)',
                         'amount': round(income * 0.01),
                         'why': f'With {deps} dependent(s), pure term cover is essential'})
        p += 1
    if annual_inc > 500000:
        products.append({'priority': p, 'category': 'Tax + Equity', 'icon': '📊',
                         'name': 'ELSS Mutual Fund (80C)',
                         'amount': min(allocation['equity']['amount'] * 0.4, 12500),
                         'why': '₹1.5L/year tax deduction + equity growth with 3-year lock-in'})
        p += 1
    if allocation['equity']['amount'] > 0:
        products.append({'priority': p, 'category': 'Growth', 'icon': '📈',
                         'name': 'Nifty 50 Index Fund SIP',
                         'amount': round(allocation['equity']['amount'] * 0.5),
                         'why': 'Low-cost market exposure, 12–14% CAGR long-term'})
        p += 1
    if allocation['debt']['amount'] > 0:
        products.append({'priority': p, 'category': 'Stability', 'icon': '🔒',
                         'name': 'PPF (Public Provident Fund)',
                         'amount': min(allocation['debt']['amount'] * 0.5, 12500),
                         'why': '~7.1% tax-free guaranteed returns (EEE)'})
        p += 1
    if allocation['gold']['amount'] > 0:
        products.append({'priority': p, 'category': 'Hedge', 'icon': '🥇',
                         'name': 'Sovereign Gold Bond',
                         'amount': allocation['gold']['amount'],
                         'why': '2.5% interest + price appreciation, no physical gold hassle'})
    return sorted(products, key=lambda x: x['priority'])
