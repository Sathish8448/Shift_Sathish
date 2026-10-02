import { apiCall } from './api';
import { Schedule } from '../types';

export const scheduleService = {
  getSchedulesByMonth: (monthYear: string) => 
    apiCall<Schedule[]>('GET', `/schedules?month_year=${encodeURIComponent(monthYear)}`),
    
  getSchedulesByDate: (date: string) => 
    apiCall<Schedule[]>('GET', `/schedules?schedule_date=${encodeURIComponent(date)}`),
    
  getTodaySchedule: (date: string) => 
    apiCall<Schedule>('GET', `/schedules/today?date=${encodeURIComponent(date)}`),
};
