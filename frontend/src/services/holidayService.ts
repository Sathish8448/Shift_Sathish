import { apiCall } from './api';
import { PublicHoliday } from '../types';

export const holidayService = {
  getHolidays: () => apiCall<PublicHoliday[]>('GET', '/holidays')
};
