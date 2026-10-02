import { useAuth } from '../../auth/AuthContext';

const Header = () => {
  const { profile, signOut } = useAuth();
  const isMobile = window.innerWidth <= 768;

  return (
    <header className="app-header">
      <div className="header-brand">ShiftApp</div>
      <div className="header-actions">
        {profile && (
          <div className="user-info">
            <span className="user-name">{profile.full_name}</span>
            <span className={`role-badge role-${profile.role}`}>{profile.role}</span>
          </div>
        )}
        {!isMobile && (
          <button className="logout-btn" onClick={signOut}>Logout</button>
        )}
      </div>
    </header>
  );
};

export default Header;
