import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const userNav = [
  { section: 'Overview',     items: [{ to: '/',           icon: '◈', label: 'Dashboard'       }] },
  { section: 'Learn',        items: [{ to: '/quiz',    icon: '◎', label: 'Quiz Arena' }, { to: '/chatbot', icon: '◐', label: 'AI Advisor' }] },
  { section: 'Plan',         items: [{ to: '/planner', icon: '◆', label: 'Finance Planner' }, { to: '/schemes', icon: '◇', label: 'Scheme Finder' }] },
  { section: 'Achievements', items: [{ to: '/streaks',    icon: '◉', label: 'Streaks & XP'     }] },
  { section: 'Records',      items: [{ to: '/blockchain', icon: '⬡', label: 'Blockchain'       }] },
];

const adminNav = [
  { section: 'Admin',   items: [{ to: '/',        icon: '◈', label: 'User Approvals' }] },
  { section: 'App',     items: [{ to: '/quiz',    icon: '◎', label: 'Quiz Arena' }, { to: '/planner', icon: '◆', label: 'Finance Planner' }, { to: '/schemes', icon: '◇', label: 'Scheme Finder' }] },
];

const MiniChart: React.FC = () => {
  const [vals, setVals] = useState<number[]>([30, 45, 38, 52, 48, 60, 55, 70, 65, 80, 72, 88]);
  useEffect(() => {
    const id = setInterval(() => {
      setVals(prev => {
        const next = [...prev.slice(1), prev[prev.length - 1] + (Math.random() - 0.4) * 8];
        return next.map(v => Math.max(15, Math.min(95, v)));
      });
    }, 2000);
    return () => clearInterval(id);
  }, []);
  const max = Math.max(...vals), min = Math.min(...vals);
  const pts = vals.map((v, i) => `${(i / (vals.length - 1)) * 100},${100 - ((v - min) / (max - min + 1)) * 80}`).join(' ');
  return (
    <svg width="100%" height="32" viewBox="0 0 100 100" preserveAspectRatio="none" style={{ display: 'block' }}>
      <polyline points={pts} fill="none" stroke="var(--green)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" style={{ transition: 'd 0.5s ease' }} />
    </svg>
  );
};

const Sidebar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const isAdmin = user?.is_admin || user?.approval_status === 'admin';
  const nav = isAdmin ? adminNav : userNav;
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const id = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <div className="logo-icon">₳</div>
          <span className="logo-text">ARTH</span>
        </div>
        <div className="sidebar-logo-sub">{isAdmin ? 'ADMIN PANEL' : 'FINANCE TERMINAL'}</div>
      </div>

      {/* Live clock */}
      <div style={{ padding: '8px 1.25rem', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', color: 'var(--green)', fontWeight: 700 }}>
          {time.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false })}
        </span>
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '10px', color: 'var(--green)' }}>
          <span className="live-dot" style={{ width: '5px', height: '5px' }} />
          <span style={{ fontWeight: 700, letterSpacing: '0.06em' }}>LIVE</span>
        </div>
      </div>

      {/* Mini chart (user only) */}
      {!isAdmin && (
        <div style={{ padding: '10px 1.25rem 4px', borderBottom: '1px solid var(--border)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '9.5px', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: '4px' }}>
            <span>NIFTY 50</span>
            <span style={{ color: 'var(--green)' }}>+0.84%</span>
          </div>
          <MiniChart />
        </div>
      )}

      {/* Nav */}
      <nav className="sidebar-nav">
        {nav.map(section => (
          <div className="nav-section" key={section.section}>
            <div className="nav-section-title">{section.section}</div>
            {section.items.map(item => (
              <NavLink key={item.to} to={item.to} end={item.to === '/'}
                className={({ isActive }: { isActive: boolean }) => `nav-link ${isActive ? 'active' : ''}`}>
                <span className="nav-icon" style={{ fontFamily: 'monospace', fontSize: '13px' }}>{item.icon}</span>
                {item.label}
              </NavLink>
            ))}
          </div>
        ))}
      </nav>

      {/* User */}
      <div className="sidebar-user">
        <div className="sidebar-avatar">
          {user?.username?.charAt(0).toUpperCase() || '?'}
        </div>
        <div className="sidebar-user-info">
          <div className="sidebar-username">
            {user?.username}
            {isAdmin && <span style={{ marginLeft: '5px', fontSize: '9.5px', background: 'var(--green-subtle)', color: 'var(--green)', border: '1px solid var(--border-green)', borderRadius: '4px', padding: '0px 5px', fontWeight: 800, letterSpacing: '0.06em' }}>ADMIN</span>}
          </div>
          <div className="sidebar-email">{user?.email}</div>
        </div>
        <button onClick={() => { logout(); navigate('/login'); }} title="Logout"
          style={{ background: 'transparent', border: '1px solid var(--border)', borderRadius: 'var(--r-sm)', color: 'var(--text-muted)', cursor: 'pointer', padding: '5px 8px', fontSize: '13px', transition: 'all 0.18s', flexShrink: 0 }}
          onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.borderColor = 'var(--border-red)'; (e.currentTarget as HTMLButtonElement).style.color = 'var(--red)'; }}
          onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.borderColor = 'var(--border)'; (e.currentTarget as HTMLButtonElement).style.color = 'var(--text-muted)'; }}
        >
          ⏻
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
