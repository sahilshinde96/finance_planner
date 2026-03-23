import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Login: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [pendingStatus, setPendingStatus] = useState<'pending' | 'rejected' | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.username || !form.password) return;
    setLoading(true);
    setError('');
    setPendingStatus(null);

    const result = await login(form.username, form.password);

    if (result.status === 'approved') {
      navigate('/');
    } else if (result.status === 'pending') {
      setPendingStatus('pending');
    } else if (result.status === 'rejected') {
      setPendingStatus('rejected');
    } else {
      setError(result.error || 'Login failed.');
    }
    setLoading(false);
  };

  if (pendingStatus === 'pending') {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg-primary)', padding: '2rem' }}>
        <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-xl)', padding: '3rem 2.5rem', maxWidth: '440px', width: '100%', textAlign: 'center' }}>
          <div style={{ fontSize: '56px', marginBottom: '1rem' }}>⏳</div>
          <h2 style={{ marginBottom: '0.75rem' }}>Awaiting Admin Approval</h2>
          <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7, marginBottom: '1.5rem' }}>
            Your account is registered but not yet approved. Please try again after the administrator approves your account.
          </p>
          <button className="btn btn-secondary" style={{ width: '100%' }} onClick={() => setPendingStatus(null)}>
            Back to Login
          </button>
        </div>
      </div>
    );
  }

  if (pendingStatus === 'rejected') {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg-primary)', padding: '2rem' }}>
        <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-xl)', padding: '3rem 2.5rem', maxWidth: '440px', width: '100%', textAlign: 'center' }}>
          <div style={{ fontSize: '56px', marginBottom: '1rem' }}>❌</div>
          <h2 style={{ marginBottom: '0.75rem' }}>Registration Rejected</h2>
          <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7, marginBottom: '1.5rem' }}>
            Your registration was not approved. Please contact the administrator for more information.
          </p>
          <button className="btn btn-secondary" style={{ width: '100%' }} onClick={() => setPendingStatus(null)}>
            Back to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg-primary)', padding: '2rem' }}>
      <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-xl)', padding: '2.5rem', maxWidth: '420px', width: '100%' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{ fontSize: '48px', marginBottom: '8px' }}>₳</div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>ARTH</h1>
          <p style={{ color: 'var(--text-secondary)', marginTop: '6px' }}>Sign in to your account</p>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div className="form-group">
            <label className="form-label">Username</label>
            <input className="form-input" type="text" placeholder="Enter username" value={form.username}
              onChange={e => setForm(f => ({ ...f, username: e.target.value }))} autoFocus />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input className="form-input" type="password" placeholder="Enter password" value={form.password}
              onChange={e => setForm(f => ({ ...f, password: e.target.value }))} />
          </div>

          {error && (
            <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: 'var(--radius-md)', padding: '10px 14px', color: 'var(--accent-red)', fontSize: '14px' }}>
              {error}
            </div>
          )}

          <button type="submit" className="btn btn-primary" disabled={loading || !form.username || !form.password}>
            {loading ? '⏳ Signing in...' : 'Sign In'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: '1.5rem', color: 'var(--text-secondary)', fontSize: '14px' }}>
          Don't have an account?{' '}
          <Link to="/signup" style={{ color: 'var(--accent-primary-light)', textDecoration: 'none', fontWeight: 600 }}>
            Register
          </Link>
        </p>

        <div style={{ textAlign: 'center', marginTop: '0.75rem', color: 'var(--text-muted)', fontSize: '12px' }}>
          New registrations require admin approval before access is granted.
        </div>
      </div>
    </div>
  );
};

export default Login;
