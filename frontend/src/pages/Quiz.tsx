import React, { useState, useEffect, useRef, useCallback } from 'react';
import api from '../api/client';
import './Quiz.css';

// ─── Types ────────────────────────────────────────────────────────────────────
interface Question {
  id: number; text: string;
  option_a: string; option_b: string; option_c: string; option_d: string;
  hint: string; difficulty_score: number;
}
interface Quiz {
  id: number; title: string; description: string;
  difficulty: string; user_type: string; level: number;
  question_count: number; topic: string;
}
interface QuizResult {
  score: number; total: number; percentage: number;
  xp_earned: number; streak_bonus: number; stars: number;
  hearts_remaining: number; hearts_lost: number; max_streak: number;
  results: Array<{ question_id: number; question_text: string; correct_option: string; user_answer: string; is_correct: boolean; hint: string; explanation: string; }>;
}
interface LeaderboardEntry { rank: number; username: string; total_xp: number; attempts: number; total_stars: number; is_me: boolean; }

const USER_TYPES = [
  { id: 'farmer',    icon: '🌾', label: 'Farmer',       color: '#00ff88', desc: 'Crop profits, soil science, farm finance' },
  { id: 'corporate', icon: '🏢', label: 'Corporate',    color: '#00d4ff', desc: 'Markets, investing, corporate finance' },
  { id: 'general',   icon: '👥', label: 'General Public', color: '#a855f7', desc: 'Money basics, saving, planning ahead' },
];
const OPTIONS = ['A', 'B', 'C', 'D'] as const;
const OPTION_KEYS = ['option_a', 'option_b', 'option_c', 'option_d'] as const;
const TIMER_SECONDS = 25;

// ─── Particle burst on correct ────────────────────────────────────────────────
function spawnParticles(x: number, y: number, count = 12, color = '#00ff88') {
  for (let i = 0; i < count; i++) {
    const el = document.createElement('div');
    el.className = 'particle';
    const angle = (Math.PI * 2 * i) / count;
    const dist  = 60 + Math.random() * 60;
    el.style.cssText = `
      left:${x}px; top:${y}px;
      background:${color};
      --dx:${Math.cos(angle) * dist}px;
      --dy:${Math.sin(angle) * dist}px;
      animation-duration:${0.5 + Math.random() * 0.3}s;
      width:${5 + Math.random() * 5}px;
      height:${5 + Math.random() * 5}px;
    `;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 900);
  }
}

// ─── Floating XP number ───────────────────────────────────────────────────────
function spawnXP(x: number, y: number, text: string, isBonus = false) {
  const el = document.createElement('div');
  el.className = `xp-float${isBonus ? ' streak-bonus' : ''}`;
  el.textContent = text;
  el.style.left = `${x - 20}px`;
  el.style.top  = `${y - 20}px`;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 1200);
}

