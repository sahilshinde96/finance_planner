import React, { useState, useEffect, useRef } from 'react';
import api from '../api/client';

interface UserRecord {
  id: number; username: string; email: string; category: string; location: string;
  registered_at: string; approval_status: string; is_approved: boolean; is_rejected: boolean;
  rejection_reason: string; approved_at: string | null; approved_by_username: string | null;
}
interface Stats { total_users: number; pending: number; approved: number; rejected: number; }

const CATEGORY_ICONS: Record<string, string> = { farmer: '🌾', corporate: '🏢', student: '🎓', business: '💼', general: '👤' };
const CATEGORY_COLORS: Record<string, string> = {
  farmer: 'var(--green)', corporate: 'var(--cyan)', student: 'var(--purple)',
  business: 'var(--gold)', general: 'var(--text-muted)'
};

const AnimCounter: React.FC<{ target: number; duration?: number }> = ({ target, duration = 800 }) => {
  const [val, setVal] = useState(0);
  const raf = useRef<number>();
  useEffect(() => {
    if (!target) { setVal(0); return; }
    const start = performance.now();
    const tick = (now: number) => {
      const t = Math.min((now - start) / duration, 1);
      setVal(Math.floor((1 - Math.pow(1 - t, 3)) * target));
      if (t < 1) raf.current = requestAnimationFrame(tick);
    };
    raf.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf.current!);
  }, [target]);
  return <>{val}</>;
};

const TABS = ['pending', 'approved', 'rejected', 'all'] as const;
type Tab = typeof TABS[number];

