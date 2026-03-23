import React, { useEffect, useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../api/client';

const TICKERS = [
  { symbol: 'NIFTY 50', price: '24,386', change: '+0.84%', up: true },
  { symbol: 'SENSEX',   price: '80,242', change: '+0.79%', up: true },
  { symbol: 'GOLD',     price: '₹72,850', change: '+0.32%', up: true },
  { symbol: 'RELIANCE', price: '₹2,948', change: '-0.41%', up: false },
  { symbol: 'TCS',      price: '₹4,102', change: '+1.12%', up: true },
  { symbol: 'USD/INR',  price: '83.92',  change: '-0.06%', up: false },
  { symbol: 'CRUDE OIL',price: '$77.34', change: '+1.20%', up: true },
  { symbol: 'BITCOIN',  price: '$67,412', change: '+2.45%', up: true },
  { symbol: 'HDFC BANK',price: '₹1,764', change: '-0.18%', up: false },
  { symbol: 'INFY',     price: '₹1,883', change: '+0.67%', up: true },
];

const AnimCounter: React.FC<{ target: number; duration?: number }> = ({ target, duration = 1200 }) => {
  const [val, setVal] = useState(0);
  const raf = useRef<number>();
  useEffect(() => {
    if (!target) return;
    const start = performance.now();
    const tick = (now: number) => {
      const t = Math.min((now - start) / duration, 1);
      setVal(Math.floor((1 - Math.pow(1 - t, 3)) * target));
      if (t < 1) raf.current = requestAnimationFrame(tick);
    };
    raf.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf.current!);
  }, [target]);
  return <>{val.toLocaleString()}</>;
};

const SparkBars: React.FC<{ up: boolean }> = ({ up }) => {
  const bars = [35, 55, 42, 68, 45, 72, 58, 80, 65, 90, 78, 95].map((h, i) => ({
    h, isUp: i > 8 ? up : Math.random() > 0.45
  }));
  return (
    <div style={{ display: 'flex', alignItems: 'flex-end', gap: '2px', height: '40px' }}>
      {bars.map((b, i) => (
        <div key={i} style={{
          width: '5px', height: `${b.h}%`,
          background: b.isUp ? 'var(--green)' : 'var(--red)',
          borderRadius: '2px', opacity: 0.6 + i * 0.03,
          animationDelay: `${i * 0.05}s`,
        }} />
      ))}
    </div>
  );
};

