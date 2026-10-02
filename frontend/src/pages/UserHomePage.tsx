import { Link } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';

export default function UserHomePage() {
  const { profile } = useAuth();

  const cards = [
    { title: 'Monthly Schedule', link: '/schedule', icon: '📅', desc: 'View your schedule' },
    { title: 'Today Schedule', link: '/today', icon: '📋', desc: 'See today\'s shifts' },
    { title: 'Leaves & Holidays', link: '/leaves', icon: '🏖️', desc: 'View time off' },
    { title: 'Messages', link: '/messages', icon: '💬', desc: 'Group chat' },
    { title: 'Profile', link: '/profile', icon: '👤', desc: 'Your account' },
  ];

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Welcome, {profile?.full_name}</h1>
        <p className="text-gray-500 text-sm">Your Dashboard</p>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {cards.map((card, idx) => (
          <Link key={idx} to={card.link} className="bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow border border-gray-100">
            <div className="text-2xl mb-2">{card.icon}</div>
            <h2 className="font-semibold text-gray-800">{card.title}</h2>
            <p className="text-xs text-gray-500 mt-1">{card.desc}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
