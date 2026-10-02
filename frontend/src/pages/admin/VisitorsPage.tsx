import { useState, useEffect } from 'react';
import { useAuth } from '../../auth/AuthContext';

export default function VisitorsPage() {
  const { session } = useAuth();
  const [todayVisitors, setTodayVisitors] = useState<any[]>([]);
  const [stats, setStats] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { fetchData(); }, []);

  const fetchData = async () => {
    if (!session) return;
    const h = { 'Authorization': `Bearer ${session.access_token}` };
    const [tRes, sRes] = await Promise.all([
      fetch('/api/visitors/today', { headers: h }),
      fetch('/api/visitors/stats', { headers: h }),
    ]);
    if (tRes.ok) setTodayVisitors(await tRes.json());
    if (sRes.ok) setStats(await sRes.json());
    setLoading(false);
  };

  if (loading) return <p className="text-gray-500 p-4">Loading...</p>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Visitors</h1>

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">Today's Visitors ({todayVisitors.length})</h2>
        {todayVisitors.length === 0 ? (
          <p className="text-gray-400">No visitors today yet.</p>
        ) : (
          <div className="space-y-2">
            {todayVisitors.map((v, i) => (
              <div key={i} className="flex justify-between items-center bg-gray-50 p-3 rounded">
                <span className="font-medium">{v.profiles?.full_name || 'Unknown'}</span>
                <span className="text-sm text-gray-500">{new Date(v.visited_at).toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata' })}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">All-Time Stats</h2>
        {stats.length === 0 ? (
          <p className="text-gray-400">No visitor data yet.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead className="bg-gray-50">
                <tr>
                  <th className="p-3 text-sm font-semibold">User</th>
                  <th className="p-3 text-sm font-semibold">Total Visits</th>
                </tr>
              </thead>
              <tbody>
                {stats.map((s, i) => (
                  <tr key={i} className="border-t border-gray-100">
                    <td className="p-3 text-sm font-medium">{s.full_name || 'Unknown'}</td>
                    <td className="p-3 text-sm">{s.visits}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
