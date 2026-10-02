import os

files = {
    'package.json': """{
  "name": "frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@supabase/supabase-js": "^2.39.0",
    "date-fns": "^3.3.1",
    "date-fns-tz": "^2.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.2.2",
    "vite": "^5.0.8"
  }
}
""",
    'tsconfig.json': """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
""",
    'tsconfig.node.json': """{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true,
    "strict": true
  },
  "include": ["vite.config.ts"]
}
""",
    'vite.config.ts': """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
""",
    'index.html': """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Shift Schedule Management</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
""",
    '.env': """VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_API_URL=http://localhost:8000
""",
    'src/main.tsx': """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './styles/global.css'
import { AuthProvider } from './auth/AuthContext.tsx'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>,
)
""",
    'src/App.tsx': """import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './auth/ProtectedRoute';
import AppLayout from './components/layout/AppLayout';
import LoginPage from './pages/LoginPage';
import AdminHomePage from './pages/AdminHomePage';
import UserHomePage from './pages/UserHomePage';
import MonthlySchedulePage from './pages/MonthlySchedulePage';
import TodaySchedulePage from './pages/TodaySchedulePage';
import LeavesHolidaysPage from './pages/LeavesHolidaysPage';
import MessagesPage from './pages/MessagesPage';
import ProfilePage from './pages/ProfilePage';
import UpdatePage from './pages/admin/UpdatePage';
import VisitorsPage from './pages/admin/VisitorsPage';
import ImportSchedulePage from './pages/admin/ImportSchedulePage';
import ManageUsersPage from './pages/admin/ManageUsersPage';
import { useAuth } from './auth/AuthContext';

function App() {
  const { role } = useAuth();

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        
        <Route element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
          <Route path="/" element={<Navigate to="/home" replace />} />
          <Route path="/home" element={role === 'admin' ? <AdminHomePage /> : <UserHomePage />} />
          <Route path="/schedule" element={<MonthlySchedulePage />} />
          <Route path="/today" element={<TodaySchedulePage />} />
          <Route path="/leaves" element={<LeavesHolidaysPage />} />
          <Route path="/messages" element={<MessagesPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          
          <Route path="/admin/*" element={<ProtectedRoute adminOnly><></ProtectedRoute>}>
            <Route path="update" element={<UpdatePage />} />
            <Route path="visitors" element={<VisitorsPage />} />
            <Route path="import" element={<ImportSchedulePage />} />
            <Route path="users" element={<ManageUsersPage />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
""",
    'src/vite-env.d.ts': """/// <reference types="vite/client" />
""",
    'src/styles/global.css': """:root {
  --color-black: #1a1a1a;
  --color-white: #ffffff;
  --color-grey: #666666;
  --color-light-grey: #f0f0f0;
  --color-dark-grey: #333333;
  --color-danger: #dc3545;
  --color-success: #28a745;
  
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--font-family);
  background-color: var(--color-light-grey);
  color: var(--color-black);
  line-height: 1.5;
}

a {
  text-decoration: none;
  color: inherit;
}

button {
  cursor: pointer;
  font-family: inherit;
  border: none;
  outline: none;
}

.btn {
  display: inline-block;
  padding: 10px 16px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  text-align: center;
  transition: background-color 0.2s, color 0.2s;
  min-height: 44px; /* Touch-friendly */
}

.btn-primary {
  background-color: var(--color-black);
  color: var(--color-white);
}

.btn-primary:hover {
  background-color: var(--color-dark-grey);
}

.btn-secondary {
  background-color: var(--color-white);
  color: var(--color-black);
  border: 1px solid var(--color-grey);
}

.btn-secondary:hover {
  background-color: var(--color-light-grey);
}

.btn-danger {
  background-color: var(--color-danger);
  color: var(--color-white);
}

.card {
  background: var(--color-white);
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  margin-bottom: 16px;
}

.input-field {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--color-grey);
  border-radius: 4px;
  margin-bottom: 12px;
  font-size: 16px; /* Prevents iOS zoom */
  min-height: 44px;
}

/* Utilities */
.text-center { text-align: center; }
.mb-1 { margin-bottom: 8px; }
.mb-2 { margin-bottom: 16px; }
.mt-1 { margin-top: 8px; }
.mt-2 { margin-top: 16px; }
.flex { display: flex; }
.flex-col { display: flex; flex-direction: column; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.gap-2 { gap: 16px; }

/* Desktop overrides */
@media (min-width: 768px) {
  /* Tablet up */
}
@media (min-width: 1024px) {
  /* Desktop up */
}
""",
    'src/auth/supabaseClient.ts': """import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || '';
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY || '';

export const supabase = createClient(supabaseUrl, supabaseKey);
""",
    'src/auth/AuthContext.tsx': """import React, { createContext, useContext, useEffect, useState } from 'react';
import { Session, User } from '@supabase/supabase-js';
import { supabase } from './supabaseClient';
import { Profile } from '../types';

interface AuthContextType {
  session: Session | null;
  user: User | null;
  profile: Profile | null;
  role: 'admin' | 'user' | null;
  loading: boolean;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [session, setSession] = useState<Session | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setUser(session?.user ?? null);
      if (session?.user) {
        fetchProfile(session.user.id);
      } else {
        setLoading(false);
      }
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      setUser(session?.user ?? null);
      if (session?.user) {
        fetchProfile(session.user.id);
      } else {
        setProfile(null);
        setLoading(false);
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  const fetchProfile = async (userId: string) => {
    try {
      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', userId)
        .single();
        
      if (!error && data) {
        setProfile(data);
        
        // Track visitor when profile is loaded
        fetch(`${import.meta.env.VITE_API_URL}/api/visitors/track`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${(await supabase.auth.getSession()).data.session?.access_token}`
          }
        }).catch(err => console.error('Visitor track error', err));
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const signOut = async () => {
    await supabase.auth.signOut();
  };

  return (
    <AuthContext.Provider value={{ session, user, profile, role: profile?.role ?? null, loading, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
""",
    'src/auth/ProtectedRoute.tsx': """import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from './AuthContext';
import Loading from '../components/common/Loading';

interface ProtectedRouteProps {
  children?: React.ReactNode;
  adminOnly?: boolean;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, adminOnly = false }) => {
  const { user, role, loading } = useAuth();

  if (loading) return <Loading />;

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (adminOnly && role !== 'admin') {
    return <Navigate to="/home" replace />;
  }

  return children ? <>{children}</> : <Outlet />;
};

export default ProtectedRoute;
""",
    'src/types/index.ts': """export interface Profile {
  id: string;
  name: string;
  mobile: string;
  role: 'admin' | 'user';
  is_active: boolean;
  created_at: string;
}

export interface Shift {
  id: number;
  name: string;
  start_time: string;
  end_time: string;
  color_code: string;
}

export interface Schedule {
  id: number;
  user_id: string;
  date: string;
  shift_id: number;
  shift: Shift;
  profile: Profile;
}

export interface Leave {
  id: number;
  user_id: string;
  start_date: string;
  end_date: string;
  reason: string;
  status: string;
  profile?: Profile;
}

export interface Holiday {
  id: number;
  date: string;
  name: string;
}

export interface Message {
  id: number;
  sender_id: string;
  content: string;
  created_at: string;
  sender?: Profile;
}
""",
    'src/services/api.ts': """import { supabase } from '../auth/supabaseClient';

const BASE_URL = import.meta.env.VITE_API_URL || '';

export const apiFetch = async (endpoint: string, options: RequestInit = {}) => {
  const { data: { session } } = await supabase.auth.getSession();
  const token = session?.access_token;
  
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || 'API request failed');
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
};
""",
    'src/services/scheduleService.ts': """import { supabase } from '../auth/supabaseClient';
import { Schedule } from '../types';

export const getSchedulesByDateRange = async (startDate: string, endDate: string): Promise<Schedule[]> => {
  const { data, error } = await supabase
    .from('schedules')
    .select('*, shift:shifts(*), profile:profiles(*)')
    .gte('date', startDate)
    .lte('date', endDate);
    
  if (error) throw error;
  return data as any;
};
""",
    'src/services/messageService.ts': """import { supabase } from '../auth/supabaseClient';

export const getMessages = async (limit = 50) => {
  const { data, error } = await supabase
    .from('messages')
    .select('*, sender:profiles(name)')
    .order('created_at', { ascending: false })
    .limit(limit);
    
  if (error) throw error;
  return data.reverse();
};

export const sendMessage = async (content: string, sender_id: string) => {
  const { error } = await supabase
    .from('messages')
    .insert([{ content, sender_id }]);
  if (error) throw error;
};

export const deleteMessage = async (id: number) => {
  const { error } = await supabase
    .from('messages')
    .delete()
    .eq('id', id);
  if (error) throw error;
};
""",
    'src/services/leaveService.ts': """import { supabase } from '../auth/supabaseClient';

export const getLeaves = async () => {
  const { data, error } = await supabase
    .from('leaves')
    .select('*, profile:profiles(name)')
    .order('start_date', { ascending: true });
    
  if (error) throw error;
  return data;
};
""",
    'src/services/holidayService.ts': """import { supabase } from '../auth/supabaseClient';

export const getHolidays = async () => {
  const { data, error } = await supabase
    .from('holidays')
    .select('*')
    .order('date', { ascending: true });
    
  if (error) throw error;
  return data;
};
""",
    'src/services/userService.ts': """import { apiFetch } from './api';

export const getUsers = () => apiFetch('/api/users');
export const createUser = (data: any) => apiFetch('/api/users', { method: 'POST', body: JSON.stringify(data) });
""",
    'src/services/visitorService.ts': """import { apiFetch } from './api';

export const getVisitors = () => apiFetch('/api/visitors');
""",
    'src/services/shiftService.ts': """import { supabase } from '../auth/supabaseClient';

export const getShifts = async () => {
  const { data, error } = await supabase.from('shifts').select('*');
  if (error) throw error;
  return data;
};
""",
    'src/hooks/useMessages.ts': """import { useState, useEffect } from 'react';
import { supabase } from '../auth/supabaseClient';
import { getMessages } from '../services/messageService';
import { Message } from '../types';

export const useMessages = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  
  useEffect(() => {
    let mounted = true;
    
    getMessages().then(data => {
      if (mounted) setMessages(data as any);
    });

    const channel = supabase
      .channel('public:messages')
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'messages' }, payload => {
        // Fetch full message with profile to append
        supabase.from('messages').select('*, sender:profiles(name)').eq('id', payload.new.id).single().then(({data}) => {
          if (data) {
            setMessages(prev => [...prev, data as any]);
          }
        });
      })
      .on('postgres_changes', { event: 'DELETE', schema: 'public', table: 'messages' }, payload => {
        setMessages(prev => prev.filter(m => m.id !== payload.old.id));
      })
      .subscribe();
      
    return () => {
      mounted = false;
      supabase.removeChannel(channel);
    };
  }, []);

  return { messages };
};
""",
    'src/hooks/useUnreadMessages.ts': """import { useState, useEffect } from 'react';
import { supabase } from '../auth/supabaseClient';
import { useAuth } from '../auth/AuthContext';

export const useUnreadMessages = () => {
  const [hasUnread, setHasUnread] = useState(false);
  const { user } = useAuth();
  
  useEffect(() => {
    if (!user) return;
    
    const checkUnread = async () => {
      const { data: statusData } = await supabase
        .from('message_read_status')
        .select('last_read_at')
        .eq('user_id', user.id)
        .single();
        
      const lastRead = statusData?.last_read_at ? new Date(statusData.last_read_at) : new Date(0);
      
      const { data: latestMsg } = await supabase
        .from('messages')
        .select('created_at')
        .order('created_at', { ascending: false })
        .limit(1)
        .single();
        
      if (latestMsg && new Date(latestMsg.created_at) > lastRead) {
        setHasUnread(true);
      } else {
        setHasUnread(false);
      }
    };
    
    checkUnread();
    
    const channel = supabase
      .channel('public:messages:unread')
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'messages' }, payload => {
        if (payload.new.sender_id !== user.id) {
          setHasUnread(true);
        }
      })
      .subscribe();
      
    return () => { supabase.removeChannel(channel); };
  }, [user]);

  return { hasUnread, setHasUnread };
};
""",
    'src/hooks/useSchedule.ts': """import { useState, useEffect } from 'react';
import { getSchedulesByDateRange } from '../services/scheduleService';
import { Schedule } from '../types';

export const useSchedule = (startDate: string, endDate: string) => {
  const [schedules, setSchedules] = useState<Schedule[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSchedulesByDateRange(startDate, endDate)
      .then(setSchedules)
      .finally(() => setLoading(false));
  }, [startDate, endDate]);

  return { schedules, loading };
};
""",
    'src/utils/dateUtils.ts': """import { format, toZonedTime } from 'date-fns-tz';

const TIMEZONE = 'Asia/Kolkata';

export const getISTDateString = (date = new Date()) => {
  const zonedDate = toZonedTime(date, TIMEZONE);
  return format(zonedDate, 'yyyy-MM-dd', { timeZone: TIMEZONE });
};

export const formatIST = (dateStr: string, formatStr: string) => {
  return format(toZonedTime(new Date(dateStr), TIMEZONE), formatStr, { timeZone: TIMEZONE });
};
""",
    'src/components/common/Loading.tsx': """import React from 'react';
export default function Loading() {
  return <div style={{ padding: 20, textAlign: 'center' }}>Loading...</div>;
}
""",
    'src/components/common/ErrorMessage.tsx': """import React from 'react';
export default function ErrorMessage({ message }: { message: string }) {
  return <div style={{ color: 'var(--color-danger)', padding: 10 }}>{message}</div>;
}
""",
    'src/components/common/ConfirmDialog.tsx': """import React from 'react';
export default function ConfirmDialog({ message, onConfirm, onCancel }: { message: string, onConfirm: () => void, onCancel: () => void }) {
  return (
    <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div className="card">
        <p className="mb-2">{message}</p>
        <div className="flex gap-2">
          <button className="btn btn-secondary" onClick={onCancel}>Cancel</button>
          <button className="btn btn-primary" onClick={onConfirm}>Confirm</button>
        </div>
      </div>
    </div>
  );
}
""",
    'src/components/common/Badge.tsx': """import React from 'react';
export default function Badge({ show }: { show: boolean }) {
  if (!show) return null;
  return <span style={{ display: 'inline-block', width: 8, height: 8, borderRadius: '50%', background: 'var(--color-danger)', marginLeft: 8 }} />;
}
""",
    'src/components/layout/AppLayout.tsx': """import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header';
import Sidebar from './Sidebar';
import MobileNav from './MobileNav';
import './layout.css';

export default function AppLayout() {
  return (
    <div className="layout">
      <Header />
      <div className="layout-body">
        <Sidebar />
        <main className="layout-content">
          <Outlet />
        </main>
      </div>
      <MobileNav />
    </div>
  );
}
""",
    'src/components/layout/layout.css': """.layout { display: flex; flex-direction: column; height: 100vh; }
.layout-body { display: flex; flex: 1; overflow: hidden; }
.layout-content { flex: 1; padding: 16px; overflow-y: auto; padding-bottom: 70px; }
.header { background: var(--color-black); color: white; padding: 16px; display: flex; justify-content: space-between; }
.sidebar { display: none; width: 250px; background: white; padding: 16px; border-right: 1px solid var(--color-grey); }
.mobile-nav { display: flex; position: fixed; bottom: 0; left: 0; right: 0; background: white; border-top: 1px solid var(--color-grey); justify-content: space-around; padding: 10px; z-index: 100; }
@media(min-width: 768px) {
  .sidebar { display: block; }
  .mobile-nav { display: none; }
  .layout-content { padding-bottom: 16px; }
}
""",
    'src/components/layout/Header.tsx': """import React from 'react';
import { useAuth } from '../../auth/AuthContext';
export default function Header() {
  const { profile, signOut } = useAuth();
  return (
    <header className="header">
      <h2>ShiftApp</h2>
      <div>
        <span style={{ marginRight: 16 }}>{profile?.name}</span>
        <button onClick={signOut} style={{ background: 'transparent', color: 'white' }}>Logout</button>
      </div>
    </header>
  );
}
""",
    'src/components/layout/Sidebar.tsx': """import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../../auth/AuthContext';
import { useUnreadMessages } from '../../hooks/useUnreadMessages';
import Badge from '../common/Badge';

export default function Sidebar() {
  const { role } = useAuth();
  const { hasUnread } = useUnreadMessages();

  const getStyle = ({ isActive }: { isActive: boolean }) => ({
    display: 'block', padding: '10px', marginBottom: '5px',
    background: isActive ? 'var(--color-light-grey)' : 'transparent',
    borderRadius: '4px', color: 'var(--color-black)', fontWeight: isActive ? 'bold' as any : 'normal' as any
  });

  return (
    <div className="sidebar">
      <NavLink to="/home" style={getStyle}>Home</NavLink>
      <NavLink to="/schedule" style={getStyle}>Monthly Schedule</NavLink>
      <NavLink to="/today" style={getStyle}>Today Schedule</NavLink>
      <NavLink to="/leaves" style={getStyle}>Leaves & Holidays</NavLink>
      <NavLink to="/messages" style={getStyle}>
        Messages <Badge show={hasUnread} />
      </NavLink>
      <NavLink to="/profile" style={getStyle}>Profile</NavLink>
      {role === 'admin' && (
        <>
          <hr style={{ margin: '10px 0', borderColor: 'var(--color-grey)' }} />
          <NavLink to="/admin/update" style={getStyle}>Update</NavLink>
          <NavLink to="/admin/visitors" style={getStyle}>Visitors</NavLink>
          <NavLink to="/admin/import" style={getStyle}>Import Schedule</NavLink>
          <NavLink to="/admin/users" style={getStyle}>Manage Users</NavLink>
        </>
      )}
    </div>
  );
}
""",
    'src/components/layout/MobileNav.tsx': """import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../../auth/AuthContext';
import { useUnreadMessages } from '../../hooks/useUnreadMessages';
import Badge from '../common/Badge';

export default function MobileNav() {
  const { role } = useAuth();
  const { hasUnread } = useUnreadMessages();
  
  const getStyle = ({ isActive }: { isActive: boolean }) => ({
    display: 'flex', flexDirection: 'column' as any, alignItems: 'center',
    color: isActive ? 'var(--color-black)' : 'var(--color-grey)', fontSize: '12px'
  });

  return (
    <div className="mobile-nav">
      <NavLink to="/home" style={getStyle}><span>🏠</span>Home</NavLink>
      <NavLink to="/today" style={getStyle}><span>📅</span>Today</NavLink>
      <NavLink to="/messages" style={getStyle}>
        <span style={{ position: 'relative' }}>💬 <Badge show={hasUnread} /></span>
        Chat
      </NavLink>
      {role === 'admin' && (
        <NavLink to="/admin/update" style={getStyle}><span>⚙️</span>Admin</NavLink>
      )}
    </div>
  );
}
""",
    'src/pages/LoginPage.tsx': """import React, { useState } from 'react';
import { supabase } from '../auth/supabaseClient';
import { useNavigate } from 'react-router-dom';

export default function LoginPage() {
  const [mobile, setMobile] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const email = `${mobile}@shiftapp.local`;
    
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      setError('Invalid mobile number or password');
      setLoading(false);
    } else {
      navigate('/home');
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', padding: 20 }}>
      <form className="card" onSubmit={handleLogin} style={{ width: '100%', maxWidth: 400 }}>
        <h2 className="text-center mb-2">Login to ShiftApp</h2>
        {error && <div style={{ color: 'red', marginBottom: 10 }}>{error}</div>}
        <input 
          type="text" 
          placeholder="Mobile Number (10 digits)" 
          className="input-field" 
          value={mobile} 
          onChange={e => setMobile(e.target.value)} 
          pattern="\\d{10}"
          required 
        />
        <input 
          type="password" 
          placeholder="Password" 
          className="input-field" 
          value={password} 
          onChange={e => setPassword(e.target.value)} 
          required 
        />
        <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
          {loading ? 'Loading...' : 'Login'}
        </button>
      </form>
    </div>
  );
}
""",
    'src/pages/AdminHomePage.tsx': """import React from 'react';
import { Link } from 'react-router-dom';
export default function AdminHomePage() {
  return (
    <div>
      <h1>Admin Dashboard</h1>
      <div className="flex flex-col gap-2 mt-2">
        <Link to="/today" className="card"><h3>Today's Schedule</h3></Link>
        <Link to="/admin/users" className="card"><h3>Manage Users</h3></Link>
        <Link to="/admin/update" className="card"><h3>Update Schedules</h3></Link>
        <Link to="/messages" className="card"><h3>Messages</h3></Link>
      </div>
    </div>
  );
}
""",
    'src/pages/UserHomePage.tsx': """import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';
export default function UserHomePage() {
  const { profile } = useAuth();
  return (
    <div>
      <h1>Welcome, {profile?.name}</h1>
      <div className="flex flex-col gap-2 mt-2">
        <Link to="/today" className="card"><h3>Today's Schedule</h3></Link>
        <Link to="/schedule" className="card"><h3>My Monthly Schedule</h3></Link>
        <Link to="/messages" className="card"><h3>Messages</h3></Link>
      </div>
    </div>
  );
}
""",
    'src/pages/MonthlySchedulePage.tsx': """import React, { useState } from 'react';
import { useSchedule } from '../hooks/useSchedule';
import { getISTDateString } from '../utils/dateUtils';
import Loading from '../components/common/Loading';

export default function MonthlySchedulePage() {
  const [date] = useState(new Date());
  const start = new Date(date.getFullYear(), date.getMonth(), 1);
  const end = new Date(date.getFullYear(), date.getMonth() + 1, 0);
  
  const { schedules, loading } = useSchedule(getISTDateString(start), getISTDateString(end));

  if (loading) return <Loading />;

  return (
    <div>
      <h2>Monthly Schedule</h2>
      <div className="card mt-2">
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--color-grey)' }}>
                <th style={{ padding: 8 }}>Date</th>
                <th style={{ padding: 8 }}>User</th>
                <th style={{ padding: 8 }}>Shift</th>
              </tr>
            </thead>
            <tbody>
              {schedules.map(s => (
                <tr key={s.id} style={{ borderBottom: '1px solid var(--color-light-grey)' }}>
                  <td style={{ padding: 8 }}>{s.date}</td>
                  <td style={{ padding: 8 }}>{s.profile.name}</td>
                  <td style={{ padding: 8, color: s.shift.color_code }}>{s.shift.name}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
""",
    'src/pages/TodaySchedulePage.tsx': """import React, { useState } from 'react';
import { useSchedule } from '../hooks/useSchedule';
import { getISTDateString } from '../utils/dateUtils';
import Loading from '../components/common/Loading';

export default function TodaySchedulePage() {
  const [dateStr, setDateStr] = useState(getISTDateString(new Date()));
  const { schedules, loading } = useSchedule(dateStr, dateStr);

  return (
    <div>
      <div className="flex justify-between items-center">
        <h2>Schedule for {dateStr}</h2>
        <input 
          type="date" 
          value={dateStr} 
          onChange={(e) => setDateStr(e.target.value)} 
          className="input-field" 
          style={{ width: 'auto', marginBottom: 0 }} 
        />
      </div>
      
      {loading ? <Loading /> : (
        <div className="mt-2">
          {schedules.length === 0 ? (
            <p>No schedules found for this date.</p>
          ) : (
            schedules.map(s => (
              <div key={s.id} className="card" style={{ borderLeft: `5px solid ${s.shift.color_code}` }}>
                <h3>{s.profile.name}</h3>
                <p>{s.shift.name} ({s.shift.start_time} - {s.shift.end_time})</p>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
""",
    'src/pages/LeavesHolidaysPage.tsx': """import React, { useEffect, useState } from 'react';
import { getLeaves } from '../services/leaveService';
import { getHolidays } from '../services/holidayService';
import Loading from '../components/common/Loading';

export default function LeavesHolidaysPage() {
  const [leaves, setLeaves] = useState<any[]>([]);
  const [holidays, setHolidays] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getLeaves(), getHolidays()]).then(([l, h]) => {
      setLeaves(l);
      setHolidays(h);
      setLoading(false);
    });
  }, []);

  if (loading) return <Loading />;

  return (
    <div>
      <h2>Leaves & Holidays</h2>
      
      <h3 className="mt-2">Planned Leaves</h3>
      <div className="card">
        {leaves.map(l => (
          <div key={l.id} className="mb-1" style={{ borderBottom: '1px solid #eee', paddingBottom: 8 }}>
            <strong>{l.profile.name}</strong>: {l.start_date} to {l.end_date} - {l.reason} ({l.status})
          </div>
        ))}
      </div>

      <h3 className="mt-2">Public Holidays</h3>
      <div className="card">
        {holidays.map(h => (
          <div key={h.id} className="mb-1">
            <strong>{h.date}</strong>: {h.name}
          </div>
        ))}
      </div>
    </div>
  );
}
""",
    'src/pages/MessagesPage.tsx': """import React, { useState, useEffect, useRef } from 'react';
import { useMessages } from '../hooks/useMessages';
import { sendMessage, deleteMessage } from '../services/messageService';
import { useAuth } from '../auth/AuthContext';
import { useUnreadMessages } from '../hooks/useUnreadMessages';
import { supabase } from '../auth/supabaseClient';

export default function MessagesPage() {
  const { messages } = useMessages();
  const { user, role } = useAuth();
  const [content, setContent] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { setHasUnread } = useUnreadMessages();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (user) {
      supabase.from('message_read_status').upsert({ user_id: user.id, last_read_at: new Date().toISOString() }).then();
      setHasUnread(false);
    }
  }, [user, messages, setHasUnread]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim() || !user) return;
    await sendMessage(content, user.id);
    setContent('');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 150px)' }}>
      <h2>Messages</h2>
      <div className="card" style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 10 }}>
        {messages.map(m => (
          <div key={m.id} style={{ alignSelf: m.sender_id === user?.id ? 'flex-end' : 'flex-start', background: 'var(--color-light-grey)', padding: 10, borderRadius: 8, maxWidth: '80%' }}>
            <div style={{ fontSize: '0.8rem', color: 'var(--color-grey)', marginBottom: 4 }}>
              {m.sender?.name} - {new Date(m.created_at).toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata' })}
            </div>
            <div>{m.content}</div>
            {role === 'admin' && (
              <button onClick={() => deleteMessage(m.id)} style={{ fontSize: '0.7rem', color: 'red', marginTop: 4, background: 'none' }}>Delete</button>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSend} className="flex gap-2" style={{ marginTop: 10 }}>
        <input className="input-field" style={{ marginBottom: 0 }} value={content} onChange={e => setContent(e.target.value)} placeholder="Type a message..." />
        <button type="submit" className="btn btn-primary">Send</button>
      </form>
    </div>
  );
}
""",
    'src/pages/ProfilePage.tsx': """import React, { useState } from 'react';
import { useAuth } from '../auth/AuthContext';
import { supabase } from '../auth/supabaseClient';

export default function ProfilePage() {
  const { profile, user } = useAuth();
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    const { error } = await supabase.auth.updateUser({ password });
    if (error) setMsg('Error updating password');
    else setMsg('Password updated successfully');
  };

  return (
    <div>
      <h2>Profile</h2>
      <div className="card mt-2">
        <p><strong>Name:</strong> {profile?.name}</p>
        <p><strong>Mobile:</strong> {profile?.mobile}</p>
        <p><strong>Role:</strong> {profile?.role}</p>
      </div>

      <div className="card mt-2">
        <h3>Change Password</h3>
        {msg && <p className="mb-1" style={{ color: msg.includes('Error') ? 'red' : 'green' }}>{msg}</p>}
        <form onSubmit={handlePasswordChange}>
          <input type="password" placeholder="New Password" value={password} onChange={e => setPassword(e.target.value)} className="input-field" required minLength={6} />
          <button type="submit" className="btn btn-primary">Update Password</button>
        </form>
      </div>
    </div>
  );
}
""",
    'src/pages/admin/UpdatePage.tsx': """import React from 'react';
export default function UpdatePage() {
  return (
    <div>
      <h2>Update Schedule</h2>
      <p className="card mt-2">Schedule editor forms will be here.</p>
    </div>
  );
}
""",
    'src/pages/admin/VisitorsPage.tsx': """import React from 'react';
export default function VisitorsPage() {
  return (
    <div>
      <h2>Visitors Log</h2>
      <p className="card mt-2">Visitor tracking data will go here.</p>
    </div>
  );
}
""",
    'src/pages/admin/ImportSchedulePage.tsx': """import React from 'react';
export default function ImportSchedulePage() {
  return (
    <div>
      <h2>Import Schedule</h2>
      <p className="card mt-2">File upload component here.</p>
    </div>
  );
}
""",
    'src/pages/admin/ManageUsersPage.tsx': """import React from 'react';
export default function ManageUsersPage() {
  return (
    <div>
      <h2>Manage Users</h2>
      <p className="card mt-2">User list and creation form here.</p>
    </div>
  );
}
"""
}

# Write files
for filepath, content in files.items():
    full_path = os.path.join(r"d:\Project\frontend", filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Files generated successfully.")
