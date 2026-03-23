import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Signup: React.FC = () => {
  const { register } = useAuth();
  const [form, setForm] = useState({ username: '', email: '', password: '', confirm: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    if (form.password !== form.confirm) { setError('Passwords do not match.'); return; }
    if (form.password.length < 6) { setError('Password must be at least 6 characters.'); return; }

    setLoading(true);
    try {
      await register(form.username, form.email, form.password);
      setSuccess(true);
    } catch (err: any) {
      const data = err.response?.data;
      const msg = data?.username?.[0] || data?.email?.[0] || data?.password?.[0] || data?.detail || 'Registration failed.';
      setError(msg);
    }
    setLoading(false);
  };

  if (success) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg-primary)', padding: '2rem' }}>
        <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-xl)', padding: '3rem 2.5rem', maxWidth: '440px', width: '100%', textAlign: 'center' }}>
          <div style={{ fontSize: '56px', marginBottom: '1rem' }}>🎉</div>
          <h2 style={{ marginBottom: '0.75rem' }}>Registration Successful!</h2>
          <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7, marginBottom: '2rem' }}>
            Your account has been created. However, you won't be able to log in until an administrator approves your registration. Please check back later.
          </p>
          <div style={{ background: 'rgba(245,158,11,0.08)', border: '1px solid rgba(245,158,11,0.25)', borderRadius: 'var(--radius-md)', padding: '1rem', marginBottom: '2rem', textAlign: 'left' }}>
            <div style={{ color: '#f59e0b', fontWeight: 600, marginBottom: '4px' }}>⏳ What happens next?</div>
            <div style={{ color: 'var(--text-secondary)', fontSize: '14px', lineHeight: 1.6 }}>
              The admin has been notified. Once your account is approved, you can sign in and access all features of ARTH.
            </div>
          </div>
          <Link to="/login" className="btn btn-primary" style={{ display: 'block', width: '100%', textAlign: 'center', textDecoration: 'none' }}>
            Go to Login
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg-primary)', padding: '2rem' }}>
      <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-xl)', padding: '2.5rem', maxWidth: '420px', width: '100%' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{ fontSize: '48px', marginBottom: '8px' }}>₳</div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>Join ARTH</h1>
          <p style={{ color: 'var(--text-secondary)', marginTop: '6px', fontSize: '14px' }}>
            Create your account — access granted after admin approval
          </p>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div className="form-group">
            <label className="form-label">Username</label>
            <input className="form-input" type="text" placeholder="Choose a username" value={form.username}
              onChange={e => setForm(f => ({ ...f, username: e.target.value }))} autoFocus />
          </div>
          <div className="form-group">
            <label className="form-label">Email</label>
            <input className="form-input" type="email" placeholder="your@email.com" value={form.email}
              onChange={e => setForm(f => ({ ...f, email: e.target.value }))} />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input className="form-input" type="password" placeholder="Min. 6 characters" value={form.password}
              onChange={e => setForm(f => ({ ...f, password: e.target.value }))} />
          </div>
          <div className="form-group">
            <label className="form-label">Confirm Password</label>
            <input className="form-input" type="password" placeholder="Repeat password" value={form.confirm}
              onChange={e => setForm(f => ({ ...f, confirm: e.target.value }))} />
          </div>

          {error && (
            <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: 'var(--radius-md)', padding: '10px 14px', color: 'var(--accent-red)', fontSize: '14px' }}>
              {error}
            </div>
          )}

          <button type="submit" className="btn btn-primary" disabled={loading || !form.username || !form.email || !form.password}>
            {loading ? '⏳ Registering...' : 'Create Account'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: '1.5rem', color: 'var(--text-secondary)', fontSize: '14px' }}>
          Already registered? <Link to="/login" style={{ color: 'var(--accent-primary-light)', textDecoration: 'none', fontWeight: 600 }}>Sign In</Link>
        </p>
      </div>
    </div>
  );
};

export default Signup;
