import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Card, CardBody, CardHeader, CardTitle } from '../components/ui/Card';
import { User, Mail, Phone, Building2, Award } from 'lucide-react';
import { capitalize } from '../utils/helpers';

export default function Profile() {
  const { user } = useAuth();
  if (!user) return null;
  return (
    <div className="max-w-2xl space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">My Profile</h1>
      <Card>
        <CardHeader>
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center text-2xl font-bold text-green-700">
              {user.full_name.charAt(0).toUpperCase()}
            </div>
            <div>
              <p className="text-xl font-bold text-gray-900">{user.full_name}</p>
              <p className="text-sm text-gray-500">{capitalize(user.user_type)}</p>
            </div>
          </div>
        </CardHeader>
        <CardBody className="space-y-4">
          {[
            { icon: Mail, label: 'Email', value: user.email },
            { icon: Building2, label: 'Organization', value: user.organization || '—' },
            { icon: Phone, label: 'Phone', value: user.phone_number || '—' },
            { icon: Award, label: 'Role', value: user.is_admin ? 'Administrator' : capitalize(user.user_type) },
          ].map(({ icon: Icon, label, value }) => (
            <div key={label} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
              <Icon className="w-4 h-4 text-gray-400" />
              <div>
                <p className="text-xs text-gray-400">{label}</p>
                <p className="text-sm font-medium text-gray-800">{value}</p>
              </div>
            </div>
          ))}
        </CardBody>
      </Card>
    </div>
  );
}
