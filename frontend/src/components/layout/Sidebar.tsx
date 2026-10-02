import { NavLink } from 'react-router-dom';
import { useAuth } from '../../auth/AuthContext';

const Sidebar = () => {
  const { profile, role, signOut } = useAuth();

  return (
    <aside className="app-sidebar">
      <div className="sidebar-brand">ShiftApp</div>
      <nav className="sidebar-nav">
        <NavLink to="/home" className="nav-link">Home</NavLink>
        <NavLink to="/schedule" className="nav-link">Monthly Schedule</NavLink>
        <NavLink to="/today" className="nav-link">Today Schedule</NavLink>
        <NavLink to="/leaves" className="nav-link">Leaves & Holidays</NavLink>
        <NavLink to="/messages" className="nav-link">Messages</NavLink>
        <NavLink to="/profile" className="nav-link">Profile</NavLink>
        {role === 'admin' && (
          <>
            <div className="nav-divider"></div>
            <NavLink to="/admin/update" className="nav-link">Update Schedule</NavLink>
            <NavLink to="/admin/import" className="nav-link">Import Schedule</NavLink>
            <NavLink to="/admin/users" className="nav-link">Manage Users</NavLink>
            <NavLink to="/admin/visitors" className="nav-link">Visitors</NavLink>
          </>
        )}
      </nav>
      <div className="sidebar-footer">
        <div className="user-profile">
          <div className="user-name">{profile?.full_name}</div>
          <div className="user-role">{role}</div>
        </div>
        <button className="logout-btn-sidebar" onClick={signOut}>Logout</button>
      </div>
    </aside>
  );
};

export default Sidebar;
