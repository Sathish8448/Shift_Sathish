import { NavLink } from 'react-router-dom';
import { useAuth } from '../../auth/AuthContext';

const MobileNav = () => {
  const { role } = useAuth();

  return (
    <nav className="mobile-nav">
      <NavLink to="/home" className="mobile-nav-item">
        <span className="icon">🏠</span>
        <span className="label">Home</span>
      </NavLink>
      <NavLink to="/schedule" className="mobile-nav-item">
        <span className="icon">📅</span>
        <span className="label">Schedule</span>
      </NavLink>
      <NavLink to="/today" className="mobile-nav-item">
        <span className="icon">📋</span>
        <span className="label">Today</span>
      </NavLink>
      <NavLink to="/messages" className="mobile-nav-item">
        <span className="icon">💬</span>
        <span className="label">Messages</span>
      </NavLink>
      <NavLink to={role === 'admin' ? '/admin/update' : '/leaves'} className="mobile-nav-item">
        <span className="icon">☰</span>
        <span className="label">More</span>
      </NavLink>
    </nav>
  );
};

export default MobileNav;
