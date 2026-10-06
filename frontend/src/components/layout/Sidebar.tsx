import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard, PlusCircle, History, GitCompare,
  Package, FileText, User, ShieldCheck, Package2
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/recommend', icon: PlusCircle, label: 'New Recommendation' },
  { to: '/history', icon: History, label: 'History' },
  { to: '/compare', icon: GitCompare, label: 'Compare' },
  { to: '/packaging', icon: Package, label: 'Materials' },
  { to: '/reports', icon: FileText, label: 'Reports' },
  { to: '/profile', icon: User, label: 'Profile' },
];

const adminItems = [
  { to: '/admin', icon: ShieldCheck, label: 'Admin Panel' },
];

export default function Sidebar() {
  const { user } = useAuth();

  return (
    <aside className="hidden lg:flex flex-col w-60 min-h-screen bg-white border-r border-gray-200">
      {/* Logo */}
      <div className="px-6 py-5 border-b border-gray-100">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
            <Package2 className="w-5 h-5 text-white" />
          </div>
          <div>
            <p className="font-bold text-gray-900 text-base leading-tight">PackSmart <span className="text-green-600">AI</span></p>
            <p className="text-[10px] text-gray-400 leading-tight">SIH 2026</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink key={to} to={to} end={to === '/dashboard'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive ? 'bg-green-50 text-green-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              }`
            }>
            <Icon className="w-4 h-4 flex-shrink-0" />
            {label}
          </NavLink>
        ))}

        {user?.is_admin && (
          <>
            <div className="pt-4 pb-2 px-3">
              <p className="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Admin</p>
            </div>
            {adminItems.map(({ to, icon: Icon, label }) => (
              <NavLink key={to} to={to}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                    isActive ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`
                }>
                <Icon className="w-4 h-4 flex-shrink-0" />
                {label}
              </NavLink>
            ))}
          </>
        )}
      </nav>

      {/* User badge */}
      <div className="px-4 py-4 border-t border-gray-100">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-green-700 font-bold text-sm">
            {user?.full_name?.charAt(0).toUpperCase()}
          </div>
          <div className="min-w-0">
            <p className="text-sm font-medium text-gray-800 truncate">{user?.full_name}</p>
            <p className="text-xs text-gray-400 truncate capitalize">{user?.user_type?.replace('_', ' ')}</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
