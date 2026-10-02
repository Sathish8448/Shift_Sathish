import { apiCall } from './api';
import { Profile } from '../types';

export const userService = {
  listUsers: () => apiCall<Profile[]>('GET', '/users'),
  createUser: (userData: any) => apiCall<Profile>('POST', '/users', userData),
  updateUser: (id: string, userData: any) => apiCall<Profile>('PUT', `/users/${id}`, userData),
  deactivateUser: (id: string) => apiCall<Profile>('POST', `/users/${id}/deactivate`),
  activateUser: (id: string) => apiCall<Profile>('POST', `/users/${id}/activate`),
  resetPassword: (id: string) => apiCall('POST', `/users/${id}/reset-password`),
};
