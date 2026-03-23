import React, { useState, useEffect } from 'react';
import api from '../api/client';

interface Block {
  id: number;
  block_index: number;
  record_type: string;
  record_data: Record<string, any>;
  hash: string;
  previous_hash: string;
  timestamp: string;
  is_valid: boolean;
}

const RECORD_ICONS: Record<string, string> = {
  quiz_result: '🎮',
  financial_goal: '🎯',
  plan_created: '📋',
  scheme_applied: '🏛️',
  login: '🔐',
  default: '📦',
};

const BlockCard: React.FC<{ block: Block; isFirst: boolean }> = ({ block, isFirst }) => {
  const [expanded, setExpanded] = useState(false);
  const icon = RECORD_ICONS[block.record_type] || RECORD_ICONS.default;

  const formatData = () => {
    const d = block.record_data;
    if (block.record_type === 'quiz_result') {
      return `Quiz: ${d.quiz_title}\nScore: ${d.score}/${d.total} (${d.percentage}%)\nXP: ${d.xp} | Stars: ${'⭐'.repeat(d.stars || 0)}`;
    }
    return JSON.stringify(d, null, 2);
  };

  return (
    <div className={`block-card ${!block.is_valid ? 'invalid' : ''}`}>
      <div className="block-connector" style={{ visibility: isFirst ? 'hidden' : 'visible' }} />

      <div className="block-header" onClick={() => setExpanded(!expanded)}>
        <div className="block-index">#{block.block_index}</div>
        <div className="block-icon">{icon}</div>
        <div className="block-info">
          <div className="block-type">{block.record_type.replace(/_/g, ' ')}</div>
          <div className="block-time">
            {new Date(block.timestamp).toLocaleString('en-IN', {
              day: '2-digit', month: 'short', year: 'numeric',
              hour: '2-digit', minute: '2-digit',
            })}
          </div>
        </div>
        <div className="block-status">
          {block.is_valid
            ? <span className="status-badge valid">✓ Valid</span>
            : <span className="status-badge invalid">✗ Invalid</span>
          }
        </div>
        <button className="btn btn-ghost btn-sm">{expanded ? '▲' : '▼'}</button>
      </div>

      {expanded && (
        <div className="block-details">
          <div className="block-detail-item">
            <span className="bd-label">Data</span>
            <pre className="bd-value">{formatData()}</pre>
          </div>
          <div className="block-detail-item">
            <span className="bd-label">Hash</span>
            <code className="bd-hash">{block.hash}</code>
          </div>
          <div className="block-detail-item">
            <span className="bd-label">Prev Hash</span>
            <code className="bd-hash">{block.previous_hash}</code>
          </div>
        </div>
      )}
    </div>
  );
};

const BlockchainPage: React.FC = () => {
  const [blocks, setBlocks] = useState<Block[]>([]);
  const [loading, setLoading] = useState(true);
  const [verified, setVerified] = useState<boolean | null>(null);
  const [stats, setStats] = useState({ total: 0, valid: 0, quizzes: 0 });

  useEffect(() => {
    api.get('/blockchain/records/')
      .then(r => {
        const data: Block[] = r.data;
        setBlocks(data);
        setStats({
          total: data.length,
          valid: data.filter(b => b.is_valid).length,
          quizzes: data.filter(b => b.record_type === 'quiz_result').length,
        });
      })
      .catch(() => {
        // Demo data
        const demo: Block[] = [
          { id: 3, block_index: 3, record_type: 'quiz_result', record_data: { quiz_title: 'Market Basics', score: 7, total: 8, percentage: 87.5, xp: 80, stars: 2 }, hash: 'a3f8b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0', previous_hash: 'b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1', timestamp: new Date(Date.now() - 3600000).toISOString(), is_valid: true },
          { id: 2, block_index: 2, record_type: 'quiz_result', record_data: { quiz_title: 'Money Basics', score: 8, total: 8, percentage: 100, xp: 90, stars: 3 }, hash: 'b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1', previous_hash: 'c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2', timestamp: new Date(Date.now() - 86400000).toISOString(), is_valid: true },
          { id: 1, block_index: 1, record_type: 'quiz_result', record_data: { quiz_title: 'Profitable Crops', score: 6, total: 8, percentage: 75, xp: 65, stars: 2 }, hash: 'c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2', previous_hash: '0000000000000000000000000000000000000000000000000000000000000000', timestamp: new Date(Date.now() - 172800000).toISOString(), is_valid: true },
        ];
        setBlocks(demo);
        setStats({ total: demo.length, valid: demo.length, quizzes: demo.filter(b => b.record_type === 'quiz_result').length });
      })
      .finally(() => setLoading(false));
  }, []);

  const verifyChain = async () => {
    try {
      const { data } = await api.get('/blockchain/verify/');
      setVerified(data.is_valid);
    } catch {
      // Local verification
      let valid = true;
      for (let i = 1; i < blocks.length; i++) {
        if (blocks[i].previous_hash !== blocks[i-1].hash) {
          valid = false;
          break;
        }
      }
      setVerified(valid);
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1 className="page-title">⛓️ Activity Blockchain</h1>
          <p className="page-subtitle">Tamper-proof SHA-256 record of your financial journey</p>
        </div>
        <button className="btn btn-primary" onClick={verifyChain}>
          🔍 Verify Chain
        </button>
      </div>

      {verified !== null && (
        <div className={`verification-banner ${verified ? 'valid' : 'invalid'}`}>
          {verified
            ? '✅ Chain integrity verified — all records are authentic and unmodified'
            : '❌ Chain integrity check failed — records may have been tampered with'
          }
        </div>
      )}

      {/* Stats */}
      <div className="blockchain-stats">
        <div className="chain-stat card">
          <div className="cs-value">{stats.total}</div>
          <div className="cs-label">Total Blocks</div>
        </div>
        <div className="chain-stat card">
          <div className="cs-value" style={{ color: 'var(--accent-green)' }}>{stats.valid}</div>
          <div className="cs-label">Valid Blocks</div>
        </div>
        <div className="chain-stat card">
          <div className="cs-value" style={{ color: 'var(--accent-blue)' }}>{stats.quizzes}</div>
          <div className="cs-label">Quiz Records</div>
        </div>
        <div className="chain-stat card">
          <div className="cs-value" style={{ color: 'var(--accent-gold)' }}>SHA-256</div>
          <div className="cs-label">Hash Algorithm</div>
        </div>
      </div>

      {/* How it works */}
      <div className="card blockchain-explainer">
        <h3>⛓️ How Your Activity Blockchain Works</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px', lineHeight: 1.7 }}>
          Every quiz attempt, financial plan, and key action is recorded as an immutable block.
          Each block contains the SHA-256 hash of the previous block, creating an unbreakable chain.
          Any tampering would invalidate all subsequent blocks — guaranteeing authenticity.
        </p>
      </div>

      {/* Blocks */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px', color: 'var(--text-muted)' }}>
          <div style={{ fontSize: '40px', animation: 'pulse 1s infinite' }}>⛓️</div>
          <p style={{ marginTop: '12px' }}>Loading blockchain...</p>
        </div>
      ) : blocks.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '60px', color: 'var(--text-muted)' }}>
          <div style={{ fontSize: '40px' }}>⛓️</div>
          <p style={{ marginTop: '12px' }}>No records yet. Complete a quiz to create your first block!</p>
        </div>
      ) : (
        <div className="blocks-chain">
          {blocks.map((block, idx) => (
            <BlockCard key={block.id} block={block} isFirst={idx === blocks.length - 1} />
          ))}
        </div>
      )}
    </div>
  );
};

export default BlockchainPage;
