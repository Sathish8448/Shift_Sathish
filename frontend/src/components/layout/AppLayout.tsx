import { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import { useAuth } from '../../auth/AuthContext';
import Header from './Header';
import Sidebar from './Sidebar';
import MobileNav from './MobileNav';
import './layout.css';

const AppLayout = () => {
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);

  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth <= 768);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="app-layout">
      {isMobile ? (
        <>
          <Header />
          <main className="main-content mobile-content">
            <Outlet />
          </main>
          <MobileNav />
        </>
      ) : (
        <>
          <Sidebar />
          <div className="desktop-wrapper">
            <Header />
            <main className="main-content desktop-content">
              <Outlet />
            </main>
          </div>
        </>
      )}
    </div>
  );
};

export default AppLayout;
