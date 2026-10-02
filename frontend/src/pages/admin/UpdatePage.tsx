import { useState, useEffect } from 'react';
import { supabase } from '../../services/supabase';
import { useAuth } from '../../auth/AuthContext';
import { getISTMonthYear, getMonthYearDisplay, getPrevMonth, getNextMonth, formatDateIST } from '../../utils/dateUtils';

export default function UpdatePage() {
  const { session } = useAuth();
  const [monthYear, setMonthYear] = useState(getISTMonthYear());
  const [schedules, setSchedules] = useState<any[]>([]);
  const [users, setUsers] = useState<any[]>([]);
  const [shifts, setShifts] = useState<any[]>([]);
  const [formData, setFormData] = useState({ schedule_date: '', user_id: '', shift_id: '', notes: '' });
  const [message, setMessage] = useState('');

  useEffect(() => { fetchMetadata(); }, []);
  useEffect(() => { fetchSchedules(); }, [monthYear]);

  const fetchMetadata = async () => {
    const [uRes, sRes] = await Promise.all([
      supabase.from('profiles').select('id, full_name').eq('is_active', true).order('full_name'),
      supabase.from('shifts').select('*').order('display_order'),
    ]);
    if (uRes.data) setUsers(uRes.data);
    if (sRes.data) setShifts(sRes.data);
  };

  const fetchSchedules = async () => {
    const { data } = await supabase
      .from('schedules')
      .select('*, profiles(full_name), shifts(name)')
      .eq('month_year', monthYear)
      .order('schedule_date');
    if (data) setSchedules(data);
  };

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!session) return;
    const res = await fetch('/api/schedules', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${session.access_token}` },
      body: JSON.stringify(formData),
    });
    if (res.ok) {
      setMessage('Schedule added!');
      setFormData({ schedule_date: '', user_id: '', shift_id: '', notes: '' });
      fetchSchedules();
    } else {
      const err = await res.json();
      setMessage('Error: ' + (err.detail || 'Failed'));
    }
  };

  const handleDelete = async (id: string) => {
    if (!session) return;
    await fetch(`/api/schedules/${id}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${session.access_token}` },
    });
    fetchSchedules();
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Update Schedule</h1>
      {message && <div className="bg-blue-50 text-blue-700 p-3 rounded-lg mb-4 text-sm">{message}</div>}

      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <h2 className="text-lg font-semibold mb-4">Add Schedule Entry</h2>
        <form onSubmit={handleAdd} className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Date</label>
            <input type="date" required className="w-full border border-gray-300 p-2 rounded-lg" value={formData.schedule_date} onChange={e => setFormData({...formData, schedule_date: e.target.value})} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Employee</label>
            <select required className="w-full border border-gray-300 p-2 rounded-lg" value={formData.user_id} onChange={e => setFormData({...formData, user_id: e.target.value})}>
              <option value="">Select employee...</option>
              {users.map(u => <option key={u.id} value={u.id}>{u.full_name}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Shift</label>
            <select required className="w-full border border-gray-300 p-2 rounded-lg" value={formData.shift_id} onChange={e => setFormData({...formData, shift_id: e.target.value})}>
              <option value="">Select shift...</option>
              {shifts.map(s => <option key={s.id} value={s.id}>{s.name} ({s.start_time?.slice(0,5)}-{s.end_time?.slice(0,5)})</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Notes (optional)</label>
            <input type="text" className="w-full border border-gray-300 p-2 rounded-lg" value={formData.notes} onChange={e => setFormData({...formData, notes: e.target.value})} />
          </div>
          <div className="md:col-span-2">
            <button type="submit" className="bg-gray-900 text-white px-6 py-2 rounded-lg hover:bg-gray-800">Add Schedule</button>
          </div>
        </form>
      </div>

      <div className="bg-white rounded-lg shadow">
        <div className="p-4 flex items-center gap-4 border-b">
          <button onClick={() => setMonthYear(getPrevMonth(monthYear))} className="bg-gray-200 px-3 py-1 rounded hover:bg-gray-300">&larr;</button>
          <span className="font-semibold">{getMonthYearDisplay(monthYear)}</span>
          <button onClick={() => setMonthYear(getNextMonth(monthYear))} className="bg-gray-200 px-3 py-1 rounded hover:bg-gray-300">&rarr;</button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-gray-50">
              <tr>
                <th className="p-3 text-sm">Date</th>
                <th className="p-3 text-sm">Employee</th>
                <th className="p-3 text-sm">Shift</th>
                <th className="p-3 text-sm">Actions</th>
              </tr>
            </thead>
            <tbody>
              {schedules.length === 0 && <tr><td colSpan={4} className="p-4 text-center text-gray-400">No schedules</td></tr>}
              {schedules.map(s => (
                <tr key={s.id} className="border-t border-gray-100">
                  <td className="p-3 text-sm">{formatDateIST(s.schedule_date)}</td>
                  <td className="p-3 text-sm">{s.profiles?.full_name}</td>
                  <td className="p-3 text-sm">{s.shifts?.name}</td>
                  <td className="p-3"><button onClick={() => handleDelete(s.id)} className="text-red-600 text-sm hover:underline">Delete</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
