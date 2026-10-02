import { apiCall } from './api';
import { Shift } from '../types';

export const shiftService = {
  getShifts: () => apiCall<Shift[]>('GET', '/shifts')
};
