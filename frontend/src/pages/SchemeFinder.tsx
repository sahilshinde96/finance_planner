import React, { useState, useEffect } from 'react';
import api from '../api/client';

interface Scheme {
  id: number;
  name: string;
  description: string;
  category: string;
  benefits: string;
  eligibility_criteria: string;
  min_age?: number;
  max_age?: number;
  max_income?: number;
  state: string;
  applicable_categories: string;
}

const CATEGORIES = [
  { id: '', label: 'All Categories', icon: '🏛️' },
  { id: 'savings', label: 'Savings', icon: '💰' },
  { id: 'insurance', label: 'Insurance', icon: '🛡️' },
  { id: 'pension', label: 'Pension', icon: '👴' },
  { id: 'business', label: 'Business/MSME', icon: '🏢' },
  { id: 'education', label: 'Education', icon: '🎓' },
  { id: 'subsidy', label: 'Subsidy', icon: '🌾' },
  { id: 'health', label: 'Healthcare', icon: '🏥' },
];

const SchemeFinder: React.FC = () => {
  const [schemes, setSchemes] = useState<Scheme[]>([]);
  const [filtered, setFiltered] = useState<Scheme[]>([]);
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState('');
  const [search, setSearch] = useState('');
  const [age, setAge] = useState('');
  const [income, setIncome] = useState('');
  const [expanded, setExpanded] = useState<number | null>(null);

  useEffect(() => {
    setLoading(true);
    api.get('/schemes/')
      .then(r => { setSchemes(r.data); setFiltered(r.data); })
      .catch(() => {
        // Demo data
        const demo: Scheme[] = [
          { id: 1, name: 'PM Jan Dhan Yojana', description: 'Financial inclusion — zero-balance bank accounts for all', category: 'savings', benefits: 'Zero-balance account, RuPay card, ₹2L accident insurance, ₹30K life insurance', eligibility_criteria: 'Any Indian citizen 10+ years', state: 'All India', applicable_categories: 'General,SC,ST,OBC' },
          { id: 2, name: 'Sukanya Samriddhi Yojana', description: 'High-interest savings for girl children', category: 'savings', benefits: '8.2% interest, tax-free, 80C deduction, ₹1.5L max annual', eligibility_criteria: 'Parents of girl child below 10 years', max_age: 10, state: 'All India', applicable_categories: 'General,SC,ST,OBC' },
          { id: 3, name: 'Atal Pension Yojana', description: 'Guaranteed pension for unorganized sector workers', category: 'pension', benefits: '₹1,000–5,000/month pension after age 60', eligibility_criteria: 'Age 18-40 with savings bank account', min_age: 18, max_age: 40, state: 'All India', applicable_categories: 'General,SC,ST,OBC' },
          { id: 4, name: 'PM Mudra Yojana', description: 'Collateral-free business loans for micro enterprises', category: 'business', benefits: 'Up to ₹10L loan: Shishu (₹50K), Kishore (₹5L), Tarun (₹10L)', eligibility_criteria: 'Any Indian with non-farm business plan, age 18+', min_age: 18, state: 'All India', applicable_categories: 'General,SC,ST,OBC' },
          { id: 5, name: 'PM Kisan Samman Nidhi', description: 'Direct income support for farmers', category: 'subsidy', benefits: '₹6,000/year in 3 installments to bank account', eligibility_criteria: 'Small/marginal farmers with cultivable land', min_age: 18, state: 'All India', applicable_categories: 'General,SC,ST,OBC' },
          { id: 6, name: 'PM Fasal Bima Yojana', description: 'Comprehensive crop insurance scheme', category: 'insurance', benefits: 'Crop failure coverage: 2% premium Kharif, 1.5% Rabi', eligibility_criteria: 'All farmers growing notified crops', min_age: 18, state: 'All India', applicable_categories: 'General,SC,ST,OBC' },
          { id: 7, name: 'National Scholarship Portal', description: 'Merit-cum-means scholarships for students', category: 'education', benefits: 'Full tuition + monthly stipend + book allowance', eligibility_criteria: 'Students from families with income below ₹8L', min_age: 16, max_age: 30, max_income: 800000, state: 'All India', applicable_categories: 'SC,ST,OBC' },
          { id: 8, name: 'NPS (National Pension System)', description: 'Market-linked voluntary retirement savings', category: 'pension', benefits: 'Extra ₹50K tax deduction (80CCD), flexible allocation', eligibility_criteria: 'Any Indian citizen age 18-70', min_age: 18, max_age: 70, state: 'All India', applicable_categories: 'General,SC,ST,OBC' },
        ];
        setSchemes(demo);
        setFiltered(demo);
      })
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    let result = schemes;
    if (category) result = result.filter(s => s.category === category);
    if (search) {
      const q = search.toLowerCase();
      result = result.filter(s => s.name.toLowerCase().includes(q) || s.description.toLowerCase().includes(q) || s.benefits.toLowerCase().includes(q));
    }
    if (age) {
      const a = parseInt(age);
      result = result.filter(s => {
        if (s.min_age && a < s.min_age) return false;
        if (s.max_age && a > s.max_age) return false;
        return true;
      });
    }
    if (income) {
      const inc = parseInt(income);
      result = result.filter(s => !s.max_income || inc <= s.max_income);
    }
    setFiltered(result);
  }, [schemes, category, search, age, income]);

  const getCatIcon = (cat: string) => CATEGORIES.find(c => c.id === cat)?.icon || '🏛️';

  const getCatColor = (cat: string) => ({
    savings: '#22c55e', insurance: '#3b82f6', pension: '#a855f7',
    business: '#f59e0b', education: '#06b6d4', subsidy: '#84cc16',
    health: '#ec4899', housing: '#f97316'
  }[cat] || '#6b7280');

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1 className="page-title">🏛️ Government Scheme Finder</h1>
          <p className="page-subtitle">Discover schemes you're eligible for based on your profile</p>
        </div>
        <div className="scheme-count-badge">{filtered.length} schemes found</div>
      </div>

      {/* Filters */}
      <div className="scheme-filters card">
        <div className="filter-row">
          <div className="form-group" style={{ flex: 2 }}>
            <label className="form-label">🔍 Search</label>
            <input
              type="text" className="form-input" placeholder="Search schemes..."
              value={search} onChange={e => setSearch(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label className="form-label">👤 Your Age</label>
            <input
              type="number" className="form-input" placeholder="e.g. 28"
              value={age} onChange={e => setAge(e.target.value)} min={1} max={100}
            />
          </div>
          <div className="form-group">
            <label className="form-label">💰 Annual Income (₹)</label>
            <input
              type="number" className="form-input" placeholder="e.g. 500000"
              value={income} onChange={e => setIncome(e.target.value)} min={0}
            />
          </div>
        </div>

        <div className="category-pills">
          {CATEGORIES.map(cat => (
            <button
              key={cat.id}
              className={`category-pill ${category === cat.id ? 'active' : ''}`}
              onClick={() => setCategory(cat.id)}
            >
              {cat.icon} {cat.label}
            </button>
          ))}
        </div>
      </div>

      {/* Schemes list */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px', color: 'var(--text-muted)' }}>
          <div style={{ fontSize: '40px' }}>🏛️</div>
          <p style={{ marginTop: '12px' }}>Loading schemes...</p>
        </div>
      ) : filtered.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '60px', color: 'var(--text-muted)' }}>
          <div style={{ fontSize: '40px' }}>😕</div>
          <p style={{ marginTop: '12px' }}>No schemes match your filters.</p>
          <button className="btn btn-secondary" style={{ marginTop: '12px' }} onClick={() => { setCategory(''); setSearch(''); setAge(''); setIncome(''); }}>
            Clear Filters
          </button>
        </div>
      ) : (
        <div className="schemes-list">
          {filtered.map(scheme => (
            <div key={scheme.id} className="scheme-card card">
              <div className="scheme-card-header" onClick={() => setExpanded(expanded === scheme.id ? null : scheme.id)}>
                <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                  <div className="scheme-cat-icon" style={{ background: getCatColor(scheme.category) + '22', color: getCatColor(scheme.category) }}>
                    {getCatIcon(scheme.category)}
                  </div>
                  <div style={{ flex: 1 }}>
                    <h3 className="scheme-name">{scheme.name}</h3>
                    <p className="scheme-desc">{scheme.description}</p>
                    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '8px' }}>
                      <span className="scheme-tag" style={{ background: getCatColor(scheme.category) + '22', color: getCatColor(scheme.category) }}>
                        {scheme.category}
                      </span>
                      <span className="scheme-tag">🗺️ {scheme.state}</span>
                    </div>
                  </div>
                </div>
                <button className="btn btn-ghost btn-sm">{expanded === scheme.id ? '▲' : '▼'}</button>
              </div>

              {expanded === scheme.id && (
                <div className="scheme-details">
                  <div className="scheme-detail-grid">
                    <div className="scheme-detail-item">
                      <div className="scheme-detail-label">🎁 Benefits</div>
                      <div className="scheme-detail-value">{scheme.benefits}</div>
                    </div>
                    <div className="scheme-detail-item">
                      <div className="scheme-detail-label">✅ Eligibility</div>
                      <div className="scheme-detail-value">{scheme.eligibility_criteria}</div>
                    </div>
                    {(scheme.min_age || scheme.max_age) && (
                      <div className="scheme-detail-item">
                        <div className="scheme-detail-label">👤 Age Requirement</div>
                        <div className="scheme-detail-value">
                          {scheme.min_age && `Min: ${scheme.min_age} years`}
                          {scheme.min_age && scheme.max_age && ' · '}
                          {scheme.max_age && `Max: ${scheme.max_age} years`}
                        </div>
                      </div>
                    )}
                    {scheme.max_income && (
                      <div className="scheme-detail-item">
                        <div className="scheme-detail-label">💰 Income Limit</div>
                        <div className="scheme-detail-value">Up to ₹{(scheme.max_income / 100000).toFixed(1)}L per year</div>
                      </div>
                    )}
                  </div>
                  <button className="btn btn-primary" style={{ width: '100%', marginTop: '12px' }}>
                    📋 Apply / Learn More
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SchemeFinder;
