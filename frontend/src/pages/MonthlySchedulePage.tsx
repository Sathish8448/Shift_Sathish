import { useState, useEffect } from 'react';
import { supabase } from '../services/supabase';
import { useAuth } from '../auth/AuthContext';
import { getISTMonthYear, getMonthYearDisplay, getPrevMonth, getNextMonth, formatDateIST } from '../utils/dateUtils';

export default function MonthlySchedulePage() {
  const { user } = useAuth();
  const [monthYear, setMonthYear] = useState(getISTMonthYear());
  const [schedules, setSchedules] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSchedules();
  }, [monthYear]);

  const fetchSchedules = async () => {
    setLoading(true);
    const { data, error } = await supabase
      .from('schedules')
      .select('*, profiles(full_name), shifts(name, start_time, end_time)')
      .eq('month_year', monthYear)
      .order('schedule_date', { ascending: true });
    if (data) setSchedules(data);
    setLoading(false);
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Monthly Schedule</h1>
      <div className="flex items-center gap-4 mb-6">
        <button onClick={() => setMonthYear(getPrevMonth(monthYear))} className="bg-gray-200 px-3 py-1 rounded hover:bg-gray-300">&larr;</button>
        <span className="text-lg font-semibold">{getMonthYearDisplay(monthYear)}</span>
        <button onClick={() => setMonthYear(getNextMonth(monthYear))} className="bg-gray-200 px-3 py-1 rounded hover:bg-gray-300">&rarr;</button>
      </div>
      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : schedules.length === 0 ? (
        <p className="text-gray-500">No schedules found for this month.</p>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-gray-50">
              <tr>
                <th className="p-3 text-sm font-semibold text-gray-600">Date</th>
                <th className="p-3 text-sm font-semibold text-gray-600">Employee</th>
                <th className="p-3 text-sm font-semibold text-gray-600">Shift</th>
                <th className="p-3 text-sm font-semibold text-gray-600">Time</th>
              </tr>
            </thead>
            <tbody>
              {schedules.map(s => (
                <tr key={s.id} className="border-t border-gray-100">
                  <td className="p-3 text-sm">{formatDateIST(s.schedule_date)}</td>
                  <td className="p-3 text-sm font-medium">{s.profiles?.full_name}</td>
                  <td className="p-3 text-sm">{s.shifts?.name}</td>
                  <td className="p-3 text-sm text-gray-500">{s.shifts?.start_time?.slice(0,5)} - {s.shifts?.end_time?.slice(0,5)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
