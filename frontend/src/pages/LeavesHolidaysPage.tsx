import { useState, useEffect } from 'react';
import { supabase } from '../services/supabase';
import { useAuth } from '../auth/AuthContext';
import { formatDateIST } from '../utils/dateUtils';

export default function LeavesHolidaysPage() {
  const { role, session } = useAuth();
  const [tab, setTab] = useState<'leaves' | 'holidays'>('leaves');
  const [leaves, setLeaves] = useState<any[]>([]);
  const [holidays, setHolidays] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { fetchAll(); }, []);

  const fetchAll = async () => {
    setLoading(true);
    const [lRes, hRes] = await Promise.all([
      supabase.from('planned_leaves').select('*, profiles(full_name)').order('leave_date'),
      supabase.from('public_holidays').select('*').order('holiday_date'),
    ]);
    if (lRes.data) setLeaves(lRes.data);
    if (hRes.data) setHolidays(hRes.data);
    setLoading(false);
  };

  const deleteLeave = async (id: string) => {
    if (!session) return;
    await fetch(`/api/leaves/${id}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${session.access_token}` } });
    fetchAll();
  };

  const deleteHoliday = async (id: string) => {
    if (!session) return;
    await fetch(`/api/holidays/${id}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${session.access_token}` } });
    fetchAll();
  };

  if (loading) return <p className="text-gray-500 p-4">Loading...</p>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Leaves & Holidays</h1>
      <div className="flex gap-2 mb-6">
        <button onClick={() => setTab('leaves')} className={`px-4 py-2 rounded-lg font-medium ${tab === 'leaves' ? 'bg-gray-900 text-white' : 'bg-gray-200 text-gray-700'}`}>
          Planned Leaves
        </button>
        <button onClick={() => setTab('holidays')} className={`px-4 py-2 rounded-lg font-medium ${tab === 'holidays' ? 'bg-gray-900 text-white' : 'bg-gray-200 text-gray-700'}`}>
          Public Holidays
        </button>
      </div>

      {tab === 'leaves' && (
        <div className="bg-white rounded-lg shadow overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-gray-50">
              <tr>
                <th className="p-3 text-sm font-semibold text-gray-600">Employee</th>
                <th className="p-3 text-sm font-semibold text-gray-600">Leave Date</th>
                <th className="p-3 text-sm font-semibold text-gray-600">Reason</th>
                {role === 'admin' && <th className="p-3 text-sm font-semibold text-gray-600">Actions</th>}
              </tr>
            </thead>
            <tbody>
              {leaves.length === 0 && <tr><td colSpan={4} className="p-4 text-center text-gray-400">No planned leaves</td></tr>}
              {leaves.map(l => (
                <tr key={l.id} className="border-t border-gray-100">
                  <td className="p-3 text-sm font-medium">{l.profiles?.full_name}</td>
                  <td className="p-3 text-sm">{formatDateIST(l.leave_date)}</td>
                  <td className="p-3 text-sm text-gray-500">{l.reason || '-'}</td>
                  {role === 'admin' && (
                    <td className="p-3"><button onClick={() => deleteLeave(l.id)} className="text-red-600 text-sm hover:underline">Delete</button></td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 'holidays' && (
        <div className="bg-white rounded-lg shadow overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-gray-50">
              <tr>
                <th className="p-3 text-sm font-semibold text-gray-600">Holiday</th>
                <th className="p-3 text-sm font-semibold text-gray-600">Date</th>
                {role === 'admin' && <th className="p-3 text-sm font-semibold text-gray-600">Actions</th>}
              </tr>
            </thead>
            <tbody>
              {holidays.length === 0 && <tr><td colSpan={3} className="p-4 text-center text-gray-400">No holidays</td></tr>}
              {holidays.map(h => (
                <tr key={h.id} className="border-t border-gray-100">
                  <td className="p-3 text-sm font-medium">{h.name}</td>
                  <td className="p-3 text-sm">{formatDateIST(h.holiday_date)}</td>
                  {role === 'admin' && (
                    <td className="p-3"><button onClick={() => deleteHoliday(h.id)} className="text-red-600 text-sm hover:underline">Delete</button></td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
