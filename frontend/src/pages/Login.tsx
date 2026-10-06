import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Package2, Mail, Lock, AlertCircle, Zap } from 'lucide-react';
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
    e.preventDefault(); setError(''); setLoading(true);
    try { await login(email, password); navigate('/dashboard'); }
    catch { setError('Invalid email or password. Please try again.'); }
    finally { setLoading(false); }
  };

  const handleDemo = async () => {
    setError(''); setLoading(true);
    try { await login('admin@packsmart.ai', 'Admin@123'); navigate('/dashboard'); }
    catch { setError('Demo login failed. Please register first.'); }
    finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen bg-mesh flex items-center justify-center px-4 relative overflow-hidden">
      {/* Orbs */}
      <div className="orb w-96 h-96 bg-brand-500/20 -top-20 -left-20" />
      <div className="orb w-80 h-80 bg-accent-500/15 bottom-0 right-0" />

      <div className="relative w-full max-w-md animate-slide-up">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-gradient-to-br from-brand-500 to-accent-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-neon-green">
            <Package2 className="w-9 h-9 text-white" />
          </div>
          <h1 className="text-3xl font-black text-white">Welcome back</h1>
          <p className="text-gray-500 mt-1">Sign in to PackSmart AI</p>
        </div>

        <div className="glass-lg rounded-3xl p-8 border border-white/10">
          {error && (
            <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-xl mb-6 text-sm">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />{error}
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
            <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-white/10" /></div>
            <div className="relative flex justify-center text-xs text-gray-600 bg-transparent px-2">or</div>
          </div>

          <button onClick={handleDemo} disabled={loading}
            className="w-full glass border border-brand-500/20 text-brand-400 font-semibold py-3 rounded-xl hover:bg-brand-500/10 hover:border-brand-500/40 transition text-sm flex items-center justify-center gap-2">
            <Zap className="w-4 h-4" /> Try Demo (Admin Login)
          </button>

          <p className="text-center text-sm text-gray-500 mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-brand-400 font-semibold hover:text-brand-300 transition">Register free</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
