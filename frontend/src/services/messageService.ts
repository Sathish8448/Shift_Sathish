import { apiCall } from './api';
import { Message } from '../types';

export const messageService = {
  getMessages: () => apiCall<Message[]>('GET', '/messages'),
  sendMessage: (content: string) => apiCall<Message>('POST', '/messages', { content }),
  deleteMessage: (id: string) => apiCall('DELETE', `/messages/${id}`),
};
