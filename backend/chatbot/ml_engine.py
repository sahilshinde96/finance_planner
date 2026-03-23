"""Rule-based NLP chatbot engine for ARTH financial queries."""

RESPONSES = {
    'sip': """📈 **SIP (Systematic Investment Plan)**

A SIP lets you invest a fixed amount in mutual funds every month automatically.

**Why SIP works:**
• Rupee cost averaging — buy more units when markets fall
• Power of compounding over time
• Start with as low as ₹500/month
• No need to time the market

**Example:** ₹5,000/month SIP at 12% returns for 20 years = **₹49.9 lakh** corpus!

Use the Finance Planner to calculate your own SIP projection. 🎯""",

    'mutual fund': """💰 **Mutual Funds — The Basics**

A mutual fund pools money from thousands of investors. Professional fund managers invest in stocks, bonds, or both.

**Types:**
• **Equity funds** — invest in stocks, higher risk/return (for 5+ year goals)
• **Debt funds** — invest in bonds, lower risk (for 1-3 year goals)
• **Hybrid funds** — mix of both
• **Index funds** — track NIFTY/SENSEX, very low cost ⭐

**Tax:** LTCG (>1 year) taxed at 10% on gains above ₹1 lakh.""",

    'emergency fund': """🛡️ **Emergency Fund — Your Financial Foundation**

Before any investing, build an emergency fund.

**How much:** 3–6 months of your monthly expenses
**Where to keep:** High-yield savings account or liquid mutual fund
**NOT in:** FDs (premature withdrawal penalty), stocks (volatile)

**Why it matters:** Job loss, medical emergency, car breakdown — emergencies don't announce themselves. Without this fund, you'll be forced to break investments or take loans. 

Build this FIRST before SIPs or any investments.""",

    'insurance': """🛡️ **Insurance — Protection Before Investment**

**Two must-haves:**

1. **Term Life Insurance**
   • Pure life cover, no investment component
   • ₹1 Crore cover costs ~₹10,000–12,000/year
   • Must-have if you have dependents (spouse, children, parents)

2. **Health Insurance**
   • Minimum ₹10 lakh family floater
   • Medical emergencies can cost ₹5–15 lakh easily
   • Get it young — premiums are lower
   
❌ **Avoid:** ULIPs, endowment plans, money-back policies — they mix insurance + investment badly.""",

    'fd': """🏦 **Fixed Deposits (FD)**

FDs are the safest investment option — DICGC insured up to **₹5 lakh per bank**.

**Current rates (approx):** 6.5% – 7.5% per year (varies by bank/tenure)

**Best for:** Emergency fund (liquid FDs), short-term goals (1–3 years)
**Not ideal for:** Long-term wealth creation (inflation eats returns)

**Tax:** Interest is fully taxable as per your income slab. FD returns often don't beat inflation for people in higher tax brackets.""",

    'tax': """💼 **Tax Saving Investments (80C)**

Save up to **₹46,800 in tax** per year with ₹1.5 lakh 80C investments:

| Option | Lock-in | Returns | Best For |
|--------|---------|---------|----------|
| ELSS | 3 years | 12–15% | Wealth creation |
| PPF | 15 years | 7.1% | Safe, tax-free |
| NPS | Till 60 | 10–12% | Retirement |
| EPF | Till 58 | 8.25% | Salary savings |

**Bonus:** NPS gives extra **₹50,000 deduction** under 80CCD(1B) beyond 80C.""",

    'home loan': """🏠 **Home Loan Guide**

**Key factors affecting your EMI:**
• Interest rate (every 0.5% matters significantly)
• Loan tenure (20 vs 30 years = big EMI vs big interest difference)
• Down payment (minimum 20%)

**Rule of thumb:** EMI should not exceed **40% of monthly income**

**Example:** ₹50L loan @ 8.5% for 20 years = **₹43,391/month EMI**

**Tax benefits:**
• Principal repayment — up to ₹1.5L under 80C
• Interest — up to ₹2L under Section 24(b)""",

    'cibil': """📊 **CIBIL Score Guide**

Your CIBIL score (300–900) determines loan approvals and interest rates.

| Score | Rating | Impact |
|-------|--------|--------|
| 750+ | Excellent | Best rates, fast approval |
| 700–749 | Good | Approved with standard rates |
| 650–699 | Fair | Higher rates, some rejections |
| Below 650 | Poor | Likely rejection |

**How to improve your score:**
✅ Pay EMIs/credit card bills on time (biggest factor — 35%)
✅ Keep credit utilisation below 30%
✅ Don't apply for many loans/cards at once
✅ Maintain old credit accounts""",

    'ppf': """🔒 **PPF (Public Provident Fund)**

One of India's best tax-free investment options.

**Key facts:**
• Interest rate: ~7.1% per year (government sets quarterly)
• Lock-in: **15 years** (partial withdrawal from Year 7)
• Max investment: ₹1.5 lakh per year
• Tax status: **EEE** — Exempt at investment, interest, and maturity
• Backed by Government of India — zero default risk

**Who should invest:** Anyone in the 20–30% tax bracket wanting safe, guaranteed, tax-free returns.""",

    'retirement': """🏖️ **Retirement Planning**

The earlier you start, the less you need to invest.

**Rule of 72:** Divide 72 by return rate = years to double money
At 12%: 72/12 = **6 years to double**

**For ₹1 Crore at retirement (12% returns):**
• Start at 25 → need **₹4,000/month SIP** for 35 years
• Start at 35 → need **₹13,500/month SIP** for 25 years
• Start at 45 → need **₹53,000/month SIP** for 15 years

**Best vehicles:** NPS (extra tax benefit), ELSS SIP, PPF combo

Use ARTH's Finance Planner for a personalised retirement projection! 🎯""",

    'nifty': """📈 **NIFTY 50 — India's Benchmark Index**

NIFTY 50 tracks the 50 largest companies on NSE across 13 sectors.

**Long-term returns:** ~12–14% CAGR over 15+ years
**Best way to invest:** Low-cost Nifty 50 Index Fund via SIP

**Top holdings (approx):** Reliance, TCS, HDFC Bank, Infosys, ICICI Bank

**Why index funds beat most active funds:** Lower expense ratio (0.1% vs 1–2%), consistent market returns, no fund manager risk.""",

    'budget': """💰 **The 50-30-20 Budgeting Rule**

Divide your take-home salary:

• **50% Needs** — rent, food, utilities, EMIs, insurance
• **30% Wants** — dining out, shopping, entertainment, travel  
• **20% Savings** — investments, emergency fund, goals

**Pro tip:** Pay yourself first — set up an auto-debit on salary day to move 20% to savings before you can spend it.

If your EMIs alone are >40% of income, focus on paying down debt before increasing lifestyle spending.""",
}

