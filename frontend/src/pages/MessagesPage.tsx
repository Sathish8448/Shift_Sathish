import { useState, useEffect, useRef } from 'react';
import { supabase } from '../services/supabase';
import { useAuth } from '../auth/AuthContext';
import { formatDateTimeIST } from '../utils/dateUtils';

export default function MessagesPage() {
  const { user, role, session } = useAuth();
  const [messages, setMessages] = useState<any[]>([]);
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchMessages();
    markAsRead();

    const channel = supabase
      .channel('public:messages')
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'messages' }, (payload) => {
        supabase.from('messages').select('*, profiles(full_name)').eq('id', payload.new.id).single().then(({ data }) => {
          if (data) setMessages(prev => [...prev, data]);
        });
      })
      .on('postgres_changes', { event: 'DELETE', schema: 'public', table: 'messages' }, (payload) => {
        setMessages(prev => prev.filter(m => m.id !== payload.old.id));
      })
      .subscribe();

    return () => { supabase.removeChannel(channel); };
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchMessages = async () => {
    const { data } = await supabase
      .from('messages')
      .select('*, profiles(full_name)')
      .order('created_at', { ascending: true })
      .limit(200);
    if (data) setMessages(data);
    setLoading(false);
  };

  const markAsRead = async () => {
    if (!user) return;
    await supabase.from('message_read_status').upsert({
      user_id: user.id,
      last_read_at: new Date().toISOString(),
    });
  };

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim() || !user) return;
    await supabase.from('messages').insert({ content: content.trim(), user_id: user.id });
    setContent('');
  };

  const handleDelete = async (id: string) => {
    if (!session) return;
    await fetch('/api/messages/' + id, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${session.access_token}` },
    });
  };

  if (loading) return <p className="text-gray-500 p-4">Loading messages...</p>;

  return (
    <div className="flex flex-col h-[calc(100vh-140px)]">
      <h1 className="text-2xl font-bold mb-4">Messages</h1>
      <div className="flex-1 bg-white rounded-lg shadow p-4 overflow-y-auto space-y-3">
        {messages.length === 0 && <p className="text-gray-400 text-center">No messages yet. Start the conversation!</p>}
        {messages.map(m => {
          const isOwn = m.user_id === user?.id;
          return (
            <div key={m.id} className={`flex ${isOwn ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[75%] px-4 py-2 rounded-lg ${isOwn ? 'bg-gray-800 text-white' : 'bg-gray-100 text-gray-800'}`}>
                {!isOwn && <div className="text-xs font-semibold mb-1 text-gray-500">{m.profiles?.full_name}</div>}
                <div className="text-sm">{m.content}</div>
                <div className={`text-xs mt-1 ${isOwn ? 'text-gray-300' : 'text-gray-400'}`}>
                  {formatDateTimeIST(m.created_at)}
                </div>
                {role === 'admin' && (
                  <button onClick={() => handleDelete(m.id)} className="text-xs text-red-400 hover:text-red-600 mt-1">Delete</button>
                )}
              </div>
            </div>
          );
        })}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSend} className="flex gap-2 mt-3">
        <input
          className="flex-1 border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-gray-800 focus:border-transparent outline-none"
          value={content}
          onChange={e => setContent(e.target.value)}
          placeholder="Type a message..."
        />
        <button type="submit" className="bg-gray-900 text-white px-6 py-3 rounded-lg hover:bg-gray-800 font-medium">Send</button>
      </form>
    </div>
  );
}
