import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Sidebar from './components/Sidebar';
import './index.css';

const Dashboard    = React.lazy(() => import('./pages/Dashboard'));
const Quiz         = React.lazy(() => import('./pages/Quiz'));
const Chatbot      = React.lazy(() => import('./pages/Chatbot'));
const FinancePlanner = React.lazy(() => import('./pages/FinancePlanner'));
const SchemeFinder = React.lazy(() => import('./pages/SchemeFinder'));
const Streaks      = React.lazy(() => import('./pages/Streaks'));
const Blockchain   = React.lazy(() => import('./pages/Blockchain'));
const Login        = React.lazy(() => import('./pages/Login'));
const Signup       = React.lazy(() => import('./pages/Signup'));
const ProfileSetup = React.lazy(() => import('./pages/ProfileSetup'));
const AdminDashboard = React.lazy(() => import('./pages/AdminDashboard'));

const Loading = () => (
  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh', background: 'var(--bg-primary)' }}>
    <div style={{ textAlign: 'center' }}>
      <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>₳</div>
      <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-primary)' }}>ARTH</div>
      <div style={{ fontSize: '0.8rem', marginTop: '0.5rem', color: 'var(--text-muted)' }}>Loading...</div>
    </div>
  </div>
);

const ProtectedLayout: React.FC = () => {
  const { user, loading } = useAuth();

  if (loading) return <Loading />;
  if (!user) return <Navigate to="/login" replace />;

  // Admins get their own layout
  if (user.is_admin || user.approval_status === 'admin') {
    return (
      <div className="app-layout">
        <Sidebar />
        <main className="main-content">
          <React.Suspense fallback={<Loading />}>
            <Routes>
              <Route path="/"        element={<AdminDashboard />} />
              <Route path="/admin"   element={<AdminDashboard />} />
              <Route path="/quiz"    element={<Quiz />} />
              <Route path="/chatbot" element={<Chatbot />} />
              <Route path="/planner" element={<FinancePlanner />} />
              <Route path="/schemes" element={<SchemeFinder />} />
              <Route path="/streaks" element={<Streaks />} />
              <Route path="/blockchain" element={<Blockchain />} />
              <Route path="*"        element={<Navigate to="/" replace />} />
            </Routes>
          </React.Suspense>
        </main>
      </div>
    );
  }

  // Regular approved users
  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <React.Suspense fallback={<Loading />}>
          <Routes>
            <Route path="/"           element={<Dashboard />} />
            <Route path="/quiz"       element={<Quiz />} />
            <Route path="/chatbot"    element={<Chatbot />} />
            <Route path="/planner"    element={<FinancePlanner />} />
            <Route path="/schemes"    element={<SchemeFinder />} />
            <Route path="/streaks"    element={<Streaks />} />
            <Route path="/blockchain" element={<Blockchain />} />
            <Route path="/profile-setup" element={<ProfileSetup />} />
            <Route path="*"           element={<Navigate to="/" replace />} />
          </Routes>
        </React.Suspense>
      </main>
    </div>
  );
};

const App: React.FC = () => (
  <BrowserRouter>
    <AuthProvider>
      <React.Suspense fallback={<Loading />}>
        <Routes>
          <Route path="/login"  element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/*"      element={<ProtectedLayout />} />
        </Routes>
      </React.Suspense>
    </AuthProvider>
  </BrowserRouter>
);

export default App;