// ─── Quiz Selector ────────────────────────────────────────────────────────────
const QuizSelector: React.FC<{ onStart: (quiz: Quiz) => void }> = ({ onStart }) => {
  const [selectedType, setSelectedType] = useState<string | null>(null);
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [showLeaderboard, setShowLeaderboard] = useState(false);

  useEffect(() => {
    api.get('/quiz/leaderboard/').then(r => setLeaderboard(r.data)).catch(() => {});
  }, []);

  useEffect(() => {
    if (!selectedType) return;
    setLoading(true);
    api.get(`/quiz/?user_type=${selectedType}`).then(r => setQuizzes(r.data)).finally(() => setLoading(false));
  }, [selectedType]);

  const getLevelLabel = (l: number) => ['', 'Level 1 — Beginner', 'Level 2 — Intermediate', 'Level 3 — Advanced'][l] || '';
  const getLevelColor = (l: number) => ['', '#00ff88', '#f0b90b', '#ff4444'][l] || '#888';

  return (
    <div className="quiz-selector">
      <div className="quiz-selector-header">
        <h1>🎮 Quiz Arena</h1>
        <p className="quiz-selector-sub">Master financial knowledge. Earn XP. Climb the ranks.</p>
        <div className="quiz-stats-bar">
          <button className={`tab-btn ${!showLeaderboard ? 'active' : ''}`} onClick={() => setShowLeaderboard(false)}>📚 Quizzes</button>
          <button className={`tab-btn ${showLeaderboard ? 'active' : ''}`} onClick={() => setShowLeaderboard(true)}>🏆 Leaderboard</button>
        </div>
      </div>

      {showLeaderboard ? (
        <div className="leaderboard-panel">
          <h2>🏆 Top Learners</h2>
          <div className="leaderboard-list">
            {leaderboard.length === 0 && <p className="empty-state">No scores yet. Be the first!</p>}
            {leaderboard.map(e => (
              <div key={e.rank} className={`leaderboard-entry ${e.is_me ? 'is-me' : ''}`} style={{ animationDelay: `${e.rank * 0.05}s` }}>
                <div className="lb-rank">{e.rank === 1 ? '🥇' : e.rank === 2 ? '🥈' : e.rank === 3 ? '🥉' : `#${e.rank}`}</div>
                <div className="lb-user">
                  <div className="lb-username">{e.username}{e.is_me && <span className="you-badge">YOU</span>}</div>
                  <div className="lb-stats">{e.attempts} quizzes · {'⭐'.repeat(Math.min(e.total_stars, 5))}</div>
                </div>
                <div className="lb-xp">⚡ {e.total_xp.toLocaleString()} XP</div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <>
          <div className="user-type-grid">
            {USER_TYPES.map(ut => (
              <button key={ut.id} className={`user-type-card ${selectedType === ut.id ? 'selected' : ''}`}
                style={{ '--card-color': ut.color } as any} onClick={() => setSelectedType(ut.id)}>
                <span className="utc-icon">{ut.icon}</span>
                <div className="utc-label">{ut.label}</div>
                <div className="utc-desc">{ut.desc}</div>
                {selectedType === ut.id && <div className="utc-check">✓ Selected</div>}
              </button>
            ))}
          </div>

          {selectedType && (
            <div className="quiz-levels" style={{ animation: 'fadeUp 0.3s ease' }}>
              <h2>{USER_TYPES.find(u => u.id === selectedType)?.icon} {USER_TYPES.find(u => u.id === selectedType)?.label} Quizzes</h2>
              {loading && <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '1rem' }}>⏳ Loading quizzes...</div>}
              <div className="quiz-cards-grid">
                {quizzes.map((quiz, i) => (
                  <div key={quiz.id} className="quiz-card" onClick={() => onStart(quiz)} style={{ animationDelay: `${i * 0.07}s` }}>
                    <div className="qc-level-badge" style={{ background: getLevelColor(quiz.level) }}>{getLevelLabel(quiz.level)}</div>
                    <div className="qc-title">{quiz.title}</div>
                    <div className="qc-desc">{quiz.description}</div>
                    <div className="qc-meta">
                      <span>❓ {quiz.question_count || 8} questions</span>
                      <span className={`qc-diff diff-${quiz.difficulty}`}>
                        {quiz.difficulty === 'easy' ? '🟢' : quiz.difficulty === 'medium' ? '🟡' : '🔴'} {quiz.difficulty}
                      </span>
                    </div>
                    <button className="btn btn-primary qc-start-btn">Start Quiz →</button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

// ─── Countdown Timer ──────────────────────────────────────────────────────────
const CountdownTimer: React.FC<{ seconds: number; total: number; onExpire: () => void }> = ({ seconds, total }) => {
  const pct = seconds / total;
  const circumference = 2 * Math.PI * 18;
  const dashOffset = circumference * (1 - pct);
  const color = seconds > 10 ? 'var(--green)' : seconds > 5 ? 'var(--gold)' : 'var(--red)';
  return (
    <div className="timer-circle">
      <svg className="timer-svg" width="48" height="48" viewBox="0 0 40 40">
        <circle className="timer-track" cx="20" cy="20" r="18" />
        <circle className="timer-fill" cx="20" cy="20" r="18"
          stroke={color} strokeDasharray={circumference}
          strokeDashoffset={dashOffset}
          style={{ transition: 'stroke-dashoffset 1s linear, stroke 0.5s' }} />
      </svg>
      <div className="timer-num" style={{ color }}>{seconds}</div>
    </div>
  );
};

// ─── Quiz Game ────────────────────────────────────────────────────────────────
const QuizGame: React.FC<{ quiz: Quiz; questions: Question[]; onFinish: (r: QuizResult) => void; onBack: () => void }> = ({ quiz, questions, onFinish, onBack }) => {
  const [idx, setIdx]                   = useState(0);
  const [selected, setSelected]         = useState<string | null>(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [answers, setAnswers]           = useState<Record<string, string>>({});
  const [hearts, setHearts]             = useState(3);
  const [streak, setStreak]             = useState(0);
  const [xp, setXp]                     = useState(0);
  const [showHint, setShowHint]         = useState(false);
  const [submitting, setSubmitting]     = useState(false);
  const [flashState, setFlashState]     = useState<'idle' | 'correct' | 'wrong'>('idle');
  const [timeLeft, setTimeLeft]         = useState(TIMER_SECONDS);
  const [timerActive, setTimerActive]   = useState(true);
  const [xpBump, setXpBump]             = useState(false);
  const [localCorrect, setLocalCorrect] = useState<boolean | null>(null);

  const confirmBtnRef = useRef<HTMLButtonElement>(null);
  const q = questions[idx];
  const progress = (idx / questions.length) * 100;
  const isLast = idx === questions.length - 1;

  // Timer
  useEffect(() => {
    if (!timerActive || showFeedback) return;
    if (timeLeft <= 0) { handleTimeUp(); return; }
    const id = setTimeout(() => setTimeLeft(t => t - 1), 1000);
    return () => clearTimeout(id);
  }, [timeLeft, timerActive, showFeedback]);

  // Reset timer on new question
  useEffect(() => {
    setTimeLeft(TIMER_SECONDS);
    setTimerActive(true);
    setFlashState('idle');
    setLocalCorrect(null);
  }, [idx]);

  const handleTimeUp = () => {
    if (showFeedback) return;
    setTimerActive(false);
    setHearts(h => Math.max(0, h - 1));
    setStreak(0);
    setShowFeedback(true);
    setFlashState('wrong');
    setLocalCorrect(false);
    const newAnswers = { ...answers, [q.id]: '' };
    setAnswers(newAnswers);
    if (isLast) submitQuiz(newAnswers);
  };

  const handleSelect = (opt: string) => { if (!showFeedback && timerActive) setSelected(opt); };

  const handleConfirm = useCallback((_e?: React.MouseEvent) => {
    if (!selected || showFeedback) return;
    setTimerActive(false);
    setShowFeedback(true);

    const newAnswers = { ...answers, [q.id]: selected };
    setAnswers(newAnswers);

    // Determine correctness by checking if the option matches correct_option from API
    // We reveal it by comparing — actual check is backend; local is visual only
    const isCorrect = localCheck(selected, q);
    setLocalCorrect(isCorrect);

    if (isCorrect) {
      const newStreak = streak + 1;
      setStreak(newStreak);
      const gained = 10 + (newStreak > 2 ? 5 : 0);
      setXp(x => x + gained);
      setFlashState('correct');
      setXpBump(true);
      setTimeout(() => setXpBump(false), 600);

      // Particles + floating XP
      const btn = confirmBtnRef.current;
      if (btn) {
        const rect = btn.getBoundingClientRect();
        const cx = rect.left + rect.width / 2;
        const cy = rect.top + rect.height / 2;
        spawnParticles(cx, cy, 14, '#00ff88');
        spawnXP(cx, cy, `+${gained} XP`);
        if (newStreak > 2) spawnXP(cx - 40, cy - 30, `🔥 ×${newStreak} Streak!`, true);
      }
    } else {
      setStreak(0);
      setHearts(h => Math.max(0, h - 1));
      setFlashState('wrong');

      const btn = confirmBtnRef.current;
      if (btn) {
        const rect = btn.getBoundingClientRect();
        spawnParticles(rect.left + rect.width / 2, rect.top + rect.height / 2, 8, '#ff4444');
      }
    }

    if (isLast) submitQuiz(newAnswers);
  }, [selected, showFeedback, answers, streak, q, isLast, idx]);

  // Simple local check — actual truth from backend; this is just for immediate UI
  const localCheck = (opt: string, question: Question): boolean => {
    // We don't have correct_option in Question type (hidden by API), so we optimistically
    // treat selection as pending — actual result comes from backend
    // For immediate feedback, we'll just show "selected" and let backend decide
    // But for better UX, we do have access to it if serializer exposes it
    return (question as any).correct_option === opt;
  };

  const submitQuiz = async (finalAnswers: Record<string, string>) => {
    setSubmitting(true);
    try {
      const res = await api.post('/quiz/submit/', { quiz_id: quiz.id, answers: finalAnswers });
      setTimeout(() => onFinish(res.data), 800);
    } catch {
      // Fallback: compute locally
      const total = questions.length;
      const score = Object.entries(finalAnswers).filter(([qid, ans]) => {
        const q2 = questions.find(q => q.id === parseInt(qid));
        return q2 && (q2 as any).correct_option === ans;
      }).length;
      const pct = Math.round(score / total * 100);
      setTimeout(() => onFinish({
        score, total, percentage: pct, xp_earned: xp,
        streak_bonus: streak * 5, stars: pct >= 90 ? 3 : pct >= 60 ? 2 : pct >= 30 ? 1 : 0,
        hearts_remaining: hearts, hearts_lost: 3 - hearts, max_streak: streak, results: [],
      }), 800);
    }
    setSubmitting(false);
  };

  const handleNext = () => {
    if (isLast) return;
    setIdx(i => i + 1);
    setSelected(null);
    setShowFeedback(false);
    setShowHint(false);
  };

  return (
    <div className="quiz-game">
      {/* Header */}
      <div className="qg-header">
        <button className="qg-back" onClick={() => window.confirm('Quit quiz? Progress will be lost.') && onBack()}>✕</button>
        <div className="qg-progress-wrap">
          <div className="qg-progress-bar" style={{ width: `${progress}%` }} />
        </div>
        <CountdownTimer seconds={timeLeft} total={TIMER_SECONDS} onExpire={handleTimeUp} />
        <div className="qg-hearts">
          {[0, 1, 2].map(i => (
            <span key={i} className={`heart ${i < hearts ? 'active' : 'lost'}`}>
              {i < hearts ? '❤️' : '🖤'}
            </span>
          ))}
        </div>
      </div>

      {/* Stats bar */}
      <div className="qg-stats">
        <div className={`qg-xp ${xpBump ? 'bump' : ''}`}>⚡ {xp} XP</div>
        <div className="qg-streak">
          {streak > 0 ? (
            <>
              <span className="streak-flame-icon">🔥</span>
              <span style={{ fontFamily: 'var(--font-mono)' }}>{streak}</span>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>streak</span>
            </>
          ) : (
            <span style={{ color: 'var(--text-muted)', fontSize: '12px' }}>No streak yet</span>
          )}
        </div>
        <div className="qg-counter">{idx + 1} / {questions.length}</div>
      </div>

      {/* Question */}
      <div className={`qg-question-card ${flashState === 'correct' ? 'correct-flash' : flashState === 'wrong' ? 'wrong-flash' : ''}`}
        key={q.id}>
        <div className="qg-q-number">Question {idx + 1} of {questions.length}</div>
        <div className="qg-q-text">{q.text}</div>
        {q.hint && (
          <div className="qg-hint-area">
            {showHint
              ? <div className="qg-hint-reveal">💡 {q.hint}</div>
              : !showFeedback && <button className="btn-hint" onClick={() => setShowHint(true)}>💡 Reveal Hint</button>
            }
          </div>
        )}
      </div>

      {/* Options */}
      <div className="qg-options" key={`opts-${idx}`}>
        {OPTIONS.map((opt, i) => {
          const text = q[OPTION_KEYS[i]];
          const correctOpt = (q as any).correct_option;
          const isCorrect  = showFeedback && correctOpt && opt === correctOpt;
          const isWrong    = showFeedback && selected === opt && correctOpt && opt !== correctOpt;
          const isDim      = showFeedback && opt !== selected && !isCorrect;

          let cls = 'qg-option';
          if (!showFeedback && selected === opt) cls += ' selected';
          if (isCorrect) cls += ' correct';
          if (isWrong)   cls += ' wrong';
          if (isDim)     cls += ' dim';

          return (
            <button key={opt} className={cls} onClick={() => handleSelect(opt)} disabled={showFeedback}>
              <span className="opt-letter">{opt}</span>
              <span className="opt-text">{text}</span>
              {isCorrect && <span className="opt-icon">✓</span>}
              {isWrong   && <span className="opt-icon">✗</span>}
            </button>
          );
        })}
      </div>

      {/* Explanation on wrong */}
      {showFeedback && localCorrect === false && (q as any).explanation && (
        <div className="qg-explanation">
          <div className="qg-explanation-title">📖 Explanation</div>
          <div className="qg-explanation-text">{(q as any).explanation}</div>
        </div>
      )}

      {/* Action button */}
      <div className="qg-actions">
        {!showFeedback ? (
          <button ref={confirmBtnRef} className={`btn btn-primary btn-confirm ${selected ? 'active' : ''}`}
            onClick={handleConfirm} disabled={!selected}>
            {isLast ? '🏁 Submit Quiz' : '✓ Confirm Answer'}
          </button>
        ) : isLast ? (
          <button className="btn btn-primary btn-confirm" disabled style={{ opacity: 0.7 }}>
            {submitting ? '⚡ Calculating results...' : '✅ Quiz Complete!'}
          </button>
        ) : (
          <button className="btn btn-primary btn-confirm" onClick={handleNext} style={{ animation: 'bounceIn 0.4s ease' }}>
            Continue → {idx + 2}/{questions.length}
          </button>
        )}
      </div>
    </div>
  );
};

// ─── Results Screen ───────────────────────────────────────────────────────────
const QuizResults: React.FC<{ result: QuizResult; quiz: Quiz; onRetry: () => void; onBack: () => void }> = ({ result, onRetry, onBack }) => {
  const [showReview, setShowReview] = useState(false);
  const circumference = 2 * Math.PI * 40;
  const fillAmt = (result.percentage / 100) * circumference;

  const emoji      = result.percentage >= 90 ? '🏆' : result.percentage >= 60 ? '🎉' : result.percentage >= 30 ? '💪' : '📚';
  const msg        = result.percentage >= 90 ? 'Outstanding!' : result.percentage >= 60 ? 'Well Done!' : result.percentage >= 30 ? 'Keep Practicing!' : "Don't Give Up!";
  const ringColor  = result.percentage >= 80 ? 'var(--green)' : result.percentage >= 50 ? 'var(--gold)' : 'var(--red)';

  useEffect(() => {
    // Confetti burst on load if good score
    if (result.percentage >= 60) {
      setTimeout(() => {
        const colors = ['#00ff88', '#00d4ff', '#f0b90b', '#a855f7', '#ff4444'];
        for (let i = 0; i < 30; i++) {
          setTimeout(() => {
            spawnParticles(
              100 + Math.random() * (window.innerWidth - 200),
              window.innerHeight * 0.3,
              6,
              colors[Math.floor(Math.random() * colors.length)]
            );
          }, i * 60);
        }
      }, 400);
    }
  }, []);

  return (
    <div className="quiz-results">
      <div className="qr-card">
        <span className="qr-emoji">{emoji}</span>

        <div className="qr-stars">
          {[1, 2, 3].map(i => (
            <span key={i} className={`star ${i <= result.stars ? 'earned' : ''}`}>⭐</span>
          ))}
        </div>

        <div className="qr-title">{msg}</div>

        {/* Animated ring */}
        <div className="qr-score-ring">
          <svg width="130" height="130" viewBox="0 0 100 100" className="score-ring-svg">
            <circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="7" />
            <circle cx="50" cy="50" r="40" fill="none"
              stroke={ringColor} strokeWidth="7"
              strokeDasharray={`0 ${circumference}`}
              strokeLinecap="round"
              transform="rotate(-90 50 50)"
              className="score-ring-circle"
              style={{
                '--fill': `${fillAmt}`,
                strokeDasharray: `${fillAmt} ${circumference}`,
                transition: 'stroke-dasharray 1.2s ease 0.5s',
              } as any}
            />
          </svg>
          <div className="score-ring-text">
            <div className="score-pct" style={{ color: ringColor }}>{result.percentage.toFixed(0)}%</div>
            <div className="score-frac">{result.score}/{result.total}</div>
          </div>
        </div>

        {/* XP bar */}
        <div style={{ marginBottom: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: 'var(--text-muted)', marginBottom: '4px', fontFamily: 'var(--font-mono)' }}>
            <span>XP Earned</span>
            <span style={{ color: 'var(--gold)', fontWeight: 700 }}>+{result.xp_earned} XP</span>
          </div>
          <div className="xp-bar-wrap">
            <div className="xp-bar-fill" style={{ '--xp-pct': `${Math.min(100, result.xp_earned / 2)}%` } as any} />
          </div>
        </div>

        {result.streak_bonus > 0 && (
          <div className="streak-bonus-pill">
            🔥 Streak Bonus: +{result.streak_bonus} XP
          </div>
        )}

        {/* Stats */}
        <div className="qr-stats-grid">
          {[
            { val: `⚡ ${result.xp_earned}`,        label: 'XP Earned'    },
            { val: `🔥 ×${result.max_streak}`,      label: 'Best Streak'  },
            { val: `❤️ ${result.hearts_remaining}`, label: 'Hearts Left'  },
            { val: `🎯 ${result.score}/${result.total}`, label: 'Score'   },
          ].map((s, i) => (
            <div key={i} className="qr-stat" style={{ animationDelay: `${0.4 + i * 0.1}s` }}>
              <div className="qrs-value" style={{ fontFamily: 'var(--font-mono)' }}>{s.val}</div>
              <div className="qrs-label">{s.label}</div>
            </div>
          ))}
        </div>

        <div className="qr-actions">
          <button className="btn btn-primary" style={{ padding: '14px' }} onClick={onRetry}>🔄 Try Again</button>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button className="btn btn-secondary" style={{ flex: 1 }} onClick={onBack}>← All Quizzes</button>
            <button className="btn btn-secondary" style={{ flex: 1 }} onClick={() => setShowReview(r => !r)}>
              {showReview ? '▲ Hide' : '📖 Review'}
            </button>
          </div>
        </div>
      </div>

      {showReview && (
        <div className="qr-review">
          <h3>📖 Answer Review</h3>
          {result.results.length === 0
            ? <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '1rem' }}>Detailed review requires backend connection.</p>
            : result.results.map((r, i) => (
              <div key={r.question_id} className={`review-item ${r.is_correct ? 'correct' : 'incorrect'}`} style={{ animationDelay: `${i * 0.04}s` }}>
                <div className="ri-header">
                  <span className="ri-num">Q{i + 1}</span>
                  <span className="ri-status">{r.is_correct ? '✅ Correct' : '❌ Wrong'}</span>
                </div>
                <div className="ri-question">{r.question_text}</div>
                <div className="ri-answers">
                  <span className="ri-your">Your answer: <strong>{r.user_answer || '—'}</strong></span>
                  {!r.is_correct && <span className="ri-correct">Correct: <strong>{r.correct_option}</strong></span>}
                </div>
                {r.explanation && <div className="ri-explanation">💡 {r.explanation}</div>}
              </div>
            ))}
        </div>
      )}
    </div>
  );
};

// ─── Main Quiz Page ───────────────────────────────────────────────────────────
const QuizPage: React.FC = () => {
  const [phase, setPhase] = useState<'select' | 'game' | 'results'>('select');
  const [activeQuiz, setActiveQuiz] = useState<Quiz | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [result, setResult] = useState<QuizResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleStart = async (quiz: Quiz) => {
    setLoading(true);
    try {
      const res = await api.get(`/quiz/${quiz.id}/`);
      setActiveQuiz(quiz);
      setQuestions(res.data.questions || []);
      setPhase('game');
    } catch { console.error('Failed to load quiz'); }
    finally { setLoading(false); }
  };

  const handleFinish = (res: QuizResult) => { setResult(res); setPhase('results'); };
  const handleRetry  = async () => { if (activeQuiz) await handleStart(activeQuiz); };
  const handleBack   = () => { setPhase('select'); setActiveQuiz(null); setQuestions([]); setResult(null); };

  if (loading) return (
    <div className="page-container"><div className="loading-state">
      <div className="loading-spinner-large">⚡</div>
      <p style={{ fontFamily: 'var(--font-mono)', fontSize: '13px', letterSpacing: '0.1em' }}>LOADING QUIZ...</p>
    </div></div>
  );

  return (
    <div className="page-container quiz-page">
      {phase === 'select'  && <QuizSelector onStart={handleStart} />}
      {phase === 'game'    && activeQuiz && <QuizGame quiz={activeQuiz} questions={questions} onFinish={handleFinish} onBack={handleBack} />}
      {phase === 'results' && result && activeQuiz && <QuizResults result={result} quiz={activeQuiz} onRetry={handleRetry} onBack={handleBack} />}
    </div>
  );
};

export default QuizPage;
