import React, { useState, useRef, useEffect } from 'react';
import api from '../api/client';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const QUICK_PROMPTS = [
  '💰 How do I start investing with ₹5,000/month?',
  '📊 Explain SIP vs lump sum investment',
  '🛡️ What insurance do I really need?',
  '🏠 Should I rent or buy a home?',
  '📈 What is a mutual fund?',
  '🔥 How to build an emergency fund?',
  '💳 How to improve my CIBIL score?',
  '🎯 Explain the 50-30-20 rule',
];

const TypingIndicator = () => (
  <div className="chat-message assistant">
    <div className="chat-avatar">₳</div>
    <div className="chat-bubble typing-bubble">
      <span className="typing-dot" />
      <span className="typing-dot" />
      <span className="typing-dot" />
    </div>
  </div>
);

const ChatbotPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '0',
      role: 'assistant',
      content: "Hi! I'm ARTH, your personal financial advisor 🤖\n\nI can help you with:\n• Investment strategies & mutual funds\n• Tax planning & savings\n• Loans, EMI & credit scores\n• Insurance & risk management\n• Government schemes & benefits\n• Retirement & goal planning\n\nWhat financial question can I help you with today?",
      timestamp: new Date(),
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const sendMessage = async (text: string) => {
    if (!text.trim() || loading) return;
    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text.trim(),
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const { data } = await api.post('/chatbot/message/', { message: text.trim() });
      const botMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response || data.message || 'I encountered an error. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, botMsg]);
    } catch {
      const errMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '❌ Sorry, I\'m having trouble connecting right now. Please check that the backend server is running at localhost:8000.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errMsg]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(input);
  };

  const clearChat = () => {
    setMessages([{
      id: '0',
      role: 'assistant',
      content: "Hi! I'm ARTH. How can I help you with your finances today?",
      timestamp: new Date(),
    }]);
  };

  const formatContent = (content: string) => {
    return content.split('\n').map((line, i) => (
      <React.Fragment key={i}>
        {line}
        {i < content.split('\n').length - 1 && <br />}
      </React.Fragment>
    ));
  };

  return (
    <div className="page-container chatbot-page">
      <div className="chat-layout">
        {/* Header */}
        <div className="chat-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div className="chat-bot-avatar">₳</div>
            <div>
              <div style={{ fontWeight: 700, fontSize: '16px' }}>ARTH Financial Advisor</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--accent-green)', fontSize: '13px' }}>
                <div style={{ width: '7px', height: '7px', borderRadius: '50%', background: 'var(--accent-green)' }} />
                Online • AI-powered
              </div>
            </div>
          </div>
          <button className="btn btn-ghost btn-sm" onClick={clearChat} title="Clear chat">
            🗑️ Clear
          </button>
        </div>

        {/* Quick prompts */}
        {messages.length <= 1 && (
          <div className="quick-prompts">
            <div className="qp-label">Quick Questions:</div>
            <div className="qp-chips">
              {QUICK_PROMPTS.map(prompt => (
                <button key={prompt} className="qp-chip" onClick={() => sendMessage(prompt.replace(/^[^\s]+ /, ''))}>
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Messages */}
        <div className="chat-messages">
          {messages.map(msg => (
            <div key={msg.id} className={`chat-message ${msg.role}`}>
              {msg.role === 'assistant' && <div className="chat-avatar">₳</div>}
              <div className="chat-bubble">
                <div className="chat-content">{formatContent(msg.content)}</div>
                <div className="chat-time">
                  {msg.timestamp.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
              {msg.role === 'user' && <div className="chat-avatar user-avatar">U</div>}
            </div>
          ))}
          {loading && <TypingIndicator />}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <form className="chat-input-form" onSubmit={handleSubmit}>
          <input
            ref={inputRef}
            type="text"
            className="form-input chat-input"
            placeholder="Ask about investing, insurance, taxes, loans..."
            value={input}
            onChange={e => setInput(e.target.value)}
            disabled={loading}
            autoComplete="off"
          />
          <button type="submit" className="btn btn-primary" disabled={!input.trim() || loading}>
            {loading ? '⏳' : '➤'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatbotPage;
