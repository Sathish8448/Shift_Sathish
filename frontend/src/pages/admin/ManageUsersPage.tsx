import { useState, useEffect } from 'react';
import { useAuth } from '../../auth/AuthContext';

export default function ManageUsersPage() {
  const { session } = useAuth();
  const [users, setUsers] = useState<any[]>([]);
  const [newUser, setNewUser] = useState({ mobile_number: '', full_name: '', password: '' });
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => { fetchUsers(); }, []);

  const headers = () => ({
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${session?.access_token}`,
  });

  const fetchUsers = async () => {
    if (!session) return;
    const res = await fetch('/api/users', { headers: headers() });
    if (res.ok) setUsers(await res.json());
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newUser.mobile_number.length !== 10) { setMessage('Phone must be 10 digits.'); return; }
    if (newUser.password.length < 6) { setMessage('Password must be at least 6 characters.'); return; }
    setLoading(true);
    const res = await fetch('/api/users', {
      method: 'POST',
      headers: headers(),
      body: JSON.stringify(newUser),
    });
    setLoading(false);
    if (res.ok) {
      setMessage('User created successfully!');
      setNewUser({ mobile_number: '', full_name: '', password: '' });
      fetchUsers();
    } else {
      const err = await res.json();
      setMessage('Error: ' + (err.detail || 'Failed to create user'));
    }
  };

  const handleToggle = async (id: string, isActive: boolean) => {
    const endpoint = isActive ? 'deactivate' : 'activate';
    await fetch(`/api/users/${id}/${endpoint}`, { method: 'PATCH', headers: headers() });
    fetchUsers();
  };

  const handleResetPassword = async (id: string) => {
    const pwd = prompt('Enter new password (min 6 characters):');
    if (!pwd || pwd.length < 6) { alert('Password must be at least 6 characters'); return; }
    const res = await fetch(`/api/users/${id}/reset-password`, {
      method: 'POST',
      headers: headers(),
      body: JSON.stringify({ new_password: pwd }),
    });
    if (res.ok) setMessage('Password reset successful!');
    else setMessage('Error resetting password');
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Manage Users</h1>
      {message && <div className="bg-blue-50 text-blue-700 p-3 rounded-lg mb-4 text-sm">{message}</div>}

      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <h2 className="text-lg font-semibold mb-4">Create New User</h2>
        <form onSubmit={handleCreate} className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Mobile Number</label>
            <input type="text" maxLength={10} required className="w-full border border-gray-300 p-2 rounded-lg" placeholder="10 digits" value={newUser.mobile_number} onChange={e => setNewUser({...newUser, mobile_number: e.target.value.replace(/\D/g, '')})} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Full Name</label>
            <input type="text" required className="w-full border border-gray-300 p-2 rounded-lg" value={newUser.full_name} onChange={e => setNewUser({...newUser, full_name: e.target.value})} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input type="password" required className="w-full border border-gray-300 p-2 rounded-lg" value={newUser.password} onChange={e => setNewUser({...newUser, password: e.target.value})} />
          </div>
          <div className="md:col-span-3">
            <button type="submit" disabled={loading} className="bg-gray-900 text-white px-6 py-2 rounded-lg hover:bg-gray-800 disabled:opacity-50">
              {loading ? 'Creating...' : 'Create User'}
            </button>
          </div>
        </form>
      </div>

      <div className="bg-white rounded-lg shadow overflow-x-auto">
        <table className="w-full text-left">
          <thead className="bg-gray-50">
            <tr>
              <th className="p-3 text-sm font-semibold">Name</th>
              <th className="p-3 text-sm font-semibold">Mobile</th>
              <th className="p-3 text-sm font-semibold">Role</th>
              <th className="p-3 text-sm font-semibold">Status</th>
              <th className="p-3 text-sm font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map(u => (
              <tr key={u.id} className="border-t border-gray-100">
                <td className="p-3 text-sm font-medium">{u.full_name}</td>
                <td className="p-3 text-sm">{u.mobile_number}</td>
                <td className="p-3 text-sm capitalize">{u.role}</td>
                <td className="p-3">
                  <span className={`px-2 py-1 text-xs rounded-full ${u.is_active !== false ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {u.is_active !== false ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="p-3 flex gap-3">
                  <button onClick={() => handleToggle(u.id, u.is_active !== false)} className="text-sm text-blue-600 hover:underline">
                    {u.is_active !== false ? 'Deactivate' : 'Activate'}
                  </button>
                  <button onClick={() => handleResetPassword(u.id)} className="text-sm text-gray-600 hover:underline">Reset PW</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
