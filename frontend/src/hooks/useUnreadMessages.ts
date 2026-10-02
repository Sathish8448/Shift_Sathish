import { useState, useEffect } from 'react';
import { supabase } from '../auth/supabaseClient';
import { Message, MessageReadStatus } from '../types';
import { apiCall } from '../services/api';
import { useAuth } from '../auth/AuthContext';

export const useUnreadMessages = () => {
  const [unreadCount, setUnreadCount] = useState(0);
  const { user } = useAuth();

  useEffect(() => {
    if (!user) return;

    const fetchUnread = async () => {
      try {
        const status = await apiCall<MessageReadStatus>('GET', '/messages/read-status');
        const latestMessages = await apiCall<Message[]>('GET', '/messages');
        
        const count = latestMessages.filter(m => 
          new Date(m.created_at) > new Date(status?.last_read_at || 0)
        ).length;
        
        setUnreadCount(count);
      } catch (error) {
        console.error('Error fetching unread messages:', error);
      }
    };

    fetchUnread();

    const channel = supabase
      .channel('public:messages_unread')
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'messages' }, () => {
        setUnreadCount(prev => prev + 1);
      })
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, [user]);

  const markAsRead = async () => {
    try {
      await apiCall('POST', '/messages/read-status');
      setUnreadCount(0);
    } catch (error) {
      console.error('Error marking messages as read:', error);
    }
  };

  return { unreadCount, markAsRead };
};
