import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard, PlusCircle, History, GitCompare,
  Package, FileText, User, ShieldCheck, Package2, LogOut
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/recommend', icon: PlusCircle, label: 'New Recommendation' },
  { to: '/history', icon: History, label: 'History' },
  { to: '/compare', icon: GitCompare, label: 'Compare' },
  { to: '/packaging', icon: Package, label: 'Materials' },
  { to: '/reports', icon: FileText, label: 'Reports' },
  { to: '/profile', icon: User, label: 'Profile' },
];

export default function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const handleLogout = () => { logout(); navigate('/'); };

  return (
    <aside className="hidden lg:flex flex-col w-64 min-h-screen bg-surface-800 border-r border-white/[0.06]">
      {/* Logo */}
      <div className="px-5 py-5 border-b border-white/[0.06]">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-brand-500 to-accent-500 rounded-xl flex items-center justify-center shadow-neon-green">
            <Package2 className="w-5 h-5 text-white" />
          </div>
          <div>
            <p className="font-black text-white text-base leading-tight">
              Pack<span className="text-gradient">Smart AI</span>
            </p>
            <p className="text-[10px] text-gray-500 font-medium">SIH 2026 · MoFPI</p>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
        <p className="text-[10px] font-bold text-gray-600 uppercase tracking-widest px-3 mb-2">Menu</p>
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink key={to} to={to} end={to === '/dashboard'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                isActive
                  ? 'bg-brand-500/15 text-brand-400 border border-brand-500/20 shadow-sm'
                  : 'text-gray-400 hover:bg-white/[0.04] hover:text-gray-200'
              }`
            }>
            {({ isActive }) => (
              <>
                <Icon className={`w-4 h-4 flex-shrink-0 ${isActive ? 'text-brand-400' : ''}`} />
                {label}
              </>
            )}
          </NavLink>
        ))}

        {user?.is_admin && (
          <>
            <p className="text-[10px] font-bold text-gray-600 uppercase tracking-widest px-3 mt-5 mb-2">Admin</p>
            {[
              { to: '/admin', icon: ShieldCheck, label: 'Admin Panel' },
              { to: '/admin/users', icon: User, label: 'Users' },
              { to: '/admin/materials', icon: Package, label: 'Materials' },
            ].map(({ to, icon: Icon, label }) => (
              <NavLink key={to} to={to} end
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                    isActive ? 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20' : 'text-gray-400 hover:bg-white/[0.04] hover:text-gray-200'
                  }`
                }>
                <Icon className="w-4 h-4" />
                {label}
              </NavLink>
            ))}
          </>
        )}
      </nav>

      {/* User footer */}
      <div className="px-4 py-4 border-t border-white/[0.06]">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-gradient-to-br from-brand-500/30 to-accent-500/30 border border-brand-500/30 rounded-full flex items-center justify-center flex-shrink-0">
            <span className="text-brand-400 font-bold text-sm">{user?.full_name?.charAt(0).toUpperCase()}</span>
          </div>
          <div className="min-w-0 flex-1">
            <p className="text-sm font-semibold text-gray-200 truncate">{user?.full_name}</p>
            <p className="text-xs text-gray-500 truncate capitalize">{user?.user_type?.replace('_', ' ')}</p>
          </div>
          <button onClick={handleLogout} className="text-gray-600 hover:text-red-400 transition p-1 rounded-lg hover:bg-red-500/10 flex-shrink-0">
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
}
