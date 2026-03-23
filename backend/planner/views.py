from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FinancialGoal
from .serializers import (
    FinancialGoalSerializer, SIPSerializer, EMISerializer,
    TaxSerializer, RetirementSerializer,
)
from .calculators import calculate_sip, calculate_emi, calculate_tax, calculate_retirement


# ─── Standard Calculators ─────────────────────────────────────────────────────

class FinancialGoalListCreateView(generics.ListCreateAPIView):
    serializer_class = FinancialGoalSerializer
    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FinancialGoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FinancialGoalSerializer
    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user)


class SIPCalculatorView(APIView):
    def post(self, request):
        s = SIPSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        return Response(calculate_sip(**s.validated_data))


class EMICalculatorView(APIView):
    def post(self, request):
        s = EMISerializer(data=request.data)
        s.is_valid(raise_exception=True)
        return Response(calculate_emi(**s.validated_data))


class TaxCalculatorView(APIView):
    def post(self, request):
        s = TaxSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        return Response(calculate_tax(**s.validated_data))


class RetirementCalculatorView(APIView):
    def post(self, request):
        s = RetirementSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        return Response(calculate_retirement(**s.validated_data))


# ─── ML Finance Planner ────────────────────────────────────────────────────────

class MLFinancePlannerView(APIView):
    """
    Personalized ML-based financial plan.
    Accepts questionnaire inputs and returns a structured financial plan
    with investment allocation, savings targets, and actionable recommendations.
    """

    def post(self, request):
        data = request.data

        # Extract questionnaire inputs
        monthly_income = float(data.get('monthly_income', 0))
        housing = data.get('housing', 'rented')          # 'rented' or 'owned'
        monthly_rent = float(data.get('monthly_rent', 0))
        monthly_food = float(data.get('monthly_food', 0))
        monthly_transport = float(data.get('monthly_transport', 0))
        monthly_utilities = float(data.get('monthly_utilities', 0))
        monthly_emi = float(data.get('monthly_emi', 0))
        monthly_other = float(data.get('monthly_other', 0))
        dependents = int(data.get('dependents', 0))
        age = int(data.get('age', 30))
        risk_appetite = data.get('risk_appetite', 'medium')  # low/medium/high
        goals = data.get('goals', [])                         # list of strings
        has_emergency_fund = data.get('has_emergency_fund', False)
        has_health_insurance = data.get('has_health_insurance', False)
        has_life_insurance = data.get('has_life_insurance', False)

        if monthly_income <= 0:
            return Response({'error': 'Monthly income must be positive'}, status=400)

        # ─── Expense Analysis ──────────────────────────────────────────────────
        housing_cost = monthly_rent if housing == 'rented' else 0
        total_fixed = housing_cost + monthly_emi
        total_variable = monthly_food + monthly_transport + monthly_utilities + monthly_other
        total_expenses = total_fixed + total_variable
        disposable_income = monthly_income - total_expenses
        savings_rate = (disposable_income / monthly_income) * 100 if monthly_income > 0 else 0

        # ─── Health Score (0–100) ──────────────────────────────────────────────
        score = 100
        health_issues = []
        health_positives = []

        if savings_rate < 10:
            score -= 30
            health_issues.append(f'Very low savings rate ({savings_rate:.0f}%) — target ≥20%')
        elif savings_rate < 20:
            score -= 15
            health_issues.append(f'Savings rate {savings_rate:.0f}% — aim for 20%+')
        else:
            health_positives.append(f'Good savings rate: {savings_rate:.0f}%')

        if not has_emergency_fund:
            score -= 20
            health_issues.append('No emergency fund — critical gap')
        else:
            health_positives.append('Emergency fund in place ✓')

        if not has_health_insurance:
            score -= 15
            health_issues.append('No health insurance — high risk')
        else:
            health_positives.append('Health insurance active ✓')

        if not has_life_insurance and dependents > 0:
            score -= 10
            health_issues.append(f'{dependents} dependent(s) with no life cover')
        elif has_life_insurance:
            health_positives.append('Life insurance active ✓')

        emi_to_income = (monthly_emi / monthly_income) * 100 if monthly_income > 0 else 0
        if emi_to_income > 50:
            score -= 15
            health_issues.append(f'High EMI burden: {emi_to_income:.0f}% of income')
        elif emi_to_income > 30:
            score -= 5
            health_issues.append(f'EMI at {emi_to_income:.0f}% — manageable')

        score = max(0, min(100, score))

        # ─── Investment Allocation (rule-based ML engine) ─────────────────────
        years_to_retire = max(1, 60 - age)
        investable = max(0, disposable_income)

        if risk_appetite == 'high' and age < 45:
            equity_pct = 80; debt_pct = 10; gold_pct = 5; liquid_pct = 5
        elif risk_appetite == 'medium':
            equity_pct = min(70, max(40, 100 - age)); debt_pct = 100 - equity_pct - 10; gold_pct = 7; liquid_pct = 3
            debt_pct = max(0, debt_pct)
        else:  # low
            equity_pct = max(20, 60 - age); debt_pct = 60; gold_pct = 10; liquid_pct = 30 - equity_pct
            liquid_pct = max(0, liquid_pct)

        # Normalise to 100
        total_pct = equity_pct + debt_pct + gold_pct + liquid_pct
        equity_pct = round(equity_pct * 100 / total_pct)
        debt_pct = round(debt_pct * 100 / total_pct)
        gold_pct = round(gold_pct * 100 / total_pct)
        liquid_pct = 100 - equity_pct - debt_pct - gold_pct

        equity_amt = round(investable * equity_pct / 100)
        debt_amt = round(investable * debt_pct / 100)
        gold_amt = round(investable * gold_pct / 100)
        liquid_amt = round(investable * liquid_pct / 100)

        # ─── Recommended Products ─────────────────────────────────────────────
        products = []

        # Emergency fund first
        emergency_target = monthly_income * 6
        if not has_emergency_fund:
            products.append({
                'priority': 1, 'category': 'Safety Net',
                'name': 'Emergency Fund (Liquid Mutual Fund)',
                'amount': min(investable * 0.5, emergency_target / 12),
                'why': f'Build {emergency_target:,.0f} corpus (6 months expenses) — your financial foundation',
                'icon': '🛡️'
            })

        # Health insurance
        if not has_health_insurance:
            products.append({
                'priority': 2, 'category': 'Protection',
                'name': 'Family Health Insurance (₹10-15L cover)',
                'amount': round(monthly_income * 0.03),
                'why': 'Medical emergencies can wipe out years of savings. ₹10L cover for ~₹15K/year premium.',
                'icon': '🏥'
            })

        # Life insurance
        if not has_life_insurance and dependents > 0:
            cover = monthly_income * 12 * 20  # 20x annual income
            products.append({
                'priority': 3, 'category': 'Protection',
                'name': f'Term Life Insurance (₹{cover/100000:.0f}L cover)',
                'amount': round(monthly_income * 0.01),
                'why': f'With {dependents} dependent(s), {cover/100000:.0f}L cover at ~₹1,000/month protects your family',
                'icon': '💼'
            })

        # Tax saving (if income > 5L)
        annual_income = monthly_income * 12
        if annual_income > 500000:
            products.append({
                'priority': 4, 'category': 'Tax + Equity',
                'name': 'ELSS Mutual Fund (80C)',
                'amount': min(equity_amt * 0.4, 12500),  # max 1.5L/year = 12.5K/month
                'why': '₹1.5L/year tax deduction + equity growth. Best of both worlds with 3-yr lock-in.',
                'icon': '📊'
            })

        # Equity investments
        if equity_amt > 0:
            products.append({
                'priority': 5, 'category': 'Growth',
                'name': 'Nifty 50 Index Fund SIP',
                'amount': round(equity_amt * 0.5),
                'why': 'Low-cost market exposure. 15+ year track record of 12-14% CAGR. Start small, stay consistent.',
                'icon': '📈'
            })
            if risk_appetite == 'high':
                products.append({
                    'priority': 6, 'category': 'Growth',
                    'name': 'Mid/Small Cap Fund SIP',
                    'amount': round(equity_amt * 0.3),
                    'why': 'Higher growth potential (15-18% long-term) with higher volatility. Suitable for 7+ year horizon.',
                    'icon': '🚀'
                })

        # Debt
        if debt_amt > 0:
            products.append({
                'priority': 7, 'category': 'Stability',
                'name': 'PPF (Public Provident Fund)',
                'amount': min(debt_amt * 0.5, 12500),
                'why': '~7.1% tax-free guaranteed returns (EEE). Government backed, 15-year lock-in. Ideal for retirement.',
                'icon': '🔒'
            })

        # Retirement via NPS
        if 'retirement' in [g.lower() for g in goals]:
            products.append({
                'priority': 8, 'category': 'Retirement',
                'name': 'NPS (National Pension System)',
                'amount': min(4166, debt_amt * 0.3),  # 50K/year extra deduction
                'why': 'Extra ₹50,000 deduction under 80CCD(1B) beyond 80C. Market-linked pension with tax benefits.',
                'icon': '🏖️'
            })

        # Gold
        if gold_amt > 0:
            products.append({
                'priority': 9, 'category': 'Hedge',
                'name': 'Sovereign Gold Bond / Digital Gold',
                'amount': gold_amt,
                'why': 'Hedge against inflation. SGBs give 2.5% interest + price appreciation. No physical gold hassle.',
                'icon': '🥇'
            })

        # Liquid buffer
        if liquid_amt > 0:
            products.append({
                'priority': 10, 'category': 'Liquidity',
                'name': 'Savings Account / Liquid Fund',
                'amount': liquid_amt,
                'why': 'Keep 1-2 months expenses in high-yield savings / liquid fund for short-term needs.',
                'icon': '💧'
            })

        # ─── Budget Breakdown ─────────────────────────────────────────────────
        budget = {
            'monthly_income': monthly_income,
            'housing': housing_cost,
            'food': monthly_food,
            'transport': monthly_transport,
            'utilities': monthly_utilities,
            'emis': monthly_emi,
            'other': monthly_other,
            'total_expenses': total_expenses,
            'investable_surplus': investable,
            'savings_rate_pct': round(savings_rate, 1),
        }

        # ─── Actionable Priorities ────────────────────────────────────────────
        priorities = []
        if not has_emergency_fund:
            priorities.append({'step': 1, 'action': 'Build emergency fund', 'timeline': '0-6 months',
                                'detail': f'Save ₹{emergency_target/12:,.0f}/month until you have ₹{emergency_target:,.0f} (6 months expenses)'})
        if not has_health_insurance:
            priorities.append({'step': 2, 'action': 'Get health insurance', 'timeline': 'This month',
                                'detail': 'Compare policies on Policybazaar — minimum ₹10L family floater'})
        if savings_rate < 20:
            priorities.append({'step': 3, 'action': 'Reduce discretionary spending', 'timeline': 'Next 3 months',
                                'detail': f'Cut monthly_other expenses by ₹{monthly_other * 0.2:,.0f} to reach 20% savings rate'})
        priorities.append({'step': len(priorities) + 1, 'action': 'Start SIP investing', 'timeline': 'This month',
                            'detail': f'Start with ₹{min(2000, max(500, investable * 0.3)):,.0f}/month in Nifty 50 Index Fund — scale up quarterly'})

        # ─── SIP Projection ───────────────────────────────────────────────────
        monthly_sip = equity_amt
        if monthly_sip > 0 and years_to_retire > 0:
            sip_proj = calculate_sip(
                monthly_investment=monthly_sip,
                annual_rate=12.0 if risk_appetite == 'high' else 10.0 if risk_appetite == 'medium' else 8.0,
                years=min(years_to_retire, 30)
            )
        else:
            sip_proj = None

        return Response({
            'health_score': score,
            'health_grade': 'Excellent' if score >= 80 else 'Good' if score >= 60 else 'Fair' if score >= 40 else 'Needs Work',
            'health_issues': health_issues,
            'health_positives': health_positives,
            'budget': budget,
            'allocation': {
                'equity': {'pct': equity_pct, 'amount': equity_amt},
                'debt': {'pct': debt_pct, 'amount': debt_amt},
                'gold': {'pct': gold_pct, 'amount': gold_amt},
                'liquid': {'pct': liquid_pct, 'amount': liquid_amt},
            },
            'products': sorted(products, key=lambda x: x['priority']),
            'priorities': priorities,
            'sip_projection': sip_proj,
            'profile_summary': {
                'age': age, 'years_to_retire': years_to_retire,
                'risk_appetite': risk_appetite, 'dependents': dependents,
                'annual_income': annual_income,
            }
        })
