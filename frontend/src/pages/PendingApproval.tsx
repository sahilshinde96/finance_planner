import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const PendingApproval: React.FC<{ status?: 'pending' | 'rejected'; reason?: string }> = ({
  status = 'pending',
  reason,
}) => {
  const { logout } = useAuth();

  return (
    <div style={{
      minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: 'var(--bg-primary)', padding: '2rem',
    }}>
      <div style={{
        background: 'var(--bg-card)', border: '1px solid var(--border-color)',
        borderRadius: 'var(--radius-xl)', padding: '3rem 2.5rem',
        maxWidth: '480px', width: '100%', textAlign: 'center',
      }}>
        <div style={{ fontSize: '64px', marginBottom: '1.5rem' }}>
          {status === 'pending' ? '⏳' : '❌'}
        </div>

        <h1 style={{ fontSize: '1.6rem', fontWeight: 800, marginBottom: '0.75rem' }}>
          {status === 'pending' ? 'Awaiting Approval' : 'Registration Rejected'}
        </h1>

        {status === 'pending' ? (
          <>
            <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7, marginBottom: '2rem' }}>
              Your account has been registered and is currently under review.
              The admin will approve your access shortly. You'll be able to log in once approved.
            </p>
            <div style={{
              background: 'rgba(245,158,11,0.08)', border: '1px solid rgba(245,158,11,0.25)',
              borderRadius: 'var(--radius-md)', padding: '1rem', marginBottom: '2rem',
            }}>
              <div style={{ color: '#f59e0b', fontWeight: 600, marginBottom: '4px' }}>What happens next?</div>
              <div style={{ color: 'var(--text-secondary)', fontSize: '14px', lineHeight: 1.6 }}>
                The admin reviews new registrations and approves them manually.
                This usually takes a few hours. Please try logging in again after some time.
              </div>
            </div>
          </>
        ) : (
          <>
            <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7, marginBottom: '1rem' }}>
              Unfortunately, your registration has been rejected by the administrator.
            </p>
            {reason && (
              <div style={{
                background: 'rgba(239,68,68,0.08)', border: '1px solid rgba(239,68,68,0.25)',
                borderRadius: 'var(--radius-md)', padding: '1rem', marginBottom: '2rem',
              }}>
                <div style={{ color: 'var(--accent-red)', fontWeight: 600, marginBottom: '4px' }}>Reason</div>
                <div style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>{reason}</div>
              </div>
            )}
          </>
        )}

        <button
          onClick={logout}
          className="btn btn-secondary"
          style={{ width: '100%' }}
        >
          Back to Login
        </button>
      </div>
    </div>
  );
};

export default PendingApproval;
