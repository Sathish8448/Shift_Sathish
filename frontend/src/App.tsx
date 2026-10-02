import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './auth/AuthContext';
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

function HomePage() {
  const { role } = useAuth();
  return role === 'admin' ? <AdminHomePage /> : <UserHomePage />;
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />

          <Route element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
            <Route path="/" element={<Navigate to="/home" replace />} />
            <Route path="/home" element={<HomePage />} />
            <Route path="/schedule" element={<MonthlySchedulePage />} />
            <Route path="/today" element={<TodaySchedulePage />} />
            <Route path="/leaves" element={<LeavesHolidaysPage />} />
            <Route path="/messages" element={<MessagesPage />} />
            <Route path="/profile" element={<ProfilePage />} />
          </Route>

          <Route element={<ProtectedRoute adminOnly><AppLayout /></ProtectedRoute>}>
            <Route path="/admin/update" element={<UpdatePage />} />
            <Route path="/admin/visitors" element={<VisitorsPage />} />
            <Route path="/admin/import" element={<ImportSchedulePage />} />
            <Route path="/admin/users" element={<ManageUsersPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
