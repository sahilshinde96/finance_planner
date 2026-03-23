import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../api/client';

const ProfileSetup: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    age: '', income_range: '', risk_level: 'medium',
    financial_goals: [] as string[],
    category: 'general', location: '',
  });

  const GOALS = ['Retirement', 'Home Purchase', 'Child Education', 'Emergency Fund', 'Wealth Creation', 'Car Purchase', 'Travel'];
  const CATEGORIES = [
    { id: 'general', label: 'General Public', icon: '👥' },
    { id: 'farmer', label: 'Farmer', icon: '🌾' },
    { id: 'corporate', label: 'Corporate', icon: '🏢' },
    { id: 'student', label: 'Student', icon: '🎓' },
    { id: 'business', label: 'Business Owner', icon: '💼' },
  ];

  const handleInput = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm(f => ({ ...f, [e.target.name]: e.target.value }));
  };

  const toggleGoal = (goal: string) => {
    setForm(f => ({
      ...f,
      financial_goals: f.financial_goals.includes(goal)
        ? f.financial_goals.filter(g => g !== goal)
        : [...f.financial_goals, goal],
    }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      await api.patch('/accounts/profile/', {
        ...form,
        age: parseInt(form.age) || undefined,
      });
      navigate('/');
    } catch (e) {
      console.error(e);
      navigate('/');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page" style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg-primary)', padding: '2rem' }}>
      <div className="auth-card" style={{ maxWidth: '560px', width: '100%' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{ fontSize: '48px', marginBottom: '8px' }}>₳</div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-primary)' }}>Set Up Your Profile</h1>
          <p style={{ color: 'var(--text-secondary)', marginTop: '8px' }}>
            Help ARTH personalise your financial journey, {user?.username}
          </p>
        </div>

        {/* Progress */}
        <div style={{ display: 'flex', gap: '8px', marginBottom: '2rem' }}>
          {[1, 2, 3].map(s => (
            <div key={s} style={{ flex: 1, height: '4px', borderRadius: '2px', background: s <= step ? 'var(--accent-primary)' : 'var(--border-color)', transition: 'background 0.3s' }} />
          ))}
        </div>

        {step === 1 && (
          <div>
            <h2 style={{ marginBottom: '1.5rem' }}>Who are you?</h2>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
              {CATEGORIES.map(cat => (
                <button
                  key={cat.id}
                  className={`user-type-card ${form.category === cat.id ? 'selected' : ''}`}
                  onClick={() => setForm(f => ({ ...f, category: cat.id }))}
                  style={{ textAlign: 'center', padding: '1.25rem' }}
                >
                  <div style={{ fontSize: '32px', marginBottom: '8px' }}>{cat.icon}</div>
                  <div style={{ fontWeight: 600 }}>{cat.label}</div>
                </button>
              ))}
            </div>
            <button className="btn btn-primary" style={{ width: '100%', marginTop: '24px' }} onClick={() => setStep(2)}>
              Next →
            </button>
          </div>
        )}

        {step === 2 && (
          <div>
            <h2 style={{ marginBottom: '1.5rem' }}>Basic Information</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div className="form-group">
                <label className="form-label">Your Age</label>
                <input type="number" name="age" className="form-input" placeholder="e.g. 28" value={form.age} onChange={handleInput} min={15} max={90} />
              </div>
              <div className="form-group">
                <label className="form-label">Monthly Income Range</label>
                <select name="income_range" className="form-input" value={form.income_range} onChange={handleInput}>
                  <option value="">Select range</option>
                  <option value="under_25k">Under ₹25,000</option>
                  <option value="25k_50k">₹25,000 – ₹50,000</option>
                  <option value="50k_1l">₹50,000 – ₹1,00,000</option>
                  <option value="1l_2l">₹1L – ₹2L</option>
                  <option value="above_2l">Above ₹2L</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Risk Appetite</label>
                <div style={{ display: 'flex', gap: '8px' }}>
                  {['low', 'medium', 'high'].map(r => (
                    <button
                      key={r}
                      className={`btn ${form.risk_level === r ? 'btn-primary' : 'btn-secondary'}`}
                      style={{ flex: 1, textTransform: 'capitalize' }}
                      onClick={() => setForm(f => ({ ...f, risk_level: r }))}
                    >
                      {r === 'low' ? '🛡️' : r === 'medium' ? '⚖️' : '🚀'} {r}
                    </button>
                  ))}
                </div>
              </div>
              <div className="form-group">
                <label className="form-label">Location (City/State)</label>
                <input type="text" name="location" className="form-input" placeholder="e.g. Mumbai, Maharashtra" value={form.location} onChange={handleInput} />
              </div>
            </div>
            <div style={{ display: 'flex', gap: '12px', marginTop: '24px' }}>
              <button className="btn btn-secondary" style={{ flex: 1 }} onClick={() => setStep(1)}>← Back</button>
              <button className="btn btn-primary" style={{ flex: 2 }} onClick={() => setStep(3)}>Next →</button>
            </div>
          </div>
        )}

        {step === 3 && (
          <div>
            <h2 style={{ marginBottom: '0.5rem' }}>Your Financial Goals</h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '1.5rem' }}>Select all that apply</p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginBottom: '24px' }}>
              {GOALS.map(goal => (
                <button
                  key={goal}
                  className={`category-pill ${form.financial_goals.includes(goal) ? 'active' : ''}`}
                  onClick={() => toggleGoal(goal)}
                >
                  {form.financial_goals.includes(goal) ? '✓ ' : ''}{goal}
                </button>
              ))}
            </div>
            <div style={{ display: 'flex', gap: '12px' }}>
              <button className="btn btn-secondary" style={{ flex: 1 }} onClick={() => setStep(2)}>← Back</button>
              <button className="btn btn-primary" style={{ flex: 2 }} onClick={handleSubmit} disabled={loading}>
                {loading ? '⏳ Saving...' : '🚀 Complete Setup'}
              </button>
            </div>
            <button className="btn btn-ghost" style={{ width: '100%', marginTop: '8px' }} onClick={() => navigate('/')}>
              Skip for now →
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProfileSetup;
