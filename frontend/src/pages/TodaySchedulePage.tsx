import { useState, useEffect } from 'react';
import { supabase } from '../services/supabase';
import { getISTDateString, formatFullDateIST, formatDateIST } from '../utils/dateUtils';

export default function TodaySchedulePage() {
  const [selectedDate, setSelectedDate] = useState(getISTDateString());
  const [schedules, setSchedules] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSchedules();
  }, [selectedDate]);

  const fetchSchedules = async () => {
    setLoading(true);
    const { data } = await supabase
      .from('schedules')
      .select('*, profiles(full_name), shifts(name, start_time, end_time)')
      .eq('schedule_date', selectedDate)
      .order('created_at', { ascending: true });
    if (data) setSchedules(data);
    setLoading(false);
  };

  // Group by shift
  const grouped = schedules.reduce((acc: Record<string, any[]>, s) => {
    const shiftName = s.shifts?.name || 'Unassigned';
    if (!acc[shiftName]) acc[shiftName] = [];
    acc[shiftName].push(s);
    return acc;
  }, {});

  const isToday = selectedDate === getISTDateString();

  return (
    <div>
      <h1 className="text-2xl font-bold mb-2">
        {isToday ? "Today's Schedule" : 'Schedule'}
      </h1>
      <p className="text-gray-500 mb-4">{formatFullDateIST(selectedDate)}</p>

      <div className="flex items-center gap-4 mb-6">
        <input
          type="date"
          value={selectedDate}
          onChange={e => setSelectedDate(e.target.value)}
          className="border border-gray-300 rounded-lg p-2"
        />
        {!isToday && (
          <button onClick={() => setSelectedDate(getISTDateString())} className="text-sm text-blue-600 hover:underline">
            Back to Today
          </button>
        )}
      </div>

      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : schedules.length === 0 ? (
        <div className="bg-white p-6 rounded-lg shadow text-center text-gray-500">
          No schedule found for this date.
        </div>
      ) : (
        <div className="space-y-4">
          {Object.entries(grouped).map(([shiftName, employees]) => (
            <div key={shiftName} className="bg-white rounded-lg shadow p-4">
              <h2 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-gray-800 inline-block"></span>
                {shiftName}
                <span className="text-xs text-gray-400 font-normal">
                  ({(employees as any[])[0]?.shifts?.start_time?.slice(0,5)} - {(employees as any[])[0]?.shifts?.end_time?.slice(0,5)})
                </span>
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                {(employees as any[]).map(emp => (
                  <div key={emp.id} className="bg-gray-50 px-3 py-2 rounded text-sm">
                    {emp.profiles?.full_name}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
