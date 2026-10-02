import { apiCall } from './api';
import { VisitorLog } from '../types';

export const visitorService = {
  trackVisit: () => apiCall<VisitorLog>('POST', '/visitors/track'),
  getTodayVisitors: (date: string) => apiCall<VisitorLog[]>('GET', `/visitors/today?date=${encodeURIComponent(date)}`),
  getVisitorStats: (monthYear: string) => apiCall<any>('GET', `/visitors/stats?month_year=${encodeURIComponent(monthYear)}`),
};
