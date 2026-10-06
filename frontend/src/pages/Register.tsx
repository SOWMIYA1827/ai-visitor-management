import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { Package2, AlertCircle } from 'lucide-react';
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

  const [form, setForm] = useState({
    full_name: '', email: '', password: '', user_type: 'farmer',
    organization: '', phone_number: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Auto-fill demo data
  useEffect(() => {
    if (isDemo) {
      setForm(f => ({ ...f, full_name: 'Demo User', email: 'demo@packsmart.ai', password: 'Demo@123456', user_type: 'food_processor', organization: 'PackSmart Demo' }));
    }
  }, [isDemo]);

  const set = (k: string) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) =>
    setForm(f => ({ ...f, [k]: e.target.value }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(''); setLoading(true);
    try {
      await authService.register({ ...form, user_type: form.user_type as any });
      await login(form.email, form.password);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Registration failed. Email may already exist.');
    } finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-green-700 flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-lg">
        <div className="text-center mb-8">
          <div className="w-14 h-14 bg-white rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
            <Package2 className="w-8 h-8 text-green-600" />
          </div>
          <h1 className="text-2xl font-bold text-white">Create Your Account</h1>
          <p className="text-blue-200 mt-1">Start getting AI packaging recommendations</p>
        </div>

        <div className="bg-white rounded-2xl shadow-2xl p-8">
          {isDemo && (
            <div className="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg mb-6 text-sm">
              🚀 Demo mode — form pre-filled. Click Register to continue.
            </div>
          )}
          {error && (
            <div className="flex items-center gap-2 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6 text-sm">
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
            <Link to="/login" className="text-green-600 font-medium hover:underline">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
