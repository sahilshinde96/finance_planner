import React, { useState } from 'react';
import api from '../api/client';

// ─── Types ─────────────────────────────────────────────────────────────────────
interface Allocation { pct: number; amount: number; }
interface Product { priority: number; category: string; name: string; amount: number; why: string; icon: string; }
interface Priority { step: number; action: string; timeline: string; detail: string; }
interface SIPProjection { total_value: number; total_invested: number; wealth_gain: number; }
interface PlanResult {
  health_score: number;
  health_grade: string;
  health_issues: string[];
  health_positives: string[];
  budget: { monthly_income: number; housing: number; food: number; transport: number;
    utilities: number; emis: number; other: number; total_expenses: number;
    investable_surplus: number; savings_rate_pct: number; };
  allocation: { equity: Allocation; debt: Allocation; gold: Allocation; liquid: Allocation; };
  products: Product[];
  priorities: Priority[];
  sip_projection: SIPProjection | null;
  profile_summary: { age: number; years_to_retire: number; risk_appetite: string; dependents: number; annual_income: number; };
}

const FinancePlanner: React.FC = () => {
  const [step, setStep] = useState<'intro' | 'form' | 'result'>('intro');
  const [loading, setLoading] = useState(false);
  const [plan, setPlan] = useState<PlanResult | null>(null);
  const [activeTab, setActiveTab] = useState<'plan' | 'calculators'>('plan');

  const [form, setForm] = useState({
    monthly_income: '', housing: 'rented', monthly_rent: '',
    monthly_food: '', monthly_transport: '', monthly_utilities: '',
    monthly_emi: '', monthly_other: '', dependents: '0', age: '',
    risk_appetite: 'medium', goals: [] as string[],
    has_emergency_fund: false, has_health_insurance: false, has_life_insurance: false,
  });

  const [calc, setCalc] = useState({ type: 'sip', amount: '', rate: '', years: '', loan: '', result: null as any });

  const GOALS = ['Retirement', 'Home Purchase', 'Child Education', 'Emergency Fund', 'Car', 'Travel', 'Investment Growth'];

  const toggleGoal = (goal: string) => {
    setForm(f => ({
      ...f,
      goals: f.goals.includes(goal) ? f.goals.filter(g => g !== goal) : [...f.goals, goal]
    }));
  };

  const handleInput = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    const val = type === 'checkbox' ? (e.target as HTMLInputElement).checked : value;
    setForm(f => ({ ...f, [name]: val }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const payload = {
        ...form,
        monthly_income: Number(form.monthly_income),
        monthly_rent: Number(form.monthly_rent),
        monthly_food: Number(form.monthly_food),
        monthly_transport: Number(form.monthly_transport),
        monthly_utilities: Number(form.monthly_utilities),
        monthly_emi: Number(form.monthly_emi),
        monthly_other: Number(form.monthly_other),
        dependents: Number(form.dependents),
        age: Number(form.age),
      };
      const res = await api.post('/planner/ml-plan/', payload);
      setPlan(res.data);
      setStep('result');
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const runCalc = async () => {
    try {
      let endpoint = '', payload: any = {};
      if (calc.type === 'sip') {
        endpoint = '/planner/calculate/sip/';
        payload = { monthly_investment: Number(calc.amount), annual_rate: Number(calc.rate), years: Number(calc.years) };
      } else if (calc.type === 'emi') {
        endpoint = '/planner/calculate/emi/';
        payload = { principal: Number(calc.loan), annual_rate: Number(calc.rate), years: Number(calc.years) };
      } else if (calc.type === 'tax') {
        endpoint = '/planner/calculate/tax/';
        payload = { annual_income: Number(calc.amount) };
      } else {
        endpoint = '/planner/calculate/retirement/';
        payload = { current_age: Number(calc.amount), monthly_savings: Number(calc.loan), annual_rate: Number(calc.rate) };
      }
      const res = await api.post(endpoint, payload);
      setCalc(c => ({ ...c, result: res.data }));
    } catch (e) { console.error(e); }
  };

  const scoreColor = (score: number) =>
    score >= 80 ? 'var(--accent-green)' : score >= 60 ? '#f59e0b' : score >= 40 ? 'var(--accent-orange)' : 'var(--accent-red)';

  // ─── Intro Screen ─────────────────────────────────────────────────────────────
  if (step === 'intro') return (
    <div className="page-container">
      <div className="planner-intro">
        <div className="intro-hero">
          <div className="intro-hero-icon">🧠</div>
          <h1>AI Finance Planner</h1>
          <p>Answer a few questions and get a personalized financial plan with investment allocations, priority actions, and growth projections.</p>
          <div className="intro-features">
            {['📊 Budget Analysis', '🎯 Investment Allocation', '🛡️ Insurance Gaps', '📈 Growth Projections', '⚡ Priority Actions'].map(f => (
              <span key={f} className="intro-feature-tag">{f}</span>
            ))}
          </div>
          <div className="intro-actions">
            <button className="btn btn-primary btn-lg" onClick={() => setStep('form')}>
              Create My Plan →
            </button>
            <button className="btn btn-secondary btn-lg" onClick={() => { setStep('result'); setActiveTab('calculators'); setPlan(null); }}>
              🧮 Calculators Only
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  // ─── Questionnaire ─────────────────────────────────────────────────────────────
  if (step === 'form') return (
    <div className="page-container">
      <div className="planner-form">
        <div className="form-header">
          <button className="btn btn-secondary btn-sm" onClick={() => setStep('intro')}>← Back</button>
          <h2>📋 Your Financial Profile</h2>
          <p>All data is used only to generate your plan — not stored permanently.</p>
        </div>

        <div className="form-grid">
          {/* Income */}
          <div className="form-section">
            <h3>💰 Income</h3>
            <div className="form-row">
              <label>Monthly Take-home Income (₹)</label>
              <input name="monthly_income" value={form.monthly_income} onChange={handleInput} type="number" placeholder="e.g., 75000" className="form-input" />
            </div>
            <div className="form-row">
              <label>Your Age</label>
              <input name="age" value={form.age} onChange={handleInput} type="number" placeholder="e.g., 28" className="form-input" />
            </div>
          </div>

          {/* Housing */}
          <div className="form-section">
            <h3>🏠 Housing</h3>
            <div className="form-row">
              <label>Housing Status</label>
              <select name="housing" value={form.housing} onChange={handleInput} className="form-input">
                <option value="rented">Renting</option>
                <option value="owned">Own Home</option>
                <option value="family">Living with Family</option>
              </select>
            </div>
            {form.housing === 'rented' && (
              <div className="form-row">
                <label>Monthly Rent (₹)</label>
                <input name="monthly_rent" value={form.monthly_rent} onChange={handleInput} type="number" placeholder="e.g., 20000" className="form-input" />
              </div>
            )}
          </div>

          {/* Monthly Expenses */}
          <div className="form-section full-width">
            <h3>🛒 Monthly Expenses</h3>
            <div className="expense-grid">
              <div className="form-row">
                <label>Food & Groceries (₹)</label>
                <input name="monthly_food" value={form.monthly_food} onChange={handleInput} type="number" placeholder="e.g., 10000" className="form-input" />
              </div>
              <div className="form-row">
                <label>Transport (₹)</label>
                <input name="monthly_transport" value={form.monthly_transport} onChange={handleInput} type="number" placeholder="e.g., 5000" className="form-input" />
              </div>
              <div className="form-row">
                <label>Utilities & Bills (₹)</label>
                <input name="monthly_utilities" value={form.monthly_utilities} onChange={handleInput} type="number" placeholder="e.g., 3000" className="form-input" />
              </div>
              <div className="form-row">
                <label>Loan EMIs (₹)</label>
                <input name="monthly_emi" value={form.monthly_emi} onChange={handleInput} type="number" placeholder="e.g., 15000" className="form-input" />
              </div>
              <div className="form-row">
                <label>Other (dining, entertainment, etc.) (₹)</label>
                <input name="monthly_other" value={form.monthly_other} onChange={handleInput} type="number" placeholder="e.g., 8000" className="form-input" />
              </div>
            </div>
          </div>

          {/* Family */}
          <div className="form-section">
            <h3>👨‍👩‍👧 Family</h3>
            <div className="form-row">
              <label>Number of Dependents</label>
              <input name="dependents" value={form.dependents} onChange={handleInput} type="number" min="0" className="form-input" />
            </div>
          </div>

          {/* Risk Appetite */}
          <div className="form-section">
            <h3>📊 Risk Appetite</h3>
            <div className="risk-buttons">
              {(['low', 'medium', 'high'] as const).map(r => (
                <button
                  key={r}
                  className={`risk-btn ${form.risk_appetite === r ? 'active' : ''} risk-${r}`}
                  onClick={() => setForm(f => ({ ...f, risk_appetite: r }))}
                >
                  {r === 'low' ? '🛡️ Low' : r === 'medium' ? '⚖️ Medium' : '🚀 High'}
                </button>
              ))}
            </div>
            <p className="form-hint">
              {form.risk_appetite === 'low' ? 'Conservative — prioritize capital preservation, less market exposure'
               : form.risk_appetite === 'medium' ? 'Balanced — mix of growth and stability'
               : 'Aggressive — maximize long-term returns, comfortable with volatility'}
            </p>
          </div>

          {/* Financial Goals */}
          <div className="form-section full-width">
            <h3>🎯 Financial Goals</h3>
            <div className="goals-grid">
              {GOALS.map(g => (
                <button
                  key={g}
                  className={`goal-tag ${form.goals.includes(g) ? 'active' : ''}`}
                  onClick={() => toggleGoal(g)}
                >
                  {form.goals.includes(g) ? '✓ ' : ''}{g}
                </button>
              ))}
            </div>
          </div>

          {/* Current Coverage */}
          <div className="form-section full-width">
            <h3>🔒 Current Protection</h3>
            <div className="checkbox-grid">
              {[
                { name: 'has_emergency_fund', label: '✅ I have an Emergency Fund (3-6 months expenses)' },
                { name: 'has_health_insurance', label: '🏥 I have Health Insurance' },
                { name: 'has_life_insurance', label: '💼 I have Life/Term Insurance' },
              ].map(c => (
                <label key={c.name} className="checkbox-label">
                  <input type="checkbox" name={c.name} checked={(form as any)[c.name]} onChange={handleInput} />
                  {c.label}
                </label>
              ))}
            </div>
          </div>
        </div>

        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <button
            className="btn btn-primary btn-lg"
            onClick={handleSubmit}
            disabled={loading || !form.monthly_income || !form.age}
          >
            {loading ? '⏳ Generating Your Plan...' : '🧠 Generate My Financial Plan →'}
          </button>
        </div>
      </div>
    </div>
  );

  // ─── Result Screen ──────────────────────────────────────────────────────────────
  return (
    <div className="page-container">
      {plan && (
        <div className="plan-header-banner" style={{ background: `linear-gradient(135deg, ${scoreColor(plan.health_score)}22, transparent)`, borderLeft: `4px solid ${scoreColor(plan.health_score)}` }}>
          <div className="phb-left">
            <div className="health-score-circle" style={{ borderColor: scoreColor(plan.health_score) }}>
              <div className="hsc-number" style={{ color: scoreColor(plan.health_score) }}>{plan.health_score}</div>
              <div className="hsc-label">Health Score</div>
            </div>
            <div>
              <div className="phb-grade" style={{ color: scoreColor(plan.health_score) }}>{plan.health_grade}</div>
              <div className="phb-sub">Financial Health Assessment</div>
            </div>
          </div>
          <button className="btn btn-secondary btn-sm" onClick={() => setStep('form')}>📋 Retake Quiz</button>
        </div>
      )}

      <div className="planner-tabs">
        <button className={`tab-btn ${activeTab === 'plan' ? 'active' : ''}`} onClick={() => setActiveTab('plan')}>
          🧠 My Plan
        </button>
        <button className={`tab-btn ${activeTab === 'calculators' ? 'active' : ''}`} onClick={() => setActiveTab('calculators')}>
          🧮 Calculators
        </button>
      </div>

      {activeTab === 'plan' && plan && (
        <div className="plan-content">
          {/* Issues + Positives */}
          <div className="plan-two-col">
            {plan.health_issues.length > 0 && (
              <div className="plan-card issues-card">
                <h3>⚠️ Issues to Address</h3>
                {plan.health_issues.map((issue, i) => (
                  <div key={i} className="issue-item">🔴 {issue}</div>
                ))}
              </div>
            )}
            {plan.health_positives.length > 0 && (
              <div className="plan-card positives-card">
                <h3>✅ What You're Doing Right</h3>
                {plan.health_positives.map((p, i) => (
                  <div key={i} className="positive-item">🟢 {p}</div>
                ))}
              </div>
            )}
          </div>

          {/* Budget Breakdown */}
          <div className="plan-card">
            <h3>💰 Budget Breakdown</h3>
            <div className="budget-grid">
              <div className="budget-item income">
                <div className="bi-label">Monthly Income</div>
                <div className="bi-value">₹{plan.budget.monthly_income.toLocaleString()}</div>
              </div>
              <div className="budget-item expense">
                <div className="bi-label">Total Expenses</div>
                <div className="bi-value">₹{plan.budget.total_expenses.toLocaleString()}</div>
              </div>
              <div className="budget-item surplus">
                <div className="bi-label">Investable Surplus</div>
                <div className="bi-value">₹{plan.budget.investable_surplus.toLocaleString()}</div>
              </div>
              <div className="budget-item rate">
                <div className="bi-label">Savings Rate</div>
                <div className="bi-value">{plan.budget.savings_rate_pct}%</div>
              </div>
            </div>
          </div>

          {/* Allocation */}
          <div className="plan-card">
            <h3>📊 Recommended Investment Allocation</h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
              Based on your age ({plan.profile_summary.age}), risk appetite ({plan.profile_summary.risk_appetite}), and surplus of ₹{plan.budget.investable_surplus.toLocaleString()}/month
            </p>
            <div className="allocation-bars">
              {[
                { key: 'equity', label: '📈 Equity', color: '#22c55e' },
                { key: 'debt', label: '🔒 Debt/Fixed', color: '#3b82f6' },
                { key: 'gold', label: '🥇 Gold', color: '#f59e0b' },
                { key: 'liquid', label: '💧 Liquid', color: '#8b5cf6' },
              ].map(({ key, label, color }) => {
                const alloc = plan.allocation[key as keyof typeof plan.allocation];
                return (
                  <div key={key} className="alloc-row">
                    <div className="alloc-label">{label}</div>
                    <div className="alloc-bar-wrap">
                      <div className="alloc-bar" style={{ width: `${alloc.pct}%`, background: color }} />
                    </div>
                    <div className="alloc-pct">{alloc.pct}%</div>
                    <div className="alloc-amt">₹{alloc.amount.toLocaleString()}/mo</div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Investment Products */}
          <div className="plan-card">
            <h3>🎯 Recommended Investment Products</h3>
            <div className="products-list">
              {plan.products.map((prod, i) => (
                <div key={i} className="product-item">
                  <div className="prod-icon">{prod.icon}</div>
                  <div className="prod-body">
                    <div className="prod-cat-badge">{prod.category}</div>
                    <div className="prod-name">{prod.name}</div>
                    <div className="prod-why">{prod.why}</div>
                  </div>
                  <div className="prod-amount">
                    <div className="pa-value">₹{Math.round(prod.amount).toLocaleString()}</div>
                    <div className="pa-label">/month</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Priority Actions */}
          <div className="plan-card">
            <h3>⚡ Priority Action Plan</h3>
            {plan.priorities.map((p) => (
              <div key={p.step} className="priority-item">
                <div className="pi-step">{p.step}</div>
                <div className="pi-body">
                  <div className="pi-action">{p.action}</div>
                  <div className="pi-timeline">⏱ {p.timeline}</div>
                  <div className="pi-detail">{p.detail}</div>
                </div>
              </div>
            ))}
          </div>

          {/* SIP Projection */}
          {plan.sip_projection && (
            <div className="plan-card projection-card">
              <h3>📈 SIP Growth Projection</h3>
              <div className="proj-grid">
                <div className="proj-item">
                  <div className="proj-label">Total Invested</div>
                  <div className="proj-value">₹{plan.sip_projection.total_invested?.toLocaleString()}</div>
                </div>
                <div className="proj-item highlight">
                  <div className="proj-label">Estimated Corpus</div>
                  <div className="proj-value">₹{plan.sip_projection.total_value?.toLocaleString()}</div>
                </div>
                <div className="proj-item">
                  <div className="proj-label">Wealth Gain</div>
                  <div className="proj-value gain">₹{plan.sip_projection.wealth_gain?.toLocaleString()}</div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'calculators' && (
        <div className="calculators-panel">
          <div className="calc-tabs">
            {[{ id: 'sip', label: '📈 SIP' }, { id: 'emi', label: '🏠 EMI' }, { id: 'tax', label: '📄 Tax' }, { id: 'retirement', label: '🏖️ Retirement' }].map(c => (
              <button key={c.id} className={`calc-tab ${calc.type === c.id ? 'active' : ''}`}
                onClick={() => setCalc(c2 => ({ ...c2, type: c.id, result: null }))}>
                {c.label}
              </button>
            ))}
          </div>

          <div className="calc-form-card">
            {calc.type === 'sip' && (
              <>
                <h3>SIP Return Calculator</h3>
                <div className="calc-inputs">
                  <div className="form-row"><label>Monthly SIP (₹)</label><input className="form-input" type="number" value={calc.amount} onChange={e => setCalc(c => ({ ...c, amount: e.target.value }))} placeholder="5000" /></div>
                  <div className="form-row"><label>Annual Return Rate (%)</label><input className="form-input" type="number" value={calc.rate} onChange={e => setCalc(c => ({ ...c, rate: e.target.value }))} placeholder="12" /></div>
                  <div className="form-row"><label>Investment Period (Years)</label><input className="form-input" type="number" value={calc.years} onChange={e => setCalc(c => ({ ...c, years: e.target.value }))} placeholder="20" /></div>
                </div>
              </>
            )}
            {calc.type === 'emi' && (
              <>
                <h3>Loan EMI Calculator</h3>
                <div className="calc-inputs">
                  <div className="form-row"><label>Loan Amount (₹)</label><input className="form-input" type="number" value={calc.loan} onChange={e => setCalc(c => ({ ...c, loan: e.target.value }))} placeholder="2000000" /></div>
                  <div className="form-row"><label>Annual Interest Rate (%)</label><input className="form-input" type="number" value={calc.rate} onChange={e => setCalc(c => ({ ...c, rate: e.target.value }))} placeholder="8.5" /></div>
                  <div className="form-row"><label>Loan Tenure (Years)</label><input className="form-input" type="number" value={calc.years} onChange={e => setCalc(c => ({ ...c, years: e.target.value }))} placeholder="20" /></div>
                </div>
              </>
            )}
            {calc.type === 'tax' && (
              <>
                <h3>Income Tax Estimator (Old Regime)</h3>
                <div className="calc-inputs">
                  <div className="form-row"><label>Annual Income (₹)</label><input className="form-input" type="number" value={calc.amount} onChange={e => setCalc(c => ({ ...c, amount: e.target.value }))} placeholder="1000000" /></div>
                </div>
              </>
            )}
            {calc.type === 'retirement' && (
              <>
                <h3>Retirement Corpus Estimator</h3>
                <div className="calc-inputs">
                  <div className="form-row"><label>Current Age</label><input className="form-input" type="number" value={calc.amount} onChange={e => setCalc(c => ({ ...c, amount: e.target.value }))} placeholder="30" /></div>
                  <div className="form-row"><label>Monthly Savings (₹)</label><input className="form-input" type="number" value={calc.loan} onChange={e => setCalc(c => ({ ...c, loan: e.target.value }))} placeholder="10000" /></div>
                  <div className="form-row"><label>Expected Annual Return (%)</label><input className="form-input" type="number" value={calc.rate} onChange={e => setCalc(c => ({ ...c, rate: e.target.value }))} placeholder="12" /></div>
                </div>
              </>
            )}

            <button className="btn btn-primary" onClick={runCalc} style={{ marginTop: '1rem' }}>Calculate</button>

            {calc.result && (
              <div className="calc-result-card">
                <h4>📊 Results</h4>
                <pre className="calc-result-pre">
                  {Object.entries(calc.result).map(([k, v]) =>
                    `${k.replace(/_/g, ' ')}: ${typeof v === 'number' ? '₹' + Math.round(v as number).toLocaleString() : v}\n`
                  ).join('')}
                </pre>
              </div>
            )}
          </div>
        </div>
      )}

      {activeTab === 'plan' && !plan && (
        <div className="empty-plan-state">
          <div style={{ fontSize: '4rem' }}>🧠</div>
          <h3>No plan generated yet</h3>
          <p>Complete the questionnaire to get your personalized financial plan.</p>
          <button className="btn btn-primary btn-lg" onClick={() => setStep('form')}>Create My Plan →</button>
        </div>
      )}
    </div>
  );
};

export default FinancePlanner;
