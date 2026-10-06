import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Package, Menu, X, User, LogOut, LayoutDashboard } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  const handleLogout = () => { logout(); navigate('/'); };

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
              <Package className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="font-bold text-gray-900 text-lg">PackSmart</span>
              <span className="font-bold text-green-600 text-lg"> AI</span>
            </div>
          </Link>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-6">
            {!isAuthenticated ? (
              <>
                <Link to="/#how-it-works" className="text-sm text-gray-600 hover:text-green-600 transition">How It Works</Link>
                <Link to="/login" className="text-sm text-gray-600 hover:text-green-600 transition">Login</Link>
                <Link to="/register" className="bg-green-600 text-white text-sm px-4 py-2 rounded-lg hover:bg-green-700 transition">Get Started</Link>
              </>
            ) : (
              <>
                <Link to="/dashboard" className="text-sm text-gray-600 hover:text-green-600 transition flex items-center gap-1"><LayoutDashboard className="w-4 h-4" />Dashboard</Link>
                <Link to="/recommend" className="text-sm text-gray-600 hover:text-green-600 transition">New Recommendation</Link>
                {user?.is_admin && <Link to="/admin" className="text-sm text-gray-600 hover:text-green-600 transition">Admin</Link>}
                <div className="flex items-center gap-2 pl-4 border-l border-gray-200">
                  <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                    <User className="w-4 h-4 text-green-700" />
                  </div>
                  <span className="text-sm font-medium text-gray-700">{user?.full_name?.split(' ')[0]}</span>
                  <button onClick={handleLogout} className="text-gray-400 hover:text-red-500 transition ml-1"><LogOut className="w-4 h-4" /></button>
                </div>
              </>
            )}
          </div>

          {/* Mobile toggle */}
          <button className="md:hidden text-gray-600" onClick={() => setOpen(!open)}>
            {open ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="md:hidden bg-white border-t border-gray-100 px-4 py-3 space-y-2">
          {!isAuthenticated ? (
            <>
              <Link to="/login" className="block py-2 text-sm text-gray-700" onClick={() => setOpen(false)}>Login</Link>
              <Link to="/register" className="block py-2 text-sm text-green-600 font-medium" onClick={() => setOpen(false)}>Get Started</Link>
            </>
          ) : (
            <>
              <Link to="/dashboard" className="block py-2 text-sm text-gray-700" onClick={() => setOpen(false)}>Dashboard</Link>
              <Link to="/recommend" className="block py-2 text-sm text-gray-700" onClick={() => setOpen(false)}>New Recommendation</Link>
              <Link to="/history" className="block py-2 text-sm text-gray-700" onClick={() => setOpen(false)}>History</Link>
              {user?.is_admin && <Link to="/admin" className="block py-2 text-sm text-gray-700" onClick={() => setOpen(false)}>Admin</Link>}
              <button onClick={handleLogout} className="block py-2 text-sm text-red-600 w-full text-left">Logout</button>
            </>
          )}
        </div>
      )}
    </nav>
  );
}
