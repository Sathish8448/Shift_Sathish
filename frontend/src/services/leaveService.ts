import { apiCall } from './api';
import { PlannedLeave } from '../types';

export const leaveService = {
  getLeaves: () => apiCall<PlannedLeave[]>('GET', '/leaves')
};
