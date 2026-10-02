import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../services/supabase';

export default function LoginPage() {
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (phone.length !== 10) {
      setError('Mobile number must be 10 digits');
      return;
    }
    setLoading(true);
    setError('');

    const email = `${phone}@shiftapp.local`;
    const { error: authError } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    setLoading(false);
    if (authError) {
      setError('Invalid mobile number or password');
    } else {
      navigate('/home');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm mx-4">
        <h1 className="text-2xl font-bold mb-1 text-center text-gray-800">ShiftApp</h1>
        <p className="text-gray-500 text-sm text-center mb-6">Sign in to your account</p>
        {error && <div className="bg-red-50 text-red-700 p-3 rounded mb-4 text-sm">{error}</div>}
        <form onSubmit={handleLogin}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">Mobile Number</label>
            <input
              type="text"
              maxLength={10}
              placeholder="Enter 10-digit mobile number"
              className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-gray-800 focus:border-transparent outline-none"
              value={phone}
              onChange={e => setPhone(e.target.value.replace(/\D/g, ''))}
              required
            />
          </div>
          <div className="mb-6 relative">
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              type={showPassword ? 'text' : 'password'}
              placeholder="Enter password"
              className="w-full border border-gray-300 rounded-lg p-3 pr-16 focus:ring-2 focus:ring-gray-800 focus:border-transparent outline-none"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
            <button
              type="button"
              className="absolute right-3 top-9 text-sm text-gray-500 hover:text-gray-800"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? 'Hide' : 'Show'}
            </button>
          </div>
          <button
            type="submit"
            className="w-full bg-gray-900 text-white p-3 rounded-lg hover:bg-gray-800 disabled:opacity-50 font-medium"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
}