interface Stats { total_quizzes: number; total_xp: number; current_streak: number; total_stars: number; best_streak: number; }

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState<Stats>({ total_quizzes: 0, total_xp: 0, current_streak: 0, total_stars: 0, best_streak: 0 });
  const [recentAttempts, setRecentAttempts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.allSettled([api.get('/quiz/history/'), api.get('/streaks/')])
      .then(([h, s]) => {
        if (h.status === 'fulfilled') {
          const a = h.value.data || [];
          setRecentAttempts(a.slice(0, 5));
          setStats(p => ({ ...p, total_quizzes: a.length, total_xp: a.reduce((s: number, x: any) => s + (x.xp_earned || 0), 0), total_stars: a.reduce((s: number, x: any) => s + (x.stars || 0), 0) }));
        }
        if (s.status === 'fulfilled') {
          const d = s.value.data?.streak || s.value.data;
          setStats(p => ({ ...p, current_streak: d?.current_streak || 0, best_streak: d?.longest_streak || 0 }));
        }
      }).finally(() => setLoading(false));
  }, []);

  const greeting = () => { const h = new Date().getHours(); return h < 12 ? 'Good morning' : h < 17 ? 'Good afternoon' : 'Good evening'; };

  const markets = [
    { name: 'NIFTY 50', val: '24,386', pct: '+0.84%', up: true },
    { name: 'GOLD/g',   val: '₹7,285', pct: '+0.32%', up: true },
    { name: 'USD/INR',  val: '83.92',  pct: '-0.06%', up: false },
    { name: 'CRUDE',    val: '$77.34', pct: '+1.20%', up: true },
  ];

  const statCards = [
    { icon: '⚡', label: 'Total XP',    val: stats.total_xp,      sub: 'experience points', color: 'var(--gold)',   glow: 'rgba(240,185,11,0.15)' },
    { icon: '🎮', label: 'Quizzes',     val: stats.total_quizzes, sub: '9 modules total',   color: 'var(--cyan)',   glow: 'rgba(0,212,255,0.12)' },
    { icon: '⭐', label: 'Stars',       val: stats.total_stars,   sub: 'max 3 per quiz',    color: 'var(--purple)', glow: 'rgba(168,85,247,0.12)' },
    { icon: '🔥', label: 'Best Streak', val: stats.best_streak,   sub: 'days consecutive',  color: 'var(--red)',    glow: 'rgba(255,68,68,0.12)' },
  ];

  const actions = [
    { to: '/quiz',    icon: '🎮', label: 'Quiz Arena',   desc: 'Earn XP · Climb ranks',   border: 'var(--border-green)',  glow: 'var(--green-glow)',  c: 'var(--green)' },
    { to: '/planner', icon: '📊', label: 'Finance Plan', desc: 'AI · Personalised',        border: 'var(--border-cyan)',   glow: 'var(--cyan-glow)',   c: 'var(--cyan)' },
    { to: '/schemes', icon: '🏛️', label: 'Gov Schemes',  desc: 'Benefits you qualify for', border: 'rgba(168,85,247,0.3)', glow: 'var(--purple-glow)', c: 'var(--purple)' },
    { to: '/chatbot', icon: '🤖', label: 'AI Advisor',   desc: 'Instant finance advice',   border: 'var(--border-gold)',   glow: 'var(--gold-glow)',   c: 'var(--gold)' },
  ];

  return (
    <div className="page-container">
      {/* Ticker */}
      <div className="ticker-tape" style={{ marginBottom: '1.5rem', borderRadius: 'var(--r-md)', border: '1px solid var(--border)' }}>
        <div className="ticker-inner">
          {[...TICKERS, ...TICKERS].map((t, i) => (
            <div key={i} className="ticker-item">
              <span className="ticker-symbol">{t.symbol}</span>
              <span className="ticker-price">{t.price}</span>
              <span className={`ticker-change ${t.up ? 'up' : 'down'}`}>{t.change}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontFamily: 'var(--font-head)', fontSize: '1.75rem', fontWeight: 800, lineHeight: 1.2 }}>
            {greeting()}, <span style={{ color: 'var(--green)' }}>{user?.username}</span>
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '13px', marginTop: '3px' }}>
            Financial Command Centre · {new Date().toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'long' })}
          </p>
        </div>
        {stats.current_streak > 0 && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', background: 'var(--gold-glow)', border: '1px solid var(--border-gold)', borderRadius: 'var(--r-lg)', padding: '10px 18px' }}>
            <span style={{ fontSize: '26px', filter: 'drop-shadow(0 0 8px rgba(240,185,11,0.5))' }}>🔥</span>
            <div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.5rem', fontWeight: 800, color: 'var(--gold)', lineHeight: 1 }}>{stats.current_streak}</div>
              <div style={{ fontSize: '10px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>day streak</div>
            </div>
          </div>
        )}
      </div>

      {/* Market pulse */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: '10px', marginBottom: '1.5rem' }}>
        {markets.map((m, i) => (
          <div key={i} style={{ background: 'var(--bg-card)', border: `1px solid ${m.up ? 'var(--border-green)' : 'var(--border-red)'}`, borderRadius: 'var(--r-lg)', padding: '0.875rem 1rem', boxShadow: m.up ? 'var(--shadow-green)' : '0 0 16px rgba(255,68,68,0.08)' }}>
            <div style={{ fontSize: '10.5px', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: '4px' }}>{m.name}</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontWeight: 800, fontSize: '1.05rem', marginBottom: '6px' }}>{m.val}</div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '12px', fontWeight: 700, color: m.up ? 'var(--green)' : 'var(--red)' }}>{m.pct}</span>
              <SparkBars up={m.up} />
            </div>
          </div>
        ))}
      </div>

      {/* Stat cards */}
      <div className="stats-grid">
        {statCards.map((s, i) => (
          <div key={i} style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 'var(--r-lg)', padding: '1.25rem', position: 'relative', overflow: 'hidden', transition: 'all 0.25s ease', cursor: 'default', '--stat-color': s.color } as any}
            onMouseEnter={e => { const el = e.currentTarget as HTMLDivElement; el.style.borderColor = s.color.replace(')', '').replace('var(--', '').trim(); el.style.boxShadow = s.glow.replace('glow', 'shadow').replace('rgba', '0 0 20px rgba'); el.style.transform = 'translateY(-2px)'; }}
            onMouseLeave={e => { const el = e.currentTarget as HTMLDivElement; el.style.borderColor = 'var(--border)'; el.style.boxShadow = 'none'; el.style.transform = 'translateY(0)'; }}
          >
            <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: '2px', background: s.color, opacity: 0.7 }} />
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
              <span style={{ fontSize: '20px' }}>{s.icon}</span>
              <span style={{ fontSize: '9.5px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: s.color, background: s.glow, padding: '2px 7px', borderRadius: '999px' }}>LIVE</span>
            </div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.8rem', fontWeight: 800, color: s.color, lineHeight: 1, marginBottom: '4px' }}>
              {loading ? '—' : <AnimCounter target={s.val} />}
            </div>
            <div style={{ fontSize: '11.5px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.07em', fontWeight: 700, marginBottom: '2px' }}>{s.label}</div>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', opacity: 0.7 }}>{s.sub}</div>
          </div>
        ))}
      </div>

      {/* Quick actions */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div className="card-header">
          <h2 className="card-title">⚡ Quick Actions</h2>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '11.5px', color: 'var(--green)' }}><span className="live-dot" />Live</span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: '10px' }}>
          {actions.map(a => (
            <Link key={a.to} to={a.to} style={{ textDecoration: 'none', display: 'block' }}>
              <div style={{ background: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: 'var(--r-lg)', padding: '1.25rem 1rem', transition: 'all 0.22s ease', position: 'relative', overflow: 'hidden' }}
                onMouseEnter={e => { const el = e.currentTarget as HTMLDivElement; el.style.borderColor = a.border; el.style.boxShadow = `0 0 20px ${a.glow}`; el.style.transform = 'translateY(-3px)'; }}
                onMouseLeave={e => { const el = e.currentTarget as HTMLDivElement; el.style.borderColor = 'var(--border)'; el.style.boxShadow = 'none'; el.style.transform = 'translateY(0)'; }}
              >
                <div style={{ fontSize: '24px', marginBottom: '8px' }}>{a.icon}</div>
                <div style={{ fontWeight: 700, fontSize: '13.5px', color: 'var(--text-primary)', marginBottom: '3px' }}>{a.label}</div>
                <div style={{ fontSize: '11.5px', color: 'var(--text-muted)' }}>{a.desc}</div>
                <div style={{ position: 'absolute', bottom: '10px', right: '12px', color: a.c, fontSize: '14px', opacity: 0.6 }}>→</div>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Recent activity */}
      {recentAttempts.length > 0 ? (
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">📈 Recent Activity</h2>
            <Link to="/quiz" className="btn btn-sm btn-secondary">View All →</Link>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            {recentAttempts.map((a, i) => {
              const pct = a.total_questions > 0 ? Math.round(a.score / a.total_questions * 100) : 0;
              const c = pct >= 80 ? 'var(--green)' : pct >= 50 ? 'var(--gold)' : 'var(--red)';
              return (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '12px', background: 'var(--bg-secondary)', borderRadius: 'var(--r-md)', padding: '10px 12px', border: '1px solid var(--border)', transition: 'border-color 0.2s' }}
                  onMouseEnter={e => (e.currentTarget.style.borderColor = 'var(--border-bright)')}
                  onMouseLeave={e => (e.currentTarget.style.borderColor = 'var(--border)')}>
                  <span style={{ fontSize: '18px', width: '26px', textAlign: 'center', flexShrink: 0 }}>{a.quiz_user_type === 'farmer' ? '🌾' : a.quiz_user_type === 'corporate' ? '🏢' : '👥'}</span>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 600, fontSize: '13.5px' }}>{a.quiz_title}</div>
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px', display: 'flex', gap: '8px' }}>
                      <span>L{a.quiz_level}</span><span>·</span><span>{a.score}/{a.total_questions} correct</span><span>·</span><span>{new Date(a.completed_at).toLocaleDateString('en-IN')}</span>
                    </div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '13px', fontWeight: 700, color: c }}>{pct}%</span>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '11.5px', fontWeight: 700, color: 'var(--gold)', background: 'var(--gold-glow)', padding: '2px 8px', borderRadius: '999px' }}>⚡+{a.xp_earned}</span>
                    <span style={{ fontSize: '12px' }}>{'⭐'.repeat(a.stars || 0)}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ) : !loading && (
        <div className="card" style={{ textAlign: 'center', padding: '3rem 2rem' }}>
          <div style={{ fontSize: '3.5rem', marginBottom: '1rem', filter: 'drop-shadow(0 0 16px rgba(0,255,136,0.35))' }}>🚀</div>
          <h3 style={{ fontFamily: 'var(--font-head)', fontSize: '1.3rem', marginBottom: '0.5rem' }}>Start Your Financial Journey</h3>
          <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem', fontSize: '14px' }}>Take your first quiz to earn XP, unlock badges, and get personalized financial insights.</p>
          <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <Link to="/quiz" className="btn btn-primary btn-lg">🎮 Start First Quiz</Link>
            <Link to="/planner" className="btn btn-secondary btn-lg">📊 Finance Plan</Link>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