const AdminDashboard: React.FC = () => {
  const [tab, setTab] = useState<Tab>('pending');
  const [users, setUsers] = useState<UserRecord[]>([]);
  const [stats, setStats] = useState<Stats>({ total_users: 0, pending: 0, approved: 0, rejected: 0 });
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<number | null>(null);
  const [rejectModal, setRejectModal] = useState<{ id: number; name: string } | null>(null);
  const [rejectReason, setRejectReason] = useState('');
  const [search, setSearch] = useState('');
  const [notification, setNotification] = useState<{ msg: string; type: 'success' | 'error' } | null>(null);

  const notify = (msg: string, type: 'success' | 'error' = 'success') => {
    setNotification({ msg, type });
    setTimeout(() => setNotification(null), 3200);
  };

  const fetchData = async () => {
    setLoading(true);
    try {
      const [uRes, sRes] = await Promise.all([
        api.get(`/accounts/admin/users/?status=${tab}`),
        api.get('/accounts/admin/stats/'),
      ]);
      setUsers(uRes.data);
      setStats(sRes.data);
    } catch { /* use demo data */ }
    setLoading(false);
  };

  useEffect(() => { fetchData(); }, [tab]);

  const handleAction = async (id: number, action: 'approve' | 'reject', reason = '') => {
    setActionLoading(id);
    try {
      await api.post(`/accounts/admin/users/${id}/action/`, { action, reason });
      notify(action === 'approve' ? 'User approved successfully!' : 'User rejected.', action === 'approve' ? 'success' : 'error');
      await fetchData();
      setRejectModal(null);
      setRejectReason('');
    } catch { notify('Action failed. Please try again.', 'error'); }
    setActionLoading(null);
  };

  const fmt = (d: string | null) => {
    if (!d) return '—';
    return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
  };

  const filtered = users.filter(u =>
    !search || u.username.toLowerCase().includes(search.toLowerCase()) || u.email.toLowerCase().includes(search.toLowerCase())
  );

  const statCardsData = [
    { label: 'Total Users', val: stats.total_users, icon: '👥', color: 'var(--cyan)',   border: 'var(--border-cyan)',  glow: 'var(--cyan-glow)' },
    { label: 'Pending',     val: stats.pending,     icon: '⏳', color: 'var(--gold)',   border: 'var(--border-gold)',  glow: 'var(--gold-glow)' },
    { label: 'Approved',    val: stats.approved,    icon: '✅', color: 'var(--green)',  border: 'var(--border-green)', glow: 'var(--green-subtle)' },
    { label: 'Rejected',    val: stats.rejected,    icon: '❌', color: 'var(--red)',    border: 'var(--border-red)',   glow: 'var(--red-glow)' },
  ];

  return (
    <div className="page-container">
      {/* Toast notification */}
      {notification && (
        <div style={{
          position: 'fixed', top: '20px', right: '20px', zIndex: 9999,
          background: notification.type === 'success' ? 'var(--green-subtle)' : 'var(--red-glow)',
          border: `1px solid ${notification.type === 'success' ? 'var(--border-green)' : 'var(--border-red)'}`,
          color: notification.type === 'success' ? 'var(--green)' : 'var(--red)',
          padding: '12px 20px', borderRadius: 'var(--r-lg)', fontWeight: 600, fontSize: '14px',
          animation: 'fadeSlideUp 0.3s ease',
          boxShadow: notification.type === 'success' ? 'var(--shadow-green)' : '0 0 20px rgba(255,68,68,0.2)',
        }}>
          {notification.type === 'success' ? '✓' : '✗'} {notification.msg}
        </div>
      )}

      {/* Header */}
      <div style={{ marginBottom: '1.75rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '4px' }}>
          <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--green)', boxShadow: '0 0 8px var(--green)', animation: 'pulseDot 2s ease infinite' }} />
          <span style={{ fontSize: '11px', color: 'var(--green)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.1em' }}>Admin Panel</span>
        </div>
        <h1 style={{ fontFamily: 'var(--font-head)', fontSize: '1.8rem', fontWeight: 800 }}>User Management</h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '13px', marginTop: '3px' }}>
          Review and approve user registrations · {new Date().toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })}
        </p>
      </div>

      {/* Stat cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: '12px', marginBottom: '1.75rem' }}>
        {statCardsData.map((s, i) => (
          <div key={i} style={{
            background: 'var(--bg-card)', border: `1px solid ${s.border}`,
            borderRadius: 'var(--r-lg)', padding: '1.25rem 1.5rem',
            position: 'relative', overflow: 'hidden',
            boxShadow: `0 0 24px ${s.glow}`,
            transition: 'all 0.25s',
            cursor: 'default',
          }}
            onMouseEnter={e => { (e.currentTarget as HTMLDivElement).style.transform = 'translateY(-3px)'; }}
            onMouseLeave={e => { (e.currentTarget as HTMLDivElement).style.transform = 'translateY(0)'; }}
          >
            <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: '2px', background: s.color }} />
            <div style={{ position: 'absolute', right: '12px', bottom: '8px', fontSize: '44px', opacity: 0.07, lineHeight: 1 }}>{s.icon}</div>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '8px' }}>{s.label}</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '2.4rem', fontWeight: 800, color: s.color, lineHeight: 1, marginBottom: '6px' }}>
              <AnimCounter target={s.val} />
            </div>
            {s.label === 'Pending' && s.val > 0 && (
              <div style={{ fontSize: '11.5px', color: s.color, fontWeight: 600 }}>
                ↑ Awaiting review
              </div>
            )}
            {s.label === 'Approved' && s.val > 0 && (
              <div style={{ fontSize: '11.5px', color: 'var(--text-muted)' }}>
                {stats.total_users > 0 ? Math.round(s.val / stats.total_users * 100) : 0}% approval rate
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Controls */}
      <div style={{ display: 'flex', gap: '10px', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap' }}>
        {/* Tabs */}
        <div style={{ display: 'flex', background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 'var(--r-lg)', padding: '4px', gap: '2px' }}>
          {TABS.map(t => (
            <button key={t} onClick={() => setTab(t)} style={{
              padding: '6px 14px', borderRadius: 'var(--r-md)', border: 'none', cursor: 'pointer',
              fontFamily: 'var(--font-body)', fontSize: '12.5px', fontWeight: 600,
              transition: 'all 0.18s', textTransform: 'capitalize',
              background: tab === t ? 'var(--green-subtle)' : 'transparent',
              color: tab === t ? 'var(--green)' : 'var(--text-secondary)',
              position: 'relative',
            }}>
              {t}
              {t === 'pending' && stats.pending > 0 && (
                <span style={{ position: 'absolute', top: '-5px', right: '-4px', background: 'var(--gold)', color: 'var(--bg-base)', borderRadius: '50%', width: '16px', height: '16px', fontSize: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800 }}>
                  {stats.pending}
                </span>
              )}
            </button>
          ))}
        </div>

        {/* Search */}
        <div style={{ flex: 1, maxWidth: '320px', position: 'relative' }}>
          <span style={{ position: 'absolute', left: '11px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)', fontSize: '14px' }}>🔍</span>
          <input className="form-input" placeholder="Search username or email..." value={search}
            onChange={e => setSearch(e.target.value)}
            style={{ paddingLeft: '34px', height: '38px', fontSize: '13px' }} />
        </div>

        <button className="btn btn-secondary btn-sm" onClick={fetchData} style={{ marginLeft: 'auto' }}>
          ↻ Refresh
        </button>
      </div>

      {/* Column headers */}
      <div style={{
        display: 'grid', gridTemplateColumns: '1fr 160px 100px 160px',
        gap: '12px', padding: '6px 1.25rem', marginBottom: '6px',
        fontSize: '10.5px', fontWeight: 700, textTransform: 'uppercase',
        letterSpacing: '0.08em', color: 'var(--text-muted)',
      }}>
        <span>User</span><span>Registered</span><span>Status</span><span style={{ textAlign: 'right' }}>Actions</span>
      </div>

      {/* User list */}
      {loading ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {[1, 2, 3].map(i => (
            <div key={i} className="shimmer" style={{ height: '72px', borderRadius: 'var(--r-lg)' }} />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '4rem', color: 'var(--text-muted)' }}>
          <div style={{ fontSize: '48px', marginBottom: '12px' }}>
            {tab === 'pending' ? '⏳' : tab === 'approved' ? '✅' : tab === 'rejected' ? '❌' : '👥'}
          </div>
          <div style={{ fontSize: '15px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '4px' }}>
            No {tab === 'all' ? '' : tab} users
          </div>
          <div style={{ fontSize: '13px' }}>
            {tab === 'pending' ? 'All registrations have been reviewed.' : `No users in ${tab} state.`}
          </div>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {filtered.map((u, idx) => {
            const catColor = CATEGORY_COLORS[u.category] || 'var(--text-muted)';
            const statusColor = u.is_approved ? 'var(--green)' : u.is_rejected ? 'var(--red)' : 'var(--gold)';
            const statusBg = u.is_approved ? 'var(--green-subtle)' : u.is_rejected ? 'var(--red-glow)' : 'var(--gold-glow)';
            const statusBorder = u.is_approved ? 'var(--border-green)' : u.is_rejected ? 'var(--border-red)' : 'var(--border-gold)';
            return (
              <div key={u.id} style={{
                background: 'var(--bg-card)', border: '1px solid var(--border)',
                borderRadius: 'var(--r-lg)', padding: '1rem 1.25rem',
                display: 'grid', gridTemplateColumns: '1fr 160px 100px 160px',
                gap: '12px', alignItems: 'center',
                transition: 'all 0.2s', animation: `fadeSlideUp 0.3s ease ${idx * 0.04}s both`,
              }}
                onMouseEnter={e => { const el = e.currentTarget as HTMLDivElement; el.style.borderColor = 'var(--border-bright)'; el.style.background = 'var(--bg-card-hover)'; }}
                onMouseLeave={e => { const el = e.currentTarget as HTMLDivElement; el.style.borderColor = 'var(--border)'; el.style.background = 'var(--bg-card)'; }}
              >
                {/* User info */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', minWidth: 0 }}>
                  <div style={{
                    width: '40px', height: '40px', borderRadius: '50%', flexShrink: 0,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '18px', background: `${catColor}15`,
                    border: `1.5px solid ${catColor}44`,
                  }}>
                    {CATEGORY_ICONS[u.category] || '👤'}
                  </div>
                  <div style={{ minWidth: 0 }}>
                    <div style={{ fontWeight: 700, fontSize: '14px', display: 'flex', alignItems: 'center', gap: '7px' }}>
                      {u.username}
                      <span style={{ fontSize: '10.5px', background: `${catColor}15`, color: catColor, borderRadius: '4px', padding: '1px 7px', fontWeight: 700, textTransform: 'capitalize', letterSpacing: '0.04em', flexShrink: 0 }}>
                        {u.category}
                      </span>
                    </div>
                    <div style={{ fontSize: '12px', color: 'var(--text-muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{u.email}</div>
                    {u.location && <div style={{ fontSize: '11px', color: 'var(--text-muted)', opacity: 0.7, marginTop: '1px' }}>📍 {u.location}</div>}
                  </div>
                </div>

                {/* Date */}
                <div style={{ fontSize: '11.5px', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                  {fmt(u.registered_at)}
                  {u.approved_at && (
                    <div style={{ fontSize: '10.5px', color: u.is_approved ? 'var(--green)' : 'var(--red)', marginTop: '2px' }}>
                      {u.is_approved ? '✓' : '✗'} {fmt(u.approved_at)}
                    </div>
                  )}
                </div>

                {/* Status */}
                <div>
                  <span style={{ padding: '3px 10px', borderRadius: '999px', fontSize: '11px', fontWeight: 700, textTransform: 'capitalize', background: statusBg, color: statusColor, border: `1px solid ${statusBorder}` }}>
                    {u.approval_status}
                  </span>
                  {u.rejection_reason && (
                    <div style={{ fontSize: '10.5px', color: 'var(--red)', marginTop: '3px', opacity: 0.8 }} title={u.rejection_reason}>
                      {u.rejection_reason.slice(0, 24)}{u.rejection_reason.length > 24 ? '…' : ''}
                    </div>
                  )}
                </div>

                {/* Actions */}
                <div style={{ display: 'flex', gap: '7px', justifyContent: 'flex-end' }}>
                  {!u.is_approved && !u.is_rejected && (
                    <>
                      <button className="btn btn-sm btn-primary" disabled={actionLoading === u.id} onClick={() => handleAction(u.id, 'approve')}
                        style={{ padding: '5px 14px', fontSize: '12px' }}>
                        {actionLoading === u.id ? '⏳' : '✓ Approve'}
                      </button>
                      <button className="btn btn-sm btn-danger" disabled={actionLoading === u.id}
                        onClick={() => setRejectModal({ id: u.id, name: u.username })}>
                        ✗ Reject
                      </button>
                    </>
                  )}
                  {u.is_rejected && (
                    <button className="btn btn-sm btn-secondary" disabled={actionLoading === u.id} onClick={() => handleAction(u.id, 'approve')}>
                      ↩ Re-approve
                    </button>
                  )}
                  {u.is_approved && (
                    <button className="btn btn-sm btn-danger" disabled={actionLoading === u.id}
                      onClick={() => setRejectModal({ id: u.id, name: u.username })}
                      style={{ opacity: 0.75 }}>
                      Revoke
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Reject Modal */}
      {rejectModal && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.8)', backdropFilter: 'blur(4px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000, padding: '1rem' }}>
          <div style={{ background: 'var(--bg-card)', borderRadius: 'var(--r-2xl)', border: '1px solid var(--border-red)', padding: '2rem', maxWidth: '420px', width: '100%', boxShadow: '0 0 40px rgba(255,68,68,0.2)', animation: 'fadeSlideUp 0.25s ease' }}>
            <div style={{ fontSize: '40px', textAlign: 'center', marginBottom: '1rem' }}>⚠️</div>
            <h3 style={{ textAlign: 'center', marginBottom: '0.5rem', fontFamily: 'var(--font-head)' }}>Reject <span style={{ color: 'var(--red)' }}>{rejectModal.name}</span>?</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '13.5px', textAlign: 'center', marginBottom: '1.25rem', lineHeight: 1.6 }}>
              This user will be notified and locked out. You can re-approve them later.
            </p>
            <div className="form-group" style={{ marginBottom: '1.25rem' }}>
              <label className="form-label">Rejection reason (optional)</label>
              <input type="text" className="form-input" placeholder="e.g. Incomplete information provided"
                value={rejectReason} onChange={e => setRejectReason(e.target.value)} autoFocus />
            </div>
            <div style={{ display: 'flex', gap: '10px' }}>
              <button className="btn btn-secondary" style={{ flex: 1 }}
                onClick={() => { setRejectModal(null); setRejectReason(''); }}>
                Cancel
              </button>
              <button className="btn btn-danger" style={{ flex: 1, background: 'var(--red)', color: '#fff', border: 'none', fontWeight: 700 }}
                onClick={() => handleAction(rejectModal.id, 'reject', rejectReason)}>
                Confirm Reject
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
