import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { Package2, AlertCircle, Zap } from 'lucide-react';
import { authService } from '../services/auth';
import { useAuth } from '../context/AuthContext';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import Select from '../components/ui/Select';
import { USER_TYPES } from '../utils/constants';

export default function Register() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [params] = useSearchParams();
  const isDemo = params.get('demo') === '1';
  const [form, setForm] = useState({ full_name: '', email: '', password: '', user_type: 'farmer', organization: '', phone_number: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isDemo) setForm(f => ({ ...f, full_name: 'Demo User', email: 'demo@packsmart.ai', password: 'Demo@123456', user_type: 'food_processor', organization: 'PackSmart Demo' }));
  }, [isDemo]);

  const set = (k: string) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) =>
    setForm(f => ({ ...f, [k]: e.target.value }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); setError(''); setLoading(true);
    try {
      await authService.register({ ...form, user_type: form.user_type as any });
      await login(form.email, form.password);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Registration failed. Email may already exist.');
    } finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen bg-mesh flex items-center justify-center px-4 py-10 relative overflow-hidden">
      <div className="orb w-96 h-96 bg-brand-500/15 -top-32 -right-20" />
      <div className="orb w-72 h-72 bg-accent-500/10 bottom-10 -left-20" />

      <div className="relative w-full max-w-lg animate-slide-up">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-gradient-to-br from-brand-500 to-accent-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-neon-green">
            <Package2 className="w-9 h-9 text-white" />
          </div>
          <h1 className="text-3xl font-black text-white">Create Account</h1>
          <p className="text-gray-500 mt-1">Start getting AI packaging recommendations</p>
        </div>

        <div className="glass-lg rounded-3xl p-8 border border-white/10">
          {isDemo && (
            <div className="flex items-center gap-2 bg-brand-500/10 border border-brand-500/20 text-brand-400 px-4 py-3 rounded-xl mb-5 text-sm">
              <Zap className="w-4 h-4" /> Demo mode — form pre-filled. Click Register to continue.
            </div>
          )}
          {error && (
            <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-3 rounded-xl mb-5 text-sm">
              <AlertCircle className="w-4 h-4" />{error}
            </div>
          )}
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input label="Full Name" value={form.full_name} onChange={set('full_name')} placeholder="Your full name" required />
            <Input label="Email Address" type="email" value={form.email} onChange={set('email')} placeholder="you@example.com" required />
            <Input label="Password" type="password" value={form.password} onChange={set('password')} placeholder="Min 8 characters" required />
            <Select label="User Type" value={form.user_type} onChange={set('user_type')} options={USER_TYPES} />
            <Input label="Organization" value={form.organization} onChange={set('organization')} placeholder="Company / Farm / Institute" />
            <Input label="Phone Number" type="tel" value={form.phone_number} onChange={set('phone_number')} placeholder="+91 9999999999" />
            <Button type="submit" size="lg" loading={loading} className="w-full mt-2">Create Account</Button>
          </form>
          <p className="text-center text-sm text-gray-500 mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-brand-400 font-semibold hover:text-brand-300 transition">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
