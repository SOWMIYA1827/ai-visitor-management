import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Package2, Menu, X, User, LogOut, LayoutDashboard, Zap } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const handleLogout = () => { logout(); navigate('/'); };

  return (
    <nav className="sticky top-0 z-50 glass border-b border-white/[0.06]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 bg-gradient-to-br from-brand-500 to-accent-500 rounded-xl flex items-center justify-center shadow-neon-green group-hover:scale-105 transition-transform">
              <Package2 className="w-5 h-5 text-white" />
            </div>
            <div className="leading-tight">
              <span className="font-black text-white text-lg">Pack</span>
              <span className="font-black text-gradient text-lg">Smart AI</span>
            </div>
          </Link>

          {/* Desktop */}
          <div className="hidden md:flex items-center gap-1">
            {!isAuthenticated ? (
              <>
                <Link to="/#how-it-works" className="text-sm text-gray-400 hover:text-white px-3 py-2 rounded-lg hover:bg-white/5 transition">How It Works</Link>
                <Link to="/login" className="text-sm text-gray-400 hover:text-white px-3 py-2 rounded-lg hover:bg-white/5 transition">Login</Link>
                <Link to="/register" className="btn-glow text-white text-sm px-4 py-2 rounded-xl font-semibold flex items-center gap-1.5">
                  <Zap className="w-3.5 h-3.5" /> Get Started
                </Link>
              </>
            ) : (
              <>
                <Link to="/dashboard" className="text-sm text-gray-400 hover:text-white px-3 py-2 rounded-lg hover:bg-white/5 transition flex items-center gap-1.5">
                  <LayoutDashboard className="w-3.5 h-3.5" />Dashboard
                </Link>
                <Link to="/recommend" className="text-sm text-gray-400 hover:text-white px-3 py-2 rounded-lg hover:bg-white/5 transition">Recommend</Link>
                {user?.is_admin && (
                  <Link to="/admin" className="text-sm text-yellow-400 hover:text-yellow-300 px-3 py-2 rounded-lg hover:bg-yellow-400/5 transition">Admin</Link>
                )}
                <div className="flex items-center gap-2 pl-3 ml-2 border-l border-white/10">
                  <div className="w-8 h-8 bg-gradient-to-br from-brand-500/30 to-accent-500/30 border border-brand-500/30 rounded-full flex items-center justify-center">
                    <span className="text-brand-400 font-bold text-sm">{user?.full_name?.charAt(0).toUpperCase()}</span>
                  </div>
                  <span className="text-sm font-medium text-gray-300">{user?.full_name?.split(' ')[0]}</span>
                  <button onClick={handleLogout} className="text-gray-500 hover:text-red-400 transition ml-1 p-1 rounded-lg hover:bg-red-500/10">
                    <LogOut className="w-4 h-4" />
                  </button>
                </div>
              </>
            )}
          </div>

          <button className="md:hidden text-gray-400 hover:text-white p-2 rounded-lg hover:bg-white/5" onClick={() => setOpen(!open)}>
            {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {open && (
        <div className="md:hidden glass-lg border-t border-white/[0.06] px-4 py-3 space-y-1">
          {!isAuthenticated ? (
            <>
              <Link to="/login" className="block py-2.5 px-3 text-sm text-gray-300 hover:text-white rounded-lg hover:bg-white/5" onClick={() => setOpen(false)}>Login</Link>
              <Link to="/register" className="block py-2.5 px-3 text-sm text-brand-400 font-semibold rounded-lg hover:bg-brand-500/10" onClick={() => setOpen(false)}>Get Started</Link>
            </>
          ) : (
            <>
              {['/dashboard', '/recommend', '/history', '/compare'].map(path => (
                <Link key={path} to={path} className="block py-2.5 px-3 text-sm text-gray-300 hover:text-white rounded-lg hover:bg-white/5 capitalize" onClick={() => setOpen(false)}>
                  {path.replace('/', '')}
                </Link>
              ))}
              <button onClick={handleLogout} className="block w-full text-left py-2.5 px-3 text-sm text-red-400 hover:text-red-300 rounded-lg hover:bg-red-500/10">Logout</button>
            </>
          )}
        </div>
      )}
    </nav>
  );
}
