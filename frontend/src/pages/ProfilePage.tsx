import { useState } from 'react';
import { useAuth } from '../auth/AuthContext';
import { supabase } from '../services/supabase';

export default function ProfilePage() {
  const { profile, signOut } = useAuth();
  const [newPassword, setNewPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword.length < 6) {
      setMessage('Password must be at least 6 characters');
      return;
    }
    const { error } = await supabase.auth.updateUser({ password: newPassword });
    if (error) {
      setMessage('Error: ' + error.message);
    } else {
      setMessage('Password updated successfully!');
      setNewPassword('');
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Profile</h1>
      <div className="bg-white rounded-lg shadow p-6 max-w-lg">
        <div className="space-y-4 mb-6">
          <div>
            <label className="text-sm text-gray-500">Full Name</label>
            <p className="text-lg font-medium">{profile?.full_name}</p>
          </div>
          <div>
            <label className="text-sm text-gray-500">Mobile Number</label>
            <p className="text-lg">{profile?.mobile_number}</p>
          </div>
          <div>
            <label className="text-sm text-gray-500">Role</label>
            <p className="text-lg capitalize">{profile?.role}</p>
          </div>
          <div>
            <label className="text-sm text-gray-500">Status</label>
            <p className={`text-lg ${profile?.is_active ? 'text-green-600' : 'text-red-600'}`}>
              {profile?.is_active ? 'Active' : 'Inactive'}
            </p>
          </div>
        </div>

        <hr className="my-6" />

        <h2 className="text-lg font-semibold mb-3">Change Password</h2>
        {message && <div className="bg-blue-50 text-blue-700 p-3 rounded mb-4 text-sm">{message}</div>}
        <form onSubmit={handleChangePassword} className="flex gap-3">
          <input
            type="password"
            placeholder="New password"
            className="flex-1 border border-gray-300 rounded-lg p-2"
            value={newPassword}
            onChange={e => setNewPassword(e.target.value)}
            required
          />
          <button type="submit" className="bg-gray-900 text-white px-4 py-2 rounded-lg hover:bg-gray-800">Update</button>
        </form>

        <hr className="my-6" />
        <button onClick={signOut} className="text-red-600 hover:text-red-800 font-medium">Logout</button>
      </div>
    </div>
  );
}
