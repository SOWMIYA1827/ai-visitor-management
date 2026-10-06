import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Package2, Mail, Lock, AlertCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(''); setLoading(true);
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch {
      setError('Invalid email or password. Please try again.');
    } finally { setLoading(false); }
  };

  const handleDemo = async () => {
    setError(''); setLoading(true);
    try {
      await login('admin@packsmart.ai', 'Admin@123');
      navigate('/dashboard');
    } catch {
      setError('Demo login failed. Please register first.');
    } finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-green-700 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-14 h-14 bg-white rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
            <Package2 className="w-8 h-8 text-green-600" />
          </div>
          <h1 className="text-2xl font-bold text-white">Welcome back</h1>
          <p className="text-blue-200 mt-1">Sign in to PackSmart AI</p>
        </div>

        <div className="bg-white rounded-2xl shadow-2xl p-8">
          {error && (
            <div className="flex items-center gap-2 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6 text-sm">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              {error}
            </div>
          )}
          <form onSubmit={handleSubmit} className="space-y-5">
            <Input label="Email Address" type="email" value={email} onChange={e => setEmail(e.target.value)}
              placeholder="you@example.com" icon={<Mail className="w-4 h-4" />} required />
            <Input label="Password" type="password" value={password} onChange={e => setPassword(e.target.value)}
              placeholder="••••••••" icon={<Lock className="w-4 h-4" />} required />
            <Button type="submit" size="lg" loading={loading} className="w-full">Sign In</Button>
          </form>

          <div className="relative my-5">
            <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-gray-200" /></div>
            <div className="relative flex justify-center text-xs text-gray-400 bg-white px-2">or</div>
          </div>

          <button onClick={handleDemo} disabled={loading}
            className="w-full border-2 border-dashed border-green-300 text-green-700 font-medium py-2.5 rounded-lg hover:bg-green-50 transition text-sm">
            🚀 Try Demo (Admin Login)
          </button>

          <p className="text-center text-sm text-gray-500 mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-green-600 font-medium hover:underline">Register free</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
