"""Financial calculators for ARTH planner."""


def calculate_sip(monthly_investment: float, annual_rate: float, years: int) -> dict:
    r = annual_rate / 100 / 12
    n = years * 12
    if r == 0:
        total_value = monthly_investment * n
    else:
        total_value = monthly_investment * (((1 + r) ** n - 1) / r) * (1 + r)
    total_invested = monthly_investment * n
    wealth_gain = total_value - total_invested
    return {
        'monthly_investment': round(monthly_investment, 2),
        'annual_rate': annual_rate,
        'years': years,
        'total_invested': round(total_invested, 2),
        'total_value': round(total_value, 2),
        'wealth_gain': round(wealth_gain, 2),
        'growth_multiple': round(total_value / total_invested, 2) if total_invested else 0,
    }


def calculate_emi(principal: float, annual_rate: float, years: int) -> dict:
    r = annual_rate / 100 / 12
    n = years * 12
    if r == 0:
        emi = principal / n
    else:
        emi = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)
    total_payment = emi * n
    total_interest = total_payment - principal
    return {
        'principal': round(principal, 2),
        'annual_rate': annual_rate,
        'years': years,
        'emi': round(emi, 2),
        'total_payment': round(total_payment, 2),
        'total_interest': round(total_interest, 2),
        'interest_percentage': round(total_interest / principal * 100, 1),
    }


def calculate_tax(annual_income: float, deductions_80c: float = 0,
                  deductions_80d: float = 0, other_deductions: float = 0,
                  regime: str = 'new') -> dict:
    tax = 0
    if regime == 'new':
        # New regime FY 2024-25
        slabs = [(300000, 0), (300000, 0.05), (300000, 0.10),
                 (300000, 0.15), (300000, 0.20), (float('inf'), 0.30)]
        taxable = annual_income
        remaining = taxable
        for limit, rate in slabs:
            if remaining <= 0:
                break
            slab_income = min(remaining, limit)
            tax += slab_income * rate
            remaining -= slab_income
        if taxable <= 700000:
            tax = 0  # Rebate u/s 87A
    else:
        # Old regime
        total_deductions = min(deductions_80c, 150000) + min(deductions_80d, 25000) + other_deductions
        taxable = max(0, annual_income - 50000 - total_deductions)  # 50K standard deduction
        if taxable <= 250000:
            tax = 0
        elif taxable <= 500000:
            tax = (taxable - 250000) * 0.05
        elif taxable <= 1000000:
            tax = 12500 + (taxable - 500000) * 0.20
        else:
            tax = 112500 + (taxable - 1000000) * 0.30
        if taxable <= 500000:
            tax = 0  # Rebate 87A

    cess = tax * 0.04
    total_tax = tax + cess
    return {
        'annual_income': round(annual_income, 2),
        'regime': regime,
        'total_deductions': round(deductions_80c + deductions_80d + other_deductions, 2),
        'income_tax': round(tax, 2),
        'cess': round(cess, 2),
        'total_tax': round(total_tax, 2),
        'effective_rate': round(total_tax / annual_income * 100, 2) if annual_income else 0,
        'monthly_take_home': round((annual_income - total_tax) / 12, 2),
    }


def calculate_retirement(current_age: int, retirement_age: int,
                         monthly_expenses: float, current_savings: float = 0,
                         expected_return: float = 10.0, inflation_rate: float = 6.0) -> dict:
    years_to_retire = retirement_age - current_age
    years_in_retirement = max(25, 85 - retirement_age)

    # Future monthly expenses at retirement (inflation-adjusted)
    future_monthly = monthly_expenses * ((1 + inflation_rate / 100) ** years_to_retire)

    # Corpus needed (25x annual expenses — 4% withdrawal rule)
    corpus_needed = future_monthly * 12 * 25

    # Grow current savings
    grown_savings = current_savings * ((1 + expected_return / 100) ** years_to_retire)

    # Additional corpus needed
    additional_needed = max(0, corpus_needed - grown_savings)

    # Monthly SIP needed
    r = expected_return / 100 / 12
    n = years_to_retire * 12
    if r == 0 or n == 0:
        monthly_sip = additional_needed / max(n, 1)
    else:
        monthly_sip = additional_needed * r / (((1 + r) ** n - 1) * (1 + r))

    return {
        'current_age': current_age,
        'retirement_age': retirement_age,
        'years_to_retire': years_to_retire,
        'current_monthly_expenses': round(monthly_expenses, 2),
        'future_monthly_expenses': round(future_monthly, 2),
        'corpus_needed': round(corpus_needed, 2),
        'grown_savings': round(grown_savings, 2),
        'additional_corpus_needed': round(additional_needed, 2),
        'monthly_sip_required': round(monthly_sip, 2),
        'years_in_retirement': years_in_retirement,
    }
