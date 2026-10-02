import { useState, useEffect, useCallback } from 'react';
import { Schedule } from '../types';
import { scheduleService } from '../services/scheduleService';

export const useSchedule = (monthYear: string) => {
  const [schedules, setSchedules] = useState<Schedule[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchSchedules = useCallback(async () => {
    try {
      setLoading(true);
      const data = await scheduleService.getSchedulesByMonth(monthYear);
      setSchedules(data);
    } catch (error) {
      console.error('Error fetching schedules:', error);
    } finally {
      setLoading(false);
    }
  }, [monthYear]);

  useEffect(() => {
    if (monthYear) {
      fetchSchedules();
    }
  }, [fetchSchedules]);

  return { schedules, loading, refetch: fetchSchedules };
};