FALLBACK = """🤔 I can help with financial topics like:

• **Investments** — SIP, mutual funds, stocks, FDs, PPF, NPS
• **Insurance** — term life, health, ULIPs
• **Tax planning** — 80C, 80D, ELSS, NPS
• **Loans** — home loan, EMI, CIBIL score
• **Budgeting** — 50-30-20 rule, emergency fund
• **Retirement** — planning, corpus calculation

Try asking: *"How do I start a SIP?"* or *"What insurance do I need?"*"""


def get_response(message: str) -> str:
    msg = message.lower()

    # Match keywords to response
    if any(k in msg for k in ['sip', 'systematic investment']):
        return RESPONSES['sip']
    if any(k in msg for k in ['mutual fund', 'mf', 'elss', 'nfo', 'nav']):
        return RESPONSES['mutual fund']
    if any(k in msg for k in ['emergency fund', 'emergency', 'liquid fund']):
        return RESPONSES['emergency fund']
    if any(k in msg for k in ['insurance', 'term life', 'health cover', 'ulip', 'policy']):
        return RESPONSES['insurance']
    if any(k in msg for k in ['fd', 'fixed deposit', 'fdrate']):
        return RESPONSES['fd']
    if any(k in msg for k in ['tax', '80c', '80d', 'tax saving', 'itr', 'income tax']):
        return RESPONSES['tax']
    if any(k in msg for k in ['home loan', 'housing loan', 'mortgage', 'emi']):
        return RESPONSES['home loan']
    if any(k in msg for k in ['cibil', 'credit score', 'credit rating']):
        return RESPONSES['cibil']
    if any(k in msg for k in ['ppf', 'public provident']):
        return RESPONSES['ppf']
    if any(k in msg for k in ['retire', 'retirement', 'pension', 'nps']):
        return RESPONSES['retirement']
    if any(k in msg for k in ['nifty', 'sensex', 'index fund', 'stock market', 'market']):
        return RESPONSES['nifty']
    if any(k in msg for k in ['budget', '50-30-20', '50 30 20', 'budgeting', 'expense']):
        return RESPONSES['budget']

    # Greeting
    if any(k in msg for k in ['hello', 'hi ', 'hey', 'helo', 'namaste', 'good morning', 'good evening']):
        return "Hello! 👋 I'm ARTH, your AI financial advisor. What financial question can I help you with today?"

    return FALLBACK
