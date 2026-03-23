import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import api from '../api/client';

interface User {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  category?: string;
  age?: number;
  risk_level?: string;
  approval_status?: 'pending' | 'approved' | 'rejected' | 'admin';
  is_admin?: boolean;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<{ status?: string; error?: string }>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);
export const useAuth = () => useContext(AuthContext);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      fetchUser().finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUser = async () => {
    try {
      const { data } = await api.get('/accounts/profile/');
      setUser(data);
    } catch {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      setUser(null);
    }
  };

  const login = async (username: string, password: string) => {
    try {
      const { data } = await api.post('/accounts/login/', { username, password });
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      setUser({ ...data.user, is_admin: data.is_admin });
      return { status: 'approved' };
    } catch (err: any) {
      const errData = err.response?.data;
      // Return status so UI can show pending/rejected screen
      return {
        status: errData?.status || 'error',
        error: errData?.error || 'Login failed.',
      };
    }
  };

  const register = async (username: string, email: string, password: string) => {
    await api.post('/accounts/register/', { username, email, password });
    // Don't log in automatically — registration requires approval
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  };

  const refreshUser = () => fetchUser();

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
};
