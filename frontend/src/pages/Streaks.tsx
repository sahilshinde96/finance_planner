import React, { useEffect, useState } from 'react';
import api from '../api/client';

const Streaks: React.FC = () => {
  const [streak, setStreak] = useState<any>(null);
  const [badges, setBadges] = useState<any[]>([]);
  const [allBadges, setAllBadges] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [checkedIn, setCheckedIn] = useState(false);

  useEffect(() => {
    Promise.allSettled([
      api.get('/streaks/'),
      api.get('/streaks/badges/'),
      api.get('/streaks/all-badges/'),
    ]).then(([s, b, ab]) => {
      if (s.status === 'fulfilled') setStreak(s.value.data);
      if (b.status === 'fulfilled') setBadges(b.value.data);
      if (ab.status === 'fulfilled') setAllBadges(ab.value.data);
    }).finally(() => setLoading(false));
  }, []);

  const handleCheckIn = async () => {
    try {
      await api.post('/streaks/checkin/');
      setCheckedIn(true);
      const res = await api.get('/streaks/');
      setStreak(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const earnedIds = new Set(badges.map((b: any) => b.badge?.id || b.id));

  if (loading) return <div className="page-container"><div className="loading-spinner">Loading...</div></div>;

  return (
    <div className="page-container">
      <h1 style={{ marginBottom: '1.5rem', fontSize: '1.75rem', fontWeight: 800 }}>🔥 Streaks & Achievements</h1>

      {/* Streak Hero */}
      {streak && (
        <div className="streak-hero-card">
          <div className="shc-flames">
            {[...Array(Math.min(streak.current_streak, 7))].map((_, i) => (
              <span key={i} className="shc-flame" style={{ animationDelay: `${i * 0.1}s` }}>🔥</span>
            ))}
          </div>
          <div className="shc-number">{streak.current_streak}</div>
          <div className="shc-label">Day Streak</div>
          <div className="shc-stats">
            <div className="shcs-item">
              <div className="shcs-val">⚡ {streak.total_points?.toLocaleString()}</div>
              <div className="shcs-label">Total XP</div>
            </div>
            <div className="shcs-divider" />
            <div className="shcs-item">
              <div className="shcs-val">🏆 {streak.longest_streak}</div>
              <div className="shcs-label">Best Streak</div>
            </div>
          </div>
          {!checkedIn && (
            <button className="btn btn-primary" onClick={handleCheckIn} style={{ marginTop: '1rem' }}>
              ✅ Check In Today (+10 XP)
            </button>
          )}
          {checkedIn && <div className="checkin-done">✅ Checked in today!</div>}
        </div>
      )}

      {/* XP Progress Bar */}
      {streak && (
        <div className="card" style={{ marginBottom: '1.5rem' }}>
          <h3 className="card-title">⚡ XP Level</h3>
          <div style={{ marginTop: '1rem' }}>
            {[
              { level: 'Bronze', min: 0, max: 500, color: '#cd7f32' },
              { level: 'Silver', min: 500, max: 2000, color: '#c0c0c0' },
              { level: 'Gold', min: 2000, max: 5000, color: '#f59e0b' },
              { level: 'Platinum', min: 5000, max: 15000, color: '#7c3aed' },
              { level: 'Diamond', min: 15000, max: 50000, color: '#22c55e' },
            ].map(tier => {
              const xp = streak.total_points || 0;
              const isCurrent = xp >= tier.min && xp < tier.max;
              const pct = isCurrent ? Math.min(((xp - tier.min) / (tier.max - tier.min)) * 100, 100) : xp >= tier.max ? 100 : 0;
              return (
                <div key={tier.level} className={`xp-tier ${isCurrent ? 'current' : xp >= tier.max ? 'completed' : ''}`}>
                  <div className="xp-tier-label" style={{ color: isCurrent ? tier.color : 'var(--text-muted)' }}>
                    {isCurrent ? '▶ ' : xp >= tier.max ? '✓ ' : '  '}{tier.level}
                  </div>
                  <div className="xp-tier-bar">
                    <div className="xp-tier-fill" style={{ width: `${pct}%`, background: tier.color }} />
                  </div>
                  <div className="xp-tier-range">{tier.min.toLocaleString()}–{tier.max.toLocaleString()}</div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Badges */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">🏅 Achievements ({badges.length}/{allBadges.length})</h3>
        </div>
        <div className="badges-grid">
          {allBadges.map((badge: any) => {
            const earned = earnedIds.has(badge.id);
            return (
              <div key={badge.id} className={`badge-item ${earned ? 'earned' : 'locked'}`}>
                <div className="badge-icon">{badge.icon || '🏆'}</div>
                <div className="badge-name">{badge.name}</div>
                <div className="badge-desc">{badge.description}</div>
                <div className="badge-pts">+{badge.points_value} XP</div>
                {!earned && <div className="badge-lock">🔒</div>}
              </div>
            );
          })}
        </div>
      </div>

      <style>{`
        .streak-hero-card {
          background: linear-gradient(135deg, rgba(245,158,11,0.12), rgba(239,68,68,0.08));
          border: 1px solid rgba(245,158,11,0.3);
          border-radius: 24px;
          padding: 2.5rem;
          text-align: center;
          margin-bottom: 1.5rem;
        }
        .shc-flames { font-size: 1.5rem; margin-bottom: 0.5rem; }
        .shc-flame { display: inline-block; animation: flame-pulse 1.5s ease-in-out infinite; }
        @keyframes flame-pulse { 0%,100%{transform:scale(1)} 50%{transform:scale(1.2)} }
        .shc-number { font-size: 5rem; font-weight: 900; color: #f59e0b; line-height: 1; font-family: 'Space Grotesk', sans-serif; }
        .shc-label { font-size: 1.2rem; color: var(--text-muted); margin-bottom: 1.5rem; }
        .shc-stats { display: flex; justify-content: center; align-items: center; gap: 2rem; }
        .shcs-item { text-align: center; }
        .shcs-val { font-size: 1.3rem; font-weight: 700; }
        .shcs-label { font-size: 0.75rem; color: var(--text-muted); }
        .shcs-divider { width: 1px; height: 40px; background: var(--border-color); }
        .checkin-done { margin-top: 1rem; color: var(--accent-green); font-weight: 600; }

        .xp-tier { display: grid; grid-template-columns: 80px 1fr 100px; gap: 0.75rem; align-items: center; padding: 0.375rem 0; }
        .xp-tier.current .xp-tier-label { font-weight: 700; }
        .xp-tier-label { font-size: 0.82rem; }
        .xp-tier-bar { height: 8px; background: var(--bg-tertiary); border-radius: 4px; overflow: hidden; }
        .xp-tier-fill { height: 100%; border-radius: 4px; transition: width 0.5s ease; }
        .xp-tier-range { font-size: 0.7rem; color: var(--text-muted); text-align: right; }

        .badges-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 0.875rem; }
        .badge-item {
          position: relative;
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: 14px;
          padding: 1.25rem 1rem;
          text-align: center;
          transition: all 0.2s;
        }
        .badge-item.earned {
          border-color: rgba(245,158,11,0.4);
          background: rgba(245,158,11,0.05);
        }
        .badge-item.locked { opacity: 0.55; filter: grayscale(0.7); }
        .badge-icon { font-size: 2rem; margin-bottom: 0.5rem; }
        .badge-name { font-size: 0.8rem; font-weight: 700; margin-bottom: 0.25rem; }
        .badge-desc { font-size: 0.7rem; color: var(--text-muted); margin-bottom: 0.4rem; }
        .badge-pts { font-size: 0.7rem; color: var(--accent-primary); font-weight: 600; }
        .badge-lock { position: absolute; top: 0.5rem; right: 0.5rem; font-size: 0.75rem; }
      `}</style>
    </div>
  );
};

export default Streaks;
