import React from 'react';
import { Loader2 } from 'lucide-react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'glass';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  icon?: React.ReactNode;
}

export default function Button({
  variant = 'primary', size = 'md', loading = false,
  icon, children, className = '', disabled, ...props
}: ButtonProps) {
  const base = 'inline-flex items-center justify-center gap-2 font-semibold rounded-xl transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-surface-900 disabled:opacity-40 disabled:cursor-not-allowed select-none';

  const variants: Record<string, string> = {
    primary:   'btn-glow text-white focus:ring-brand-500',
    secondary: 'bg-surface-600 hover:bg-surface-500 text-white border border-white/10 focus:ring-accent-500',
    outline:   'border-2 border-brand-500/50 text-brand-400 hover:bg-brand-500/10 hover:border-brand-400 focus:ring-brand-500',
    ghost:     'text-gray-400 hover:bg-white/5 hover:text-white focus:ring-white/20',
    danger:    'bg-red-600/80 hover:bg-red-500 text-white border border-red-500/50 focus:ring-red-500',
    glass:     'glass text-white hover:bg-white/10 border border-white/10 focus:ring-white/20',
  };

  const sizes: Record<string, string> = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-4 py-2.5 text-sm',
    lg: 'px-6 py-3.5 text-base',
  };

  return (
    <button
      className={`${base} ${variants[variant]} ${sizes[size]} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : icon}
      {children}
    </button>
  );
}
